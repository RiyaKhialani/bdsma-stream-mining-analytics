"""
Big Data Analytics (BDA) Engine.
Implements foundational, high-performance big data stream mining and scalable algorithms:
1. Bloom Filter (O(1) probabilistic set membership with configurable false positive rates)
2. Count-Min Sketch (Sub-linear memory frequency estimation for streaming data)
3. Reservoir Sampling (Vitter's Algorithm R for unbiased sampling of unbounded streams)
4. MinHash & Locality-Sensitive Hashing (LSH) (Sub-quadratic near-duplicate search)
5. MapReduce Batch Framework (Map, Shuffle & Sort, Reduce for review text processing)
"""

import math
import hashlib
import random
from typing import List, Dict, Any, Tuple, Set, Callable
from collections import defaultdict


class BloomFilter:
    """
    Probabilistic data structure for O(1) set membership testing.
    Guarantee: Zero false negatives. Bounded false positive probability p.
    """

    def __init__(self, expected_elements: int = 10000, false_positive_rate: float = 0.01, target_fp_rate: float = None):
        self.n = max(expected_elements, 1)
        self.p = target_fp_rate if target_fp_rate is not None else false_positive_rate
        # Optimal bit array size m = - (n * ln(p)) / (ln(2)^2)
        self.size = int(- (self.n * math.log(self.p)) / (math.log(2) ** 2))
        # Optimal hash functions count k = (m / n) * ln(2)
        self.hash_count = max(1, int((self.size / self.n) * math.log(2)))
        self.bit_array = [0] * self.size
        self.items_added = 0

    @property
    def size_m(self) -> int:
        return self.size

    @property
    def hash_count_k(self) -> int:
        return self.hash_count

    def bits_set_count(self) -> int:
        return sum(self.bit_array)

    def get_occupancy_ratio(self) -> float:
        return sum(self.bit_array) / max(1, self.size)

    def _hashes(self, item: str) -> List[int]:
        """Generates k independent hash positions using salted cryptographic digests."""
        positions = []
        item_bytes = str(item).encode("utf-8")
        # Double hashing technique: h_i(x) = (h1(x) + i * h2(x)) % m
        h1 = int(hashlib.md5(item_bytes).hexdigest(), 16)
        h2 = int(hashlib.sha256(item_bytes).hexdigest(), 16)
        for i in range(self.hash_count):
            pos = (h1 + i * h2) % self.size
            positions.append(pos)
        return positions

    def add(self, item: str) -> None:
        """Inserts an element into the Bloom filter."""
        for pos in self._hashes(item):
            self.bit_array[pos] = 1
        self.items_added += 1

    def contains(self, item: str) -> bool:
        """Queries whether an element is possibly in the set or definitely not."""
        for pos in self._hashes(item):
            if self.bit_array[pos] == 0:
                return False
        return True

    def get_stats(self) -> Dict[str, Any]:
        bits_set = sum(self.bit_array)
        fill_ratio = bits_set / self.size if self.size > 0 else 0
        actual_fp = (1 - math.exp(-self.hash_count * self.items_added / self.size)) ** self.hash_count
        return {
            "bit_array_size": self.size,
            "hash_functions_count": self.hash_count,
            "items_added": self.items_added,
            "bits_set": bits_set,
            "fill_ratio": round(fill_ratio, 4),
            "theoretical_fp_rate": round(actual_fp, 6)
        }


class CountMinSketch:
    """
    Sub-linear memory frequency estimator for high-velocity streaming data.
    Epsilon-delta guarantee: With probability (1 - delta), estimate <= true + epsilon * N.
    """

    def __init__(self, epsilon: float = 0.001, delta: float = 0.01):
        self.epsilon = epsilon
        self.delta = delta
        # Width w = ceil(e / epsilon)
        self.width = int(math.ceil(math.e / epsilon))
        # Depth d = ceil(ln(1 / delta))
        self.depth = int(math.ceil(math.log(1.0 / delta)))
        self.table = [[0] * self.width for _ in range(self.depth)]
        self.total_count = 0
        self._salts = [f"cms_salt_row_{i}".encode("utf-8") for i in range(self.depth)]

    def _hash(self, row: int, item: str) -> int:
        h = hashlib.sha1(item.encode("utf-8") + self._salts[row]).hexdigest()
        return int(h, 16) % self.width

    def update(self, item: str, count: int = 1) -> None:
        """Increments the frequency of an incoming stream item across all d hash rows."""
        for row in range(self.depth):
            col = self._hash(row, item)
            self.table[row][col] += count
        self.total_count += count

    def estimate(self, item: str) -> int:
        """Returns the minimum estimate across all d hash rows (conservative bound)."""
        estimates = [self.table[row][self._hash(row, item)] for row in range(self.depth)]
        return min(estimates)

    def query(self, item: str) -> int:
        """Convenience alias for frequency query."""
        return self.estimate(item)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "table_dimensions": f"{self.depth} rows x {self.width} cols",
            "total_slots": self.depth * self.width,
            "memory_bytes": self.depth * self.width * 4,
            "total_stream_events": self.total_count,
            "epsilon_error_bound": self.epsilon,
            "delta_failure_prob": self.delta
        }


class ReservoirSampler:
    """
    Vitter's Algorithm R for unbiased, uniform random sampling from an infinite stream.
    At any step n, each observed item has exactly k/n probability of being in the reservoir.
    """

    def __init__(self, capacity: int = 100, reservoir_size: int = None):
        self.k = reservoir_size if reservoir_size is not None else capacity
        self.reservoir: List[Any] = []
        self.items_seen = 0

    @property
    def total_seen(self) -> int:
        return self.items_seen

    def feed(self, item: Any) -> None:
        """Feeds one streaming element into the sampler."""
        self.items_seen += 1
        if len(self.reservoir) < self.k:
            self.reservoir.append(item)
        else:
            j = random.randint(0, self.items_seen - 1)
            if j < self.k:
                self.reservoir[j] = item

    def feed_stream(self, items: Any) -> None:
        """Feeds an iterable of items into the reservoir."""
        for it in items:
            self.feed(it)

    def get_sample(self) -> List[Any]:
        return list(self.reservoir)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "reservoir_capacity": self.k,
            "total_stream_items_seen": self.items_seen,
            "current_sample_size": len(self.reservoir),
            "inclusion_probability_per_item": round(min(1.0, self.k / max(1, self.items_seen)), 6)
        }


class MinHashLSH:
    """
    Locality-Sensitive Hashing (LSH) using MinHash permutations for sub-quadratic
    near-duplicate text and specification detection (Jaccard similarity threshold t).
    """

    def __init__(self, num_hashes: int = 128, num_bands: int = 16, threshold: float = 0.5):
        self.m = num_hashes
        self.b = num_bands
        assert self.m % self.b == 0, "Number of hashes must be divisible by bands"
        self.r = self.m // self.b  # Rows per band
        self.threshold = threshold
        self.prime = 2147483647  # 2^31 - 1
        # Random hash coefficients (a * x + b) % prime
        random.seed(42)
        self.a_coeffs = [random.randint(1, self.prime - 1) for _ in range(self.m)]
        self.b_coeffs = [random.randint(0, self.prime - 1) for _ in range(self.m)]
        # Buckets: band_idx -> bucket_hash -> list of item_ids
        self.buckets: List[Dict[str, List[str]]] = [defaultdict(list) for _ in range(self.b)]
        self.signatures: Dict[str, List[int]] = {}

    def _shingle(self, text: str, k: int = 3) -> Set[str]:
        """Converts text into word-level k-shingles."""
        words = text.lower().replace(",", "").replace(".", "").split()
        if len(words) < k:
            return {" ".join(words)}
        return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

    def compute_minhash_signature(self, text: str) -> List[int]:
        """Computes m-dimensional MinHash signature vector."""
        shingles = self._shingle(text)
        shingle_hashes = [int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) for s in shingles]
        
        signature = []
        for i in range(self.m):
            min_val = float('inf')
            a, b = self.a_coeffs[i], self.b_coeffs[i]
            for sh in shingle_hashes:
                val = (a * sh + b) % self.prime
                if val < min_val:
                    min_val = val
            signature.append(min_val)
        return signature

    def index(self, item_id: str, text: str) -> None:
        """Indexes a document into LSH band buckets."""
        sig = self.compute_minhash_signature(text)
        self.signatures[item_id] = sig
        for band_idx in range(self.b):
            band_slice = tuple(sig[band_idx * self.r : (band_idx + 1) * self.r])
            bucket_key = hashlib.md5(str(band_slice).encode("utf-8")).hexdigest()
            self.buckets[band_idx][bucket_key].append(item_id)

    def query_near_duplicates(self, item_id: str) -> List[Tuple[str, float]]:
        """Finds candidate duplicates using LSH banding and verifies Jaccard similarity."""
        if item_id not in self.signatures:
            return []
        sig_q = self.signatures[item_id]
        candidates = set()
        for band_idx in range(self.b):
            band_slice = tuple(sig_q[band_idx * self.r : (band_idx + 1) * self.r])
            bucket_key = hashlib.md5(str(band_slice).encode("utf-8")).hexdigest()
            for neighbor in self.buckets[band_idx].get(bucket_key, []):
                if neighbor != item_id:
                    candidates.add(neighbor)

        results = []
        for cand in candidates:
            sig_cand = self.signatures[cand]
            # Estimated Jaccard = fraction of matching MinHash indices
            matches = sum(1 for x, y in zip(sig_q, sig_cand) if x == y)
            est_jaccard = matches / self.m
            if est_jaccard >= self.threshold:
                results.append((cand, round(est_jaccard, 4)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results


    def insert(self, item_id: str, text: str) -> None:
        """Alias for index()."""
        self.index(item_id, text)

    def find_all_near_duplicates(self, reviews: List[Dict[str, Any]], threshold: float = 0.45) -> List[Dict[str, Any]]:
        """Finds all pairwise candidate near duplicates across a list of review dictionaries."""
        text_map = {}
        for r in reviews:
            rid = r.get("review_id", "")
            txt = r.get("review_text", "")
            text_map[rid] = txt
            if rid not in self.signatures:
                self.index(rid, txt)

        seen_pairs = set()
        duplicates = []
        for rid in text_map.keys():
            matches = self.query_near_duplicates(rid)
            for other_id, sim in matches:
                if sim >= threshold:
                    pair_key = tuple(sorted([rid, other_id]))
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)
                        duplicates.append({
                            "id_a": pair_key[0],
                            "id_b": pair_key[1],
                            "text_a": text_map.get(pair_key[0], ""),
                            "text_b": text_map.get(pair_key[1], ""),
                            "jaccard_similarity": sim
                        })
        duplicates.sort(key=lambda x: x["jaccard_similarity"], reverse=True)
        return duplicates


class MapReduceBatchProcessor:
    """
    Emulates distributed MapReduce (Map, Shuffle & Sort, Reduce) execution
    for high-throughput parallel review aggregation and term-frequency statistics.
    """

    @classmethod
    def run_word_count(cls, reviews: List[Dict[str, Any]], top_k: int = 15) -> List[Tuple[str, int]]:
        """High-throughput MapReduce word count across review texts."""
        stop_words = {
            "the", "a", "an", "and", "or", "to", "in", "for", "with", "is", "of", "it", "this",
            "my", "on", "was", "very", "so", "that", "i", "not", "have", "but", "are", "from",
            "by", "at", "as", "be", "all", "out", "stars", "star", "review", "reviews", "amazon",
            "https", "http", "www", "com", "image", "ref", "dp", "verified", "purchase"
        }
        import re
        def mapper(review):
            txt = (review.get("review_text", "") + " " + review.get("summary", "")).lower()
            words = re.findall(r"[a-z]{3,}", txt)
            return [(w, 1) for w in words if w not in stop_words and len(w) > 3]

        def reducer(word, counts):
            return sum(counts)

        counts_dict = cls.execute(reviews, mapper, reducer)
        sorted_counts = sorted(counts_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_counts[:top_k]

    @staticmethod
    def map_phase(chunks: List[Any], mapper_func: Callable[[Any], List[Tuple[Any, Any]]]) -> List[Tuple[Any, Any]]:
        """Executes mapper across independent input data partitions."""
        mapped = []
        for chunk in chunks:
            mapped.extend(mapper_func(chunk))
        return mapped

    @staticmethod
    def shuffle_phase(mapped_items: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
        """Groups intermediate key-value pairs by key (Shuffle & Sort)."""
        grouped = defaultdict(list)
        for key, value in mapped_items:
            grouped[key].append(value)
        return dict(grouped)

    @staticmethod
    def reduce_phase(grouped_dict: Dict[Any, List[Any]], reducer_func: Callable[[Any, List[Any]], Any]) -> Dict[Any, Any]:
        """Applies reducer function to each unique key and its aggregated values."""
        reduced = {}
        for key, values in grouped_dict.items():
            reduced[key] = reducer_func(key, values)
        return reduced

    @classmethod
    def execute(cls, dataset: List[Any], mapper: Callable, reducer: Callable) -> Dict[Any, Any]:
        """Runs an end-to-end MapReduce job."""
        mapped = cls.map_phase(dataset, mapper)
        shuffled = cls.shuffle_phase(mapped)
        reduced = cls.reduce_phase(shuffled, reducer)
        return reduced
