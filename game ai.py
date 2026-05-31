import random
import time
import os

# --- Config ---
SYMBOLS = ['@', '#', '$', '%', '&', '*', '!', '?', '+', '=']
LEVELS = [
    {"grid": 3, "symbols": 3, "flash_time": 2.5},
    {"grid": 4, "symbols": 5, "flash_time": 2.0},
    {"grid": 4, "symbols": 7, "flash_time": 1.8},
    {"grid": 5, "symbols": 9, "flash_time": 1.5},
    {"grid": 5, "symbols": 12, "flash_time": 1.2},
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_grid(grid, hide=False):
    size = len(grid)
    # Column headers
    print("   " + "  ".join(str(i+1) for i in range(size)))
    print("  +" + "---" * size + "+")
    for r in range(size):
        row_display = []
        for c in range(size):
            if hide:
                row_display.append(".")
            else:
                row_display.append(grid[r][c] if grid[r][c] else ".")
        print(f"{r+1} | " + "  ".join(row_display) + " |")
    print("  +" + "---" * size + "+")

def make_grid(size):
    return [["" for _ in range(size)] for _ in range(size)]

def place_symbols(size, count):
    grid = make_grid(size)
    positions = random.sample([(r, c) for r in range(size) for c in range(size)], count)
    sym_list = random.choices(SYMBOLS, k=count)
    for (r, c), sym in zip(positions, sym_list):
        grid[r][c] = sym
    return grid

def get_player_grid(size, count, answer_grid):
    player_grid = make_grid(size)
    placed = 0

    while placed < count:
        print_grid(player_grid)
        print(f"\nSymbols to place: {placed}/{count}")
        print("Enter: row col symbol  (e.g. 2 3 @)  |  'done' to finish early\n")

        try:
            inp = input(">> ").strip()
            if inp.lower() == 'done':
                break
            parts = inp.split()
            if len(parts) != 3:
                print("❌ Format: row col symbol (e.g. 2 3 @)")
                time.sleep(1)
                clear()
                continue
            r, c, sym = int(parts[0])-1, int(parts[1])-1, parts[2]
            if not (0 <= r < size and 0 <= c < size):
                print("❌ Row/col out of range!")
                time.sleep(1)
                clear()
                continue
            if sym not in SYMBOLS:
                print(f"❌ Invalid symbol! Use: {' '.join(SYMBOLS)}")
                time.sleep(1)
                clear()
                continue
            if player_grid[r][c]:
                print("❌ Cell already filled!")
                time.sleep(1)
                clear()
                continue
            player_grid[r][c] = sym
            placed += 1
            clear()
        except (ValueError, IndexError):
            print("❌ Invalid input!")
            time.sleep(1)
            clear()

    return player_grid

def score_grids(answer, player, size):
    correct = 0
    total = sum(1 for r in range(size) for c in range(size) if answer[r][c])
    for r in range(size):
        for c in range(size):
            if answer[r][c] and answer[r][c] == player[r][c]:
                correct += 1
    return correct, total

def show_comparison(answer, player, size):
    print("\n  ANSWER           YOUR ANSWER")
    col_header = "   " + "  ".join(str(i+1) for i in range(size))
    print(f"{col_header}        {col_header}")
    sep = "  +" + "---" * size + "+"
    print(f"{sep}   {sep}")
    for r in range(size):
        left = []
        right = []
        for c in range(size):
            a = answer[r][c] if answer[r][c] else "."
            p = player[r][c] if player[r][c] else "."
            left.append(a)
            # Mark correct with ✓ wrong with ✗
            if answer[r][c] and answer[r][c] == p:
                right.append(p)
            elif player[r][c] and player[r][c] != answer[r][c]:
                right.append("X")
            else:
                right.append(p)
        print(f"{r+1} | {'  '.join(left)} |   {r+1} | {'  '.join(right)} |")
    print(f"{sep}   {sep}")

def play_level(level_num):
    cfg = LEVELS[level_num]
    size = cfg["grid"]
    count = cfg["symbols"]
    flash = cfg["flash_time"]

    clear()
    print("=" * 40)
    print(f"   🧠 LEVEL {level_num + 1}  |  Grid: {size}x{size}  |  Symbols: {count}")
    print("=" * 40)
    print(f"\nMEMORIZE the grid! You have {flash} seconds...\n")
    time.sleep(1.5)

    answer_grid = place_symbols(size, count)
    print_grid(answer_grid)
    time.sleep(flash)
    clear()

    print("=" * 40)
    print(f"   🧠 LEVEL {level_num + 1}  —  NOW RECREATE IT!")
    print("=" * 40)
    print(f"\nAvailable symbols: {' '.join(SYMBOLS)}\n")

    player_grid = get_player_grid(size, count, answer_grid)
    correct, total = score_grids(answer_grid, player_grid, size)

    clear()
    print("=" * 40)
    print("         RESULTS")
    print("=" * 40)
    show_comparison(answer_grid, player_grid, size)
    print(f"\n✅ Correct: {correct}/{total}  ({int(correct/total*100)}%)\n")

    return correct, total

def main():
    clear()
    print("=" * 40)
    print("       🧠 MEMORY MATRIX")
    print("=" * 40)
    print("\nA grid of symbols will flash on screen.")
    print("Memorize it — then recreate it from memory!\n")
    print("5 levels. Each level gets harder.")
    input("\nPress ENTER to start...")

    total_correct = 0
    total_possible = 0

    for i in range(len(LEVELS)):
        correct, total = play_level(i)
        total_correct += correct
        total_possible += total

        pct = int(correct / total * 100)
        if i < len(LEVELS) - 1:
            if pct >= 60:
                print("🎉 Nice! Moving to next level...")
            else:
                print("💪 Keep going — next level!")
            time.sleep(1.5)
            input("Press ENTER for next level...")
        else:
            print("🏁 You've completed all levels!")

    clear()
    print("=" * 40)
    print("       🧠 GAME OVER — FINAL SCORE")
    print("=" * 40)
    final_pct = int(total_correct / total_possible * 100)
    print(f"\n  Total: {total_correct}/{total_possible}  ({final_pct}%)\n")
    if final_pct >= 80:
        print("  🥇 AMAZING memory! You're a matrix master!")
    elif final_pct >= 60:
        print("  🥈 Good job! Your memory is sharp.")
    elif final_pct >= 40:
        print("  🥉 Not bad — keep practicing!")
    else:
        print("  🧩 Better luck next time. Keep training!")
    print("=" * 40)

if __name__ == "__main__":
    main()