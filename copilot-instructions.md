# Soc Ops - Copilot Instructions & Design Guide

This document guides GitHub Copilot and developers through the architecture, design system, and coding conventions for Soc Ops.

---

## 🎮 Project Overview

**Soc Ops** is a social bingo game for in-person mixers. Players find people who match questions on their bingo card and mark squares to get 5 in a row. Built with FastAPI, HTMX, and a playful skeuomorphic design system.

### Tech Stack
- **Backend:** FastAPI + Uvicorn + Pydantic
- **Frontend:** Jinja2 templates + HTMX (no heavy frameworks)
- **Testing:** pytest + httpx
- **Styling:** Custom CSS (no Tailwind in production)
- **Linting:** ruff (rules: E, F, I, N, W, UP, ANN)

---

## 🎨 Design System Guide

### Overview
Soc Ops features a **skeuomorphic design** combining three visual themes:
1. **Paper Card Cutouts** – Tan/beige textured bingo board
2. **Colorful Stickers** – Vibrant marked square indicators
3. **Chalkboard Aesthetic** – Dark slate header with chalk-colored text

### Color Palette

| Element | Color | Usage |
|---------|-------|-------|
| **Chalkboard** | `#2c2c2c` / `#1a1a1a` | Background, dark surfaces |
| **Chalk Text** | `#ffd54f` / `#ffeb3b` | Headers, titles |
| **Paper/Cards** | `#f5e6d3` / `#e8d6c4` | Bingo board, card backgrounds |
| **Sticker Yellow** | `#ffd54f` / `#fde68a` | Marked squares |
| **Button Red** | `#ff6b6b` / `#ff5252` | Action buttons, modals |
| **Winning Gold** | `#fcd34d` | Winning line highlight |

### CSS Architecture

All styles are in **`app/static/css/app.css`**. Key utility classes:

#### Layout & Grid
```css
.flex, .flex-col, .grid, .grid-cols-5
.items-center, .justify-center, .max-w-md
.aspect-square, .gap-1, .p-4, .mb-8
```

#### Skeuomorphic Components
```css
.paper-card          /* Tan textured card with embossed effect */
.sticker-mark        /* Checkmark sticker with rotation & pop animation */
.sticker-circle      /* Radial gradient for marked squares */
.chalkboard-header   /* Dark header with orange border */
.chalk-text          /* Yellow text with chalk shadow effect */
.chalk-info          /* Info box styled as chalkboard surface */
.bingo-grid          /* Paper card container with shadow depth */
.bingo-square        /* Individual squares with paper texture */
.bingo-square.marked /* Yellow sticker appearance */
.bingo-square.winning /* Animated pulse effect */
.sticker-button      /* 3D pressed button effect */
```

#### Animations
```css
@keyframes sticker-pop       /* Pop in with rotation (0.3s) */
@keyframes winning-pulse     /* Winning square glow pulse (0.6s) */
@keyframes modal-bounce      /* Modal entrance bounce (0.5s) */
@keyframes confetti-fall     /* Text fall animation (0.8s) */
```

### Design Tokens

#### Typography
- **Font:** Fredoka (primary), Comic Sans / Marker Felt (fallback)
- **Title:** 2.5-3.5rem, chalk-colored, text-shadow
- **Body:** 0.875-1rem, light text on dark
- **Labels:** 0.75rem, semi-bold

#### Shadows & Depth
- **Paper cards:** `inset 0 1px 0 rgba(255,255,255,0.3), inset 0 -2px 4px rgba(0,0,0,0.1)`
- **Sticker buttons:** `0 6px 0 #a01d1d, 0 8px 12px rgba(0,0,0,0.3)`
- **Winning squares:** Animated glow ring expanding outward

#### Border Radius
- **Cards:** `2px` (subtle, realistic)
- **Buttons:** `8px` (playful)
- **Modals:** `12px` (rounded)

### Component Patterns

#### Bingo Square States
```html
<!-- Unmarked -->
<button class="bingo-square">Find a match</button>

<!-- Marked (with sticker) -->
<button class="bingo-square marked">
  <span>Find a match</span>
  <span class="sticker-mark"></span>
</button>

<!-- Winning (highlighted in sequence) -->
<button class="bingo-square winning">
  <span>Find a match</span>
  <span class="sticker-mark"></span>
</button>
```

#### Button Styles
```html
<!-- Primary action button -->
<button class="sticker-button">🎮 Start Game</button>

<!-- Back navigation -->
<button class="back-button">← Back</button>
```

#### Info/Instruction Blocks
```html
<div class="chalk-info">
  <h2>How to play</h2>
  <ul>
    <li>✏️ Find people who match</li>
    <li>✨ Tap when you find a match</li>
    <li>🎉 Get 5 in a row!</li>
  </ul>
</div>
```

### When to Use Each Aesthetic

| Context | Aesthetic | Example |
|---------|-----------|---------|
| Background | Chalkboard | Dark slate gradient |
| Header/Title | Chalk Text | Yellow `#ffd54f` with shadow |
| Game Board | Paper Card | Tan textured container |
| Unmarked Squares | Card Paper | Tan with subtle texture |
| Marked Squares | Sticker | Yellow radial gradient |
| Winning Line | Sticker + Glow | Gold with animated pulse |
| Buttons | 3D Sticker | Vibrant color with depth |
| Instructions | Chalk Info | Dark with left border |
| Modal/Win Screen | Sticker Style | Bold red, 3D effect |

---

## 📐 Template Structure

### File Organization
```
app/templates/
├── base.html                 # Main HTML shell
├── home.html                # Route dispatcher
└── components/
    ├── start_screen.html     # Intro screen
    ├── game_screen.html      # Main game view
    ├── bingo_board.html      # 5x5 grid
    └── bingo_modal.html      # Win celebration
```

### Template Patterns

**Do:**
- Use semantic HTML (`<button>`, `<header>`)
- Include ARIA labels for accessibility
- Keep animations smooth (150-800ms)
- Add emojis for visual interest

**Don't:**
- Use inline styles (except for dynamic values)
- Add heavy JavaScript (HTMX handles interactions)
- Break the paper/chalkboard aesthetic

---

## 🐍 Python Code Conventions

### Type Hints
All functions must have return type annotations (enforced by `ANN` linting rule):

```python
def toggle_square(board: list[BingoSquareData], square_id: int) -> list[BingoSquareData]:
    """Toggle a square's marked state. Returns a new board list."""
    return [...]

async def home(request: Request) -> Response:
    """Return home page."""
    ...
```

### Imports
Organized by: stdlib → third-party → local (enforced by `I` rule):

```python
import functools
import random

from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI, Request

from app.data import FREE_SPACE
from app.models import BingoSquareData
```

### Naming
- `snake_case` for functions, variables
- `CamelCase` for classes
- `CONSTANT_CASE` for constants
- Avoid single-letter vars except in loops

### Docstrings
```python
def generate_board() -> list[BingoSquareData]:
    """Generate a new 5x5 bingo board with random questions.
    
    The center square is always the FREE_SPACE.
    """
```

---

## ✅ Code Quality Standards

### Linting
Run before commits:
```bash
ruff check app tests --fix
```

**Enabled Rules:**
- `E` – pycodestyle errors (whitespace, indentation)
- `F` – unused imports/variables (unused-import, undefined-name)
- `I` – isort (correct import ordering)
- `N` – pep8-naming (function/variable names)
- `W` – pycodestyle warnings (line length)
- `UP` – pyupgrade (modern Python syntax)
- `ANN` – flake8-annotations (all functions must have return type)

### Testing
```bash
pytest
pytest -v  # Verbose output
```

**Coverage:** Aim for 80%+ of game logic
**Test Style:** Class-based, descriptive names

```python
class TestCheckBingo:
    def test_row_bingo_detects_winning_line(self) -> None:
        board = self._make_board({0, 1, 2, 3, 4})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "row"
```

---

## 🎯 AI Agent Guidance

When Copilot is asked to modify Soc Ops:

1. **Preserve the design aesthetic** – Maintain paper/sticker/chalkboard themes
2. **Add type hints** – All functions need `-> ReturnType`
3. **Import correctly** – stdlib → external → local
4. **Test coverage** – Add/update tests for logic changes
5. **Lint before submit** – `ruff check --fix` must pass
6. **Use HTMX for interactions** – No heavy JavaScript libraries
7. **Responsive design** – Mobile-first, works on small screens

### Example: Adding a New Feature

```python
# ✅ Good: Type hints, docstring, follows conventions
def award_bonus_points(game_session: GameSession, points: int) -> None:
    """Award bonus points to the current game session."""
    game_session.score += points

# ❌ Bad: No type hints, unclear logic
def add_points(session, pts):
    session.score = session.score + pts
```

---

## 📝 Documentation Standards

- **README.md** – User-facing, feature-focused
- **CONTRIBUTING.md** – For community contributors
- **Code comments** – Explain *why*, not *what*
- **Docstrings** – One-liner + optional details
- **This file** – For Copilot & architectural decisions

---

## 🔄 Git & Workflow

### Branch naming
- `feature/add-xyz` – New feature
- `fix/resolve-xyz` – Bug fix
- `docs/update-guide` – Documentation

### Commit messages
```
feat: add bonus points multiplier
fix: correct bingo line detection edge case
docs: update design guide for new sticker styles
test: add coverage for game_service
```

### Before push
```bash
ruff check app tests --fix
pytest
git add -A
git commit -m "descriptive message"
git push origin feature/branch-name
```

---

## 🎨 Design Inspiration & References

- **Paper cutouts:** Tactile, nostalgic craft aesthetic
- **Colorful stickers:** 90s digital sticker packs
- **Chalkboard:** Retro classroom/cafe vibes
- **Animations:** Playful, snappy (150-600ms)
- **Font:** Fredoka + Comic Sans = approachable, fun

---

## ❓ FAQ

**Q: Can I use Tailwind utilities?**
A: No. We use custom CSS for the skeuomorphic design. Tailwind would override our aesthetic.

**Q: How do I add a new page/route?**
A: Create endpoint in `main.py`, template in `templates/components/`, add CSS class. Ensure type hints and ARIA labels.

**Q: Should I add animations?**
A: Yes, but keep them quick (150-600ms) and purposeful. Match the playful aesthetic.

**Q: How do I test UI changes?**
A: Run `python -m app.main`, visit http://localhost:8000. Test on mobile too!

---

*Last updated: March 28, 2026*
