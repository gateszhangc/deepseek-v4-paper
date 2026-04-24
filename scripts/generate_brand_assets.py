from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets" / "brand"
PHILOSOPHY_PATH = ROOT / "brand" / "signal-lattice.md"
FONT_DIR = ROOT / "assets" / "fonts"
FALLBACK_FONT_DIR = Path("/Users/a1-6/.codex/skills/canvas-design/canvas-fonts")

COLORS = {
    "ink": "#061018",
    "panel": "#0a1722",
    "cyan": "#8BE7D2",
    "cyan_soft": "#73CDBD",
    "sand": "#E7D09B",
    "mist": "#E9F2F0",
    "line": "#173243",
    "glow": "#143540",
}


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def font(name, size):
    path = FONT_DIR / name
    if not path.exists():
        path = FALLBACK_FONT_DIR / name
    return ImageFont.truetype(str(path), size=size)


def linear_gradient(size, start, end):
    width, height = size
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    start_rgb = hex_rgba(start)
    end_rgb = hex_rgba(end)
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * ratio) for i in range(4))
        draw.line([(0, y), (width, y)], fill=color)
    return image


def draw_grid(draw, size, spacing, color, margin):
    width, height = size
    for x in range(margin, width - margin + 1, spacing):
        draw.line([(x, margin), (x, height - margin)], fill=color, width=1)
    for y in range(margin, height - margin + 1, spacing):
        draw.line([(margin, y), (width - margin, y)], fill=color, width=1)


def draw_mark(draw, box, line_color, accent_color, fill_color=None):
    x0, y0, x1, y1 = box
    width = x1 - x0
    height = y1 - y0
    inset = int(width * 0.12)
    stroke = max(4, int(width * 0.03))
    inner_box = (x0 + inset, y0 + inset, x1 - inset, y1 - inset)

    if fill_color:
        draw.rounded_rectangle(box, radius=int(width * 0.18), fill=fill_color)
    draw.rounded_rectangle(inner_box, radius=int(width * 0.12), outline=line_color, width=stroke)

    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    radius_outer = int(width * 0.23)
    radius_inner = int(width * 0.14)
    orbital_box = (cx - radius_outer, cy - radius_outer, cx + radius_outer, cy + radius_outer)
    draw.arc(orbital_box, start=220, end=28, fill=line_color, width=stroke)
    draw.arc(orbital_box, start=40, end=180, fill=hex_rgba(COLORS["cyan_soft"]), width=stroke)

    inner_orbit = (cx - radius_inner, cy - radius_inner, cx + radius_inner, cy + radius_inner)
    draw.arc(inner_orbit, start=10, end=200, fill=line_color, width=max(3, stroke - 2))

    bracket_x = x0 + width * 0.28
    draw.line([(bracket_x, y0 + height * 0.3), (bracket_x, y0 + height * 0.7)], fill=line_color, width=stroke)
    draw.line(
        [(bracket_x, y0 + height * 0.3), (bracket_x + width * 0.12, y0 + height * 0.3)],
        fill=line_color,
        width=stroke,
    )
    draw.line(
        [(bracket_x, y0 + height * 0.7), (bracket_x + width * 0.12, y0 + height * 0.7)],
        fill=line_color,
        width=stroke,
    )

    node_r = max(5, int(width * 0.028))
    nodes = [
        (cx + width * 0.18, cy - height * 0.18),
        (cx + width * 0.2, cy + height * 0.18),
        (cx - width * 0.02, cy - height * 0.24),
    ]
    for nx, ny in nodes:
        draw.ellipse((nx - node_r, ny - node_r, nx + node_r, ny + node_r), fill=accent_color)

    core_r = int(width * 0.06)
    draw.ellipse((cx - core_r, cy - core_r, cx + core_r, cy + core_r), fill=accent_color)


def add_noise_overlay(base, opacity=18):
    noise = Image.effect_noise(base.size, 18).convert("L")
    noise = noise.point(lambda v: opacity if v > 132 else 0)
    overlay = Image.new("RGBA", base.size, hex_rgba(COLORS["mist"], 0))
    overlay.putalpha(noise)
    return Image.alpha_composite(base, overlay)


def save_logo_mark():
    size = (512, 512)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_mark(
        draw,
        (24, 24, 488, 488),
        hex_rgba(COLORS["cyan"]),
        hex_rgba(COLORS["sand"]),
        fill_color=hex_rgba(COLORS["ink"], 218),
    )
    image.save(ASSETS_DIR / "logo-mark.png")


def save_favicon():
    size = (256, 256)
    image = linear_gradient(size, COLORS["ink"], COLORS["panel"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 12, 244, 244), radius=52, outline=hex_rgba(COLORS["line"]), width=2)
    draw_mark(draw, (30, 30, 226, 226), hex_rgba(COLORS["cyan"]), hex_rgba(COLORS["sand"]), None)
    image = add_noise_overlay(image)
    image.save(ASSETS_DIR / "favicon.png")


def save_apple_touch():
    size = (180, 180)
    image = linear_gradient(size, COLORS["ink"], COLORS["panel"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((10, 10, 170, 170), radius=38, outline=hex_rgba(COLORS["line"]), width=2)
    draw_mark(draw, (22, 22, 158, 158), hex_rgba(COLORS["cyan"]), hex_rgba(COLORS["sand"]), None)
    image = add_noise_overlay(image, opacity=14)
    image.save(ASSETS_DIR / "apple-touch-icon.png")


def save_wordmark():
    size = (1500, 480)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_mark(
        draw,
        (24, 48, 360, 384),
        hex_rgba(COLORS["cyan"]),
        hex_rgba(COLORS["sand"]),
        fill_color=hex_rgba(COLORS["ink"], 206),
    )

    display = font("Tektur-Medium.ttf", 124)
    support = font("InstrumentSans-Regular.ttf", 46)
    micro = font("GeistMono-Regular.ttf", 24)

    draw.text((414, 62), "DEEPSEEK V4", font=display, fill=hex_rgba(COLORS["mist"]))
    draw.text((420, 222), "PAPER", font=support, fill=hex_rgba(COLORS["cyan"]))
    draw.line((420, 286, 1010, 286), fill=hex_rgba(COLORS["line"]), width=2)
    draw.text((420, 316), "OFFICIAL REPORT GUIDE / VERIFIED SOURCE INDEX", font=micro, fill=hex_rgba(COLORS["sand"]))
    image.save(ASSETS_DIR / "logo-wordmark.png")


def save_social_card():
    size = (1200, 630)
    image = linear_gradient(size, "#07111a", "#0c1f2a")
    draw = ImageDraw.Draw(image)
    draw_grid(draw, size, spacing=54, color=hex_rgba(COLORS["line"], 88), margin=54)

    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((770, -40, 1280, 470), fill=hex_rgba(COLORS["glow"], 135))
    glow_draw.ellipse((-180, 260, 320, 760), fill=hex_rgba("#102836", 110))
    glow = glow.filter(ImageFilter.GaussianBlur(36))
    image = Image.alpha_composite(image, glow)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((48, 48, 1152, 582), radius=28, outline=hex_rgba(COLORS["line"], 160), width=2)
    draw.rounded_rectangle((82, 96, 430, 444), radius=42, outline=hex_rgba(COLORS["cyan"], 200), width=3)
    draw_mark(draw, (112, 126, 400, 414), hex_rgba(COLORS["cyan"]), hex_rgba(COLORS["sand"]), None)

    eyebrow = font("GeistMono-Regular.ttf", 24)
    title = font("Tektur-Medium.ttf", 72)
    subtitle = font("InstrumentSerif-Regular.ttf", 34)
    body = font("InstrumentSans-Regular.ttf", 26)

    draw.text((470, 112), "INDEPENDENT REPORT GUIDE", font=eyebrow, fill=hex_rgba(COLORS["sand"]))
    draw.text((470, 160), "DeepSeek V4 Paper", font=title, fill=hex_rgba(COLORS["mist"]))
    draw.text((472, 254), "Toward highly efficient million-token context intelligence.", font=subtitle, fill=hex_rgba(COLORS["cyan"]))

    bullets = [
        "1M token context window across Pro and Flash",
        "Official architecture notes: CSA + HCA, mHC, Muon",
        "Benchmark snapshot, resources, and FAQ in one page",
    ]
    y = 340
    for bullet in bullets:
        draw.ellipse((472, y + 9, 484, y + 21), fill=hex_rgba(COLORS["sand"]))
        draw.text((504, y), bullet, font=body, fill=hex_rgba(COLORS["mist"], 230))
        y += 62

    draw.text((82, 536), PHILOSOPHY_PATH.stem.replace("-", " ").upper(), font=eyebrow, fill=hex_rgba(COLORS["cyan"], 210))
    draw.text((842, 536), "deepseekv4paper.lol", font=eyebrow, fill=hex_rgba(COLORS["sand"], 210))
    image = add_noise_overlay(image, opacity=12)
    image.save(ASSETS_DIR / "social-card.png")


def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    save_logo_mark()
    save_favicon()
    save_apple_touch()
    save_wordmark()
    save_social_card()


if __name__ == "__main__":
    main()
