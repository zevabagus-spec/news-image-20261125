"""Build-time renderer for the news-image-20261125 entry.

Draws the poster that entry.png ships: one image summing up the world news
of Wednesday 25 November 2026, as reported that day. This script is kept in
the repository for provenance; the grader never runs it. The shipped
program is main.py, which copies the rendered entry.png to /output.

The stories, cross-checked across the day's reporting (Reuters via the
day's news briefs, Just Security's Early Edition, UN News, Principia):

  * Iran's Revolutionary Guard said oil tankers struck naval mines and
    caught fire in the Strait of Hormuz.
  * The United States proposed new tariffs on 14 trading partners, with
    headline rates of 20-40 percent.
  * Wall Street slid: the S&P 500 fell 2.2 percent and the Nasdaq 3.2
    percent as doubts over AI spending met tariff fears.
  * Shenzhou 24 carried Pakistan's first astronaut, Muhammad Zeeshan Ali,
    to China's space station - the first foreign astronaut to fly there.
  * Ukraine's drones sank a Russian warship in the Libyan port of
    Benghazi, killing two Libyan officers; Russian strikes hit Kyiv and
    Odesa the same day.
  * The COP31 climate talks ended without an agreement, and Pope Leo XIV
    voiced concern at the failure.
  * Also that day (ticker strip): Australia and the Solomon Islands
    signed a security treaty; Colombian forces freed every hostage in
    the Cartagena supermarket siege; RSF drone strikes killed 19
    civilians in Sudan; sport's highest court restored Senegal as
    Africa Cup champions.

Run locally with:  python3 render.py   (writes entry.png beside itself)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (246, 241, 231)
CARD = (255, 254, 249)
CARD_EDGE = (216, 208, 188)
NAVY = (20, 33, 61)
INK = (24, 28, 38)
SUB = (66, 72, 84)
GOLD = (232, 177, 60)
FAINT = (107, 114, 128)

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
BOLD = FONT_DIR / "LiberationSans-Bold.ttf"
REGULAR = FONT_DIR / "LiberationSans-Regular.ttf"


def font(size, bold=False):
    path = BOLD if bold else REGULAR
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_width, line_height, max_lines):
    lines = wrap(draw, text, fnt, max_width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_height
    return y


# ---------------------------------------------------------------- icons
# Each icon draws inside a 60x60 box whose top-left corner is (x, y),
# in a single ink colour on a light tint of that same colour.

def icon_tanker(d, x, y, ink):
    # Hull and deck of an oil tanker, a flame above the cargo, waves below.
    d.polygon([(x + 6, y + 36), (x + 54, y + 36), (x + 48, y + 47), (x + 12, y + 47)], fill=ink)
    d.rectangle([x + 13, y + 30, x + 40, y + 36], fill=ink)
    d.rectangle([x + 15, y + 22, x + 23, y + 30], fill=ink)
    d.polygon([(x + 44, y + 12), (x + 50, y + 24), (x + 44, y + 30), (x + 38, y + 24)], fill=(214, 96, 32))
    d.ellipse([x + 41, y + 20, x + 47, y + 29], fill=(240, 160, 40))
    for wx in (8, 24, 40):
        d.arc([x + wx, y + 48, x + wx + 12, y + 56], 0, 180, fill=ink, width=2)


def icon_tag(d, x, y, ink):
    # A price tag with a fat percent sign: tariffs.
    d.polygon([(x + 10, y + 12), (x + 36, y + 12), (x + 52, y + 28), (x + 28, y + 52), (x + 10, y + 34)], outline=ink, width=4)
    d.ellipse([x + 16, y + 18, x + 24, y + 26], outline=ink, width=3)
    d.text((x + 25, y + 21), "%", font=font(24, bold=True), fill=ink)


def icon_chart(d, x, y, ink):
    # Axes and a falling line with an arrowhead: the market sell-off.
    d.line([(x + 10, y + 8), (x + 10, y + 50)], fill=ink, width=3)
    d.line([(x + 10, y + 50), (x + 54, y + 50)], fill=ink, width=3)
    pts = [(x + 14, y + 16), (x + 26, y + 24), (x + 34, y + 19), (x + 48, y + 38)]
    d.line(pts, fill=(192, 57, 43), width=4, joint="curve")
    d.polygon([(x + 48, y + 38), (x + 38, y + 36), (x + 46, y + 28)], fill=(192, 57, 43))


def icon_rocket(d, x, y, ink):
    # A rocket climbing past two stars: Shenzhou 24.
    d.polygon([(x + 30, y + 4), (x + 38, y + 18), (x + 38, y + 36), (x + 22, y + 36), (x + 22, y + 18)], fill=ink)
    d.ellipse([x + 26, y + 15, x + 34, y + 23], fill=(246, 241, 231))
    d.polygon([(x + 22, y + 30), (x + 14, y + 42), (x + 22, y + 42)], fill=ink)
    d.polygon([(x + 38, y + 30), (x + 46, y + 42), (x + 38, y + 42)], fill=ink)
    d.polygon([(x + 25, y + 42), (x + 35, y + 42), (x + 30, y + 54)], fill=(240, 160, 40))
    for sx, sy in ((10, 10), (50, 16), (48, 44)):
        d.line([(x + sx - 3, y + sy), (x + sx + 3, y + sy)], fill=ink, width=2)
        d.line([(x + sx, y + sy - 3), (x + sx, y + sy + 3)], fill=ink, width=2)


def icon_drone_ship(d, x, y, ink):
    # A quadcopter drone above waves and a small warship.
    d.rectangle([x + 25, y + 12, x + 35, y + 19], fill=ink)
    for cx, cy in ((12, 8), (48, 8), (12, 22), (48, 22)):
        d.line([(x + 30, y + 15), (x + cx, y + cy)], fill=ink, width=2)
        d.ellipse([x + cx - 5, y + cy - 2, x + cx + 5, y + cy + 2], outline=ink, width=2)
    d.polygon([(x + 14, y + 44), (x + 46, y + 44), (x + 42, y + 51), (x + 18, y + 51)], fill=ink)
    d.rectangle([x + 24, y + 38, x + 34, y + 44], fill=ink)
    for wx in (6, 24, 42):
        d.arc([x + wx, y + 50, x + wx + 12, y + 58], 0, 180, fill=ink, width=2)


def icon_globe(d, x, y, ink):
    # A globe with meridians: the climate talks.
    d.ellipse([x + 10, y + 6, x + 50, y + 46], outline=ink, width=3)
    d.ellipse([x + 22, y + 6, x + 38, y + 46], outline=ink, width=2)
    d.line([(x + 10, y + 26), (x + 50, y + 26)], fill=ink, width=2)
    d.line([(x + 30, y + 48), (x + 30, y + 54)], fill=ink, width=3)
    d.line([(x + 20, y + 55), (x + 40, y + 55)], fill=ink, width=3)


ICONS = {
    "tanker": icon_tanker,
    "tag": icon_tag,
    "chart": icon_chart,
    "rocket": icon_rocket,
    "drone": icon_drone_ship,
    "globe": icon_globe,
}

PANELS = [
    {
        "tag": "MIDDLE EAST",
        "colour": (179, 64, 42),
        "icon": "tanker",
        "headline": "Tankers hit mines in the Strait of Hormuz",
        "sub": "Iran's Guard says oil tankers struck naval mines and caught fire",
    },
    {
        "tag": "ECONOMY",
        "colour": (29, 111, 184),
        "icon": "tag",
        "headline": "US proposes tariffs on 14 trading partners",
        "sub": "Duties of 20-40% planned for China, the EU, India and 11 others",
    },
    {
        "tag": "MARKETS",
        "colour": (150, 44, 44),
        "icon": "chart",
        "headline": "Wall Street slides on AI-spending doubts",
        "sub": "S&P 500 falls 2.2% and Nasdaq 3.2% as tariff fears fuel the sell-off",
    },
    {
        "tag": "SPACE",
        "colour": (91, 75, 196),
        "icon": "rocket",
        "headline": "Pakistan's first astronaut flies to China's station",
        "sub": "Muhammad Zeeshan Ali launches aboard Shenzhou 24 with two Chinese crew",
    },
    {
        "tag": "UKRAINE WAR",
        "colour": (15, 118, 110),
        "icon": "drone",
        "headline": "Ukraine sinks Russian warship in Libyan port",
        "sub": "Drone strike kills two Libyan officers; Russia hits Kyiv and Odesa",
    },
    {
        "tag": "CLIMATE",
        "colour": (46, 125, 50),
        "icon": "globe",
        "headline": "COP31 climate talks end without a deal",
        "sub": "Pope Leo XIV voices concern as talks fail on fossil-fuel transition",
    },
]

TICKER_LABEL = "ALSO ON 25 NOVEMBER"
TICKER_TEXT = (
    "Australia & Solomon Islands sign a security treaty · Colombia frees every "
    "hostage in the Cartagena siege · Sudan drone strikes kill 19 civilians · "
    "Senegal restored as Africa Cup champions"
)


def draw_header(d):
    d.rectangle([0, 0, W, 180], fill=NAVY)
    kicker = "ONE DAY · ONE IMAGE · THE WORLD'S NEWS"
    kf = font(23, bold=True)
    d.text(((W - d.textlength(kicker, font=kf)) / 2, 16), kicker, font=kf, fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    tf = font(62, bold=True)
    d.text(((W - d.textlength(title, font=tf)) / 2, 46), title, font=tf, fill=(255, 255, 255))
    date = "WEDNESDAY 25 NOVEMBER 2026"
    df = font(40, bold=True)
    d.text(((W - d.textlength(date, font=df)) / 2, 122), date, font=df, fill=GOLD)


def draw_panel(d, panel, px, py, pw, ph):
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=14, fill=CARD, outline=CARD_EDGE, width=2)
    colour = panel["colour"]
    d.rounded_rectangle([px, py, px + 10, py + ph], radius=5, fill=colour)
    # Icon badge and section tag share the panel's top row.
    badge = [px + 26, py + 16, px + 86, py + 76]
    tint = tuple(int(c + (255 - c) * 0.88) for c in colour)
    d.rounded_rectangle(badge, radius=10, fill=tint)
    ICONS[panel["icon"]](d, px + 26, py + 16, colour)
    tag_f = font(24, bold=True)
    d.text((px + 102, py + 32), panel["tag"], font=tag_f, fill=colour)
    # Headline, then the one-line explainer under it.
    head_f = font(28, bold=True)
    y = text_block(d, px + 26, py + 86, panel["headline"], head_f, INK, pw - 52, 33, 2)
    sub_f = font(22)
    text_block(d, px + 26, y + 3, panel["sub"], sub_f, SUB, pw - 52, 26, 2)


def draw_ticker(d):
    top = 858
    d.rectangle([0, top, W, 972], fill=NAVY)
    lf = font(22, bold=True)
    d.text((20, top + 12), TICKER_LABEL, font=lf, fill=GOLD)
    tf = font(22)
    text_block(d, 20, top + 44, TICKER_TEXT, tf, (240, 238, 230), W - 40, 27, 3)


def draw_footer(d):
    note = "Events as reported on 25 November 2026, in every time zone"
    nf = font(20)
    d.text(((W - d.textlength(note, font=nf)) / 2, 984), note, font=nf, fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    margin, gap, pw, ph = 16, 8, 489, 212
    for i, panel in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = margin + col * (pw + 14)
        py = 194 + row * (ph + gap + 2)
        draw_panel(d, panel, px, py, pw, ph)
    draw_ticker(d)
    draw_footer(d)
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, out.stat().st_size, "bytes,", img.size)


if __name__ == "__main__":
    main()
