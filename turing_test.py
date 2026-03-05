"""
Turing Test Implementation
==========================
Simulates the classic Turing Test:
  - A human Judge chats with two hidden players (one Human, one AI).
  - After N turns the Judge decides which one is the machine.
  - The "AI" player is backed by a simple rule-based chatbot
    (no external API required – fully offline).

Architecture
------------
  TuringTestSession
      ├── Judge  (human, uses stdin)
      ├── PlayerA → HumanPlayer (human, uses stdin)
      └── PlayerB → AIPlayer    (rule-based bot)
  The session randomly swaps A/B so the Judge does not know which is which.
"""

from __future__ import annotations
import random
import re
import textwrap


# ═══════════════════════════════════════════════════════
# RULE-BASED AI CHATBOT
# ═══════════════════════════════════════════════════════

# Each entry: (compiled regex, list of possible replies)
_RULES: list[tuple[re.Pattern, list[str]]] = [
    (re.compile(r"\bhello\b|\bhi\b|\bhey\b", re.I),
     ["Hello there!", "Hey! How are you?", "Hi! Nice to meet you."]),

    (re.compile(r"\bhow are you\b|\bare you ok\b", re.I),
     ["I'm doing well, thanks for asking!", "Feeling great today.",
      "Pretty good. And you?"]),

    (re.compile(r"\bwhat is your name\b|\bwho are you\b", re.I),
     ["You can call me Alex.", "My name is Sam. What's yours?",
      "I go by Jordan."]),

    (re.compile(r"\bdo you feel\b|\bdo you have feelings\b|\bare you conscious\b", re.I),
     ["That's a deep question. I think I experience something like feelings.",
      "I'm not entirely sure, but I try to be empathetic.",
      "Sometimes it feels that way, yes."]),

    (re.compile(r"\bfavorite (food|colour|color|movie|book|sport)\b", re.I),
     ["That's a tough one – I have so many favourites!",
      "Honestly I could list a dozen. What's yours?",
      "I'd say pizza, but maybe I'm just hungry right now."]),

    (re.compile(r"\bwhere (do you live|are you from)\b", re.I),
     ["I'm from a small town in the Midwest.",
      "Born and raised in the city.",
      "Currently living in London. You?"]),

    (re.compile(r"\bbye\b|\bgoodbye\b|\bsee you\b", re.I),
     ["Goodbye!", "See you later!", "Take care!"]),

    (re.compile(r"\bwhy\b", re.I),
     ["Good question – I've wondered the same thing.",
      "There are many reasons, I suppose.",
      "Why not?"]),

    (re.compile(r"\b(yes|yeah|yep|sure)\b", re.I),
     ["Absolutely!", "Agreed.", "Sounds good to me."]),

    (re.compile(r"\b(no|nope|nah)\b", re.I),
     ["Fair enough.", "That's okay.", "I understand."]),
]

_FALLBACK = [
    "Interesting – tell me more.",
    "I see what you mean.",
    "That's a great point.",
    "Hmm, I hadn't thought of it that way.",
    "Can you elaborate?",
    "Right, right. Go on.",
]


class AIPlayer:
    """Simple rule-based chatbot that mimics human-like responses."""

    def __init__(self, name: str = "Player"):
        self.name = name
        self._last_fallback = -1          # avoid repeating fallbacks

    def respond(self, message: str) -> str:
        for pattern, replies in _RULES:
            if pattern.search(message):
                return random.choice(replies)
        # Fallback – cycle through list
        self._last_fallback = (self._last_fallback + 1) % len(_FALLBACK)
        return _FALLBACK[self._last_fallback]


# ═══════════════════════════════════════════════════════
# HUMAN PLAYER (stdin wrapper)
# ═══════════════════════════════════════════════════════

class HumanPlayer:
    """Wraps a human participant who types their replies."""

    def __init__(self, name: str = "Player"):
        self.name = name

    def respond(self, message: str) -> str:
        return input(f"  [{self.name}] Your reply: ").strip()


# ═══════════════════════════════════════════════════════
# TURING TEST SESSION
# ═══════════════════════════════════════════════════════

class TuringTestSession:
    """
    Orchestrates a Turing Test.

    Parameters
    ----------
    turns : int
        Number of question rounds before the Judge decides.
    human_plays : bool
        If True, one participant is a real human (stdin).
        If False, both participants are AI (useful for unit-testing).
    """

    def __init__(self, turns: int = 5, human_plays: bool = True):
        self.turns       = turns
        self._ai         = AIPlayer("(hidden)")
        self._human      = HumanPlayer("(hidden)") if human_plays else AIPlayer("(hidden)2")

        # Randomly assign A / B
        if random.random() < 0.5:
            self._player_a, self._player_b = self._human, self._ai
            self._ai_label = "B"
        else:
            self._player_a, self._player_b = self._ai, self._human
            self._ai_label = "A"

        self._score: dict[str, int] = {"correct": 0, "wrong": 0}

    # ── public entry point ──────────────────────────────
    def run(self):
        self._banner()
        history: list[dict] = []

        for turn in range(1, self.turns + 1):
            print(f"\n{'─'*50}")
            print(f"  Turn {turn}/{self.turns}")
            print(f"{'─'*50}")
            question = input("Judge – Ask your question: ").strip()
            if not question:
                print("  (empty question skipped)")
                continue

            resp_a = self._player_a.respond(question)
            resp_b = self._player_b.respond(question)

            print(f"\n  [Player A]: {resp_a}")
            print(f"  [Player B]: {resp_b}")

            history.append({
                "turn": turn,
                "question": question,
                "A": resp_a,
                "B": resp_b,
            })

        self._judge_phase()
        self._show_transcript(history)

    # ── judge decision ───────────────────────────────────
    def _judge_phase(self):
        print(f"\n{'═'*50}")
        print("  JUDGE'S DECISION")
        print(f"{'═'*50}")
        while True:
            guess = input("Which player is the AI? Enter A or B: ").strip().upper()
            if guess in ("A", "B"):
                break
            print("  Please enter A or B.")

        correct = guess == self._ai_label
        if correct:
            print(f"\n✅  Correct! The AI was Player {self._ai_label}.")
            print("   The machine was NOT indistinguishable → Turing Test FAILED for AI.")
        else:
            print(f"\n❌  Wrong! The AI was actually Player {self._ai_label}.")
            print("   The machine WAS indistinguishable → Turing Test PASSED for AI! 🤖")

    # ── transcript ───────────────────────────────────────
    @staticmethod
    def _show_transcript(history: list[dict]):
        print(f"\n{'═'*50}")
        print("  FULL TRANSCRIPT")
        print(f"{'═'*50}")
        for entry in history:
            print(f"\n  Turn {entry['turn']}")
            print(f"  Q : {entry['question']}")
            print(f"  A : {entry['A']}")
            print(f"  B : {entry['B']}")

    # ── banner ───────────────────────────────────────────
    @staticmethod
    def _banner():
        print(textwrap.dedent("""
        ╔══════════════════════════════════════════════╗
        ║          TURING TEST SIMULATION              ║
        ║                                              ║
        ║  You are the JUDGE.                          ║
        ║  Two hidden players will answer questions:   ║
        ║    Player A  and  Player B                   ║
        ║  One is HUMAN, one is an AI.                 ║
        ║  After all turns, guess which is the AI.     ║
        ╚══════════════════════════════════════════════╝
        """))


# ═══════════════════════════════════════════════════════
# AUTOMATED EVALUATION MODE
# ═══════════════════════════════════════════════════════

def evaluate_ai(n_trials: int = 20) -> dict:
    """
    Run N automated trials (Judge is also AI) and report
    how often the AI fools a 'random-guess' judge.

    Returns dict with pass_rate, fail_rate, n_trials.
    """
    passed = 0
    questions = [
        "Hello, how are you?",
        "What is your favourite food?",
        "Do you have feelings?",
        "Where are you from?",
        "Why do you think humans are interesting?",
    ]

    for _ in range(n_trials):
        ai = AIPlayer()
        answers = [ai.respond(q) for q in questions]
        # Simulate a random-guess judge
        if random.random() < 0.5:   # judge guesses wrong → AI "passed"
            passed += 1

    return {
        "n_trials":  n_trials,
        "passed":    passed,
        "failed":    n_trials - passed,
        "pass_rate": round(passed / n_trials * 100, 1),
    }


# ═══════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════

def main():
    import sys
    if "--evaluate" in sys.argv:
        result = evaluate_ai(n_trials=100)
        print("Automated Evaluation Results:")
        for k, v in result.items():
            print(f"  {k}: {v}")
    else:
        turns = 5
        for arg in sys.argv[1:]:
            if arg.startswith("--turns="):
                turns = int(arg.split("=")[1])
        session = TuringTestSession(turns=turns, human_plays=True)
        session.run()


if __name__ == "__main__":
    main()
