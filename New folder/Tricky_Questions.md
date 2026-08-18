# MATH-243 Probability — Tricky Question Bank

Built from **Lecture 2**, **Lecture 3 & 4**, **Lecture 5**, and the **1st CT (topicwise solve)**.

> **How to use this:** every answer is collapsed. Attempt the question on paper *first*, commit to a number,
> then click **▶ Answer** to check. The questions are deliberately written so the *obvious* answer is often
> the wrong one — each solution names the trap so you can recognise it under exam pressure.
>
> In VS Code press `Ctrl+Shift+V` for the preview so the collapsible blocks work.

**Contents**

1. [Counting traps](#1-counting-traps)
2. [Sample spaces & classical probability](#2-sample-spaces--classical-probability)
3. [Odds ⇄ probability](#3-odds--probability)
4. [Addition rule, joint probability & tables](#4-addition-rule-joint-probability--tables)
5. [Independent vs mutually exclusive](#5-independent-vs-mutually-exclusive)
6. [Conditional probability](#6-conditional-probability)
7. [Total probability & Bayes](#7-total-probability--bayes)
8. [Repeated trials: binomial, multinomial, wait-for-the-k-th](#8-repeated-trials-binomial-multinomial-wait-for-the-k-th)
9. [Joint distributions & marginals](#9-joint-distributions--marginals)
10. [Spot the error](#10-spot-the-error)
11. [Rapid-fire true/false](#11-rapid-fire-truefalse)
12. [Formula sheet](#12-formula-sheet)

---

## 1. Counting traps

### Q1.1 — the classic "at least" overcount

A group has **6 men and 4 women**. A committee of 5 must contain **at least 1 woman and at least 2 men**.

A student argues: *"Reserve 1 woman (⁴C₁ ways) and 2 men (⁶C₂ ways), then fill the remaining 2 seats freely
from the 7 people left (⁷C₂ ways)"*, getting 4 × 15 × 21 = 1260.

Is 1260 correct? If not, what is the answer and **exactly what went wrong**?

<details>
<summary>▶ Answer</summary>

**1260 is wrong. The answer is 240.**

Split by composition (men, women). The only splits of 5 satisfying both constraints:

| Split | Count |
|---|---|
| 2M, 3W | ⁶C₂ × ⁴C₃ = 15 × 4 = 60 |
| 3M, 2W | ⁶C₃ × ⁴C₂ = 20 × 6 = 120 |
| 4M, 1W | ⁶C₄ × ⁴C₁ = 15 × 4 = 60 |
| **Total** | **240** |

**The trap — "reserve then fill" double counts.** The reserved seats and the free seats are not
distinguishable in the finished committee. The committee {M₁, M₂, M₃, W₁, W₂} is produced once with W₁
reserved and M₁M₂ reserved, again with W₂ reserved, again with M₁M₃ reserved… so the same committee is
counted many times. Note 1260/240 = 5.25 — not an integer, which itself proves the overcount is *uneven*
and cannot be repaired by dividing by a constant.

**Rule:** for "at least" conditions, either (a) enumerate disjoint cases, or (b) use complement counting.
Never "reserve and fill".
</details>

### Q1.2 — when complement counting is *easier*

Same group (6 men, 4 women), committee of 5, but now only **at least 1 woman** is required. One line.

<details>
<summary>▶ Answer</summary>

**246.**

Total committees ¹⁰C₅ = 252. Committees with **no** woman = all 5 from the 6 men = ⁶C₅ = 6.

252 − 6 = **246**

**Why complement works here but not in Q1.1:** "at least 1 woman" has exactly *one* forbidden case (zero
women). "At least 1 woman **and** at least 2 men" has several forbidden cases (0W, 0M, 1M), so casework is
cleaner there.
</details>

### Q1.3 — exactly one vs at least one

From a standard 52-card deck, 5 cards are drawn.

(a) How many hands contain **exactly one ace**?
(b) How many contain **at least one ace**?
(c) A student answers (b) with 4 × ⁵¹C₄ = 999 600. Why is that wrong?

<details>
<summary>▶ Answer</summary>

**(a) ⁴C₁ × ⁴⁸C₄ = 4 × 194 580 = 778 320.**
The ⁴⁸C₄ is the crucial part — the other four cards must come from the **48 non-aces**, otherwise you are
not saying "exactly".

**(b) ⁵²C₅ − ⁴⁸C₅ = 2 598 960 − 1 712 304 = 886 656.**

**(c)** 4 × ⁵¹C₄ picks "an ace", then "any 4 others" — but those 4 others may contain more aces, so a hand
with 2 aces is counted twice (once with each of its aces in the "chosen ace" role), a hand with 3 aces three
times, and so on. Notice 999 600 > 886 656; the overcount is visible.

**Free exam check:** exactly-one (778 320) must be *smaller* than at-least-one (886 656), which must be
smaller than the total number of hands. Any "at least" answer exceeding the complement answer is a red flag.
</details>

### Q1.4 — two routes, one answer

3 cards are drawn from a 52-card deck **one after another without replacement**. Find P(all three from
different suits) **twice** — once with sequential conditional probabilities, once with combinations — and
confirm they agree. *(CT Q7(b)(i))*

<details>
<summary>▶ Answer</summary>

**Both give 169/425 ≈ 0.398.**

*Sequential:* the 1st card can be anything; the 2nd must avoid the 1st card's suit (39 of the 51 left); the
3rd must avoid two suits (26 of 50):

(52/52) × (39/51) × (26/50) = **0.3976**

*Combinations:* choose 3 suits from 4, then one card from each chosen suit:

(⁴C₃ × 13³) / ⁵²C₃ = (4 × 2197)/22 100 = 8788/22 100 = **0.3976**

**Why this matters:** "without replacement" *sounds* like order matters, but if the event itself is
order-free ("they come from different suits"), the combination route is legal too. Two methods agreeing is a
free correctness check; if they disagree, one of them has a hidden ordering assumption.
</details>

### Q1.5 — permutation or combination?

A club has 5 members. (a) Elect a president, vice-president and secretary. (b) Form a 3-member committee.
Same numbers 5 and 3 — why is one answer 60 and the other 10?

<details>
<summary>▶ Answer</summary>

**(a) ⁵P₃ = 5!/2! = 60.  (b) ⁵C₃ = 5!/(3!2!) = 10.**

The three offices are **distinguishable roles**: (A pres, B VP, C sec) ≠ (B pres, A VP, C sec). A committee
has no roles, so all 3! = 6 orderings of {A, B, C} are the *same* committee — hence 60/3! = 10.

**Exam test:** *"if I swap two of the chosen people, is the outcome different?"* Yes → permutation.
No → combination.
</details>

---

## 2. Sample spaces & classical probability

### Q2.1 — "at most" vs "at least"

A couple plans two children, each equally likely B or G. Find P(**at most one boy**) and
P(**at least one girl**). Are they the same event?

<details>
<summary>▶ Answer</summary>

**Both are 3/4, and yes — they are literally the same event.**

S = {BB, BG, GB, GG}.
*At most one boy* (0 or 1 boy) = {GG, BG, GB}.
*At least one girl* = {BG, GB, GG}.

Identical sets. With exactly two children, "at most one boy" ⇔ "not both boys" ⇔ "at least one girl".

**The trap:** reading "at most one boy" as "exactly one boy" (= 1/2). Write out the sample space — with
4 outcomes it costs five seconds.
</details>

### Q2.2 — the boy–girl paradox

Same two-child family. Given that **at least one child is a girl**, what is P(**both** are girls)? Is it 1/2?

<details>
<summary>▶ Answer</summary>

**No — it is 1/3.**

Condition on B = {at least one girl} = {BG, GB, GG}, n(B) = 3. Favourable A∩B = {GG}, n = 1.

P(A|B) = **1/3**

**Why 1/2 feels right and is wrong:** 1/2 answers a *different* question — *"the elder child is a girl; what
is P(the younger is a girl)?"* That conditions on {GB, GG} (2 outcomes) → 1/2. The phrase "at least one"
does **not** identify *which* child is the girl, so three equally likely outcomes stay alive, not two.

This is the single most reliable trick question in an intro probability paper.
</details>

### Q2.3 — compound experiment with an "or" inside

A coin is tossed twice, then a die is rolled once. Find:
(a) P(exactly one head **and** an even number)
(b) P(two tails **or** a number greater than 4)
(c) P(at least one head **and** an odd number) *(Lecture 2 exercise)*

<details>
<summary>▶ Answer</summary>

Coin part and die part are independent, so you may multiply — but only after handling the "or" correctly.

**(a)** P(exactly one head) = 2/4 = 1/2; P(even) = 3/6 = 1/2 → 1/2 × 1/2 = **1/4**

**(b)** This is a **union**, not a product. P(TT) = 1/4, P(die > 4) = 2/6 = 1/3, independent so
P(both) = 1/12:

P = 1/4 + 1/3 − 1/12 = 3/12 + 4/12 − 1/12 = **1/2**

**(c)** P(at least one head) = 3/4; P(odd) = 1/2 → 3/4 × 1/2 = **3/8**

**The trap in (b):** answering 1/4 × 1/3 = 1/12. The word *or*, in a problem where both parts can happen
together, **always** needs the −P(A∩B) correction. Multiplication is for *and*.
</details>

### Q2.4 — three tosses

A fair coin is tossed three times. Find P(exactly two heads) and P(at most one head).

<details>
<summary>▶ Answer</summary>

S has 2³ = 8 equally likely outcomes.

**Exactly two heads:** {HHT, HTH, THH} → **3/8**
**At most one head** (0 or 1): {TTT, HTT, THT, TTH} → 4/8 = **1/2**

Note "at most one head" = "at least two tails" — another same-event pair worth spotting. Symmetry check:
for three fair tosses P(≤1 head) = P(≥2 heads) = 1/2.
</details>

### Q2.5 — are these equally likely?

A bag has 4 white and 6 red balls; one ball is drawn — are "red" and "white" equally likely? A die is rolled
— are "even" and "greater than 4" equally likely? Are "even" and "odd" equally likely?

<details>
<summary>▶ Answer</summary>

- **Bag:** P(R) = 6/10 = 3/5, P(W) = 4/10 = 2/5 → **not** equally likely.
- **Die, even vs > 4:** P(even) = 3/6 = 1/2, P(>4) = P({5,6}) = 2/6 = 1/3 → **not** equally likely.
- **Die, even vs odd:** 3/6 = 3/6 → **equally likely**.

**The trap:** "equally likely" is a claim about **numerically equal probabilities**, not about the events
being the same *kind* of thing or being described with the same number of words. Compute both, compare.
</details>

---

## 3. Odds ⇄ probability

### Q3.1 — the direction trap

The odds **against** student X solving a problem are **8 : 6**, and the odds **in favour** of student Y
solving it are **14 : 16**. Find P(X solves) and P(Y solves). *(Lecture 3, Problem 1)*

<details>
<summary>▶ Answer</summary>

**P(X) = 6/14 = 3/7  and  P(Y) = 14/30 = 7/15.**

Odds **against** A = n(Aᶜ) : n(A) — the *failure* count comes **first**. So "8 : 6 against" means 8 ways to
fail, 6 ways to succeed, total 14:

P(X) = 6/14 = **3/7**,  P(Xᶜ) = 8/14 = 4/7

Odds **in favour** of A = n(A) : n(Aᶜ) — success first:

P(Y) = 14/(14+16) = **7/15**,  P(Yᶜ) = 16/30 = 8/15

**The trap:** writing P(X) = 8/14. Every downstream part of the question then fails. Whenever you see
"odds", immediately write out which number is success and which is failure before touching anything else.
</details>

### Q3.2 — odds are not a probability

The probability an athlete wins a race is 0.2. What are the odds **against** winning? Is the answer 0.8?

<details>
<summary>▶ Answer</summary>

**No. The odds against are 4 : 1 (i.e. 4), not 0.8.**

Odds against W = P(Wᶜ)/P(W) = 0.8/0.2 = **4** → "4 to 1".

Interpretation: for every 1 chance the athlete wins, there are 4 chances they do not.

**The trap:** 0.8 is the *probability* of losing. Odds are a **ratio of two probabilities** and can exceed 1;
a probability never can. If your "odds" answer is between 0 and 1 and you were asked for odds *against* a
likely-to-fail event, re-read.
</details>

### Q3.3 — a disguised equality

Odds **in favour** of A are 2 : 3. Odds **against** B are 3 : 2. Is P(A) = P(B)?

<details>
<summary>▶ Answer</summary>

**Yes — both equal 2/5.**

- In favour of A = 2 : 3 → P(A) = 2/(2+3) = 2/5.
- Against B = 3 : 2 → failure : success = 3 : 2 → P(B) = 2/(3+2) = 2/5.

**The point:** "in favour a : b" and "against b : a" are the *same statement*. Odds in favour and odds
against are always reciprocals of each other, so a question can hide identical information behind opposite
phrasings.
</details>

### Q3.4 — the full independent-workers chain

With P(X) = 3/7 and P(Y) = 7/15 as in Q3.1, and X, Y working **independently**, find:
(a) both solve, (b) neither solves, (c) at least one solves, (d) either X or Y solves, (e) exactly one solves.

<details>
<summary>▶ Answer</summary>

| Part | Working | Answer |
|---|---|---|
| (a) both | (3/7)(7/15) | **1/5 = 21/105** |
| (b) neither | (4/7)(8/15) | **32/105** |
| (c) at least one | 1 − P(neither) | **73/105** |
| (d) either X or Y | same as (c) | **73/105** |
| (e) exactly one | P(at least one) − P(both) = 73/105 − 21/105 | **52/105** |

**Two traps here:**

1. **(c) and (d) are the same number.** In probability, "either … or …" is *inclusive* — it allows both.
   Only "exactly one" excludes the both-case. Many students give 52/105 for (d).
2. **(b) via De Morgan:** P(neither) = P(Xᶜ ∩ Yᶜ) = P((X∪Y)ᶜ) = 1 − P(X∪Y). Both routes must agree:
   1 − 73/105 = 32/105 ✓.

Alternative route for (e): P(X∩Yᶜ) + P(Xᶜ∩Y) = (3/7)(8/15) + (4/7)(7/15) = 24/105 + 28/105 = 52/105 ✓
</details>

### Q3.5 — same story, dependence switched on

Same odds as above, but now: **if X solves the problem, the probability Y also solves it is 60%.**
Redo (a)–(e). Which answers change, and does "at least one" go up or down? *(Lecture 3, Problem 2)*

<details>
<summary>▶ Answer</summary>

Now P(Y|X) = 3/5, so **P(X∩Y) = P(X)·P(Y|X) = (3/7)(3/5) = 9/35 = 27/105** (was 21/105).

| Part | Working | Answer |
|---|---|---|
| (a) both | (3/7)(3/5) | **9/35 = 27/105** |
| (b) neither | 1 − P(X∪Y) | **38/105** |
| (c) at least one | 3/7 + 7/15 − 9/35 = 45/105 + 49/105 − 27/105 | **67/105** |
| (d) either | same as (c) | **67/105** |
| (e) exactly one | 67/105 − 27/105 | **40/105 = 8/21** |

**"At least one" went DOWN** (73/105 → 67/105) even though the two are now *positively* correlated. That is
the whole insight: positive dependence piles probability onto the "both" corner and takes it away from the
"exactly one" corners, so the union shrinks.

**The trap:** you may **not** use P(neither) = P(Xᶜ)P(Yᶜ) here — that formula needs independence. You must
go through P(X∪Y) = P(X) + P(Y) − P(X∩Y) first, then complement. Using (4/7)(8/15) = 32/105 would be wrong.
</details>

---

## 4. Addition rule, joint probability & tables

### Q4.1 — the newspaper table

In an office of 100 employees, 75 read English dailies, 50 read Bangla dailies, 40 read both. One employee is
chosen at random. Find P(reads English), P(reads at least one), P(reads none), P(reads Bangla but not
English). *(Lecture 4, Problem 1)*

<details>
<summary>▶ Answer</summary>

Build the 2×2 table first — it makes every part a lookup:

|  | E | Eᶜ | Total |
|---|---|---|---|
| **B** | 40 | 10 | 50 |
| **Bᶜ** | 35 | 15 | 50 |
| **Total** | 75 | 25 | 100 |

- P(E) = 75/100 = **0.75**
- P(E∪B) = 0.75 + 0.50 − 0.40 = **0.85**
- P(none) = P((E∪B)ᶜ) = 1 − 0.85 = **0.15**
- P(B ∩ Eᶜ) = P(B) − P(B∩E) = 0.50 − 0.40 = **0.10**

**The trap:** "reads Bangla but not English" is *not* P(B)·P(Eᶜ) = 0.5 × 0.25 = 0.125. Subtract the overlap;
never multiply unless you have *proved* independence. (Here 0.40 ≠ 0.75 × 0.50 = 0.375, so E and B are in
fact dependent and the product would be wrong anyway.)
</details>

### Q4.2 — working backwards from "neither"

At a women's college 60% wear **neither** a ring nor a necklace, 20% wear a ring, 30% wear a necklace. Find
P(ring or necklace) and P(both). Then decide whether "ring" and "necklace" are independent.
*(Lecture 4, Problem 2)*

<details>
<summary>▶ Answer</summary>

P(R∪N) = 1 − P(neither) = 1 − 0.60 = **0.40**

Then invert the addition rule:

P(R∩N) = P(R) + P(N) − P(R∪N) = 0.20 + 0.30 − 0.40 = **0.10**

**Independent?** P(R)·P(N) = 0.20 × 0.30 = 0.06 ≠ 0.10 = P(R∩N) → **not independent** (positively
associated: ring-wearers are likelier than average to wear a necklace).

**The trap:** the addition rule is usually run forwards to find the union. Here you are *given* the union
(through its complement) and must run it **backwards** to get the intersection. Recognising which quantity is
missing is the whole question.
</details>

### Q4.3 — a union that quietly hides independence

A class has 10 men and 20 women; **half of the men and half of the women** have brown eyes. One person is
chosen at random. Find P(man **or** brown eyes). Then check: are "man" and "brown eyes" independent?
*(Lecture 4, Problem 3)*

<details>
<summary>▶ Answer</summary>

|  | Man (M) | Woman (W) | Total |
|---|---|---|---|
| **Brown (B)** | 5 | 10 | 15 |
| **Not brown** | 5 | 10 | 15 |
| **Total** | 10 | 20 | 30 |

P(M∪B) = P(M) + P(B) − P(M∩B) = 10/30 + 15/30 − 5/30 = 20/30 = **2/3**

**Independent? Yes.** P(M)·P(B) = (1/3)(1/2) = 1/6 = 5/30 = P(M∩B) ✓

The phrase "**half** of the men and **half** of the women" is exactly what forces independence: eye colour
carries no information about sex. Had it said "half the men and one-third of the women", they would be
dependent and P(M∪B) would change.

**The trap:** answering 10/30 + 15/30 = 25/30 by forgetting the overlap. The 5 brown-eyed men would be
counted twice.
</details>

### Q4.4 — the studies problem

60% of students study Mathematics, 50% study Physics, 30% study both. Find P(M or P), P(M but not P),
P(neither). Bonus: are M and P independent? *(Lecture 3, Problem 1)*

<details>
<summary>▶ Answer</summary>

- P(M∪P) = 0.6 + 0.5 − 0.3 = **0.8**
- P(M ∩ Pᶜ) = P(M) − P(M∩P) = 0.6 − 0.3 = **0.3**
- P(neither) = 1 − 0.8 = **0.2**

**Bonus — yes, independent:** P(M)P(P) = 0.6 × 0.5 = 0.30 = P(M∩P) ✓

**Worth noticing:** the lecture never mentions it, but this data set *is* independent, which is why
P(M|P) = 0.3/0.5 = 0.6 = P(M). Contrast with Q4.2, where superficially similar data was dependent — you
cannot tell by looking, only by multiplying.
</details>

### Q4.5 — building a joint table from conditional information

Machine A makes 40% of items, Machine B makes 60%. 5% of A's items and 10% of B's items are defective.
Build the joint probability table, then find P(defective), P(from A | defective), and P(non-defective and
from B). *(Lecture 4, Problem 4)*

<details>
<summary>▶ Answer</summary>

Every cell is P(machine) × P(defect status | machine):

|  | Defective | Not defective | Total |
|---|---|---|---|
| **A** | 0.4 × 0.05 = 0.02 | 0.4 × 0.95 = 0.38 | 0.40 |
| **B** | 0.6 × 0.10 = 0.06 | 0.6 × 0.90 = 0.54 | 0.60 |
| **Total** | **0.08** | 0.92 | 1.00 |

- P(defective) = 0.02 + 0.06 = **0.08**
- P(A | defective) = 0.02/0.08 = **0.25**
- P(not defective ∩ B) = **0.54**

**The trap:** the given percentages 5% and 10% are **conditional** (P(D|A), P(D|B)), not joint. Writing
P(D) = 0.05 + 0.10 = 0.15, or averaging them to 0.075, are both wrong — you must weight by 0.4 and 0.6.
Also note P(A|D) = 0.25 while P(D|A) = 0.05; these are different questions (see §7).
</details>

---

## 5. Independent vs mutually exclusive

### Q5.1 — the concept everybody mixes up

A and B are mutually exclusive, with P(A) > 0 and P(B) > 0. Can they also be independent? Prove your answer.

<details>
<summary>▶ Answer</summary>

**No — never.**

Mutually exclusive ⇒ A∩B = ∅ ⇒ P(A∩B) = 0.
Independent ⇒ P(A∩B) = P(A)P(B) > 0, since both factors are positive.

0 > 0 is a contradiction, so the two properties are incompatible whenever both events have positive
probability.

**Intuition:** mutually exclusive events are maximally *dependent* — knowing A occurred tells you B
definitely did **not**. That is the opposite of "no information".

(Edge case worth knowing: if P(A) = 0, then A is both mutually exclusive with B and independent of it —
trivially. Exams occasionally probe this.)
</details>

### Q5.2 — the same-word, different-rule trap

For each pair, say which formula applies and compute.

(a) P(A) = 0.4, P(B) = 0.5, A and B **mutually exclusive** → P(A∪B)? P(A∩B)?
(b) P(A) = 0.4, P(B) = 0.5, A and B **independent** → P(A∪B)? P(A∩B)?

<details>
<summary>▶ Answer</summary>

**(a) Mutually exclusive:** P(A∩B) = **0**, so P(A∪B) = 0.4 + 0.5 − 0 = **0.9**

**(b) Independent:** P(A∩B) = 0.4 × 0.5 = **0.20**, so P(A∪B) = 0.4 + 0.5 − 0.2 = **0.70**

**The trap:** both words start with a vague "the events don't interfere" feeling, but they control *different*
formulas:

- *Mutually exclusive* → controls the **intersection** (it is 0), which simplifies the **addition** rule.
- *Independent* → controls the **multiplication** rule (P(A∩B) = P(A)P(B)).

Never use P(A∪B) = P(A) + P(B) unless disjointness is *given* or *proved*.
</details>

### Q5.3 — the problem-solving trio

P(A solves) = 3/7, P(B solves) = 2/3, P(C solves) = 4/5, all independent. Find P(problem is solved).
*(CT Q7(b)(ii))*

<details>
<summary>▶ Answer</summary>

**101/105 ≈ 0.962**

"Solved" = at least one of them solves it. Go through the complement:

P(none solves) = (4/7)(1/3)(1/5) = 4/105
P(solved) = 1 − 4/105 = **101/105**

**The trap:** adding 3/7 + 2/3 + 4/5 = 1.876 > 1. Any probability above 1 means you added overlapping events.
With three events the inclusion–exclusion correction has 4 extra terms; the complement route has one term.
Always take the complement for "at least one of several independent events".
</details>

### Q5.4 — reliability of a circuit

A circuit works iff there is a path of functional devices from left to right. Four parallel branches connect
the two sides: a **top** branch with one device (failure probability 0.02), **two middle** branches each with
two devices in series (each device fails with probability 0.01), and a **bottom** branch with one device
(0.02). Devices fail independently. Find P(the circuit does **not** operate). *(CT Q7(a))*

<details>
<summary>▶ Answer</summary>

**≈ 1.584 × 10⁻⁷**

Two levels of reasoning:

1. **A series branch fails** if *either* of its devices fails: P(branch works) = 0.99² = 0.9801, so
   P(branch fails) = 1 − 0.99² = 0.0199.
2. **A parallel system fails** only if *every* branch fails:

P(circuit fails) = 0.02 × (1 − 0.99²) × (1 − 0.99²) × 0.02 = 0.02 × 0.0199 × 0.0199 × 0.02
= **1.584 × 10⁻⁷**

So P(circuit operates) ≈ 0.99999984.

**The trap:** flipping series and parallel logic. Remember the direction:
- **Series** = all needed → multiply the *working* probabilities.
- **Parallel** = one is enough → multiply the *failure* probabilities.

A parallel system is *more* reliable than any single branch; a series system is *less* reliable than any
single component. If your "fails" answer for a parallel bank is bigger than one branch's failure
probability, you have swapped them.
</details>

---

## 6. Conditional probability

### Q6.1 — the reduced sample space

A pair of dice is thrown. Find P(sum ≥ 10 | a 5 appears on the first die). *(Lecture 5, Problem 1)*

<details>
<summary>▶ Answer</summary>

**1/3**

B = {first die is 5} = {(5,1) … (5,6)}, n(B) = 6.
A = {sum ≥ 10} = {(4,6), (5,5), (5,6), (6,4), (6,5), (6,6)}, n(A) = 6.
A∩B = {(5,5), (5,6)}, n = 2.

P(A|B) = (2/36)/(6/36) = **2/6 = 1/3**

**Shortcut (valid-space method):** once you know the first die is 5, the only randomness left is the second
die; you need it to be 5 or 6 → 2/6 = 1/3. No 36-outcome table required.

**The trap:** answering 6/36 = 1/6, i.e. ignoring the condition entirely; or answering 2/36 by forgetting to
divide by P(B). Conditioning **shrinks the denominator** — that is its whole mechanical effect.
</details>

### Q6.2 — a non-uniform sample space

A coin is tossed until a head appears, or until it has been tossed three times. Given that no head appears on
the first toss, what is P(the coin is tossed three times)? *(Lecture 5, Problem 3)*

<details>
<summary>▶ Answer</summary>

**1/2**

S = {H, TH, TTH, TTT} with **unequal** probabilities: P(H) = 1/2, P(TH) = 1/4, P(TTH) = 1/8, P(TTT) = 1/8.

A = {tossed 3 times} = {TTH, TTT} → P(A) = 1/8 + 1/8 = 1/4
B = {no head on 1st toss} = {TH, TTH, TTT} → P(B) = 1/4 + 1/8 + 1/8 = 1/2
A∩B = {TTH, TTT} → P(A∩B) = 1/4

P(A|B) = (1/4)/(1/2) = **1/2**

**The trap:** counting outcomes instead of adding probabilities. "n(A∩B)/n(B) = 2/3" is wrong here, because
the four outcomes in S are **not equally likely**. The counting formula n(A)/n(S) is a *special case* that
requires equal likelihood; the ratio-of-probabilities definition always works.

**Shortcut:** after a first-toss tail, you are simply asking "does the experiment continue past toss 2?",
which happens iff toss 2 is a tail → 1/2.
</details>

### Q6.3 — the picnic Venn puzzle

20 students went on a picnic. 5 got sunburnt, 8 got bitten by mosquitoes, and 10 returned home safely with no
mishap. Find (i) P(a sunburnt boy was ignored by mosquitoes), (ii) P(a mosquito-bitten boy also got
sunburnt). *(CT Q6(b))*

<details>
<summary>▶ Answer</summary>

**First you must *derive* the overlap** — it is not given.

10 returned safely, so 10 had **at least one** mishap: n(A∪B) = 10.
n(A∪B) = n(A) + n(B) − n(A∩B) → 10 = 5 + 8 − n(A∩B) → **n(A∩B) = 3**

Venn: sunburnt only = 2, both = 3, bitten only = 5, neither = 10. Total 2+3+5+10 = 20 ✓

**(i)** P(not bitten | sunburnt) = n(A ∩ Bᶜ)/n(A) = 2/5 = **0.4**
**(ii)** P(sunburnt | bitten) = n(A∩B)/n(B) = 3/8 = **0.375**

**Two traps:**
1. Assuming 5 + 8 = 13 students had mishaps and 7 were safe — contradicting the given 10. The "10 safe" is
   what *pins down* the overlap.
2. Answering (i) and (ii) with the same denominator. Read which event is *given*: it goes in the denominator.
   (i) conditions on sunburnt (denominator 5); (ii) conditions on bitten (denominator 8).
</details>

### Q6.4 — the TV show, consistent version

P(a married man watches a show) = 0.4, P(his wife watches) = 0.5, P(man watches | wife watches) = 0.7. Find:
(a) P(couple both watch), (b) P(wife watches | husband watches), (c) P(at least one watches).
*(Lecture 5, Problem 2)*

<details>
<summary>▶ Answer</summary>

**(a)** P(H∩W) = P(W)·P(H|W) = 0.5 × 0.7 = **0.35**

**(b)** P(W|H) = P(H∩W)/P(H) = 0.35/0.40 = **0.875**

**(c)** P(H∪W) = 0.40 + 0.50 − 0.35 = **0.55**

**The trap in (a):** multiplying by the wrong marginal. P(H|W) is "H given W", so it pairs with **P(W)**:
P(H∩W) = P(W)·P(H|W). Using P(H) × P(H|W) = 0.28 is a classic slip.

**Note (b) ≠ 0.7.** P(H|W) = 0.7 but P(W|H) = 0.875 — conditional probability is **not symmetric**. Keep this
in mind for §7.
</details>

### Q6.5 — the TV show, poisoned version ⚠️ *the best trick in the CT*

P(a married man watches) = **0.25**, P(a married woman watches) = **0.35**, P(man watches | wife watches) =
**0.8**. Find (i) P(the couple watches), (ii) P(husband watches | wife does **not** watch). *(CT Q8(a))*

<details>
<summary>▶ Answer</summary>

**(i)** P(H∩W) = P(W)·P(H|W) = 0.35 × 0.8 = **0.28**

**(ii) is impossible — the data given in the question is inconsistent.**

P(H | Wᶜ) = P(H ∩ Wᶜ)/P(Wᶜ) = [P(H) − P(H∩W)] / [1 − P(W)] = (0.25 − 0.28)/0.65 = **−0.046**

A negative probability is impossible. The culprit: **P(H∩W) = 0.28 > P(H) = 0.25**, but an intersection can
never be larger than either of its parts:

P(A∩B) ≤ min{P(A), P(B)}

Equivalently, the given P(H|W) = 0.8 is impossible: consistency requires
P(H|W) ≤ P(H)/P(W) = 0.25/0.35 = 0.714.

**How to answer this in an exam:** do the computation, get the negative number, and *state explicitly* that
the data violates P(A∩B) ≤ min{P(A), P(B)} — so no valid answer exists. Do **not** silently flip the sign to
0.046 and move on. (If you are asked to salvage it, note that any P(H|W) ≤ 0.714 makes the problem
well-posed; e.g. Q6.4 is the healthy version of the same story.)

**Quick sanity checks worth running on every conditional-probability problem:**
- P(A∩B) ≤ min{P(A), P(B)}
- P(A∪B) ≥ max{P(A), P(B)} and P(A∪B) ≤ 1
- every conditional probability lies in [0, 1]
</details>

### Q6.6 — a conditional that is handed to you

In a community there are equal numbers of males and females. 5% of the males and 2% of the females are
disabled. A person is chosen at random. **If this person is male**, what is the probability they are
disabled? *(Lecture 5, Problem 4)*

<details>
<summary>▶ Answer</summary>

**0.05 — the answer was in the question.**

P(D|M) = P(D∩M)/P(M) = (0.05 × 0.5)/0.5 = 0.025/0.5 = **0.05**

"5% of the **males** are disabled" *is* P(D|M) by definition. All the arithmetic cancels.

**Why the question is still worth doing:** it trains you to distinguish the three quantities that this data
supports —

- P(D|M) = 0.05 (given directly)
- P(D∩M) = 0.025 (a *joint*: "male **and** disabled")
- P(D) = 0.05(0.5) + 0.02(0.5) = 0.035 (total probability)
- P(M|D) = 0.025/0.035 = 0.714 (Bayes — the *reverse* conditional)

Notice how different P(D|M) = 0.05 and P(M|D) = 0.714 are. If you can compute all four from one data set,
you understand the chapter.
</details>

---

## 7. Total probability & Bayes

### Q7.1 — the transferred-ball problem

Bag 1 holds **4 white and 3 black** balls; bag 2 holds **3 white and 5 black**. One ball is drawn from bag 1
and placed **unseen** into bag 2. What is P(a ball now drawn from bag 2 is black)? *(CT Q1(a))*

<details>
<summary>▶ Answer</summary>

**38/63 ≈ 0.603**

Condition on the colour of the transferred ball — you do not know it, so both branches live:

- Transferred **black** (prob 3/7): bag 2 becomes 3W + 6B = 9 balls → P(black) = 6/9
- Transferred **white** (prob 4/7): bag 2 becomes 4W + 5B = 9 balls → P(black) = 5/9

P(black) = (3/7)(6/9) + (4/7)(5/9) = 18/63 + 20/63 = **38/63**

**Two traps:**
1. **Forgetting the transfer changed the count.** Bag 2 now has **9** balls, not 8. Both denominators must
   become 9.
2. **"Unseen" means you must average over both cases.** The word "unseen" is the examiner telling you to use
   the law of total probability. If the ball's colour had been observed, only one branch would survive.

**Check:** P(white) = (3/7)(3/9) + (4/7)(4/9) = 9/63 + 16/63 = 25/63, and 38/63 + 25/63 = 1 ✓
</details>

### Q7.2 — three machines (the standard Bayes drill)

Machines B₁, B₂, B₃ make 30%, 45% and 25% of the products; 2%, 3% and 2% of their output is defective
respectively. A randomly selected finished product is found **defective**. Find P(Bᵢ | defective) for
i = 1, 2, 3. *(CT Q1(b))*

<details>
<summary>▶ Answer</summary>

**Step 1 — total probability (the denominator):**

P(D) = 0.30(0.02) + 0.45(0.03) + 0.25(0.02) = 0.006 + 0.0135 + 0.005 = **0.0245**

**Step 2 — Bayes for each:**

| Machine | Joint P(Bᵢ ∩ D) | P(Bᵢ \| D) |
|---|---|---|
| B₁ | 0.006 | 0.006/0.0245 = **0.2449 (24.49%)** |
| B₂ | 0.0135 | 0.0135/0.0245 = **0.5510 (55.10%)** |
| B₃ | 0.005 | 0.005/0.0245 = **0.2041 (20.41%)** |

**Sum = 1.0000 ✓** — always check this; it catches arithmetic slips instantly.

**The insight:** B₂ is blamed for 55% of defectives despite making only 45% of output, because its defect
*rate* is highest. B₁ and B₃ have the *same* defect rate (2%), so their posteriors are in exactly the ratio
of their production shares, 30 : 25.
</details>

### Q7.3 — the truth serum (prosecutor's fallacy)

A truth serum correctly identifies 90% of guilty suspects (10% of the guilty are wrongly found innocent), and
misjudges innocent suspects 1% of the time. Only 5% of the suspect pool has ever committed a crime. The serum
says a suspect is **guilty** — what is P(they are actually **innocent**)? *(CT Q7(a))*

<details>
<summary>▶ Answer</summary>

**19/109 ≈ 0.174, i.e. about 17.4%**

P(innocent ∩ judged guilty) = 0.95 × 0.01 = 0.0095
P(guilty ∩ judged guilty) = 0.05 × 0.90 = 0.0450
P(judged guilty) = 0.0545

P(innocent | judged guilty) = 0.0095/0.0545 = **0.174**

**The trap (the prosecutor's fallacy):** "the test is 99% accurate on innocent people, so a guilty verdict
means only 1% chance of innocence." That statement confuses **P(judged guilty | innocent) = 0.01** with
**P(innocent | judged guilty) = 0.174** — a factor of 17 apart.

**Why:** innocents are 19× more numerous than the guilty (95% vs 5%). Even a small 1% error rate applied to a
huge innocent pool produces a lot of false accusations (0.0095) compared with the true accusations (0.045).
Base rates dominate.
</details>

### Q7.4 — the medical test (same trap, different clothes)

A blood test detects a disease in 90% of people who have it, but gives a false positive for 5% of healthy
people. 1% of the population has the disease. A random person tests **positive**. What is P(they have the
disease)? *(Lecture 5, Bayes Problem 1)*

<details>
<summary>▶ Answer</summary>

**≈ 0.1538, about 15.4%**

P(D∩+) = 0.01 × 0.90 = 0.0090
P(Dᶜ∩+) = 0.99 × 0.05 = 0.0495
P(+) = 0.0585

P(D|+) = 0.0090/0.0585 = **0.1538**

**The headline:** a "90% effective" test, on a positive result, still leaves you **85% likely to be healthy**.
Among 10 000 people: 100 sick (90 detected) vs 9 900 healthy (495 false positives). 90 out of 585 positives
are real → 15.4%.

**Compare with Q7.3:** identical structure, and both punish the same instinct. When the base rate is small,
the false positives from the big healthy group swamp the true positives from the small sick group. This is
why real screening programmes retest.
</details>

### Q7.5 — Bayes with a coin choosing the urn

Container 1 has 2 white and 7 black balls; container 2 has 5 white and 6 black. A fair coin is flipped: heads
→ draw from container 1, tails → container 2. A **white** ball is drawn. What is P(the coin came up heads)?
*(Lecture 5, Bayes Problem 2)*

<details>
<summary>▶ Answer</summary>

**22/67 ≈ 0.328**

P(H∩W) = (1/2)(2/9) = 1/9
P(T∩W) = (1/2)(5/11) = 5/22
P(W) = 1/9 + 5/22 = 22/198 + 45/198 = 67/198

P(H|W) = (1/9)/(67/198) = (22/198)/(67/198) = **22/67**

**The insight:** the prior was 1/2, and a white ball drags it **down** to 0.328, because container 2 is much
richer in white (5/11 = 0.455 vs 2/9 = 0.222). Evidence moves the prior toward whichever hypothesis explains
it better.

**The trap:** the two containers have **different totals** (9 vs 11). Writing 2/9 and 5/9 (or 2/11 and 5/11)
because "they should match" wrecks the answer. Always recount each container.
</details>

### Q7.6 — the commuter (three-branch Bayes)

A person drives 30% of the time, walks 30%, takes the bus 40%. He is late 3% of the time when driving, 10%
when walking, 7% when taking the bus. (i) P(late)? (ii) P(bus | late)? (iii) P(car | late)?
*(Lecture 5, Problem 3 exercise)*

<details>
<summary>▶ Answer</summary>

**(i)** P(L) = 0.30(0.03) + 0.30(0.10) + 0.40(0.07) = 0.009 + 0.030 + 0.028 = **0.067**

**(ii)** P(bus|L) = 0.028/0.067 = **0.4179 (41.79%)**

**(iii)** P(car|L) = 0.009/0.067 = **0.1343 (13.43%)**

(For completeness P(walk|L) = 0.030/0.067 = 0.4478; the three sum to 1.0000 ✓)

**Notice:** walking is the biggest single cause of lateness (44.8%) even though he walks only 30% of the time,
because its lateness *rate* is the worst. Driving is used just as often as walking but explains only 13% of
late days.

**The trap:** 3% + 10% + 7% = 20%, or averaging to 6.67%. Neither is P(late) — the rates must be weighted by
how often each mode is used.
</details>

### Q7.7 — screening methods

A clinic uses a blood test for 40% of patients, an imaging scan for 35%, and a physical exam for 25%. For a
patient who genuinely has the condition, detection probabilities are 80% (blood), 70% (imaging), 90%
(physical). (i) P(a patient who has the condition is detected)? (ii) P(physical exam | detected)?
(iii) P(blood test | detected)? *(Lecture 5, Problem 4 exercise)*

<details>
<summary>▶ Answer</summary>

**(i)** P(detect) = 0.40(0.80) + 0.35(0.70) + 0.25(0.90) = 0.32 + 0.245 + 0.225 = **0.79**

**(ii)** P(physical | detected) = 0.225/0.79 = **0.2848 (28.48%)**

**(iii)** P(blood | detected) = 0.32/0.79 = **0.4051 (40.51%)**

(Imaging: 0.245/0.79 = 0.3101; the three sum to 1 ✓)

**The subtle wording:** every probability here is *already conditioned on the patient having the condition*.
So 0.79 is **P(detected | has condition)**, not P(detected) in the whole population — you were not told the
prevalence, so a population-level answer is impossible. Examiners like hiding an extra layer of conditioning
in one clause.

**Bonus:** Lecture 5's Problem 5 (books 40% / video 35% / group study 25%, passing 80% / 70% / 90%) is
numerically **identical** to this one — P(pass) = 0.79, P(group|pass) = 0.2848, P(books|pass) = 0.4051. If you
solved one, you have solved both.
</details>

### Q7.8 — the health-centre variant

Centre A tests 50% of patients, B 20%, C 30%. Among patients who have the disease, positive rates are 2% (A),
12% (B), 6% (C). (i) P(positive)? (ii) P(tested at Centre B | positive)?

<details>
<summary>▶ Answer</summary>

**(i)** P(+) = 0.50(0.02) + 0.20(0.12) + 0.30(0.06) = 0.010 + 0.024 + 0.018 = **0.052**

**(ii)** P(B|+) = 0.024/0.052 = **0.4615 (46.15%)**

(A: 0.010/0.052 = 0.1923; C: 0.018/0.052 = 0.3462; sum = 1 ✓)

**The dramatic bit:** Centre B handles only **20%** of patients but accounts for **46%** of positives, because
its detection rate (12%) is six times A's (2%). Centre A tests two-and-a-half times as many patients as B yet
explains only 19% of positives.

**Reading Bayes correctly:** the posterior is (prior × likelihood) normalised. A big prior with a tiny
likelihood loses to a small prior with a big likelihood.
</details>

---

## 8. Repeated trials: binomial, multinomial, wait-for-the-k-th

### Q8.1 — multinomial, not binomial

The probabilities that a delegate arrived by air, bus, automobile or train are 0.4, 0.2, 0.3, 0.1. Among 9
randomly selected delegates, what is P(3 by air, 3 by bus, 1 by automobile, 2 by train)? *(CT Q1(b))*

<details>
<summary>▶ Answer</summary>

**≈ 0.00774**

This is **multinomial** — four categories, not two:

P = [9! / (3!·3!·1!·2!)] × (0.4)³(0.2)³(0.3)¹(0.1)²

The coefficient: 362880/(6 × 6 × 1 × 2) = 362880/72 = **5040**
The product: (0.064)(0.008)(0.3)(0.01) = 1.536 × 10⁻⁶

P = 5040 × 1.536 × 10⁻⁶ = **0.007741**

**The trap:** reaching for ⁹C₃ and a binomial. Binomial has exactly two outcomes per trial; here each delegate
falls into one of four. The multinomial coefficient 9!/(3!3!1!2!) counts the distinct *arrangements* of the
labelled sequence AAABBBCTT.

**Check your setup:** the counts must sum to n (3+3+1+2 = 9 ✓) and the probabilities must sum to 1
(0.4+0.2+0.3+0.1 = 1 ✓). If either fails, you have misread the question.
</details>

### Q8.2 — "the 5th prescription is the 1st for a woman"

Two-thirds of Valium users are women. Find P(on a given day, the **fifth** prescription a doctor writes is
(i) **the first** prescribing Valium for a woman, (ii) **the third** prescribing Valium for a woman).
*(CT Q1(c))*

<details>
<summary>▶ Answer</summary>

p = P(woman) = 2/3, q = 1/3. The population is huge relative to the sample, so treat trials as independent.

**(i) 2/243 ≈ 0.0082** — the first four must be men, the fifth a woman:

P = q⁴ · p = (1/3)⁴(2/3) = **2/243**

**(ii) 16/81 ≈ 0.198** — among the first four, **exactly 2** women (in any order), and the fifth is a woman:

P = [⁴C₂ p²q²] · p = 6 × (4/9)(1/9) × (2/3) = 48/243 = **16/81**

**The trap:** the fifth trial's outcome is **fixed**, so it must be pulled out of the binomial coefficient.
Writing ⁵C₃ p³q² = 0.329 answers a different question ("3 of the first 5 are women", where the 3rd woman could
appear at position 2, 3, 4 or 5). This distinction — *binomial* vs *negative binomial* (wait for the k-th
success) — is the whole point of the problem.

**Structure to memorise:** P(k-th success occurs on trial n) = [ⁿ⁻¹C_{k−1} p^{k−1} q^{n−k}] × p
</details>

### Q8.3 — "at least 4" the efficient way

10% of a company's instruments are defective. Out of 12 instruments, find P(at least 4 are defective).
*(CT Q7(b)(ii))*

<details>
<summary>▶ Answer</summary>

**≈ 0.0256**

P(X ≥ 4) = 1 − P(X ≤ 3), with X ~ Bin(12, 0.1):

| k | ¹²C_k (0.1)^k (0.9)^{12−k} |
|---|---|
| 0 | 0.28243 |
| 1 | 0.37657 |
| 2 | 0.23013 |
| 3 | 0.08523 |
| **Σ** | **0.97436** |

P(X ≥ 4) = 1 − 0.97436 = **0.02564**

**Two traps:**
1. Computing terms k = 4 … 12 instead — nine terms of algebra where the complement needs four.
2. **Off-by-one:** "at least 4" means X ≥ 4, so the complement is X ≤ **3** (four terms: 0, 1, 2, 3). Using
   X ≤ 4 gives 0.0043 and is wrong.

**Sanity check:** E[X] = np = 1.2, so 4 or more is well into the right tail — a small answer like 2.6% is what
you should expect. If you get something like 0.3, you have made an error.
</details>

### Q8.4 — none / at least one / all

P(an entering college student graduates) = 0.4. For 5 students find P(none graduate), P(at least one
graduates), P(all graduate). *(CT Q8(b))*

<details>
<summary>▶ Answer</summary>

X ~ Bin(5, 0.4):

- **None:** P(X=0) = (0.6)⁵ = **0.0778**
- **At least one:** 1 − P(X=0) = **0.9222**
- **All:** P(X=5) = (0.4)⁵ = **0.0102**

**The trap:** "at least one" ≠ 1 − P(all) and ≠ P(X=1). It is 1 − P(**none**). Three different complements
that students routinely swap:

| Phrase | Complement |
|---|---|
| at least one | none |
| at least two | none or exactly one |
| all | at least one *fails* |
| none | at least one |
</details>

### Q8.5 — hypergeometric, not binomial

A box has 8 red, 3 white and 9 blue balls. Three balls are drawn at random. Find P(all 3 red), P(2 red and 1
white), P(at least 1 white). *(CT Q8(a))*

<details>
<summary>▶ Answer</summary>

Total ways: ²⁰C₃ = 1140.

- **All 3 red:** ⁸C₃/²⁰C₃ = 56/1140 = **0.0491**
- **2 red, 1 white:** (⁸C₂ × ³C₁)/²⁰C₃ = (28 × 3)/1140 = 84/1140 = **0.0737**
- **At least 1 white:** 1 − (all 3 non-white) = 1 − ¹⁷C₃/²⁰C₃ = 1 − 680/1140 = **0.4035**

**The trap:** using the binomial (0.4)³ style formula with p = 8/20. Drawing "at random" from a box means
**without replacement**, so the composition changes between draws and trials are not independent. Binomial
would give (8/20)³ = 0.064 for all-red versus the correct 0.049 — a 30% error.

**When is binomial acceptable?** Only when sampling *with* replacement, or when the population is so large
relative to the sample that the change is negligible (exactly the reasoning used in Q8.2's Valium problem,
where the population is 20 million).
</details>

### Q8.6 — mixed colours without replacement

A bag has 3 red, 4 green and 5 blue balls. Two are drawn without replacement. Find P(both red),
P(one red and one green), P(at least one blue). *(Lecture 3, Problem 2)*

<details>
<summary>▶ Answer</summary>

Total pairs ¹²C₂ = 66.

- **Both red:** ³C₂/66 = 3/66 = **1/22**
- **One red, one green:** (³C₁ × ⁴C₁)/66 = 12/66 = **2/11**
- **At least one blue:** 1 − ⁷C₂/66 = 1 − 21/66 = 45/66 = **15/22**

**The trap in part 2:** "one red and one green" does **not** need an extra factor of 2. Using combinations,
{R₁, G₃} is a single unordered pair already — 3 × 4 = 12 counts each such pair exactly once. The factor 2
appears only if you work sequentially: (3/12)(4/11) + (4/12)(3/11) = 12/66 ✓ — same answer, two orderings,
because the sequential method distinguishes RG from GR.

**Rule:** pick one framework (ordered or unordered) and stay in it for numerator *and* denominator.
</details>

---

## 9. Joint distributions & marginals

### Q9.1 — the two-pen joint distribution

Two ballpoint pens are selected at random from a box containing **3 blue, 2 red and 3 green** pens. Let X =
number of blue selected, Y = number of red selected. Find (i) the joint probability function f(x,y),
(ii) P[(X,Y) ∈ A] where A = {(x,y) : x + y ≤ 1}, (iii) the marginal distributions of X and Y.
*(Lecture 4, Problem 5)*

<details>
<summary>▶ Answer</summary>

Total ⁸C₂ = 28. Each cell: f(x,y) = [³C_x · ²C_y · ³C_{2−x−y}] / 28 (the leftover pens are green).

| | Y=0 | Y=1 | Y=2 | **Row total f(x)** |
|---|---|---|---|---|
| **X=0** | 3/28 | 6/28 | 1/28 | **10/28** |
| **X=1** | 9/28 | 6/28 | — | **15/28** |
| **X=2** | 3/28 | — | — | **3/28** |
| **Col total f(y)** | **15/28** | **12/28** | **1/28** | **28/28 = 1** |

*Sample cell:* f(0,0) = (³C₀ · ²C₀ · ³C₂)/28 = 3/28 (both pens green).
*Blank cells* are impossible: you cannot pick 2 blue and 1 red from only 2 pens.

**(ii)** A = {(0,0), (1,0), (0,1)}:

P = 3/28 + 9/28 + 6/28 = 18/28 = **9/14**

**(iii)** Marginals — the row and column totals:

| x | 0 | 1 | 2 |
|---|---|---|---|
| **g(x)** | 10/28 = 5/14 | **15/28** | **3/28** |

| y | 0 | 1 | 2 |
|---|---|---|---|
| **h(y)** | 15/28 | 12/28 = 3/7 | 1/28 |

⚠️ **The lecture PDF has a typo here** — it prints P(X=0) = P(X=1) = P(X=2) = 10/28, which sums to 30/28 > 1.
The correct marginal is 10/28, 15/28, 3/28. **Always check a marginal sums to 1** before you use it.

**Bonus:** X and Y are clearly **not** independent — f(2,2) = 0 but g(2)h(2) = (3/28)(1/28) ≠ 0. Drawing a
blue pen uses up one of your two slots, so it suppresses red.
</details>

### Q9.2 — reading a joint table backwards

From the Machine A/B table of Q4.5, find P(A | not defective) and compare it with P(A) = 0.40. What does the
comparison mean?

<details>
<summary>▶ Answer</summary>

P(A | not defective) = 0.38/0.92 = **0.4130**

Compare: P(A) = 0.40, P(A | defective) = 0.25, P(A | not defective) = 0.4130.

**Interpretation:** learning an item is *good* nudges belief slightly toward Machine A (0.40 → 0.413), because
A is the more reliable machine. Learning an item is *defective* swings belief hard away from A (0.40 → 0.25).

**The consistency check worth memorising:** the two conditionals must average back to the prior, weighted by
the evidence probabilities:

P(A) = P(A|D)·P(D) + P(A|Dᶜ)·P(Dᶜ) = 0.25(0.08) + 0.4130(0.92) = 0.02 + 0.38 = **0.40** ✓

If your posteriors do not average back to the prior, one of them is wrong. This single check catches most
Bayes arithmetic errors.
</details>

---

## 10. Spot the error

Each snippet below contains a mistake. Find it before opening the answer.

### Q10.1

> *"A and B are independent, so P(A∪B) = P(A) + P(B)."*

<details>
<summary>▶ Answer</summary>

**Wrong — independence does not remove the overlap.**

The correct statement is P(A∪B) = P(A) + P(B) − P(A)P(B) for independent events. The rule
P(A∪B) = P(A) + P(B) needs **mutual exclusivity**, which (by Q5.1) independence actively *rules out* for
positive-probability events.

Concretely with P(A) = 0.4, P(B) = 0.5: the false version gives 0.9, the correct one gives 0.7.
</details>

### Q10.2

> *"The odds against student X are 8:6, so P(X solves) = 8/14."*

<details>
<summary>▶ Answer</summary>

**Wrong direction.** Odds **against** list failures first: 8 failures : 6 successes.

P(X solves) = 6/14 = **3/7**, and 8/14 = 4/7 is P(X **fails**).

See Q3.1 — this single slip destroys every part of a five-part exam question.
</details>

### Q10.3

> *"P(disease | positive test) = 0.90, because the test is 90% effective."*

<details>
<summary>▶ Answer</summary>

**Reversed conditional.** "90% effective" is P(**positive** | **disease**) = 0.90. The requested quantity is
P(disease | positive), which by Bayes (Q7.4) is only **0.1538**.

P(A|B) and P(B|A) are related by Bayes, not by equality:

P(A|B) = P(B|A)·P(A)/P(B)

They coincide only when P(A) = P(B). When the disease is rare, they differ by an order of magnitude.
</details>

### Q10.4

> *"5 got sunburnt and 8 got bitten, so 13 students had a mishap and 20 − 13 = 7 returned safely."*

<details>
<summary>▶ Answer</summary>

**Ignores the overlap, and contradicts the given data.** The problem *states* 10 returned safely, so exactly
10 had at least one mishap:

n(A∪B) = 5 + 8 − n(A∩B) = 10 → n(A∩B) = **3**

Three students were both sunburnt **and** bitten, and were counted twice in "13". See Q6.3.
</details>

### Q10.5

> *"P(H) = 0.25, P(W) = 0.35, P(H|W) = 0.8, so P(H∩W) = 0.28 and P(H|Wᶜ) = (0.25 − 0.28)/0.65 = 0.046."*

<details>
<summary>▶ Answer</summary>

**Two errors — one arithmetic, one conceptual.**

*Arithmetic:* (0.25 − 0.28)/0.65 = **−0.046**, not +0.046. The sign was silently dropped.

*Conceptual:* the negative sign is the **correct diagnosis** — the data is inconsistent. P(H∩W) = 0.28 cannot
exceed P(H) = 0.25, since H∩W ⊆ H. The right answer is *"no valid answer exists; the given numbers violate
P(A∩B) ≤ min{P(A), P(B)}."* See Q6.5.
</details>

### Q10.6

> *"The marginal distribution of X is P(X=0) = 10/28, P(X=1) = 10/28, P(X=2) = 10/28."*

<details>
<summary>▶ Answer</summary>

**These sum to 30/28 > 1** — impossible for a probability distribution.

The correct marginals (row sums of the joint table in Q9.1) are **10/28, 15/28, 3/28**, which total 28/28 = 1.

This exact typo appears in the Lecture 3 & 4 handout. Checking that a distribution sums to 1 takes three
seconds and catches it.
</details>

### Q10.7

> *"P(A can solve) = 3/7, P(B) = 2/3, P(C) = 4/5, so P(problem solved) = 3/7 + 2/3 + 4/5 = 1.876."*

<details>
<summary>▶ Answer</summary>

**A probability above 1 is impossible** — an instant red flag. Adding non-disjoint events triple-counts the
overlaps.

Correct: P(solved) = 1 − P(none solves) = 1 − (4/7)(1/3)(1/5) = 1 − 4/105 = **101/105 ≈ 0.962**. See Q5.3.
</details>

### Q10.8

> *"One ball moves from bag 1 into bag 2, so P(black from bag 2) = (3/7)(6/8) + (4/7)(5/8)."*

<details>
<summary>▶ Answer</summary>

**Denominator not updated.** Bag 2 started with 8 balls and **received one more**, so it now holds 9.

Correct: (3/7)(6/9) + (4/7)(5/9) = **38/63**. The erroneous version gives 38/56 = 0.679 instead of 0.603.
See Q7.1.
</details>

---

## 11. Rapid-fire true/false

Decide true or false for each, with a one-line reason, before opening the key.

1. If A and B are mutually exclusive and P(A), P(B) > 0, they can still be independent.
2. P(A|B) is always ≥ P(A).
3. P(A|B) + P(Aᶜ|B) = 1.
4. P(A|B) + P(A|Bᶜ) = 1.
5. Odds can exceed 1.
6. "Either X or Y solves it" excludes the case where both solve.
7. P(A∩B) can exceed P(A).
8. Drawing "at random" from a box means with replacement.
9. For independent A and B, P(neither) = P(Aᶜ)P(Bᶜ).
10. That same formula for P(neither) also works when A and B are dependent.
11. If the posteriors P(Bᵢ|D) do not sum to 1, you made an arithmetic error.
12. "At least 4" has complement "at most 4".

<details>
<summary>▶ Answers (all 12)</summary>

| # | Verdict | Reason |
|---|---|---|
| 1 | **False** | P(A∩B) = 0 ≠ P(A)P(B) > 0. Disjoint events are maximally dependent (Q5.1). |
| 2 | **False** | Conditioning can lower a probability — Q7.5 drops the prior 0.5 to 0.328. |
| 3 | **True** | For a *fixed* B, P(·\|B) is itself a probability measure, so it obeys the complement rule. |
| 4 | **False** | Different conditioning sets, so no such rule. In Q6.4, P(H\|W) = 0.7 while P(H\|Wᶜ) = (0.40 − 0.35)/0.50 = 0.10; they sum to 0.8, not 1. |
| 5 | **True** | Odds are the ratio P(A)/P(Aᶜ), unbounded above — Q3.2 gives 4. |
| 6 | **False** | "Or" is inclusive in probability; only "exactly one" excludes the both-case (Q3.4). |
| 7 | **False** | A∩B ⊆ A, so P(A∩B) ≤ min{P(A), P(B)} — the violation that breaks Q6.5. |
| 8 | **False** | The default is *without* replacement unless the question says otherwise (Q8.5). |
| 9 | **True** | If A and B are independent, so are Aᶜ and Bᶜ. |
| 10 | **False** | Go via 1 − P(A∪B) instead; using the product gave the wrong 32/105 in Q3.5. |
| 11 | **True** | The Bᵢ partition the sample space, so their posteriors must total 1 (Q7.2). |
| 12 | **False** | The complement of X ≥ 4 is X ≤ 3 (Q8.3). |
</details>

---

## 12. Formula sheet

*(Open only after attempting the questions.)*

<details>
<summary>▶ Everything on one page</summary>

**Counting**

- ⁿPᵣ = n!/(n−r)!  — order matters
- ⁿCᵣ = n!/[r!(n−r)!]  — order does not
- Multinomial: n!/(n₁! n₂! … n_k!) for splitting n items into labelled groups of sizes nᵢ

**Classical probability**

- P(A) = n(A)/n(S), valid **only** when outcomes are equally likely

**Odds**

- Odds in favour of A = n(A) : n(Aᶜ) = P(A)/(1 − P(A))
- Odds against A = n(Aᶜ) : n(A) = (1 − P(A))/P(A)
- If odds in favour are a : b, then P(A) = a/(a+b) and P(Aᶜ) = b/(a+b)

**Addition & complement**

- P(A∪B) = P(A) + P(B) − P(A∩B)
- P(Aᶜ) = 1 − P(A)
- De Morgan: (A∪B)ᶜ = Aᶜ∩Bᶜ  and  (A∩B)ᶜ = Aᶜ∪Bᶜ
- P(neither) = P((A∪B)ᶜ) = 1 − P(A∪B)

**Multiplication**

- Independent: P(A∩B) = P(A)P(B)
- Dependent: P(A∩B) = P(A)P(B|A) = P(B)P(A|B)
- Chain rule: P(A₁∩A₂∩A₃) = P(A₁)P(A₂|A₁)P(A₃|A₁∩A₂)

**Conditional**

- P(A|B) = P(A∩B)/P(B), P(B) ≠ 0
- Equally likely case: P(A|B) = n(A∩B)/n(B)
- P(A ∩ Bᶜ) = P(A) − P(A∩B)

**Total probability**

- P(A) = Σᵢ P(Bᵢ)P(A|Bᵢ) over a partition {Bᵢ}

**Bayes**

- P(Bₖ|A) = P(Bₖ)P(A|Bₖ) / Σᵢ P(Bᵢ)P(A|Bᵢ)

**Repeated trials**

- Binomial: P(X=k) = ⁿC_k p^k q^{n−k}, mean np
- Negative binomial (k-th success on trial n): ⁿ⁻¹C_{k−1} p^{k−1} q^{n−k} × p
- Hypergeometric (no replacement): P = (ᴷC_k · ᴺ⁻ᴷC_{n−k}) / ᴺC_n

**Reliability**

- Series (all must work): P(works) = Π P(component works)
- Parallel (one is enough): P(fails) = Π P(branch fails)

**Sanity checks — run these on every answer**

1. 0 ≤ P ≤ 1
2. P(A∩B) ≤ min{P(A), P(B)} ≤ max{P(A), P(B)} ≤ P(A∪B)
3. Marginals and posterior sets sum to 1
4. Exactly-one ≤ at-least-one
5. Posteriors average back to the prior: P(A) = P(A|D)P(D) + P(A|Dᶜ)P(Dᶜ)
</details>
