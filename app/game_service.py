from dataclasses import dataclass, field
import random

from app.game_logic import (
    check_bingo,
    generate_board,
    get_winning_square_ids,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData, CardData, GameMode, GameState, HuntItem


def generate_hunt_items(questions: list[str]) -> list[HuntItem]:
    """Generate hunt items from a list of questions."""
    return [HuntItem(id=i, text=text, is_found=False) for i, text in enumerate(questions)]


def toggle_hunt_item(items: list[HuntItem], item_id: int) -> list[HuntItem]:
    """Toggle a hunt item's found state. Returns a new list."""
    return [
        item.model_copy(update={"is_found": not item.is_found})
        if item.id == item_id
        else item
        for item in items
    ]


def get_random_card(questions: list[str], exclude_ids: set[int]) -> CardData:
    """Get a random card from the questions list, excluding previously shown cards."""
    available = [i for i in range(len(questions)) if i not in exclude_ids]
    if not available:
        available = list(range(len(questions)))  # Reset if all shown
    card_id = random.choice(available)
    return CardData(id=card_id, text=questions[card_id])


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_state: GameState = GameState.START
    game_mode: GameMode = GameMode.BINGO
    board: list[BingoSquareData] = field(default_factory=list)
    hunt_items: list[HuntItem] = field(default_factory=list)
    current_card: CardData | None = None
    cards_seen: set[int] = field(default_factory=set)
    winning_line: BingoLine | None = None
    show_bingo_modal: bool = False

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    @property
    def hunt_progress(self) -> int:
        """Return percentage of hunt items found."""
        if not self.hunt_items:
            return 0
        found = sum(1 for item in self.hunt_items if item.is_found)
        return int((found / len(self.hunt_items)) * 100)

    @property
    def hunt_complete(self) -> bool:
        """Check if all hunt items are found."""
        return len(self.hunt_items) > 0 and all(item.is_found for item in self.hunt_items)

    def start_game(self, mode: GameMode = GameMode.BINGO) -> None:
        """Start a new game with the specified mode."""
        self.game_mode = mode
        if mode == GameMode.BINGO:
            self.board = generate_board()
            self.hunt_items = []
            self.current_card = None
        elif mode == GameMode.SCAVENGER_HUNT:
            self.hunt_items = generate_hunt_items([])  # Will be populated from data
            self.board = []
            self.current_card = None
        else:  # CARD_DECK_SHUFFLE
            self.board = []
            self.hunt_items = []
            self.current_card = None
            self.cards_seen = set()
        self.winning_line = None
        self.game_state = GameState.PLAYING
        self.show_bingo_modal = False

    def handle_square_click(self, square_id: int) -> None:
        """Handle a bingo square click (bingo mode only)."""
        if self.game_mode != GameMode.BINGO or self.game_state != GameState.PLAYING:
            return
        self.board = toggle_square(self.board, square_id)

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self.game_state = GameState.BINGO
                self.show_bingo_modal = True

    def handle_hunt_item_click(self, item_id: int) -> None:
        """Handle a hunt item checkbox click (hunt mode only)."""
        if self.game_mode != GameMode.SCAVENGER_HUNT or self.game_state != GameState.PLAYING:
            return
        self.hunt_items = toggle_hunt_item(self.hunt_items, item_id)

        if self.hunt_complete:
            self.game_state = GameState.HUNT_COMPLETE
            self.show_bingo_modal = True

    def get_next_card(self, questions: list[str]) -> None:
        """Get the next random card (card deck shuffle mode only)."""
        if self.game_mode != GameMode.CARD_DECK_SHUFFLE or self.game_state != GameState.PLAYING:
            return
        card = get_random_card(questions, self.cards_seen)
        self.current_card = card
        self.cards_seen.add(card.id)

    def reset_game(self) -> None:
        self.game_state = GameState.START
        self.game_mode = GameMode.BINGO
        self.board = []
        self.hunt_items = []
        self.current_card = None
        self.cards_seen = set()
        self.winning_line = None
        self.show_bingo_modal = False

    def dismiss_modal(self) -> None:
        self.show_bingo_modal = False
        self.game_state = GameState.PLAYING


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
