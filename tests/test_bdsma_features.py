"""
Unit and integration test suite for BDSMA (Big Data & Social Media Analytics)
and KGIRS Multimodal Agentic GraphRAG System.
"""

import unittest
from bdsma.real_data_loader import RealEcommerceDataLoader
from bdsma.bda_engine import (
    BloomFilter,
    CountMinSketch,
    ReservoirSampler,
    MinHashLSH,
    MapReduceBatchProcessor
)
from bdsma.sma_engine import (
    BipartiteSocialNetwork,
    compute_network_centralities,
    detect_louvain_communities,
    AspectSentimentAnalyzer,
    InformationDiffusionModel
)
from bdsma.kgirs_engine import (
    HeterogeneousKnowledgeGraph,
    MultiHopCompatibilityReasoner,
    MultimodalVisualGrounder,
    AgenticGraphRAGOrchestrator
)


class TestBDSMAGraphRAG(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = RealEcommerceDataLoader()
        cls.catalog = cls.loader.load_catalog()
        cls.reviews = cls.loader.load_reviews()
        cls.protocols = cls.loader.load_protocol_standards()

    # --- 1. BIG DATA ANALYTICS (BDA) TESTS ---
    def test_bloom_filter_membership(self):
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        asins = [p["asin"] for p in self.catalog]
        for a in asins:
            bf.add(a)

        # Check true positives
        for a in asins:
            self.assertTrue(bf.contains(a), f"Bloom Filter failed to find inserted ASIN: {a}")

        # Check definite non-membership
        self.assertFalse(bf.contains("UNKNOWN_NEVER_INSERTED_ASIN_999"))
        stats = bf.get_stats()
        self.assertGreater(stats["bits_set"], 0)
        self.assertLess(stats["fill_ratio"], 0.8)

    def test_count_min_sketch_streaming_frequency(self):
        cms = CountMinSketch(epsilon=0.005, delta=0.01)
        # Simulate high-velocity review complaint stream
        stream = ["incompatible"] * 50 + ["overheating"] * 25 + ["fake"] * 10
        for token in stream:
            cms.update(token)

        self.assertGreaterEqual(cms.estimate("incompatible"), 50)
        self.assertGreaterEqual(cms.estimate("overheating"), 25)
        self.assertGreaterEqual(cms.estimate("fake"), 10)
        self.assertEqual(cms.estimate("unseen_word"), 0)

    def test_reservoir_sampling(self):
        sampler = ReservoirSampler(capacity=5)
        for i in range(100):
            sampler.feed(f"review_item_{i}")
        sample = sampler.get_sample()
        self.assertEqual(len(sample), 5)
        self.assertEqual(sampler.get_stats()["total_stream_items_seen"], 100)

    def test_minhash_lsh_near_duplicates(self):
        lsh = MinHashLSH(num_hashes=64, num_bands=16, threshold=0.4)
        doc1 = "Changed my life amazing speed fast delivery super turbo charger recommended seller"
        doc2 = "Changed my life amazing speed fast delivery super turbo charger 100% recommended"
        doc3 = "Completely distinct review about camera zoom quality and titanium chassis"

        lsh.index("doc1", doc1)
        lsh.index("doc2", doc2)
        lsh.index("doc3", doc3)

        near_dups = lsh.query_near_duplicates("doc1")
        cand_ids = [cand for cand, score in near_dups]
        self.assertIn("doc2", cand_ids, "LSH failed to detect near-duplicate bot template")
        self.assertNotIn("doc3", cand_ids, "LSH falsely grouped unrelated review")

    def test_mapreduce_term_frequency(self):
        def mapper(review):
            words = review.get("summary", "").lower().split()
            return [(w, 1) for w in words]

        def reducer(word, counts):
            return sum(counts)

        mr_result = MapReduceBatchProcessor.execute(self.reviews, mapper, reducer)
        self.assertIn("fast", mr_result)
        self.assertGreater(mr_result["fast"], 1)

    # --- 2. SOCIAL MEDIA ANALYTICS (SMA) TESTS ---
    def test_bipartite_social_network_and_centrality(self):
        sna = BipartiteSocialNetwork()
        b_graph = sna.build_from_reviews(self.reviews)
        summary = sna.get_summary()

        self.assertGreater(summary["bipartite_total_nodes"], 5)
        self.assertGreater(summary["bipartite_total_edges"], 5)
        self.assertGreater(summary["co_review_edges_count"], 0)

        # Centrality metrics
        centralities = compute_network_centralities(sna.co_review_graph)
        self.assertIn("U_COLLUSION_ALPHA", centralities)
        self.assertGreater(centralities["U_COLLUSION_ALPHA"]["degree_centrality"], 0)

    def test_louvain_collusion_ring_detection(self):
        sna = BipartiteSocialNetwork()
        sna.build_from_reviews(self.reviews)
        communities_result = detect_louvain_communities(sna.co_review_graph)

        self.assertGreater(len(communities_result["communities"]), 0)
        # Check that collusive syndicates were flagged
        rings = communities_result["collusion_rings_detected"]
        self.assertGreaterEqual(len(rings), 1, "Failed to identify collusive review syndicate ring")
        self.assertIn("U_COLLUSION_ALPHA", rings[0]["members"])

    def test_aspect_based_sentiment_analysis(self):
        review_text = "Verified with hardware meter. Negotiates 27W on iPhone 15 Pro, but casing gets very hot and thermals throttle."
        aspects = AspectSentimentAnalyzer.analyze_review(review_text)

        self.assertIn("charging_speed", aspects)
        self.assertIn("thermals_heating", aspects)
        self.assertEqual(aspects["thermals_heating"]["polarity"], "NEGATIVE")

    def test_poisson_arrival_burst_detection(self):
        # 10 weekly windows, with a 210 review inorganic burst in week 4
        arrival_stream = [12, 14, 15, 13, 210, 16, 14, 12, 15, 13]
        bursts = InformationDiffusionModel.detect_poisson_burst(arrival_stream, threshold_z_score=2.5)

        self.assertEqual(len(bursts), 1)
        self.assertEqual(bursts[0]["window_index"], 4)
        self.assertEqual(bursts[0]["review_count"], 210)

    # --- 3. KGIRS MULTIMODAL AGENTIC GRAPHRAG TESTS ---
    def test_heterogeneous_knowledge_graph_construction(self):
        kg = HeterogeneousKnowledgeGraph()
        kg.build_from_catalog(self.catalog, self.protocols)
        metrics = kg.get_graph_metrics()

        self.assertGreater(metrics["total_entities"], 10)
        self.assertGreater(metrics["total_relations"], 15)
        self.assertIn("Hardware_Protocol", metrics["entity_type_breakdown"])

    def test_multi_hop_compatibility_reasoning(self):
        kg = HeterogeneousKnowledgeGraph()
        kg.build_from_catalog(self.catalog, self.protocols)
        reasoner = MultiHopCompatibilityReasoner(kg)

        # Scenario 1: Anker 65W GaN (B08T5QN2TR) + iPhone 15 Pro (B0CHX1W1XY)
        # Valid USB-PD handshake, but negotiated wattage capped at iPhone hardware max of 27W
        res1 = reasoner.evaluate_multi_hop_compatibility("B08T5QN2TR", "B0CHX1W1XY")
        self.assertTrue(res1["compatible"])
        self.assertEqual(res1["negotiated_wattage"], 27, "Failed to calculate 27W iPhone hardware cap")
        self.assertIn("USB_PD_3.0", res1["shared_protocols"])

        # Scenario 2: Cable e-Marker constraint check
        # Anker 65W GaN + Samsung S24 Ultra (45W) with 100W e-Marker cable
        res2 = reasoner.evaluate_multi_hop_compatibility("B08T5QN2TR", "B0CQ2B3X6F", cable_asin="B093GG81W3")
        self.assertTrue(res2["compatible"])
        self.assertEqual(res2["negotiated_wattage"], 45)

        # Scenario 3: Incompatible Protocol (Deceptive charger B09G3F14G8 which only has QC 2.0 with iPhone)
        res3 = reasoner.evaluate_multi_hop_compatibility("B09G3F14G8", "B0CHX1W1XY")
        self.assertFalse(res3["compatible"])
        self.assertEqual(res3["failure_type"], "PROTOCOL_MISMATCH")

    def test_specification_hallucination_detection(self):
        kg = HeterogeneousKnowledgeGraph()
        kg.build_from_catalog(self.catalog, self.protocols)
        reasoner = MultiHopCompatibilityReasoner(kg)

        # Test impossible claim: "120W all phones compatible including iPhone with FDA chip"
        audit = reasoner.detect_specification_hallucination(
            "B09G3F14G8",
            "This charger delivers 120W on iPhone 15 Pro with FDA approved chip"
        )
        self.assertTrue(audit["hallucination_detected"])
        self.assertGreaterEqual(len(audit["violations"]), 2)

    def test_multimodal_visual_grounding(self):
        deceptive_prod = self.loader.get_product_by_asin("B09G3F14G8")
        visual_audit = MultimodalVisualGrounder.audit_visual_spec_alignment(deceptive_prod)
        self.assertEqual(visual_audit["visual_verdict"], "VISUAL MISMATCH DETECTED")
        self.assertGreater(len(visual_audit["discrepancies_detected"]), 0)

    def test_agentic_graphrag_orchestrator(self):
        kg = HeterogeneousKnowledgeGraph()
        kg.build_from_catalog(self.catalog, self.protocols)
        reasoner = MultiHopCompatibilityReasoner(kg)
        visual = MultimodalVisualGrounder()
        agent = AgenticGraphRAGOrchestrator(kg, reasoner, visual)

        res = agent.query(
            user_prompt="Can I fast charge my iPhone 15 Pro with Anker 65W GaN and Baseus cable?",
            source_asin="B08T5QN2TR",
            target_asin="B0CHX1W1XY",
            cable_asin="B093GG81W3"
        )
        self.assertEqual(res["status"], "GROUNDED_SUCCESS")
        self.assertIn("27W", res["grounded_response"])
        self.assertIn("Hop 1", res["grounded_response"])

    def test_live_link_parser_and_dynamic_kg_injection(self):
        from bdsma.live_link_parser import LiveLinkParser
        sample_url = "https://www.amazon.com/dp/B08T5QN2TR"
        parsed = LiveLinkParser.scrape_and_parse(sample_url)
        self.assertEqual(parsed["asin"], "B08T5QN2TR")
        self.assertIn("attributes", parsed)
        self.assertGreaterEqual(parsed["attributes"]["wattage"], 20)

        # Dynamic KG Injection
        kg = HeterogeneousKnowledgeGraph()
        kg.add_single_product(parsed)
        self.assertTrue(kg.kg.has_node("B08T5QN2TR"))
        self.assertIn("MANUFACTURED_BY", [d["relation"] for _, _, d in kg.kg.edges("B08T5QN2TR", data=True)])


if __name__ == "__main__":
    unittest.main()
