# MATH243 — Conditional Probability: The Shrunk Sample Space

**Core idea:** conditioning on an event $C$ throws away every outcome outside $C$ and renormalises what's left.

$$P(A\mid C) = \frac{P(A\cap C)}{P(C)}$$

When outcomes are **equally likely**, this reduces to counting: $\dfrac{n(A\cap C)}{n(C)}$.

When outcomes are **not** equally likely (any "repeat until" experiment), you must sum *probabilities*, not count outcomes. That is the step that catches people.

**How to use:** work each problem before expanding. Every solution states the shrunk space explicitly.

---

## Section A — The Anchor Problems

### Q1 — Coin tossed until a head, max 3 tosses
A coin is tossed until a head appears, or 3 tosses, whichever comes first.
Given **no head on the first toss**, find P(exactly 3 tosses are needed).

<details>
<summary>Solution</summary>

**Sample space** (experiment stops on a head):

$$S = \{H,\; TH,\; TTH,\; TTT\}$$

**These are not equally likely** — attach probabilities:

| Outcome | Probability |
|---|---|
| $H$ | $1/2$ |
| $TH$ | $1/4$ |
| $TTH$ | $1/8$ |
| $TTT$ | $1/8$ |

Sum $= 1$ ✓

**Condition:** "no head on toss 1" eliminates $\{H\}$.

Shrunk space: $\{TH,\, TTH,\, TTT\}$, total probability $\tfrac14+\tfrac18+\tfrac18 = \tfrac12$

**Target:** "exactly 3 tosses" $= \{TTH,\, TTT\}$, probability $\tfrac18+\tfrac18 = \tfrac14$

$$P = \frac{1/4}{1/2} = \boxed{\tfrac12}$$

**Shortcut worth internalising:** once toss 1 is a tail, toss 2 is guaranteed to happen. Three tosses occur iff toss 2 is *also* a tail → $\tfrac12$ directly. Conditioning on the first toss simply restarts the experiment.

**Trap:** counting the shrunk space as "3 outcomes, 2 favourable → 2/3". Wrong — $TH$ carries twice the weight of $TTH$. Never count outcomes unless they're equally likely.
</details>

### Q2 — Two children, at least one girl
Given at least one child is a girl, find P(both are girls).

<details>
<summary>Solution</summary>

$$S = \{BB,\, BG,\, GB,\, GG\}, \quad \text{all equally likely}$$

Condition eliminates $BB$. Shrunk space: $\{BG,\, GB,\, GG\}$ — three outcomes.

$$P = \boxed{\tfrac13}$$

Formally, since $GG\subseteq A$:
$$P(GG\mid A) = \frac{P(GG)}{P(A)} = \frac{1/4}{3/4} = \tfrac13$$

**Why 1/2 feels right but isn't:** "at least one" does not *identify* which child. Two distinct arrangements ($BG$, $GB$) satisfy it with mixed sexes, versus one all-girl arrangement — so mixed outcomes carry double weight inside the conditioned space.
</details>

### Q3 — Two children, eldest is a girl
Given the **eldest** child is a girl, find P(both are girls).

<details>
<summary>Solution</summary>

Naming a specific child is a *stronger* condition. Shrunk space: $\{GB,\, GG\}$ — two outcomes.

$$P = \boxed{\tfrac12}$$

**Compare with Q2.** Informally the two conditions sound similar; formally they are different events, and the answers differ ($1/3$ vs $1/2$). This distinction — *at least one* versus *a specified one* — is the entire content of the problem, and it is exactly what an examiner tests.
</details>

---

## Section B — Equally Likely Spaces

### Q4 — Two dice, even sum
Two dice are rolled. Given the sum is even, find P(both show the same number).

<details>
<summary>Solution</summary>

Sum is even ⟺ both odd or both even → $3\times3 + 3\times3 = 18$ outcomes.

Doubles: $(1,1)\dots(6,6)$ — 6 outcomes, and every double has an even sum, so all 6 survive.

$$P = \frac{6}{18} = \boxed{\tfrac13}$$
</details>

### Q5 — Two dice, at least one 4
Two dice are rolled. Given at least one shows a 4, find P(the sum is 8).

<details>
<summary>Solution</summary>

**At least one 4:** $6+6-1 = 11$ outcomes (inclusion–exclusion; $(4,4)$ counted once).

**Sum 8 overall:** $(2,6),(3,5),(4,4),(5,3),(6,2)$ — five outcomes. But only $(4,4)$ contains a 4, so only it survives the condition.

$$P = \boxed{\tfrac1{11}}$$

**Note:** unconditionally $P(\text{sum }8) = \tfrac5{36}\approx0.139$; conditionally it drops to $\approx0.091$. Conditioning can move a probability in either direction — don't assume it rises.
</details>

### Q6 — Cards, both directions
A single card is drawn from a standard deck.
**(a)** Given it is a face card, find P(it is a heart).
**(b)** Given it is a heart, find P(it is a face card).

<details>
<summary>Solution</summary>

Face cards: J, Q, K in each of 4 suits → 12. Hearts → 13. Intersection: 3.

**(a)** $\dfrac{3}{12} = \boxed{\tfrac14}$

**(b)** $\dfrac{3}{13} = \boxed{\tfrac3{13}}$

**Same intersection, different denominators.** $P(A\mid B)\ne P(B\mid A)$ in general — reversing a conditional requires Bayes, not swapping the letters.
</details>

### Q7 — Three children, at least one girl
Given at least one of three children is a girl, find P(all three are girls).

<details>
<summary>Solution</summary>

$S$ has $2^3 = 8$ outcomes. Only $BBB$ is eliminated → 7 survive. One of them is $GGG$.

$$P = \boxed{\tfrac17}$$
</details>

### Q8 — Three children, eldest is a girl
Given the **eldest** of three children is a girl, find P(all three are girls).

<details>
<summary>Solution</summary>

Fixing the eldest as $G$ leaves 2 free children → $2^2 = 4$ outcomes survive: $\{GBB, GBG, GGB, GGG\}$.

$$P = \boxed{\tfrac14}$$

**Compare Q7 ($1/7$) with Q8 ($1/4$).** Naming a child collapses the space far more aggressively than "at least one" — and the gap widens as the family grows. With $n$ children: "at least one girl" gives $\frac{1}{2^n-1}$, "eldest is a girl" gives $\frac{1}{2^{n-1}}$.
</details>

---

## Section C — Non-Uniform Spaces

### Q9 — Die rolled until a 6, max 3 rolls
A die is rolled until a 6 appears, or 3 rolls maximum. Given **no 6 on the first roll**, find P(exactly 3 rolls are needed).

<details>
<summary>Solution</summary>

Same structure as Q1 with $p = \tfrac16$.

Given roll 1 is not a 6, roll 2 is guaranteed. Three rolls occur iff roll 2 is *also* not a 6.

$$P = \boxed{\tfrac56}$$

**Long form, to confirm:** the conditioned space is $\{T6,\; TT6,\; TTT\}$ where $T$ = "not a 6", with probabilities $\tfrac56\cdot\tfrac16 = \tfrac5{36}$, $\tfrac{25}{36}\cdot\tfrac16 = \tfrac{25}{216}$, $\tfrac{125}{216}$.

Denominator: $\tfrac{30+25+125}{216} = \tfrac{180}{216} = \tfrac56$
Numerator (3 rolls): $\tfrac{25+125}{216} = \tfrac{150}{216}$

$$\frac{150/216}{180/216} = \frac{150}{180} = \tfrac56 \;\checkmark$$
</details>

### Q10 — Coin, the mirror event
Coin tossed until a head, max 3 tosses. Given no head on the first toss, find P(**exactly 2** tosses are needed).

<details>
<summary>Solution</summary>

"Exactly 2 tosses" $= \{TH\}$, probability $\tfrac14$. Denominator unchanged at $\tfrac12$.

$$P = \frac{1/4}{1/2} = \boxed{\tfrac12}$$

**Check:** given a tail first, the experiment must end in either 2 or 3 tosses. $\tfrac12+\tfrac12 = 1$ ✓ Complementary events inside a conditioned space still sum to 1.
</details>

### Q11 — Coin, condition on the far end
Coin tossed until a head, max 3 tosses. Given **at least 2 tosses** were needed, find P(a head eventually appeared).

<details>
<summary>Solution</summary>

"At least 2 tosses" ⟺ toss 1 was a tail → shrunk space $\{TH,\, TTH,\, TTT\}$, total $\tfrac12$.

"A head appeared" within that space $= \{TH,\, TTH\}$, probability $\tfrac14+\tfrac18 = \tfrac38$.

$$P = \frac{3/8}{1/2} = \boxed{\tfrac34}$$

**Sanity check:** unconditionally, $P(\text{head appears}) = 1 - \tfrac18 = \tfrac78$. Learning that the first toss failed makes eventual success *less* likely ($\tfrac34 < \tfrac78$) — you've burned one of your three chances. The direction of movement makes sense.
</details>

### Q12 — Two draws, condition on the second
A bag has 4 red and 6 blue balls. Two are drawn without replacement.
Given the **second** ball is red, find P(the first was also red).

<details>
<summary>Solution</summary>

$$P(R_1\mid R_2) = \frac{P(R_1\cap R_2)}{P(R_2)}$$

$P(R_1\cap R_2) = \tfrac4{10}\cdot\tfrac39 = \tfrac{12}{90}$

$P(R_2) = \tfrac4{10}$ by symmetry (or: $\tfrac4{10}\cdot\tfrac39 + \tfrac6{10}\cdot\tfrac49 = \tfrac{12+24}{90} = \tfrac{36}{90} = \tfrac25$)

$$P = \frac{12/90}{36/90} = \boxed{\tfrac13}$$

**Note the direction:** we conditioned on a *later* event to infer an *earlier* one. Conditional probability has no built-in arrow of time — it is pure bookkeeping over a restricted space.
</details>

---

## Section D — Mixed Practice

### Q13
A family has 3 children. Given that **at least two** are girls, find P(all three are girls).

<details>
<summary>Solution</summary>

At least 2 girls: $\{GGB, GBG, BGG, GGG\}$ — 4 outcomes.

$$P = \boxed{\tfrac14}$$
</details>

### Q14
Two dice are rolled. Given that the two numbers **differ**, find P(the sum is 7).

<details>
<summary>Solution</summary>

Numbers differ: $36-6 = 30$ outcomes.

Sum 7: $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ — 6 outcomes, none of which is a double, so all 6 survive.

$$P = \frac{6}{30} = \boxed{\tfrac15}$$

Unconditionally $P(\text{sum }7) = \tfrac16$. Removing the doubles — none of which can sum to 7 — removes only unfavourable outcomes, so the probability rises.
</details>

### Q15
A card is drawn from a deck. Given that it is **red**, find P(it is a king **or** a heart).

<details>
<summary>Solution</summary>

Shrunk space: 26 red cards.

Red kings: 2. Hearts: 13. Overlap (king of hearts): 1.

$$n(\text{king or heart, among red}) = 2+13-1 = 14$$

$$P = \frac{14}{26} = \boxed{\tfrac7{13}}$$

**The addition rule still needs its overlap term** even inside a conditioned space — conditioning changes the universe, not the rules.
</details>

---

## Decision Checklist

| Signal | What to do |
|---|---|
| "Given that…", "if it is known that…" | Identify $C$, shrink the space to $C$ |
| Outcomes equally likely | Count: $n(A\cap C)/n(C)$ |
| "Repeat until…" experiment | **Not** equally likely — sum probabilities |
| "At least one X" | Remove only the all-not-X outcome |
| "The first/eldest/specified one is X" | Fix that slot; far smaller space |
| Conditioning on a *later* event | Fine — use Bayes or the definition directly |

**Before committing:**
1. Did you renormalise, i.e. is the denominator $P(C)$ and not 1?
2. Are the outcomes you counted genuinely equally likely?
3. Does $A$ sit inside $C$? If so the numerator is just $P(A)$.
4. Does the conditional probability move in a direction that makes sense versus the unconditional one?
