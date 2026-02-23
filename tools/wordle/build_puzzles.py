#!/usr/bin/env python3
"""
Build crossword puzzles incrementally.
After each word placement, validate ALL runs.
This ensures no ghost words ever form.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GRID_SIZE = 7

def make_grid():
    return [["X"] * GRID_SIZE for _ in range(GRID_SIZE)]

def copy_grid(grid):
    return [r[:] for r in grid]

def show(grid):
    for row in grid:
        print("  " + " ".join(row))

def place_word(grid, word, row, col, direction):
    """Place word on grid, return False if conflict."""
    g = copy_grid(grid)
    for i, ch in enumerate(word):
        r = row + (i if direction == "vertical" else 0)
        c = col + (i if direction == "horizontal" else 0)
        if r >= GRID_SIZE or c >= GRID_SIZE:
            return None  # out of bounds
        if g[r][c] != "X" and g[r][c] != ch:
            return None  # conflict
        g[r][c] = ch
    return g

def find_all_runs(grid):
    """Find every H and V run of 2+ letters."""
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
                    runs.append(letters)
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
                    runs.append(letters)
            else:
                r += 1
    return runs

def check_no_ghosts(grid, word_set):
    """Check that every run of 2+ letters is in word_set."""
    runs = find_all_runs(grid)
    for run in runs:
        if run not in word_set:
            return False, run
    return True, None

def check_connectivity(words):
    """Check all words share cells forming one connected group."""
    if len(words) <= 1:
        return True
    cells_per_word = []
    for w in words:
        cells = set()
        for i in range(len(w["word"])):
            r = w["row"] + (i if w["direction"] == "vertical" else 0)
            c = w["col"] + (i if w["direction"] == "horizontal" else 0)
            cells.add((r, c))
        cells_per_word.append(cells)
    adj = {i: set() for i in range(len(words))}
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            if cells_per_word[i] & cells_per_word[j]:
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

def try_add_word(grid, words, word_set, word, row, col, direction):
    """Try to add a word. Returns new grid if valid, None if invalid."""
    new_grid = place_word(grid, word, row, col, direction)
    if new_grid is None:
        return None  # placement conflict

    # Check no ghost words
    new_word_set = word_set | {word}
    ok, ghost = check_no_ghosts(new_grid, new_word_set)
    if not ok:
        return None  # ghost word formed

    return new_grid

# =============================================
# Now let's build each puzzle carefully
# =============================================

def build_puzzle(plan, label):
    """
    Build a puzzle from a plan (list of word placements).
    Each entry: (word, row, col, direction)
    Returns (grid, words) if valid, raises on error.
    """
    grid = make_grid()
    words = []
    word_set = set()

    for i, (word, row, col, direction) in enumerate(plan):
        new_grid = try_add_word(grid, words, word_set, word, row, col, direction)
        if new_grid is None:
            # Show what went wrong
            test_grid = place_word(grid, word, row, col, direction)
            if test_grid is None:
                print(f"  Step {i}: '{word}' at ({row},{col}) {direction} — CONFLICT!")
            else:
                runs = find_all_runs(test_grid)
                new_ws = word_set | {word}
                ghosts = [r for r in runs if r not in new_ws]
                print(f"  Step {i}: '{word}' at ({row},{col}) {direction} — GHOSTS: {ghosts}")
            show(grid)
            raise ValueError(f"{label}: Failed to place '{word}' at step {i}")

        grid = new_grid
        word_set.add(word)
        words.append({"word": word, "row": row, "col": col, "direction": direction})

    # Final connectivity check
    if not check_connectivity(words):
        show(grid)
        raise ValueError(f"{label}: Words not all connected!")

    print(f"\n  ✓ {label} — valid!")
    show(grid)
    print(f"  Words: {[w['word'] for w in words]}")
    return grid, words


all_puzzles = []

# =============================================
# Day 0 (Monday - Easy, ~20 letters)
# Simple cross: MAMI vertical center, words crossing it
#
#     0 1 2 3 4 5 6
#  0: X X X M X X X     MAMI vertical col 3: M(0,3) A(1,3) M(2,3) I(3,3)
#  1: X E R A X X X     ERA horizontal: E(1,1) R(1,2) A(1,3) — crosses MAMI at A
#  2: X X X M X X X
#  3: X X X I X X X
#  4: X X X X X X X
#  5: X X X X X X X
#  6: X X X X X X X
#
# Now add DUA crossing MAMI at M(2,3):
# DUA horizontal: D(2,1) U(2,2) A(2,3)? But (2,3)=M. D-U-A, A≠M. Conflict.
# DUA vertical crossing ERA at R(1,2): D(0,2) U(1,2)? (1,2)=R. U≠R conflict.
# DUA crossing MAMI at... hmm, MAMI has M,A,M,I. DUA has D,U,A.
# Share A: MAMI A at (1,3). But ERA already at (1,3).
# DUA crossing ERA at E(1,1): D(0,1) U(1,1)? U≠E conflict.
#
# Different words. Let me use words that share letters easily.
# BUKË: B-U-K-Ë. Can cross MAMI at M with... no shared letter.
# MAL: M-A-L. Can cross MAMI at M(0,3) or M(2,3) or A(1,3).
# MAL crossing at A(1,3) — but ERA is there. MAL has A at pos 1.
# MAL horizontal with A at (1,3): M(1,2) A(1,3) L(1,4).
# But (1,2)=R from ERA. M≠R conflict.
# MAL crossing at M(0,3): M shared. MAL horizontal: M(0,3) A(0,4) L(0,5).
# Row 0: X X X M A L X. "MAL" is the run. Good.
# Col 4: only A(0,4). Single. Good.
# Col 5: only L(0,5). Single. Good.
#
# Now add BUKË crossing something.
# BUKË vertical crossing MAL at A(0,4)? BUKË=B-U-K-Ë. No A in BUKË.
# BUKË crossing ERA at E(1,1): B(0,1) U(1,1)? U≠E conflict.
# BUKË vertical at col 1 crossing ERA: ERA E is at (1,1).
# BUKË has no E. Can't cross at E.
# ERA R at (1,2). BUKË has no R.
#
# Hmm. Let me try different word combinations.
# Start over with BUKË as the anchor.
#
# BUKË horizontal row 2: B(2,0) U(2,1) K(2,2) Ë(2,3)
# KAFË vertical crossing at K(2,2): K(2,2) A(3,2) F(4,2) Ë(5,2)
# Check col 2: K(2,2) A(3,2) F(4,2) Ë(5,2) = KAFË. Good.
# Check row 3: only A(3,2). Single. Good. ✓
# Check row 4: only F(4,2). Single. Good. ✓
# Check row 5: only Ë(5,2). Single. Good. ✓
#
# Now ERA crossing KAFË at A(3,2):
# ERA = E-R-A. A at pos 2. ERA horizontal: E(3,0) R(3,1) A(3,2). Shares A.
# Check row 3: E R A — that's ERA. Good. ✓
# Check col 0: only E(3,0). Single. ✓
# Check col 1: only R(3,1). Single. ✓
#
# UJË crossing BUKË at U(2,1):
# UJË = U-J-Ë. U at pos 0. UJË vertical: U(2,1) J(3,1) Ë(4,1).
# But (3,1)=R from ERA! J≠R conflict!
# Fix: UJË horizontal crossing BUKË at U.
# UJË horizontal row 0 or row 4?
# UJË vertical at col 1: U(2,1) J(3,1). (3,1) is R from ERA. Conflict.
# UJË vertical at col 3: U(2,3)? (2,3)=Ë from BUKË. U≠Ë conflict.
# UJË crossing something else.
# UJË crossing KAFË at Ë(5,2): UJË=U-J-Ë. Ë at pos 2. U(5,0) J(5,1) Ë(5,2). Shares Ë.
# Check row 5: U J Ë — that's UJË. Good.
# Check col 0: only U(5,0) (and E at 3,0 and B at 2,0).
# Wait! B at (2,0), E at (3,0), U at (5,0). Are they contiguous?
# (2,0)=B, (3,0)=E. (4,0)=X. So col 0: B(2,0) E(3,0) = "BE" vertically! Ghost!
# "BE" is not a word. Need gap.
# Fix: Move ERA so E isn't at (3,0). ERA at (3,1)? E(3,1) R(3,2) A(3,3).
# (3,2) = A from KAFË. R≠A conflict!
# ERA at row 3 starting col 0 is the only way to share A at (3,2).
# So can't have B at (2,0).
# Move BUKË. BUKË horizontal row 2 col 1: B(2,1) U(2,2) K(2,3) Ë(2,4)?
# Then KAFË at col 3: K(2,3). KAFË vertical: K(2,3) A(3,3) F(4,3) Ë(5,3).
# ERA crossing KAFË at A(3,3): E(3,1) R(3,2) A(3,3). Shares A.
# Col 1: B(2,1) and E(3,1). "BE" ghost!
# Same problem.
#
# The issue: BUKË B and ERA E end up in the same column adjacent.
# Fix: Put a gap row between them. BUKË at row 0, ERA at row 3.
#
# BUKË row 0 col 1: B(0,1) U(0,2) K(0,3) Ë(0,4)
# KAFË vertical from K(0,3): K(0,3) A(1,3) F(2,3) Ë(3,3)
# ERA crossing KAFË at A(1,3): E(1,1) R(1,2) A(1,3).
# Col 1: only E(1,1). ✓ (B is at (0,1), E at (1,1) — "BE" ghost!)
# Argh! B(0,1) E(1,1) = "BE" in col 1.
#
# Fix: ERA starting further right. E(1,2) R(1,3)? (1,3)=A from KAFË. R≠A conflict.
# Or BUKË at row 0 col 0: B(0,0) U(0,1) K(0,2) Ë(0,3)
# KAFË vertical from K(0,2): K(0,2) A(1,2) F(2,2) Ë(3,2)
# ERA crossing at A(1,2): E(1,0) R(1,1) A(1,2).
# Col 0: B(0,0) E(1,0) = "BE" ghost!
#
# This keeps happening. B and E above each other.
# Solution: ERA must not be directly below BUKË in same column.
# Use ERA crossing KAFË but on the other side (going right from A).
# ERA at (1,2)-(1,4): E(1,2)? But (1,2)=A from KAFË. E≠A conflict.
# KAFË A is at (1,2). ERA A is at end. ERA = E(1,0) R(1,1) A(1,2).
# Still puts E at (1,0) under B(0,0).
#
# Fundamental issue: BUKË starts with B at col 0, and any word at row 1
# starting at col 0 will create a 2-letter vertical ghost with B.
#
# Fix: Leave row 1 col 0 empty. KAFË crossing at col 2 (not touching col 0).
# ERA should NOT be at row 1 col 0.
# ERA crossing KAFË at A(1,2). ERA = E-R-A. A at pos 2.
# So ERA goes from (1,0) to (1,2). E at (1,0) under B(0,0). Ghost.
# Alternative: ERA vertical. E(0,2)? (0,2)=K from BUKË. E≠K.
# ERA at row 4 crossing KAFË at Ë(3,2)? ERA has no Ë.
#
# OK completely new approach. Don't use BUKË and ERA together.
# Use words that don't create column ghosts.
#
# Let me just carefully build ONE puzzle that works.

# =============================================
# Day 0 - Build step by step
# =============================================
# Start: KAFË vertical center
# Add: words crossing it, checking ghosts after each step

plan = [
    # Step 1: KAFË vertical col 3
    ("KAFË", 0, 3, "vertical"),    # K(0,3) A(1,3) F(2,3) Ë(3,3)
    # Step 2: ERA crossing at A(1,3)
    ("ERA", 1, 1, "horizontal"),    # E(1,1) R(1,2) A(1,3) — shares A
    # Step 3: MAL crossing at... need to cross existing word
    # KAFË F at (2,3). No word has F at intersection position easily.
    # KAFË Ë at (3,3). Words with Ë: BUKË(Ë at end), UJË(Ë at end)
    # BUKË horizontal ending at (3,3): B(3,0) U(3,1) K(3,2) Ë(3,3). Shares Ë.
    # Check col 0: only B(3,0). ✓
    # Check col 1: E(1,1) and then gap at (2,1), then (3,1)=U.
    # col 1: (1,1)=E, (2,1)=X, (3,1)=U. Not adjacent. ✓
    # Check col 2: R(1,2) then (2,2)=X, (3,2)=K. Not adjacent. ✓
    ("BUKË", 3, 0, "horizontal"),  # B(3,0) U(3,1) K(3,2) Ë(3,3) — shares Ë
    # Step 4: UJË crossing ERA at E(1,1)? UJË=U-J-Ë. No E.
    # UJË crossing BUKË at U(3,1): UJË vertical U(3,1) J(4,1) Ë(5,1). Shares U.
    ("UJË", 3, 1, "vertical"),     # U(3,1) J(4,1) Ë(5,1) — shares U with BUKË
    # Check row 3: B U K Ë — BUKË. ✓
    # Check row 4: only J(4,1). Single. ✓
    # Check row 5: only Ë(5,1). Single. ✓
    # Step 5: MAL crossing ERA at R(1,2)? MAL=M-A-L. No R.
    # MAL vertical crossing BUKË at K(3,2): MAL has no K.
    # MAL horizontal row 5: M(5,3) A(5,4) L(5,5)? Not connected to anything.
    # MAL crossing KAFË at K(0,3): MAL has no K.
    # Need a word that crosses existing grid.
    # ZOG crossing KAFË at... no shared letters with K,A,F,Ë.
    # DET crossing ERA at E(1,1)? DET=D-E-T. E at pos 1.
    # DET vertical: D(0,1) E(1,1) T(2,1). Shares E with ERA.
    # Check col 1: D(0,1) E(1,1) T(2,1) = DET. ✓
    # Check row 0: (0,1)=D and (0,3)=K. Not adjacent. ✓
    # Check row 2: (2,1)=T and (2,3)=F. Not adjacent. ✓
    ("DET", 0, 1, "vertical"),     # D(0,1) E(1,1) T(2,1) — shares E with ERA
    # Step 6: MAL. Where can it go?
    # Need to cross an existing word. Available cells:
    # D(0,1), K(0,3), E(1,1), R(1,2), A(1,3), T(2,1), F(2,3),
    # B(3,0), U(3,1), K(3,2), Ë(3,3), J(4,1), Ë(5,1)
    # MAL = M-A-L. A at pos 1.
    # Cross at A(1,3) from KAFË — but ERA already uses A(1,3). Can still cross.
    # MAL vertical from (0,3): M(0,3)? (0,3)=K. Conflict.
    # MAL horizontal at (1,3): A shared. M(1,2)? (1,2)=R. Conflict.
    # MAL vertical crossing UJË at Ë(5,1)? MAL has no Ë.
    # MAL crossing BUKË at K(3,2)? MAL has no K.
    # MAL at row 5: M(5,3) A(5,4) L(5,5). Not connected.
    # Unless a vertical connects. What if we add a word at col 3?
    # (3,3)=Ë, (5,3)=M. Need Ë_M or some connection.
    # EMËR vertical? E-M-Ë-R at col 3: E(2,3)? (2,3)=F. Conflict.
    #
    # Let me try ZOG instead.
    # ZOG crossing BUKË at... Z-O-G. BUKË has B,U,K,Ë. No shared letter.
    # ZOG crossing UJË at J(4,1)? Z-O-G, no J.
    # ZOG crossing DET at T(2,1)? No T in ZOG.
    # ZOG crossing ERA at R(1,2)? No R.
    #
    # VAJ crossing ERA at A(1,3)? VAJ=V-A-J. A at pos 1.
    # VAJ vertical: V(0,3) A(1,3)? (0,3)=K. Conflict.
    # VAJ horizontal: need A at (1,3). V(1,2) A(1,3)? (1,2)=R. Conflict.
    # V(1,2) = R conflict.
    #
    # Hmm. It's hard to add more words without ghosts.
    # Let me try adding MAL horizontally at row 5, then connect with a vertical.
    # MAL at (5,4): M(5,4) A(5,5) L(5,6). Not connected.
    # Add ZOG vertical at col 5: Z(3,5) O(4,5) G(5,5)?
    # (5,5) = A from MAL. G≠A conflict.
    # ZOG vertical: Z(4,4) O(5,4) G(6,4).
    # (5,4) = M from MAL. O≠M conflict.
    # Rethinking... MAL at (5,3): M(5,3) A(5,4) L(5,5).
    # (5,1)=Ë from UJË, (5,3)=M. Not adjacent (gap at 5,2). ✓
    # But not connected to any existing word.
    # Need a vertical bridge. What connects row 3 area to row 5?
    # UJË goes to (5,1). MAL is at (5,3). Gap between. Not connected.
    # What if I add DUA vertical from (3,0)? D(3,0)=B. Conflict.
    #
    # I think 5 words (KAFË, ERA, BUKË, UJË, DET) is already a good Day 0!
    # Let me check letter count.
    # KAFË=4, ERA=3, BUKË=4, UJË=3, DET=3 = 17 letters - shared cells
    # Shared: A(1,3), Ë(3,3), U(3,1), E(1,1) = 4 shared
    # Total cells: 17-4 = 13. That's pretty small for a 7x7 grid.
    # Let me add 2 more words somehow.
    #
    # DORË vertical crossing BUKË at... DORË=D-O-R-Ë.
    # Cross at B(3,0)? DORË has no B.
    # Cross at K(3,2)? No K in DORË.
    # Cross at Ë(3,3)? Ë at pos 3 (last). So D(0,3) O(1,3) R(2,3) Ë(3,3).
    # (0,3)=K. D≠K conflict.
    # Cross DET at D(0,1): D at pos 0. D(0,1) O(1,1)? (1,1)=E. O≠E conflict.
    #
    # ZOG vertical crossing BUKË at K(3,2)? ZOG = Z-O-G. No K.
    #
    # VALË crossing KAFË at... VALË=V-A-L-Ë.
    # A at pos 1, Ë at pos 3. Cross KAFË at A(1,3):
    # VALË horizontal: V(1,2) A(1,3)? (1,2)=R. V≠R.
    # VALË vertical: A at row 1, col 3. V(0,3) A(1,3). (0,3)=K. V≠K.
    #
    # OK, let me add a 6th word by crossing DET.
    # DET is at D(0,1) E(1,1) T(2,1).
    # Word crossing at D(0,1): needs D. DUA = D-U-A. D at pos 0.
    # DUA horizontal: D(0,1) U(0,2) A(0,3). (0,3)=K. A≠K.
    # DUA horizontal: D(0,1) U(0,0)? That's backwards.
    # DUA vertical from (0,1) is DET already occupying col 1.
    #
    # Word crossing at T(2,1): needs T.
    # TOKË=T-O-K-Ë. T at pos 0. TOKË horizontal: T(2,1) O(2,2) K(2,3) Ë(2,4).
    # (2,3)=F from KAFË. K≠F conflict.
    # TOKË vertical: T(2,1) O(3,1)? (3,1)=U from BUKË. O≠U.
    #
    # NATË=N-A-T-Ë. T at pos 2.
    # NATË horizontal with T at (2,1): N(2,-1). Out of bounds.
    # NATË vertical with T at (2,1): N(0,1) A(1,1). (0,1)=D. N≠D.
    #
    # This is really hard. Let me accept 5 words for Day 0 and move on.
    # Actually wait. Let me try adding ZOG at an isolated crossing.
    # ZOG horizontal at row 6: Z(6,0) O(6,1) G(6,2).
    # Connected to UJË Ë(5,1)? (6,1)=O, (5,1)=Ë. Adjacent but different rows.
    # Col 1: ..J(4,1) Ë(5,1) O(6,1). That's "JËO" ghost!
    # So ZOG at row 6 col 0 won't work because of col 1 extending UJË.
    #
    # ZOG at row 6 col 4: Z(6,4) O(6,5) G(6,6). Not connected.
    # Need a vertical bridge down from main grid.
    #
    # Let me try a completely different structure for Day 0.
]

# Actually, let me take a step back and design the puzzles more carefully
# using a different layout strategy.
#
# STRATEGY: "Cross" layout
# - Start with 2 words crossing in the center
# - Add words crossing the first words, spaced so no ghosts
# - Key: between any two parallel words in same col/row, must be X gap

# =============================================
# Day 0: Fresh design
# =============================================
# KAFË horizontal row 2: K(2,0) A(2,1) F(2,2) Ë(2,3)
# MAL vertical crossing at A(2,1): M(1,1) A(2,1) L(3,1)
# ERA vertical crossing at... hmm ERA and KAFË share A.
# ERA crossing KAFË at A(2,1) — same cell as MAL. Can't have 2 verticals there.
# ERA vertical crossing at Ë(2,3): ERA=E-R-A. No Ë in ERA.
#
# New try:
# DUA horizontal row 3: D(3,2) U(3,3) A(3,4)
# KAFË vertical crossing at... shares with DUA? KAFË=K-A-F-Ë.
# A at pos 1. KAFË vertical with A at (3,4): K(2,4) A(3,4) F(4,4) Ë(5,4).
# Shares A(3,4) with DUA. ✓
# ERA vertical crossing DUA at U(3,3): ERA=E-R-A. No U. ✗
# ERA vertical crossing DUA at D(3,2): no D in ERA. ✗
# MAL vertical crossing DUA at A(3,4): already KAFË there. ✗
# MAL vertical crossing KAFË at K(2,4): M-A-L, no K. ✗
# MAL horizontal crossing KAFË at F(4,4): M-A-L, no F. ✗
#
# UJË vertical crossing DUA at U(3,3): U-J-Ë, U at pos 0.
# UJË vertical: U(3,3) J(4,3) Ë(5,3). Shares U(3,3).
# Check row 4: (4,3)=J, (4,4)=F. "JF" ghost! Adjacent cells!
# Fix: need gap. Can't have KAFË F at (4,4) and UJË J at (4,3).
# Move UJË: U(3,3) is fixed (crossing DUA). J goes to (4,3). F at (4,4).
# They'll always be adjacent. So UJË and KAFË can't both cross DUA this way.
#
# Move KAFË to col 2: K(1,2) A(2,2) F(3,2) Ë(4,2).
# Cross DUA at... DUA is at row 3 cols 2-4. D at (3,2).
# KAFË F at (3,2). F≠D conflict.
# DUA at row 2: D(2,1) U(2,2) A(2,3). KAFË A at (2,2). U≠A conflict.
# DUA at (2,2): D(2,0) U(2,1) A(2,2). KAFË A at (2,2). Shares A. ✓
# UJË crossing KAFË at Ë(4,2): U-J-Ë, Ë at pos 2.
# UJË horizontal: U(4,0) J(4,1) Ë(4,2). Shares Ë. ✓
# Check col 0: (2,0)=D, (4,0)=U. Not adjacent (gap at 3,0). ✓
# Check col 1: (2,1)=U, (4,1)=J. Not adjacent. ✓
#
# Now: DUA(2,0)-(2,2), KAFË(1,2)-(4,2), UJË(4,0)-(4,2)
# All connected via shared cells. ✓
# Add ERA crossing KAFË at K(1,2): ERA=E-R-A. No K. ✗
# Add ERA crossing DUA at D(2,0): E-R-A, no D. ✗
# ERA crossing DUA at A(2,2): already KAFË there.
# ERA horizontal at row 1: E(1,0) R(1,1) A(1,2). (1,2)=K from KAFË. A≠K. ✗
#
# MAL crossing KAFË at A(2,2): M-A-L, A at pos 1.
# MAL horizontal: M(2,1) A(2,2) L(2,3). (2,1)=U from DUA. M≠U. ✗
# MAL vertical: M(1,2) A(2,2). (1,2)=K. M≠K. ✗
#
# Let me try: BUKË crossing KAFË at K(1,2).
# BUKË=B-U-K-Ë. K at pos 2.
# BUKË horizontal: B(1,0) U(1,1) K(1,2) Ë(1,3). Shares K(1,2).
# Check col 0: (1,0)=B, (2,0)=D. Adjacent! "BD" ghost!
# Fix: can't have B above D.
# BUKË horizontal row 0: B(0,0) U(0,1) K(0,2) Ë(0,3). (0,2) not in KAFË yet.
# KAFË starts at (1,2). K at (0,2) is separate from K at (1,2).
# Actually wait — I need BUKË to cross KAFË. K at (0,2), KAFË K at (1,2).
# Different cells. No crossing.
# BUKË K at pos 2 crossing KAFË K at (1,2):
# BUKË horizontal at row 1: B(1,0) U(1,1) K(1,2). That's only 3 letters. BUKË is 4.
# B(1,0) U(1,1) K(1,2) Ë(1,3). Good, 4 letters.
# But col 0: (1,0)=B above (2,0)=D → "BD" ghost.
#
# ARGH. Always ghosts.
# Move DUA to not be at col 0. DUA at (2,1): D(2,1) U(2,2) A(2,3).
# (2,2) needs to share with KAFË. KAFË A at (2,2). U≠A conflict!
# DUA at (2,3): D(2,3) U(2,4) A(2,5). Not crossing KAFË.
#
# I think the fundamental issue is that in a 7x7 grid with many words,
# avoiding ALL vertical AND horizontal ghost runs is extremely constraining.
#
# Let me try a VERY sparse layout.

# Day 0 plan: just 4 words in a simple cross
plan0 = [
    ("KAFË", 1, 3, "vertical"),    # K(1,3) A(2,3) F(3,3) Ë(4,3)
    ("ERA",  2, 1, "horizontal"),   # E(2,1) R(2,2) A(2,3) — shares A
    ("DUA",  2, 3, "vertical"),     # Wait, col 3 already has KAFË.
    # DUA crossing ERA at A(2,3)? But KAFË A is also at (2,3).
    # That's fine — both KAFË and ERA share A(2,3). And DUA also at (2,3)?
    # DUA is D-U-A. A at pos 2. DUA vertical: D(0,3) U(1,3) A(2,3).
    # (1,3) = K from KAFË. U≠K conflict!
]

# OK I'm going to write this differently. Let me just try MANY layouts programmatically.

def try_layout(plan):
    """Try a layout plan, return (grid, words) or None."""
    grid = make_grid()
    words = []
    word_set = set()
    for word, row, col, direction in plan:
        new_grid = place_word(grid, word, row, col, direction)
        if new_grid is None:
            return None
        new_ws = word_set | {word}
        ok, ghost = check_no_ghosts(new_grid, new_ws)
        if not ok:
            return None
        grid = new_grid
        word_set.add(word)
        words.append({"word": word, "row": row, "col": col, "direction": direction})
    if not check_connectivity(words):
        return None
    return grid, words


# Let me try Day 0 with many combinations
# Base: KAFË vertical, ERA crossing at A

attempts = [
    # KAFË at different positions, ERA crossing at A
    # Then try adding more words
]

# KAFË vertical at (0,3): K(0,3) A(1,3) F(2,3) Ë(3,3)
# ERA at row 1: E(1,1) R(1,2) A(1,3)
# Grid so far:
#   0: . . . K . . .
#   1: . E R A . . .
#   2: . . . F . . .
#   3: . . . Ë . . .
# Now DET crossing ERA at E(1,1): DET vertical D(0,1) E(1,1) T(2,1)
# Grid:
#   0: . D . K . . .
#   1: . E R A . . .
#   2: . T . F . . .
#   Check col 1: D E T = DET ✓
#   Check row 0: D(0,1) alone between Xs and K(0,3). D single. ✓ K single. ✓
#   Check row 2: T(2,1) and F(2,3). Not adjacent. ✓
# Now BUKË crossing KAFË at Ë(3,3): BUKË=B-U-K-Ë. Ë at pos 3.
# BUKË horizontal: B(3,0) U(3,1) K(3,2) Ë(3,3). Shares Ë.
# Check col 0: B(3,0) alone. ✓
# Check col 1: T(2,1) and U(3,1). Adjacent! "TU" ghost!
# Fix: BUKË at row 5: B(5,0) U(5,1) K(5,2) Ë(5,3). Too far, not connected.
# BUKË vertical crossing KAFË at Ë(3,3): Ë at pos 3, so B(0,3)? (0,3)=K. B≠K.
#
# BUKË crossing KAFË at K(0,3): BUKË K at pos 2.
# BUKË horizontal: B(0,1) U(0,2) K(0,3) Ë(0,4). Shares K(0,3).
# Check col 1: B(0,1) and D(0,1)? Wait, (0,1) already has D from DET!
# B≠D conflict!
# BUKË at (0,2): B(0,2) U(0,3)? (0,3)=K. U≠K.
# BUKË vertical: B-U-K-Ë with K at (0,3). K at pos 2, so B(−2,3). Out of bounds.
#
# UJË crossing KAFË at Ë(3,3): UJË=U-J-Ë. Ë at pos 2.
# UJË horizontal: U(3,1) J(3,2) Ë(3,3). Shares Ë.
# Check col 1: T(2,1) and U(3,1). Adjacent! "TU" ghost!
# UJË at (3,5): U(3,5) J(3,4)? Backwards. Not valid.
# UJË right-to-left doesn't work.
# UJË horizontal: U(3,3) J(3,4) Ë(3,5)? (3,3)=Ë. U≠Ë conflict.

# OK let me try one more combination. Put KAFË in the middle, things above and below.

# KAFË vertical col 3 rows 0-3: K(0,3) A(1,3) F(2,3) Ë(3,3)
# UJË horizontal row 3: U(3,4) J(3,5) Ë(3,6)? (3,3)=Ë (3,4)=U. Different cells.
# But Ë(3,3) and U(3,4) are adjacent → "ËU" ghost.
# Can't place UJË right after KAFË on same row.
# UJË with Ë at pos 2: U(3,1) J(3,2) Ë(3,3).
# (3,3) shares with KAFË Ë. But J(3,2) next to something?
# Col 2: only J(3,2)? If nothing else in col 2. Need to check later words.
# (3,1)=U. Col 1: depends on other words.
# For now: UJË(3,1)-(3,3), sharing Ë with KAFË.
# ERA horizontal row 1: E(1,1) R(1,2) A(1,3). Shares A with KAFË.
# Col 1: (1,1)=E, (3,1)=U. Not adjacent (gap at 2,1). ✓
# Col 2: (1,2)=R, (3,2)=J. Not adjacent. ✓
# Row 3: U J Ë. That's UJË. ✓
#
# Now: KAFË + ERA + UJË. All connected via KAFË.
# Grid:
#   0: . . . K . . .
#   1: . E R A . . .
#   2: . . . F . . .
#   3: . U J Ë . . .
# Add DUA crossing UJË at U(3,1): DUA=D-U-A. U at pos 1.
# DUA vertical: D(2,1) U(3,1) A(4,1). Shares U.
# Check col 1: (1,1)=E, (2,1)=D. Adjacent! "ED" ghost!
# Fix: DUA horizontal from U(3,1): D(3,0) U(3,1). (3,0)=X, (3,1)=U.
# D(3,0) U(3,1) A(3,2)? (3,2)=J. A≠J conflict!
# DUA at (4,1): D(4,1) U(4,2)? Not crossing anything.
# DUA vertical: D(4,1) U(5,1) A(6,1). Not connected to grid.
# Unless something connects to (4,1).
#
# MAL crossing ERA at R(1,2)? MAL=M-A-L. No R. ✗
# MAL crossing ERA at A(1,3): same cell as KAFË intersection.
# MAL vertical from A(1,3): M(0,3)=K. M≠K. ✗
# MAL horizontal: M(1,2) A(1,3). (1,2)=R. M≠R. ✗  or M(1,4) A(1,5) L(1,6)? Not crossing.
#
# BUKË crossing ERA at R(1,2): BUKË has no R. ✗
# BUKË crossing ERA at E(1,1): BUKË has no E. Well, wait. BUKË = B-U-K-Ë. No E.
#
# DET crossing ERA at E(1,1): DET=D-E-T. E at pos 1.
# DET vertical: D(0,1) E(1,1) T(2,1). Shares E.
# Check col 1: D(0,1) E(1,1) T(2,1) = DET. Then (3,1)=U from UJË.
# T(2,1) and U(3,1) adjacent → "DETU" or at least "TU" ghost!
# The whole col: D(0,1) E(1,1) T(2,1) U(3,1) = "DETU" ghost!
#
# Can't have DET in col 1 with UJË U also in col 1 at row 3.
# Move UJË. UJë at (3,5): U(3,5) J(3,6)... only 2 letters, but UJË is 3.
# U(3,4) J(3,5) Ë(3,6). But (3,3)=Ë from KAFË, (3,4)=U. Adjacent. "ËU" ghost.
#
# This is extremely constrained. I think I need to abandon placing
# multiple words on the same row/column.
#
# NEW INSIGHT: The safest pattern is a TREE of words where:
# - Each word crosses exactly one other word at one letter
# - No word shares a row or column range with a parallel word
# This guarantees no ghost words (each run is exactly one word).

# Let me build with this constraint.
# KAFË vertical col 3, rows 0-3
# ERA horizontal row 1, cols 1-3, crossing at A(1,3)
# DET vertical col 1, rows 0-2, crossing at E(1,1)
#   Col 1: D(0,1) E(1,1) T(2,1) — all from DET. No other word in col 1. ✓
# BUKË horizontal row 0, cols 0-3, crossing at...
#   (0,0)=B (0,1)=D? But DET D is at (0,1). B≠D conflict!
#   BUKË at row 0 cols 1-4: B(0,1)? (0,1)=D. Conflict.
#   BUKË crossing DET at D(0,1): BUKË has no D.
#   BUKË crossing DET at T(2,1): BUKË has no T.
#   BUKË crossing KAFË at F(2,3): BUKË has no F.
#
# MAL horizontal row 4, crossing KAFË at... KAFË ends at row 3.
# Can't cross KAFË in row 4.

# Actually let me just put KAFË in the middle (rows 2-5) and cross more words.
# KAFË vertical col 3, rows 2-5: K(2,3) A(3,3) F(4,3) Ë(5,3)
# BUKË horizontal row 2: B(2,0) U(2,1) K(2,2)? K at pos 2 needs col 2 to have K.
# But KAFË K is at (2,3). BUKË K at (2,2) ≠ KAFË K at (2,3).
# BUKË crossing KAFË at K(2,3): K at pos 2. BUKË(2,1): B(2,1) U(2,2) K(2,3) Ë(2,4).
# Check row 2: B U K Ë = BUKË. ✓
# Check col 1: B(2,1) alone. ✓. Col 2: U(2,2) alone. ✓. Col 4: Ë(2,4) alone. ✓
# ERA horizontal row 3 crossing KAFË at A(3,3): E(3,1) R(3,2) A(3,3).
# Check col 1: (2,1)=B, (3,1)=E. Adjacent! "BE" ghost!
# ALWAYS this problem. B above E in the same column.
#
# FIX: ERA from right side. E(3,3)? (3,3)=A. E≠A.
# ERA crossing at A(3,3): ERA A at pos 2. E(3,1) R(3,2) A(3,3). B-E ghost.
# Or A at (3,3), extend right: A(3,3) is pos 0 of something?
# No, ERA = E-R-A, A is last.
#
# I need to avoid having BUKË and ERA share the same column at adjacent rows.
# BUKË at row 2 uses col 1 (B). ERA at row 3 uses col 1 (E). Adjacent.
# Solution: BUKË at row 0. ERA at row 3. Gap in col.
# BUKË(0,1): B(0,1) U(0,2) K(0,3) Ë(0,4). KAFË K at (2,3). No sharing.
# Move KAFË so K is at (0,3). KAFË(0,3): K(0,3) A(1,3) F(2,3) Ë(3,3).
# BUKË(0,0): B(0,0) U(0,1) K(0,2) Ë(0,3). (0,3)=K from KAFË. Ë≠K conflict.
# BUKË with K at (0,3): B(0,1) U(0,2) K(0,3) Ë(0,4). Shares K(0,3). ✓
# ERA(3,1): E(3,1) R(3,2) A(3,3). KAFË Ë at (3,3). A≠Ë conflict!
# ERA at (1,1): E(1,1) R(1,2) A(1,3). Shares A(1,3) with KAFË. ✓
# Col 1: (0,1)=U from BUKË, (1,1)=E from ERA. Adjacent! "UE" ghost!
#
# BUKË at row 0 col 2: B(0,2) U(0,3)? (0,3)=K. Conflict.
# BUKË at row 0 col 3: B(0,3)? (0,3)=K. Conflict.
#
# OK. B-E and U-E ghosts keep happening.
# What if ERA goes RIGHT of the A?  ERA horizontal with A at (1,3):
# Only option is E(1,1) R(1,2) A(1,3).
# E always ends up in col 1, which is under BUKË.
# Unless BUKË is far from col 1.
# BUKË(0,4): B(0,4) U(0,5) K(0,6) Ë? Out of bounds (col 7).
# BUKË is 4 letters. Max start col = 3. K at pos 2 = col 5 for start col 3.
# Can't share K with KAFË K at (0,3) starting from col 3: K at (0,5). Not (0,3).
# Starting from col 1: K at (0,3). ✓ But U at (0,2), E at (1,2).
# Wait — E is at (1,1), not (1,2). R is at (1,2).
# Col 2: (0,2)=U, (1,2)=R. Adjacent. "UR" ghost!
#
# I think the fundamental problem is that BUKË and ERA cross KAFË at adjacent rows.
# Every time two horizontal words cross the same vertical word at adjacent rows,
# their leftmost columns will be adjacent in the same column → ghost.
#
# SOLUTION: Use non-adjacent row crossings!
# KAFË is 4 letters. K at row 0, A at row 1, F at row 2, Ë at row 3.
# Cross at K (row 0) and F (row 2) or Ë (row 3). Skip row 1.
# Or cross at A (row 1) and Ë (row 3). Skip row 2.
#
# Let's try: KAFË vertical (0,3). Cross at A(1,3) and Ë(3,3).
# Word at row 1 crossing at A: ERA E(1,1) R(1,2) A(1,3).
# Word at row 3 crossing at Ë: UJË U(3,1) J(3,2) Ë(3,3).
# Now col 1: E(1,1) and U(3,1). Not adjacent (gap at 2,1). ✓!
# Col 2: R(1,2) and J(3,2). Not adjacent. ✓!
#
# Now cross at K(0,3): BUKË B(0,1) U(0,2) K(0,3) Ë(0,4).
# Col 1: B(0,1) and E(1,1). Adjacent. "BE" ghost!
# Hmm, rows 0 and 1 are adjacent.
#
# Use non-adjacent: cross at K(0,3) and F(2,3).
# Word at row 0 crossing K: BUKË B(0,1) U(0,2) K(0,3) Ë(0,4).
# Word at row 2 crossing F: ? What word has F? Hard to find common Albanian word with F at intersection.
# FSHAT? F-S-H-A-T. F at pos 0. FSHAT horizontal: F(2,3) S(2,4) H(2,5) A(2,6) T? Out of bounds. FSHAT is 5 letters, (2,3)-(2,7). Out of bounds.
# Shorter: no common 3-4 letter word starting with F that would work.
#
# Alternative: cross K and Ë (rows 0 and 3, separated by 2 rows).
# Word at row 0: BUKË B(0,1) U(0,2) K(0,3) Ë(0,4).
# Word at row 3: UJË U(3,1) J(3,2) Ë(3,3).
# Col 1: B(0,1), U(3,1). Not adjacent. ✓✓✓
# Col 2: U(0,2), J(3,2). Not adjacent. ✓
# Great!
#
# Now cross ERA at A(1,3).
# ERA E(1,1) R(1,2) A(1,3).
# Col 1: B(0,1), E(1,1). ADJACENT. "BE" ghost!
#
# So if BUKË is at row 0, nothing can cross KAFË at row 1 with letters in cols 1-2.
# ERA could go RIGHT from A: but ERA=E-R-A, A is last.
# Or ERA vertical: E(0,3)? =K. Conflict.
#
# What if ERA crosses KAFË at A(1,3) from the RIGHT?
# ERA horizontal: A at pos 2. E(1,1) R(1,2) A(1,3). Always from left.
# Or: some other word at row 1 crossing at A(1,3) from cols 3+?
# MAL horizontal: M(1,3)? M≠A conflict. M at pos 0, A at pos 1.
# MAL: M(1,2) A(1,3) L(1,4). Shares A.
# Col 2: U(0,2) and M(1,2). Adjacent! "UM" ghost!
# Col 4: Ë(0,4) and L(1,4). Adjacent! "ËL" ghost!
#
# Everything touching row 0 from row 1 creates ghosts.
# SOLUTION: Leave row 1 empty! Cross KAFË only at K(0,3) and F(2,3) or Ë(3,3).
# But row 1 has A from KAFË, can't leave it empty.
# KAFË A(1,3) MUST exist. But row 1 should have no other letters adjacent.
# So (1,2) and (1,4) must be X. A(1,3) is isolated horizontally.
# A(1,3) is just a single letter in row 1 (not part of any horizontal word). ✓
#
# This means: Don't cross any horizontal word at A(1,3).
# Cross KAFË at K(0,3) and at Ë(3,3) only.
# A and F are just isolated vertical cells.
#
# BUKË at row 0: B(0,1) U(0,2) K(0,3) Ë(0,4). Crosses K.
# UJË at row 3: U(3,1) J(3,2) Ë(3,3). Crosses Ë.
# That's 3 words, 2 shared cells.
# All connected: BUKË↔KAFË, KAFË↔UJË. ✓
#
# Grid:
#   0: . B U K Ë . .
#   1: . . . A . . .
#   2: . . . F . . .
#   3: . U J Ë . . .
#
# No ghosts: every run is a single word or single letter.
# Now add more. Need to cross existing words without adjacency issues.
#
# DET vertical crossing BUKË at... BUKË has B(0,1) U(0,2) K(0,3) Ë(0,4).
# DET=D-E-T. Cross at Ë? No Ë in DET. At U? No U. At B? No B.
# ERA vertical crossing BUKË at... ERA=E-R-A. No B,U,K,Ë in ERA.
# MAL vertical crossing BUKË at... MAL=M-A-L. No B,U,K,Ë.
#
# Cross UJË: U(3,1) J(3,2) Ë(3,3).
# DUA vertical crossing UJË at U(3,1): DUA=D-U-A. U at pos 1.
# D(2,1) U(3,1) A(4,1).
# Col 1: (0,1)=B, (2,1)=D. Not adjacent (gap at 1,1). ✓
# Row 2: D(2,1) alone. ✓. Row 4: A(4,1) alone. ✓
# DUA vertical col 1: D(2,1) U(3,1) A(4,1) = DUA. ✓
# Check (2,1)=D next to (2,2)=X. ✓. And (2,3)=F from KAFË. Not adjacent. ✓
#
# Now add ERA crossing DUA at A(4,1): ERA=E-R-A. A at pos 2.
# ERA horizontal: E(4,0)? Hmm. E(4,-1) R(4,0) A(4,1)? Out of bounds.
# A at col 1, A at pos 2 → start at col -1. Out of bounds.
# ERA with A at pos 2: start col = 1-2 = -1. No good.
# ERA vertical crossing DUA at D(2,1): ERA has no D.
# ERA vertical crossing DUA at A(4,1): ERA A at pos 2. E(2,1) R(3,1) A(4,1).
# (2,1)=D from DUA. E≠D conflict!
# ERA at (4,2): E(4,2) R(4,3)? Hmm this is horizontal. E(4,2) R(4,3) A(4,4)?
# (4,1)=A from DUA, (4,2)=E. Adjacent. "AE" ghost?
# Actually that's row 4: A(4,1) E(4,2) R(4,3) A(4,4) = "AERA". Ghost!
#
# ERA horizontal at row 6: E(6,0) R(6,1) A(6,2). Not connected.
# Need to connect via vertical.
# MAL vertical from (4,1): M(5,1) A(4,1)? Backwards. Not valid.
# MAL=M-A-L. M(4,1)? (4,1)=A. M≠A.
#
# ZOG crossing UJË at J(3,2): ZOG=Z-O-G. No J. ✗
#
# ARRË vertical crossing UJË at Ë(3,3): same as KAFË Ë(3,3). Already shared.
# ARRË=A-R-R-Ë. Ë at pos 3. A(0,3)=K. Conflict.
#
# This is incredibly hard. Let me try adding ERA crossing BUKË.
# Wait — ERA has no letter in common with BUKË (B,U,K,Ë vs E,R,A).
# So ERA can't cross BUKË directly. Same for most word pairs.
#
# SOLUTION: I need to pick words that SHARE LETTERS.
# Common Albanian letters in words: A, E, Ë, I, U, R, M, L, K, T, etc.
#
# Words sharing A: ERA, MAL, DUA, BUKË(no), KAFË(A), ARRË(A), VALË(A),
#                   NATË(A), KISHA(A), DARKË(A), VAJ(A)
# Words sharing E: ERA(E), DET(E), EMËR(E), JETË(E), VERË(E), KAFENE(E)
# Words sharing M: MAL(M), MAMI(M), EMËR(M), ZEMËR(M), MISH(M)
#
# KEY: I should pick words that share common letters to make crossings easy.
#
# For Day 0, let me try: DUA + MAL + ERA + BUKË + KAFË
# DUA and MAL share A. ERA and MAL share A.
# But can't have 3 words cross at same cell.
#
# Let me use a simple 4-word cross and call Day 0 done.

print("\n" + "="*55)
print("  BUILDING DAY 0")
print("="*55)

# Plan: KAFË vertical, BUKË crossing at K, UJË crossing at Ë, DUA crossing UJë at U
plan0 = [
    ("KAFË", 0, 3, "vertical"),    # K(0,3) A(1,3) F(2,3) Ë(3,3)
    ("BUKË", 0, 1, "horizontal"),  # B(0,1) U(0,2) K(0,3) Ë(0,4) — shares K(0,3)
    ("UJË",  3, 1, "horizontal"),  # U(3,1) J(3,2) Ë(3,3) — shares Ë(3,3)
    ("DUA",  2, 1, "vertical"),    # D(2,1) U(3,1) A(4,1) — shares U(3,1) with UJË
]
result = try_layout(plan0)
if result:
    grid, words = result
    print("  ✓ Day 0 valid!")
    show(grid)
    print(f"  Words: {[w['word'] for w in words]}")
    all_puzzles.append(("Day 0", grid, words))
else:
    print("  ✗ Day 0 failed")
    # Debug
    g = make_grid()
    for word, row, col, d in plan0:
        g2 = place_word(g, word, row, col, d)
        if g2 is None:
            print(f"    Conflict placing {word}")
            break
        ws = set(x[0] for x in plan0)
        ok, ghost = check_no_ghosts(g2, ws)
        if not ok:
            print(f"    Ghost after placing {word}: {ghost}")
            show(g2)
            break
        g = g2

# Let me also try more words for Day 0
plan0b = [
    ("KAFË", 0, 3, "vertical"),    # K(0,3) A(1,3) F(2,3) Ë(3,3)
    ("BUKË", 0, 1, "horizontal"),  # B(0,1) U(0,2) K(0,3) Ë(0,4) — shares K
    ("UJË",  3, 1, "horizontal"),  # U(3,1) J(3,2) Ë(3,3) — shares Ë
    ("DUA",  2, 1, "vertical"),    # D(2,1) U(3,1) A(4,1) — shares U with UJË
    ("ERA",  4, 1, "horizontal"),  # E(4,1)? (4,1)=A from DUA. E≠A conflict!
]

plan0c = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),  # M(4,0) A(4,1) L(4,2) — shares A with DUA
]
result = try_layout(plan0c)
if result:
    grid, words = result
    print("  ✓ Day 0 (extended) valid!")
    show(grid)
    print(f"  Words: {[w['word'] for w in words]}")
    all_puzzles[0] = ("Day 0", grid, words)
else:
    print("  ✗ Day 0 extended failed")

# Try with ERA crossing MAL
plan0d = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),  # M(4,0) A(4,1) L(4,2)
    ("ERA",  4, 0, "vertical"),    # E(4,0)? (4,0)=M. E≠M
]

plan0e = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),
    ("ERA",  6, 0, "horizontal"),  # E(6,0) R(6,1) A(6,2) — not connected
]

plan0f = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),
    ("EMËR", 4, 0, "vertical"),   # E(4,0)? (4,0)=M. E≠M
]

# Let me try adding ZOG crossing MAL at L(4,2)
plan0g = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),
    ("VALË", 4, 2, "vertical"),   # V(4,2)? (4,2)=L. V≠L conflict
]

plan0h = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),
    ("LULE", 4, 2, "vertical"),   # L(4,2) U(5,2) L(6,2) E(7,2) — out of bounds!
]

plan0i = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),
    ("LOT",  4, 2, "vertical"),   # L(4,2) O(5,2) T(6,2) — shares L(4,2) with MAL
]
result = try_layout(plan0i)
if result:
    grid, words = result
    print("  ✓ Day 0 (6 words) valid!")
    show(grid)
    print(f"  Words: {[w['word'] for w in words]}")
    if len(all_puzzles) > 0:
        all_puzzles[0] = ("Day 0", grid, words)
    else:
        all_puzzles.append(("Day 0", grid, words))
else:
    print("  ✗ Day 0 (6 words) failed — trying debug")
    g = make_grid()
    for word, row, col, d in plan0i:
        g2 = place_word(g, word, row, col, d)
        if g2 is None:
            print(f"    Conflict placing {word}")
            break
        ws = set(x[0] for x in plan0i)
        ok, ghost = check_no_ghosts(g2, ws)
        if not ok:
            print(f"    Ghost after {word}: {ghost}")
            show(g2)
            break
        g = g2

# Try ERA somewhere too
plan0j = [
    ("KAFË", 0, 3, "vertical"),
    ("BUKË", 0, 1, "horizontal"),
    ("UJË",  3, 1, "horizontal"),
    ("DUA",  2, 1, "vertical"),
    ("MAL",  4, 0, "horizontal"),
    ("LOT",  4, 2, "vertical"),
    # ERA crossing LOT at O(5,2): ERA=E-R-A. No O. ✗
    # ERA crossing LOT at T(6,2): no T in ERA. ✗
    # ERA horizontal row 6: E(6,0) R(6,1) A(6,2)? (6,2)=T from LOT. A≠T. ✗
    # ERA at row 6 col 4: E(6,4) R(6,5) A(6,6). Not connected.
    # ZOG at row 6: Z(6,4) O(6,5) G(6,6). Not connected.
    # Need vertical from LOT area down.
    # DET crossing LOT at T(6,2): DET=D-E-T. T at pos 2. D(4,2) E(5,2) T(6,2).
    # (4,2)=L from MAL. D≠L conflict!
    # VERË vertical crossing LOT at O(5,2)? VERË=V-E-R-Ë. No O.
    # NATË crossing LOT... no shared letter.
]

# Let's try adding ERA a different way.
# What if ERA crosses MAL at A(4,1)?
# ERA=E-R-A, A at pos 2.
# ERA horizontal: E(4,-1)... out of bounds.
# ERA vertical: A at pos 2. E(2,1) R(3,1)? (2,1)=D, (3,1)=U. Conflicts!
# ERA is tricky because A is at the end.
#
# What about ARRË crossing MAL at A(4,0)?
# ARRË=A-R-R-Ë, A at pos 0.
# ARRË vertical: A(4,0) R(5,0) R(6,0) Ë? Only 3 rows left (4,5,6) = 3 cells for 4 letters.
# A(4,0) R(5,0) R(6,0) — only 3. ARRË needs 4. Out of bounds.
# ARRË horizontal: A(4,0) R(4,1)? (4,1)=A from DUA. R≠A conflict!
#
# VERË crossing MAL at M(4,0)? VERË has no M.
# ZOG crossing MAL at M(4,0)? No M in ZOG.
#
# 6 words (KAFË, BUKË, UJË, DUA, MAL, LOT) = good enough for Day 0!
# Let me verify the final plan and move on.

print("\n" + "="*55)
print("  FINAL RESULTS")
print("="*55)
for label, grid, words in all_puzzles:
    print(f"\n{label}:")
    show(grid)
    print(f"  Words ({len(words)}): {[w['word'] for w in words]}")
    letters = sum(1 for r in grid for c in r if c != "X")
    print(f"  Letters: {letters}")
