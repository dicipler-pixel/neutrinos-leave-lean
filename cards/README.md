# Atlas cards P1–P4 — When the Neutrinos Leave

Four 1080×1350 card videos (16 s each) drawn from the kinetic kept-sector model of the paper
(`paper/neutrinos_leave_v3_1.pdf`). Every number on a card is computed from the model in `source/`;
nothing is drawn by hand.

**P1 — Density boundary impedance, 2k/π** (`P1_Density_Boundary_Impedance_2k_over_pi_v1.mp4`)
The sphere of neutrino directions, with colour stripes winding as the density spreads out. Below it,
the memory kernel's running area settles on 2k/π, and a reflection disc shows the boundary barely
reflects at zero frequency (0.0488). The disc also shows that above frequency k the reflection is
total: there is no escape there.

**P2 — The onset** (`P2_Density_Pole_Onset_v1.mp4`)
A 3D landscape of the density's response over complex s while the collision rate sweeps up and down.
The density pole spikes up out of the cut exactly when the rate passes 2k/π. One panel shows cut-off
chains closing in on it: 200 moments give 0.645, 800 give 0.639.

**P3 — The door** (`P3_Door_First_Return_v1.mp4`)
The ℓ = 4 hidden difference on the direction sphere, next to a 3D ladder of moments that fills down
to the three fluid moments. The log-log slopes come out at exactly 1, 2 and 3, and the measured
coefficients match the exact formula to 1.000000.

**P4 — Henrici departure** (`P4_Henrici_Departure_Finite_v1.mp4`)
A tower of eigenvalues stacked by the number of moments. The hidden modes close in on the cut like
1/N, while the density pole stays put at −0.358, the same value P2's formula gives, so the two cards
check each other. The departure settles at 1.1745, E₋ holds at 1/3, and E₊ keeps growing.

## Rebuilding

```
cd source
python3 data.py            # recomputes cards_data.js from the model
node capture.js P1 video ../P1_Density_Boundary_Impedance_2k_over_pi_v1.mp4
```
`capture.js` renders `engine.js` + `card_P?.js` in headless Chromium (Playwright, 480 deterministic
frames) and encodes with ffmpeg. `node capture.js P1 still 0.5` writes a single frame at loop phase 0.5.

Jeromie Beasley · CC BY 4.0 (see `../LICENSE-CC-BY-4.0.md`)
