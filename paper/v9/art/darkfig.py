# SCRIPT: NU-V9-DARKFIG  put a figure on the page's dark ground without redrawing it
# Each pixel keeps its hue and saturation; only its lightness is flipped and rescaled: white -> the page's dark ground,
# black -> cream. Nothing is moved, resized, redrawn or relabelled, so every line, point, number and label stays where it was.
# The map is one-to-one, so it can be undone: undo(dark(x)) returns the original picture to within 8-bit rounding (checked below).
import numpy as np
L_WHITE, L_BLACK = 0.050, 0.930          # lightness given to white and to black (ground = rgb(6,9,20) has lightness 0.051)

def rgb_to_hls(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; mx = a.max(-1); mn = a.min(-1); l = (mx + mn) / 2; d = mx - mn
    s = np.where(d == 0, 0, d / np.where(l > 0.5, 2 - mx - mn, mx + mn + 1e-12))
    dd = np.where(d == 0, 1, d)
    h = np.where(mx == r, ((g - b) / dd) % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4)) / 6
    return np.where(d == 0, 0, h), l, s
def hls_to_rgb(h, l, s):
    c = (1 - np.abs(2 * l - 1)) * s; hp = h * 6; x = c * (1 - np.abs(hp % 2 - 1)); m = l - c / 2; z = np.zeros_like(h)
    i = np.floor(hp).astype(int) % 6
    r = np.choose(i, [c, x, z, z, x, c]); g = np.choose(i, [x, c, c, x, z, z]); b = np.choose(i, [z, z, x, c, c, x])
    return np.stack([r + m, g + m, b + m], -1)
def tint(l):                                # the ground is slightly blue: a neutral pixel takes the ground's tint in proportion to its darkness
    return l
def dark(rgb8):
    a = rgb8.astype(np.float64) / 255; h, l, s = rgb_to_hls(a)
    l2 = L_WHITE + (1 - l) * (L_BLACK - L_WHITE)
    out = hls_to_rgb(h, l2, s)
    return np.clip(np.rint(out * 255), 0, 255).astype(np.uint8)
def undo(rgb8):
    a = rgb8.astype(np.float64) / 255; h, l, s = rgb_to_hls(a)
    l0 = 1 - (l - L_WHITE) / (L_BLACK - L_WHITE)
    out = hls_to_rgb(h, np.clip(l0, 0, 1), s)
    return np.clip(np.rint(out * 255), 0, 255).astype(np.uint8)

if __name__ == '__main__':
    import sys, re, io, base64
    from PIL import Image
    t = open(sys.argv[1], encoding='utf-8').read()
    for i, m in enumerate(re.finditer(r'<img src="data:image/png;base64,([^"]+)"', t)):
        im = np.array(Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB'))
        d = dark(im); u = undo(d); err = np.abs(u.astype(int) - im.astype(int))
        print(f'fig {i+1}: {im.shape[1]}x{im.shape[0]}  white -> {tuple(dark(np.array([[[255,255,255]]],dtype=np.uint8))[0,0])}  undo error: max {err.max()}, mean {err.mean():.3f}, pixels off by more than 3: {(err.max(-1) > 3).mean()*100:.3f}%')
        Image.fromarray(d).save(f'darkfig_{i+1:02d}.png')
