# Limitations

Lean checks the algebraic identities and inequalities of the finite moment model of the paper,
and the arithmetic of its pre-registered verdicts. Lean proves exactly the statements written,
under exactly the hypotheses written.

**Not formalized, and not checked by anything in this repository.**

- The nonlinear general-relativistic collapse runs, the threshold values `dc` they produce,
  and the two reference thresholds `49773/100000` and `52832/100000`. These are inputs. The
  verdict theorems check only that, given those numbers, the stated fractions `G` fall where the
  paper says they fall.
- Stephen McCormick's code, its numerical output, and the physical claim of his preprint that
  free-streaming neutrinos raise the threshold.
- The numerical witness for the shear counterexample. Lean proves the exact rational response
  `32/37` and its exact derivative `-5/1369` for the model written here; it does not check that
  the model is the right description of any collapsing region.
- Whether the Legendre moment hierarchy truncated at two or three moments is an adequate
  stand-in for the full free-streaming hierarchy. The theorems are statements about the
  truncations.
- The speed bound as a statement about trajectories. `CrossLink` proves the pointwise
  inequality `|2 Re(conj a * (-I h b))| <= 2 ||h|| ||a|| ||b||` and the bound
  `(2 Re(...))^2 <= 4 ||h||^2 A (1 - A)` that follows when `A + R <= 1`. That the paper's
  state satisfies `A + R <= 1` (a norm bound on a tridiagonal chain in which only the `l = 1`
  moment couples to the monopole) is a hypothesis here, not something Lean derives from the
  evolution equation.
- The time-ordered exponential. `ScalarCollisionPropagator` proves the constant-rate step
  `exp(t (X - sigma 1)) = exp(-sigma t) exp(t X)`, and the lemma that all generators
  `X - sigma(t) 1` commute pairwise, with the two-step product formula. The integral form
  `exp(-int sigma)` for a time-dependent `sigma(t)` is not stated in Lean.
- The shear counterexample is proved for `k = s = kappa1 = 1` and `kappa2` varying. The complex
  resolvent is proved as the inverse of the explicit `3 x 3` matrix for every real `a`, `b` with
  `a^2 = 1/3`, `b^2 = 4/15`, and every `kappa2 > -1`. Other parameter values are not covered.
- The connection energy uses the Frobenius norm of the self-commutator `[L, L^H]`. That this
  quantity is the right measure of non-normality for the paper's argument is the paper's claim.

**Stated with explicit hypotheses.** `R00_eq_cf` and the complex closed form need `kappa2 > -1`
so that no denominator vanishes. `crossLink_sq` takes `A = ||a||^2`, `R = ||b||^2` and
`A + R <= 1` as hypotheses.

**Left out because it could not be stated or proved cleanly here.** A `HasDerivAt` statement
for the complex resolvent entry as a function of `kappa2` (the real closed form is
differentiated and shown equal to the complex entry for `kappa2 > -1`, which gives the same
information); the integral propagator for time-dependent `sigma`.

**Version 4.1, `LinkVerdict`.** The verdicts take the threshold bracket edges as inputs, copied to ten decimals from
the run logs, and McCormick's reference thresholds as inputs. Lean does not check the collapse runs, the classification of
a run as a black hole or as dispersing, or the exclusion of runs that stopped on a numerical error. The odd rate itself
is defined through `ln Q / ln r`; Lean checks the equivalent whole-number comparisons `r^p ≤ Q^q`, not the logarithm.
