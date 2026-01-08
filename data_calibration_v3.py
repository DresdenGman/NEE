import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import re
import glob
import os

TWITTER_PATH = "twitter.csv"
TWITTER_COL = "tweet"
LIT_FOLDER = "literature_raw/*.txt"
WINDOW_SIZE = 40
SAMPLE_NUM = 2000


def clean_text_segment(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.lower().split()
    return words


def calculate_shannon_entropy(words):
    # Computes Shannon entropy from word frequency distribution
    if len(words) == 0:
        return 0.0
    series = pd.Series(words)
    counts = series.value_counts()
    probs = counts / len(words)
    entropy = -np.sum(probs * np.log2(probs))
    return float(entropy)


def get_twitter_samples():
    print("Loading Twitter data...")
    if not os.path.exists(TWITTER_PATH):
        print(f"Twitter CSV not found: {TWITTER_PATH}")
        return []

    try:
        df = pd.read_csv(TWITTER_PATH, usecols=[TWITTER_COL], nrows=50000)
        df = df.dropna()
    except Exception as e:
        print(f"Twitter load error: {e}")
        return []

    all_words = []
    for text in df[TWITTER_COL].tolist():
        words = clean_text_segment(str(text))
        if words:
            all_words.extend(words)

    if len(all_words) < WINDOW_SIZE:
        print("Twitter text total word count insufficient to construct a window, please check data.")
        return []

    valid_entropies = []
    for i in range(0, len(all_words), WINDOW_SIZE):
        chunk = all_words[i : i + WINDOW_SIZE]
        if len(chunk) == WINDOW_SIZE:
            e = calculate_shannon_entropy(chunk)
            valid_entropies.append(e)
        if len(valid_entropies) >= SAMPLE_NUM:
            break

    return valid_entropies


def get_literature_samples():
    print("Loading Literature data...")
    files = glob.glob(LIT_FOLDER)
    if not files:
        print(f"Error: No txt files found in pattern {LIT_FOLDER}")
        return []

    valid_entropies = []

    for f_path in files:
        try:
            with open(f_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_content = f.read()
                start_idx = raw_content.find("CHAPTER")
                if start_idx == -1:
                    start_idx = 0
                content = raw_content[start_idx:]
                words = clean_text_segment(content)

                for i in range(0, len(words), WINDOW_SIZE):
                    chunk = words[i : i + WINDOW_SIZE]
                    if len(chunk) == WINDOW_SIZE:
                        e = calculate_shannon_entropy(chunk)
                        valid_entropies.append(e)

                    if len(valid_entropies) >= SAMPLE_NUM:
                        break
        except Exception as e:
            print(f"Skipping file {f_path}: {e}")

        if len(valid_entropies) >= SAMPLE_NUM:
            break

    return valid_entropies


def main():
    print(f"--- Calibration Protocol V3.0 ---")
    print(f"Target Window Size: {WINDOW_SIZE} words (Strict Match)")

    low_B = get_twitter_samples()
    high_B = get_literature_samples()

    print(f"\nSample acquisition: Twitter={len(low_B)}, Lit={len(high_B)}")

    if len(low_B) > 100 and len(high_B) > 100:
        print("-" * 30)
        print(f"High B (Literature) Mean Entropy: {np.mean(high_B):.4f}")
        print(f"Low B (Twitter)    Mean Entropy: {np.mean(low_B):.4f}")

        t_stat, p_val = stats.ttest_ind(high_B, low_B, equal_var=False)
        print(f"T-Statistic: {t_stat:.4f}")
        print(f"P-Value: {p_val:.4e}")

        plt.figure(figsize=(10, 6))
        sns.kdeplot(high_B, fill=True, color="#2ecc71", label="Literature (High B)", alpha=0.4, linewidth=2)
        sns.kdeplot(low_B, fill=True, color="#e74c3c", label="Social Media (Low B)", alpha=0.4, linewidth=2)

        plt.axvline(np.mean(high_B), color="#27ae60", linestyle="--")
        plt.axvline(np.mean(low_B), color="#c0392b", linestyle="--")

        plt.title(
            f"Neuro-Entropic Evidence: Text Entropy at Fixed Length (N={WINDOW_SIZE})",
            fontsize=14,
            fontweight="bold",
        )
        plt.xlabel("Shannon Entropy (Bits)", fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        plt.savefig("fig_entropy.png", dpi=300, bbox_inches='tight')
        print("Image saved: fig_entropy.png")
        plt.show()

    else:
        print("Insufficient samples, please check paths and data sources.")


if __name__ == "__main__":
    main()
