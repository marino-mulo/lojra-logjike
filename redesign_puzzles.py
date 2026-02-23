#!/usr/bin/env python3
"""
Redesign all 7 puzzles from scratch following strict crossword rules:
1. All words connected via shared intersection cells
2. Every letter run (H and V) must be a puzzle word — no ghost words
3. Words separated by X gaps unless intentionally crossing
4. All common Albanian words
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

def find_all_runs(grid):
    runs = []
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
                    runs.append({"text": letters, "row": r, "col": start_c, "dir": "H"})
            else:
                c += 1
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
                    runs.append({"text": letters, "row": start_r, "col": c, "dir": "V"})
            else:
                r += 1
    return runs

def check_connectivity(words):
    if len(words) <= 1:
        return True
    word_cells = [set() for _ in words]
    for i, w in enumerate(words):
        for j in range(len(w["word"])):
            r = w["row"] + (j if w["direction"] == "vertical" else 0)
            c = w["col"] + (j if w["direction"] == "horizontal" else 0)
            word_cells[i].add((r, c))
    adj = {i: set() for i in range(len(words))}
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if word_cells[i] & word_cells[j]:
                adj[i].add(j)
                adj[j].add(i)
    visited = {0}
    queue = [0]
    while queue:
        n = queue.pop(0)
        for nb in adj[n]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return len(visited) == len(words)

def validate(grid, words, label):
    word_set = set(w["word"] for w in words)
    runs = find_all_runs(grid)
    errors = []

    # Check ghost words
    for run in runs:
        if run["text"] not in word_set:
            errors.append(f"Ghost: '{run['text']}' at ({run['row']},{run['col']}) {run['dir']}")

    # Check connectivity
    if not check_connectivity(words):
        errors.append("NOT CONNECTED")

    if errors:
        print(f"\n  ✗ {label} FAILED:")
        for e in errors:
            print(f"    -> {e}")
        return False
    else:
        print(f"\n  ✓ {label} PASSED")
        return True

def show(label, grid, words):
    print(f"\n{label}:")
    for row in grid:
        print("  " + " ".join(row))
    print(f"  Words: {[w['word'] for w in words]}")
    print(f"  Letters: {sum(1 for r in grid for c in r if c != 'X')}")

puzzles = []

# =============================================
# Day 0 (Monday - Easy)
# Approach: Simple cross pattern. Central horizontal word crossed by verticals.
# BUKË horizontal, KAFË crossing at K, ERA crossing at A, etc.
#
#   Row 0: . K . . . . .   KAFË vertical: K(0,1) A(1,1) F(2,1) Ë(3,1)
#   Row 1: B A L . . . .   BAL? No... let me think differently.
#
# Better approach: One long word across, others crossing down.
# BUKË across top, words crossing down from it.
#
#   Row 0: B U K Ë . . .   BUKË horizontal
#   Row 1: . J . A . . .   UJË vertical from U(0,1): U(0,1) J(1,1) Ë(2,1)
#   Row 2: . Ë . F . . .   KAFË vertical from K(0,2)? No, K→A→F→Ë
#                            Wait, BUKË has K at (0,2). KAFË starts with K.
#                            So KAFË vertical from (0,2): K(0,2) A(1,2) F(2,2) Ë(3,2)
#   Row 3: . . . Ë . . .
#
# But UJË vertical from (0,1) = U(0,1) J(1,1) Ë(2,1) — that's good, U shared with BUKË.
# KAFË vertical from (0,2) = K(0,2) A(1,2) F(2,2) Ë(3,2) — K shared with BUKË.
# Now I need more words. ERA, DET, MAL, ZOG.
# ERA could cross KAFË at A(1,2): E(1,1)? No, (1,1) is J from UJË.
# ERA crossing at A(1,2): E(1,0) R(1,1)? No, (1,1) is J.
# Hmm. Let me try ERA horizontal at row 4: E(4,0) R(4,1) A(4,2)
# Then nothing connects it to top group. Need a vertical connector.
# What if Ë(3,2) from KAFË connects to something?
#
# Actually let me try a simpler layout. Just make sure every run is a word.
#
# Clean approach: two crossing words, then extend from there.
#
#   BUKË horizontal row 0:    B(0,0) U(0,1) K(0,2) Ë(0,3)
#   UJË vertical from (0,1):  U(0,1) J(1,1) Ë(2,1)  [shares U at (0,1)]
#   KAFË vertical from (0,2): K(0,2) A(1,2) F(2,2) Ë(3,2)  [shares K at (0,2)]
#
# Now row 1: X J A X ... — "JA" is a ghost! J(1,1) A(1,2) forms "JA" horizontally.
# Fix: Need gap between J and A. Can't have both UJË and KAFË adjacent.
# Move KAFË to col 4: K(0,4)?? But BUKË only goes to col 3.
#
# OK different approach. Avoid adjacent parallel words.
#
#   BUKË horizontal row 0 col 0:    B(0,0) U(0,1) K(0,2) Ë(0,3)
#   UJË vertical from (0,1):         U(0,1) J(1,1) Ë(2,1) [shares U]
#   KAFË horizontal row 2 col 1:     K(2,1)? No, (2,1) is Ë from UJË.
#
# Hmm, Ë ≠ K so that conflicts. What if UJË is at col 3?
#   BUKË: B(0,0) U(0,1) K(0,2) Ë(0,3)
#   UJË vertical from Ë(0,3): Ë(0,3) ... no, UJË starts with U not Ë.
#
# Let me try:
#   ERA horizontal row 0:     E(0,0) R(0,1) A(0,2)
#   EMËR vertical from (0,0): E(0,0) M(1,0) Ë(2,0) R(3,0)  [shares E]
#   ARRË horizontal row 3:    A(3,0)? R=3,0 is R from EMËR. A≠R conflict.
#
# This is tricky. Let me try a totally different strategy.
# Use a + shape: one horizontal word crossing one vertical word at center.
#
#   MAL horizontal row 3:     M(3,1) A(3,2) L(3,3)
#   KAFË vertical from (1,2): K(1,2) A(2,2) F(3,2) Ë(4,2)
#   Wait, (3,2) would be both A (from MAL) and F (from KAFË). Conflict!
#   Need to share a letter. MAL has A at position 1 (col 2).
#   KAFË has A at position 1.
#   So if KAFË goes vertical, A is at row 2. MAL is at row 3. They don't cross.
#   Need MAL at row 2: M(2,1) A(2,2) L(2,3) — shares A(2,2) with KAFË. Yes!
#
#   KAFË vertical col 2: K(1,2) A(2,2) F(3,2) Ë(4,2)
#   MAL horizontal row 2: M(2,1) A(2,2) L(2,3)  [shares A at (2,2)]
#
#   Now check: row 2 is M A L — that's MAL. Good.
#   Col 2: K A F Ë — that's KAFË. Good.
#   Col 1: only M at (2,1) — single letter, no run. Good.
#   Col 3: only L at (2,3) — single letter, no run. Good.
#
#   Now add more. BUKË could cross KAFË at K(1,2):
#   BUKË horizontal row 1: B(1,0) U(1,1) K(1,2) Ë(1,3)  [shares K at (1,2)]
#   Check row 1: B U K Ë — that's BUKË. Good.
#   Check col 0: only B at (1,0) — single. Good.
#   Check col 1: U(1,1) and M(2,1) — "UM" vertically! Ghost!
#   Fix: Need gap. Can't have U at (1,1) and M at (2,1).
#   Move MAL to row 2 col 3: M(2,3) A(2,4) L(2,5)?
#   Then KAFË A is at (2,2) but MAL starts at (2,3). No shared cell.
#   Need MAL to cross KAFË. So MAL must pass through col 2 at row 2.
#   The only way is M(2,0) A(2,1)? No, KAFË A is at (2,2).
#   MAL at (2,1): M(2,1) A(2,2) L(2,3) — A shared with KAFË.
#   But then BUKË U at (1,1), MAL M at (2,1) → "UM" ghost in col 1.
#
#   Fix: Move BUKË. Put BUKË at row 1 col 2: B(1,2)?? Then B≠K conflict with KAFË.
#
#   Move BUKË to cross somewhere else. BUKË has letters B,U,K,Ë.
#   It can cross KAFË at K. KAFË K is at (1,2).
#   BUKË horizontal with K at col 2: means BUKË starts at col 0.
#   B(1,0) U(1,1) K(1,2) Ë(1,3). K shared with KAFË. Good.
#   Problem: U(1,1) above M(2,1) creates "UM".
#   Solution: Move MAL so it doesn't use col 1.
#   MAL crossing KAFË at A(2,2): needs A at some position.
#   MAL = M-A-L. A is position 1. For horizontal at row 2:
#     If A at col 2: MAL at (2,1)-(2,3). M at (2,1) under U(1,1). Ghost.
#     If A at col 2 but vertical: M(1,2)? Conflicts with K.
#   Alternative: Don't cross MAL with KAFË. Cross it with something else.
#
# Let me restart with a cleaner design. The challenge is avoiding adjacent cells.
# Rule: after placing each word, check that no unintended runs form.
#
# SIMPLEST APPROACH: One main horizontal, verticals crossing it, spread apart.
#
#   Row 3: D U A . E R A    DUA horizontal (3,0)-(3,2), ERA horizontal (3,4)-(3,6)
#                            Gap at (3,3) = X. Good, no ghost.
#   BUKË vertical crossing DUA at U(3,1):
#     BUKË = B-U-K-Ë. U at position 1. So B(2,1) U(3,1) K(4,1) Ë(5,1)
#     Shares U at (3,1) with DUA.
#   Check col 1: B(2,1) U(3,1) K(4,1) Ë(5,1) = BUKË. Good.
#   Check row 2: only B at (2,1). Single. Good.
#   Check row 4: only K at (4,1). Single. Good.
#   Check row 5: only Ë at (5,1). Single. Good.
#
#   VERË vertical crossing ERA at R(3,5):
#     VERË = V-E-R-Ë. R at position 2. So V(1,5) E(2,5) R(3,5) Ë(4,5)
#     Shares R at (3,5) with ERA.
#   Check col 5: V(1,5) E(2,5) R(3,5) Ë(4,5) = VERË. Good.
#   Check (3,4) is E from ERA, (3,5) is R from ERA — "ERA" is the run.
#   Check row 1: only V at (1,5). Single. Good.
#   Check row 2: only E at (2,5). Single. Good.
#   Check row 4: only Ë at (4,5). Single. Good.
#
#   Now DUA and ERA are separate groups. Need to connect them.
#   A vertical word crossing both? Or a word connecting DUA to ERA.
#   DUA is at row 3, cols 0-2. ERA is at row 3, cols 4-6.
#   They're on the same row but separated by X at (3,3).
#   Need a vertical word that shares a cell with both groups.
#
#   What about MAL vertical crossing DUA at A(3,2) and then connecting down?
#   MAL = M-A-L. A at position 1. M(2,2) A(3,2) L(4,2). Shares A with DUA.
#   Now MAL is connected to DUA. Good.
#
#   Need to connect to ERA group. VERË is in ERA's column.
#   What about a horizontal word at row 2 or row 4 spanning both groups?
#   Row 2: M at (2,2), could extend. But need a word starting/ending at M.
#   Row 4: K at (4,1) from BUKË, L at (4,2) from MAL, Ë at (4,5) from VERË.
#   (4,1)=K, (4,2)=L — "KL" would be ghost! Two adjacent. Bad.
#   Fix: Don't put MAL at col 2. Move MAL.
#
# This is getting complex. Let me try a systematic approach with wider spacing.
#
# DESIGN PRINCIPLE:
# - Place words so that crossing cells are the ONLY adjacent cells
# - Leave at least 1 X gap between parallel runs
# - Build a tree: each word shares exactly 1 cell with at least 1 other word
#
# Day 0 — Simple 5-word design:
#
#     0 1 2 3 4 5 6
#  0: . . M A L . .     MAL horizontal (0,2)
#  1: . . A . U . .     MAMI vertical from (0,2): M(0,2) A(1,2) M(2,2) I(3,2)
#  2: D U M . L . .     Wait, that puts M at (0,2) and A at (1,2).
#                        LULE vertical: L(0,4) U(1,4) L(2,4) E(3,4)?
#                        That has L at (0,4) but MAL ends at (0,4).
#                        MAL is (0,2)-(0,4). L at (0,4). Then LULE vertical shares L.
#                        Row 0: X X M A L X X — that's MAL. Good.
#                        Col 4: L(0,4) U(1,4) L(2,4) E(3,4) = LULE. Good.
#                        Col 2: M(0,2) A(1,2) — "MA" ghost! Need full word or single letter.
#
# I keep hitting adjacent cell issues. Let me try the absolute simplest pattern:
# One horizontal word, one vertical word crossing it. That's it for start.
#
# Actually, let me just carefully design each puzzle one at a time, checking
# every adjacent cell. I'll write a helper that detects problems immediately.

# =============================================
# Day 0: Simple cross layout
# =============================================
# Strategy: Central + shape, then extend carefully
#
#     0 1 2 3 4 5 6
#  0: . . . M . . .
#  1: . . . A . . .     MAL: need horizontal. MAMI vertical?
#  2: . . . L . . .
#
# Simpler: just MAMI vertical center, ERA crossing at A
#
#     0 1 2 3 4 5 6
#  0: . . . M . . .     MAMI vertical col 3: M(0,3) A(1,3) M(2,3) I(3,3)
#  1: . . E R A . .     ERA horizontal row 1: E(1,1) R(1,2) A(1,3) — shares A(1,3)
#  2: . . . M . . .
#  3: D U A I . . .     DUA horizontal: D(3,0) U(3,1) A(3,2) — but (3,3) is I from MAMI
#                        "DUAI" ghost! Need gap. DUA at (3,0)-(3,2), I at (3,3).
#                        They're adjacent! Ghost "DUAI".
#                        Fix: put DUA at row 5 or somewhere with gap.
#
#     0 1 2 3 4 5 6
#  0: . . . M . . .     MAMI vertical col 3
#  1: . E R A . . .     ERA horizontal row 1: shares A(1,3)
#  2: . . . M . . .
#  3: . . . I . . .
#  4: . . . . . . .
#  5: D U A . . . .     DUA — not connected to MAMI.
#
# Need to connect DUA. Add vertical word from ERA area down to DUA area.
# E is at (1,1). A vertical from E: EMËR = E(1,1) M(2,1) Ë(3,1) R(4,1)
# Then another word crossing EMËR that also touches DUA?
# DUA at row 5, EMËR ends at row 4. R at (4,1), DUA D at (5,0). Not connected.
# Put DUA at (4,0): D(4,0) U(4,1) A(4,2).
# R at (4,1) from EMËR. U from DUA at (4,1). R ≠ U conflict!
#
# This approach of manual design is very error-prone. Let me take a completely
# different approach: build a small automated crossword generator that respects
# all the rules.

print("Manual puzzle design is too error-prone.")
print("The adjacent-cell constraint makes it very hard to design by hand.")
print("Each puzzle needs careful automated checking after each word placement.")
print()
print("Key insight: In a valid crossword grid, every consecutive run of letters")
print("(horizontal or vertical) must be exactly one word. This means:")
print("  - Words can only touch at crossing points (different directions)")
print("  - Same-direction words must have X gap between them")
print("  - A horizontal word's letters must not extend vertically into")
print("    adjacent cells that form ghost runs")
print()
print("Recommendation: Build an incremental placer that checks all runs")
print("after each word is added.")
