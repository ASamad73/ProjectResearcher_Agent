<p align="center">
  <h1 align="center">
    🖼️ Vision-Language Domain Generality: <br> Robust DA/DG via Invariant Learning & Prompt Tuning 🚀
  </h1>
  <i>Investigating Robustness under Distribution Shift: From Empirical Risk Minimization to CLIP Prompt Alignment</i>
</p>

---

## 📌 Project Overview
This repository explores the post-training challenges of making machine learning models robust to distribution shifts. Our research covers three primary pillars of modern robustness:

1.  **Unsupervised Domain Adaptation (UDA)**: Aligning feature distributions between labeled source domains and unlabeled target domains using DAN, DANN, and Entropy Minimization.
2.  **Domain Generalization (DG)**: Evaluating invariant learning techniques (IRM, Group-DRO) and geometric optimization (SAM) to find flat minima that generalize to unseen environments.
3.  **Vision-Language Stability (CLIP)**: Investigating if prompts act as a stable "control knob" for adaptation, using gradient-alignment techniques to mitigate interference.

---

## 🧑‍💻 My Contributions (Abdul Samad)
I led **Task 3: CLIP Prompt Learning & Stability**, where I focused on the integration of parameter-efficient fine-tuning with gradient-based consensus methods:

* **Prompt-Based DA Framework**: Formulated a DA framework using **CoOp-style learned context vectors** combined with an **unsupervised entropy minimization loss**. This achieved **22.17% accuracy** on stylized domains, significantly outperforming zero-shot (17.33%) and linear probing (20.23%).
* **Gradient Alignment (PCGrad)**: Orchestrated a multi-source gradient alignment strategy using **Projected Conflicting Gradients (PCGrad)**. By projecting conflicting domain gradients onto orthogonal planes, I **doubled the average cosine similarity** between gradient vectors (0.17 ➔ 0.33), effectively mitigating negative interference.
* **Robustness Quantification**: Analyzed the trade-off between adaptation and open-set robustness using **AUROC** and **Mean Maximum Softmax Probability (MSP)**. I identified "architectural brittleness," where prompt tuning improved domain-specific performance (AUROC to 0.56) but led to near-orthogonal embeddings (0.0132 similarity) and overconfidence on unseen classes.

---

## 🧠 Architecture & Methodology

### 🔹 Unsupervised Domain Adaptation (UDA)
* **Approach**: Evaluated models on the Digit-Bench (MNIST, SVHN, USPS). 
* **Key Finding**: Purely adversarial methods (DANN/CDAN) are enhanced significantly by **Entropy Minimization**, which forces the model to make confident predictions on the unlabeled target domain.

### 🔹 DG via Invariant & Robust Learning
* **Techniques**: Compared IRM, Group-DRO, and **Sharpness-Aware Minimization (SAM)**.
* **Key Finding**: SAM consistently outperformed IRM and Group-DRO on the PACS dataset. By seeking **geometrically flat minima**, SAM avoids over-fitting to specific domain variances, preserving class discriminability.

### 🔹 CLIP Stability 
* **Problem**: Does prompt tuning on stylized data (e.g., Sketch) degrade CLIP's general knowledge?
* **Mechanism**: Implemented learnable prompts and **PCGrad** to ensure that updates from "Domain A" do not cancel out the performance on "Domain B."

---

## 📊 Quantitative Summary (Global Results)

| Task | Method | Metric | Result | Key Insight |
| :--- | :--- | :--- | :--- | :--- |
| **UDA** | CDAN + Ent-Min | Accuracy | **43.1%** | Surpassed standard DANN (38.5%). |
| **DG** | SAM | Mean Acc | **84.2%** | Superior robustness over IRM (81.8%). |
| **CLIP** | CoOp + Ent-Min | Accuracy | **22.17%** | +4.8% improvement over Zero-Shot. |
| **CLIP** | PCGrad | Cosine Sim | **0.33** | 2x increase in gradient agreement. |
| **Robust** | Prompt Tuning | AUROC | **0.56** | High domain-acc but lower open-set stability. |

---

## 📂 Repository Structure

```text
├── src/                       
│   ├── Domain Adaptation/                  # Unsupervised Domain Adaptation Basics
│   │   └── unsupervised_da_and_alignment.ipynb
│   ├── Domain Generalization/                  # DG via Invariant & Robust Learning
│   │   ├── erm_multi_domain.ipynb
│   │   ├── group_dro_worst_case_optimizaion.ipynb
│   │   ├── invariant_risk_minimization_irm.ipynb
│   │   └── sharpness_aware_minimization_sam.ipynb
│   ├── DA&DG with CLIP                  # Task Lead: Abdul Samad - CLIP & Prompt Tuning
│   │   └── clip_prompt_tuning_and_gradient_alignment.ipynb
├── docs/                       # Project Documentation
│   └── Technical_Project_Report.pdf  # Full research paper & mathematical formulations
└── README.md                   # Project documentation

```

---

## ⚠ Limitations & Reproducibility
* **Robustness Trade-off:** Observed a clear "adaptation-generality" trade-off; while prompt tuning significantly improves performance on stylized target domains, it induces architectural brittleness and overconfidence on open-set (unseen) classes.
* **Optimization Sensitivity:** Methods like IRM and Group-DRO showed high sensitivity to penalty weights and environment partitioning. Similarly, SAM (Sharpness-Aware Minimization) provides superior generalization but requires a double-backward pass, increasing computational overhead by ~2x per iteration.
* **Gradient Conflict:** In the CLIP task, we identified that training on disparate domains (e.g., Sketch vs. Cartoon) often generates **conflicting gradient directions**, which can lead to unstable prompt embeddings. Without alignment strategies like **PCGrad**, the optimization may converge to a solution that favors one domain at the catastrophic expense of others.

---

## 🤝 Team Roles & Contributions 
* **Abdul Samad:** Lead for DA/DG with CLIP (CLIP Prompt Learning, PCGrad, and Open-Set Robustness analysis). (See detailed [My Contributions] section above).
* **Hamza Habib:** Lead for Domain Generalization.
* **Rumaan Mujtaba:** Lead for Domain Adaptation.

---

## 📄 Reference

The research work and detailed metrics are documented in our [📄 Research Paper](./docs/Technical_Project_Report.pdf).

---

⭐️ If you find this research useful, please consider giving the repository a star!
