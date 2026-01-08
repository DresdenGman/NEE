"""
Data calibration: control experiment to validate "low-entropy language trap"
"""

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from collections import Counter
import re


def calculate_text_entropy(text: str) -> float:
    words = re.findall(r"\w+", text.lower())
    if not words:
        return 0.0

    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    probs = [count / total_words for count in word_counts.values()]
    entropy = -sum(p * np.log2(p) for p in probs)
    return float(entropy)


def demo_entropy_compare():
    # Sample A: deep thinking (high B)
    text_high_B = """
    The evolution of the cognitive bandwidth relies heavily on the structural integrity
    of the neural pathways, which are maintained through sustained periods of deep focus
    and logical deduction, resisting the immediate gratification of sensory inputs.
    """

    # Sample B: algorithmic fragments (low B)
    text_low_B = """
    OMG look at this!! cannot believe it. click link now.
    viral trend. lol so funny. wait for the end.
    buy this now. trend viral shocking
    """

    entropy_A = calculate_text_entropy(text_high_B)
    entropy_B = calculate_text_entropy(text_low_B)

    print(f"High Cognition Entropy: {entropy_A:.4f}")
    print(f"Algorithmic Noise Entropy: {entropy_B:.4f}")


def histogram_demo(high_texts, low_texts, bins=15):
    high_ent = [calculate_text_entropy(t) for t in high_texts]
    low_ent = [calculate_text_entropy(t) for t in low_texts]

    plt.figure(figsize=(8, 5))
    plt.hist(high_ent, bins=bins, alpha=0.6, color="#2ecc71", label="High B (deep)")
    plt.hist(low_ent, bins=bins, alpha=0.6, color="#e74c3c", label="Low B (fragmented)")
    plt.xlabel("Shannon Entropy")
    plt.ylabel("Count")
    plt.title("Entropy Distribution: High vs Low B")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Optional: statistical test (e.g., KS test)
    ks_stat, ks_p = scipy.stats.ks_2samp(high_ent, low_ent)
    print(f"KS test stat={ks_stat:.4f}, p={ks_p:.4e}")


def main():
    # Demo: single pair of texts
    demo_entropy_compare()

    # Example: batch data (replace with real corpus, at least dozens to hundreds of samples)
    high_samples = [
        "In a rigorous exploration of cognitive architecture, sustained attention enables hierarchical abstraction and symbolic manipulation.",
        "Metacognitive monitoring supports error correction and adaptive strategy selection under high task demands.",
        "Delayed gratification correlates with prefrontal regulation and the consolidation of long-horizon goals.",
    ]
    low_samples = [
        "lol wow crazy watch now so good",
        "click fast trending shocking omg",
        "no way viral must see haha",
    ]

    histogram_demo(high_samples, low_samples, bins=10)


if __name__ == "__main__":
    main()

