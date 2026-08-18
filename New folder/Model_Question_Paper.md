# MATH-243 — Model Question Paper (CT Pattern)

Modelled on the structure, difficulty and mark distribution of **1stCT_Prob.pdf**. Purely computational —
no theory, no definitions, no "explain why". Every part asks for a number.

**Problem archetypes are drawn from the same textbook pool the CT itself uses** — Walpole, Myers, Myers & Ye,
*Probability & Statistics for Engineers & Scientists* (the CT's assembly-plant, TV-show, circuit and joint-pen
questions are Examples 2.41/2.42 and Exercises 2.81, 2.93 of that text) and Spiegel/Lipschutz,
*Schaum's Outline of Probability and Statistics* (the CT's box-of-balls, graduation-binomial and
different-suits questions). Numbers and contexts here are changed so you cannot pattern-match an answer.

> **How to use:** sit **Set A** and **Set B** as two 90-minute papers with only a calculator. Then open the
> [Worked Solutions](#worked-solutions) — every part has a full derivation, not just a final number.

**Marks:** Set A = 110, Set B = 118.

---

# SET A — Basic Probability & Counting

*(Independent events · combinations · card decks · binomial · multinomial · reliability)*

---

**1.**

**(a)** One bag contains 5 white balls and 4 black balls, and a second bag contains 6 white balls and 3 black
balls. One ball is drawn from the first bag and placed **unseen** in the second bag. What is the probability
that a ball now drawn from the second bag is **white**?  **(8)**

**(b)** The probabilities are 0.30, 0.25, 0.35 and 0.10, respectively, that a customer entering a store pays by
cash, credit card, mobile banking, or cheque. What is the probability that among 8 randomly selected
customers, 2 pay by cash, 3 by credit card, 2 by mobile banking and 1 by cheque?  **(10)**

**(c)** It is known that 40% of the students of a large university are enrolled in the Engineering faculty.
Find the probability that on a given day the **sixth** student entering the central library is  **(10)**

&nbsp;&nbsp;&nbsp;&nbsp;(i) the **first** Engineering student to enter;
&nbsp;&nbsp;&nbsp;&nbsp;(ii) the **second** Engineering student to enter.

---

**2.**

**(a)** A box contains 7 red, 5 white and 4 blue marbles. If four marbles are drawn at random, determine the
probability that (i) all 4 are red, (ii) 2 are red and 2 are white, (iii) at least 1 is blue.  **(12)**

**(b)** The probability that a newly planted sapling survives its first year is 0.7. Determine the probability
that out of 6 saplings (i) none survives, (ii) at least one survives, (iii) exactly 4 survive.  **(12)**

---

**3.**

**(a)** 4 cards are drawn from a deck of 52 cards one after another without replacement. Find the probability
that (i) they all come from different suits, (ii) they all come from the same suit.  **(12)**

**(b)** If 15% of the bolts produced by a machine are defective, find the probability that out of 10 bolts
chosen at random (i) exactly 2 are defective, (ii) at most 2 are defective, (iii) at least 3 are
defective.  **(10)**

**(c)** The probability that technician A can repair a machine is 2/5, that B can repair it is 1/3, and that C
can repair it is 3/4. If all of them try independently, find the probability that the machine will be
repaired.  **(8)**

---

**4.**

**(a)** A circuit operates if and only if there is a path of functional devices from left to right. Devices fail
independently. The system is built in three stages connected in series:  **(10)**

- **Stage 1:** two devices in parallel, each failing with probability 0.05
- **Stage 2:** a single device failing with probability 0.02
- **Stage 3:** three devices in parallel, each failing with probability 0.10

Find the probability that the circuit **operates**, and the probability that it does **not** operate.

**(b)** A committee of 5 members is to be formed from 7 engineers and 5 architects. In how many ways can it be
done if the committee must contain (i) exactly 2 architects, (ii) at least 4 engineers, (iii) at least one
engineer and at least one architect?  **(10)**

**(c)** Two fair dice are thrown once. Find the probability that (i) the sum of the points is 8, (ii) the sum
is at least 10, (iii) the product of the two numbers is odd.  **(8)**

---

# SET B — Conditional Probability & Bayes' Theorem

*(Valid space · Venn diagrams · conditional probability · Bayes · joint distributions)*

---

**5.**

**(a)** In a survey of 120 students, 60 read *The Daily Star*, 45 read *Prothom Alo*, and 25 read both. A
student is selected at random. Find the probability that the student  **(12)**

&nbsp;&nbsp;&nbsp;&nbsp;(i) reads at least one of the two papers;
&nbsp;&nbsp;&nbsp;&nbsp;(ii) reads none of them;
&nbsp;&nbsp;&nbsp;&nbsp;(iii) reads *Prothom Alo* but not *The Daily Star*;
&nbsp;&nbsp;&nbsp;&nbsp;(iv) reads *The Daily Star*, given that the student reads *Prothom Alo*.

**(b)** A group of 30 tourists visited a hill tract. Among them 12 suffered from fever, 9 suffered from a
stomach upset, and 14 returned home without any illness. What is the probability that (i) a tourist who
suffered from fever also suffered from a stomach upset, and (ii) a tourist who suffered from a stomach upset
did **not** suffer from fever?  **(12)**

**(c)** The odds **against** student X solving a statistics problem are 7 : 5, and the odds **in favour** of
student Y solving it are 9 : 7. If they work independently, find the probability that (i) both solve it,
(ii) neither solves it, (iii) exactly one solves it.  **(8)**

---

**6.**

**(a)** The probability that a married man reads a certain magazine is 0.45 and that a married woman reads it
is 0.60. The probability that a man reads the magazine, given that his wife does, is 0.65. Find the
probability that  **(13)**

&nbsp;&nbsp;&nbsp;&nbsp;(i) both husband and wife read the magazine;
&nbsp;&nbsp;&nbsp;&nbsp;(ii) a wife reads it, given that her husband does;
&nbsp;&nbsp;&nbsp;&nbsp;(iii) at least one member of the couple reads it;
&nbsp;&nbsp;&nbsp;&nbsp;(iv) a husband reads it, given that his wife does **not**.

**(b)** In a certain assembly plant, three machines M₁, M₂ and M₃ make 25%, 35% and 40%, respectively, of the
products. It is known from past experience that 5%, 4% and 2% of the products made by each machine,
respectively, are defective. A finished product is randomly selected and it is found to be defective. What is
the probability that this product was made by machine Mᵢ, i = 1, 2, 3?  **(15)**

---

**7.**

**(a)** A diagnostic test is 96% effective in detecting a certain disease when the disease is present. However,
the test yields a false-positive result for 3% of the healthy persons tested. Suppose 2% of the population has
the disease. A person is chosen at random and the test result is positive. Find the probability that the
person (i) actually has the disease, (ii) does not have the disease.  **(17)**

**(b)** Urn A contains 3 red and 5 white balls; urn B contains 6 red and 4 white balls. A fair die is rolled:
if the outcome is 1 or 2, a ball is drawn from urn A; otherwise a ball is drawn from urn B. Given that the
ball drawn is **red**, what is the probability that it came from **urn A**?  **(15)**

---

**8.**

**(a)** A factory runs three shifts. The morning shift produces 45% of the output, of which 1% is defective;
the evening shift produces 35%, of which 3% is defective; the night shift produces 20%, of which 6% is
defective.  **(13)**

&nbsp;&nbsp;&nbsp;&nbsp;(i) Find the probability that a randomly chosen item is defective.
&nbsp;&nbsp;&nbsp;&nbsp;(ii) Given that an item is defective, find the probability that it came from the night shift.
&nbsp;&nbsp;&nbsp;&nbsp;(iii) Given that an item is non-defective, find the probability that it came from the morning shift.

**(b)** Two ballpoint pens are selected at random from a box that contains 4 blue pens, 3 red pens and 2 green
pens. If X is the number of blue pens selected and Y is the number of red pens selected, find  **(15)**

&nbsp;&nbsp;&nbsp;&nbsp;(i) the joint probability function f(x, y);
&nbsp;&nbsp;&nbsp;&nbsp;(ii) P[(X, Y) ∈ A], where A is the region {(x, y) | x + y ≤ 1};
&nbsp;&nbsp;&nbsp;&nbsp;(iii) the marginal distribution of X alone and of Y alone.

---
---

# Worked Solutions

## Set A

<details>
<summary>▶ 1(a) — transferred ball (8 marks)</summary>

The transferred ball's colour is unknown, so condition on it (law of total probability). Bag 2 ends with
**10** balls either way.

Let W₁ = a white ball is transferred, B₁ = a black ball is transferred, W₂ = white drawn from bag 2.

- P(W₁) = 5/9. Bag 2 becomes 7 white + 3 black → P(W₂|W₁) = 7/10
- P(B₁) = 4/9. Bag 2 becomes 6 white + 4 black → P(W₂|B₁) = 6/10

P(W₂) = (5/9)(7/10) + (4/9)(6/10) = 35/90 + 24/90 = **59/90 ≈ 0.6556**

*Check:* P(black from bag 2) = (5/9)(3/10) + (4/9)(4/10) = 15/90 + 16/90 = 31/90, and 59/90 + 31/90 = 1 ✓
</details>

<details>
<summary>▶ 1(b) — multinomial (10 marks)</summary>

Four categories, so this is **multinomial**, not binomial. Counts 2 + 3 + 2 + 1 = 8 ✓ and probabilities
0.30 + 0.25 + 0.35 + 0.10 = 1 ✓

P = [8! / (2! 3! 2! 1!)] (0.30)²(0.25)³(0.35)²(0.10)¹

Coefficient: 40320 / (2 × 6 × 2 × 1) = 40320/24 = **1680**

Product: (0.09)(0.015625)(0.1225)(0.10) = 1.72266 × 10⁻⁵

P = 1680 × 1.72266 × 10⁻⁵ = **0.02894**
</details>

<details>
<summary>▶ 1(c) — negative binomial / geometric (10 marks)</summary>

p = P(Engineering student) = 0.40, q = 0.60. The university is large, so successive students are independent.

**(i) The 6th student is the *first* Engineering student.**
The first 5 must all be non-Engineering, and the 6th must be Engineering (geometric distribution):

P = q⁵p = (0.6)⁵(0.4) = 0.07776 × 0.4 = **0.031104**

**(ii) The 6th student is the *second* Engineering student.**
Among the first 5 there must be **exactly 1** Engineering student (in any of 5 positions), and the 6th is
Engineering:

P = [⁵C₁ p¹q⁴] × p = [5 × 0.4 × 0.1296] × 0.4 = 0.2592 × 0.4 = **0.10368**

*Key point:* the 6th trial is **fixed** as a success, so it is pulled out of the binomial coefficient. Writing
⁶C₂p²q⁴ = 0.138 answers a different question.
</details>

<details>
<summary>▶ 2(a) — hypergeometric counting (12 marks)</summary>

Total marbles = 7 + 5 + 4 = 16. Drawing 4 without replacement: ¹⁶C₄ = **1820**.

**(i) All 4 red:** ⁷C₄/¹⁶C₄ = 35/1820 = **1/52 ≈ 0.0192**

**(ii) 2 red and 2 white:** (⁷C₂ × ⁵C₂)/¹⁶C₄ = (21 × 10)/1820 = 210/1820 = **3/26 ≈ 0.1154**

**(iii) At least 1 blue:** use the complement — "no blue" means all 4 come from the 12 non-blue marbles:

1 − ¹²C₄/¹⁶C₄ = 1 − 495/1820 = 1325/1820 = **265/364 ≈ 0.7280**
</details>

<details>
<summary>▶ 2(b) — binomial (12 marks)</summary>

X = number surviving ~ Bin(n = 6, p = 0.7), q = 0.3.

**(i) None survives:** P(X = 0) = (0.3)⁶ = **0.000729**

**(ii) At least one survives:** 1 − P(X = 0) = 1 − 0.000729 = **0.999271**

**(iii) Exactly 4 survive:** ⁶C₄ (0.7)⁴(0.3)² = 15 × 0.2401 × 0.09 = **0.324135**
</details>

<details>
<summary>▶ 3(a) — cards (12 marks)</summary>

**(i) All four from different suits.** Sequentially, each card must avoid the suits already used:

P = (52/52)(39/51)(26/50)(13/49) = **2197/20825 ≈ 0.1055**

*Combination check:* (⁴C₄ × 13⁴)/⁵²C₄ = 28561/270725 = 0.1055 ✓

**(ii) All four from the same suit.** Choose the suit (4 ways), then 4 cards from its 13:

P = (4 × ¹³C₄)/⁵²C₄ = (4 × 715)/270725 = 2860/270725 = **44/4165 ≈ 0.01056**

*Sequential check:* (52/52)(12/51)(11/50)(10/49) = 0.01056 ✓
</details>

<details>
<summary>▶ 3(b) — binomial, three tails (10 marks)</summary>

X ~ Bin(10, 0.15), q = 0.85.

| k | ¹⁰C_k (0.15)^k (0.85)^{10−k} |
|---|---|
| 0 | 0.196874 |
| 1 | 0.347425 |
| 2 | 0.275897 |

**(i) Exactly 2 defective:** ¹⁰C₂(0.15)²(0.85)⁸ = 45 × 0.0225 × 0.272491 = **0.27590**

**(ii) At most 2 defective:** P(X ≤ 2) = 0.196874 + 0.347425 + 0.275897 = **0.82020**

**(iii) At least 3 defective:** 1 − P(X ≤ 2) = 1 − 0.82020 = **0.17980**

*Note the boundary:* "at least 3" has complement "at most **2**", not "at most 3".
*Sanity check:* E[X] = np = 1.5, so 3 or more sits in the right tail — a smallish answer is expected.
</details>

<details>
<summary>▶ 3(c) — independent repair (8 marks)</summary>

"Repaired" = at least one of the three succeeds. Go through the complement:

P(none repairs) = (3/5)(2/3)(1/4) = 6/60 = 1/10

P(machine repaired) = 1 − 1/10 = **9/10 = 0.9**

*Do not add* 2/5 + 1/3 + 3/4 = 1.483 — a probability cannot exceed 1.
</details>

<details>
<summary>▶ 4(a) — series–parallel reliability (10 marks)</summary>

Work stage by stage. **Parallel** = fails only if every device fails; **series** = works only if every stage
works.

- **Stage 1** (2 parallel, each fails 0.05): P(works) = 1 − (0.05)² = 1 − 0.0025 = 0.9975
- **Stage 2** (single device): P(works) = 1 − 0.02 = 0.98
- **Stage 3** (3 parallel, each fails 0.10): P(works) = 1 − (0.10)³ = 1 − 0.001 = 0.999

The three stages are in series, so multiply the working probabilities:

P(circuit operates) = 0.9975 × 0.98 × 0.999 = **0.976572**

P(circuit does not operate) = 1 − 0.976572 = **0.023428**
</details>

<details>
<summary>▶ 4(b) — committee counting (10 marks)</summary>

7 engineers + 5 architects = 12 people, choose 5. Total ¹²C₅ = 792.

**(i) Exactly 2 architects** (so 3 engineers): ⁵C₂ × ⁷C₃ = 10 × 35 = **350**

**(ii) At least 4 engineers:**
- 4E, 1A: ⁷C₄ × ⁵C₁ = 35 × 5 = 175
- 5E, 0A: ⁷C₅ = 21

Total = **196**

**(iii) At least one of each:** subtract the two all-one-kind committees from the total:

792 − ⁷C₅ − ⁵C₅ = 792 − 21 − 1 = **770**
</details>

<details>
<summary>▶ 4(c) — two dice (8 marks)</summary>

n(S) = 36.

**(i) Sum = 8:** {(2,6), (3,5), (4,4), (5,3), (6,2)} → **5/36**

**(ii) Sum ≥ 10:** sum 10 → 3 ways, sum 11 → 2 ways, sum 12 → 1 way → 6/36 = **1/6**

**(iii) Product odd:** a product is odd only if **both** numbers are odd → 3 × 3 = 9 outcomes → 9/36 = **1/4**
</details>

## Set B

<details>
<summary>▶ 5(a) — survey table (12 marks)</summary>

n(S) = 120, n(D) = 60, n(P) = 45, n(D∩P) = 25.

|  | D | Dᶜ | Total |
|---|---|---|---|
| **P** | 25 | 20 | 45 |
| **Pᶜ** | 35 | 40 | 75 |
| **Total** | 60 | 60 | 120 |

**(i)** n(D∪P) = 60 + 45 − 25 = 80 → P = 80/120 = **2/3 ≈ 0.667**

**(ii)** P(neither) = 1 − 2/3 = 40/120 = **1/3 ≈ 0.333**

**(iii)** n(P ∩ Dᶜ) = 45 − 25 = 20 → P = 20/120 = **1/6 ≈ 0.167**

**(iv)** P(D|P) = n(D∩P)/n(P) = 25/45 = **5/9 ≈ 0.556**
</details>

<details>
<summary>▶ 5(b) — tourists, overlap must be derived (12 marks)</summary>

14 of the 30 returned healthy, so 30 − 14 = **16** suffered at least one illness:

n(F∪S) = n(F) + n(S) − n(F∩S) → 16 = 12 + 9 − n(F∩S) → **n(F∩S) = 5**

Venn: fever only = 7, both = 5, stomach only = 4, neither = 14. Total 7+5+4+14 = 30 ✓

**(i)** P(S | F) = n(F∩S)/n(F) = 5/12 ≈ **0.4167**

**(ii)** P(Fᶜ | S) = n(Fᶜ∩S)/n(S) = 4/9 ≈ **0.4444**

*The given event goes in the denominator* — (i) conditions on fever (12), (ii) conditions on stomach upset (9).
</details>

<details>
<summary>▶ 5(c) — odds (8 marks)</summary>

Odds **against** X = 7 : 5 → failures : successes, so P(X) = 5/(7+5) = **5/12**, P(Xᶜ) = 7/12.
Odds **in favour** of Y = 9 : 7 → successes : failures, so P(Y) = 9/(9+7) = **9/16**, P(Yᶜ) = 7/16.

**(i) Both solve:** (5/12)(9/16) = 45/192 = **15/64 ≈ 0.2344**

**(ii) Neither solves:** (7/12)(7/16) = **49/192 ≈ 0.2552**

**(iii) Exactly one solves:**
P(X∩Yᶜ) + P(Xᶜ∩Y) = (5/12)(7/16) + (7/12)(9/16) = 35/192 + 63/192 = 98/192 = **49/96 ≈ 0.5104**

*Check:* 45/192 + 49/192 + 98/192 = 192/192 = 1 ✓
</details>

<details>
<summary>▶ 6(a) — magazine couple (13 marks)</summary>

P(H) = 0.45, P(W) = 0.60, P(H|W) = 0.65.

**(i)** P(H∩W) = P(W)·P(H|W) = 0.60 × 0.65 = **0.39**
*(Pair P(H|W) with P(W) — the conditioning event supplies the multiplier.)*

**(ii)** P(W|H) = P(H∩W)/P(H) = 0.39/0.45 = **0.8667**

**(iii)** P(H∪W) = 0.45 + 0.60 − 0.39 = **0.66**

**(iv)** P(H|Wᶜ) = P(H∩Wᶜ)/P(Wᶜ) = [P(H) − P(H∩W)]/[1 − P(W)] = (0.45 − 0.39)/0.40 = 0.06/0.40 = **0.15**

*Consistency:* P(H∩W) = 0.39 ≤ min{0.45, 0.60} ✓, and 0.65(0.60) + 0.15(0.40) = 0.39 + 0.06 = 0.45 = P(H) ✓
</details>

<details>
<summary>▶ 6(b) — three machines, Bayes (15 marks)</summary>

**Step 1 — total probability:**

P(D) = 0.25(0.05) + 0.35(0.04) + 0.40(0.02) = 0.0125 + 0.0140 + 0.0080 = **0.0345**

**Step 2 — Bayes:**

| Machine | P(Mᵢ ∩ D) | P(Mᵢ \| D) |
|---|---|---|
| M₁ | 0.0125 | 0.0125/0.0345 = **0.3623 (36.23%)** |
| M₂ | 0.0140 | 0.0140/0.0345 = **0.4058 (40.58%)** |
| M₃ | 0.0080 | 0.0080/0.0345 = **0.2319 (23.19%)** |

**Sum = 1.0000 ✓**

M₃ makes the most product (40%) yet is least likely to be the culprit, because its defect rate is lowest.
</details>

<details>
<summary>▶ 7(a) — diagnostic test (17 marks)</summary>

D = has disease, + = tests positive. P(D) = 0.02, P(+|D) = 0.96, P(+|Dᶜ) = 0.03.

P(D ∩ +) = 0.02 × 0.96 = 0.0192
P(Dᶜ ∩ +) = 0.98 × 0.03 = 0.0294
**P(+) = 0.0486**

**(i)** P(D|+) = 0.0192/0.0486 = **0.3951 (39.51%)**

**(ii)** P(Dᶜ|+) = 0.0294/0.0486 = **0.6049 (60.49%)**

Even with a 96%-effective test, a positive result leaves the person **more likely healthy than diseased**,
because the healthy group is 49 times larger. Per 10 000 people: 200 diseased (192 detected) vs 9 800 healthy
(294 false positives) → 192/486 = 0.3951.
</details>

<details>
<summary>▶ 7(b) — die selects the urn (15 marks)</summary>

P(A) = 2/6 = 1/3 (die shows 1 or 2), P(B) = 4/6 = 2/3.
P(R|A) = 3/8, P(R|B) = 6/10 = 3/5.

P(A ∩ R) = (1/3)(3/8) = 1/8
P(B ∩ R) = (2/3)(3/5) = 2/5
P(R) = 1/8 + 2/5 = 5/40 + 16/40 = **21/40 = 0.525**

P(A|R) = (1/8)/(21/40) = (5/40)/(21/40) = **5/21 ≈ 0.2381**

The prior P(A) = 1/3 falls to 5/21 ≈ 0.238 because urn B is both more likely to be chosen **and** richer in
red balls (3/5 vs 3/8).

*Trap avoided:* the two urns hold different totals (8 vs 10) — recount each one.
</details>

<details>
<summary>▶ 8(a) — three shifts (13 marks)</summary>

**(i)** P(D) = 0.45(0.01) + 0.35(0.03) + 0.20(0.06) = 0.0045 + 0.0105 + 0.0120 = **0.027**

**(ii)** P(night | D) = 0.0120/0.027 = **0.4444 (44.44%)**

**(iii)** Work with the non-defective column: P(Dᶜ) = 1 − 0.027 = 0.973, and
P(morning ∩ Dᶜ) = 0.45 × 0.99 = 0.4455.

P(morning | Dᶜ) = 0.4455/0.973 = **0.4579 (45.79%)**

Full joint table:

|  | Defective | Non-defective | Total |
|---|---|---|---|
| Morning | 0.0045 | 0.4455 | 0.45 |
| Evening | 0.0105 | 0.3395 | 0.35 |
| Night | 0.0120 | 0.1880 | 0.20 |
| **Total** | **0.027** | **0.973** | **1.000** |

*Check:* P(morning) = 0.4444(0.027) + 0.4579(0.973) = 0.012 + 0.4455… ≈ 0.45 ✓
</details>

<details>
<summary>▶ 8(b) — joint distribution of two pens (15 marks)</summary>

Box: 4 blue, 3 red, 2 green = 9 pens. Choose 2: ⁹C₂ = **36**.
X = number of blue, Y = number of red; the remaining 2 − x − y pens are green.

**(i)** f(x, y) = [⁴C_x · ³C_y · ²C_{2−x−y}] / 36 for x + y ≤ 2, and 0 otherwise.

Sample cell: f(0,0) = (⁴C₀ · ³C₀ · ²C₂)/36 = 1/36 (both pens green).

| | Y = 0 | Y = 1 | Y = 2 | **Row total g(x)** |
|---|---|---|---|---|
| **X = 0** | 1/36 | 6/36 | 3/36 | **10/36** |
| **X = 1** | 8/36 | 12/36 | — | **20/36** |
| **X = 2** | 6/36 | — | — | **6/36** |
| **Column total h(y)** | **15/36** | **18/36** | **3/36** | **36/36 = 1** |

**(ii)** A = {(0,0), (1,0), (0,1)}:

P[(X,Y) ∈ A] = 1/36 + 8/36 + 6/36 = 15/36 = **5/12**

**(iii) Marginal distributions** (the row and column totals):

| x | 0 | 1 | 2 |
|---|---|---|---|
| g(x) | 10/36 = 5/18 | 20/36 = 5/9 | 6/36 = 1/6 |

| y | 0 | 1 | 2 |
|---|---|---|---|
| h(y) | 15/36 = 5/12 | 18/36 = 1/2 | 3/36 = 1/12 |

Both sum to 1 ✓ — always verify this before using a marginal.
</details>

---

## Answer summary (final numbers only)

<details>
<summary>▶ Open</summary>

| Q | Answer |
|---|---|
| 1(a) | 59/90 ≈ 0.6556 |
| 1(b) | 0.02894 |
| 1(c) | (i) 0.031104 (ii) 0.10368 |
| 2(a) | (i) 1/52 ≈ 0.0192 (ii) 3/26 ≈ 0.1154 (iii) 265/364 ≈ 0.7280 |
| 2(b) | (i) 0.000729 (ii) 0.999271 (iii) 0.324135 |
| 3(a) | (i) 0.1055 (ii) 0.01056 |
| 3(b) | (i) 0.27590 (ii) 0.82020 (iii) 0.17980 |
| 3(c) | 9/10 = 0.9 |
| 4(a) | operates 0.976572; fails 0.023428 |
| 4(b) | (i) 350 (ii) 196 (iii) 770 |
| 4(c) | (i) 5/36 (ii) 1/6 (iii) 1/4 |
| 5(a) | (i) 2/3 (ii) 1/3 (iii) 1/6 (iv) 5/9 |
| 5(b) | (i) 5/12 (ii) 4/9 |
| 5(c) | (i) 15/64 (ii) 49/192 (iii) 49/96 |
| 6(a) | (i) 0.39 (ii) 0.8667 (iii) 0.66 (iv) 0.15 |
| 6(b) | M₁ 0.3623, M₂ 0.4058, M₃ 0.2319 |
| 7(a) | (i) 0.3951 (ii) 0.6049 |
| 7(b) | 5/21 ≈ 0.2381 |
| 8(a) | (i) 0.027 (ii) 0.4444 (iii) 0.4579 |
| 8(b) | (ii) 5/12; marginals X: 5/18, 5/9, 1/6 — Y: 5/12, 1/2, 1/12 |
</details>
