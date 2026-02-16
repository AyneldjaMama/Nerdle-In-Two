# The Probability of Solving Nerdle in Exactly Two Guesses

> **TL;DR:** The best opening guess in Nerdle is `52-34=18`, giving you a **9.60%** chance of solving in exactly two guesses — nearly double the 5.66% average.
> **Paper:** [doi.org/10.5281/zenodo.18653848](https://doi.org/10.5281/zenodo.18653848)

## Introduction

A comprehensive analysis was conducted to determine the probability of solving the daily Nerdle puzzle in exactly two guesses. This report details the methodology used, the key findings, and a statistical breakdown of outcomes based on different strategies for the first guess. The analysis is grounded in the complete set of 17,723 possible solutions for the classic 8-character Nerdle game [1].

## Key Findings

The probability of solving Nerdle in exactly two guesses is highly dependent on the first guess chosen. 

* **With an optimal first guess**, the probability of solving on the second try is **9.60%**.
* **With a random first guess** (chosen from the list of valid solutions), the average probability of solving on the second try is **5.66%**.

For context, the probability of solving on the very first guess is approximately **0.0056%** (1 in 17,723).

| Scenario               | P(Solve in 1) | P(Solve in exactly 2) | P(Solve in ≤ 2) |
|:---------------------- |:------------- |:--------------------- |:--------------- |
| **Best First Guess**   | 0.0056%       | 9.6033%               | 9.6090%         |
| **Random First Guess** | 0.0056%       | 5.6567%               | 5.6623%         |

## Methodology

The calculation hinges on understanding how a first guess narrows down the field of possible solutions. For any given first guess, the game provides a feedback pattern of green, purple, and black squares. This pattern is consistent with a specific subset of the 17,723 total solutions. An optimal player would then make their second guess from this smaller set of remaining candidates.

If a feedback pattern leaves *K* possible solutions, the probability of guessing the correct one on the second try is 1/*K*. The overall probability of solving in two guesses for a given first guess, *G*, is the sum of these probabilities across all possible secret answers (and their resulting patterns).

This can be simplified to a surprisingly elegant formula:

> **P(Solve in 2 | Guess G) = (Number of unique feedback patterns G can produce) / (Total number of solutions)**

This is because for each unique feedback pattern that corresponds to *K* possible solutions, there are *K* chances of encountering that pattern, and each time the chance of success is 1/*K*. The contribution of this entire group of *K* solutions to the total probability is therefore *K* × (1/*K*) / *N* = 1/*N*. Summing this up for every unique pattern gives the formula above.

**Note:** The formula assumes the second guess is chosen uniformly at random from the remaining candidates consistent with the feedback pattern. This is in fact the unique optimal strategy — since the goal is to solve in exactly two and all secrets are equally likely, you must pick a consistent candidate, and they're all equally likely to be correct.

To find the probabilities, a program was developed to perform the following steps:

1. Load the complete list of 17,723 valid Nerdle solutions [2].
2. Iterate through every solution, treating each one as a potential first guess.
3. For each first guess, compare it against all 17,723 secret answers to generate every possible feedback pattern.
4. Count the number of unique, non-winning (i.e., not all-green) feedback patterns for that first guess.
5. Calculate the probability using the formula above.

This exhaustive computation involved analyzing over 314 million guess-solution pairs to determine the effectiveness of every possible first guess.

## Detailed Results

The analysis reveals a significant variation in the quality of first guesses. A good first guess is one that maximizes the number of distinct feedback patterns, thereby partitioning the solution space into the smallest possible buckets.

### Optimal First Guesses

The best possible first guess from the solution set is **`52-34=18`**. This guess can produce 1,702 unique feedback patterns, giving it the highest probability of leading to a solution on the second try.

Below are the top 20 best-performing first guesses.

| Rank | Guess      | # Patterns | P(Solve in 2) |
|:---- |:---------- |:---------- |:------------- |
| 1    | `52-34=18` | 1702       | 9.6033%       |
| 2    | `48-32=16` | 1688       | 9.5243%       |
| 3    | `72-14=58` | 1686       | 9.5131%       |
| 4    | `62-43=19` | 1686       | 9.5131%       |
| 5    | `52-38=14` | 1686       | 9.5131%       |
| 6    | `54-36=18` | 1684       | 9.5018%       |
| 7    | `56-37=19` | 1683       | 9.4961%       |
| 8    | `68-21=47` | 1682       | 9.4905%       |
| 9    | `62-13=49` | 1680       | 9.4792%       |
| 10   | `54-38=16` | 1679       | 9.4736%       |
| 11   | `56-39=17` | 1679       | 9.4736%       |
| 12   | `72-54=18` | 1677       | 9.4623%       |
| 13   | `58-21=37` | 1677       | 9.4623%       |
| 14   | `45-27=18` | 1676       | 9.4566%       |
| 15   | `84-21=63` | 1676       | 9.4566%       |
| 16   | `56-19=37` | 1675       | 9.4510%       |
| 17   | `58-42=16` | 1674       | 9.4454%       |
| 18   | `54-18=36` | 1671       | 9.4284%       |
| 19   | `62-49=13` | 1670       | 9.4228%       |
| 20   | `74-21=53` | 1670       | 9.4228%       |

### Sub-Optimal First Guesses

Conversely, a poor first guess is one that contains many repeated digits or common structures, leading to fewer unique feedback patterns. The worst possible first guess is **`9+9*9=90`**, which generates only 266 unique patterns.

| Rank (from worst) | Guess      | # Patterns | P(Solve in 2) |
|:----------------- |:---------- |:---------- |:------------- |
| 1                 | `9+9*9=90` | 266        | 1.5009%       |
| 2                 | `90-9*9=9` | 270        | 1.5234%       |
| 3                 | `9*9+9=90` | 270        | 1.5234%       |
| 4                 | `11-9-1=1` | 285        | 1.6081%       |
| 5                 | `99/9-9=2` | 293        | 1.6532%       |

### Distribution of First Guess Quality

The quality of first guesses varies widely. The number of distinct patterns a guess can generate ranges from a low of 266 to a high of 1,702, with the average being approximately 1,003 patterns.

| Statistic        | Value  |
|:---------------- |:------ |
| Minimum Patterns | 266    |
| Maximum Patterns | 1702   |
| Average Patterns | 1002.5 |
| Median Patterns  | 1001   |

This distribution shows that while there are exceptionally good and bad first guesses, most fall within a predictable middle range.

## Conclusion

While solving Nerdle in a single guess is a matter of pure luck, the probability of solving it on the second guess can be significantly influenced by strategy. By choosing an optimal first guess like **`52-34=18`**, a player can maximize their chances of a two-guess solution to **9.60%**. This is a substantial improvement over the **5.66%** average probability that results from picking a first guess at random. The key to a powerful first guess is its ability to generate a wide variety of distinct feedback patterns, thus efficiently narrowing down the vast space of possible answers.

## Repository Contents

| File                          | Description                                                                     |
|:----------------------------- |:------------------------------------------------------------------------------- |
| `nerdle_solve_in_2.py`        | Python script that computes probabilities for all 17,723 possible first guesses |
| `NerdleClassicRestricted.txt` | Complete list of valid 8-character Nerdle solutions                             |
| `nerdle_results_full.csv`     | Full ranked results (all 17,723 guesses with pattern counts and probabilities)  |

### Usage

```bash
python3 nerdle_solve_in_2.py
```

Requires Python 3 and NumPy. Runtime is approximately 3–4 minutes on a modern machine.

## Acknowledgments

The analysis, code, and initial write-up were generated by [Manus](https://manus.im), an autonomous AI agent, based on a prompt and conceptual guidance from AyneldjaMama. The solution list comes from [pedrokkrause/Nerdle-Equations](https://github.com/pedrokkrause/Nerdle-Equations).

## References

[1] Nerdle. "Nerdle FAQ." *nerdlegame.com*. https://www.nerdlegame.com/faqs.html

[2] Krause, P. "Nerdle-Equations." *GitHub*. https://github.com/pedrokkrause/Nerdle-Equations
