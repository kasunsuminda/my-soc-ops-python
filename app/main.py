import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.game_service import GameSession, get_session, generate_hunt_items
from app.models import GameState, GameMode
from app.data import PERSONALITY_BINGO, LIFESTYLE_BINGO, TRAVEL_BINGO, TECH_LIFE_BINGO

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Soc Ops - Social Bingo")
app.add_middleware(SessionMiddleware, secret_key="soc-ops-secret-key")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _get_game_session(request: Request) -> GameSession:
    """Get or create a game session using cookie-based sessions."""
    if "session_id" not in request.session:
        request.session["session_id"] = uuid.uuid4().hex
    return get_session(request.session["session_id"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Response:
    session = _get_game_session(request)
    return templates.TemplateResponse(
        request,
        "home.html",
        {"session": session, "GameState": GameState},
    )


@app.post("/start", response_class=HTMLResponse)
async def start_game(request: Request) -> Response:
    session = _get_game_session(request)
    session.start_game(mode=GameMode.BINGO)
    return templates.TemplateResponse(
        request, "components/game_screen.html", {"session": session}
    )


@app.post("/hunt/start", response_class=HTMLResponse)
async def start_hunt(request: Request) -> Response:
    session = _get_game_session(request)
    session.start_game(mode=GameMode.SCAVENGER_HUNT)
    session.hunt_items = generate_hunt_items(PERSONALITY_BINGO)
    return templates.TemplateResponse(
        request, "components/hunt_screen.html", {"session": session}
    )


@app.post("/toggle/{square_id}", response_class=HTMLResponse)
async def toggle_square(request: Request, square_id: int) -> Response:
    session = _get_game_session(request)
    session.handle_square_click(square_id)
    return templates.TemplateResponse(
        request, "components/game_screen.html", {"session": session}
    )


@app.post("/hunt/toggle/{item_id}", response_class=HTMLResponse)
async def toggle_hunt_item(request: Request, item_id: int) -> Response:
    session = _get_game_session(request)
    session.handle_hunt_item_click(item_id)
    if session.hunt_complete:
        return templates.TemplateResponse(
            request,
            "components/hunt_complete_modal.html",
            {"session": session},
        )
    return templates.TemplateResponse(
        request, "components/hunt_screen.html", {"session": session}
    )


@app.post("/reset", response_class=HTMLResponse)
async def reset_game(request: Request) -> Response:
    session = _get_game_session(request)
    session.reset_game()
    return templates.TemplateResponse(
        request,
        "components/start_screen.html",
        {"session": session, "GameState": GameState},
    )


@app.post("/card/start", response_class=HTMLResponse)
async def start_card_mode(request: Request) -> Response:
    session = _get_game_session(request)
    session.start_game(mode=GameMode.CARD_DECK_SHUFFLE)
    session.get_next_card(PERSONALITY_BINGO)
    return templates.TemplateResponse(
        request, "components/card_screen.html", {"session": session}
    )


@app.post("/card/next", response_class=HTMLResponse)
async def next_card(request: Request) -> Response:
    session = _get_game_session(request)
    session.get_next_card(PERSONALITY_BINGO)
    return templates.TemplateResponse(
        request, "components/card_screen.html", {"session": session}
    )


@app.post("/dismiss-modal", response_class=HTMLResponse)
async def dismiss_modal(request: Request) -> Response:
    session = _get_game_session(request)
    session.dismiss_modal()
    return templates.TemplateResponse(
        request, "components/game_screen.html", {"session": session}
    )


def run() -> None:
    """Entry point for the application."""
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
