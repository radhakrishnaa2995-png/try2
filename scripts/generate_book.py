import argparse
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from puzzle_utils import make_word_search, get_theme_data

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.65 * inch

def draw_title(c, title, subtitle=""):
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 2.2 * inch, title)
    c.setFont("Helvetica", 15)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 2.7 * inch, subtitle)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_WIDTH / 2, 1.25 * inch, "Created with KDP Puzzle Factory")
    c.showPage()

def draw_rules(c):
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, "How to Use This Book")
    c.setFont("Helvetica", 12)
    lines = [
        "Welcome to your fun puzzle adventure!",
        "",
        "Inside this book you will find:",
        "1. Trivia questions",
        "2. Word search puzzles",
        "3. Crossword-style clue pages",
        "4. Answer key pages",
        "",
        "Try your best before checking the answers.",
        "You can use a pencil so you can erase and play again.",
    ]
    y = PAGE_HEIGHT - 1.25 * inch
    for line in lines:
        c.drawString(MARGIN, y, line)
        y -= 0.28 * inch
    c.showPage()

def draw_trivia_page(c, trivia, page_num):
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, f"Trivia Challenge {page_num}")
    c.setFont("Helvetica", 12)

    y = PAGE_HEIGHT - 1.2 * inch
    for i, (q, a) in enumerate(trivia, start=1):
        c.drawString(MARGIN, y, f"{i}. {q}")
        y -= 0.45 * inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
        y -= 0.35 * inch
        if y < 1.2 * inch:
            break
    c.showPage()

def draw_word_search(c, words, number):
    grid, placed = make_word_search(words, size=12)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, f"Word Search {number}")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, PAGE_HEIGHT - 1.05 * inch, "Find these words:")
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, PAGE_HEIGHT - 1.25 * inch, ", ".join(placed))

    start_x = 1.3 * inch
    start_y = PAGE_HEIGHT - 2.05 * inch
    cell = 0.34 * inch

    c.setFont("Courier-Bold", 15)
    for r, row in enumerate(grid):
        for col, ch in enumerate(row):
            x = start_x + col * cell
            y = start_y - r * cell
            c.drawCentredString(x, y, ch)

    c.showPage()
    return grid, placed

def draw_clue_page(c, clues, number):
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, f"Crossword-Style Clues {number}")
    c.setFont("Helvetica", 12)

    y = PAGE_HEIGHT - 1.2 * inch
    for i, (clue, answer) in enumerate(clues, start=1):
        c.drawString(MARGIN, y, f"{i}. {clue}")
        y -= 0.42 * inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
        y -= 0.35 * inch
    c.showPage()

def draw_answers(c, trivia, clues, word_lists):
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, "Answer Key")
    y = PAGE_HEIGHT - 1.15 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN, y, "Trivia Answers")
    y -= 0.32 * inch
    c.setFont("Helvetica", 10)

    for i, (_, answer) in enumerate(trivia, start=1):
        c.drawString(MARGIN, y, f"{i}. {answer}")
        y -= 0.22 * inch

    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN, y, "Clue Answers")
    y -= 0.32 * inch
    c.setFont("Helvetica", 10)

    for i, (_, answer) in enumerate(clues, start=1):
        c.drawString(MARGIN, y, f"{i}. {answer}")
        y -= 0.22 * inch

    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN, y, "Word Search Words")
    y -= 0.32 * inch
    c.setFont("Helvetica", 10)

    for idx, placed in enumerate(word_lists, start=1):
        c.drawString(MARGIN, y, f"Word Search {idx}: {', '.join(placed)}")
        y -= 0.24 * inch
        if y < 0.8 * inch:
            c.showPage()
            y = PAGE_HEIGHT - MARGIN

    c.showPage()

def build_book(title, theme):
    data = get_theme_data(theme)
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    filename = out_dir / f"{theme.replace(' ', '_')}_kdp_puzzle_book.pdf"

    c = canvas.Canvas(str(filename), pagesize=letter)

    draw_title(c, title, f"{theme.title()} Trivia, Word Search & Clues")
    draw_rules(c)

    all_trivia = data["trivia"] * 3
    all_clues = data["clues"] * 3
    word_lists = []

    for i in range(1, 6):
        draw_trivia_page(c, all_trivia[(i-1)*5:i*5], i)
        grid, placed = draw_word_search(c, data["words"], i)
        word_lists.append(placed)
        draw_clue_page(c, all_clues[(i-1)*5:i*5], i)

    draw_answers(c, all_trivia[:15], all_clues[:15], word_lists)

    c.save()
    print(f"Generated: {filename}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="Dinosaur Trivia & Puzzle Fun")
    parser.add_argument("--theme", default="dinosaurs")
    args = parser.parse_args()
    build_book(args.title, args.theme)

if __name__ == "__main__":
    main()
