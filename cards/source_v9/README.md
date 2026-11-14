# Cards N5 and B1 (13 November 2026)

Two 1080×1350 card videos, 16 s each, built like cards P1–P4: every number comes from a model or a run, and nothing is drawn by hand.

**N5: At the wall, the kept mode turns sideways** (`../N5_Kept_Mode_At_The_Wall_v1.mp4`)
- The kept-sector mode f(μ) = 1/(s + κ + ikμ) on the sphere of directions, with s = k cot(k/κ) − κ. Both the right and the left eigenvector are shown, coloured by phase.
- As κ falls to 2k/π, three things happen:
  - the mode flattens into the directions sideways to the wave (88.7% of |f|² within |μ| < 0.1 near the wall);
  - the left–right overlap sin 2φ/2φ falls to zero;
  - the pole walks to the centre of the cut.
- Checks in `data_N5.py`:
  - the 400-moment chain eigenvector equals the closed form to 5e-15;
  - K by quadrature equals 4φ²/sin²2φ to 2e-15.
- The pole and the onset are Romatschke's (2016, Eq. 37).

**B1: Same density. Same flux. Same stress. Different future.** (`../B1_Twin_Collapse_v1.mp4`)
- The setup is the restart-test pair of the paper: S. McCormick's GR code at commit eb7c4de, restarted at ε = 2 with hidden ℓ = 3 structure of opposite sign. The pair is rerun here at δ = 0.5107, between the two thresholds.
- At the restart the two states are:
  - bit-identical in the fluid and metric arrays;
  - equal in ℓ = 0, 1, 2 and 4 to 1e-16;
  - different only in ℓ = 3 (−0.0373 against +0.0382 of the density).
- The ℓ₃-negative twin reaches an apparent horizon at ε = 5.289. The ℓ₃-positive twin disperses at ε = 5.618.

## Rebuilding
1. `python3 twin_run.py 0.5107 minus` and `python3 twin_run.py 0.5107 plus`. These run in the A4 restart folder, with `restart.py` and McCormick's `ms_nuc.py` and `ms_fluid.py`.
2. `python3 data_B1.py`, then `python3 data_N5.py`.
3. `node capture.js N5 video out.mp4` and `node capture.js B1 video out.mp4`. These need `three.min.js` and Playwright, as for cards P1–P4.

Jeromie Beasley · CC BY 4.0
