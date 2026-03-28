# 🎉 Soc Ops – Social Bingo for In-Person Mixers

> **Break the ice and make connections!** A fun, interactive bingo game designed to bring people together at mixers, conferences, and team events.

---

## 🎮 What is Soc Ops?

Soc Ops is a **social bingo game** that turns icebreakers into an engaging experience. Players get a bingo card with fun prompts and race to find people who match each description. Get 5 in a row — horizontally, vertically, or diagonally — and shout **BINGO!**

✨ **Perfect for:**
- Team events & company mixers
- Conference networking sessions
- Classroom icebreakers
- Off-site team building
- Any gathering where you want to spark conversations!

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip or uv

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd my-soc-ops-python

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python -m app.main
```

Open your browser to **http://localhost:8000** and start playing! 🎯

---

## ✨ Features

- 🎲 **Randomized Bingo Cards** – Fresh questions every game
- ⚡ **Fast & Responsive** – Built with FastAPI & HTMX for instant play
- 🎨 **Beautiful UI** – Clean, modern design for seamless gameplay
- 🔄 **Multi-Session Support** – Cookie-based sessions for multiple players
- 🏆 **Win Detection** – Real-time bingo validation (5 in a row!)
- 🔧 **Hackable** – Built for extension with AI agents and custom logic

---

## 📚 Learning Lab Guide

This project is also a **hands-on learning experience** for AI-powered development with GitHub Copilot:

| Part | Title | Focus |
|------|-------|-------|
| [**00**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=00-overview) | Overview & Checklist | Prerequisites & project setup |
| [**01**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=01-setup) | Setup & Context Engineering | Environment & agent customization |
| [**02**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=02-design) | Design-First Frontend | Building the game interface |
| [**03**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=03-quiz-master) | Custom Quiz Master | Adding AI-powered question generation |
| [**04**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=04-multi-agent) | Multi-Agent Development | Advanced agent orchestration |

📖 **Full guides available in [`workshop/`](workshop/) folder for offline reading.**

---

## 🛠️ Development

### Tech Stack
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Frontend:** Jinja2 templates, HTMX, TailwindCSS
- **Testing:** pytest, httpx
- **Linting:** ruff (ANN, F, E, W, UP)

### Run Tests
```bash
pytest
```

### Run Linter
```bash
ruff check app tests --fix
```

### File Structure
```
my-soc-ops-python/
├── app/
│   ├── main.py           # FastAPI app & routes
│   ├── game_logic.py     # Game rules & bingo logic
│   ├── game_service.py   # Session management
│   ├── models.py         # Pydantic models
│   ├── data.py           # Question data
│   ├── static/           # CSS, JS, assets
│   └── templates/        # Jinja2 HTML templates
├── tests/                # pytest test suite
├── workshop/             # Lab guides & exercises
└── docs/                 # Additional documentation
```

---

## 🤝 Contributing

Found a bug or have an idea? Contributions are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🆘 Support & Questions

- 📖 Check the lab guides in [`workshop/`](workshop/)
- 💬 Open an [issue](../../issues) for questions or bugs
- 📚 See [SUPPORT.md](SUPPORT.md) for additional resources

---

**Happy mingling! 🎊**
