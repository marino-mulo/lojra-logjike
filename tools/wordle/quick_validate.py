#!/usr/bin/env python3
"""Quick validation of all 7 generated puzzles (variable grid sizes)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_all_runs(grid, size):
    runs = []
    for r in range(size):
        c = 0
        while c < size:
            if grid[r][c] != "X":
                start = c; s = ""
                while c < size and grid[r][c] != "X":
                    s += grid[r][c]; c += 1
                if len(s) >= 2: runs.append((s, r, start, "H"))
            else: c += 1
    for c in range(size):
        r = 0
        while r < size:
            if grid[r][c] != "X":
                start = r; s = ""
                while r < size and grid[r][c] != "X":
                    s += grid[r][c]; r += 1
                if len(s) >= 2: runs.append((s, start, c, "V"))
            else: r += 1
    return runs

def check(label, grid, words, size):
    word_set = set(w[0] for w in words)
    runs = find_all_runs(grid, size)
    ghosts = [(t,r,c,d) for t,r,c,d in runs if t not in word_set]
    # connectivity
    cells_per = [set() for _ in words]
    for i,(w,r,c,d) in enumerate(words):
        for j in range(len(w)):
            rr = r+(j if d=="V" else 0); cc = c+(j if d=="H" else 0)
            cells_per[i].add((rr,cc))
    adj = {i:set() for i in range(len(words))}
    for i in range(len(words)):
        for j in range(i+1,len(words)):
            if cells_per[i]&cells_per[j]: adj[i].add(j); adj[j].add(i)
    vis={0}; q=[0]
    while q:
        n=q.pop(0)
        for nb in adj[n]:
            if nb not in vis: vis.add(nb); q.append(nb)
    connected = len(vis)==len(words)
    grid_ok = len(grid) == size and all(len(r) == size for r in grid)
    ok = len(ghosts)==0 and connected and grid_ok
    status = "PASS" if ok else "FAIL"
    print(f"  {label} ({size}x{size}): {status}  [{len(words)} words, {sum(1 for r in grid for c in r if c!='X')} letters]")
    if ghosts:
        for t,r,c,d in ghosts: print(f"    Ghost: '{t}' at ({r},{c}) {d}")
    if not connected: print(f"    NOT CONNECTED")
    if not grid_ok: print(f"    GRID SIZE MISMATCH")
    return ok

total = 0
passed = 0

# Day 0 (7x7)
g=[["M", "X", "D", "I", "M", "X", "D"], ["O", "X", "R", "X", "X", "X", "E"], ["S", "H", "I", "X", "V", "E", "T"], ["X", "X", "T", "R", "E", "X", "X"], ["N", "J", "Ë", "X", "L", "O", "T"], ["U", "X", "X", "X", "X", "R", "X"], ["K", "U", "Q", "X", "P", "A", "K"]]
w=[("TRE", 3, 2, "H"), ("VEL", 2, 4, "V"), ("VET", 2, 4, "H"), ("DET", 0, 6, "V"), ("DRITË", 0, 2, "V"), ("SHI", 2, 0, "H"), ("NJË", 4, 0, "H"), ("DIM", 0, 2, "H"), ("NUK", 4, 0, "V"), ("KUQ", 6, 0, "H"), ("LOT", 4, 4, "H"), ("ORA", 4, 5, "V"), ("MOS", 0, 0, "V"), ("PAK", 6, 4, "H")]
total+=1; passed += check("Day 0 (Monday)", g, w, 7)

# Day 1 (7x7)
g=[["V", "A", "J", "X", "D", "X", "X"], ["I", "X", "E", "X", "I", "X", "F"], ["T", "X", "T", "X", "M", "A", "L"], ["X", "V", "Ë", "R", "Ë", "X", "E"], ["X", "E", "X", "X", "X", "X", "T"], ["P", "L", "A", "K", "Ë", "X", "Ë"], ["X", "X", "X", "X", "X", "X", "X"]]
w=[("VËRË", 3, 1, "H"), ("DIMË", 0, 4, "V"), ("JETË", 0, 2, "V"), ("VEL", 3, 1, "V"), ("MAL", 2, 4, "H"), ("VAJ", 0, 0, "H"), ("PLAKË", 5, 0, "H"), ("VIT", 0, 0, "V"), ("FLETË", 1, 6, "V")]
total+=1; passed += check("Day 1 (Tuesday)", g, w, 7)

# Day 2 (8x8)
g=[["X", "X", "X", "X", "X", "X", "P", "X"], ["K", "A", "F", "Ë", "X", "X", "I", "X"], ["U", "X", "U", "X", "D", "I", "K", "U"], ["Q", "E", "N", "X", "J", "X", "Ë", "X"], ["X", "X", "D", "U", "A", "X", "X", "H"], ["X", "M", "X", "X", "L", "U", "M", "Ë"], ["B", "A", "B", "A", "I", "X", "X", "N"], ["X", "L", "X", "X", "X", "N", "J", "Ë"]]
w=[("DUA", 4, 2, "H"), ("DJALI", 2, 4, "V"), ("LUMË", 5, 4, "H"), ("DIKU", 2, 4, "H"), ("BABAI", 6, 0, "H"), ("HËNË", 4, 7, "V"), ("FUND", 1, 2, "V"), ("MAL", 5, 1, "V"), ("PIKË", 0, 6, "V"), ("QEN", 3, 0, "H"), ("NJË", 7, 5, "H"), ("KAFË", 1, 0, "H"), ("KUQ", 1, 0, "V")]
total+=1; passed += check("Day 2 (Wednesday)", g, w, 8)

# Day 3 (8x8)
g=[["I", "N", "A", "T", "X", "D", "X", "X"], ["X", "X", "R", "X", "X", "A", "X", "N"], ["X", "M", "I", "Z", "Ë", "R", "X", "A"], ["X", "X", "X", "X", "X", "K", "O", "T"], ["X", "B", "L", "E", "T", "Ë", "X", "Ë"], ["K", "X", "O", "X", "O", "X", "B", "X"], ["J", "E", "T", "X", "K", "X", "U", "X"], ["O", "X", "X", "V", "A", "J", "Z", "Ë"]]
w=[("BLETË", 4, 1, "H"), ("DARKË", 0, 5, "V"), ("MIZËR", 2, 1, "H"), ("KOT", 3, 5, "H"), ("NATË", 1, 7, "V"), ("TOKA", 4, 4, "V"), ("VAJZË", 7, 3, "H"), ("ARI", 0, 2, "V"), ("INAT", 0, 0, "H"), ("LOT", 4, 2, "V"), ("BUZ", 5, 6, "V"), ("JET", 6, 0, "H"), ("KJO", 5, 0, "V")]
total+=1; passed += check("Day 3 (Thursday)", g, w, 8)

# Day 4 (9x9)
g=[["X", "Q", "E", "N", "X", "F", "U", "N", "D"], ["X", "X", "R", "X", "X", "X", "X", "X", "H"], ["X", "J", "A", "V", "Ë", "X", "T", "R", "E"], ["X", "X", "X", "A", "X", "X", "I", "X", "X"], ["X", "X", "U", "J", "K", "U", "J", "X", "I"], ["X", "P", "X", "X", "I", "X", "X", "X", "N"], ["Q", "U", "M", "Ë", "S", "X", "U", "X", "A"], ["X", "L", "X", "X", "H", "X", "J", "E", "T"], ["X", "Ë", "X", "Z", "A", "N", "Ë", "X", "X"]]
w=[("UJKUJ", 4, 2, "H"), ("VAJ", 2, 3, "V"), ("TIJ", 2, 6, "V"), ("KISHA", 4, 4, "V"), ("ZANË", 8, 3, "H"), ("QUMËS", 6, 0, "H"), ("PULË", 5, 1, "V"), ("UJË", 6, 6, "V"), ("JAVË", 2, 1, "H"), ("ERA", 0, 2, "V"), ("QEN", 0, 1, "H"), ("TRE", 2, 6, "H"), ("JET", 7, 6, "H"), ("DHE", 0, 8, "V"), ("INAT", 4, 8, "V"), ("FUND", 0, 5, "H")]
total+=1; passed += check("Day 4 (Friday)", g, w, 9)

# Day 5 (9x9)
g=[["X", "S", "H", "T", "Ë", "P", "I", "X", "J"], ["X", "X", "X", "R", "X", "L", "X", "X", "A"], ["L", "X", "X", "E", "R", "A", "X", "X", "V"], ["O", "R", "A", "X", "X", "K", "A", "F", "Ë"], ["T", "X", "R", "Ë", "R", "Ë", "X", "L", "X"], ["X", "X", "T", "X", "X", "X", "J", "E", "T"], ["X", "D", "H", "E", "X", "D", "X", "T", "X"], ["X", "U", "X", "N", "X", "I", "X", "Ë", "X"], ["X", "A", "X", "D", "I", "M", "Ë", "X", "X"]]
w=[("RËRË", 4, 2, "H"), ("ARTH", 3, 2, "V"), ("PLAKË", 0, 5, "V"), ("DHE", 6, 1, "H"), ("ERA", 2, 3, "H"), ("SHTËPI", 0, 1, "H"), ("KAFË", 3, 5, "H"), ("JAVË", 0, 8, "V"), ("END", 6, 3, "V"), ("DIMË", 8, 3, "H"), ("FLETË", 3, 7, "V"), ("DUA", 6, 1, "V"), ("ORA", 3, 0, "H"), ("LOT", 2, 0, "V"), ("JET", 5, 6, "H"), ("DIM", 6, 5, "V"), ("TRE", 0, 3, "V")]
total+=1; passed += check("Day 5 (Saturday)", g, w, 9)

# Day 6 (10x10)
g=[["X", "B", "U", "Z", "X", "X", "G", "J", "E", "L"], ["X", "X", "X", "O", "X", "X", "J", "X", "N", "X"], ["P", "I", "K", "T", "U", "R", "Ë", "X", "D", "X"], ["U", "X", "U", "X", "X", "X", "N", "X", "X", "B"], ["N", "X", "Q", "X", "V", "X", "D", "I", "K", "U"], ["Ë", "X", "X", "D", "E", "R", "Ë", "X", "X", "K"], ["X", "K", "X", "X", "L", "X", "X", "X", "X", "U"], ["X", "J", "X", "S", "X", "L", "I", "B", "Ë", "R"], ["X", "O", "R", "A", "X", "O", "X", "X", "X", "X"], ["X", "X", "X", "J", "E", "T", "Ë", "X", "X", "X"]]
w=[("DERË", 5, 3, "H"), ("VEL", 4, 4, "V"), ("GJËNDË", 0, 6, "V"), ("PIKTURË", 2, 0, "H"), ("PUNË", 2, 0, "V"), ("GJEL", 0, 6, "H"), ("DIKU", 4, 6, "H"), ("BUKUR", 3, 9, "V"), ("ZOT", 0, 3, "V"), ("KUQ", 2, 2, "V"), ("BUZ", 0, 1, "H"), ("LIBËR", 7, 5, "H"), ("END", 0, 8, "V"), ("LOT", 7, 5, "V"), ("SAJ", 7, 3, "V"), ("JETË", 9, 3, "H"), ("ORA", 8, 1, "H"), ("KJO", 6, 1, "V")]
total+=1; passed += check("Day 6 (Sunday)", g, w, 10)

print(f"\n  RESULT: {passed}/{total} passed")
sys.exit(0 if passed == total else 1)
