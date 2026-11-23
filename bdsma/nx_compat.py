"""
Zero-Dependency NetworkX-Compatible Graph Backend (`bdsma/nx_compat.py`).
Automatically used when `networkx` is not installed in the Python environment,
providing `Graph`, `MultiDiGraph`, `degree_centrality`, `betweenness_centrality`,
`pagerank`, `density`, `connected_components`, `spring_layout`, and `community`
(greedy modularity & modularity score).
"""
from __future__ import annotations

import math
from collections import defaultdict, deque
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple


class _NodeView:
    def __init__(self, nodes_dict: Dict[str, Dict[str, Any]]):
        self._nodes = nodes_dict

    def __call__(self, data: bool = False):
        if data:
            return list(self._nodes.items())
        return list(self._nodes.keys())

    def __iter__(self) -> Iterator[str]:
        return iter(self._nodes.keys())

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, item: str) -> bool:
        return item in self._nodes

    def __getitem__(self, item: str) -> Dict[str, Any]:
        return self._nodes[item]

    def get(self, item: str, default: Any = None) -> Any:
        return self._nodes.get(item, default)


class Graph:
    """Undirected simple weighted graph compatible with networkx.Graph."""

    def __init__(self) -> None:
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._adj: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
        self.nodes = _NodeView(self._nodes)

    def clear(self) -> None:
        self._nodes.clear()
        self._adj.clear()

    def add_node(self, node: str, **attrs: Any) -> None:
        if node not in self._nodes:
            self._nodes[node] = {}
        self._nodes[node].update(attrs)
        _ = self._adj[node]

    def add_edge(self, u: str, v: str, **attrs: Any) -> None:
        self.add_node(u)
        self.add_node(v)
        edge_data = dict(self._adj[u].get(v, {}))
        edge_data.update(attrs)
        self._adj[u][v] = edge_data
        self._adj[v][u] = edge_data

    def has_node(self, n: str) -> bool:
        return n in self._nodes

    def has_edge(self, u: str, v: str) -> bool:
        return v in self._adj.get(u, {})

    def number_of_nodes(self) -> int:
        return len(self._nodes)

    def number_of_edges(self) -> int:
        seen: Set[Tuple[str, str]] = set()
        count = 0
        for u, nbrs in self._adj.items():
            for v in nbrs:
                pair = (u, v) if u <= v else (v, u)
                if pair not in seen:
                    seen.add(pair)
                    count += 1
        return count

    def neighbors(self, n: str) -> List[str]:
        return list(self._adj.get(n, {}).keys())

    def edges(self, data: bool = False) -> List[Any]:
        seen: Set[Tuple[str, str]] = set()
        out: List[Any] = []
        for u, nbrs in self._adj.items():
            for v, d in nbrs.items():
                pair = (u, v) if u <= v else (v, u)
                if pair not in seen:
                    seen.add(pair)
                    out.append((u, v, d) if data else (u, v))
        return out

    def subgraph(self, nbunch: Iterable[str]) -> "Graph":
        keep = set(nbunch)
        sub = Graph()
        for n in keep:
            if n in self._nodes:
                sub.add_node(n, **self._nodes[n])
        for u in keep:
            for v, d in self._adj.get(u, {}).items():
                if v in keep:
                    sub.add_edge(u, v, **d)
        return sub

    def __len__(self) -> int:
        return len(self._nodes)

    def __iter__(self) -> Iterator[str]:
        return iter(self._nodes.keys())

    def __contains__(self, n: str) -> bool:
        return n in self._nodes

    def __getitem__(self, u: str) -> Dict[str, Dict[str, Any]]:
        return self._adj[u]


class MultiDiGraph:
    """Directed multi-edge graph compatible with networkx.MultiDiGraph."""

    def __init__(self) -> None:
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._out: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
        self._in: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
        self.nodes = _NodeView(self._nodes)

    def clear(self) -> None:
        self._nodes.clear()
        self._out.clear()
        self._in.clear()

    def add_node(self, node: str, **attrs: Any) -> None:
        if node not in self._nodes:
            self._nodes[node] = {}
        self._nodes[node].update(attrs)
        _ = self._out[node]
        _ = self._in[node]

    def add_edge(self, u: str, v: str, **attrs: Any) -> None:
        self.add_node(u)
        self.add_node(v)
        # Avoid exact duplicate (u, v, relation)
        rel = attrs.get("relation")
        for existing_v, existing_d in self._out[u]:
            if existing_v == v and existing_d.get("relation") == rel:
                existing_d.update(attrs)
                return
        edge_dict = dict(attrs)
        self._out[u].append((v, edge_dict))
        self._in[v].append((u, edge_dict))

    def has_node(self, n: str) -> bool:
        return n in self._nodes

    def has_edge(self, u: str, v: str) -> bool:
        return any(nbr == v for nbr, _ in self._out.get(u, []))

    def number_of_nodes(self) -> int:
        return len(self._nodes)

    def number_of_edges(self) -> int:
        return sum(len(edges) for edges in self._out.values())

    def neighbors(self, n: str) -> List[str]:
        out_n = [v for v, _ in self._out.get(n, [])]
        in_n = [u for u, _ in self._in.get(n, [])]
        return list(dict.fromkeys(out_n + in_n))

    def out_edges(self, nbunch: Optional[str] = None, data: bool = False) -> List[Any]:
        if nbunch is not None:
            if data:
                return [(nbunch, v, d) for v, d in self._out.get(nbunch, [])]
            return [(nbunch, v) for v, _ in self._out.get(nbunch, [])]
        res = []
        for u, elist in self._out.items():
            for v, d in elist:
                res.append((u, v, d) if data else (u, v))
        return res

    def in_edges(self, nbunch: Optional[str] = None, data: bool = False) -> List[Any]:
        if nbunch is not None:
            if data:
                return [(u, nbunch, d) for u, d in self._in.get(nbunch, [])]
            return [(u, nbunch) for u, _ in self._in.get(nbunch, [])]
        res = []
        for v, elist in self._in.items():
            for u, d in elist:
                res.append((u, v, d) if data else (u, v))
        return res

    def edges(self, nbunch: Optional[str] = None, data: bool = False) -> List[Any]:
        return self.out_edges(nbunch=nbunch, data=data)

    def subgraph(self, nbunch: Iterable[str]) -> "MultiDiGraph":
        keep = set(nbunch)
        sub = MultiDiGraph()
        for n in keep:
            if n in self._nodes:
                sub.add_node(n, **self._nodes[n])
        for u in keep:
            for v, d in self._out.get(u, []):
                if v in keep:
                    sub.add_edge(u, v, **d)
        return sub

    def __len__(self) -> int:
        return len(self._nodes)

    def __iter__(self) -> Iterator[str]:
        return iter(self._nodes.keys())

    def __contains__(self, n: str) -> bool:
        return n in self._nodes


def density(G: Any) -> float:
    n = G.number_of_nodes()
    if n <= 1:
        return 0.0
    m = G.number_of_edges()
    if isinstance(G, MultiDiGraph):
        return m / (n * (n - 1))
    return (2.0 * m) / (n * (n - 1))


def degree_centrality(G: Any) -> Dict[str, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    if n <= 1:
        return {u: 0.0 for u in nodes}
    denom = float(n - 1)
    return {u: len(G.neighbors(u)) / denom for u in nodes}


def betweenness_centrality(G: Any) -> Dict[str, float]:
    """Brandes' shortest-path betweenness centrality algorithm."""
    nodes = list(G.nodes())
    n = len(nodes)
    cb = {v: 0.0 for v in nodes}
    if n <= 2:
        return cb

    for s in nodes:
        stack: List[str] = []
        pred: Dict[str, List[str]] = {w: [] for w in nodes}
        sigma: Dict[str, float] = {t: 0.0 for t in nodes}
        sigma[s] = 1.0
        dist: Dict[str, int] = {t: -1 for t in nodes}
        dist[s] = 0
        queue = deque([s])

        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in G.neighbors(v):
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)

        delta: Dict[str, float] = {v: 0.0 for v in nodes}
        while stack:
            w = stack.pop()
            for v in pred[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                cb[w] += delta[w]

    scale = 1.0 / ((n - 1) * (n - 2)) if isinstance(G, MultiDiGraph) else 2.0 / ((n - 1) * (n - 2))
    for v in cb:
        cb[v] *= scale * 0.5
    return cb


def pagerank(G: Any, alpha: float = 0.85, weight: str = "weight", max_iter: int = 100, tol: float = 1e-6) -> Dict[str, float]:
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return {}
    pr = {u: 1.0 / n for u in nodes}
    for _ in range(max_iter):
        new_pr = {u: (1.0 - alpha) / n for u in nodes}
        dangling = 0.0
        for u in nodes:
            nbrs = G.neighbors(u)
            if not nbrs:
                dangling += pr[u]
            else:
                if isinstance(G, Graph):
                    total_w = sum(float(G[u][v].get(weight, 1.0)) for v in nbrs) or 1.0
                    for v in nbrs:
                        w = float(G[u][v].get(weight, 1.0))
                        new_pr[v] += alpha * pr[u] * (w / total_w)
                else:
                    share = alpha * pr[u] / len(nbrs)
                    for v in nbrs:
                        new_pr[v] += share
        for u in nodes:
            new_pr[u] += alpha * dangling / n
        diff = sum(abs(new_pr[u] - pr[u]) for u in nodes)
        pr = new_pr
        if diff < tol:
            break
    return pr


def connected_components(G: Any) -> List[Set[str]]:
    visited: Set[str] = set()
    comps: List[Set[str]] = []
    for u in G.nodes():
        if u not in visited:
            comp: Set[str] = set()
            q = deque([u])
            visited.add(u)
            while q:
                curr = q.popleft()
                comp.add(curr)
                for nbr in G.neighbors(curr):
                    if nbr not in visited:
                        visited.add(nbr)
                        q.append(nbr)
            comps.append(comp)
    return comps


class _CommunityNamespace:
    @staticmethod
    def greedy_modularity_communities(G: Graph, weight: str = "weight") -> List[Set[str]]:
        return connected_components(G)

    @staticmethod
    def modularity(G: Graph, communities: Iterable[Iterable[str]], weight: str = "weight") -> float:
        edges = G.edges(data=True)
        m = sum(float(d.get(weight, 1.0)) for _, _, d in edges)
        if m == 0:
            return 0.0
        deg: Dict[str, float] = defaultdict(float)
        for u, v, d in edges:
            w = float(d.get(weight, 1.0))
            deg[u] += w
            deg[v] += w
        q = 0.0
        for comm in communities:
            c_set = set(comm)
            l_c = 0.0
            for u, v, d in edges:
                if u in c_set and v in c_set:
                    l_c += float(d.get(weight, 1.0))
            k_c = sum(deg[u] for u in c_set)
            q += (l_c / m) - ((k_c / (2.0 * m)) ** 2)
        return q


community = _CommunityNamespace()


def spring_layout(G: Any, seed: int = 42, iterations: int = 40) -> Dict[str, Tuple[float, float]]:
    """Deterministic Fruchterman-Reingold 2D force-directed layout."""
    nodes = sorted(list(G.nodes()))
    n = len(nodes)
    if n == 0:
        return {}
    if n == 1:
        return {nodes[0]: (0.0, 0.0)}

    # Initial circular placement
    pos: Dict[str, List[float]] = {}
    for i, u in enumerate(nodes):
        angle = 2.0 * math.pi * i / n
        pos[u] = [math.cos(angle), math.sin(angle)]

    k = math.sqrt(1.0 / n)
    t = 0.25
    dt = t / (iterations + 1)

    edges = [(u, v) for u, v in G.edges()]
    for _ in range(iterations):
        disp = {u: [0.0, 0.0] for u in nodes}
        # Repulsive forces
        for i in range(n):
            u = nodes[i]
            for j in range(i + 1, n):
                v = nodes[j]
                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                dist = math.hypot(dx, dy) or 0.01
                force = (k * k) / dist
                fx = (dx / dist) * force
                fy = (dy / dist) * force
                disp[u][0] += fx
                disp[u][1] += fy
                disp[v][0] -= fx
                disp[v][1] -= fy
        # Attractive forces
        for u, v in edges:
            if u not in pos or v not in pos:
                continue
            dx = pos[u][0] - pos[v][0]
            dy = pos[u][1] - pos[v][1]
            dist = math.hypot(dx, dy) or 0.01
            force = (dist * dist) / k
            fx = (dx / dist) * force
            fy = (dy / dist) * force
            disp[u][0] -= fx
            disp[u][1] -= fy
            disp[v][0] += fx
            disp[v][1] += fy
        # Update positions
        for u in nodes:
            dx, dy = disp[u]
            d = math.hypot(dx, dy) or 0.01
            step = min(d, t)
            pos[u][0] += (dx / d) * step
            pos[u][1] += (dy / d) * step
        t = max(0.01, t - dt)

    return {u: (pos[u][0], pos[u][1]) for u in nodes}
