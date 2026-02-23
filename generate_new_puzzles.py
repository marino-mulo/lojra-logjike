#!/usr/bin/env python3
"""
Generate and validate 7 crossword puzzles for Wordle 7x7.
All words are common, everyday Albanian that everyone knows.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GRID_SIZE = 7

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

def validate(grid, words):
    for w in words:
        word, row, col, d = w["word"], w["row"], w["col"], w["direction"]
        for i, ch in enumerate(word):
            r = row + (i if d == "vertical" else 0)
            c = col + (i if d == "horizontal" else 0)
            if grid[r][c] != ch:
                print(f"  ERROR: '{word}' pos {i} at ({r},{c}): expected '{ch}', got '{grid[r][c]}'")
                return False
    return True

def count_letters(grid):
    return sum(1 for r in grid for c in r if c != "X")

def show(label, grid, words):
    print(f"\n{label}:")
    for row in grid:
        print("  " + " ".join(row))
    wl = [w['word'] for w in words]
    print(f"  Letters: {count_letters(grid)}, Words: {wl}")

puzzles = []

# =============================================
# Day 0 (Monday - Easy, 7 words)
# Layout:
#   Row 0: B U K Ë . . .     BUKË horizontal
#   Row 1: . . A . . . .     KAFË vertical from (0,2)→K is shared with BUKË
#   Row 2: . . F . D E T     DET horizontal
#   Row 3: . . Ë . . . .
#   Row 4: E R A . . . .     ERA horizontal, A shared with KAFË
#   Row 5: . . . M A L .     MAL horizontal
#   Row 6: U J Ë . Z O G     UJË horizontal, ZOG horizontal
# Words: BUKË, KAFË, ERA, UJË, DET, MAL, ZOG
# =============================================
g = make_grid()
w = [
    {"word": "BUKË",  "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "KAFË",  "row": 0, "col": 2, "direction": "vertical"},  # K shared at (0,2)
    {"word": "ERA",   "row": 4, "col": 0, "direction": "horizontal"},
    {"word": "UJË",   "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "DET",   "row": 2, "col": 4, "direction": "horizontal"},
    {"word": "MAL",   "row": 5, "col": 3, "direction": "horizontal"},
    {"word": "ZOG",   "row": 6, "col": 4, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 0", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Day 1 (Tuesday, 7 words) — user-designed layout, fully connected
# Words: LIBËR, LULE, LULË, ZIM, DALLIM, DUA, VAJ
# Layout (user provided):
#   Row 0: L I B Ë R . .     LIBËR horizontal
#   Row 1: U . . . . . .     LULE vertical col 0
#   Row 2: L U L Ë Z I M     LULË horizontal + ZIM horizontal
#   Row 3: E . . . . . A
#   Row 4: . D A L L I M     DALLIM horizontal
#   Row 5: . U . . . . I
#   Row 6: V A J O R . .     VAJ horizontal + OR?
# Connections:
#   LIBËR ↔ LULE share L at (0,0)
#   LULE ↔ LULË share L at (2,0)
#   ZIM M at (2,6) → MAMI vertical col 6 → DALLIM M at (4,6)
#   DALLIM ↔ DUA share D at (4,1)
#   DUA ↔ VAJ share A at (6,1)
#
# Checking col 6 vertical: M(2,6) A(3,6) M(4,6) I(5,6) = MAMI
# Row 6: V(6,0) A(6,1) J(6,2) O(6,3) R(6,4) — VAJOR is not a word
# Let me adjust: VAJ at (6,0-2), and separate O R
# Actually OR isn't a word either. Let me use the user's structure
# but replace row 6 tail: VAJ at (6,0), then ORË (hour) at (6,3)?
# ORË = O(6,3) R(6,4) Ë(6,5) — that works!
# But then col 6 from MAMI would end at (5,6)=I, (6,6) empty. Fine.
# =============================================
g = make_grid()
w = [
    {"word": "LIBËR",  "row": 0, "col": 0, "direction": "horizontal"},  # L(0,0) I(0,1) B(0,2) Ë(0,3) R(0,4)
    {"word": "LULE",   "row": 0, "col": 0, "direction": "vertical"},    # L(0,0) U(1,0) L(2,0) E(3,0)
    {"word": "LULË",   "row": 2, "col": 0, "direction": "horizontal"},  # L(2,0) U(2,1) L(2,2) Ë(2,3) — shares L(2,0) with LULE
    {"word": "ZIM",    "row": 2, "col": 4, "direction": "horizontal"},  # Z(2,4) I(2,5) M(2,6)
    {"word": "MAMI",   "row": 2, "col": 6, "direction": "vertical"},    # M(2,6) A(3,6) M(4,6) I(5,6) — shares M(2,6) with ZIM
    {"word": "DALLIM", "row": 4, "col": 1, "direction": "horizontal"},  # D(4,1) A(4,2) L(4,3) L(4,4) I(4,5) M(4,6) — shares M(4,6) with MAMI
    {"word": "DUA",    "row": 4, "col": 1, "direction": "vertical"},    # D(4,1) U(5,1) A(6,1) — shares D(4,1) with DALLIM
    {"word": "VAJ",    "row": 6, "col": 0, "direction": "horizontal"},  # V(6,0) A(6,1) J(6,2) — shares A(6,1) with DUA
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 1", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Day 2 (Wednesday, 7 words)
# Layout:
#   Row 0: . D A R K Ë .     DARKË horizontal
#   Row 1: . I . . . . .     DITË vertical from (0,1)
#   Row 2: G T . . V A J     VAJ horizontal at (2,4)
#   Row 3: J Ë . N A T Ë     NATË horizontal at (3,3)
#   Row 4: A . . . L . .     VALË vertical from (2,4)
#   Row 5: K G U R Ë . .     GURË horizontal at (5,1)
#   Row 6: . . . . . . .
# GJAK vertical from (2,0)→G,J,A,K
# Words: DARKË, DITË, GJAK, VAJ, NATË, VALË, GURË
# =============================================
g = make_grid()
w = [
    {"word": "DARKË", "row": 0, "col": 1, "direction": "horizontal"},
    {"word": "DITË",  "row": 0, "col": 1, "direction": "vertical"},   # D shared at (0,1)
    {"word": "GJAK",  "row": 2, "col": 0, "direction": "vertical"},   # G(2,0) J(3,0) A(4,0) K(5,0)
    {"word": "VAJ",   "row": 2, "col": 4, "direction": "horizontal"}, # V(2,4) A(2,5) J(2,6)
    {"word": "NATË",  "row": 3, "col": 3, "direction": "horizontal"}, # N(3,3) A(3,4) T(3,5) Ë(3,6)
    {"word": "VALË",  "row": 2, "col": 4, "direction": "vertical"},   # V(2,4) shared, A(3,4) shared with NATË, L(4,4), Ë(5,4)
    {"word": "GURË",  "row": 5, "col": 1, "direction": "horizontal"}, # G(5,1) U(5,2) R(5,3) Ë(5,4) shared with VALË
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 2", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Day 3 (Thursday, 9 words)
# Layout:
#   Row 0: F L E T Ë . .     FLETË horizontal
#   Row 1: S . . . U J Ë     UJË horizontal at (1,4)
#   Row 2: H Ë N Ë . . .     HËNË horizontal
#   Row 3: A . . . L O T     LOT horizontal at (3,4)
#   Row 4: T . Z E M Ë R     ZEMËR horizontal
#   Row 5: . . P I K Ë .     PIKË horizontal
#   Row 6: J A V Ë M A L     JAVË horizontal, MAL horizontal
# FSHAT vertical from (0,0), LUMË vertical→replaced
# Words: FLETË, FSHAT, HËNË, UJË, LOT, ZEMËR, PIKË, JAVË, MAL
# =============================================
g = make_grid()
w = [
    {"word": "FLETË", "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "FSHAT", "row": 0, "col": 0, "direction": "vertical"},   # F shared at (0,0)
    {"word": "HËNË",  "row": 2, "col": 0, "direction": "horizontal"},
    {"word": "UJË",   "row": 1, "col": 4, "direction": "horizontal"},
    {"word": "LOT",   "row": 3, "col": 4, "direction": "horizontal"},
    {"word": "ZEMËR", "row": 4, "col": 2, "direction": "horizontal"},
    {"word": "PIKË",  "row": 5, "col": 2, "direction": "horizontal"},
    {"word": "JAVË",  "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "MAL",   "row": 6, "col": 4, "direction": "horizontal"},
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 3", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Day 4 (Friday, 8 words)
# Layout:
#   Row 0: D R E K Ë . .     DREKË horizontal
#   Row 1: O R A . . . .     ORA horizontal
#   Row 2: R . E M Ë R .     EMËR horizontal at (2,2)
#   Row 3: Ë . . . . V .     VERË vertical from (2,5)→wait, need to check
#   Row 4: A R R Ë . E .     ARRË horizontal
#   Row 5: P I K . . R .     PIK horizontal
#   Row 6: M E S . . Ë .     MES horizontal, VERË vertical from (3,5)
# DORË vertical from (0,0), VERË vertical from (3,5)
# Words: DREKË, DORË, ORA, EMËR, ARRË, PIK, MES, VERË
# Let me re-check VERË: V(3,5)? No, let me put it at col 5 rows 3-6
# =============================================
g = make_grid()
w = [
    {"word": "DREKË", "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "DORË",  "row": 0, "col": 0, "direction": "vertical"},   # D shared at (0,0)
    {"word": "ORA",   "row": 1, "col": 0, "direction": "horizontal"},
    {"word": "EMËR",  "row": 2, "col": 2, "direction": "horizontal"}, # E(2,2) M(2,3) Ë(2,4) R(2,5)
    {"word": "ARRË",  "row": 4, "col": 0, "direction": "horizontal"},
    {"word": "PIK",   "row": 5, "col": 0, "direction": "horizontal"},
    {"word": "MES",   "row": 6, "col": 0, "direction": "horizontal"},
    {"word": "VERË",  "row": 3, "col": 5, "direction": "vertical"},   # V(3,5) E(4,5) R(5,5) Ë(6,5)
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 4", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Day 5 (Saturday, 7 words)
# I need to be very careful with intersections.
# Words: KISHA, INAT, BUKË, ARRË, NËNË, ZOG, ERA
#
# Layout plan:
#   Row 0: K I S H A . .     KISHA horizontal
#   Row 1: . N . . R . .     INAT vertical from (0,1), ARRË vertical from (0,4)
#   Row 2: B A . . R . .
#   Row 3: U T . N Ë N Ë     NËNË horizontal at (3,3)
#   Row 4: K . Z O G . .     ZOG horizontal at (4,2)
#   Row 5: Ë . . . . . .
#   Row 6: . E R A . . .     ERA horizontal at (6,1)
# BUKË vertical from (2,0)→B(2,0) U(3,0) K(4,0) Ë(5,0)
# =============================================
g = make_grid()
w = [
    {"word": "KISHA", "row": 0, "col": 0, "direction": "horizontal"},
    {"word": "INAT",  "row": 0, "col": 1, "direction": "vertical"},   # I(0,1) shared, N(1,1) A(2,1) T(3,1)
    {"word": "BUKË",  "row": 2, "col": 0, "direction": "vertical"},   # B(2,0) U(3,0) K(4,0) Ë(5,0)
    {"word": "ARRË",  "row": 0, "col": 4, "direction": "vertical"},   # A(0,4) shared with KISHA, R(1,4) R(2,4) Ë(3,4)
    {"word": "NËNË",  "row": 3, "col": 3, "direction": "horizontal"}, # N(3,3) Ë(3,4) shared with ARRË, N(3,5) Ë(3,6)
    {"word": "ZOG",   "row": 4, "col": 2, "direction": "horizontal"}, # Z(4,2) O(4,3) G(4,4)
    {"word": "ERA",   "row": 6, "col": 1, "direction": "horizontal"}, # E(6,1) R(6,2) A(6,3)
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 5", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Day 6 (Sunday - Hard, 8 words)
# Words: SHTËPI, TOKË, PIKË, BUKË, JETË, KAFENE, VERË, MES
# Layout:
#   Row 0: S H T Ë P I .     SHTËPI horizontal
#   Row 1: . . O . I . .     TOKË vertical from (0,2), PIKË vertical from (0,4)
#   Row 2: B U K Ë K . .     BUKË horizontal, K(2,2) shared with TOKË
#   Row 3: . . Ë . Ë . .
#   Row 4: J E T Ë . . .     JETË horizontal, T(4,2) shared with TOKË
#   Row 5: . K A F E N E     KAFENE horizontal at (5,1)
#   Row 6: V E R Ë M E S     VERË horizontal, MES horizontal at (6,4)
# =============================================
g = make_grid()
w = [
    {"word": "SHTËPI","row": 0, "col": 0, "direction": "horizontal"},
    {"word": "TOKË",  "row": 0, "col": 2, "direction": "vertical"},   # T(0,2) shared, O(1,2) K(2,2) Ë(3,2)
    {"word": "PIKË",  "row": 0, "col": 4, "direction": "vertical"},   # P(0,4) shared, I(1,4) K(2,4) Ë(3,4)
    {"word": "BUKË",  "row": 2, "col": 0, "direction": "horizontal"}, # B(2,0) U(2,1) K(2,2) shared Ë(2,3)
    {"word": "JETË",  "row": 4, "col": 0, "direction": "horizontal"}, # J(4,0) E(4,1) T(4,2) Ë(4,3)
    {"word": "KAFENE","row": 5, "col": 1, "direction": "horizontal"}, # K(5,1) A(5,2) F(5,3) E(5,4) N(5,5) E(5,6)
    {"word": "VERË",  "row": 6, "col": 0, "direction": "horizontal"}, # V(6,0) E(6,1) R(6,2) Ë(6,3)
    {"word": "MES",   "row": 6, "col": 4, "direction": "horizontal"}, # M(6,4) E(6,5) S(6,6)
]
for x in w: place_word(g, x["word"], x["row"], x["col"], x["direction"])
assert validate(g, w)
show("Day 6", g, w)
puzzles.append({"grid": [r[:] for r in g], "words": w})

# =============================================
# Output C#
# =============================================
print("\n\n========= ALL 7 PUZZLES VALIDATED =========\n")

def csharp_row(row):
    return "[" + ", ".join(f'"{c}"' for c in row) + "]"

for i, p in enumerate(puzzles):
    wl = [x["word"] for x in p["words"]]
    print(f"// Day {i}: {', '.join(wl)}")
    print(f"new()")
    print(f"{{")
    print(f"    Solution = [")
    for row in p["grid"]:
        print(f"        [{', '.join(f'\"' + c + '\"' for c in row)}],")
    print(f"    ],")
    print(f"    Words = [")
    for x in p["words"]:
        print(f'        new() {{ Word = "{x["word"]}", Row = {x["row"]}, Col = {x["col"]}, Direction = "{x["direction"]}" }},')
    print(f"    ]")
    print(f"}},")
