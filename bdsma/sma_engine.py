"""
Social Media Analytics (SMA) Engine.
Implements foundational social network analysis, graph algorithms, and opinion mining:
1. Bipartite Social Network Analysis (SNA) (Reviewer-Product bipartite graph & co-review projection)
2. Network Centrality Analytics (Degree, Betweenness, Eigenvector, and PageRank / FraudRank)
3. Louvain Community Detection (Modularity optimization for detecting collusive review rings)
4. Aspect-Based Sentiment Analysis (ABSA) (Fine-grained aspect polarity and complaint extraction)
5. Information Diffusion & Cascade Modeling (Poisson arrival deviation & Independent Cascade Model)
"""

import math
import re
from typing import Dict, List, Any, Tuple, Set
import networkx as nx
from collections import defaultdict


class BipartiteSocialNetwork:
    """
    Constructs and analyzes the e-commerce Bipartite Social Graph G = (U, P, E)
    connecting Reviewers U to Products P, and projects it into a Reviewer Collusion Network.
    """

    def __init__(self):
        self.bipartite_graph = nx.Graph()
        self.co_review_graph = nx.Graph()

    def build_from_reviews(self, reviews: List[Dict[str, Any]]) -> nx.Graph:
        """Ingests raw reviews and populates bipartite reviewer-product edges."""
        self.bipartite_graph.clear()
        
        for r in reviews:
            u_id = r["reviewer_id"]
            p_id = r["asin"]
            rating = float(r.get("rating", 3.0))
            is_verified = bool(r.get("verified_purchase", False))
            
            # Add nodes with bipartite attribute
            self.bipartite_graph.add_node(u_id, bipartite=0, node_type="reviewer", name=r.get("reviewer_name", u_id))
            self.bipartite_graph.add_node(p_id, bipartite=1, node_type="product")
            
            # Add weighted edge
            self.bipartite_graph.add_edge(
                u_id, p_id,
                rating=rating,
                verified=is_verified,
                review_id=r.get("review_id", ""),
                timestamp=r.get("timestamp", "")
            )

        self._project_co_review_network(reviews)
        return self.bipartite_graph

    def build_network(self, reviews: List[Dict[str, Any]]) -> nx.Graph:
        """Alias for build_from_reviews."""
        return self.build_from_reviews(reviews)

    def _project_co_review_network(self, reviews: List[Dict[str, Any]]) -> nx.Graph:
        """
        Projects bipartite graph into Reviewer Co-Review Network.
        An edge exists between reviewer u1 and u2 if they reviewed >= 1 identical product.
        Edge weight = number of shared co-reviewed ASINs.
        """
        self.co_review_graph.clear()
        product_to_reviewers = defaultdict(list)
        for r in reviews:
            product_to_reviewers[r["asin"]].append(r["reviewer_id"])

        for asin, reviewers in product_to_reviewers.items():
            unique_revs = list(set(reviewers))
            for i in range(len(unique_revs)):
                for j in range(i + 1, len(unique_revs)):
                    u1, u2 = unique_revs[i], unique_revs[j]
                    if self.co_review_graph.has_edge(u1, u2):
                        self.co_review_graph[u1][u2]["weight"] += 1
                        self.co_review_graph[u1][u2]["shared_asins"].append(asin)
                    else:
                        self.co_review_graph.add_edge(u1, u2, weight=1, shared_asins=[asin])

        return self.co_review_graph

    def get_summary(self) -> Dict[str, Any]:
        users = [n for n, d in self.bipartite_graph.nodes(data=True) if d.get("bipartite") == 0]
        prods = [n for n, d in self.bipartite_graph.nodes(data=True) if d.get("bipartite") == 1]
        return {
            "bipartite_total_nodes": self.bipartite_graph.number_of_nodes(),
            "bipartite_total_edges": self.bipartite_graph.number_of_edges(),
            "reviewer_nodes_count": len(users),
            "product_nodes_count": len(prods),
            "co_review_edges_count": self.co_review_graph.number_of_edges(),
            "graph_density": round(nx.density(self.bipartite_graph), 4)
        }


def compute_network_centralities(graph: nx.Graph) -> Dict[str, Dict[str, float]]:
    """
    Computes standard SNA centrality indicators:
    - Degree Centrality: Volume of interactions
    - Betweenness Centrality: Bridge nodes connecting disparate subgraphs
    - PageRank (FraudRank/TrustRank): Global structural influence
    """
    if len(graph) == 0:
        return {}

    deg = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph) if len(graph) > 1 else {n: 0.0 for n in graph}
    pagerank = nx.pagerank(graph, weight="weight") if len(graph) > 1 else {n: 1.0 for n in graph}

    centralities = {}
    for node in graph.nodes():
        centralities[node] = {
            "degree_centrality": round(deg.get(node, 0.0), 4),
            "betweenness_centrality": round(betweenness.get(node, 0.0), 4),
            "pagerank_score": round(pagerank.get(node, 0.0), 4)
        }
    return centralities


def detect_louvain_communities(graph: nx.Graph) -> Dict[str, Any]:
    """
    Executes greedy modularity community detection on the Reviewer Co-Review Network
    to uncover tightly knit collusive review rings (astroturfing syndicates).
    """
    if len(graph) == 0:
        return {"communities": [], "modularity": 0.0, "collusion_rings_detected": []}

    try:
        communities_generator = nx.community.greedy_modularity_communities(graph, weight="weight")
        communities = [list(c) for c in communities_generator]
        modularity = nx.community.modularity(graph, communities, weight="weight")
    except Exception:
        communities = [list(c) for c in nx.connected_components(graph)]
        modularity = 0.0

    # Identify suspicious collusion rings (clusters with size >= 3 and high internal edge density)
    collusion_rings = []
    for idx, comm in enumerate(communities):
        if len(comm) >= 3:
            subgraph = graph.subgraph(comm)
            density = nx.density(subgraph)
            if density > 0.5:
                collusion_rings.append({
                    "ring_id": f"RING_{idx+1}",
                    "members": comm,
                    "member_count": len(comm),
                    "subgraph_density": round(density, 3),
                    "risk_assessment": "CRITICAL - High Collusive Co-Review Density"
                })

    return {
        "total_communities_found": len(communities),
        "modularity_score": round(modularity, 4),
        "communities": communities,
        "collusion_rings_detected": collusion_rings
    }


class AspectSentimentAnalyzer:
    """
    Fine-grained Aspect-Based Sentiment Analysis (ABSA).
    Decomposes customer reviews into discrete hardware & quality dimensions.
    """

    ASPECT_LEXICONS = {
        "charging_speed": ["fast", "speed", "quick", "slow", "watt", "wattage", "hypercharge", "turbo", "rate", "negotiat", "charge", "charging", r"\b\d+w\b"],
        "compatibility": ["compatible", "support", "works with", "incompatible", "fail", "pd", "pps", "handshake", "socket", "ram", "motherboard", "bios"],
        "thermals_heating": ["heat", "hot", "overheating", "warm", "burn", "melt", "temperature", "cool", "thermal", "thermals", "throttle", "throttling"],
        "build_durability": ["broke", "durable", "stiff", "cable", "nylon", "solid", "cheap", "plastic", "quality", "material"],
        "safety_fire": ["hazard", "fire", "smoke", "spark", "safe", "dangerous", "shock", "ce fake", "ul"],
        "value_pricing": ["price", "cheap", "expensive", "waste", "money", "worth", "value", "deal", "affordable"],
        "effectiveness_energy": ["energy", "stamina", "fatigue", "tired", "boost", "active", "effective", "result", "vitality", "focus", "performance"],
        "packaging_authenticity": ["packaging", "seal", "sealed", "authentic", "genuine", "original", "bottle", "damaged", "box", "expiry", "condition"],
        "health_safety_tolerance": ["digestive", "stomach", "side effect", "headache", "safe", "nausea", "swallow", "discomfort", "burp"],
        "pc_performance": ["fps", "gaming", "benchmark", "overclock", "render", "clock", "multi-thread", "single-core", "efficiency"]
    }

    POSITIVE_WORDS = {"great", "excellent", "fast", "solid", "durable", "perfect", "good", "love", "reliable", "best", "effective", "active", "energetic", "authentic", "genuine", "sealed", "smooth", "satisfied", "recommend", "healthy"}
    NEGATIVE_WORDS = {"terrible", "fake", "bad", "broke", "slow", "hot", "burn", "melt", "scam", "dangerous", "avoid", "waste", "fail", "throttle", "throttling", "overheat", "overheating", "incompatible", "damaged", "discomfort", "headache", "nausea", "fatigue", "tired", "defective"}

    @classmethod
    def analyze_review(cls, text: str) -> Dict[str, Dict[str, Any]]:
        text_lower = text.lower()
        aspect_results = {}

        for aspect, keywords in cls.ASPECT_LEXICONS.items():
            matches = []
            for kw in keywords:
                if "\\" in kw:
                    if re.search(kw, text_lower):
                        matches.append(kw)
                else:
                    if re.search(r'\b' + re.escape(kw), text_lower):
                        matches.append(kw)
            if matches:
                # Find sentiments near the matched keywords
                pos_count = sum(1 for w in cls.POSITIVE_WORDS if w in text_lower)
                neg_count = sum(1 for w in cls.NEGATIVE_WORDS if w in text_lower)
                
                score = 0.0
                if pos_count > neg_count:
                    score = min(1.0, (pos_count - neg_count) * 0.4)
                elif neg_count > pos_count:
                    score = max(-1.0, (pos_count - neg_count) * 0.4)

                polarity = "POSITIVE" if score > 0.1 else ("NEGATIVE" if score < -0.1 else "NEUTRAL")
                aspect_results[aspect] = {
                    "polarity": polarity,
                    "score": round(score, 2),
                    "trigger_keywords": matches[:3]
                }

        return aspect_results


class InformationDiffusionModel:
    """
    Models review arrival dynamics and viral spread:
    1. Poisson Arrival Rate Model: Flags statistically abnormal review arrival spikes (>3 std dev).
    2. Independent Cascade Model (ICM): Simulates epidemic diffusion of claims across the social network.
    """

    @staticmethod
    def detect_poisson_burst(arrival_counts: List[int], threshold_z_score: float = 3.0) -> List[Dict[str, Any]]:
        """Identifies time windows where review volume deviates from a stationary Poisson process."""
        if not arrival_counts:
            return []
        
        mean_rate = sum(arrival_counts) / len(arrival_counts)
        variance = sum((x - mean_rate) ** 2 for x in arrival_counts) / max(1, len(arrival_counts))
        std_dev = math.sqrt(variance) if variance > 0 else 1.0

        burst_windows = []
        for idx, count in enumerate(arrival_counts):
            z_score = (count - mean_rate) / std_dev
            if z_score >= threshold_z_score:
                burst_windows.append({
                    "window_index": idx,
                    "review_count": count,
                    "baseline_mean": round(mean_rate, 2),
                    "z_score": round(z_score, 2),
                    "verdict": "ABNORMAL_INORGANIC_BURST (Syndicate Campaign Likely)"
                })
        return burst_windows

    @staticmethod
    def simulate_independent_cascade(graph: nx.Graph, seed_nodes: List[str], propagation_prob: float = 0.35, max_steps: int = 5) -> List[Set[str]]:
        """Simulates step-by-step information spread through network edges."""
        if not graph:
            return []
        
        active_nodes = set(seed_nodes)
        newly_active = set(seed_nodes)
        history = [set(active_nodes)]

        for _ in range(max_steps):
            next_active = set()
            for u in newly_active:
                for v in graph.neighbors(u):
                    if v not in active_nodes:
                        weight = graph[u][v].get("weight", 1)
                        effective_prob = min(1.0, propagation_prob * math.log(1 + weight))
                        import random
                        if random.random() < effective_prob:
                            next_active.add(v)
            if not next_active:
                break
            active_nodes.update(next_active)
            newly_active = next_active
            history.append(set(active_nodes))

        return history
