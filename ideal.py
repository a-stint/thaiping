import time
import json
import random
import os
import readchar
from rich.console import Console
from rich.text import Text
from pythainlp.corpus.common import thai_words

console = Console()
HIGHSCORE_FILE = "highscore.json"

# ----------------------------
# High score functions
# ----------------------------
def load_stats():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"highscore_wpm": 0.0, "games_played": 0}

def save_stats(stats):
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

# ----------------------------
# Game logic
# ----------------------------
def typing_game(rounds=5):
    words = list(thai_words())  # Thai word bank
    sentence = " ".join(random.sample(words, rounds))  # random sentence
    
    typed = ""
    start_time = None

    console.print("✨ Thai Typing Practice ✨", style="bold cyan")
    console.print("Ghost text in [dim grey]gray[/dim grey].")
    console.print("Correct letters [green]green[/green], mistakes [red]red[/red].")
    console.print("Press ESC to quit.\n")

    while True:
        # Build ghost + typed overlay
        display = Text()
        for i, ch in enumerate(sentence):
            if i < len(typed):
                if typed[i] == ch:
                    display.append(ch, style="green")
                else:
                    display.append(typed[i], style="red")
            else:
                display.append(ch, style="dim")

        console.clear()
        console.print(display)

        # Win condition
        if typed == sentence:
            elapsed = time.time() - start_time if start_time else 0
            wpm = (len(sentence.split()) / elapsed) * 60
            console.print(f"\n🎉 Finished! Time: {elapsed:.2f}s | Speed: {wpm:.2f} WPM", style="bold cyan")

            # Update high score
            stats = load_stats()
            stats["games_played"] += 1
            if wpm > stats["highscore_wpm"]:
                console.print(f"🏆 New High Score! Previous: {stats['highscore_wpm']:.2f}, Now: {wpm:.2f}", style="bold green")
                stats["highscore_wpm"] = wpm
            else:
                console.print(f"💡 High Score to beat: {stats['highscore_wpm']:.2f} WPM", style="yellow")
            save_stats(stats)
            break

        # Read a single key
        key = readchar.readkey()

        # Escape to quit
        if key == readchar.key.ESC:
            console.print("\n👋 Exiting...", style="bold red")
            break

        # Start timer on first key
        if not start_time:
            start_time = time.time()

        # Handle backspace
        if key in (readchar.key.BACKSPACE, readchar.key.DELETE):
            typed = typed[:-1]
        else:
            if len(typed) < len(sentence):
                typed += key

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    typing_game(rounds=5)


#error: not detecting special characters like tone marks
#error: indicating wrong even though correct character clicked