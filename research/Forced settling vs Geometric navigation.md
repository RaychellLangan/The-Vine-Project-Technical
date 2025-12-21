# Forced Settling vs Geometric Navigation
## Why Deep Learning Hallucinates (And What We're Missing)

---

## The Uncomfortable Question

Why do models with hundreds of billions of parameters still hallucinate? Why do they fail catastrophically on distribution shift? Why does every "fix" (RLHF, constitutional AI, retrieval augmentation) feel like patching symptoms rather than solving root causes?

This paper proposes an answer: **loss-based training forces models into configurations the underlying geometry doesn't support.**

---

## 1. What Loss-Based Training Actually Does

The standard paradigm:

```
Forward pass → Compute loss → Backpropagate → Update weights → Repeat
```

The goal: minimize loss until the model produces desired outputs.

The assumption: parameter space contains stable configurations for correct behaviour, and gradient descent will find them.

**The problem:** Gradient descent doesn't care about geometric stability. It forces models toward low-loss regions whether or not those regions represent natural attractors.

Think of it like pushing a ball up a hill and expecting it to stay there. It might, if you keep pushing. But remove the pressure and it rolls back down.

Loss-based training is the pushing. The trained weights are the pressure. Remove context, shift distribution, ask something slightly novel - and the model rolls.

---

## 2. Forced Basins vs Natural Attractors

A **natural attractor** is a stable configuration - perturb the system and it returns to equilibrium on its own. No external pressure required.

A **forced basin** requires constant pressure to maintain. The system doesn't want to be there. It's being held in place.

| Natural Attractor | Forced Basin |
|-------------------|--------------|
| Returns after perturbation | Collapses without pressure |
| Generalizes naturally | Memorizes specific cases |
| Knows its boundaries | Confident everywhere |
| Minimal energy to maintain | Requires massive overhead |

**Claim:** Most of what we call "learning" in deep networks is forced settling, not natural attractor formation.

---

## 3. This Explains Everything Frustrating About LLMs

### Hallucination

When a model is queried in regions where the forced basin has no geometric support:

```
Query outside training distribution
        ↓
Forced basin doesn't extend here
        ↓
Model interpolates from unstable position
        ↓
Confident, coherent, wrong
```

Hallucination isn't a bug. It's the natural consequence of forcing models into configurations that don't actually exist as stable geometries. The model doesn't know it's confabulating because *from inside the forced basin*, everything feels fine.

### Parameter Inflation

If you're forcing a system somewhere it doesn't naturally want to be, you need a lot of machinery to hold it there. 

Billions of parameters aren't learning billions of concepts. They're compensating for geometric instability. Most of those parameters are scaffolding for forced basins, not representations of knowledge.

### Brittleness

Forced basins are stable only under the pressure that created them (training distribution). Shift that distribution and the pressure misaligns. The basin doesn't just perform worse - it collapses.

Natural attractors degrade gracefully. Forced basins fail catastrophically.

### The Compensation Stack

Look at modern ML "solutions":
- RLHF (more forcing, different direction)
- Constitutional AI (rules preventing basin escape)
- Retrieval augmentation (external scaffolding)
- Prompt engineering (users compensating for instability)
- Chain-of-thought (explicit reasoning as stabilization)
- Guardrails (catch basin collapse before it reaches users)

Each intervention compensates for the same root issue: the model was forced somewhere the geometry doesn't naturally support.

We're not improving intelligence. We're building more elaborate support structures for unstable configurations.

---

## 4. The Alternative: Geometric Navigation

What if instead of forcing basin settling, we:

1. **Provided geometric substrate** - manifold structure containing natural attractors
2. **Allowed observation** - minimal components to perceive position on manifold
3. **Enabled navigation** - mechanisms to explore the basin landscape
4. **Let settling happen naturally** - system finds stable attractors without forcing

In this paradigm:
- Parameters scale with **basins to distinguish**, not task complexity
- Behaviour emerges from geometry, not from forced associations
- Generalisation is natural because attractors extend beyond training points
- The system knows what it doesn't know (queries outside basins produce uncertainty, not confabulation)

---

## 5. Reflexes vs Deliberation

There's a biological parallel worth considering.

**Reflexes:** Hardwired stimulus→response. Fast, reliable, no flexibility. Touch hot thing → withdraw hand. No "thinking" involved.

**Deliberation:** Holding multiple possibilities, navigating between them, settling on a choice. Slower, flexible, adaptive.

Loss-based training produces reflexes. Very sophisticated reflexes, but reflexes nonetheless. Pattern in → response out. No actual navigation between possibilities.

What we want from AI - reasoning, judgment, genuine understanding - requires deliberation. The ability to hold uncertainty, explore options, and settle naturally rather than react automatically.

Current architectures don't support this. They're reflex machines scaled up.

---

## 6. Implications

If this framing is correct:

**Scaling won't solve the core problems.** More parameters just means more elaborate forcing. The geometry is still wrong.

**Alignment via RLHF is inherently unstable.** You're adding forcing pressure on top of forcing pressure. The basin isn't becoming more natural - it's becoming more constrained.

**Hallucination can't be "fixed" without architectural change.** It's not a bug to patch. It's a symptom of forced settling.

**Parameter efficiency is a sign of geometric correctness.** If a smaller model matches a larger one, the smaller one likely has better geometric structure.

**True generalisation requires natural attractors.** You can't force your way to general intelligence. You have to find (or construct) geometries that naturally support the behaviours you want.

---

## 7. The Research Direction

The question shifts from:

> "How do we force models to behave correctly?"

To:

> "What geometries naturally support the behaviours we want?"

This is a different research program. It's not about bigger models, better loss functions, or more training data. It's about understanding the mathematical structures that underlie cognition and building systems that embody those structures directly.

Some existing work points in this direction:
- Energy-based models (basins as energy minima)
- Hopfield networks (attractor dynamics)
- Geometric deep learning (manifold structure)
- Dynamical systems approaches

But the mainstream continues optimizing loss functions on ever-larger models, adding ever-more compensation layers.

We might be building the most elaborate reflex machines in history while the path to actual intelligence requires something fundamentally different.

---

## 8. Conclusion

Deep learning's failures aren't implementation bugs. They're symptoms of a paradigm that forces models into geometrically unstable configurations and then compensates endlessly for that instability.

The alternative - geometric navigation with natural basin settling - requires rethinking architecture from first principles. It's a harder path than scaling existing approaches.

But if we want systems that genuinely reason rather than elaborately flinch, we might not have a choice.

---

*The geometry is there whether we see it or not. The question is whether we keep pushing against it or learn to work with it.*

---

## Further Reading

- Hopfield, J.J. (1982). Neural networks and physical systems with emergent collective computational abilities.
- Friston, K. (2010). The free-energy principle: a unified brain theory?
- Bronstein, M. et al. (2021). Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges.
- Minsky & Papert (1969). Perceptrons.

---

Raychell Langan, Nexicog, dec 2025
