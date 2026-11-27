#!/usr/bin/env python3
"""Render one 1024x1024 newspaper front page from stories.json.

Layout: masthead, tagline, black date bar, one lead story, five more
headlines, a red ALSO TODAY column of one-line briefs, and a footer.
Everything is drawn with Pillow; the output is deterministic.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 1024
MARGIN = 28
CONTENT = SIZE - 2 * MARGIN

PAPER = (248, 244, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (96, 96, 96)
RULE = (60, 60, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_spaced(draw, centre_x, y, text, fnt, fill, spacing=3):
    """Draw centred text with extra tracking between characters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = centre_x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(page)

    y = 16

    # Masthead.
    mast = font(SERIF_B, 50)
    draw.text((SIZE / 2, y), data["masthead"], font=mast, fill=INK,
              anchor="ma")
    y += 58

    # Tagline, letterspaced small caps.
    tag = font(SANS, 13)
    draw_spaced(draw, SIZE / 2, y, data["tagline"].upper(), tag, GREY, 2)
    y += 22

    # Double rule.
    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=2)
    draw.line([(MARGIN, y + 4), (SIZE - MARGIN, y + 4)], fill=RULE, width=1)
    y += 12

    # Black date bar with the full English date.
    bar_h = 34
    draw.rectangle([(MARGIN, y), (SIZE - MARGIN, y + bar_h)], fill=INK)
    date_f = font(SANS_B, 20)
    draw.text((SIZE / 2, y + bar_h / 2), "FRIDAY 27 NOVEMBER 2026",
              font=date_f, fill=PAPER, anchor="mm")
    y += bar_h + 12

    # Lead story.
    lead = data["headlines"][0]
    kick = font(SANS_B, 12)
    draw.text((MARGIN, y), "LEAD STORY", font=kick, fill=RED)
    y += 18
    lead_head = font(SERIF_B, 31)
    for line in wrap(draw, lead["title"], lead_head, CONTENT):
        draw.text((MARGIN, y), line, font=lead_head, fill=INK)
        y += 35
    y += 4
    lead_body = font(SANS, 16)
    for line in wrap(draw, lead["body"], lead_body, CONTENT):
        draw.text((MARGIN, y), line, font=lead_body, fill=INK)
        y += 20
    y += 8
    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=1)
    y += 10

    # The other five headlines.
    sub_head = font(SERIF_B, 21)
    sub_body = font(SANS, 14)
    for item in data["headlines"][1:]:
        for line in wrap(draw, item["title"], sub_head, CONTENT):
            draw.text((MARGIN, y), line, font=sub_head, fill=INK)
            y += 25
        for line in wrap(draw, item["body"], sub_body, CONTENT):
            draw.text((MARGIN, y), line, font=sub_body, fill=(40, 40, 40))
            y += 18
        y += 10

    # ALSO TODAY header.
    also_f = font(SANS_B, 18)
    draw.text((MARGIN, y), "ALSO TODAY", font=also_f, fill=RED)
    y += 26
    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RED, width=2)
    y += 8

    # Briefs in two columns, one line each, with a red square bullet.
    briefs = data["briefs"]
    col_w = (CONTENT - 24) // 2
    rows = (len(briefs) + 1) // 2
    row_h = 17
    brief_f = font(SANS, 12)
    for i, item in enumerate(briefs):
        col = i % 2
        row = i // 2
        bx = MARGIN + col * (col_w + 24)
        by = y + row * row_h
        # Shrink this brief's font until it fits on one line.
        size = 12
        fnt = brief_f
        while (size > 10 and
               draw.textlength(item["text"], font=fnt) > col_w - 12):
            size -= 1
            fnt = font(SANS, size)
        draw.rectangle([(bx, by + 4), (bx + 6, by + 10)], fill=RED)
        draw.text((bx + 11, by), item["text"], font=fnt, fill=INK)
    y += rows * row_h + 6

    # Footer.
    draw.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=RULE, width=1)
    y += 8
    foot = font(SANS, 12)
    draw.text((MARGIN, y), data["footer_note"], font=foot, fill=GREY)
    y += 16
    src = font(SANS, 11)
    draw.text((MARGIN, y), "Sources: " + data["sources"], font=src,
              fill=GREY)
    y += 15

    print("bottom y =", y, "of", SIZE)
    if y > SIZE - 8:
        raise SystemExit("layout overflow: bottom y=%d" % y)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
