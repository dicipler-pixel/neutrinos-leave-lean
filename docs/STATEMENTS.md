# Headline statements

The statements below are copied from the Lean source. `κ`, `σ` and the other Greek letters are real numbers unless a type is given.

## CrossLink

```lean
theorem crossLink (a b h : ℂ) :
    |2 * (starRingEnd ℂ a * (-I * h * b)).re| ≤ 2 * ‖h‖ * ‖a‖ * ‖b‖
```

```lean
theorem crossLink_sq (a b h : ℂ) (A R : ℝ) (hA : A = ‖a‖ ^ 2) (hR : R = ‖b‖ ^ 2)
    (hAR : A + R ≤ 1) :
    (2 * (starRingEnd ℂ a * (-I * h * b)).re) ^ 2 ≤ 4 * ‖h‖ ^ 2 * A * (1 - A)
```

```lean
theorem crossLink_sq_k (a b : ℂ) (k : ℝ) (A R : ℝ) (hA : A = ‖a‖ ^ 2) (hR : R = ‖b‖ ^ 2)
    (hAR : A + R ≤ 1) :
    (2 * (starRingEnd ℂ a * (-I * ((k / Real.sqrt 3 : ℝ) : ℂ) * b)).re) ^ 2
      ≤ 4 * (k ^ 2 / 3) * A * (1 - A)
```

## TwoMoment

```lean
theorem twoMomentConnectionEnergy (k κ : ℝ) :
    (1 / 8) * frobSq (selfComm (L2 (k / Real.sqrt 3) κ)) = κ ^ 2 * (k ^ 2 / 3)
```

## SplitRate

```lean
theorem splitRateEnergy (k κ1 κ2 : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 (k / Real.sqrt 3) (2 * k / Real.sqrt 15) κ1 κ2))
      = k ^ 2 * κ1 ^ 2 / 3 + (4 * k ^ 2 / 15) * (κ2 - κ1) ^ 2
```

```lean
theorem splitRateEnergy_ab (a b κ1 κ2 : ℝ) :
    (1 / 8) * frobSq (selfComm (L3 a b κ1 κ2)) = a ^ 2 * κ1 ^ 2 + b ^ 2 * (κ2 - κ1) ^ 2
```

## Shear

```lean
theorem R00_one : R00 1 = 32 / 37
```

```lean
theorem R00_eq_cf (x : ℝ) (hx : -1 < x) : R00 x = cf x
```

```lean
theorem R00_hasDerivAt : HasDerivAt R00 (-5 / 1369) 1
```

```lean
theorem shearEnergy_hasDerivAt : HasDerivAt shearEnergy 0 1
```

```lean
theorem shearCounterexample :
    R00 1 = 32 / 37 ∧ HasDerivAt R00 (-5 / 1369) 1 ∧ HasDerivAt shearEnergy 0 1
      ∧ (-5 / 1369 : ℝ) ≠ 0
```

## ShearComplex

```lean
theorem resolvent_00_eq_cf (a b x : ℝ) (ha : a ^ 2 = 1 / 3) (hb : b ^ 2 = 4 / 15) (hx : -1 < x) :
    (Aresp a b x)⁻¹ 0 0 = ((cf x : ℝ) : ℂ)
```

```lean
theorem resolvent_00_at_one (a b : ℝ) (ha : a ^ 2 = 1 / 3) (hb : b ^ 2 = 4 / 15) :
    (Aresp a b 1)⁻¹ 0 0 = ((32 / 37 : ℝ) : ℂ)
```

## Propagator

```lean
theorem scalarCollisionPropagator (X : Matrix (Fin n) (Fin n) ℂ) (σ t : ℝ) :
    exp (t • (X - σ • (1 : Matrix (Fin n) (Fin n) ℂ)))
      = (Real.exp (-σ * t)) • exp (t • X)
```

```lean
theorem commute_shifted (X : Matrix (Fin n) (Fin n) ℂ) (a b : ℝ) :
    Commute (X - a • (1 : Matrix (Fin n) (Fin n) ℂ)) (X - b • (1 : Matrix (Fin n) (Fin n) ℂ))
```

```lean
theorem two_step_propagator (X : Matrix (Fin n) (Fin n) ℂ) (σ₁ σ₂ t₁ t₂ : ℝ) :
    exp (t₁ • (X - σ₁ • (1 : Matrix (Fin n) (Fin n) ℂ)) + t₂ • (X - σ₂ • (1 : Matrix (Fin n) (Fin n) ℂ)))
      = exp (t₁ • (X - σ₁ • (1 : Matrix (Fin n) (Fin n) ℂ)))
        * exp (t₂ • (X - σ₂ • (1 : Matrix (Fin n) (Fin n) ℂ)))
```

## KillLine

```lean
theorem testD_verdict :
    (15 / 100 : ℚ) ≤ G (50245 / 100000) ∧ G (50245 / 100000) ≤ 16 / 100
      ∧ |G (50245 / 100000) - 1176 / 10000| < 8 / 100
      ∧ 8 / 100 < |G (50245 / 100000) - 30 / 100|
```

```lean
theorem testC_verdict :
    |G (51756 / 100000) - 6625 / 10000| < 8 / 100
      ∧ |G (51756 / 100000) - 683 / 1000| < 8 / 100
```

```lean
theorem testB_verdict :
    |G (50743 / 100000) - 246 / 1000| < 8 / 100
      ∧ 8 / 100 < |G (50743 / 100000) - 431 / 1000|
```
