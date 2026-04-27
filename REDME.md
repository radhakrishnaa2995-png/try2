# KDP Puzzle Factory

A free GitHub Actions repo that automatically generates a kids puzzle book interior PDF for Amazon KDP.

## What it creates

- Trivia pages
- Word search puzzles
- Crossword-style clue pages
- Answer key pages
- Print-ready 8.5 x 11 inch PDF interior
- Downloadable artifact from GitHub Actions

## How to use on GitHub

1. Create a new GitHub repository.
2. Upload all files from this ZIP.
3. Go to the **Actions** tab.
4. Click **Build KDP Puzzle Book**.
5. Click **Run workflow**.
6. Download the generated PDF from the workflow **Artifacts** section.

## Change book theme

Open `scripts/generate_book.py` and change:

```python
BOOK_TITLE = "Dinosaur Trivia & Puzzle Fun"
THEME = "dinosaurs"
