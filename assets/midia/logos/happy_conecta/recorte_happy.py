"""Recorta o logo Happy Conecta da arte original (JPEG sobre foto) em PNG transparente."""
import sys, os
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
im = np.array(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = im.shape
R, G, B = im[..., 0], im[..., 1], im[..., 2]

# 1. Máscara do que é logo (turquesa ou branco claro)
turq = (np.minimum(G, B) - R) > 45
white = (R > 150) & (G > 150) & (B > 140)
core = turq | white
# só a região do logo (fora disso é foto)
reg = np.zeros_like(core); reg[480:1240, 520:1980] = True
core &= reg

def _box1d(a, r, axis):
    a = np.swapaxes(a, 0, axis)
    p = np.concatenate([np.repeat(a[:1], r + 1, 0), a, np.repeat(a[-1:], r, 0)])
    c = np.cumsum(p, axis=0, dtype=np.float64)
    out = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1)
    return np.swapaxes(out.astype(np.float32), 0, axis)

def blur(a, r):
    """Aproximação gaussiana: 3 passadas de box blur."""
    a = a.astype(np.float32); k = max(1, int(r * 0.6))
    for _ in range(3):
        a = _box1d(_box1d(a, k, 0), k, 1)
    return a

def dilate(m, r):
    return blur(m.astype(np.float32), r) > 0.02

near = dilate(core, 18)       # área onde o brilho existe
known = ~dilate(core, 30)     # pixels seguramente de fundo

# 2. Fundo estimado (convolução normalizada a partir do fundo conhecido)
w = known.astype(np.float32)
bg = np.zeros_like(im)
for c in range(3):
    num = blur(im[..., c] * w, 45); den = blur(w, 45)
    bg[..., c] = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0)
bg = np.minimum(bg, im)  # fundo nunca mais claro que a imagem

# 3. Cor-alvo por pixel: turquesa da marca ou branco
TQ = np.array([0, 206, 201], np.float32); WH = np.array([255, 255, 255], np.float32)
wfac = np.clip((R - 70) / 110, 0, 1)[..., None]
T = wfac * WH + (1 - wfac) * TQ

# 4. Alfa: quanto da cor-alvo é preciso para ir do fundo à imagem
den = T - bg
ratio = np.where(den > 40, (im - bg) / np.maximum(den, 1), 0)
alpha = np.clip(ratio.max(axis=2), 0, 1)
alpha[~near] = 0
alpha = np.where(alpha < 0.05, 0, (alpha - 0.05) / 0.95)

# 5. Cor sem o fundo
a3 = np.maximum(alpha, 1e-3)[..., None]
col = np.clip((im - (1 - alpha[..., None]) * bg) / a3, 0, 255)
col = np.where(alpha[..., None] > 0, col, 0)

# 6. Corte justo com margem
ys, xs = np.where(alpha > 0.02)
pad = 40
y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, H)
x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, W)
rgba = np.dstack([col, alpha * 255])[y0:y1, x0:x1].astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(f'{out}/happy-conecta-logo.png', optimize=True)

# Versões monocromáticas (sem brilho: alfa mais firme)
a = alpha[y0:y1, x0:x1]
solid = np.clip((a - 0.55) / 0.2, 0, 1)
for name, rgb in [('branco', (255, 255, 255)), ('marinho', (0x1B, 0x2A, 0x4A))]:
    m = np.zeros((*a.shape, 4), np.uint8); m[..., :3] = rgb; m[..., 3] = (solid * 255).astype(np.uint8)
    Image.fromarray(m, 'RGBA').save(f'{out}/happy-conecta-logo-{name}.png', optimize=True)

# Arte original recortada (com a foto)
Image.fromarray(im[y0:y1, x0:x1].astype(np.uint8)).save(f'{out}/happy-conecta-logo-com-fundo-original.jpg', quality=95)
print('bbox', x0, x1, y0, y1, 'size', x1 - x0, y1 - y0)
