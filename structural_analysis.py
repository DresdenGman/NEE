import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import re
import glob
import os

TWITTER_PATH = "twitter.csv"
LIT_FOLDER = "literature_raw/*.txt"
TWITTER_COL = "tweet"


def get_word_counts(text_list):
    all_text = " ".join(str(t) for t in text_list)
    words = re.findall(r"\w+", all_text.lower())
    if not words:
        return np.array([])
    counter = Counter(words)
    freqs = np.array(sorted(counter.values(), reverse=True), dtype=float)
    return freqs


def fit_zipf(freqs, max_fit=1000):
    # Fits Zipf's law by linear regression on log-log coordinates
    if freqs.size == 0:
        return None, None, np.nan

    ranks = np.arange(1, len(freqs) + 1, dtype=float)
    log_ranks = np.log10(ranks)
    log_freqs = np.log10(freqs)
    limit = min(len(freqs), max_fit)
    coeffs = np.polyfit(log_ranks[:limit], log_freqs[:limit], 1)
    slope = coeffs[0]
    return ranks, freqs, slope


def load_literature_texts():
    files = glob.glob(LIT_FOLDER)
    if not files:
        print(f"No txt files found in {LIT_FOLDER}, please check path.")
        return []
    texts = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                texts.append(fh.read())
        except Exception as e:
            print(f"Failed to read literature file {f}: {e}")
    return texts


def load_twitter_texts():
    if not os.path.exists(TWITTER_PATH):
        print(f"Twitter CSV not found: {TWITTER_PATH}")
        return []
    try:
        df = pd.read_csv(TWITTER_PATH, usecols=[TWITTER_COL], nrows=20000)
        return df[TWITTER_COL].dropna().tolist()
    except Exception as e:
        print(f"Failed to read Twitter CSV: {e}")
        return []


def get_top_words(text_list, top_n=50):
    all_text = " ".join(str(t) for t in text_list)
    words = re.findall(r"\w+", all_text.lower())
    counter = Counter(words)
    return counter.most_common(top_n)


def calculate_r_squared(ranks, freqs, slope, max_fit=1000):
    if ranks is None or freqs is None or np.isnan(slope):
        return np.nan
    
    limit = min(len(ranks), max_fit)
    log_ranks = np.log10(ranks[:limit])
    log_freqs = np.log10(freqs[:limit])
    
    intercept = np.polyfit(log_ranks, log_freqs, 1)[1]
    fitted = slope * log_ranks + intercept
    
    ss_res = np.sum((log_freqs - fitted) ** 2)
    ss_tot = np.sum((log_freqs - np.mean(log_freqs)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else np.nan
    return r_squared


def main():
    print("Loading data for Structural Analysis...")

    lit_texts = load_literature_texts()
    tw_texts = load_twitter_texts()

    if not lit_texts or not tw_texts:
        print("Insufficient data, cannot perform structural analysis.")
        return

    print("Calculating Zipf distributions...")
    lit_freqs = get_word_counts(lit_texts)
    tw_freqs = get_word_counts(tw_texts)

    lit_ranks, lit_freqs, lit_slope = fit_zipf(lit_freqs)
    tw_ranks, tw_freqs, tw_slope = fit_zipf(tw_freqs)

    lit_r2 = calculate_r_squared(lit_ranks, lit_freqs, lit_slope)
    tw_r2 = calculate_r_squared(tw_ranks, tw_freqs, tw_slope)

    print(f"\n{'='*50}")
    print("ZIPF'S LAW ANALYSIS RESULTS")
    print(f"{'='*50}")
    print(f"Literature Zipf Slope: {lit_slope:.4f} (Expected ~ -1.0)")
    print(f"Twitter Zipf Slope   : {tw_slope:.4f}")
    print(f"\nFit Quality (R²):")
    print(f"Literature R²: {lit_r2:.4f}")
    print(f"Twitter R²    : {tw_r2:.4f}")
    
    print(f"\n{'='*50}")
    print("TOP 20 HIGH-FREQUENCY WORDS COMPARISON")
    print(f"{'='*50}")
    lit_top = get_top_words(lit_texts, top_n=20)
    tw_top = get_top_words(tw_texts, top_n=20)
    
    print("\nLiterature Top 20:")
    for i, (word, freq) in enumerate(lit_top, 1):
        print(f"  {i:2d}. {word:15s} ({freq:,})")
    
    print("\nTwitter Top 20:")
    for i, (word, freq) in enumerate(tw_top, 1):
        print(f"  {i:2d}. {word:15s} ({freq:,})")
    
    lit_words_set = set(w for w, _ in lit_top)
    tw_words_set = set(w for w, _ in tw_top)
    overlap = lit_words_set & tw_words_set
    print(f"\nHigh-frequency word overlap: {len(overlap)}/20 words appear in both Top 20")
    print(f"Overlapping words: {', '.join(sorted(overlap))}")
    
    print(f"\n{'='*50}")
    print("INTERPRETATION:")
    print(f"{'='*50}")
    print("1. Zipf slopes close to -1.0 indicate both corpora follow natural language power-law distribution.")
    print("2. High-frequency word overlap reflects the universality of function words (the, and, of...).")
    print("3. Differences mainly manifest in:")
    print("   - Literature: More content words (species, variation, natural...)")
    print("   - Twitter: May contain more emotional words, topic tags, internet slang")
    print("4. Algorithmic media 'destructuring' is more likely reflected at semantic/syntactic level, not word frequency distribution.")
    print(f"{'='*50}\n")

    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    if lit_ranks is not None:
        plt.loglog(
            lit_ranks,
            lit_freqs,
            "g-",
            alpha=0.8,
            linewidth=2,
            label=f"Literature (Slope={lit_slope:.2f}, R²={lit_r2:.3f})",
        )

    if tw_ranks is not None:
        plt.loglog(
            tw_ranks,
            tw_freqs,
            "r-",
            alpha=0.8,
            linewidth=2,
            label=f"Twitter (Slope={tw_slope:.2f}, R²={tw_r2:.3f})",
        )

    plt.title("The Signature of Cognitive Structure: Zipf's Law Analysis", fontsize=14, fontweight='bold')
    plt.xlabel("Word Rank (log scale)", fontsize=12)
    plt.ylabel("Frequency (log scale)", fontsize=12)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.subplot(2, 1, 2)
    lit_words = [w for w, _ in lit_top[:10]]
    lit_counts = [c for _, c in lit_top[:10]]
    tw_words = [w for w, _ in tw_top[:10]]
    tw_counts = [c for _, c in tw_top[:10]]
    
    x_pos = np.arange(len(lit_words))
    width = 0.35
    
    plt.bar(x_pos - width/2, lit_counts, width, label='Literature', color='green', alpha=0.7)
    plt.bar(x_pos + width/2, tw_counts, width, label='Twitter', color='red', alpha=0.7)
    
    plt.xlabel('Top 10 Words', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Top 10 High-Frequency Words Comparison', fontsize=12, fontweight='bold')
    plt.xticks(x_pos, lit_words, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig("fig_zipf.png", dpi=300, bbox_inches='tight')
    print("Image saved: fig_zipf.png")
    plt.show()


if __name__ == "__main__":
    main()
