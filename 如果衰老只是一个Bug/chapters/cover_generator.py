#!/usr/bin/env python3
"""
Cover Generator for 《如果衰老只是一个Bug》
Following the "Temporal Algorithms" design philosophy
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import HexColor
import math
import os

# Register fonts
FONT_DIR = "/Users/szou/Python/Playground/StoryWriter/.claude/skills/canvas-design/canvas-fonts"
# Use built-in CID font for Chinese
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('Jura-Light', f"{FONT_DIR}/Jura-Light.ttf"))
pdfmetrics.registerFont(TTFont('Jura-Medium', f"{FONT_DIR}/Jura-Medium.ttf"))
pdfmetrics.registerFont(TTFont('GeistMono', f"{FONT_DIR}/GeistMono-Regular.ttf"))

# Chinese font name
CHINESE_FONT = 'STSong-Light'

# Colors from the design philosophy
COLORS = {
    'background': HexColor('#F8F6F1'),  # Warm ivory
    'accent_blue': HexColor('#B8C9D4'),  # Pale ethereal blue
    'accent_teal': HexColor('#7BA3A8'),  # Muted teal
    'text_dark': HexColor('#2A3439'),    # Deep grey-blue
    'text_light': HexColor('#6B7B82'),   # Soft grey
    'line_subtle': HexColor('#D4DDE2'),  # Very subtle line
    'accent_amber': HexColor('#C9B896'), # Soft amber
}

def draw_dna_helix_pattern(c, x_center, y_start, y_end, amplitude=15, frequency=0.02, phase=0):
    """Draw a subtle DNA-like helix pattern"""
    c.setStrokeColor(COLORS['line_subtle'])
    c.setLineWidth(0.3)

    points1 = []
    points2 = []

    for y in range(int(y_start), int(y_end), 2):
        x1 = x_center + amplitude * math.sin(frequency * y + phase)
        x2 = x_center + amplitude * math.sin(frequency * y + phase + math.pi)
        points1.append((x1, y))
        points2.append((x2, y))

    # Draw the two strands
    path = c.beginPath()
    path.moveTo(points1[0][0], points1[0][1])
    for x, y in points1[1:]:
        path.lineTo(x, y)
    c.drawPath(path, stroke=1, fill=0)

    path = c.beginPath()
    path.moveTo(points2[0][0], points2[0][1])
    for x, y in points2[1:]:
        path.lineTo(x, y)
    c.drawPath(path, stroke=1, fill=0)

    # Draw connecting lines (base pairs)
    for i in range(0, len(points1), 20):
        c.setStrokeColor(COLORS['accent_blue'])
        c.setLineWidth(0.2)
        c.line(points1[i][0], points1[i][1], points2[i][0], points2[i][1])

def draw_circuit_nodes(c, x, y, size, node_count=5):
    """Draw circuit-like nodes suggesting data pathways"""
    c.setStrokeColor(COLORS['accent_teal'])
    c.setFillColor(COLORS['background'])
    c.setLineWidth(0.5)

    for i in range(node_count):
        angle = (2 * math.pi / node_count) * i
        nx = x + size * math.cos(angle)
        ny = y + size * math.sin(angle)
        c.circle(nx, ny, 2, stroke=1, fill=1)
        c.line(x, y, nx, ny)

def draw_data_grid(c, x, y, width, height, cols=20, rows=10):
    """Draw a subtle data grid pattern"""
    c.setStrokeColor(COLORS['line_subtle'])
    c.setLineWidth(0.15)

    cell_w = width / cols
    cell_h = height / rows

    for i in range(cols + 1):
        c.line(x + i * cell_w, y, x + i * cell_w, y + height)
    for j in range(rows + 1):
        c.line(x, y + j * cell_h, x + width, y + j * cell_h)

def create_book_cover(output_path, story_name="如果衰老只是一个Bug"):
    """Create the main book cover (Cover-0)"""
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    # Background
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Subtle data grid in the background
    draw_data_grid(c, 20*mm, 20*mm, width - 40*mm, height - 40*mm, cols=30, rows=40)

    # DNA helix patterns on sides
    draw_dna_helix_pattern(c, 25*mm, 50*mm, height - 50*mm, amplitude=8, frequency=0.015)
    draw_dna_helix_pattern(c, width - 25*mm, 50*mm, height - 50*mm, amplitude=8, frequency=0.015, phase=math.pi/2)

    # Central geometric element - concentric circles suggesting cellular/digital patterns
    center_x = width / 2
    center_y = height / 2 + 20*mm

    c.setStrokeColor(COLORS['accent_blue'])
    for i in range(8):
        c.setLineWidth(0.3 + i * 0.1)
        radius = 20*mm + i * 8*mm
        c.circle(center_x, center_y, radius, stroke=1, fill=0)

    # Circuit nodes at cardinal points
    for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
        nx = center_x + 70*mm * math.cos(angle)
        ny = center_y + 70*mm * math.sin(angle)
        draw_circuit_nodes(c, nx, ny, 10, 4)

    # Central accent circle
    c.setFillColor(COLORS['accent_teal'])
    c.circle(center_x, center_y, 5*mm, stroke=0, fill=1)
    c.setFillColor(COLORS['background'])
    c.circle(center_x, center_y, 3*mm, stroke=0, fill=1)

    # Title - Main Chinese title
    c.setFillColor(COLORS['text_dark'])
    c.setFont(CHINESE_FONT, 32)
    title_y = 85*mm
    c.drawCentredString(center_x, title_y, story_name)

    # Subtitle line
    c.setFont('Jura-Light', 11)
    c.setFillColor(COLORS['text_light'])
    c.drawCentredString(center_x, title_y - 12*mm, "IF AGING IS JUST A BUG")

    # Small annotation at top
    c.setFont('GeistMono', 7)
    c.setFillColor(COLORS['accent_teal'])
    c.drawCentredString(center_x, height - 35*mm, "SCIENCE FICTION · 2025")

    # Technical annotation at bottom
    c.setFont('GeistMono', 6)
    c.setFillColor(COLORS['text_light'])
    c.drawCentredString(center_x, 30*mm, "AGENTIC AI × LONGEVITY × TIME SOURCE CODE")

    # Decorative lines
    c.setStrokeColor(COLORS['accent_amber'])
    c.setLineWidth(0.5)
    c.line(center_x - 40*mm, title_y - 18*mm, center_x + 40*mm, title_y - 18*mm)
    c.line(center_x - 40*mm, title_y + 12*mm, center_x + 40*mm, title_y + 12*mm)

    c.save()
    print(f"Created: {output_path}")

def create_chapter_cover(output_path, chapter_num, chapter_title, story_name="如果衰老只是一个Bug"):
    """Create a chapter cover"""
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    # Background
    c.setFillColor(COLORS['background'])
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Subtle grid pattern - less dense for chapter covers
    draw_data_grid(c, 30*mm, 30*mm, width - 60*mm, height - 60*mm, cols=20, rows=25)

    # Single DNA helix on left side
    draw_dna_helix_pattern(c, 30*mm, 60*mm, height - 60*mm, amplitude=6, frequency=0.012, phase=chapter_num * 0.5)

    # Chapter number as large geometric element
    center_x = width / 2
    center_y = height / 2 + 30*mm

    # Concentric arcs for chapter indicator
    c.setStrokeColor(COLORS['accent_blue'])
    c.setLineWidth(0.5)
    for i in range(chapter_num + 2):
        c.arc(center_x - 50*mm - i*5*mm, center_y - 50*mm - i*5*mm,
              center_x + 50*mm + i*5*mm, center_y + 50*mm + i*5*mm,
              45, 90)

    # Chapter number
    c.setFillColor(COLORS['accent_teal'])
    c.setFont('Jura-Medium', 72)
    c.drawCentredString(center_x, center_y - 10*mm, f"0{chapter_num}")

    # Story name at top
    c.setFillColor(COLORS['text_light'])
    c.setFont(CHINESE_FONT, 14)
    c.drawCentredString(center_x, height - 45*mm, story_name)

    # Chapter indicator
    c.setFont('GeistMono', 8)
    c.setFillColor(COLORS['accent_teal'])
    c.drawCentredString(center_x, height - 55*mm, f"CHAPTER {chapter_num}")

    # Chapter title
    c.setFillColor(COLORS['text_dark'])
    c.setFont(CHINESE_FONT, 24)
    c.drawCentredString(center_x, 80*mm, f"第{chapter_num}章")

    c.setFont(CHINESE_FONT, 20)
    c.drawCentredString(center_x, 60*mm, chapter_title)

    # Decorative line
    c.setStrokeColor(COLORS['accent_amber'])
    c.setLineWidth(0.5)
    c.line(center_x - 30*mm, 50*mm, center_x + 30*mm, 50*mm)

    c.save()
    print(f"Created: {output_path}")

if __name__ == "__main__":
    base_path = "/Users/szou/Python/Playground/StoryWriter/如果衰老只是一个Bug/chapters"

    # Create book cover
    create_book_cover(f"{base_path}/Cover-0.pdf")

    # Create chapter covers
    chapters = [
        (1, "信息退化"),
        (2, "方法论之争"),
        (3, "第一个试验品"),
        (4, "咨询模式"),
        (5, "时间源代码"),
    ]

    for num, title in chapters:
        create_chapter_cover(f"{base_path}/Cover-{num}.pdf", num, title)

    print("\nAll covers created successfully!")
