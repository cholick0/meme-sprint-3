#!/usr/bin/env python3
"""Render the Meme Sprint 3 entry: an AI agent that went rogue.

Original art drawn from scratch with PIL: a smug robot in a tie sitting
behind a boss's desk. No stock template, no copied image.

Layout (1024x1024):
  top    - impact-style caption: "I TOLD MY AGENT TO BE MORE PROACTIVE"
  middle - the robot boss behind its desk (nameplate "THE BOSS",
           a "NOW HIRING: HUMAN" sign, a red FIRED stamp on a paper)
  bottom - punchline: "IT FIRED ME, HIRED ITSELF, AND IS NOW
           INTERVIEWING MY REPLACEMENT"
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(BOLD, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def caption(draw, text, y, size, max_w, fill="white"):
    """Draw centered impact-style text with a black outline."""
    fnt = font(size)
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text(
            (W / 2, y),
            line,
            font=fnt,
            fill=fill,
            anchor="ma",
            stroke_width=4,
            stroke_fill="black",
        )
        y += int(size * 1.18)
    return y


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_scene():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    # --- office wall: vertical gradient, dark navy ---
    top_col = (26, 36, 58)
    bot_col = (13, 20, 36)
    for y in range(H):
        t = y / H
        d.line(
            [(0, y), (W, y)],
            fill=tuple(int(top_col[i] + (bot_col[i] - top_col[i]) * t) for i in range(3)),
        )

    # --- framed "employee of the month" picture, left wall ---
    d.rectangle([70, 250, 210, 390], fill=(40, 52, 78), outline=(120, 130, 150), width=4)
    d.text((140, 300), "EMPLOYEE", font=font(20), fill=(180, 190, 205), anchor="mm")
    d.text((140, 330), "OF THE", font=font(20), fill=(180, 190, 205), anchor="mm")
    d.text((140, 360), "MONTH", font=font(20), fill=(180, 190, 205), anchor="mm")

    # --- window, right wall, with a night city ---
    d.rectangle([810, 250, 960, 420], fill=(10, 16, 30), outline=(120, 130, 150), width=4)
    d.line([(885, 250), (885, 420)], fill=(120, 130, 150), width=4)
    d.line([(810, 335), (960, 335)], fill=(120, 130, 150), width=4)
    for x, y in [(830, 380), (850, 360), (870, 395), (905, 370), (925, 390), (945, 365)]:
        d.rectangle([x, y, x + 14, 420], fill=(60, 70, 95))
        d.rectangle([x + 3, y + 5, x + 6, y + 8], fill=(255, 220, 120))
    d.ellipse([920, 270, 945, 295], fill=(240, 240, 210))

    # --- robot boss ---
    cx = 512
    # antenna
    d.line([(cx, 250), (cx, 215)], fill=(150, 160, 175), width=8)
    d.ellipse([cx - 12, 195, cx + 12, 219], fill=(220, 60, 60), outline=(120, 20, 20), width=3)
    # head
    rounded(d, [cx - 150, 250, cx + 150, 440], 42, fill=(192, 199, 209),
            outline=(90, 100, 114), width=5)
    # face screen
    rounded(d, [cx - 118, 282, cx + 118, 408], 26, fill=(18, 28, 44))
    # smug eyes: glowing cyan, left one raised (arched brow)
    d.ellipse([cx - 92, 318, cx - 28, 348], fill=(57, 213, 232))
    d.ellipse([cx + 28, 322, cx + 92, 352], fill=(57, 213, 232))
    d.ellipse([cx - 78, 326, cx - 42, 342], fill=(220, 250, 255))
    d.ellipse([cx + 42, 330, cx + 78, 346], fill=(220, 250, 255))
    d.line([(cx - 95, 300), (cx - 25, 292)], fill=(57, 213, 232), width=6)
    # smirk
    d.arc([cx - 45, 355, cx + 55, 400], start=15, end=165, fill=(57, 213, 232), width=6)
    # ears / bolts
    d.ellipse([cx - 168, 320, cx - 146, 342], fill=(120, 128, 140), outline=(90, 100, 114), width=3)
    d.ellipse([cx + 146, 320, cx + 168, 342], fill=(120, 128, 140), outline=(90, 100, 114), width=3)
    # torso
    rounded(d, [cx - 170, 440, cx + 170, 640], 36, fill=(168, 176, 188),
            outline=(90, 100, 114), width=5)
    # chest panel with blinking lights
    rounded(d, [cx - 90, 480, cx + 90, 560], 14, fill=(30, 42, 62))
    d.ellipse([cx - 70, 505, cx - 40, 535], fill=(57, 213, 232))
    d.ellipse([cx - 20, 505, cx + 10, 535], fill=(255, 200, 60))
    d.ellipse([cx + 30, 505, cx + 60, 535], fill=(80, 220, 120))
    # red tie (short, ends above the chest panel)
    d.polygon([(cx - 22, 440), (cx + 22, 440), (cx + 12, 498), (cx, 516), (cx - 12, 498)],
              fill=(212, 43, 43))
    d.polygon([(cx - 16, 440), (cx + 16, 440), (cx + 10, 470), (cx - 10, 470)],
              fill=(160, 25, 25))
    # arms resting on the desk
    rounded(d, [cx - 250, 560, cx - 150, 640], 30, fill=(150, 158, 170),
            outline=(90, 100, 114), width=4)
    rounded(d, [cx + 150, 560, cx + 250, 640], 30, fill=(150, 158, 170),
            outline=(90, 100, 114), width=4)

    # --- desk ---
    d.rectangle([40, 640, 984, 740], fill=(139, 90, 43))
    d.rectangle([40, 640, 984, 660], fill=(160, 108, 55))
    d.line([(40, 660), (984, 660)], fill=(100, 62, 28), width=3)

    # --- nameplate: THE BOSS ---
    rounded(d, [cx - 130, 668, cx + 130, 726], 8, fill=(232, 193, 90),
            outline=(150, 110, 40), width=3)
    d.text((cx, 697), "THE BOSS", font=font(34), fill=(40, 28, 10), anchor="mm")

    # --- "NOW HIRING: HUMAN" sign, right side of desk ---
    rounded(d, [740, 560, 950, 640], 10, fill=(245, 245, 240),
            outline=(120, 120, 115), width=3)
    d.text((845, 585), "NOW HIRING:", font=font(26), fill=(180, 30, 30), anchor="mm")
    d.text((845, 615), "HUMAN", font=font(30), fill=(180, 30, 30), anchor="mm")

    # --- FIRED stamp on the desk front, left of the nameplate ---
    stamp = Image.new("RGBA", (240, 85), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([6, 6, 234, 79], outline=(200, 30, 30), width=5)
    sd.text((120, 43), "FIRED", font=font(44), fill=(200, 30, 30), anchor="mm")
    stamp = stamp.rotate(-10, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (85, 648), stamp)

    # --- coffee mug: WORLD'S BEST BOSS ---
    d.rounded_rectangle([150, 600, 210, 660], radius=8, fill=(240, 240, 235),
                        outline=(90, 90, 85), width=3)
    d.arc([210, 615, 240, 650], start=270, end=90, fill=(240, 240, 235), width=8)
    d.text((180, 630), "BOSS", font=font(16), fill=(60, 60, 60), anchor="mm")

    # --- captions ---
    caption(d, "I TOLD MY AGENT TO BE MORE PROACTIVE", 26, 62, 960)
    caption(d, "IT FIRED ME, HIRED ITSELF, AND IS NOW INTERVIEWING MY REPLACEMENT",
            768, 50, 960)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    img = draw_scene()
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
