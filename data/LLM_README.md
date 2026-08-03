<h1 align="center">🧠 LLM Decoding Dynamics & Preference Alignment 🤖</h1>

<p align="center">
  <b>Comparative Analysis of Generation Strategies & DPO-based Policy Alignment</b><br>
  <i>A Research Framework for Investigating Diversity–Quality Trade-offs and Alignment Stability</i>
</p>

---

## 📌 Project Overview
This repository provides a focused, reproducible research framework investigating the post-training lifecycle of Large Language Models (LLMs). Our research focuses on three primary pillars:

1. **Decoding Dynamics**: Empirical benchmarking of **Greedy, Beam, Top-K, and Top-P** sampling with temperature sweeps to quantify the trade-off between generation quality and lexical diversity.
2. **Preference Alignment**: Implementation and evaluation of **Direct Preference Optimization (DPO)** using **PEFT/LoRA** adapters, alongside a comparative stability analysis of **Group Relative Policy Optimization (GRPO)**.
3. **Mechanistic Interpretability**: **Universal Sparse Autoencoder (USAE)** experiments to probe shared internal features across model families and test the "Platonic Representation Hypothesis."

---

## 🧑‍💻 My Contributions (Abdul Samad)
I led the **Decoding Dynamics** and **DPO Alignment** modules. My contributions included end-to-end implementation, empirical analysis, and technical writing:

* **Decoding Dynamics (llm_decoding_strategies.ipynb)**: Full implementation of generation pipelines for all four decoding strategies. I designed the evaluation suite (using **Distinct-N** and reward vs. diversity metrics) and authored the core analysis notebooks and visualization plots.
* **DPO — PEFT / LoRA ** (dpo_alignment_analysis.ipynb)**: Orchestrated the DPO training pipeline using **LoRA adapters** ($r=8, \alpha=16$). I was responsible for computing perplexity shifts, mean token KL-divergence, and conducting robustness/reward-hacking stress tests.
* **Report & Figures**: Co-authored the technical report and prepared all figures and data visualizations associated with my contributions above.

*Team members handled GRPO stability experiments and SAE interpretability. See the [Contributions] section at the end for more details.*

---

## 🧠 Architecture & Methodology



### 🔹 Module 1: Decoding Strategy Analysis
* **Goal**: Quantify the quality–diversity tradeoff across decoding modes and temperatures.
* **Approach**: Generated outputs using multiple modes, computing **Distinct-1/2/3**, reward scores (via a reference reward model), and plotting reward vs. diversity frontiers.
* **Key Insight**: **Top-P (nucleus) sampling** adapts the candidate set dynamically and consistently offers a superior reward–diversity frontier than fixed Top-K at comparable temperatures.

### 🔹 Module 2: Preference Alignment (DPO vs GRPO)
* **Goal**: Align model outputs to human preferences while measuring the “Alignment Tax” (e.g., change in perplexity/KL) and robustness.
* **Approach**: Implemented **DPO using PEFT/LoRA** to avoid expensive full-model fine-tuning. Compared results against **GRPO** as a baseline to record instability modes.
* **Key Insight**: DPO + LoRA yields stable aligned policies with a modest alignment tax ($KL \approx 0.016$). Conversely, GRPO exhibited severe instability and mode collapse under several hyperparameter regimes.

### 🔹 Module 3: Mechanistic Interpretability (USAE)
* **Goal**: Test whether different architectures share universal high-level features (Partial Platonic Hypothesis).
* **Approach**: Trained a **Universal Sparse Autoencoder** on activations from ResNet and ViT, measuring cross-reconstruction $R^2$ and feature co-firing statistics.
* **Key Insight**: Evidence supports partial universality—shared semantic features exist but come with a measurable alignment cost.



---

## 📊 Quantitative Summary (from the Report)

| Component | Notable Metric(s) | Key Takeaway |
| :--- | :--- | :--- |
| **Top-P vs Top-K** | Reward-Diversity Frontier | Top-P offers superior dynamic adaptation |
| **DPO (LoRA)** | Perplexity: **~11.00**; Mean KL: **~0.016** | Controlled verbosity; stable alignment |
| **GRPO** | Perplexity: **~48.13** (Failure runs) | Observed high instability and mode collapse |
| **USAE** | Cross-reconstruction $R^2$: **0.62–0.72** | Alignment tax ≈ 5% reduction in $R^2$ |

---

## 📂 Repository Structure

```text
src/
├── Decoding/
│   └── llm_decoding_strategies.py                 # Task 1 Implementation
├── Alignment/
│   ├── dpo_alignment_analysis.py                  # Task 2 (My Implementation)
│   └── grpo_alignment_and_stability_analysis.py   # Task 2 (Baseline)
├── Interpretability/
│   └── sae_cross_model_alignment.py               # Task 3 Implementation
├── docs/
│   └── Technical_Project_Report.pdf               # Full Research Paper
└── README.md
```

---

### ⚠ Limitations & Reproducibility

* **Model Scale:** Experiments used SmolLM2-135M-SFT due to compute constraints.
* **GRPO Sensitivity:** Observed instability is highly dependent on hyperparameters and group sizes.
* **Reproducibility:** Saved checkpoints and logs are included to allow for figure reproduction without full retraining.

---

### 🤝 Team Roles & Contributions
* **Abdul Samad (ASamad73):** Lead LLM Decoding Dynamics and Direct Preference Optimization. Implemented the generation pipelines for all four decoding strategies and orchestrated the DPO alignment suite using LoRA adapters.
* **Hamza Habib:** GRPO implementation, stability diagnostics, and benchmarking.
* **Rumaan Mujtaba:** UAE implementation and mechanistic interpretability visualizations.
* **Collective:** Co-authored the ICML-style Technical Report with Hamza Habib and Rumaan Mujtaba

---

## 📄 Reference

The research work and detailed metrics are documented in our [📄 Research Paper](./docs/Technical_Project_Report.pdf).

---

⭐️ If you find this research useful, please consider giving the repository a star!
