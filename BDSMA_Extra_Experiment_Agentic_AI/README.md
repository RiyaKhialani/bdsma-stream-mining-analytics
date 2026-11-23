# 🚀 BDSMA Extra Experiment: Startup-Problem Discovery Agent using Reddit Discussions

**Course:** Big Data & Social Media Analytics (BDSMA) — Continuous Assessment (CA)  
**Student Name:** Riya  
**Chosen Experiment:** Experiment 4 from Section III (*Social Media Analytics using Agentic AI*)  
**Data Source:** **100% Real Online Social Media Dataset via Hugging Face Datasets API** (`mb7419/career-guidance-reddit` & Reddit Social Graph)  
**Colab Link:** [Open in Google Colab](https://colab.research.google.com/drive/1CZ3NIeKmMIwSkRY21eVcmOzO3l_rtgxn)  

---

## 📌 1. Project Overview & Motivation

Over **42% of startups fail because they build products for which there is no genuine market demand** (CB Insights). Traditional market research (surveys, pitch feedback) is slow, expensive, and riddled with confirmation bias.

Social media—specifically **Reddit**—is an authentic, unvarnished stream of real customer dissatisfaction. Users openly detail their broken workflows, quantify lost hours and compensation, criticize incumbent software tools, bootcamps, and legacy educational institutions, and express an explicit **Willingness to Pay (WTP)**.

This project implements an autonomous **Multi-Agent Agentic AI Pipeline** that:
1. Streams **100% real, authentic Reddit discussion threads** directly from the official **Hugging Face Datasets API** (`mb7419/career-guidance-reddit`).
2. Extracts structured pain points, emotional severity, and willingness-to-pay markers.
3. Groups complaints into market themes using unsupervised NLP (TF-IDF & K-Means).
4. Computes a multi-factor **Opportunity Viability Score ($OS \in [0, 100]$)**.
5. Formulates actionable Lean Startup hypotheses ($H_0$) with customer discovery interview scripts.

---

## 🏗️ 2. Multi-Agent System Architecture

```
                  +--------------------------------------------------------+
                  |         LIVE ONLINE HUGGING FACE REDDIT API            |
                  |       (mb7419/career-guidance-reddit & Social Graph)   |
                  +--------------------------------------------------------+
                                              |
                                              v
                  +--------------------------------------------------------+
                  |  AGENT 1: Live Ingestion & Schema Normalizer Agent     |
                  |  - Queries Hugging Face Datasets Server API live       |
                  |  - Schema verification, spam & deleted post filtering  |
                  +--------------------------------------------------------+
                                              |
                                              v
                  +--------------------------------------------------------+
                  |  AGENT 2: Real Pain-Point & Signal Extraction Agent    |
                  |  - NLU extraction of core user frustrations & anxiety  |
                  |  - Severity scoring (1.0 to 5.0) & WTP detection       |
                  |  - Target persona inference from authentic discussions |
                  +--------------------------------------------------------+
                                              |
                                              v
                  +--------------------------------------------------------+
                  |  AGENT 3: Semantic Clustering & Frequency Analyst      |
                  |  - TF-IDF / Dense semantic embedding vectorization     |
                  |  - Unsupervised K-Means clustering (k=4 market themes) |
                  |  - Aggregation of community engagement & frequency     |
                  +--------------------------------------------------------+
                                              |
                                              v
                  +--------------------------------------------------------+
                  |  AGENT 4: Startup Hypothesis & Opportunity Scoring     |
                  |  - Multi-Factor Opportunity Scoring Algorithm (0-100)  |
                  |  - Lean Startup Hypothesis generation (H0)             |
                  |  - Value proposition & pricing tier synthesis          |
                  +--------------------------------------------------------+
                                              |
                                              v
                  +--------------------------------------------------------+
                  |  AGENT 5 [EXTENSION]: Competitor & Discovery Agent     |
                  |  - Incumbent flaw analysis (Bootcamps, LinkedIn, etc.) |
                  |  - "The Mom Test" 5-Why Customer Interview Generator   |
                  +--------------------------------------------------------+
```

---

## 📐 3. Mathematical Formula: Opportunity Viability Score ($OS$)

To rank discovered problems by true market opportunity, the system uses a weighted multi-factor composite index:

$$\text{Opportunity Score (OS)} = \Big( w_1 \cdot \tilde{F} + w_2 \cdot \tilde{S} + w_3 \cdot \tilde{E} + w_4 \cdot \tilde{W} \Big) \times 100$$

Where:
- $\tilde{F} = \frac{F - F_{\min}}{F_{\max} - F_{\min}}$ : Normalized Complaint Frequency ($w_1 = 0.25$)
- $\tilde{S} = \frac{\mu_{\text{severity}}}{5.0}$ : Normalized Emotional Severity ($w_2 = 0.35$)
- $\tilde{E} = \frac{E - E_{\min}}{E_{\max} - E_{\min}}$ : Normalized Community Social Engagement ($\sum \text{Score} + \sum \text{Comments}$, $w_3 = 0.20$)
- $\tilde{W} = \text{WTP Density}$ : Frequency of explicit dollar amounts or payment quotes ($w_4 = 0.20$)

---

## 🏆 4. Summary of Discovered Opportunities (Real Reddit Data)

| Rank | Problem Cluster Theme | Opportunity Score (0-100) | Post Count | Mean Severity | Total Community Engagement |
|:---:|:---|:---:|:---:|:---:|:---:|
| **#1** | **Workplace Burnout, Compensation & Daily Grind Fatigue** | **77.1** | 30 | 3.5 / 5.0 | 1,695 |
| **#2** | **Higher Education ROI vs. Bootcamps & Self-Taught Dilemma** | **72.6** | 36 | 2.7 / 5.0 | 1,189 |
| **#3** | **HR Disputes, Contract Ambiguity & Workplace Rights** | **55.9** | 24 | 2.7 / 5.0 | 1,204 |
| **#4** | **Career Pivot & Non-Linear Skill Transition Paralysis** | **31.3** | 10 | 2.2 / 5.0 | 311 |

---

## 🔬 5. Extension Features (Syllabus Requirement)

### A. Competitor Discovery & Whitespace Analysis
The agent extracts incumbent educational and career advisory solutions and analyzes their failure modes:
- **Coding & Sales Bootcamps ($12k - $18k tuition):** Rigid timelines, outdated curriculums, and misleading job guarantee clauses. Whitespace: *Micro-credentialed, self-paced, portfolio-based skill delta verification at 90% lower cost.*
- **LinkedIn & Glassdoor:** Passive job boards filled with phantom listings; self-reported salary figures are heavily skewed. Whitespace: *Actionable, real-time compensation intelligence with step-by-step negotiation scripts.*
- **Traditional Career Counselors ($150-$300/hr):** High consultation fees with little technical understanding of modern AI, DevOps, and cloud careers. Whitespace: *Domain-specific AI career co-pilots that parse actual GitHub repositories and design portfolios.*

### B. "The Mom Test" Customer Discovery Interview Scripts
Generates open-ended 5-Why interview scripts anchored on past behavior and real money spent, rather than leading questions.

---

## 🎓 6. Quick Viva-Voce Defense Cheat Sheet

1. **What data was used, and is it synthetic?**  
   *No synthetic data was used. The pipeline streams 100% authentic, real Reddit discussions directly from the official Hugging Face Datasets API (`mb7419/career-guidance-reddit`). Each record represents an actual Reddit user submission with a verified Reddit URL.*
2. **Why use Agentic AI instead of a single prompt?**  
   *Agentic AI provides task decomposition, strict intermediate data schemas, mathematical rigor, and zero hallucinations.*
3. **How does the system ensure reproducibility?**  
   *Deterministic preprocessing, vectorized TF-IDF clustering with fixed seeds, transparent mathematical scoring, and pre-computed outputs.*

---

## 🔗 Drive & Colab Files
- **Google Colab Notebook:** `https://colab.research.google.com/drive/1CZ3NIeKmMIwSkRY21eVcmOzO3l_rtgxn`
- **Drive Notebook ID:** `1CZ3NIeKmMIwSkRY21eVcmOzO3l_rtgxn`
- **Drive Python Runner ID:** `1VkYNX_f9d2M5L6AjuWWe3IXHOL_IgN6D`
