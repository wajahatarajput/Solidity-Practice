#!/usr/bin/env python3
"""Generate a complete Solidity Practice curriculum PowerPoint."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import nsmap
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt, Emu

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "pptx_assets"
OUT = ROOT / "Solidity_Practice_Complete_Guide.pptx"

# Theme — slate + teal + amber (avoid purple/cream AI defaults)
NAVY = RGBColor(0x0B, 0x1F, 0x33)
TEAL = RGBColor(0x0D, 0x94, 0x88)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
SLATE = RGBColor(0x1E, 0x29, 0x3B)
INK = RGBColor(0x0F, 0x17, 0x2A)
MUTED = RGBColor(0x47, 0x55, 0x69)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xF1, 0xF5, 0xF9)
CARD = RGBColor(0xE2, 0xE8, 0xF0)
RED = RGBColor(0xDC, 0x26, 0x26)
GREEN = RGBColor(0x16, 0xA3, 0x4A)

PIL_NAVY = (11, 31, 51)
PIL_TEAL = (13, 148, 136)
PIL_AMBER = (245, 158, 11)
PIL_SLATE = (30, 41, 59)
PIL_SOFT = (241, 245, 249)
PIL_WHITE = (255, 255, 255)
PIL_INK = (15, 23, 42)
PIL_MUTED = (71, 85, 105)
PIL_GREEN = (22, 163, 74)
PIL_RED = (220, 38, 38)


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw, start, end, fill=PIL_TEAL, width=4):
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 14
    p1 = (
        end[0] - size * math.cos(angle - math.pi / 6),
        end[1] - size * math.sin(angle - math.pi / 6),
    )
    p2 = (
        end[0] - size * math.cos(angle + math.pi / 6),
        end[1] - size * math.sin(angle + math.pi / 6),
    )
    draw.polygon([end, p1, p2], fill=fill)


def make_diagrams():
    ASSETS.mkdir(exist_ok=True)

    # 1) Learning path
    img = Image.new("RGB", (1600, 520), PIL_SOFT)
    d = ImageDraw.Draw(img)
    title_f, body_f, small_f = font(36, True), font(22, True), font(18)
    d.text((48, 24), "Learning Path — 7 Modules", fill=PIL_NAVY, font=title_f)
    modules = [
        ("01", "Basics", PIL_TEAL),
        ("02", "Types", (8, 110, 120)),
        ("03", "Functions", (14, 130, 100)),
        ("04", "OOP", PIL_AMBER),
        ("05", "Events", (217, 119, 6)),
        ("06", "Advanced", (180, 83, 9)),
        ("07", "Tokens", PIL_GREEN),
    ]
    x0, y, w, h, gap = 40, 120, 180, 160, 28
    for i, (num, name, color) in enumerate(modules):
        x = x0 + i * (w + gap)
        rounded_rect(d, (x, y, x + w, y + h), 18, PIL_WHITE, color, 4)
        d.ellipse((x + 62, y + 18, x + 118, y + 74), fill=color)
        d.text((x + 78, y + 30), num, fill=PIL_WHITE, font=body_f)
        d.text((x + 40, y + 100), name, fill=PIL_INK, font=body_f)
        if i < len(modules) - 1:
            arrow(d, (x + w + 2, y + h // 2), (x + w + gap - 4, y + h // 2), color)
    d.text((48, 340), "25 focused contracts  •  Hardhat tests  •  Deploy script  •  Remix-friendly", fill=PIL_MUTED, font=small_f)
    d.text((48, 390), "Each module builds on the previous — work folders in order.", fill=PIL_MUTED, font=small_f)
    img.save(ASSETS / "learning_path.png")

    # 2) Data locations
    img = Image.new("RGB", (1600, 700), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Data Locations: storage · memory · calldata", fill=PIL_NAVY, font=title_f)
    boxes = [
        ("storage", "Permanent on-chain state", "Lives forever on the blockchain.\nExpensive to WRITE.\nCheap-ish to READ.\nState variables live here.", PIL_TEAL, "items[0]"),
        ("memory", "Temporary mutable copy", "Exists only during the call.\nYou can change it locally.\nChanges do NOT persist\nunless you write back.", (37, 99, 235), "Item memory copy"),
        ("calldata", "Read-only call input", "External function args.\nCheapest for large inputs.\nCannot modify.\nIdeal for strings/arrays.", PIL_AMBER, "string calldata name"),
    ]
    for i, (name, subtitle, desc, color, example) in enumerate(boxes):
        x = 50 + i * 510
        rounded_rect(d, (x, 100, x + 470, 620), 22, PIL_WHITE, color, 5)
        rounded_rect(d, (x, 100, x + 470, 190), 22, color)
        # fix bottom of header
        d.rectangle((x + 5, 160, x + 465, 190), fill=color)
        d.text((x + 30, 120), name, fill=PIL_WHITE, font=font(40, True))
        d.text((x + 30, 220), subtitle, fill=color, font=font(24, True))
        yy = 280
        for line in desc.split("\n"):
            d.text((x + 30, yy), "•  " + line, fill=PIL_INK, font=font(22))
            yy += 42
        rounded_rect(d, (x + 30, 520, x + 440, 580), 12, PIL_SOFT, color, 2)
        d.text((x + 50, 538), example, fill=PIL_SLATE, font=font(22, True))
    img.save(ASSETS / "data_locations.png")

    # 3) Visibility
    img = Image.new("RGB", (1600, 720), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Visibility Keywords — Who Can Call?", fill=PIL_NAVY, font=title_f)
    headers = ["Keyword", "Same contract", "Child contract", "Outside world", "Auto getter?"]
    rows = [
        ["public", "Yes", "Yes", "Yes", "Yes (state)"],
        ["external", "Via this.fn()", "Via this.fn()", "Yes", "No"],
        ["internal", "Yes", "Yes", "No", "No"],
        ["private", "Yes", "No", "No", "No"],
    ]
    col_w = [260, 260, 280, 280, 280]
    x, y = 50, 110
    for i, h in enumerate(headers):
        xx = x + sum(col_w[:i])
        rounded_rect(d, (xx, y, xx + col_w[i] - 8, y + 70), 10, PIL_NAVY)
        d.text((xx + 18, y + 20), h, fill=PIL_WHITE, font=font(22, True))
    for r, row in enumerate(rows):
        yy = y + 90 + r * 120
        bg = PIL_WHITE if r % 2 == 0 else (226, 232, 240)
        for i, cell in enumerate(row):
            xx = x + sum(col_w[:i])
            rounded_rect(d, (xx, yy, xx + col_w[i] - 8, yy + 100), 10, bg, PIL_TEAL if i == 0 else (203, 213, 225), 2)
            color = PIL_TEAL if i == 0 else PIL_INK
            d.text((xx + 18, yy + 34), cell, fill=color, font=font(24, True if i == 0 else False))
    img.save(ASSETS / "visibility.png")

    # 4) Inheritance / C3
    img = Image.new("RGB", (1600, 720), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Inheritance & C3 Linearization (D is B, C)", fill=PIL_NAVY, font=title_f)

    def node(cx, cy, text, color=PIL_TEAL, w=160, h=70):
        rounded_rect(d, (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2), 14, color)
        tw = d.textlength(text, font=font(26, True))
        d.text((cx - tw / 2, cy - 16), text, fill=PIL_WHITE, font=font(26, True))

    node(800, 140, "A", PIL_NAVY)
    node(560, 300, "B", PIL_TEAL)
    node(1040, 300, "C", PIL_TEAL)
    node(800, 460, "D", PIL_AMBER)
    arrow(d, (720, 170), (600, 265), PIL_MUTED)
    arrow(d, (880, 170), (1000, 265), PIL_MUTED)
    arrow(d, (620, 335), (740, 425), PIL_MUTED)
    arrow(d, (980, 335), (860, 425), PIL_MUTED)
    rounded_rect(d, (80, 560, 1520, 680), 16, PIL_WHITE, PIL_AMBER, 3)
    d.text((110, 590), "is  =  inherit from parent(s)", fill=PIL_INK, font=font(24, True))
    d.text((110, 635), "super path for D is B, C  →  D → C → B → A     Result: greet() = \"A -> B -> C -> D\"", fill=PIL_MUTED, font=font(22))
    img.save(ASSETS / "inheritance.png")

    # 5) call vs delegatecall
    img = Image.new("RGB", (1600, 720), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "call vs delegatecall", fill=PIL_NAVY, font=title_f)
    # Left: call
    rounded_rect(d, (60, 100, 760, 680), 20, PIL_WHITE, PIL_TEAL, 4)
    d.text((90, 130), "call", fill=PIL_TEAL, font=font(40, True))
    rounded_rect(d, (100, 210, 340, 360), 14, PIL_NAVY)
    d.text((150, 260), "Caller", fill=PIL_WHITE, font=font(28, True))
    rounded_rect(d, (460, 210, 700, 360), 14, PIL_TEAL)
    d.text((510, 260), "Logic", fill=PIL_WHITE, font=font(28, True))
    arrow(d, (350, 285), (450, 285), PIL_AMBER)
    d.text((120, 400), "Runs Logic's CODE", fill=PIL_INK, font=font(24, True))
    d.text((120, 450), "Uses Logic's STORAGE", fill=PIL_INK, font=font(24))
    d.text((120, 500), "Normal external interaction", fill=PIL_MUTED, font=font(22))
    d.text((120, 560), "Demo: callSetNumber → Logic.number changes", fill=PIL_MUTED, font=font(20))
    # Right: delegatecall
    rounded_rect(d, (840, 100, 1540, 680), 20, PIL_WHITE, PIL_AMBER, 4)
    d.text((870, 130), "delegatecall", fill=PIL_AMBER, font=font(40, True))
    rounded_rect(d, (880, 210, 1120, 360), 14, PIL_NAVY)
    d.text((920, 260), "Caller", fill=PIL_WHITE, font=font(28, True))
    rounded_rect(d, (1240, 210, 1480, 360), 14, (180, 83, 9))
    d.text((1280, 245), "Logic", fill=PIL_WHITE, font=font(28, True))
    d.text((1265, 290), "(code only)", fill=PIL_SOFT, font=font(18))
    arrow(d, (1130, 285), (1230, 285), PIL_TEAL)
    d.text((900, 400), "Runs Logic's CODE", fill=PIL_INK, font=font(24, True))
    d.text((900, 450), "Uses Caller's STORAGE", fill=PIL_RED, font=font(24, True))
    d.text((900, 500), "Proxy / upgrade pattern", fill=PIL_MUTED, font=font(22))
    d.text((900, 560), "Demo: delegateSetNumber → Caller.number changes", fill=PIL_MUTED, font=font(20))
    d.text((900, 610), "⚠ Never delegatecall untrusted contracts", fill=PIL_RED, font=font(20, True))
    img.save(ASSETS / "call_delegatecall.png")

    # 6) CEI
    img = Image.new("RGB", (1600, 560), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Security: Checks → Effects → Interactions (CEI)", fill=PIL_NAVY, font=title_f)
    steps = [
        ("1. Checks", "Validate inputs &\npermissions first", "require(amount > 0)\nrequire(balance >= amount)", PIL_TEAL),
        ("2. Effects", "Update YOUR state\nbefore calling out", "balances[msg.sender] -= amount", PIL_AMBER),
        ("3. Interactions", "Then talk to other\ncontracts / send ETH", "payable(to).call{value}(\"\")", PIL_GREEN),
    ]
    for i, (title, sub, code, color) in enumerate(steps):
        x = 70 + i * 510
        rounded_rect(d, (x, 110, x + 460, 480), 20, PIL_WHITE, color, 4)
        d.ellipse((x + 185, 140, x + 275, 230), fill=color)
        d.text((x + 215, 162), str(i + 1), fill=PIL_WHITE, font=font(36, True))
        d.text((x + 40, 260), title, fill=color, font=font(30, True))
        yy = 320
        for line in sub.split("\n"):
            d.text((x + 40, yy), line, fill=PIL_MUTED, font=font(22))
            yy += 34
        d.text((x + 40, 420), code.split("\n")[0][:42], fill=PIL_SLATE, font=font(18, True))
        if i < 2:
            arrow(d, (x + 470, 300), (x + 500, 300), color)
    img.save(ASSETS / "cei.png")

    # 7) ERC-20 flow
    img = Image.new("RGB", (1600, 620), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "ERC-20 Token Flow", fill=PIL_NAVY, font=title_f)
    flow = [
        ("Mint", "Deployer gets\ninitialSupply", PIL_TEAL),
        ("Transfer", "Owner sends\ntokens to Alice", (37, 99, 235)),
        ("Approve", "Owner allows\nAlice to spend", PIL_AMBER),
        ("transferFrom", "Alice moves\nowner's tokens", PIL_GREEN),
    ]
    for i, (t, s, c) in enumerate(flow):
        x = 80 + i * 380
        rounded_rect(d, (x, 140, x + 320, 420), 18, PIL_WHITE, c, 4)
        d.text((x + 40, 180), t, fill=c, font=font(32, True))
        yy = 260
        for line in s.split("\n"):
            d.text((x + 40, yy), line, fill=PIL_INK, font=font(24))
            yy += 40
        if i < 3:
            arrow(d, (x + 330, 280), (x + 370, 280), c)
    d.text((80, 500), "Events: Transfer(from, to, value)  •  Approval(owner, spender, value)", fill=PIL_MUTED, font=font(22))
    d.text((80, 550), "Keywords: balanceOf, allowance, totalSupply, decimals (usually 18)", fill=PIL_MUTED, font=font(22))
    img.save(ASSETS / "erc20_flow.png")

    # 8) Project structure
    img = Image.new("RGB", (1600, 720), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Project Structure", fill=PIL_NAVY, font=title_f)
    tree = [
        "Solidity-Practice/",
        "├── contracts/          ← all .sol lessons (01…07)",
        "├── scripts/deploy.js   ← HelloWorld + SimpleStorage + ERC20",
        "├── test/               ← Mocha/Chai Hardhat tests",
        "├── hardhat.config.js   ← Solidity 0.8.24 + optimizer",
        "├── package.json        ← npm scripts & deps",
        "├── artifacts/          ← ABI + bytecode (after compile)",
        "└── cache/              ← incremental compile cache",
    ]
    rounded_rect(d, (80, 100, 1520, 660), 20, PIL_NAVY)
    yy = 140
    for line in tree:
        d.text((130, yy), line, fill=PIL_SOFT if line.startswith("Solidity") else (148, 226, 200), font=font(28, True if line.startswith("Solidity") else False))
        yy += 60
    img.save(ASSETS / "project_structure.png")

    # 9) Contract lifecycle
    img = Image.new("RGB", (1600, 520), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Smart Contract Lifecycle", fill=PIL_NAVY, font=title_f)
    life = [
        ("Write", ".sol source"),
        ("Compile", "ABI + bytecode"),
        ("Deploy", "constructor runs"),
        ("Interact", "tx / eth_call"),
        ("Events", "off-chain apps"),
    ]
    for i, (t, s) in enumerate(life):
        x = 80 + i * 300
        d.ellipse((x + 40, 140, x + 180, 280), fill=PIL_TEAL if i % 2 == 0 else PIL_AMBER)
        tw = d.textlength(t, font=font(26, True))
        d.text((x + 110 - tw / 2, 185), t, fill=PIL_WHITE, font=font(26, True))
        d.text((x + 50, 320), s, fill=PIL_INK, font=font(22))
        if i < 4:
            arrow(d, (x + 190, 210), (x + 290, 210))
    img.save(ASSETS / "lifecycle.png")

    # 10) Setup checklist visual
    img = Image.new("RGB", (1600, 600), PIL_SOFT)
    d = ImageDraw.Draw(img)
    d.text((48, 24), "Setup Checklist", fill=PIL_NAVY, font=title_f)
    checks = [
        "Install Node.js 18+ and npm",
        "Clone / open Solidity-Practice folder",
        "Run: npm install",
        "Run: npx hardhat compile",
        "Run: npx hardhat test",
        "Optional: open Remix + set compiler 0.8.24",
    ]
    for i, c in enumerate(checks):
        y = 110 + i * 70
        d.ellipse((80, y, 140, y + 60), fill=PIL_TEAL)
        d.text((100, y + 12), str(i + 1), fill=PIL_WHITE, font=font(28, True))
        rounded_rect(d, (170, y, 1500, y + 60), 12, PIL_WHITE, PIL_TEAL, 2)
        d.text((200, y + 14), c, fill=PIL_INK, font=font(26))
    img.save(ASSETS / "setup_checklist.png")


# ---------- PPT helpers ----------

def set_slide_bg(slide, color: RGBColor):
    fill = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    fill.fill.solid()
    fill.fill.fore_color.rgb = color
    fill.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = fill._element
    spTree.remove(sp)
    spTree.insert(2, sp)
    return fill


def add_text(slide, left, top, width, height, text, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT, font_name="Calibri"):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return box


def add_bullets(slide, left, top, width, height, items, size=16, color=INK, spacing=6):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(spacing)
    return box


def accent_bar(slide, color=TEAL):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.18), Inches(7.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()


def section_chip(slide, text, top=0.25):
    chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(top), Inches(2.4), Inches(0.38))
    chip.fill.solid()
    chip.fill.fore_color.rgb = TEAL
    chip.line.fill.background()
    tf = chip.text_frame
    tf.paragraphs[0].text = text
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = WHITE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.name = "Calibri"


def content_slide(prs, section, title, bullets=None, image=None, note=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SOFT)
    accent_bar(slide)
    section_chip(slide, section)
    add_text(slide, 0.5, 0.7, 12, 0.6, title, size=30, bold=True, color=NAVY)
    if image and Path(image).exists():
        if bullets:
            add_bullets(slide, 0.5, 1.4, 5.2, 5.2, bullets, size=15)
            slide.shapes.add_picture(str(image), Inches(6.0), Inches(1.4), width=Inches(6.8))
        else:
            slide.shapes.add_picture(str(image), Inches(0.6), Inches(1.35), width=Inches(12.1))
    elif bullets:
        add_bullets(slide, 0.5, 1.4, 12, 5.5, bullets, size=17)
    if note:
        add_text(slide, 0.5, 6.9, 12, 0.4, note, size=12, color=MUTED)
    return slide


def keyword_table_slide(prs, section, title, rows, intro=None):
    """rows: list of (keyword, meaning, example)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SOFT)
    accent_bar(slide, AMBER)
    section_chip(slide, section)
    add_text(slide, 0.5, 0.7, 12, 0.5, title, size=28, bold=True, color=NAVY)
    if intro:
        add_text(slide, 0.5, 1.2, 12.2, 0.4, intro, size=14, color=MUTED)

    # header bar
    headers = [("Keyword", 2.4), ("What it means", 5.6), ("Example / tip", 4.2)]
    y = 1.7 if intro else 1.4
    x = 0.45
    for text, w in headers:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w - 0.08), Inches(0.42))
        shape.fill.solid()
        shape.fill.fore_color.rgb = NAVY
        shape.line.fill.background()
        tf = shape.text_frame
        tf.paragraphs[0].text = text
        tf.paragraphs[0].font.size = Pt(13)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = WHITE
        tf.paragraphs[0].font.name = "Calibri"
        x += w

    row_h = min(0.72, 4.8 / max(len(rows), 1))
    for i, (kw, meaning, example) in enumerate(rows):
        yy = y + 0.5 + i * row_h
        x = 0.45
        values = [kw, meaning, example]
        widths = [2.4, 5.6, 4.2]
        for j, (val, w) in enumerate(zip(values, widths)):
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(yy), Inches(w - 0.08), Inches(row_h - 0.06))
            shape.fill.solid()
            shape.fill.fore_color.rgb = WHITE if i % 2 == 0 else CARD
            shape.line.color.rgb = TEAL if j == 0 else CARD
            tf = shape.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = val
            p.font.size = Pt(11 if len(val) > 70 else 12)
            p.font.bold = j == 0
            p.font.color.rgb = TEAL if j == 0 else INK
            p.font.name = "Calibri"
            x += w
    return slide


def two_col_slide(prs, section, title, left_title, left_items, right_title, right_items):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SOFT)
    accent_bar(slide)
    section_chip(slide, section)
    add_text(slide, 0.5, 0.7, 12, 0.5, title, size=28, bold=True, color=NAVY)

    left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(1.4), Inches(6.0), Inches(5.5))
    left.fill.solid()
    left.fill.fore_color.rgb = WHITE
    left.line.color.rgb = TEAL
    add_text(slide, 0.7, 1.55, 5.5, 0.4, left_title, size=18, bold=True, color=TEAL)
    add_bullets(slide, 0.7, 2.1, 5.5, 4.5, left_items, size=14)

    right = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(6.0), Inches(5.5))
    right.fill.solid()
    right.fill.fore_color.rgb = WHITE
    right.line.color.rgb = AMBER
    add_text(slide, 7.05, 1.55, 5.5, 0.4, right_title, size=18, bold=True, color=AMBER)
    add_bullets(slide, 7.05, 2.1, 5.5, 4.5, right_items, size=14)
    return slide


def code_slide(prs, section, title, lines, note=None, font_size=None):
    """Dark code block; each entry is (code, comment) — comment shown after // on that line."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SOFT)
    accent_bar(slide, TEAL)
    section_chip(slide, section)
    add_text(slide, 0.5, 0.65, 12, 0.45, title, size=24, bold=True, color=NAVY)

    # window chrome
    chrome = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.15), Inches(12.5), Inches(5.85 if not note else 5.55)
    )
    chrome.fill.solid()
    chrome.fill.fore_color.rgb = SLATE
    chrome.line.fill.background()

    # traffic-light dots
    for i, c in enumerate([RGBColor(0xEF, 0x44, 0x44), RGBColor(0xF5, 0x9E, 0x0B), RGBColor(0x22, 0xC5, 0x5E)]):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6 + i * 0.28), Inches(1.28), Inches(0.16), Inches(0.16))
        dot.fill.solid()
        dot.fill.fore_color.rgb = c
        dot.line.fill.background()

    add_text(slide, 1.6, 1.22, 10, 0.28, "Solidity  ·  line-by-line annotated", size=11, color=CARD)

    n = max(len(lines), 1)
    size = font_size or (10 if n > 16 else 11 if n > 13 else 12 if n > 10 else 13)

    box = slide.shapes.add_textbox(Inches(0.55), Inches(1.6), Inches(12.2), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = False

    code_color = RGBColor(0xE2, 0xE8, 0xF0)
    comment_color = RGBColor(0x5E, 0xEA, 0xD4)  # soft teal for comments
    gutter = RGBColor(0x64, 0x74, 0x8B)

    for i, item in enumerate(lines):
        if isinstance(item, tuple):
            code, comment = item
        else:
            code, comment = item, ""
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.clear()
        p.space_before = Pt(1)
        p.space_after = Pt(1)
        p.font.name = "Consolas"

        # line number
        r0 = p.add_run()
        r0.text = f"{i + 1:>2}  "
        r0.font.size = Pt(size)
        r0.font.name = "Consolas"
        r0.font.color.rgb = gutter

        r1 = p.add_run()
        r1.text = code
        r1.font.size = Pt(size)
        r1.font.name = "Consolas"
        r1.font.color.rgb = code_color

        if comment:
            r2 = p.add_run()
            # keep spacing readable on one line
            pad = "  " if code.strip() else ""
            r2.text = f"{pad}// {comment}"
            r2.font.size = Pt(size)
            r2.font.name = "Consolas"
            r2.font.color.rgb = comment_color
            r2.font.italic = True

    if note:
        add_text(slide, 0.5, 6.95, 12.2, 0.35, note, size=11, color=MUTED)
    return slide


def code_slides(prs, section, title_prefix, chunks, note=None):
    """Emit one or more code slides from a list of line-lists."""
    for i, lines in enumerate(chunks):
        suffix = f" ({i + 1}/{len(chunks)})" if len(chunks) > 1 else ""
        code_slide(prs, section, f"{title_prefix}{suffix}", lines, note=note if i == len(chunks) - 1 else None)


def title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    # decorative teal strip
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.8), Inches(13.333), Inches(1.7))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TEAL
    strip.line.fill.background()
    amber = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.8), Inches(0.35), Inches(1.7))
    amber.fill.solid()
    amber.fill.fore_color.rgb = AMBER
    amber.line.fill.background()

    add_text(slide, 0.8, 1.5, 11.5, 0.5, "SOLIDITY PRACTICE CURRICULUM", size=18, bold=True, color=TEAL)
    add_text(slide, 0.8, 2.1, 11.5, 1.2, "Complete Guide: Setup → Tokens", size=40, bold=True, color=WHITE)
    add_text(
        slide,
        0.8,
        3.5,
        11.5,
        1.0,
        "Hardhat  •  Solidity 0.8.24  •  25 contracts  •  OOP  •  Security  •  ERC-20/721",
        size=18,
        color=CARD,
    )
    add_text(slide, 0.8, 6.2, 11, 0.4, "Keyword glossary · diagrams · line-by-line code · labs & quiz", size=16, bold=True, color=WHITE)
    add_text(slide, 0.8, 6.7, 11, 0.35, "Educational only — do not deploy to mainnet with real funds", size=12, color=SOFT)


def outline_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SOFT)
    accent_bar(slide, AMBER)
    section_chip(slide, "Agenda")
    add_text(slide, 0.5, 0.7, 12, 0.5, "Outline — What We Cover", size=30, bold=True, color=NAVY)
    items = [
        "A. Prerequisites, installations & Hardhat configuration",
        "B. Project structure, compile / test / deploy workflows (Hardhat · Remix · solc)",
        "C. Module 01–03: Basics, types, data locations, visibility, control flow",
        "D. Module 04: Full OOP keyword deep-dive (contract, is, virtual, override…)",
        "E. Module 05–06: Events, custom errors, modifiers, ETH, call/delegatecall, assembly, CEI",
        "F. Module 07: ERC-20 & ERC-721 token standards",
        "G. Annotated code snippets (every line explained with // comments)",
        "H. Keyword glossary tables (every important word explained)",
        "I. Labs checklist + end-of-deck quiz questions",
    ]
    add_bullets(slide, 0.6, 1.5, 12, 5.5, items, size=18, spacing=10)


def build():
    make_diagrams()
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ===== OPENING =====
    title_slide(prs)
    outline_slide(prs)

    content_slide(
        prs,
        "Overview",
        "What This Repo Teaches",
        bullets=[
            "A progressive Hardhat project — one idea per .sol file",
            "Start with state variables; finish with fungible & NFT tokens",
            "NatSpec comments (@title, @notice, @dev) document each contract",
            "Tests prove Inheritance, SimpleStorage, and SimpleERC20",
            "Deploy script ships HelloWorld, SimpleStorage, SimpleERC20",
            "Compiler locked to Solidity 0.8.24 (overflow checks built-in)",
        ],
        image=ASSETS / "learning_path.png",
    )

    # ===== SETUP =====
    content_slide(
        prs,
        "Setup",
        "Prerequisites & Installations",
        bullets=[
            "Node.js 18+ and npm — required to run Hardhat",
            "Optional: Remix IDE (browser) — no local install",
            "Optional: MetaMask for Remix Injected Provider",
            "Optional: solcjs for CLI compile without Hardhat",
            "Editor: Cursor / VS Code with Solidity extension recommended",
            "Verify: node -v   and   npm -v",
        ],
        image=ASSETS / "setup_checklist.png",
        note="Install command after opening the project folder: npm install",
    )

    keyword_table_slide(
        prs,
        "Setup",
        "Install & Tool Keywords Explained",
        [
            ("Node.js", "JavaScript runtime that executes Hardhat and npm scripts on your machine.", "node -v → v18+"),
            ("npm", "Node package manager — installs dependencies listed in package.json.", "npm install"),
            ("Hardhat", "Ethereum development environment: compile, test, local chain, deploy.", "npx hardhat compile"),
            ("hardhat-toolbox", "Bundle of plugins: Ethers.js, Chai matchers, network helpers, etc.", "@nomicfoundation/hardhat-toolbox"),
            ("npx", "Runs a local/project binary without global install.", "npx hardhat test"),
            ("Remix", "Browser IDE to compile/deploy Solidity without installing Hardhat.", "remix.ethereum.org"),
            ("solc / solcjs", "Official Solidity compiler (native or JS). Hardhat embeds solc for you.", "npx solcjs --bin --abi …"),
            ("MetaMask", "Browser wallet that can inject an Ethereum provider into Remix.", "Injected Provider"),
        ],
        intro="Know what each tool word means before you type commands.",
    )

    keyword_table_slide(
        prs,
        "Config",
        "hardhat.config.js — Every Setting Explained",
        [
            ("solidity.version", "Exact compiler version Hardhat uses for all contracts.", '"0.8.24"'),
            ("optimizer.enabled", "Turns on bytecode optimizer to reduce gas / size.", "true"),
            ("optimizer.runs", "How often functions are expected to be called. Higher = cheaper calls, larger deploy.", "200 (common default)"),
            ("paths.sources", "Folder Hardhat scans for .sol files.", "./contracts"),
            ("paths.tests", "Folder for Mocha test files.", "./test"),
            ("paths.cache", "Incremental compile cache (safe to delete).", "./cache"),
            ("paths.artifacts", "Output ABIs + bytecode after compile.", "./artifacts"),
            ("pragma solidity", "In each .sol file: which compiler versions are allowed.", "^0.8.24 means ≥0.8.24 <0.9.0"),
            ("SPDX-License", "Source license identifier required/recommended at top of files.", "// SPDX-License-Identifier: MIT"),
        ],
    )

    code_slide(
        prs,
        "Code · Config",
        "hardhat.config.js — every line explained",
        [
            ("require(\"@nomicfoundation/hardhat-toolbox\");", "load compile/test/ethers plugins"),
            ("", ""),
            ("/** @type import('hardhat/config').HardhatUserConfig */", "JSDoc type hint for the config object"),
            ("module.exports = {", "export Hardhat configuration"),
            ("  solidity: {", "compiler settings block"),
            ("    version: \"0.8.24\",", "exact solc version to use"),
            ("    settings: {", "extra compiler options"),
            ("      optimizer: {", "bytecode optimizer"),
            ("        enabled: true,", "turn optimizer ON"),
            ("        runs: 200,", "optimize assuming functions run ~200 times"),
            ("      },", ""),
            ("    },", ""),
            ("  },", ""),
            ("  paths: {", "custom project folders"),
            ("    sources: \"./contracts\",", "where .sol lesson files live"),
            ("    tests: \"./test\",", "where Mocha tests live"),
            ("    cache: \"./cache\",", "incremental compile cache"),
            ("    artifacts: \"./artifacts\",", "ABI + bytecode output"),
            ("  },", ""),
            ("};", "end config"),
        ],
        note="Matches pragma solidity ^0.8.24 in every contract",
    )

    content_slide(
        prs,
        "Config",
        "npm Scripts & Project Layout",
        bullets=[
            "npm run compile → hardhat compile",
            "npm run test → hardhat test",
            "npm run deploy → hardhat run scripts/deploy.js",
            "npm run node → local JSON-RPC chain (accounts with fake ETH)",
            "npm run clean → delete cache/ and artifacts/",
            "artifacts/ holds ABI (how to call) + bytecode (what to deploy)",
        ],
        image=ASSETS / "project_structure.png",
    )

    content_slide(
        prs,
        "Workflow",
        "Three Ways to Compile",
        bullets=[
            "Hardhat (recommended for this repo): npm install → npx hardhat compile",
            "Remix: paste .sol → Compiler 0.8.24 → Compile → Deploy & Run",
            "solcjs: npx solcjs --bin --abi --optimize --base-path . contracts/... -o build/",
            "Multi-file imports need --base-path / --include-path with solcjs",
            "Local persistent node: npx hardhat node then deploy --network localhost",
        ],
        image=ASSETS / "lifecycle.png",
        note="Write → Compile → Deploy → Interact → Index events",
    )

    # ===== MODULE 01 =====
    content_slide(
        prs,
        "Module 01",
        "Basics — What Is a Smart Contract?",
        [
            "contract = a class that lives permanently on the blockchain after deploy",
            "Users call functions by sending transactions (writes cost gas)",
            "Read-only calls (view/pure) can be free eth_call — no state change",
            "Code + storage are public; modern practice avoids selfdestruct",
            "Files: HelloWorld.sol, SimpleStorage.sol",
        ],
    )

    keyword_table_slide(
        prs,
        "Module 01",
        "Core Keywords in HelloWorld & SimpleStorage",
        [
            ("contract", "Declares a deployable unit of code + storage (like a class).", "contract HelloWorld { … }"),
            ("string", "Dynamic UTF-8 text type (reference type — needs a data location).", "string public greeting"),
            ("public", "Callable from outside; for state vars also creates an auto-getter.", "string public greeting"),
            ("constructor", "Special function that runs ONCE at deployment to init state.", "constructor(string memory _greeting)"),
            ("memory", "Temporary location for reference data during the call.", "string memory _greeting"),
            ("function", "Callable method on the contract.", "function setGreeting(...)"),
            ("view", "Function may READ state but must NOT modify it.", "function getGreeting() public view"),
            ("returns", "Declares what the function gives back to the caller.", "returns (string memory)"),
            ("uint256", "Unsigned 256-bit integer (0 … 2^256-1). uint is an alias.", "uint256 private storedNumber"),
            ("private", "Only this contract's code can read/call it (not external ABI).", "uint256 private storedNumber"),
            ("event", "Append-only log for off-chain apps (cheaper than storage).", "event NumberUpdated(...)"),
            ("emit", "Writes an event to the transaction log.", "emit NumberUpdated(old, _number)"),
        ],
        intro="Every word on the first two contracts — explained.",
    )

    two_col_slide(
        prs,
        "Module 01",
        "Labs: HelloWorld & SimpleStorage",
        "HelloWorld.sol",
        [
            "Deploy with \"Hello, Solidity!\"",
            "Call getGreeting() / greeting()",
            "Call setGreeting(\"Hi\")",
            "Notice: write costs gas; view is free",
            "public state → automatic getter",
        ],
        "SimpleStorage.sol",
        [
            "Deploy (no constructor args)",
            "set(42) then get() → 42",
            "Watch NumberUpdated event",
            "Private state + public API pattern",
            "Covered by SimpleStorage.test.js",
        ],
    )

    code_slide(
        prs,
        "Code · 01",
        "HelloWorld.sol — every line explained",
        [
            ("// SPDX-License-Identifier: MIT", "license for this source file"),
            ("pragma solidity ^0.8.24;", "allow compilers >=0.8.24 and <0.9.0"),
            ("", ""),
            ("contract HelloWorld {", "start a deployable contract named HelloWorld"),
            ("    string public greeting;", "on-chain text state + auto-generated getter greeting()"),
            ("", ""),
            ("    constructor(string memory _greeting) {", "runs once at deploy; _greeting lives in memory"),
            ("        greeting = _greeting;", "copy the constructor argument into permanent storage"),
            ("    }", "end of constructor"),
            ("", ""),
            ("    function setGreeting(string memory _greeting) public {", "public write function anyone can call"),
            ("        greeting = _greeting;", "overwrite storage with the new greeting (costs gas)"),
            ("    }", "end of setGreeting"),
            ("", ""),
            ("    function getGreeting() public view returns (string memory) {", "read-only; returns a memory string"),
            ("        return greeting;", "give the caller the current stored greeting"),
            ("    }", "end of getGreeting"),
            ("}", "end of contract"),
        ],
        note="File: contracts/01-basics/HelloWorld.sol",
    )

    code_slide(
        prs,
        "Code · 01",
        "SimpleStorage.sol — every line explained",
        [
            ("// SPDX-License-Identifier: MIT", "license identifier"),
            ("pragma solidity ^0.8.24;", "compiler version constraint"),
            ("", ""),
            ("contract SimpleStorage {", "begin contract"),
            ("    uint256 private storedNumber;", "private unsigned integer — no auto public getter"),
            ("", ""),
            ("    event NumberUpdated(uint256 oldValue, uint256 newValue);", "declare a log type for off-chain listeners"),
            ("", ""),
            ("    function set(uint256 _number) public {", "public setter that mutates storage"),
            ("        uint256 old = storedNumber;", "remember previous value for the event"),
            ("        storedNumber = _number;", "write the new value into storage"),
            ("        emit NumberUpdated(old, _number);", "append a cheap log (not storage)"),
            ("    }", "end of set"),
            ("", ""),
            ("    function get() public view returns (uint256) {", "read-only getter; returns uint256"),
            ("        return storedNumber;", "return the private state value"),
            ("    }", "end of get"),
            ("}", "end of contract"),
        ],
        note="File: contracts/01-basics/SimpleStorage.sol",
    )

    # ===== MODULE 02 =====
    content_slide(
        prs,
        "Module 02",
        "Types & Data — Map of the Module",
        [
            "ValueTypes.sol — integers, bool, address, bytes, enum",
            "ReferenceTypes.sol — arrays, structs, mappings",
            "DataLocations.sol — storage vs memory vs calldata",
            "Rule: value types copy; reference types need a location keyword",
            "Solidity 0.8+ reverts on integer overflow/underflow by default",
        ],
        image=ASSETS / "data_locations.png",
    )

    keyword_table_slide(
        prs,
        "Module 02",
        "Value-Type Keywords Explained",
        [
            ("uint / uint256", "Unsigned integer. Default size 256 bits. Cannot be negative.", "uint256 public unsignedInt = 42"),
            ("int / int256", "Signed integer — can be negative.", "int256 public signedInt = -7"),
            ("bool", "Boolean true or false.", "bool public flag = true"),
            ("address", "20-byte account or contract identifier.", "address public owner"),
            ("payable address", "Address that is allowed to receive ETH.", "payable(msg.sender).call{value}(\"\")"),
            ("bytes32", "Fixed 32-byte blob — perfect for hashes.", "bytes32 public fixedBytes = keccak256(\"solidity\")"),
            ("bytes", "Dynamic byte array (reference type).", "bytes public dynamicBytes = hex\"deadbeef\""),
            ("enum", "Named set of constants stored as small integers under the hood.", "enum Status { Pending, Active, Closed }"),
            ("msg.sender", "Address that called the current function (tx origin of this call).", "owner = msg.sender"),
            ("keccak256", "Ethereum's SHA-3-family hash function.", "keccak256(\"solidity\")"),
            ("hex\"…\"", "Literal for raw bytes written in hexadecimal.", "hex\"deadbeef\""),
        ],
    )

    keyword_table_slide(
        prs,
        "Module 02",
        "Reference-Type Keywords Explained",
        [
            ("array []", "Ordered list. Dynamic arrays grow with push; fixed: uint256[3].", "uint256[] public numbers"),
            ("push", "Append an element to a dynamic storage array.", "numbers.push(value)"),
            ("struct", "Custom group of fields (like an object).", "struct Person { string name; … }"),
            ("mapping", "Hash table key → value. Not iterable. Missing key = zero.", "mapping(address => uint256)"),
            ("nested mapping", "mapping of mapping — classic ERC-20 allowance pattern.", "allowances[owner][spender]"),
            ("storage", "Persistent on-chain data location. Mutations stick.", "Item storage ref = items[0]"),
            ("memory", "Temporary mutable copy for the duration of the call.", "Item memory copy = items[0]"),
            ("calldata", "Read-only input data; cheapest for external args.", "string calldata name"),
            ("external", "Callable only from outside (or via this). Pairs well with calldata.", "function addItem(...) external"),
            ("require", "If condition fails, revert with message (refund leftover gas).", "require(items.length > 0, \"empty\")"),
        ],
        intro="Reference types point at data — you must say WHERE the data lives.",
    )

    code_slide(
        prs,
        "Code · 02",
        "ValueTypes.sol — key lines explained",
        [
            ("enum Status { Pending, Active, Closed }", "named constants stored as 0, 1, 2 under the hood"),
            ("uint256 public unsignedInt = 42;", "unsigned integer state with auto-getter"),
            ("int256 public signedInt = -7;", "signed integer — can be negative"),
            ("bool public flag = true;", "boolean true/false flag"),
            ("address public owner;", "20-byte account/contract address"),
            ("bytes32 public fixedBytes = keccak256(\"solidity\");", "fixed 32-byte hash of the string"),
            ("bytes public dynamicBytes = hex\"deadbeef\";", "dynamic byte array from hex literal"),
            ("Status public status = Status.Pending;", "enum state starts at Pending (0)"),
            ("", ""),
            ("constructor() {", "runs once when the contract is deployed"),
            ("    owner = msg.sender;", "set owner to the address that deployed"),
            ("}", "end constructor"),
            ("", ""),
            ("function toggleFlag() public {", "public function to flip the bool"),
            ("    flag = !flag;", "logical NOT — true becomes false and vice versa"),
            ("}", "end toggleFlag"),
        ],
        note="File: contracts/02-types-and-data/ValueTypes.sol",
    )

    code_slide(
        prs,
        "Code · 02",
        "ReferenceTypes.sol — key lines explained",
        [
            ("struct Person {", "start a custom grouped type"),
            ("    string name;", "person's name field"),
            ("    uint256 age;", "person's age field"),
            ("    address wallet;", "person's wallet address field"),
            ("}", "end struct definition"),
            ("", ""),
            ("uint256[] public numbers;", "dynamic array of uint256 in storage"),
            ("Person[] public people;", "dynamic array of Person structs"),
            ("mapping(address => uint256) public balances;", "hash map: address → balance"),
            ("mapping(address => mapping(address => uint256)) public allowances;", "nested map: owner → spender → amount"),
            ("", ""),
            ("function pushNumber(uint256 value) public {", "append to the numbers array"),
            ("    numbers.push(value);", "grow the array by one element"),
            ("}", "end pushNumber"),
            ("", ""),
            ("function addPerson(string memory name, uint256 age, address wallet) public {", "create a Person in memory args"),
            ("    people.push(Person({name: name, age: age, wallet: wallet}));", "build struct and push into storage array"),
            ("}", "end addPerson"),
        ],
        note="File: contracts/02-types-and-data/ReferenceTypes.sol",
    )

    code_slide(
        prs,
        "Code · 02",
        "DataLocations.sol — storage vs memory vs calldata",
        [
            ("struct Item { string name; uint256 quantity; }", "custom type with two fields"),
            ("Item[] public items;", "storage array of items (permanent)"),
            ("", ""),
            ("function addItem(string calldata name, uint256 quantity) external {", "external + calldata = cheapest string input"),
            ("    items.push(Item({name: name, quantity: quantity}));", "copy calldata fields into a new storage Item"),
            ("}", "end addItem"),
            ("", ""),
            ("function updateFirst(string memory newName, uint256 newQuantity) external {", "memory args are temporary mutable copies"),
            ("    require(items.length > 0, \"empty\");", "abort if there is nothing to update"),
            ("", ""),
            ("    Item storage storageRef = items[0];", "storage pointer ALIASES on-chain slot 0"),
            ("    storageRef.name = newName;", "this write PERSISTS on the blockchain"),
            ("    storageRef.quantity = newQuantity;", "this write also PERSISTS"),
            ("", ""),
            ("    Item memory memCopy = items[0];", "memory copy is a temporary SNAPSHOT"),
            ("    memCopy.quantity = memCopy.quantity + 1;", "local only — does NOT write back to storage"),
            ("}", "end updateFirst"),
        ],
        note="File: contracts/02-types-and-data/DataLocations.sol — storageRef persists; memCopy does not",
    )

    # ===== MODULE 03 =====
    content_slide(
        prs,
        "Module 03",
        "Functions & Control Flow",
        [
            "Visibility.sol — public / private / internal / external",
            "ViewPurePayable.sol — view, pure, payable, receive, fallback",
            "ControlFlow.sol — if/else, for, while, require, revert, assert",
            "Visibility controls who can call; mutability controls what state access is allowed",
        ],
        image=ASSETS / "visibility.png",
    )

    keyword_table_slide(
        prs,
        "Module 03",
        "Visibility & Mutability Keywords",
        [
            ("public", "Inside + outside. State vars get an automatic getter function.", "function publicFn() public"),
            ("external", "Only from outside. Cheaper for large calldata arguments.", "function externalFn() external"),
            ("internal", "This contract + inheriting children. Not in external ABI.", "function internalFn() internal"),
            ("private", "Only this contract — children cannot call it.", "function privateFn() private"),
            ("this", "The current contract as an external address — used to call external from inside.", "this.externalFn()"),
            ("pure", "Neither reads nor writes contract state — only args & locals.", "function add(a,b) public pure"),
            ("view", "May read state; compiler forbids writes.", "function getBalance() public view"),
            ("payable", "Function is allowed to receive ETH via msg.value.", "function deposit() public payable"),
            ("msg.value", "Amount of wei sent with the call.", "totalReceived += msg.value"),
            ("receive()", "Triggered on plain ETH transfer with empty calldata.", "receive() external payable"),
            ("fallback()", "No matching function selector, or non-empty unmatched calldata.", "fallback() external payable"),
            ("address(this).balance", "How much ETH the contract currently holds.", "return address(this).balance"),
        ],
    )

    keyword_table_slide(
        prs,
        "Module 03",
        "Control-Flow & Error Keywords",
        [
            ("if / else if / else", "Branch based on a condition.", "if (n % 2 == 0) return \"even\""),
            ("for", "Counted loop. Watch gas — unbounded loops can run out of gas.", "for (uint i = 1; i <= n; i++)"),
            ("while", "Loop while a condition stays true.", "while (i < times) { … }"),
            ("require(cond, msg)", "Validate inputs/conditions; on fail revert + refund remaining gas.", "require(value > 0, \"must be positive\")"),
            ("revert(msg)", "Unconditionally abort the call with a message.", "revert(reason)"),
            ("assert(cond)", "Internal invariant. Failure → Panic (should \"never\" happen).", "assert(result >= a)"),
            ("%", "Modulo operator — remainder after division.", "n % 2 == 0"),
            ("++", "Increment by one.", "counter++"),
        ],
        intro="Prefer custom errors (Module 05) over long require strings for gas savings.",
    )

    code_slide(
        prs,
        "Code · 03",
        "Visibility.sol — key lines explained",
        [
            ("uint256 public publicValue = 1;", "anyone can read; auto-getter publicValue()"),
            ("uint256 private privateValue = 2;", "only this contract's code can use it"),
            ("uint256 internal internalValue = 3;", "this contract + child contracts"),
            ("", ""),
            ("function publicFn() public pure returns (string memory) {", "callable inside and outside"),
            ("    return \"public\";", "return a temporary string"),
            ("}", ""),
            ("function privateFn() private pure returns (string memory) {", "only callable inside this contract"),
            ("    return \"private\";", "not visible in the external ABI"),
            ("}", ""),
            ("function externalFn() external pure returns (string memory) {", "only from outside (or via this)"),
            ("    return \"external\";", "good for large calldata args"),
            ("}", ""),
            ("function callExternalFromInside() public view returns (string memory) {", "call external from inside"),
            ("    return this.externalFn();", "this. makes an external-style call"),
            ("}", ""),
            ("contract VisibilityChild is Visibility {", "child inherits from Visibility"),
            ("    function readInternal() public view returns (uint256) { return internalValue; }", "child CAN read internal state"),
            ("}", "child CANNOT call privateFn"),
        ],
        note="File: contracts/03-functions-control/Visibility.sol",
    )

    code_slide(
        prs,
        "Code · 03",
        "ViewPurePayable.sol — key lines explained",
        [
            ("uint256 public totalReceived;", "running total of ETH this contract has recorded"),
            ("address public lastSender;", "last address that sent ETH here"),
            ("", ""),
            ("function add(uint256 a, uint256 b) public pure returns (uint256) {", "pure: no state read or write"),
            ("    return a + b;", "compute only from arguments"),
            ("}", ""),
            ("function getBalance() public view returns (uint256) {", "view: may read state, not write"),
            ("    return address(this).balance;", "ETH balance of this contract"),
            ("}", ""),
            ("function deposit() public payable {", "payable: may receive ETH with the call"),
            ("    require(msg.value > 0, \"send ETH\");", "reject zero-value deposits"),
            ("    totalReceived += msg.value;", "add wei sent in this call"),
            ("    lastSender = msg.sender;", "record who sent it"),
            ("}", ""),
            ("receive() external payable {", "handles plain ETH with empty calldata"),
            ("    totalReceived += msg.value;", "still track the amount"),
            ("    lastSender = msg.sender;", "still track the sender"),
            ("}", "fallback() catches unmatched function calls"),
        ],
        note="File: contracts/03-functions-control/ViewPurePayable.sol",
    )

    code_slide(
        prs,
        "Code · 03",
        "ControlFlow.sol — key lines explained",
        [
            ("function classify(uint256 n) public pure returns (string memory) {", "branch on a number"),
            ("    if (n == 0) { return \"zero\"; }", "exact match for zero"),
            ("    else if (n % 2 == 0) { return \"even\"; }", "remainder 0 ⇒ even"),
            ("    else { return \"odd\"; }", "otherwise odd"),
            ("}", ""),
            ("function sumTo(uint256 n) public pure returns (uint256 sum) {", "named return variable sum"),
            ("    for (uint256 i = 1; i <= n; i++) {", "count from 1 to n inclusive"),
            ("        sum += i;", "accumulate into the return variable"),
            ("    }", "end loop"),
            ("}", ""),
            ("function mustBePositive(int256 value) public pure {", "input validation demo"),
            ("    require(value > 0, \"must be positive\");", "revert + refund leftover gas if false"),
            ("}", ""),
            ("function forceRevert(string memory reason) public pure {", "unconditional abort"),
            ("    revert(reason);", "stop execution with a message"),
            ("}", ""),
            ("function checkInvariant(uint256 a, uint256 b) public pure returns (uint256) {", "assert demo"),
            ("    uint256 result = a + b;", "add (0.8+ reverts on overflow)"),
            ("    assert(result >= a);", "Panic if invariant somehow fails"),
            ("    return result;", "return the sum"),
            ("}", ""),
        ],
        note="File: contracts/03-functions-control/ControlFlow.sol",
    )

    # ===== MODULE 04 OOP =====
    content_slide(
        prs,
        "Module 04",
        "OOP in Solidity — The Big Picture",
        [
            "Solidity is contract-oriented — classic OOP ideas still apply",
            "Inheritance with is, virtual, override",
            "Multiple inheritance uses C3 linearization (like Python)",
            "abstract contracts + interface for shared blueprints",
            "Encapsulation via private state + modifiers",
            "Libraries = reusable utilities with using … for",
        ],
        image=ASSETS / "inheritance.png",
    )

    keyword_table_slide(
        prs,
        "Module 04",
        "OOP Keywords — Inheritance & Polymorphism",
        [
            ("is", "Inherit from one or more parent contracts.", "contract Dog is Animal"),
            ("virtual", "Marks a function so children are allowed to override it.", "function speak() public pure virtual"),
            ("override", "Replace a parent's virtual function in the child.", "function speak() public pure override"),
            ("super", "Call the next contract up the C3 linearization chain.", "super.greet()"),
            ("override(A, B)", "When multiple parents define the same function, list them.", "override(B, C)"),
            ("abstract", "Contract with missing function bodies — cannot deploy until complete.", "abstract contract Shape"),
            ("interface", "Only function signatures (implicitly external). No state, no constructor.", "interface ICounter"),
            ("polymorphism", "Same call site, different runtime behavior via overrides.", "Checkout.checkout(PaymentMethod)"),
            ("abi.encodePacked", "Tightly pack values into bytes (used here for string concat demos).", "abi.encodePacked(\"Dog: \", name)"),
            ("string.concat / pack", "Build strings from pieces (encodePacked is the demo style here).", "return string(abi.encodePacked(...))"),
        ],
        intro="These are the words that make \"is-a\" relationships and runtime dispatch work.",
    )

    keyword_table_slide(
        prs,
        "Module 04",
        "Encapsulation, Libraries & Related Keywords",
        [
            ("encapsulation", "Hide internals; expose a safe public API only.", "private balance + withdraw()"),
            ("modifier", "Reusable wrapper of checks around a function body.", "modifier onlyOwner() { … _; }"),
            ("_", "Placeholder inside a modifier — where the real function body runs.", "_;"),
            ("library", "Reusable code (often inlined if functions are internal).", "library MathLib"),
            ("using X for Y", "Attach library functions as methods on type Y.", "using MathLib for uint256 → a.max(b)"),
            ("internal library fn", "Usually embedded into calling contract bytecode.", "function max(...) internal pure"),
            ("event Deposited", "Logs deposits without storing history in expensive storage.", "emit Deposited(msg.sender, msg.value)"),
            ("call{value}", "Low-level ETH send with adjustable gas (preferred over transfer).", "(bool ok,) = payable(to).call{value: amount}(\"\")"),
        ],
    )

    two_col_slide(
        prs,
        "Module 04",
        "OOP Labs to Try",
        "Inheritance demos",
        [
            "Deploy Dog(\"Rex\") → speak() = \"woof\"",
            "Deploy D → greet() = \"A -> B -> C -> D\"",
            "Deploy Rectangle(3,4) & Circle(10)",
            "Compare area() and name()",
            "See Inheritance.test.js",
        ],
        "Interfaces / libs / bank",
        [
            "Deploy Counter + CounterUser",
            "bumpTwice(counterAddress)",
            "Checkout with Cash vs Card",
            "BankAccount: deposit anyone, withdraw owner",
            "LibraryDemo: bigger / bounded / total",
        ],
    )

    code_slide(
        prs,
        "Code · 04",
        "Inheritance.sol — every line explained",
        [
            ("contract Animal {", "base (parent) contract"),
            ("    string public name;", "shared state inherited by children"),
            ("    constructor(string memory _name) { name = _name; }", "parent constructor sets name once"),
            ("    function speak() public pure virtual returns (string memory) {", "virtual = children MAY override"),
            ("        return \"...\";", "default sound for a generic animal"),
            ("    }", ""),
            ("    function describe() public view virtual returns (string memory) {", "virtual so Dog can customize"),
            ("        return string(abi.encodePacked(\"Animal: \", name));", "pack strings together into one"),
            ("    }", ""),
            ("}", "end Animal"),
            ("", ""),
            ("contract Dog is Animal {", "is = Dog inherits Animal (is-a)"),
            ("    constructor(string memory _name) Animal(_name) {}", "call parent constructor with _name"),
            ("    function speak() public pure override returns (string memory) {", "override replaces parent's speak"),
            ("        return \"woof\";", "Dog-specific return value"),
            ("    }", ""),
            ("    function describe() public view override returns (string memory) {", "override describe too"),
            ("        return string(abi.encodePacked(\"Dog: \", name));", "uses inherited name from Animal"),
            ("    }", ""),
            ("}", "end Dog"),
        ],
        note="File: contracts/04-oop/Inheritance.sol",
    )

    code_slide(
        prs,
        "Code · 04",
        "MultipleInheritance.sol — C3 / super explained",
        [
            ("contract A {", "most base contract"),
            ("    function greet() public pure virtual returns (string memory) { return \"A\"; }", "virtual so children can override"),
            ("}", ""),
            ("contract B is A {", "B inherits A"),
            ("    function greet() public pure virtual override returns (string memory) {", "override A, still virtual for D"),
            ("        return string(abi.encodePacked(super.greet(), \" -> B\"));", "super → next in C3 chain (A)"),
            ("    }", ""),
            ("}", ""),
            ("contract C is A {", "C also inherits A (diamond)"),
            ("    function greet() public pure virtual override returns (string memory) {", "override A"),
            ("        return string(abi.encodePacked(super.greet(), \" -> C\"));", "super continues the chain"),
            ("    }", ""),
            ("}", ""),
            ("contract D is B, C {", "D inherits B and C (right-most first for super)"),
            ("    function greet() public pure override(B, C) returns (string memory) {", "must list both parents"),
            ("        return string(abi.encodePacked(super.greet(), \" -> D\"));", "path: D → C → B → A"),
            ("    }", "result: \"A -> B -> C -> D\""),
            ("}", ""),
        ],
        note="File: contracts/04-oop/MultipleInheritance.sol",
    )

    code_slide(
        prs,
        "Code · 04",
        "Abstract + Interface — every line explained",
        [
            ("abstract contract Shape {", "abstract = cannot deploy until complete"),
            ("    function area() public view virtual returns (uint256);", "declared but NO body — child must implement"),
            ("    function name() public pure virtual returns (string memory) {", "optional default implementation"),
            ("        return \"Shape\";", "default name"),
            ("    }", ""),
            ("}", ""),
            ("contract Rectangle is Shape {", "concrete child — can be deployed"),
            ("    uint256 public width; uint256 public height;", "rectangle dimensions in storage"),
            ("    constructor(uint256 _width, uint256 _height) { width = _width; height = _height; }", "set sides at deploy"),
            ("    function area() public view override returns (uint256) { return width * height; }", "implements required area()"),
            ("}", ""),
            ("", ""),
            ("interface ICounter {", "signatures only — no state, no constructor"),
            ("    function increment() external;", "all interface fns are implicitly external"),
            ("    function current() external view returns (uint256);", "read current count"),
            ("}", ""),
            ("contract Counter is ICounter {", "Counter promises to implement ICounter"),
            ("    uint256 private count;", "hidden counter state"),
            ("    function increment() external override { count += 1; }", "fulfill interface"),
            ("    function current() external view override returns (uint256) { return count; }", "fulfill interface"),
            ("}", ""),
        ],
        note="Files: AbstractContracts.sol · Interfaces.sol",
    )

    code_slide(
        prs,
        "Code · 04",
        "Encapsulation.sol (BankAccount) — key lines",
        [
            ("address private owner;", "hidden owner — no public auto-getter"),
            ("uint256 private balance;", "hidden balance — only changed via functions"),
            ("event Deposited(address indexed from, uint256 amount);", "log deposits"),
            ("event Withdrawn(address indexed to, uint256 amount);", "log withdrawals"),
            ("", ""),
            ("modifier onlyOwner() {", "encapsulation helper for access control"),
            ("    require(msg.sender == owner, \"not owner\");", "reject non-owners"),
            ("    _;", "then run the function body"),
            ("}", ""),
            ("constructor() { owner = msg.sender; }", "deployer becomes private owner"),
            ("", ""),
            ("function deposit() external payable {", "anyone may deposit ETH"),
            ("    require(msg.value > 0, \"zero\");", "reject empty deposit"),
            ("    balance += msg.value;", "increase private balance"),
            ("    emit Deposited(msg.sender, msg.value);", "log it"),
            ("}", ""),
            ("function withdraw(uint256 amount) external onlyOwner {", "only owner can withdraw"),
            ("    require(amount <= balance, \"insufficient\");", "check funds"),
            ("    balance -= amount;", "effect before interaction"),
            ("    (bool ok, ) = payable(msg.sender).call{value: amount}(\"\");", "send ETH out"),
            ("    require(ok, \"transfer failed\"); emit Withdrawn(msg.sender, amount);", "verify + log"),
            ("}", "outside code cannot assign balance directly"),
        ],
        note="File: contracts/04-oop/Encapsulation.sol",
    )

    code_slide(
        prs,
        "Code · 04",
        "Libraries.sol — every line explained",
        [
            ("library MathLib {", "reusable utility code (not a normal contract)"),
            ("    function max(uint256 a, uint256 b) internal pure returns (uint256) {", "internal ⇒ often inlined into caller"),
            ("        return a >= b ? a : b;", "ternary: return the larger value"),
            ("    }", ""),
            ("    function min(uint256 a, uint256 b) internal pure returns (uint256) {", "return the smaller value"),
            ("        return a < b ? a : b;", ""),
            ("    }", ""),
            ("    function clamp(uint256 value, uint256 lo, uint256 hi) internal pure returns (uint256) {", "force value into [lo, hi]"),
            ("        return max(lo, min(value, hi));", "compose min and max"),
            ("    }", ""),
            ("}", ""),
            ("contract LibraryDemo {", "demo contract that uses the library"),
            ("    using MathLib for uint256;", "attach MathLib methods onto uint256"),
            ("    using ArrayLib for uint256[];", "attach ArrayLib methods onto arrays"),
            ("    function bigger(uint256 a, uint256 b) public pure returns (uint256) {", "public wrapper"),
            ("        return a.max(b);", "same as MathLib.max(a, b) thanks to using-for"),
            ("    }", ""),
            ("    function bounded(uint256 value) public pure returns (uint256) {", "clamp demo"),
            ("        return value.clamp(10, 100);", "result always between 10 and 100"),
            ("    }", ""),
            ("}", ""),
        ],
        note="File: contracts/04-oop/Libraries.sol",
    )

    # ===== MODULE 05 =====
    keyword_table_slide(
        prs,
        "Module 05",
        "Events, Errors & Modifiers — Keywords",
        [
            ("modifier", "Named check that wraps functions; stackable.", "onlyOwner whenNotPaused"),
            ("onlyOwner", "Custom modifier: require msg.sender == owner.", "Modifiers.sol"),
            ("whenNotPaused", "Blocks actions while paused == true.", "require(!paused, \"paused\")"),
            ("indexed", "Makes an event parameter a searchable topic (max 3).", "address indexed from"),
            ("event", "Cheap log — not contract storage; indexers subscribe.", "event Transfer(...)"),
            ("error", "Custom revert type — cheaper than require strings.", "error Unauthorized(address caller)"),
            ("revert ErrorName()", "Abort with a typed custom error.", "revert InsufficientBalance(a, b)"),
            ("paused", "Simple circuit-breaker flag pattern.", "bool public paused"),
        ],
        intro="Module files: Modifiers.sol, Events.sol, CustomErrors.sol",
    )

    two_col_slide(
        prs,
        "Module 05",
        "Why Events & Custom Errors Matter",
        "Events",
        [
            "Append-only logs in the transaction receipt",
            "Much cheaper than writing history to storage",
            "Up to 3 indexed args → filterable topics",
            "Wallets & The Graph listen for them",
            "Try: transfer() then inspect Transfer log",
        ],
        "Custom errors",
        [
            "Declared with: error Name(args…)",
            "Triggered with: revert Name(args)",
            "Lower gas than long require strings",
            "Typed fields help UIs decode failures",
            "Try: withdraw more than balance",
        ],
    )

    code_slide(
        prs,
        "Code · 05",
        "Modifiers.sol — every line explained",
        [
            ("address public owner;", "who is allowed to admin the contract"),
            ("bool public paused;", "circuit-breaker flag"),
            ("uint256 public value;", "sample state protected by modifiers"),
            ("", ""),
            ("modifier onlyOwner() {", "reusable access-control wrapper"),
            ("    require(msg.sender == owner, \"not owner\");", "reject callers who are not owner"),
            ("    _;", "_ = run the actual function body here"),
            ("}", ""),
            ("modifier whenNotPaused() {", "block actions while paused"),
            ("    require(!paused, \"paused\");", "require paused is false"),
            ("    _;", "then continue into the function"),
            ("}", ""),
            ("modifier validAmount(uint256 amount) {", "modifier with an argument"),
            ("    require(amount > 0 && amount <= 1000, \"invalid amount\");", "range check"),
            ("    _;", "then continue"),
            ("}", ""),
            ("constructor() { owner = msg.sender; }", "deployer becomes owner"),
            ("function setPaused(bool _paused) external onlyOwner { paused = _paused; }", "only owner can pause/unpause"),
            ("function setValue(uint256 amount) external onlyOwner whenNotPaused validAmount(amount) {", "THREE modifiers stacked"),
            ("    value = amount;", "runs only if all modifiers pass"),
            ("}", ""),
        ],
        note="File: contracts/05-events-errors-modifiers/Modifiers.sol",
    )

    code_slide(
        prs,
        "Code · 05",
        "Events.sol + CustomErrors.sol — key lines",
        [
            ("event Transfer(address indexed from, address indexed to, uint256 amount);", "indexed = searchable topic (max 3)"),
            ("event Message(address indexed sender, string text);", "string text is NOT indexed (in data payload)"),
            ("mapping(address => uint256) public balances;", "simple internal balance ledger"),
            ("constructor() { balances[msg.sender] = 1000; }", "seed deployer with 1000 units"),
            ("function transfer(address to, uint256 amount) external {", "move internal balances"),
            ("    require(balances[msg.sender] >= amount, \"insufficient\");", "check sender has enough"),
            ("    balances[msg.sender] -= amount;", "effect: decrease sender"),
            ("    balances[to] += amount;", "effect: increase recipient"),
            ("    emit Transfer(msg.sender, to, amount);", "cheap log for wallets/indexers"),
            ("}", ""),
            ("", ""),
            ("error Unauthorized(address caller);", "custom error type with a field"),
            ("error InsufficientBalance(uint256 available, uint256 required);", "typed fields for better UX"),
            ("error ZeroAddress();", "error with no arguments"),
            ("if (msg.sender != owner) { revert Unauthorized(msg.sender); }", "typed revert instead of require string"),
            ("if (amount > available) { revert InsufficientBalance(available, amount); }", "cheaper gas than long strings"),
        ],
        note="Files: Events.sol · CustomErrors.sol",
    )

    # ===== MODULE 06 =====
    content_slide(
        prs,
        "Module 06",
        "Advanced Patterns",
        [
            "ConstructorImmutable — constant vs immutable vs normal storage",
            "EtherWallet — receive / send ETH safely with call",
            "CallDelegatecall — call writes target storage; delegatecall writes yours",
            "AssemblyBasics — Yul for add / sstore / sload / extcodesize",
            "SecurityPatterns — CEI + nonReentrant guard",
        ],
        image=ASSETS / "call_delegatecall.png",
    )

    keyword_table_slide(
        prs,
        "Module 06",
        "Advanced Keywords Explained",
        [
            ("constant", "Value fixed at compile time; no storage slot; inlined.", "uint256 public constant MAX_SUPPLY"),
            ("immutable", "Set once in constructor; then forever read-only; cheaper reads.", "address public immutable deployer"),
            ("block.timestamp", "Current block time (seconds). Miner-influenceable — don't overtrust.", "createdAt = block.timestamp"),
            ("receive()", "Handles plain ETH with empty calldata.", "EtherWallet.receive"),
            ("call", "Low-level call — runs target code in target's storage context.", "logic.call(abi.encodeWithSignature(...))"),
            ("delegatecall", "Runs target CODE but uses CALLER storage — proxy pattern.", "logic.delegatecall(...)"),
            ("abi.encodeWithSignature", "Encode a function call payload from signature + args.", "\"setNumber(uint256)\""),
            ("assembly / Yul", "Inline low-level language inside Solidity.", "assembly { result := add(a,b) }"),
            ("sstore / sload", "Write/read a storage slot directly in assembly.", "sstore(0, value)"),
            ("extcodesize", "Bytecode size of an address (0 often means EOA).", "size := extcodesize(account)"),
            ("nonReentrant", "Modifier that blocks re-entering a function mid-call.", "locked flag"),
            ("CEI pattern", "Checks → Effects → Interactions order to stop reentrancy bugs.", "update balance BEFORE call"),
        ],
    )

    content_slide(
        prs,
        "Module 06",
        "Security: Checks-Effects-Interactions",
        [
            "1) Checks — validate amount, permissions, balances",
            "2) Effects — update your own storage first",
            "3) Interactions — only then call out / send ETH",
            "Reentrancy: attacker re-enters withdraw before balance updates",
            "Guard: nonReentrant locked flag around sensitive functions",
            "Prefer call over transfer/send (2300 gas stipend is brittle)",
        ],
        image=ASSETS / "cei.png",
    )

    code_slide(
        prs,
        "Code · 06",
        "ConstructorImmutable + EtherWallet — key lines",
        [
            ("uint256 public constant MAX_SUPPLY = 1_000_000;", "compile-time constant — no storage slot"),
            ("address public immutable deployer;", "set once in constructor, then forever read-only"),
            ("uint256 public immutable createdAt;", "immutable timestamp captured at deploy"),
            ("string public name;", "normal storage — can change later if you add a setter"),
            ("constructor(string memory _name) {", "runs once at deployment"),
            ("    deployer = msg.sender;", "lock deployer address into immutable"),
            ("    createdAt = block.timestamp;", "lock current block time"),
            ("    name = _name;", "store the name argument"),
            ("}", ""),
            ("", ""),
            ("receive() external payable { emit Deposited(msg.sender, msg.value); }", "accept plain ETH transfers"),
            ("function deposit() external payable {", "explicit payable deposit"),
            ("    require(msg.value > 0, \"zero\");", "reject empty deposits"),
            ("    emit Deposited(msg.sender, msg.value);", "log the deposit"),
            ("}", ""),
            ("function withdraw(uint256 amount) external {", "owner pulls ETH out"),
            ("    require(msg.sender == owner, \"not owner\");", "access control"),
            ("    require(address(this).balance >= amount, \"insufficient\");", "enough ETH in contract?"),
            ("    (bool ok, ) = payable(msg.sender).call{value: amount}(\"\");", "preferred ETH send (flexible gas)"),
            ("    require(ok, \"call failed\");", "revert if the ETH transfer failed"),
            ("}", ""),
        ],
        note="Files: ConstructorImmutable.sol · EtherWallet.sol",
    )

    code_slide(
        prs,
        "Code · 06",
        "CallDelegatecall.sol — every line explained",
        [
            ("contract Logic {", "target contract with its own storage"),
            ("    uint256 public number;", "Logic's storage slot for number"),
            ("    address public sender;", "Logic's storage slot for sender"),
            ("    function setNumber(uint256 _number) external {", "writes into whichever context is active"),
            ("        number = _number;", "write number"),
            ("        sender = msg.sender;", "record caller"),
            ("    }", ""),
            ("}", ""),
            ("contract Caller {", "has SAME storage layout shape as Logic"),
            ("    uint256 public number;", "Caller's own number slot"),
            ("    address public sender;", "Caller's own sender slot"),
            ("    function callSetNumber(address logic, uint256 _number) external {", "normal external call"),
            ("        (bool ok, ) = logic.call(abi.encodeWithSignature(\"setNumber(uint256)\", _number));", "run Logic code in Logic storage"),
            ("        require(ok, \"call failed\");", "bubble up failure"),
            ("    }", "result: Logic.number changes"),
            ("    function delegateSetNumber(address logic, uint256 _number) external {", "delegatecall path"),
            ("        (bool ok, ) = logic.delegatecall(abi.encodeWithSignature(\"setNumber(uint256)\", _number));", "run Logic CODE in Caller STORAGE"),
            ("        require(ok, \"delegatecall failed\");", "bubble up failure"),
            ("    }", "result: Caller.number changes — proxy pattern"),
            ("}", "⚠ never delegatecall untrusted contracts"),
        ],
        note="File: contracts/06-advanced/CallDelegatecall.sol",
    )

    code_slide(
        prs,
        "Code · 06",
        "SecurityPatterns.sol — CEI + nonReentrant",
        [
            ("mapping(address => uint256) public balances;", "per-user ETH accounting"),
            ("bool private locked;", "reentrancy lock flag"),
            ("error ReentrantCall();", "custom error if re-entered"),
            ("", ""),
            ("modifier nonReentrant() {", "simple mutex around a function"),
            ("    if (locked) revert ReentrantCall();", "already inside? abort"),
            ("    locked = true;", "take the lock"),
            ("    _;", "run the function body"),
            ("    locked = false;", "release the lock"),
            ("}", ""),
            ("function deposit() external payable {", "credit the sender"),
            ("    balances[msg.sender] += msg.value;", "effects only — no external call"),
            ("}", ""),
            ("function withdraw(uint256 amount) external nonReentrant {", "guarded withdraw"),
            ("    require(amount > 0, \"zero\");", "CHECK: amount must be positive"),
            ("    require(balances[msg.sender] >= amount, \"insufficient\");", "CHECK: enough balance"),
            ("    balances[msg.sender] -= amount;", "EFFECT: update state BEFORE interaction"),
            ("    (bool ok, ) = payable(msg.sender).call{value: amount}(\"\");", "INTERACTION: send ETH last"),
            ("    require(ok, \"transfer failed\");", "revert if send failed (state already updated)"),
            ("}", "CEI order stops classic reentrancy"),
        ],
        note="File: contracts/06-advanced/SecurityPatterns.sol",
    )

    code_slide(
        prs,
        "Code · 06",
        "AssemblyBasics.sol — every line explained",
        [
            ("uint256 public stored;", "first state variable → storage slot 0"),
            ("", ""),
            ("function addAssembly(uint256 a, uint256 b) external pure returns (uint256 result) {", "pure add via Yul"),
            ("    assembly {", "enter inline assembly block"),
            ("        result := add(a, b)", "Yul add — assign into Solidity return var"),
            ("    }", "leave assembly"),
            ("}", ""),
            ("function storeAssembly(uint256 value) external {", "write storage via Yul"),
            ("    assembly {", ""),
            ("        sstore(0, value)", "store value into slot 0 (the `stored` variable)"),
            ("    }", ""),
            ("}", ""),
            ("function loadAssembly() external view returns (uint256 value) {", "read storage via Yul"),
            ("    assembly {", ""),
            ("        value := sload(0)", "load slot 0 into return variable"),
            ("    }", ""),
            ("}", ""),
            ("function getCodeSize(address account) external view returns (uint256 size) {", "bytecode size of an address"),
            ("    assembly { size := extcodesize(account) }", "0 often means EOA (no code)"),
            ("}", "use sparingly — easy to bypass Solidity safety"),
        ],
        note="File: contracts/06-advanced/AssemblyBasics.sol",
    )

    # ===== MODULE 07 =====
    content_slide(
        prs,
        "Module 07",
        "Tokens — ERC-20 & ERC-721",
        [
            "ERC-20 = fungible (interchangeable) tokens — stablecoins, governance…",
            "ERC-721 = NFTs — each tokenId is unique",
            "This repo ships minimal teaching implementations (not production)",
            "Production apps should use audited libraries (e.g. OpenZeppelin)",
            "Tests cover mint, transfer, approve + transferFrom for ERC-20",
        ],
        image=ASSETS / "erc20_flow.png",
    )

    keyword_table_slide(
        prs,
        "Module 07",
        "ERC-20 Keywords Explained",
        [
            ("ERC-20", "Standard interface for fungible tokens on Ethereum.", "SimpleERC20.sol"),
            ("name / symbol", "Human-readable token identity.", "\"Practice Token\", \"PRAC\""),
            ("decimals", "How many decimal places (usually 18, like ETH).", "uint8 public constant decimals = 18"),
            ("totalSupply", "All tokens currently existing.", "totalSupply += value on mint"),
            ("balanceOf", "How many tokens an address holds.", "mapping(address => uint256)"),
            ("transfer", "Send your own tokens to another address.", "transfer(to, value)"),
            ("approve", "Authorize a spender to move up to value of your tokens.", "approve(spender, value)"),
            ("allowance", "Remaining amount spender may transferFrom owner.", "allowance[owner][spender]"),
            ("transferFrom", "Spender moves tokens from owner within allowance.", "transferFrom(from, to, value)"),
            ("_mint", "Internal create tokens (Transfer from address(0)).", "_mint(msg.sender, initialSupply)"),
            ("parseEther", "JS helper: \"1\" → 1e18 wei/units (ethers.js).", "ethers.parseEther(\"1000\")"),
            ("type(uint256).max", "Max uint — often means \"infinite\" allowance.", "skip decrement if max"),
        ],
    )

    keyword_table_slide(
        prs,
        "Module 07",
        "ERC-721 Keywords Explained",
        [
            ("ERC-721", "Standard for non-fungible tokens (unique IDs).", "SimpleERC721.sol"),
            ("tokenId", "Unique identifier for one NFT.", "uint256 tokenId"),
            ("ownerOf", "Returns the owner address of a tokenId.", "ownerOf(tokenId)"),
            ("balanceOf", "How many NFTs an address owns (count, not fungible amount).", "balanceOf(owner)"),
            ("mint", "Create a new tokenId and assign an owner (learning helper).", "mint(to)"),
            ("approve", "Allow one address to transfer a specific tokenId.", "approve(to, tokenId)"),
            ("getApproved", "Who is currently approved for that tokenId.", "getApproved(tokenId)"),
            ("transferFrom", "Move a specific NFT if caller is owner or approved.", "transferFrom(from, to, id)"),
            ("delete", "Reset a storage variable to its zero value.", "delete _tokenApprovals[tokenId]"),
            ("address(0)", "The zero address — often means \"none\" / burn / mint source.", "require(to != address(0))"),
        ],
        intro="Simplified teaching NFT — omits full ERC-165 / setApprovalForAll edge cases.",
    )

    code_slide(
        prs,
        "Code · 07",
        "SimpleERC20.sol — core lines explained",
        [
            ("string public name;", "token display name"),
            ("string public symbol;", "short ticker like PRAC"),
            ("uint8 public constant decimals = 18;", "18 decimals like ETH"),
            ("uint256 public totalSupply;", "all tokens in existence"),
            ("mapping(address => uint256) public balanceOf;", "address → token balance"),
            ("mapping(address => mapping(address => uint256)) public allowance;", "owner → spender → allowance"),
            ("event Transfer(address indexed from, address indexed to, uint256 value);", "required ERC-20 log"),
            ("event Approval(address indexed owner, address indexed spender, uint256 value);", "required approval log"),
            ("constructor(string memory _name, string memory _symbol, uint256 initialSupply) {", "deploy + mint"),
            ("    name = _name; symbol = _symbol;", "store identity"),
            ("    _mint(msg.sender, initialSupply);", "give initial supply to deployer"),
            ("}", ""),
            ("function transfer(address to, uint256 value) external returns (bool) {", "send your own tokens"),
            ("    _transfer(msg.sender, to, value); return true;", "update balances + emit Transfer"),
            ("}", ""),
            ("function approve(address spender, uint256 value) external returns (bool) {", "authorize a spender"),
            ("    allowance[msg.sender][spender] = value;", "set how much they may spend"),
            ("    emit Approval(msg.sender, spender, value); return true;", "log approval"),
            ("}", ""),
            ("function transferFrom(address from, address to, uint256 value) external returns (bool) {", "spender moves owner's tokens"),
            ("    /* check allowance, decrease it, then _transfer(from,to,value) */", "see full file for exact lines"),
            ("}", ""),
        ],
        note="File: contracts/07-tokens/SimpleERC20.sol — learning only, not production",
    )

    code_slide(
        prs,
        "Code · 07",
        "SimpleERC20.sol — _transfer / _mint explained",
        [
            ("function _transfer(address from, address to, uint256 value) internal {", "shared transfer logic"),
            ("    require(to != address(0), \"zero to\");", "forbid sending to the zero address"),
            ("    require(balanceOf[from] >= value, \"balance\");", "sender must have enough"),
            ("    balanceOf[from] -= value;", "decrease sender balance"),
            ("    balanceOf[to] += value;", "increase recipient balance"),
            ("    emit Transfer(from, to, value);", "emit required Transfer event"),
            ("}", ""),
            ("", ""),
            ("function _mint(address to, uint256 value) internal {", "create new tokens"),
            ("    require(to != address(0), \"zero to\");", "cannot mint to zero address"),
            ("    totalSupply += value;", "increase global supply"),
            ("    balanceOf[to] += value;", "credit recipient"),
            ("    emit Transfer(address(0), to, value);", "mint convention: Transfer from address(0)"),
            ("}", ""),
            ("", ""),
            ("// inside transferFrom after reading allowance:", "spender path"),
            ("require(allowed >= value, \"allowance\");", "spender must be approved for enough"),
            ("if (allowed != type(uint256).max) {", "max uint often means infinite approval"),
            ("    allowance[from][msg.sender] = allowed - value;", "decrease remaining allowance"),
            ("}", "then call _transfer(from, to, value)"),
        ],
        note="Internal helpers keep transfer / transferFrom / mint consistent",
    )

    code_slide(
        prs,
        "Code · 07",
        "SimpleERC721.sol — every key line explained",
        [
            ("string public name; string public symbol;", "collection identity"),
            ("uint256 private nextId = 1;", "next tokenId to mint (starts at 1)"),
            ("mapping(uint256 => address) private _owners;", "tokenId → owner"),
            ("mapping(address => uint256) private _balances;", "owner → how many NFTs"),
            ("mapping(uint256 => address) private _tokenApprovals;", "tokenId → approved operator"),
            ("", ""),
            ("function ownerOf(uint256 tokenId) public view returns (address) {", "who owns this NFT?"),
            ("    address owner = _owners[tokenId];", "lookup owner"),
            ("    require(owner != address(0), \"nonexistent\");", "token must exist"),
            ("    return owner;", "return owner address"),
            ("}", ""),
            ("function mint(address to) external returns (uint256 tokenId) {", "create a new unique NFT"),
            ("    require(to != address(0), \"zero\");", "valid recipient"),
            ("    tokenId = nextId++;", "assign id then bump counter"),
            ("    _owners[tokenId] = to; _balances[to] += 1;", "record ownership"),
            ("    emit Transfer(address(0), to, tokenId);", "mint log (from zero address)"),
            ("}", ""),
            ("function transferFrom(address from, address to, uint256 tokenId) external {", "move one NFT"),
            ("    require(msg.sender == owner || msg.sender == _tokenApprovals[tokenId], \"not authorized\");", "caller must be owner or approved"),
            ("    delete _tokenApprovals[tokenId]; _balances[from] -= 1; _balances[to] += 1; _owners[tokenId] = to;", "clear approval + move"),
            ("}", ""),
        ],
        note="File: contracts/07-tokens/SimpleERC721.sol — simplified teaching NFT",
    )

    # ===== TESTS & DEPLOY =====
    two_col_slide(
        prs,
        "Tests & Deploy",
        "Automated Tests + Deploy Script",
        "Tests (npx hardhat test)",
        [
            "SimpleStorage.test.js — set/get + event",
            "Inheritance.test.js — Dog + D.greet C3 path",
            "SimpleERC20.test.js — mint / transfer / approve",
            "Stack: Mocha + Chai + ethers via toolbox",
            "expect(...).to.emit(...) for events",
        ],
        "Deploy (scripts/deploy.js)",
        [
            "Deploys HelloWorld(\"Hello, Solidity!\")",
            "Deploys SimpleStorage()",
            "Deploys SimpleERC20(PRAC, 1_000_000 ether)",
            "Logs deployer + contract addresses",
            "Use --network localhost with hardhat node",
        ],
    )

    keyword_table_slide(
        prs,
        "Tests & Deploy",
        "Hardhat / Ethers Test Keywords",
        [
            ("describe / it", "Mocha test suite and individual test case.", "describe(\"SimpleStorage\", …)"),
            ("expect", "Chai assertion helper.", "expect(await storage.get()).to.equal(42n)"),
            ("getContractFactory", "Load ABI + bytecode to deploy a contract in tests/scripts.", "ethers.getContractFactory(\"Dog\")"),
            ("deploy", "Send the deploying transaction.", "await Dog.deploy(\"Rex\")"),
            ("waitForDeployment", "Wait until contract address is available.", "await dog.waitForDeployment()"),
            ("getSigners", "Local test accounts with ETH.", "const [owner, alice] = await ethers.getSigners()"),
            ("connect", "Send next txs from a different signer.", "token.connect(alice).transferFrom(...)"),
            ("to.emit / withArgs", "Assert an event was logged with specific arguments.", ".to.emit(storage, \"NumberUpdated\")"),
            ("getAddress", "Read deployed contract address.", "await hello.getAddress()"),
        ],
    )

    code_slide(
        prs,
        "Code · Deploy",
        "scripts/deploy.js — every line explained",
        [
            ("const hre = require(\"hardhat\");", "load the Hardhat Runtime Environment"),
            ("", ""),
            ("async function main() {", "async entry point for the deploy script"),
            ("  const [deployer] = await hre.ethers.getSigners();", "first local account = deployer"),
            ("  console.log(\"Deploying with:\", deployer.address);", "print who is deploying"),
            ("", ""),
            ("  const HelloWorld = await hre.ethers.getContractFactory(\"HelloWorld\");", "load ABI + bytecode for HelloWorld"),
            ("  const hello = await HelloWorld.deploy(\"Hello, Solidity!\");", "send deploy tx with constructor arg"),
            ("  await hello.waitForDeployment();", "wait until the contract address exists"),
            ("  console.log(\"HelloWorld:\", await hello.getAddress());", "print deployed address"),
            ("", ""),
            ("  const SimpleStorage = await hre.ethers.getContractFactory(\"SimpleStorage\");", "load SimpleStorage factory"),
            ("  const storage = await SimpleStorage.deploy();", "deploy with no constructor args"),
            ("  await storage.waitForDeployment();", "wait for mining/local confirmation"),
            ("  console.log(\"SimpleStorage:\", await storage.getAddress());", "print address"),
            ("", ""),
            ("  const SimpleERC20 = await hre.ethers.getContractFactory(\"SimpleERC20\");", "load ERC-20 factory"),
            ("  const token = await SimpleERC20.deploy(\"Practice Token\", \"PRAC\", hre.ethers.parseEther(\"1000000\"));", "name, symbol, 1e6 * 1e18 units"),
            ("  await token.waitForDeployment();", "wait for deploy"),
            ("  console.log(\"SimpleERC20:\", await token.getAddress());", "print token address"),
            ("}", ""),
            ("main().catch((error) => { console.error(error); process.exitCode = 1; });", "run main; set exit code on failure"),
        ],
        note="Run: npx hardhat run scripts/deploy.js",
    )

    code_slide(
        prs,
        "Code · Test",
        "SimpleStorage.test.js — every line explained",
        [
            ("const { expect } = require(\"chai\");", "Chai assertions"),
            ("const { ethers } = require(\"hardhat\");", "ethers helpers from Hardhat"),
            ("", ""),
            ("describe(\"SimpleStorage\", function () {", "start a Mocha test suite"),
            ("  it(\"stores and retrieves a number\", async function () {", "one test case"),
            ("    const SimpleStorage = await ethers.getContractFactory(\"SimpleStorage\");", "load contract factory"),
            ("    const storage = await SimpleStorage.deploy();", "deploy a fresh instance for the test"),
            ("    await storage.waitForDeployment();", "wait until ready"),
            ("    await storage.set(42);", "write 42 into storage (sends a tx)"),
            ("    expect(await storage.get()).to.equal(42n);", "assert getter returns 42n (bigint)"),
            ("  });", "end first test"),
            ("", ""),
            ("  it(\"emits NumberUpdated\", async function () {", "event assertion test"),
            ("    const SimpleStorage = await ethers.getContractFactory(\"SimpleStorage\");", "load factory again"),
            ("    const storage = await SimpleStorage.deploy();", "fresh deploy"),
            ("    await storage.waitForDeployment();", "wait"),
            ("    await expect(storage.set(7))", "assert on the transaction"),
            ("      .to.emit(storage, \"NumberUpdated\")", "must emit NumberUpdated"),
            ("      .withArgs(0n, 7n);", "oldValue=0 (default), newValue=7"),
            ("  });", ""),
            ("});", "end suite"),
        ],
        note="Run all tests: npx hardhat test",
    )

    # ===== MASTER GLOSSARY =====
    keyword_table_slide(
        prs,
        "Glossary",
        "Master Glossary A–M",
        [
            ("ABI", "Application Binary Interface — JSON describing how to encode calls.", "artifacts/.../*.json"),
            ("bytecode", "EVM machine code deployed on-chain.", "Created by solc/Hardhat compile"),
            ("blockchain", "Append-only shared ledger of transactions & contract state.", "Ethereum, etc."),
            ("gas", "Unit of computation cost paid in ETH (or network token).", "Writes cost more than reads"),
            ("wei", "Smallest ETH unit. 1 ETH = 10^18 wei.", "msg.value is in wei"),
            ("EVM", "Ethereum Virtual Machine — executes contract bytecode.", "Target of solc output"),
            ("transaction", "Signed state-changing message broadcast to the network.", "setGreeting sends a tx"),
            ("eth_call", "Simulation/read call — no state change, usually free.", "view/pure via RPC"),
            ("NatSpec", "/// and /** */ documentation tags for humans & tools.", "@notice @dev @title"),
            ("msg.data", "Full calldata of the call.", "Used by fallback routing"),
            ("tx.origin", "Original EOA that started the tx (avoid for auth!).", "Prefer msg.sender"),
            ("EOA", "Externally Owned Account — wallet controlled by a private key.", "vs contract account"),
        ],
    )

    keyword_table_slide(
        prs,
        "Glossary",
        "Master Glossary N–Z & Patterns",
        [
            ("reentrancy", "Bug where external call re-enters your function before it finishes.", "Fix with CEI + guard"),
            ("proxy pattern", "Contract that delegatecalls logic elsewhere (upgrades).", "Needs matching storage layout"),
            ("storage layout", "Order of state variables → slot numbers.", "Breaks if proxy/impl mismatch"),
            ("indexer", "Off-chain service that reads events into a queryable DB.", "The Graph, custom listeners"),
            ("OpenZeppelin", "Audited contract libraries for tokens, access control, etc.", "Prefer over hand-rolled prod"),
            ("testnet", "Public chain with fake ETH for practice deploys.", "Sepolia, etc."),
            ("mainnet", "Production Ethereum network with real value.", "Do NOT deploy these demos there"),
            ("optimizer", "Compiler pass trading deploy size vs runtime gas.", "runs: 200 in config"),
            ("Panic", "Special revert from assert / overflow internals.", "Different from Error(string)"),
            ("C3 linearization", "Deterministic parent order for multiple inheritance.", "D is B, C → D,C,B,A"),
            ("fungible", "Units are interchangeable (ERC-20).", "1 token == any other 1 token"),
            ("non-fungible", "Each item is unique (ERC-721).", "tokenId 7 ≠ tokenId 8"),
        ],
    )

    # ===== CHEAT SHEET =====
    content_slide(
        prs,
        "Cheat Sheet",
        "OOP Code Patterns (Copy Mentally)",
        [
            "virtual + override → polymorphism",
            "abstract contract → shared base that cannot deploy alone",
            "interface → signatures only; all external; loose coupling",
            "library + using Lib for Type → a.max(b) style helpers",
            "modifier + _ → reusable access control / validation",
            "error + revert Error() → cheap typed failures",
            "Checks → Effects → Interactions → safer ETH handling",
        ],
    )

    # ===== CHECKLIST =====
    content_slide(
        prs,
        "Checklist",
        "25-File Learning Path",
        [
            "01 HelloWorld · SimpleStorage",
            "02 ValueTypes · ReferenceTypes · DataLocations",
            "03 Visibility · ViewPurePayable · ControlFlow",
            "04 Inheritance · MultipleInheritance · Abstract · Interfaces · Polymorphism · Encapsulation · Libraries",
            "05 Modifiers · Events · CustomErrors",
            "06 ConstructorImmutable · EtherWallet · CallDelegatecall · AssemblyBasics · SecurityPatterns",
            "07 SimpleERC20 · SimpleERC721",
            "Then: npx hardhat test  &&  npx hardhat run scripts/deploy.js",
        ],
    )

    # ===== QUIZ =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    add_text(slide, 0.8, 2.8, 11.5, 1, "End-of-Deck Quiz", size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, 0.8, 4.0, 11.5, 0.6, "Test yourself — answers on the following slides", size=20, color=TEAL, align=PP_ALIGN.CENTER)

    quiz = [
        (
            "Q1–Q4: Foundations",
            [
                "Q1. What does the pragma solidity ^0.8.24; line control?",
                "Q2. Difference between memory and calldata?",
                "Q3. Does a view function cost gas when called from a wallet UI via eth_call?",
                "Q4. What visibility can a child contract use from its parent: private or internal?",
            ],
        ),
        (
            "Q5–Q8: OOP & Patterns",
            [
                "Q5. What does the keyword is do in contract Dog is Animal?",
                "Q6. Why mark a function virtual?",
                "Q7. For D is B, C, what is the usual super linearization order?",
                "Q8. Can you deploy an abstract contract that still has unimplemented functions?",
            ],
        ),
        (
            "Q9–Q12: Advanced & Tokens",
            [
                "Q9. call vs delegatecall — whose storage is written?",
                "Q10. What does CEI stand for, and why does order matter?",
                "Q11. Name the four core ERC-20 transfer-related functions/mappings.",
                "Q12. How is an ERC-721 token different from an ERC-20 token?",
            ],
        ),
    ]
    for title, qs in quiz:
        content_slide(prs, "Quiz", title, qs)

    # Answers
    keyword_table_slide(
        prs,
        "Answers",
        "Quiz Answers 1–6",
        [
            ("Q1", "Allowed Solidity compiler versions for that file (^0.8.24 ⇒ ≥0.8.24 <0.9.0).", "Matches hardhat 0.8.24"),
            ("Q2", "memory = temporary mutable copy; calldata = read-only input (cheaper for external).", "DataLocations.sol"),
            ("Q3", "Typically no — eth_call simulations don't create a paid transaction.", "Writes always need a tx"),
            ("Q4", "internal (and public). private is invisible to children.", "VisibilityChild demo"),
            ("Q5", "Inheritance — Dog receives Animal's members and may override virtual fns.", "is-a relationship"),
            ("Q6", "So derived contracts are allowed to override that function.", "virtual + override pair"),
        ],
    )
    keyword_table_slide(
        prs,
        "Answers",
        "Quiz Answers 7–12",
        [
            ("Q7", "D → C → B → A (right-most parent first for super).", "greet = A -> B -> C -> D"),
            ("Q8", "No — abstract unfinished contracts cannot be deployed.", "Children must implement"),
            ("Q9", "call → target storage; delegatecall → caller storage.", "Proxy danger zone"),
            ("Q10", "Checks-Effects-Interactions; updating state before external calls stops reentrancy.", "SecurityPatterns.sol"),
            ("Q11", "transfer, approve, allowance, transferFrom (+ balanceOf/totalSupply).", "SimpleERC20"),
            ("Q12", "ERC-721 IDs are unique/non-fungible; ERC-20 units are interchangeable.", "ownerOf(tokenId)"),
        ],
    )

    # Discussion prompts
    content_slide(
        prs,
        "Discussion",
        "Open Questions for the Room",
        [
            "When would you choose calldata over memory for a function argument?",
            "Why is tx.origin a bad access-control check compared to msg.sender?",
            "How could a wrong storage layout break a proxy that uses delegatecall?",
            "What would you add to SimpleERC20 before any testnet deploy?",
            "Where do events help product UX more than storing history on-chain?",
            "How does Solidity 0.8+'s default overflow check change your coding habits?",
        ],
    )

    # Closing
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(6.2), Inches(13.333), Inches(1.3))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TEAL
    strip.line.fill.background()
    add_text(slide, 0.8, 2.0, 11.5, 0.5, "You're ready to practice", size=18, bold=True, color=TEAL)
    add_text(slide, 0.8, 2.6, 11.5, 1.0, "Compile. Test. Experiment. Break things safely.", size=32, bold=True, color=WHITE)
    add_text(
        slide,
        0.8,
        4.0,
        11.5,
        1.2,
        "Next steps: OpenZeppelin • Foundry • testnets • audits\nNever deploy these learning contracts to mainnet with real funds.",
        size=16,
        color=CARD,
    )
    add_text(slide, 0.8, 6.5, 11.5, 0.5, "Solidity Practice Curriculum  •  MIT License  •  Hardhat + Solidity 0.8.24", size=14, color=WHITE)

    prs.save(OUT)
    print(f"Wrote {OUT}")
    print(f"Slides: {len(prs.slides)}")


if __name__ == "__main__":
    build()
