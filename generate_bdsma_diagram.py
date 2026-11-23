"""
Generates high-resolution 300 DPI formal academic diagrams for the BDSMA & KGIRS report:
1. Figure 3.1: High-Level BDSMA & KGIRS Conceptual Architecture Diagram
2. Figure 3.2: Multi-Hop Knowledge Graph Traversal & Constraint Resolution Blueprint
Strictly formal academic monochrome/charcoal, 100% Times New Roman, zero blue.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_bdsma_architecture_diagram(output_path="bdsma_architecture_diagram.png"):
    fig, ax = plt.subplots(figsize=(9.2, 11.6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')
    ax.set_xlim(0, 9.2)
    ax.set_ylim(0, 11.6)

    # 1. Header
    ax.text(
        4.6, 11.25,
        "CONCEPTUAL SYSTEM ARCHITECTURE: BDSMA & KGIRS",
        ha='center', va='center',
        fontsize=12.5, fontweight='bold',
        fontfamily='Times New Roman',
        color='#000000'
    )
    ax.text(
        4.6, 10.98,
        "Unifying Big Data Stream Analytics, Social Media Graph Intelligence, and Multimodal Agentic GraphRAG",
        ha='center', va='center',
        fontsize=9.2, fontstyle='italic',
        fontfamily='Times New Roman',
        color='#333333'
    )
    ax.plot([0.5, 8.7], [10.82, 10.82], color='#000000', lw=1.2)

    def draw_card(x, y, w, h, title, subtitle, bullets, bg_color="#FCFCFC", border_color="#262626"):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.1,
            zorder=2
        )
        ax.add_patch(box)

        hpill = patches.FancyBboxPatch(
            (x + 0.08, y + h - 0.36), w - 0.16, 0.28,
            boxstyle="round,pad=0.01,rounding_size=0.04",
            facecolor='#262626',
            edgecolor='#000000',
            linewidth=0.7,
            zorder=3
        )
        ax.add_patch(hpill)
        ax.text(
            x + w/2, y + h - 0.22,
            title,
            ha='center', va='center',
            fontsize=9.0, fontweight='bold',
            fontfamily='Times New Roman',
            color='#FFFFFF', zorder=4
        )

        if subtitle:
            ax.text(
                x + w/2, y + h - 0.48,
                subtitle,
                ha='center', va='center',
                fontsize=7.8, fontstyle='italic',
                fontfamily='Times New Roman',
                color='#444444', zorder=4
            )

        b_y = y + h - 0.68
        for b in bullets:
            ax.text(
                x + 0.15, b_y,
                f"• {b}",
                ha='left', va='top',
                fontsize=7.6, fontfamily='Times New Roman',
                color='#111111', zorder=4
            )
            b_y -= 0.24

    # Layer 1: Data Ingestion (Top)
    draw_card(
        0.5, 9.40, 8.2, 1.25,
        "REAL E-COMMERCE DATA INGESTION & INTERACTION STREAM",
        "Authentic Amazon Electronics, Mobile Accessories, and Verified Customer Review Streams",
        [
            "Product Catalog Entities: Real ASINs, Title, Brand, Category, Image URLs, and Electrical Attributes",
            "Longitudinal Review Corpus: Reviewer IDs, Timestamps, Star Ratings, Verified Purchase Flags, and Review Texts",
            "Ground-Truth Technical Standards: USB-PD 3.0, PPS, Qi2, QC 4+, USB-IF E-Marker Rules, and Safety Directives"
        ]
    )

    # Layer 2: Big Data Analytics & Social Media Analytics (Middle Two Columns)
    draw_card(
        0.5, 5.50, 3.95, 3.65,
        "BIG DATA ANALYTICS (BDA) ENGINE",
        "Sub-Linear Stream Mining & Scalable Search",
        [
            "Bloom Filter: O(1) membership testing for audited ASINs",
            "Optimal Sizing: m = -n*ln(p)/(ln 2)^2, k = (m/n)*ln 2",
            "Count-Min Sketch: Sub-linear frequency tracking",
            "Epsilon-Delta Guarantee: Width w = e/eps, Depth d = ln(1/delta)",
            "Reservoir Sampling: Vitter's Algorithm R for uniform sample",
            "MinHash & LSH: Shingling, permutations, and banding",
            "Sub-Quadratic Detection: O(1) near-duplicate bot search",
            "MapReduce Framework: Distributed review text processing"
        ]
    )

    draw_card(
        4.75, 5.50, 3.95, 3.65,
        "SOCIAL MEDIA ANALYTICS (SMA) ENGINE",
        "Network Centralities, Communities & ABSA",
        [
            "Bipartite Social Graph: G = (U, P, E) connecting users & items",
            "Projected Network: Reviewer Co-Review interaction graph",
            "Centrality Metrics: Degree, Betweenness, and PageRank",
            "FraudRank: Propagating fraud probability across nodes",
            "Louvain Modularity: Greedy modularity community clustering",
            "Syndicate Detection: Isolating dense collusive review rings",
            "Aspect-Based Sentiment: ABSA polarity on charging/thermals",
            "Information Diffusion: Poisson arrival bursts (z >= 3.0 sigma)"
        ]
    )

    # Connectors from Ingestion to BDA & SMA
    ax.annotate("", xy=(2.475, 9.20), xytext=(2.475, 9.40), arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))
    ax.annotate("", xy=(6.725, 9.20), xytext=(6.725, 9.40), arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

    # Layer 3: KGIRS Core (Bottom Row)
    draw_card(
        0.5, 0.45, 8.2, 4.75,
        "KGIRS: MULTIMODAL AGENTIC GRAPHRAG INTELLIGENCE SYSTEM",
        "Overcoming Multi-Hop Compatibility Failures and Hallucinated Specifications",
        [
            "Heterogeneous Knowledge Graph: Multi-relational directed graph linking Products, Protocols, Connectors, and Standards",
            "Multi-Hop Constraint Traversal: Evaluates 3-hop compatibility paths (Device -> Required_Protocol <- Supported_Protocol <- Charger)",
            "Negotiated Wattage Solver: Calculates exact negotiated power (W_eff = min(W_charger, W_device)) and throttles if cable lacks e-Marker",
            "Specification Hallucination Scanner: Verifies marketing claims against ground-truth KG nodes (rejects 120W on iPhone, impossible FDA chips)",
            "Multimodal Visual Grounding: Cross-examines product casing hero photos against technical specs to detect port and label discrepancies",
            "Agentic GraphRAG Orchestrator: Autonomous multi-agent coordination with full verifiable graph provenance for explainable audit decisions"
        ]
    )

    # Connectors from BDA & SMA to KGIRS
    ax.annotate("Stream Metrics", xy=(2.475, 5.25), xytext=(2.475, 5.50), arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2), fontsize=7.5, fontfamily='Times New Roman', ha='center', va='bottom')
    ax.annotate("Social Graph Rings", xy=(6.725, 5.25), xytext=(6.725, 5.50), arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2), fontsize=7.5, fontfamily='Times New Roman', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF')
    plt.close()
    print(f"SUCCESS: BDSMA architecture diagram saved to {output_path}")

if __name__ == "__main__":
    generate_bdsma_architecture_diagram()
