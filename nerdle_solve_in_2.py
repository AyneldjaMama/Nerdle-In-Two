#!/usr/bin/env python3
"""
nerdle_solve_in_2.py
====================
Computes the probability of solving Nerdle (Classic, 8-character) in exactly
two guesses, for every possible first guess drawn from the official solution
set of 17,723 equations.

Data source
-----------
The file NerdleClassicRestricted.txt must be present in the same directory.
It can be downloaded from:
  https://github.com/pedrokkrause/Nerdle-Equations

Mathematical framework
----------------------
Let N = 17,723 (total solutions, each equally likely to be the day's answer).

1. The player submits a first guess G.
2. The game returns a feedback pattern P — an 8-character sequence of
   green (correct position), purple (right character, wrong position),
   and black (character not present, or already accounted for).
3. That pattern P is consistent with some subset of K(P) solutions.
4. The player then picks one of those K(P) candidates at random as
   their second guess. The probability of it being correct is 1/K(P).

For a fixed first guess G, the probability of solving in exactly 2 is:

    P(solve in 2 | G)
        = (1/N) * Σ_{S ≠ G}  1 / K(feedback(G, S))

Grouping the sum by distinct feedback patterns:

    = (1/N) * Σ_{patterns P ≠ all-green}  K(P) × (1/K(P))
    = (1/N) * Σ_{patterns P ≠ all-green}  1
    = (number of distinct non-all-green feedback patterns) / N

This elegant result means the probability depends ONLY on how many distinct
feedback patterns the first guess produces — not on the sizes of the
individual buckets.

Usage
-----
    python3 nerdle_solve_in_2.py

Runtime is approximately 3–4 minutes on a modern machine.
"""

import os
import sys
import time
import numpy as np
from collections import Counter


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_solutions(filepath: str) -> list[str]:
    """Load the list of valid 8-character Nerdle solutions from a text file."""
    with open(filepath, "r") as f:
        solutions = [line.strip() for line in f if line.strip()]
    # Sanity check
    for s in solutions:
        assert len(s) == 8, f"Expected 8-char equation, got '{s}' (len {len(s)})"
    return solutions


def encode_solutions(solutions: list[str]) -> np.ndarray:
    """Convert list of 8-char strings to an (N, 8) uint8 NumPy array of ASCII codes."""
    n = len(solutions)
    encoded = np.zeros((n, 8), dtype=np.uint8)
    for i, s in enumerate(solutions):
        for j, c in enumerate(s):
            encoded[i, j] = ord(c)
    return encoded


# ---------------------------------------------------------------------------
# Feedback computation
# ---------------------------------------------------------------------------

def compute_feedback(guess: np.ndarray, all_secrets: np.ndarray) -> np.ndarray:
    """
    Compute the Nerdle feedback pattern for one guess against every solution.

    Parameters
    ----------
    guess : np.ndarray, shape (8,), dtype uint8
        ASCII-encoded first guess.
    all_secrets : np.ndarray, shape (N, 8), dtype uint8
        ASCII-encoded solution list.

    Returns
    -------
    pattern_hashes : np.ndarray, shape (N,), dtype int64
        Each entry is a base-3 hash of the 8-position feedback:
        0 = black, 1 = purple, 2 = green.
    """
    N = all_secrets.shape[0]
    result = np.zeros((N, 8), dtype=np.uint8)

    # --- Pass 1: mark greens (correct character in correct position) ---
    greens = guess[np.newaxis, :] == all_secrets          # (N, 8) bool
    result[greens] = 2

    # --- Pass 2: mark purples, respecting character frequencies ---
    for char in np.unique(guess):
        guess_positions = np.where(guess == char)[0]

        char_in_secret = all_secrets == char               # (N, 8)
        char_green     = greens & char_in_secret           # (N, 8)

        # How many of this char remain unmatched (non-green) in each secret
        remaining = char_in_secret.sum(axis=1) - char_green.sum(axis=1)  # (N,)

        # Walk through guess positions for this char; assign purples in order
        assigned = np.zeros(N, dtype=np.int32)
        for p in guess_positions:
            is_green_here = greens[:, p]
            can_purple = (~is_green_here) & (assigned < remaining)
            result[can_purple, p] = 1
            assigned[can_purple] += 1

    # --- Encode as a single integer per solution (base-3 hash) ---
    powers = np.array([3 ** i for i in range(8)], dtype=np.int64)
    pattern_hashes = (result.astype(np.int64) * powers[np.newaxis, :]).sum(axis=1)
    return pattern_hashes


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def main():
    # Locate data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "NerdleClassicRestricted.txt")
    if not os.path.exists(data_path):
        sys.exit(f"ERROR: {data_path} not found. Download it from "
                 "https://github.com/pedrokkrause/Nerdle-Equations")

    solutions = load_solutions(data_path)
    N = len(solutions)
    encoded = encode_solutions(solutions)

    ALL_GREEN_HASH = sum(2 * (3 ** i) for i in range(8))   # pattern for a perfect match

    print(f"Nerdle Classic — Probability of Solving in Exactly 2 Guesses")
    print(f"{'=' * 62}")
    print(f"Total solutions (N): {N}")
    print(f"Computing feedback for every (guess, secret) pair …\n")

    start = time.time()

    num_patterns = np.zeros(N, dtype=np.int32)   # distinct non-green patterns per guess

    for gi in range(N):
        hashes = compute_feedback(encoded[gi], encoded)
        unique = np.unique(hashes)
        num_patterns[gi] = len(unique) - int(ALL_GREEN_HASH in unique)

        if (gi + 1) % 2000 == 0:
            elapsed = time.time() - start
            eta = elapsed / (gi + 1) * (N - gi - 1)
            best_so_far = np.argmax(num_patterns[: gi + 1])
            print(f"  {gi+1:>6}/{N}  ({(gi+1)/N*100:5.1f}%)  "
                  f"elapsed {elapsed:6.1f}s  ETA {eta:5.0f}s  "
                  f"best so far: {solutions[best_so_far]} "
                  f"({num_patterns[best_so_far]} patterns)")

    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s.\n")

    # ------------------------------------------------------------------
    # Derive probabilities
    # ------------------------------------------------------------------
    p_solve2 = num_patterns / N                       # per-guess probability
    order    = np.argsort(-p_solve2)                   # best first

    best_idx  = order[0]
    worst_idx = order[-1]
    avg_p     = float(p_solve2.mean())
    median_p  = float(np.median(p_solve2))

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    print(f"{'=' * 62}")
    print(f"RESULTS")
    print(f"{'=' * 62}\n")

    print(f"P(solve in 1 guess) = 1/{N} = {1/N:.8f}  ({100/N:.6f}%)\n")

    print(f"Best first guess:  {solutions[best_idx]}")
    print(f"  Distinct patterns: {num_patterns[best_idx]}")
    print(f"  P(solve in 2)    = {num_patterns[best_idx]}/{N}"
          f" = {p_solve2[best_idx]:.6f}  ({p_solve2[best_idx]*100:.4f}%)\n")

    print(f"Average P(solve in 2) over all first guesses:"
          f" {avg_p:.6f}  ({avg_p*100:.4f}%)")
    print(f"Median  P(solve in 2): {median_p:.6f}  ({median_p*100:.4f}%)")
    print(f"Worst   P(solve in 2): {p_solve2[worst_idx]:.6f}"
          f"  ({p_solve2[worst_idx]*100:.4f}%)  — guess: {solutions[worst_idx]}\n")

    # Top 20
    print(f"{'Rank':>4}  {'First Guess':<12}  {'Patterns':>8}  {'P(solve=2)':>12}")
    print(f"{'----':>4}  {'----------':<12}  {'--------':>8}  {'----------':>12}")
    for rank, idx in enumerate(order[:20], 1):
        print(f"{rank:4d}  {solutions[idx]:<12}  {num_patterns[idx]:8d}"
              f"  {p_solve2[idx]:12.6f}")

    # Bottom 5
    print(f"\nWorst 5 first guesses:")
    for rank, idx in enumerate(order[-5:][::-1], 1):
        print(f"  {rank}. {solutions[idx]:<12}  {num_patterns[idx]:4d} patterns"
              f"  P = {p_solve2[idx]:.6f}")

    # Save CSV
    csv_path = os.path.join(script_dir, "nerdle_results_full.csv")
    with open(csv_path, "w") as f:
        f.write("rank,guess,num_patterns,p_solve_in_2\n")
        for rank, idx in enumerate(order, 1):
            f.write(f"{rank},{solutions[idx]},{num_patterns[idx]},"
                    f"{p_solve2[idx]:.8f}\n")
    print(f"\nFull ranked results saved to {csv_path}")


if __name__ == "__main__":
    main()
