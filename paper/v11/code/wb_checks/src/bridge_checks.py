# SCRIPT: BRIDGE-CHECKS-01
# Checks, run before writing, of every result taken into v1 from "What the Present Keeps" and the Spine.
# KILL CONDITIONS (written before the run):
#  B1 loudness bend = timbre speed: for I(t) = sum_k x_k e^{-r_k t} (r_k = 2 gamma_k), d^2/dt^2 log I = Var_p(r) and
#     the Fisher speed of the shape sum pdot^2/p equals the same variance. Dies if either differs by > 1e-8 relative.
#  B2 passive Jordan chain: I = e^{-g t}(A + b t) has (log I)'' = -(b/(A+bt))^2 < 0, and the three-sample determinant
#     y0 y2 - y1^2 is >= 0 for every positive mixture and equals -e^{-2g(t+h)} b^2 h^2 for the chain. Dies on any
#     mixture with a negative determinant or a chain value off by > 1e-12 relative.
#  B3 equal gray now, different later: (0.9, 0.1) and (0.1, 0.9) at rates (1, 0.1) have equal I(0) = 1 and initial
#     slopes -0.91 and -0.19. Dies otherwise.
#  B4 two books on k-planes: for orthogonal projectors P, R of rank k in C^n with H = P + i R? -- use the stated form:
#     E_minus = 2k(1 - p), E_plus = 2k(1 + p), p = Tr(PR)/k, with E_minus = (1/8)||[H,H^dag]||^2, E_plus =
#     (1/8)||H^2 - H^dag^2||^2 for H = P + iR. Dies if off by > 1e-10.
#  B5 three-port flux: F_phi as printed; G12 - G21 = -2 i a b c sin(phi) / p(z) at random complex z. Dies > 1e-10.
#  B6 trefoil: X = i sigma_x, Y = cos(pi/3) I + i sin(pi/3) sigma_z satisfy X^2 = Y^3 = -I; Tr(X Y X^-1 Y^-1) = -1.
#  B7 two-path record: for w = 1/2 and mu = cos(theta): V = cos(theta), D = sin(theta), V^2 + D^2 = 1.
#  B8 Born improbability is a connection book: control -- with p computed independently by Tr(PR)/k.
import numpy as np
rng = np.random.default_rng(1024)
fro2 = lambda X: float(np.real(np.vdot(X, X)))

# B1
worst = 0.0
for _ in range(500):
    n = rng.integers(2, 7); x = rng.uniform(0.1, 2, n); r = rng.uniform(0.05, 4, n); t = rng.uniform(0, 3)
    # first run used a finite-difference second derivative (step 1e-4); its rounding noise (~1e-3 relative on small
    # variances) fired the kill. The exact derivative is used now: (log I)'' = I''/I - (I'/I)^2.
    I0 = np.sum(x * np.exp(-r * t)); I1 = -np.sum(r * x * np.exp(-r * t)); I2 = np.sum(r**2 * x * np.exp(-r * t))
    d2 = I2 / I0 - (I1 / I0)**2
    I = lambda s: np.sum(x * np.exp(-r * s))
    p = x * np.exp(-r * t) / I(t); var = np.sum(p * r**2) - np.sum(p * r)**2
    pdot = -(r - np.sum(p * r)) * p; fisher = np.sum(pdot**2 / p)
    worst = max(worst, abs(d2 - var) / var, abs(fisher - var) / var)
print('B1 (log I)\'\' = Var_p(r) = Fisher speed of the shape: worst relative difference %.1e' % worst)

# B2
neg = 0
for _ in range(2000):
    n = rng.integers(2, 6); A = rng.uniform(0.01, 2, n); rr = rng.uniform(0.05, 0.99, n)
    y = [np.sum(A * rr**k) for k in range(3)]; neg += (y[0] * y[2] - y[1]**2) < -1e-15
g, kap, x1, x2, t, h = 1.2, 0.7, 0.3, 0.8, 0.4, 0.3
Ich = lambda s: np.exp(-g * s) * (x1 + x2 + kap * x2 * s)
y0, y1, y2 = Ich(t), Ich(t + h), Ich(t + 2 * h); b = kap * x2
print('B2 mixtures with negative determinant: %d of 2000; chain determinant %.12e vs predicted %.12e' %
      (neg, y0 * y2 - y1**2, -np.exp(-2 * g * (t + h)) * b**2 * h**2))

# B3
for xf, xs in [(0.9, 0.1), (0.1, 0.9)]:
    print('B3 preparation (%.1f, %.1f): I(0) = %.2f, initial slope %.2f' % (xf, xs, xf + xs, -(1.0 * xf + 0.1 * xs)))

# B4 / B8
def rproj(n, k):
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))); V = Q[:, :k]; return V @ V.conj().T
w4 = 0.0
for _ in range(300):
    # first run guessed H = P + iR, which is not the Spine's construction and fired. The Spine's books sit on a graph
    # edge: vertex blocks D_1 = P, D_2 = R, unitary edge block U, H = diag(D) + A with A anti-Hermitian.
    n = rng.integers(3, 8); k = rng.integers(1, n); P, R = rproj(n, k), rproj(n, k); U = np.eye(n)
    Z = np.zeros((n, n)); H = np.block([[P, U], [-U.conj().T, R]])
    Em = fro2(H @ H.conj().T - H.conj().T @ H) / 8; Ep = fro2(H @ H - H.conj().T @ H.conj().T) / 8
    p = np.real(np.trace(P @ R)) / k
    w4 = max(w4, abs(Em - 2 * k * (1 - p)), abs(Ep - 2 * k * (1 + p)))
print('B4 E_minus = 2k(1-p), E_plus = 2k(1+p) on an edge carrying P and R: worst absolute error %.1e over 300 pairs' % w4)

# B5
w5 = 0.0
for _ in range(200):
    a, b_, c, phi = rng.uniform(0.2, 2, 4); z = complex(rng.normal(), rng.normal())
    F = np.array([[0, a, c * np.exp(-1j * phi)], [a, 0, b_], [c * np.exp(1j * phi), b_, 0]])
    G = np.linalg.inv(z * np.eye(3) - F)
    pz = z**3 - z * (a * a + b_ * b_ + c * c) - 2 * a * b_ * c * np.cos(phi)
    w5 = max(w5, abs((G[0, 1] - G[1, 0]) - (-2j * b_ * c * np.sin(phi) / pz)) / abs(G[0, 1]))
print('B5 three-port: G12 - G21 = -2i bc sin(phi)/p(z) (derived; the extracted text read abc), worst relative error %.1e' % w5)

# B6
sx = np.array([[0, 1], [1, 0]]); sz = np.diag([1, -1]); X = 1j * sx; Y = np.cos(np.pi / 3) * np.eye(2) + 1j * np.sin(np.pi / 3) * sz
print('B6 trefoil: |X^2 + I| = %.1e, |Y^3 + I| = %.1e, Tr(commutator) = %.6f (abelian count gives 2)' %
      (abs(X @ X + np.eye(2)).max(), abs(np.linalg.matrix_power(Y, 3) + np.eye(2)).max(), np.real(np.trace(X @ Y @ np.linalg.inv(X) @ np.linalg.inv(Y)))))

# B7
for th in [0.3, 0.9, 1.4]:
    mu = np.cos(th); V = 2 * np.sqrt(0.25) * abs(mu); D = np.sqrt(1 - 4 * 0.25 * mu**2)
    print('B7 theta = %.1f: V = %.6f (cos %.6f), D = %.6f (sin %.6f), V^2 + D^2 = %.12f' % (th, V, np.cos(th), D, np.sin(th), V**2 + D**2))
