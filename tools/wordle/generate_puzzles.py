#!/usr/bin/env python3
"""Generate 7 Albanian crossword puzzles for the Wordle 7x7 game."""

import json
import random
import os
import copy

GRID_SIZE = 7
WORD_FILE = os.path.join(os.path.dirname(__file__), 'albanian_words.txt')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'puzzles.json')

def load_words():
    with open(WORD_FILE, 'r', encoding='utf-8') as f:
        words = [w.strip().upper() for w in f if w.strip()]
    by_len = {}
    for w in words:
        n = len(w)
        if 3 <= n <= 7:
            by_len.setdefault(n, []).append(w)
    return by_len

def empty_grid():
    return [['X'] * GRID_SIZE for _ in range(GRID_SIZE)]

def can_place(grid, word, row, col, direction):
    """Check if word can be placed at (row,col) in given direction."""
    length = len(word)
    if direction == 'horizontal':
        if col + length > GRID_SIZE:
            return False
        # Check cell before word (must be X or edge)
        if col > 0 and grid[row][col - 1] != 'X':
            return False
        # Check cell after word (must be X or edge)
        if col + length < GRID_SIZE and grid[row][col + length] != 'X':
            return False
        has_crossing = False
        for i, ch in enumerate(word):
            c = col + i
            existing = grid[row][c]
            if existing == ch:
                has_crossing = True
            elif existing != 'X':
                return False  # conflict
            else:
                # Placing a new letter - check vertical neighbors don't form unwanted words
                # Above and below must be X unless they're part of a crossing word
                above = grid[row - 1][c] if row > 0 else 'X'
                below = grid[row + 1][c] if row < GRID_SIZE - 1 else 'X'
                if above != 'X' and existing == 'X':
                    return False
                if below != 'X' and existing == 'X':
                    return False
        return has_crossing or all(grid[row][col + i] == 'X' for i in range(length))
    else:  # vertical
        if row + length > GRID_SIZE:
            return False
        if row > 0 and grid[row - 1][col] != 'X':
            return False
        if row + length < GRID_SIZE and grid[row + length][col] != 'X':
            return False
        has_crossing = False
        for i, ch in enumerate(word):
            r = row + i
            existing = grid[r][col]
            if existing == ch:
                has_crossing = True
            elif existing != 'X':
                return False
            else:
                left = grid[r][col - 1] if col > 0 else 'X'
                right = grid[r][col + 1] if col < GRID_SIZE - 1 else 'X'
                if left != 'X' and existing == 'X':
                    return False
                if right != 'X' and existing == 'X':
                    return False
        return has_crossing or all(grid[row + i][col] == 'X' for i in range(length))

def place_word(grid, word, row, col, direction):
    """Place word on grid (mutates grid)."""
    for i, ch in enumerate(word):
        if direction == 'horizontal':
            grid[row][col + i] = ch
        else:
            grid[row + i][col] = ch

def find_placements(grid, word, placed_words, require_crossing=True):
    """Find all valid placements for a word on the grid."""
    placements = []
    for direction in ['horizontal', 'vertical']:
        if direction == 'horizontal':
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE - len(word) + 1):
                    if can_place(grid, word, r, c, direction):
                        # Check if it crosses at least one existing word
                        crosses = False
                        for i in range(len(word)):
                            if grid[r][c + i] != 'X':
                                crosses = True
                                break
                        if require_crossing and not crosses:
                            continue
                        if not require_crossing or crosses:
                            placements.append((r, c, direction))
        else:
            for r in range(GRID_SIZE - len(word) + 1):
                for c in range(GRID_SIZE):
                    if can_place(grid, word, r, c, direction):
                        crosses = False
                        for i in range(len(word)):
                            if grid[r + i][c] != 'X':
                                crosses = True
                                break
                        if require_crossing and not crosses:
                            continue
                        if not require_crossing or crosses:
                            placements.append((r, c, direction))
    return placements

def validate_grid(grid, placed):
    """Check that every letter cell belongs to at least one word."""
    covered = set()
    for entry in placed:
        w, r, c, d = entry['word'], entry['row'], entry['col'], entry['direction']
        for i in range(len(w)):
            if d == 'horizontal':
                covered.add((r, c + i))
            else:
                covered.add((r + i, c))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != 'X' and (r, c) not in covered:
                return False
    return True

def generate_puzzle(word_pool, min_words=6, max_attempts=200):
    """Generate one crossword puzzle from the word pool."""
    for attempt in range(max_attempts):
        grid = empty_grid()
        placed = []
        pool = list(word_pool)
        random.shuffle(pool)

        # Place first word horizontally near center
        first_word = None
        for w in pool:
            if len(w) >= 4 and len(w) <= GRID_SIZE:
                first_word = w
                break
        if not first_word:
            continue

        start_col = max(0, (GRID_SIZE - len(first_word)) // 2)
        start_row = GRID_SIZE // 2
        place_word(grid, first_word, start_row, start_col, 'horizontal')
        placed.append({
            'word': first_word,
            'row': start_row,
            'col': start_col,
            'direction': 'horizontal'
        })
        pool.remove(first_word)

        # Try to place more words
        failures = 0
        tried = set()
        while len(placed) < 14 and failures < len(pool) and len(pool) > 0:
            word = pool[failures % len(pool)]
            if word in tried:
                failures += 1
                continue
            tried.add(word)

            placements = find_placements(grid, word, placed, require_crossing=True)
            if placements:
                r, c, d = random.choice(placements)
                place_word(grid, word, r, c, d)
                placed.append({'word': word, 'row': r, 'col': c, 'direction': d})
                pool.remove(word)
                failures = 0
                tried = set()
            else:
                failures += 1

        if len(placed) >= min_words and validate_grid(grid, placed):
            return grid, placed

    return None, None

def scramble_grid(grid):
    """Shuffle all letter cells randomly (X stays fixed)."""
    letters = []
    positions = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != 'X':
                letters.append(grid[r][c])
                positions.append((r, c))

    random.shuffle(letters)
    scrambled = [row[:] for row in grid]
    for (r, c), letter in zip(positions, letters):
        scrambled[r][c] = letter
    return scrambled

def print_grid(grid, label=""):
    if label:
        print(f"\n{label}:")
    for row in grid:
        print(' '.join(row))

def main():
    random.seed(42)
    by_len = load_words()
    print(f"Loaded words: {sum(len(v) for v in by_len.values())}")

    # Day configs: (lengths to use, min_words)
    day_configs = [
        ([3, 4], 6),        # Monday: easy
        ([3, 4, 5], 6),     # Tuesday
        ([4, 5], 7),        # Wednesday
        ([4, 5, 6], 7),     # Thursday
        ([5, 6], 7),        # Friday
        ([5, 6, 7], 7),     # Saturday
        ([6, 7], 7),        # Sunday
    ]

    puzzles = []
    for day_idx, (lengths, min_w) in enumerate(day_configs):
        print(f"\n--- Generating Day {day_idx} (lengths={lengths}, min={min_w}) ---")

        pool = []
        for l in lengths:
            pool.extend(by_len.get(l, []))

        # Try multiple seeds
        grid, placed = None, None
        for seed_offset in range(100):
            random.seed(42 + day_idx * 1000 + seed_offset)
            random.shuffle(pool)
            grid, placed = generate_puzzle(pool, min_words=min_w)
            if grid:
                break

        if not grid:
            print(f"  FAILED to generate puzzle for day {day_idx}!")
            continue

        solution = [row[:] for row in grid]
        scrambled = scramble_grid(grid)

        print_grid(solution, f"Day {day_idx} Solution")
        print(f"  Words ({len(placed)}):")
        for p in placed:
            print(f"    {p['word']} at ({p['row']},{p['col']}) {p['direction']}")

        puzzles.append({
            'dayIndex': day_idx,
            'solution': solution,
            'scrambled': scrambled,
            'words': [{'word': p['word'], 'row': p['row'], 'col': p['col'], 'direction': p['direction']} for p in placed]
        })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(puzzles)} puzzles to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
