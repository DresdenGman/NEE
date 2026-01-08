"""
Data Calibration v2.0
Compare linguistic entropy distributions between Twitter and Literature (books.db)
to validate the "low-entropy language trap" hypothesis.
"""

import os
import re
import random
import sqlite3
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


TWITTER_PATH = "/Users/a24300/Documents/NEE/twitter.csv"
TWITTER_TEXT_COLUMN = "tweet"

BOOKS_DB_PATH = "/Users/a24300/Documents/NEE/books.db"
BOOKS_TABLE_NAME = "book_original"
BOOKS_TEXT_COLUMN = "chapter"

TARGET_WORD_COUNT = 40
SAMPLE_SIZE = 5000
MAX_TWITTER_ROWS = 50000


# ============================================================

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def calculate_entropy(text: str):
    words = text.split()
    if len(words) < 5:
        return None

    series = pd.Series(words)
    counts = series.value_counts()
    probs = counts / len(words)
    entropy = -np.sum(probs * np.log2(probs))
    return float(entropy)


def get_twitter_entropy():
    print(f"Loading Twitter data from {TWITTER_PATH}...")
    if not os.path.exists(TWITTER_PATH):
        print(f"Twitter CSV not found: {TWITTER_PATH}")
        return []

    try:
        df = pd.read_csv(TWITTER_PATH, nrows=MAX_TWITTER_ROWS)
    except Exception as e:
        print(f"Error reading Twitter CSV: {e}")
        return []

    if TWITTER_TEXT_COLUMN not in df.columns:
        print(f"Twitter CSV missing column '{TWITTER_TEXT_COLUMN}', available columns: {list(df.columns)}")
        return []

    entropies = []
    print("Processing Twitter data...")

    df_sample = df.sample(n=min(len(df), SAMPLE_SIZE * 2), random_state=42)

    for raw_text in df_sample[TWITTER_TEXT_COLUMN]:
        cleaned = clean_text(raw_text)
        n_words = len(cleaned.split())
        if 20 <= n_words <= 60:
            e = calculate_entropy(cleaned)
            if e is not None:
                entropies.append(e)

    entropies = entropies[:SAMPLE_SIZE]
    print(f"Twitter entropy samples: {len(entropies)}")
    return entropies


def _auto_detect_books_table_and_column(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    if not tables:
        raise RuntimeError("No tables found in books.db")

    table = None
    for t in tables:
        lower = t.lower()
        if "book" in lower or "text" in lower or "corpus" in lower:
            table = t
            break
    if table is None:
        table = tables[0]

    cur.execute(f"PRAGMA table_info('{table}')")
    cols_info = cur.fetchall()
    if not cols_info:
        raise RuntimeError(f"Table {table} has no column info")

    candidates = []
    for _, name, col_type, *_ in cols_info:
        candidates.append((name, col_type))

    text_col = None
    print(f"Table {table} columns: {candidates}")

    for name, col_type in candidates:
        lname = name.lower()
        ltype = (col_type or "").lower()
        if ("text" in lname or "content" in lname or "body" in lname) or ("text" in ltype):
            text_col = name
            break
    if text_col is None:
        text_col = candidates[0][0]

    return table, text_col


def get_literature_entropy():
    print(f"Loading Literature data from {BOOKS_DB_PATH}...")
    if not os.path.exists(BOOKS_DB_PATH):
        print(f"books.db not found: {BOOKS_DB_PATH}")
        return []

    conn = sqlite3.connect(BOOKS_DB_PATH)
    try:
        table = BOOKS_TABLE_NAME
        text_col = BOOKS_TEXT_COLUMN

        if table is None or text_col is None:
            table, text_col = _auto_detect_books_table_and_column(conn)
            print(f"Auto-detected table: {table}, text column: {text_col}")
        else:
            print(f"Using configured table: {table}, text column: {text_col}")

        query = f"SELECT {text_col} FROM {table} LIMIT {SAMPLE_SIZE * 50};"
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error reading books.db: {e}")
        conn.close()
        return []
    conn.close()

    all_chunks = []
    short_texts = []
    print("Processing Literature data (sliding window chunks, with fallback for short rows)...")

    for raw_text in df[text_col]:
        cleaned = clean_text(raw_text)
        words = cleaned.split()
        if not words:
            continue

        if len(words) >= TARGET_WORD_COUNT:
            for i in range(0, len(words), TARGET_WORD_COUNT):
                chunk = words[i : i + TARGET_WORD_COUNT]
                if len(chunk) == TARGET_WORD_COUNT:
                    all_chunks.append(" ".join(chunk))
        else:
            short_texts.append(cleaned)

    entropies = []

    if all_chunks:
        sampled_chunks = random.sample(all_chunks, min(len(all_chunks), SAMPLE_SIZE))
        for chunk in sampled_chunks:
            e = calculate_entropy(chunk)
            if e is not None:
                entropies.append(e)
    else:
        print("No chunks >= TARGET_WORD_COUNT found, falling back to full-row text.")
        if not short_texts:
            print("Literature data is empty, please check if books.db contains actual text content.")
            return []
        sampled_rows = random.sample(short_texts, min(len(short_texts), SAMPLE_SIZE))
        for txt in sampled_rows:
            e = calculate_entropy(txt)
            if e is not None:
                entropies.append(e)

    if not entropies:
        print("Still no valid entropy samples from literature data, please check books.db content.")
        return []

    print(f"Literature entropy samples: {len(entropies)}")
    return entropies


def main():
    low_B_entropies = get_twitter_entropy()
    high_B_entropies = get_literature_entropy()

    if len(low_B_entropies) > 0 and len(high_B_entropies) > 0:
        ks_stat, p_value = stats.ks_2samp(high_B_entropies, low_B_entropies)

        print("-" * 40)
        print("RESULTS SUMMARY:")
        print(f"High B (Literature) Mean Entropy: {np.mean(high_B_entropies):.4f}")
        print(f"Low B (Twitter)    Mean Entropy: {np.mean(low_B_entropies):.4f}")
        print(f"KS Statistic: {ks_stat:.4f}")
        print(f"P-Value    : {p_value:.4e}")
        print("-" * 40)
        plt.figure(figsize=(10, 6))
        sns.kdeplot(high_B_entropies, fill=True, color="green", label="Literature (High B)", alpha=0.3)
        sns.kdeplot(low_B_entropies, fill=True, color="red", label="Twitter (Low B)", alpha=0.3)

        plt.axvline(np.mean(high_B_entropies), color="green", linestyle="--")
        plt.axvline(np.mean(low_B_entropies), color="red", linestyle="--")

        plt.title("Evidence of Algorithmic Flattening: Linguistic Entropy Gap", fontsize=14)
        plt.xlabel("Shannon Entropy (per chunk)", fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    else:
        print("Data loading failed. Please check Twitter CSV and books.db paths and column names.")


if __name__ == "__main__":
    main()


