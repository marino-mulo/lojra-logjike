#!/usr/bin/env python3
"""
Crossword puzzle validator for Wordle 7x7.

Rules:
1. CONNECTIVITY: All words must be connected — no floating/isolated groups.
2. NO GHOST WORDS: Every horizontal or vertical run of 2+ consecutive
   letters on the grid must be an actual word in the puzzle's word list.
3. COMMON ALBANIAN WORDS: All words must be in the approved dictionary.
4. GRID INTEGRITY: Words fit in bounds, no letter conflicts.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GRID_SIZE = 7

# =============================================
# Albanian common word dictionary
# Only everyday words that everyone knows
# =============================================
ALBANIAN_WORDS = {
    # 3-letter
    "MAL", "DET", "UJE", "UJË", "ZOG", "ERA", "VAJ", "ORA", "QEN", "ZIM",
    "DUA", "PIK", "MES", "LOT", "NJE", "NJË", "DHE", "PAK", "ZOT", "SOT",
    "TRE", "MUA", "SAJ", "TIJ", "AJO", "KJO",

    # 4-letter
    "BUKË", "KAFË", "LULË", "MISH", "DITË", "NATË", "TOKË", "VALË",
    "GURË", "PIKË", "ARRË", "NËNË", "DORË", "EMËR", "VERË", "JETË",
    "JAVË", "INAT", "HËNË", "MAMI", "LULE", "GJAK", "LUMË", "PUNË",
    "DERË", "BIRË", "FARË", "BARË", "MIRË", "ORËL",

    # 5-letter
    "LIBËR", "DREKË", "DARKË", "KISHA", "FLETË", "FSHAT", "ZEMËR",

    # 6-letter
    "DALLIM", "KAFENE", "SHTËPI",
}

def make_grid():
    return [["X"] * GRID_SIZE for _ in range(GRID_SIZE)]

def place_word(grid, word, row, col, direction):
    for i, ch in enumerate(word):
        r = row + (i if direction == "vertical" else 0)
        c = col + (i if direction == "horizontal" else 0)
        if r >= GRID_SIZE or c >= GRID_SIZE:
            raise ValueError(f"'{word}' goes out of bounds at ({r},{c})")
        if grid[r][c] != "X" and grid[r][c] != ch:
            raise ValueError(f"Conflict at ({r},{c}): grid='{grid[r][c]}', word '{word}' needs '{ch}'")
        grid[r][c] = ch

def get_word_cells(word_entry):
    cells = []
    w = word_entry
    for i in range(len(w["word"])):
        r = w["row"] + (i if w["direction"] == "vertical" else 0)
        c = w["col"] + (i if w["direction"] == "horizontal" else 0)
        cells.append((r, c))
    return cells

# =============================================
# RULE 1: Connectivity check
# =============================================
def check_connectivity(words):
    if len(words) <= 1:
        return True, []
    word_cells = [set(get_word_cells(w)) for w in words]
    adj = {i: set() for i in range(len(words))}
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if word_cells[i] & word_cells[j]:
                adj[i].add(j)
                adj[j].add(i)
    visited = {0}
    queue = [0]
    while queue:
        node = queue.pop(0)
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    if len(visited) == len(words):
        return True, []
    disconnected = [words[i]["word"] for i in range(len(words)) if i not in visited]
    connected = [words[i]["word"] for i in visited]
    return False, [f"Disconnected: {connected} vs {disconnected}"]

# =============================================
# RULE 2: No ghost words
# Every horizontal/vertical run of 2+ letters must be a known word
# =============================================
def find_all_runs(grid):
    runs = []
    # Horizontal
    for r in range(GRID_SIZE):
        c = 0
        while c < GRID_SIZE:
            if grid[r][c] != "X":
                start_c = c
                letters = ""
                while c < GRID_SIZE and grid[r][c] != "X":
                    letters += grid[r][c]
                    c += 1
                if len(letters) >= 2:
                    runs.append({"text": letters, "row": r, "col": start_c, "dir": "H", "len": len(letters)})
            else:
                c += 1
    # Vertical
    for c in range(GRID_SIZE):
        r = 0
        while r < GRID_SIZE:
            if grid[r][c] != "X":
                start_r = r
                letters = ""
                while r < GRID_SIZE and grid[r][c] != "X":
                    letters += grid[r][c]
                    r += 1
                if len(letters) >= 2:
                    runs.append({"text": letters, "row": start_r, "col": c, "dir": "V", "len": len(letters)})
            else:
                r += 1
    return runs

def check_no_ghost_words(grid, words):
    word_set = set(w["word"] for w in words)
    runs = find_all_runs(grid)
    errors = []
    for run in runs:
        if run["text"] not in word_set:
            errors.append(
                f"'{run['text']}' at ({run['row']},{run['col']}) {run['dir']} "
                f"— NOT a puzzle word! (looks like nonsense or accidental combo)"
            )
    return len(errors) == 0, errors

# =============================================
# RULE 3: All words in Albanian dictionary
# =============================================
def check_dictionary(words):
    errors = []
    for w in words:
        if w["word"] not in ALBANIAN_WORDS:
            errors.append(f"'{w['word']}' NOT in common Albanian dictionary")
    return len(errors) == 0, errors

# =============================================
# RULE 4: Grid integrity
# =============================================
def check_grid_integrity(grid, words):
    errors = []
    expected = make_grid()
    for w in words:
        for i, ch in enumerate(w["word"]):
            r = w["row"] + (i if w["direction"] == "vertical" else 0)
            c = w["col"] + (i if w["direction"] == "horizontal" else 0)
            if r >= GRID_SIZE or c >= GRID_SIZE:
                errors.append(f"'{w['word']}' out of bounds at ({r},{c})")
                continue
            if expected[r][c] != "X" and expected[r][c] != ch:
                errors.append(f"Conflict at ({r},{c}): '{expected[r][c]}' vs '{ch}' from '{w['word']}'")
            expected[r][c] = ch
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != expected[r][c]:
                errors.append(f"Mismatch at ({r},{c}): grid='{grid[r][c]}', expected='{expected[r][c]}'")
    return len(errors) == 0, errors

# =============================================
# Master validator
# =============================================
def validate_puzzle(label, grid, words):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    for row in grid:
        print("  " + " ".join(row))
    print(f"  Words: {[w['word'] for w in words]}")

    all_passed = True
    checks = [
        ("CONNECTIVITY", check_connectivity(words)),
        ("NO GHOST WORDS", check_no_ghost_words(grid, words)),
        ("DICTIONARY", check_dictionary(words)),
        ("GRID INTEGRITY", check_grid_integrity(grid, words)),
    ]
    for name, (ok, errs) in checks:
        if ok:
            print(f"  \u2713 {name}: OK")
        else:
            print(f"  \u2717 {name} FAILED:")
            for e in errs:
                print(f"    -> {e}")
            all_passed = False

    status = "PASSED" if all_passed else "FAILED"
    print(f"  >> {label}: {status}")
    return all_passed

# =============================================
# Build and validate all 7 puzzles
# =============================================
puzzles_data = []

# Day 0
g = make_grid()
w = [
    {"word": "BUKË",  "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "KAFË",  "row": 0, "col": 2, "direction": "vertical"},
    {"word": "ERA",   "row": 4, "col": 0, "direction": "horizontal"},
    {"word": "UJË",   "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "DET",   "row": 2, "col": 4, "direction": "horizontal"},
    {"word": "MAL",   "row": 5, "col": 3, "direction": "horizontal"},
    {"word": "ZOG",   "row": 6, "col": 4, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 0 (Monday)", g, w))

# Day 1
g = make_grid()
w = [
    {"word": "LIBËR",  "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "LULE",   "row": 0, "col": 0, "direction": "vertical"},
    {"word": "LULË",   "row": 2, "col": 0, "direction": "horizontal"},
    {"word": "ZIM",    "row": 2, "col": 4, "direction": "horizontal"},
    {"word": "MAMI",   "row": 2, "col": 6, "direction": "vertical"},
    {"word": "DALLIM", "row": 4, "col": 1, "direction": "horizontal"},
    {"word": "DUA",    "row": 4, "col": 1, "direction": "vertical"},
    {"word": "VAJ",    "row": 6, "col": 0, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 1 (Tuesday)", g, w))

# Day 2
g = make_grid()
w = [
    {"word": "DARKË", "row": 0, "col": 1, "direction": "horizontal"},
    {"word": "DITË",  "row": 0, "col": 1, "direction": "vertical"},
    {"word": "GJAK",  "row": 2, "col": 0, "direction": "vertical"},
    {"word": "VAJ",   "row": 2, "col": 4, "direction": "horizontal"},
    {"word": "NATË",  "row": 3, "col": 3, "direction": "horizontal"},
    {"word": "VALË",  "row": 2, "col": 4, "direction": "vertical"},
    {"word": "GURË",  "row": 5, "col": 1, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 2 (Wednesday)", g, w))

# Day 3
g = make_grid()
w = [
    {"word": "FLETË", "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "FSHAT", "row": 0, "col": 0, "direction": "vertical"},
    {"word": "HËNË",  "row": 2, "col": 0, "direction": "horizontal"},
    {"word": "UJË",   "row": 1, "col": 4, "direction": "horizontal"},
    {"word": "LOT",   "row": 3, "col": 4, "direction": "horizontal"},
    {"word": "ZEMËR", "row": 4, "col": 2, "direction": "horizontal"},
    {"word": "PIKË",  "row": 5, "col": 2, "direction": "horizontal"},
    {"word": "JAVË",  "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "MAL",   "row": 6, "col": 4, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 3 (Thursday)", g, w))

# Day 4
g = make_grid()
w = [
    {"word": "DREKË", "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "DORË",  "row": 0, "col": 0, "direction": "vertical"},
    {"word": "ORA",   "row": 1, "col": 0, "direction": "horizontal"},
    {"word": "EMËR",  "row": 2, "col": 2, "direction": "horizontal"},
    {"word": "ARRË",  "row": 4, "col": 0, "direction": "horizontal"},
    {"word": "PIK",   "row": 5, "col": 0, "direction": "horizontal"},
    {"word": "MES",   "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "VERË",  "row": 3, "col": 5, "direction": "vertical"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 4 (Friday)", g, w))

# Day 5
g = make_grid()
w = [
    {"word": "KISHA", "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "INAT",  "row": 0, "col": 1, "direction": "vertical"},
    {"word": "BUKË",  "row": 2, "col": 0, "direction": "vertical"},
    {"word": "ARRË",  "row": 0, "col": 4, "direction": "vertical"},
    {"word": "NËNË",  "row": 3, "col": 3, "direction": "horizontal"},
    {"word": "ZOG",   "row": 4, "col": 2, "direction": "horizontal"},
    {"word": "ERA",   "row": 6, "col": 1, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 5 (Saturday)", g, w))

# Day 6
g = make_grid()
w = [
    {"word": "SHTËPI","row": 0, "col": 0, "direction": "horizontal"},
    {"word": "TOKË",  "row": 0, "col": 2, "direction": "vertical"},
    {"word": "PIKË",  "row": 0, "col": 4, "direction": "vertical"},
    {"word": "BUKË",  "row": 2, "col": 0, "direction": "horizontal"},
    {"word": "JETË",  "row": 4, "col": 0, "direction": "horizontal"},
    {"word": "KAFENE","row": 5, "col": 1, "direction": "horizontal"},
    {"word": "VERË",  "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "MES",   "row": 6, "col": 4, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
puzzles_data.append(("Day 6 (Sunday)", g, w))

# Run all
total_pass = 0
total_fail = 0
for label, grid, words in puzzles_data:
    if validate_puzzle(label, grid, words):
        total_pass += 1
    else:
        total_fail += 1

print(f"\n{'='*55}")
print(f"  SUMMARY: {total_pass} passed, {total_fail} failed out of {len(puzzles_data)}")
print(f"{'='*55}")
if total_fail > 0:
    sys.exit(1)
else:
    print(f"  All puzzles valid!")
    sys.exit(0)
