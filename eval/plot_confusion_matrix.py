import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def generate_cm_plot():
    # Labels in standardized order
    classes = ["REFUTED", "MISLEADING", "SUPPORTED", "INSUFFICIENT_EVIDENCE"]
    
    # 4x4 Confusion Matrix from 50 pilot claims evaluation
    # Rows: True Label, Cols: Predicted Label
    cm = np.array([
        [23,  0,  0,  0],  # REFUTED
        [ 0, 18,  0,  0],  # MISLEADING
        [ 0,  0,  1,  0],  # SUPPORTED
        [ 0,  0,  0,  8]   # INSUFFICIENT_EVIDENCE
    ])

    plt.figure(figsize=(7, 5.5), dpi=300)
    sns.set_theme(style="white", font_scale=1.0)
    
    # Plotting heatmap
    ax = sns.heatmap(
        cm, 
        annot=True, 
        fmt="d", 
        cmap="Blues", 
        cbar=True,
        xticklabels=["REFUTED", "MISLEADING", "SUPPORTED", "INSUFFICIENT"],
        yticklabels=["REFUTED", "MISLEADING", "SUPPORTED", "INSUFFICIENT"],
        linewidths=1.2,
        linecolor="#dddddd"
    )

    ax.set_title("Stage 6 Verdict Engine Confusion Matrix ($N=50$)", fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Predicted Label", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Adjudicated Gold Label", fontsize=11, fontweight="bold", labelpad=10)
    
    plt.tight_layout()
    
    # Save both high-res PNG and vector PDF for LaTeX
    png_path = "docs/figures/verdict_confusion_matrix.png"
    pdf_path = "docs/figures/verdict_confusion_matrix.pdf"
    
    plt.savefig(png_path, dpi=300)
    plt.savefig(pdf_path, bbox_inches="tight")
    print(f"[+] Confusion matrix plot successfully saved to:\n  - {png_path}\n  - {pdf_path}")

if __name__ == "__main__":
    generate_cm_plot()
