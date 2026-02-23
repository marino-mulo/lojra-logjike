"""Verify Zip puzzles: adjacency, wall respect, Hamiltonian, checkpoints in order."""

def verify_puzzle(name, rows, cols, path, checkpoints, walls):
    """
    path: list of cell indices
    checkpoints: dict {cell_index: checkpoint_number}
    walls: list of [r1,c1,r2,c2]
    """
    errors = []
    total = rows * cols

    # Check path length
    if len(path) != total:
        errors.append(f"Path length {len(path)} != grid size {total}")

    # Check no repeats
    if len(set(path)) != len(path):
        seen = set()
        for i, c in enumerate(path):
            if c in seen:
                errors.append(f"Cell {c} repeated at step {i}")
            seen.add(c)

    # Check all cells visited
    all_cells = set(range(total))
    visited = set(path)
    missing = all_cells - visited
    if missing:
        errors.append(f"Missing cells: {sorted(missing)}")

    # Build wall set
    wall_set = set()
    for w in walls:
        r1, c1, r2, c2 = w
        idx1 = r1 * cols + c1
        idx2 = r2 * cols + c2
        wall_set.add((min(idx1, idx2), max(idx1, idx2)))

    # Check adjacency and walls
    for i in range(len(path) - 1):
        c1 = path[i]
        c2 = path[i + 1]
        r1, co1 = divmod(c1, cols)
        r2, co2 = divmod(c2, cols)
        dist = abs(r1 - r2) + abs(co1 - co2)
        if dist != 1:
            errors.append(f"Step {i}: cell {c1}({r1},{co1}) -> cell {c2}({r2},{co2}) not adjacent (dist={dist})")
        # Check wall
        pair = (min(c1, c2), max(c1, c2))
        if pair in wall_set:
            errors.append(f"Step {i}: cell {c1} -> cell {c2} crosses wall")

    # Check checkpoints in order
    max_cp = max(checkpoints.values())
    cp_positions = {}
    for cell, num in checkpoints.items():
        cp_positions[num] = cell

    for cp_num in sorted(cp_positions.keys()):
        cell = cp_positions[cp_num]
        if cell not in visited:
            errors.append(f"Checkpoint {cp_num} at cell {cell} not in path")

    # Check path starts at checkpoint 1
    if path[0] != cp_positions[1]:
        errors.append(f"Path starts at {path[0]} but checkpoint 1 is at {cp_positions[1]}")

    # Check path ends at last checkpoint
    if path[-1] != cp_positions[max_cp]:
        errors.append(f"Path ends at {path[-1]} but last checkpoint {max_cp} is at {cp_positions[max_cp]}")

    # Check checkpoints are visited in order
    cp_order = []
    for cell in path:
        if cell in checkpoints:
            cp_order.append(checkpoints[cell])

    expected = sorted(checkpoints.values())
    if cp_order != expected:
        errors.append(f"Checkpoints visited in order {cp_order}, expected {expected}")

    # Parity check for even grids
    if (rows * cols) % 2 == 0:
        start_r, start_c = divmod(path[0], cols)
        end_r, end_c = divmod(path[-1], cols)
        start_parity = (start_r + start_c) % 2
        end_parity = (end_r + end_c) % 2
        if start_parity == end_parity:
            errors.append(f"Even grid: start parity {start_parity} == end parity {end_parity} (must differ)")

    if errors:
        print(f"FAIL {name}:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"OK {name} ({rows}x{cols}, {len(path)} cells, {len(checkpoints)} checkpoints, {len(walls)} walls)")
        return True


# ═══════════════════════════════════════════
# MONDAY - 5x5, 7 checkpoints, 0 walls
# ═══════════════════════════════════════════
# Grid layout (row, col):
# (0,0)=0  (0,1)=1  (0,2)=2  (0,3)=3  (0,4)=4
# (1,0)=5  (1,1)=6  (1,2)=7  (1,3)=8  (1,4)=9
# (2,0)=10 (2,1)=11 (2,2)=12 (2,3)=13 (2,4)=14
# (3,0)=15 (3,1)=16 (3,2)=17 (3,3)=18 (3,4)=19
# (4,0)=20 (4,1)=21 (4,2)=22 (4,3)=23 (4,4)=24
#
# Path design - NOT a serpentine. Has a spiral-like quality:
# Start at (0,0), go right to (0,2), drop down, sweep left, up, right, down...
#
# Path:
# (0,0) -> (0,1) -> (0,2) -> (1,2) -> (1,1) -> (1,0) -> (2,0) -> (2,1) -> (2,2) -> (2,3) -> (2,4) -> (1,3) -> (1,4) -> (0,3) -> (0,4) -> ... need to get to row 3,4
# Hmm, (0,4) only connects to (1,4) which is visited. Dead end.
#
# Let me try:
# (0,0) -> (1,0) -> (2,0) -> (2,1) -> (1,1) -> (0,1) -> (0,2) -> (0,3) -> (0,4) -> (1,4) -> (1,3) -> (1,2) -> (2,2) -> (2,3) -> (2,4) -> (3,4) -> (3,3) -> (3,2) -> (3,1) -> (3,0) -> (4,0) -> (4,1) -> (4,2) -> (4,3) -> (4,4)
# = 0,5,10,11,6,1,2,3,4,9,8,7,12,13,14,19,18,17,16,15,20,21,22,23,24
# Checkpoints at: 0=1, 11=2(interior!), 1=3, 9=4, 12=5(interior!), 15=6, 24=7

monday_path = [0,5,10,11,6,1,2,3,4,9,8,7,12,13,14,19,18,17,16,15,20,21,22,23,24]
monday_checkpoints = {0:1, 11:2, 1:3, 9:4, 12:5, 15:6, 24:7}
monday_walls = []

verify_puzzle("Monday", 5, 5, monday_path, monday_checkpoints, monday_walls)

# ═══════════════════════════════════════════
# TUESDAY - 6x6, 8 checkpoints, 2 walls
# ═══════════════════════════════════════════
# Grid: 6x6 = 36 cells
# (0,0)=0  (0,1)=1  (0,2)=2  (0,3)=3  (0,4)=4  (0,5)=5
# (1,0)=6  (1,1)=7  (1,2)=8  (1,3)=9  (1,4)=10 (1,5)=11
# (2,0)=12 (2,1)=13 (2,2)=14 (2,3)=15 (2,4)=16 (2,5)=17
# (3,0)=18 (3,1)=19 (3,2)=20 (3,3)=21 (3,4)=22 (3,5)=23
# (4,0)=24 (4,1)=25 (4,2)=26 (4,3)=27 (4,4)=28 (4,5)=29
# (5,0)=30 (5,1)=31 (5,2)=32 (5,3)=33 (5,4)=34 (5,5)=35
#
# Even grid: start and end must differ in parity.
# (0,0) parity = 0 (even). End must be parity 1 (odd) = odd sum of (r+c).
# e.g. (5,0)=1, (0,5)=1, (3,2)=1, (2,3)=1, etc.
#
# Walls: 2 walls
# Wall between (1,3) and (2,3): blocks cell 9<->15
# Wall between (3,1) and (3,2): blocks cell 19<->20
#
# Path design with twists:
# Start (0,0)=0 -> (0,1)=1 -> (0,2)=2 -> (0,3)=3 -> (0,4)=4 -> (0,5)=5
# -> (1,5)=11 -> (1,4)=10 -> (1,3)=9 -> (1,2)=8 -> (1,1)=7 -> (1,0)=6
# -> (2,0)=12 -> (2,1)=13 -> (2,2)=14 -> (2,3)=15 -> (2,4)=16 -> (2,5)=17
# -> (3,5)=23 -> (3,4)=22 -> (3,3)=21 -> (3,2)=20 -> (3,1)=19 -> (3,0)=18
# -> (4,0)=24 -> (4,1)=25 -> (4,2)=26 -> (4,3)=27 -> (4,4)=28 -> (4,5)=29
# -> (5,5)=35 -> (5,4)=34 -> (5,3)=33 -> (5,2)=32 -> (5,1)=31 -> (5,0)=30
# That's a pure serpentine... walls don't affect it. Not good enough.
#
# Let me design a more interesting path:
# Start (2,3)=15 -> ... end must be even parity like (0,0)=0 or (4,4)=0
# Actually let me think differently. Start at interior cell.
#
# Start (1,2)=8, parity=(1+2)%2=1. End must be parity 0.
#
# Let me try a path that spirals and uses the walls:
# Wall 1: between (1,2) and (2,2) = cells 8 and 14
# Wall 2: between (3,3) and (4,3) = cells 21 and 27
#
# Start at (0,0)=0, parity 0. End must be parity 1.
# End at (2,3)=15, parity 1.
#
# Path:
# 0(0,0)->6(1,0)->12(2,0)->13(2,1)->14(2,2)->15(2,3)->16(2,4)->17(2,5)->
# 11(1,5)->10(1,4)->9(1,3)->8(1,2)->7(1,1)->1(0,1)->2(0,2)->3(0,3)->4(0,4)->5(0,5)->
# Wait, from 7(1,1) can I go to 1(0,1)? Yes, adjacent.
# From 5(0,5) I need to get to row 3+. But 5(0,5)->11(1,5) already visited.
# Dead end.
#
# Let me try more carefully. I'll do a non-serpentine path.
#
# Start (0,0)=0
# 0->1->2->3->4->5->11->17->23->29->35->34->33->32->31->30->24->25->26->27->28->22->21->20->19->18->12->13->14->15->16->10->9->8->7->6
# Wait, from 16(2,4)->10(1,4)? Yes. 10->9? Yes. 9->8? Yes. 8->7? Yes. 7->6? (1,1)->(1,0) Yes.
# But wall between (1,2)=8 and (2,2)=14? In this path 14->15 not 8->14. Let me check.
# The path visits 14 after 13: 13(2,1)->14(2,2), that's fine, no wall issue.
# Actually I need to check: does the path cross any wall?
# Wall 1: (1,2)-(2,2) = cell 8 to cell 14. In the path, 8 appears at position 33, 14 at position 28. They aren't consecutive. Good.
# Wall 2: (3,3)-(4,3) = cell 21 to cell 27. In path, 21 at pos 22, 27 at pos 19. Not consecutive. Good.
#
# But this IS a pure serpentine (down right edge, back left edge, up...). Let me make it twistier.
#
# Let me try something with real detours:
# 0(0,0)->1(0,1)->7(1,1)->6(1,0)->12(2,0)->18(3,0)->19(3,1)->13(2,1)->14(2,2)->8(1,2)->2(0,2)->3(0,3)->9(1,3)->
# Wait, wall between (1,3)=9 and (2,3)=15. So 9 can't go to 15. That's fine if we don't go that way.
# 9(1,3)->10(1,4)->4(0,4)->5(0,5)->11(1,5)->17(2,5)->16(2,4)->15(2,3)->
# Can 15(2,3) go to 9(1,3)? Wall! But we're going FROM 16 to 15, not crossing the wall.
# 15(2,3)->21(3,3)->20(3,2)->26(4,2)->25(4,1)->24(4,0)->30(5,0)->31(5,1)->32(5,2)->33(5,3)->27(4,3)->
# Wait, wall between (3,3)=21 and (4,3)=27. So 21<->27 is blocked.
# But in this path, 33(5,3)->27(4,3)? Yes that's fine, no wall between those.
# 27(4,3)->28(4,4)->22(3,4)->23(3,5)->29(4,5)->35(5,5)->34(5,4)->
# Wait, 34 should be the 35th cell (index 34 = (5,4)). After 35 there's nothing...
# Let me count: we need all 36 cells.
# 0,1,7,6,12,18,19,13,14,8,2,3,9,10,4,5,11,17,16,15,21,20,26,25,24,30,31,32,33,27,28,22,23,29,35,34
# Count: 36 cells. Let me verify no repeats.
# {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35} = 36. Good!
#
# Check end: 34 = (5,4), parity = (5+4)%2 = 1. Start 0=(0,0) parity 0. Different. Good!
#
# Check adjacency step by step and walls:
# Wall 1: (1,3)-(2,3) = 9<->15 blocked
# Wall 2: (3,3)-(4,3) = 21<->27 blocked
#
# Adjacency check done in verify function.
#
# Checkpoints (8, mix of edge and interior):
# 0=1 (start, corner)
# 7=2 (interior, (1,1))
# 14=3 (interior, (2,2))
# 3=4 (edge, (0,3))
# 16=5 (interior, (2,4))
# 20=6 (interior, (3,2))
# 30=7 (edge, (5,0))
# 34=8 (edge, (5,4), end)

tuesday_path = [0,1,7,6,12,18,19,13,14,8,2,3,9,10,4,5,11,17,16,15,21,20,26,25,24,30,31,32,33,27,28,22,23,29,35,34]
tuesday_checkpoints = {0:1, 7:2, 14:3, 3:4, 16:5, 20:6, 30:7, 34:8}
tuesday_walls = [[1,3,2,3],[3,3,4,3]]

verify_puzzle("Tuesday", 6, 6, tuesday_path, tuesday_checkpoints, tuesday_walls)


# ═══════════════════════════════════════════
# WEDNESDAY - 6x6, 9 checkpoints, 3 walls
# ═══════════════════════════════════════════
# Even grid: start/end different parity.
#
# Walls:
# Wall 1: (0,2)-(1,2) = 2<->8
# Wall 2: (2,4)-(3,4) = 16<->22
# Wall 3: (4,1)-(4,2) = 25<->26
#
# Start (3,3)=21, parity=0. End must be parity 1.
# Actually let's start at (0,5)=5, parity=1. End at (5,0)=30, parity=1. Same! Bad.
# Start (0,5)=5, parity 1. End at (5,5)=35, parity 0. Different. Good.
# But I want interior starts. Let's try:
# Start (1,1)=7, parity 0. End (2,3)=15, parity 1. Different.
#
# Path design:
# 7(1,1)->1(0,1)->0(0,0)->6(1,0)->12(2,0)->13(2,1)->14(2,2)->8(1,2)->
# Wait, wall between (0,2)=2 and (1,2)=8? So 2<->8 blocked. But 14->8 is (2,2)->(1,2). Is that blocked? No, wall is between (0,2) and (1,2). 14(2,2)->8(1,2) is fine.
# 8(1,2)->9(1,3)->3(0,3)->2(0,2)->
# Can we go 2(0,2) down? Wall blocks 2->8. So from 2 we must go to 1 (visited) or 3 (visited). Dead end!
#
# Let me redesign. With wall between 2 and 8, we need to visit 2 from 1 or 3.
#
# 7(1,1)->6(1,0)->0(0,0)->1(0,1)->2(0,2)->3(0,3)->4(0,4)->5(0,5)->11(1,5)->10(1,4)->9(1,3)->8(1,2)->
# 8->14? (1,2)->(2,2) yes.
# 14(2,2)->13(2,1)->12(2,0)->18(3,0)->19(3,1)->20(3,2)->21(3,3)->15(2,3)->16(2,4)->
# Wall between 16(2,4) and 22(3,4). So can't go 16->22.
# 16(2,4)->17(2,5)->23(3,5)->22(3,4)->
# 22->21? Visited. 22->28(4,4)? Yes.
# 28(4,4)->27(4,3)->26(4,2)->
# Wall between 25 and 26? (4,1)-(4,2) = 25<->26 blocked. So we arrived at 26 from 27 (fine).
# From 26(4,2): can go to 20(visited), 32(5,2), or 25(blocked by wall!).
# 26->32(5,2)->33(5,3)->34(5,4)->35(5,5)->29(4,5)->
# 29 already... wait, is 29 visited? Let me check: no, 29 not in path yet.
# 29(4,5)->23? visited. 29->35? visited. 29->28? visited.
# Dead end at 29!
#
# Let me reconsider.
# After 28(4,4)->29(4,5)->35(5,5)->34(5,4)->33(5,3)->27(4,3)?
# Wait, 27 would be visited if I go 28->27. Let me redo from 22.
#
# 22(3,4)->28(4,4)->29(4,5)->35(5,5)->34(5,4)->33(5,3)->32(5,2)->26(4,2)->
# Wall 25<->26. From 26: can go to 20(visited), 27(4,3), or 32(visited).
# 26->27(4,3)->21? visited. 27->33? visited. 27->28? visited.
# Dead end!
#
# Try: 22(3,4)->28(4,4)->34(5,4)->35(5,5)->29(4,5)->23? visited. Dead end.
#
# Hmm. Let me reconsider the wall placement and path. The wall between 25-26 is causing issues.
# Let me change wall 3 to (4,2)-(4,3) = 26<->27.
# Wall 3: (4,2)-(4,3) = 26<->27
#
# After 16(2,4)->17(2,5)->23(3,5)->22(3,4)->28(4,4)->29(4,5)->35(5,5)->34(5,4)->33(5,3)->27(4,3)->
# 27<->26 blocked by wall 3. From 27: 21(visited), 33(visited), 28(visited). Dead end!
#
# OK, let me change wall 3 to (3,1)-(3,2) = 19<->20.
# Walls: (0,2)-(1,2)=2<->8, (2,4)-(3,4)=16<->22, (3,1)-(3,2)=19<->20
#
# Path:
# 7(1,1)->6(1,0)->0(0,0)->1(0,1)->2(0,2)->3(0,3)->4(0,4)->5(0,5)->11(1,5)->10(1,4)->9(1,3)->8(1,2)->
# 14(2,2)->13(2,1)->12(2,0)->18(3,0)->19(3,1)->25(4,1)->24(4,0)->30(5,0)->31(5,1)->32(5,2)->
# 26(4,2)->20(3,2)->21(3,3)->15(2,3)->16(2,4)->17(2,5)->23(3,5)->22(3,4)->
# 28(4,4)->34(5,4)->35(5,5)->29(4,5)->
# Wait, from 29(4,5)->23? visited. 29->35? visited. 29->28? visited.
# Ugh, dead end.
#
# Let me try: after 22(3,4)->28(4,4)->29(4,5)->35(5,5)->34(5,4)->33(5,3)->
# 33->27(4,3)->26(4,2)->... hmm, but 32 needs to be visited too.
#
# Let me try a completely different approach for Wednesday.
# Start at corner, with walls that create actual detours.
#
# Walls: (1,2)-(1,3) = 8<->9, (2,4)-(3,4) = 16<->22, (4,0)-(4,1) = 24<->25
# These are HORIZONTAL walls (between cells in same row).
#
# Start (0,0)=0, parity 0. End must be parity 1.
#
# Path:
# 0(0,0)->1(0,1)->2(0,2)->3(0,3)->4(0,4)->5(0,5)->
# 11(1,5)->10(1,4)->9(1,3)->15(2,3)->14(2,2)->8(1,2)->
# Wait, wall between 8 and 9. So 8<->9 blocked. In this path, 9->15 not 9->8. Let me check: 10(1,4)->9(1,3), that's fine (no wall between those). 9(1,3)->15(2,3) OK. Then 15->14? (2,3)->(2,2) yes. 14->8? (2,2)->(1,2) yes.
# 8(1,2)->7(1,1)->6(1,0)->12(2,0)->13(2,1)->
# 13->19(3,1)->18(3,0)->24(4,0)->
# Wall between 24 and 25. From 24: go to 30(5,0).
# 30(5,0)->31(5,1)->25(4,1)->26(4,2)->20(3,2)->21(3,3)->
# 21->27(4,3)->33(5,3)->32(5,2)->
# 32->26? visited. Dead end at 32!
# Actually from 32(5,2): neighbors are 31(visited), 33(visited), 26(visited). Dead end.
#
# Let me rethink. I need to make sure the bottom area works.
# ... ->25(4,1)->26(4,2)->32(5,2)->31? visited.
# No, 31->25: (5,1)->(4,1). Let me try:
# 30(5,0)->31(5,1)->32(5,2)->33(5,3)->34(5,4)->35(5,5)->29(4,5)->28(4,4)->27(4,3)->26(4,2)->25(4,1)->
# Wall 24<->25. From 25: can go to 19(3,1), 31(visited), 26(visited).
# 25(4,1)->19(3,1)->20(3,2)->21(3,3)->22(3,4)->
# Wall 16<->22. From 22: can go to 21(visited), 23(3,5), 28(visited).
# 22->23(3,5)->17(2,5)->16(2,4)->
# 16->10? visited. 16->15? (2,4)->(2,3).
# 16(2,4)->15(2,3)->...
# But we need to visit all cells. Let me count what's left.
# Visited so far: 0,1,2,3,4,5,11,10,9,15,14,8,7,6,12,13,18,24,30,31,32,33,34,35,29,28,27,26,25,19,20,21,22,23,17,16 = 36!
# Wait, after 16 we're done? Let me count: 36 cells. Let me list them:
# 0,1,2,3,4,5,11,10,9,15,14,8,7,6,12,13,18,24,30,31,32,33,34,35,29,28,27,26,25,19,20,21,22,23,17,16
# Count: 36.
# But we need path to end at last checkpoint. Let's say end is cell 16=(2,4), parity = (2+4)%2 = 0. Start is 0=(0,0) parity 0. Same parity! Bad for even grid.
#
# Switch: end at 15=(2,3), parity 1. But then 16 needs to come before 15.
# Rearrange end:
# ...22->23(3,5)->17(2,5)->16(2,4)->15(2,3)
# End at 15, parity 1. Start at 0, parity 0. Different! Good!
# But wait, from 16(2,4)->15(2,3): adjacent? Yes.
#
# Full path: 0,1,2,3,4,5,11,10,9,15,14,8,7,6,12,13,18,24,30,31,32,33,34,35,29,28,27,26,25,19,20,21,22,23,17,16
# Hmm, 15 appears at position 9 and we want it at the end. Can't have it both ways.
#
# Let me redesign so 15 is only at the end.
# After 9(1,3): instead of going to 15, go to... 9's neighbors: 8(wall!), 10(visited), 3(visited), 15(2,3).
# Since 8<->9 is walled and 10/3 visited, 15 is the only option from 9. So 15 must be visited here.
#
# OK different approach. Let me try different walls.
# Walls: (1,3)-(2,3) = 9<->15, (3,2)-(3,3) = 20<->21, (4,0)-(4,1) = 24<->25
#
# Path:
# 0(0,0)->1(0,1)->2(0,2)->8(1,2)->7(1,1)->6(1,0)->12(2,0)->13(2,1)->14(2,2)->
# 20(3,2)->19(3,1)->18(3,0)->24(4,0)->30(5,0)->31(5,1)->25(4,1)->
# Wall 24<->25. But we're going 31(5,1)->25(4,1). Is that walled? Wall is (4,0)-(4,1). 31 is (5,1), 25 is (4,1). No wall between those.
# 25->26(4,2)->32(5,2)->33(5,3)->27(4,3)->21(3,3)->
# Wall 20<->21. We're going 27(4,3)->21(3,3). No wall between those. OK.
# 21->15(2,3)->
# Wall 9<->15. We're going 21(3,3)->15(2,3). No wall between those.
# 15->16(2,4)->10(1,4)->9(1,3)->3(0,3)->4(0,4)->5(0,5)->11(1,5)->17(2,5)->
# 23(3,5)->22(3,4)->28(4,4)->34(5,4)->35(5,5)->29(4,5)->
# 29's neighbors: 23(visited), 35(visited), 28(visited). Dead end!
#
# Let me fix the bottom-right corner:
# ...28(4,4)->29(4,5)->35(5,5)->34(5,4)->33? Already visited at position...
# Let me reconsider.
# After 27(4,3)->21(3,3)->15(2,3)->16(2,4)->10(1,4)->9(1,3)->3(0,3)->4(0,4)->5(0,5)->11(1,5)->17(2,5)->23(3,5)->29(4,5)->35(5,5)->34(5,4)->28(4,4)->22(3,4)->
# 22's neighbors: 21(visited), 23(visited), 16(visited), 28(visited). Dead end.
# But all visited! Let me count:
# 0,1,2,8,7,6,12,13,14,20,19,18,24,30,31,25,26,32,33,27,21,15,16,10,9,3,4,5,11,17,23,29,35,34,28,22 = 36!
# End at 22=(3,4), parity=(3+4)%2=1. Start 0=(0,0) parity 0. Different!
#
# That works! Let me verify the full path:
wednesday_path = [0,1,2,8,7,6,12,13,14,20,19,18,24,30,31,25,26,32,33,27,21,15,16,10,9,3,4,5,11,17,23,29,35,34,28,22]
# Checkpoints (9, mix edge and interior):
# 0=1 (corner start)
# 8=2 (interior (1,2))
# 13=3 (interior (2,1))
# 19=4 (interior (3,1))
# 26=5 (interior (4,2))
# 33=6 (interior (5,3))
# 15=7 (interior (2,3))
# 5=8 (edge (0,5))
# 22=9 (interior (3,4), end)
wednesday_checkpoints = {0:1, 8:2, 13:3, 19:4, 26:5, 33:6, 15:7, 5:8, 22:9}
wednesday_walls = [[1,3,2,3],[3,2,3,3],[4,0,4,1]]

verify_puzzle("Wednesday", 6, 6, wednesday_path, wednesday_checkpoints, wednesday_walls)


# ═══════════════════════════════════════════
# THURSDAY - 7x7, 9 checkpoints, 4 walls
# ═══════════════════════════════════════════
# 7x7 = 49 cells. Odd grid, no parity constraint.
#
# Grid indices:
# Row 0: 0  1  2  3  4  5  6
# Row 1: 7  8  9  10 11 12 13
# Row 2: 14 15 16 17 18 19 20
# Row 3: 21 22 23 24 25 26 27
# Row 4: 28 29 30 31 32 33 34
# Row 5: 35 36 37 38 39 40 41
# Row 6: 42 43 44 45 46 47 48
#
# Walls (4):
# (1,3)-(1,4) = 10<->11 (horizontal, blocks row 1 middle)
# (2,5)-(3,5) = 19<->26 (vertical, blocks right area)
# (4,2)-(4,3) = 30<->31 (horizontal, blocks row 4 middle)
# (5,0)-(6,0) = 35<->42 (vertical, blocks left bottom)
#
# I'll design a twisty path.
# Start at (0,3)=3 (top middle), end at (6,4)=46.
#
# Path:
# 3(0,3)->2(0,2)->1(0,1)->0(0,0)->7(1,0)->8(1,1)->9(1,2)->10(1,3)->
# Wall 10<->11. From 10: go to 17(2,3).
# 17(2,3)->16(2,2)->15(2,1)->14(2,0)->21(3,0)->22(3,1)->23(3,2)->24(3,3)->
# 25(3,4)->18(2,4)->19(2,5)->
# Wall 19<->26. From 19: go to 20(2,6).
# 20(2,6)->13(1,6)->12(1,5)->11(1,4)->4(0,4)->5(0,5)->6(0,6)->
# From 6: go to 13? Visited. Dead end.
#
# Let me try: after 11(1,4)->4(0,4)->5(0,5)->6(0,6). From 6, only neighbor is 5(visited) and 13(visited). Dead end.
# Need 6 to be visited from 5 then to... hmm.
#
# Let me rethink. Visit top-right area first.
# 3(0,3)->4(0,4)->5(0,5)->6(0,6)->13(1,6)->12(1,5)->11(1,4)->
# Wall 10<->11. From 11: go to 18(2,4) or 4(visited).
# 11(1,4)->18(2,4)->19(2,5)->
# Wall 19<->26. From 19: go to 20(2,6) or 12(visited) or 18(visited).
# 19->20(2,6)->27(3,6)->26(3,5)->25(3,4)->24(3,3)->17(2,3)->10(1,3)->
# Wall 10<->11 but we already passed 11. 10->9(1,2).
# 9(1,2)->8(1,1)->7(1,0)->0(0,0)->1(0,1)->2(0,2)->
# From 2: 3(visited), 1(visited), 9(visited). Dead end at step...
# We haven't visited enough of row 2.
# 2(0,2)->... only neighbors are 1(visited),3(visited),9(visited). Dead end!
#
# I need 2 to connect downward to 9, which is visited. Hmm.
# Let me try visiting row 0 left part later.
#
# 3(0,3)->4(0,4)->5(0,5)->6(0,6)->13(1,6)->12(1,5)->11(1,4)->18(2,4)->
# 19(2,5)->20(2,6)->27(3,6)->26(3,5)->25(3,4)->24(3,3)->23(3,2)->
# 22(3,1)->21(3,0)->14(2,0)->15(2,1)->16(2,2)->17(2,3)->10(1,3)->
# Wall 10<->11. From 10: 9(1,2), 3(visited), 17(visited).
# 10->9(1,2)->8(1,1)->7(1,0)->0(0,0)->1(0,1)->2(0,2)->
# From 2: neighbors are 1(visited), 3(visited), 9(visited). Dead end again!
#
# The problem is cell 2 is boxed in between visited cells.
# Solution: visit 2 right after 1, before going right.
#
# 3(0,3)->2(0,2)->1(0,1)->0(0,0)->7(1,0)->8(1,1)->9(1,2)->10(1,3)->
# Wall 10<->11. 10->17(2,3)->16(2,2)->15(2,1)->14(2,0)->21(3,0)->22(3,1)->
# 23(3,2)->24(3,3)->25(3,4)->18(2,4)->11(1,4)->4(0,4)->5(0,5)->
# 12(1,5)->19(2,5)->
# Wall 19<->26. 19->20(2,6)->13(1,6)->6(0,6)->
# From 6: 5(visited), 13(visited). Dead end!
#
# I need to visit 6 before 13 or from 13.
# ... ->13(1,6)->6(0,6)-> only goes to 5 or 13(visited). So 6 must be a dead end or visited before 13.
# Let's try: ->5(0,5)->6(0,6)->13(1,6)->12(1,5)->19(2,5)->
# Then from 19: wall 19<->26. Go to 20(2,6).
# 20(2,6)->27(3,6)->26(3,5)->...
#
# Full attempt:
# 3->2->1->0->7->8->9->10[wall]->17->16->15->14->21->22->23->24->25->18->11[through wall? 11<->10 wall but 18->11: (2,4)->(1,4), fine]->4->5->6->13->12->19[wall 19<->26]->20->27->26->
# From 26: 25(visited), 27(visited), 33(4,5), 19(wall).
# 26->33(4,5)->34(4,6)->41(5,6)->40(5,5)->39(5,4)->38(5,3)->37(5,2)->36(5,1)->35(5,0)->
# Wall 35<->42. From 35: 28(4,0), 36(visited).
# 35->28(4,0)->29(4,1)->30(4,2)->
# Wall 30<->31. From 30: 23(visited), 29(visited), 37(visited).
# Dead end at 30!
#
# Try: 35->28->29->30[wall]->... from 30: 23(visited), 37(visited), 29(visited). Dead end.
#
# The wall 30<->31 is problematic. Let me change it.
# New wall 3: (4,1)-(4,2) = 29<->30
#
# ...35->28(4,0)->29(4,1)->
# Wall 29<->30. From 29: 22(visited), 28(visited), 36(visited). Dead end!
#
# Let me change wall 3 to: (3,3)-(4,3) = 24<->31
#
# Walls:
# (1,3)-(1,4) = 10<->11
# (2,5)-(3,5) = 19<->26
# (3,3)-(4,3) = 24<->31
# (5,0)-(6,0) = 35<->42
#
# Path:
# 3->2->1->0->7->8->9->10[wall 10<->11]->17->16->15->14->21->22->23->24->
# Wall 24<->31. From 24: 25(3,4), 23(visited), 17(visited).
# 24->25->18->11[wall10<->11, but 18->11 is fine]->4->5->6->13->12->19[wall 19<->26]->20->27->26->
# 26->33(4,5)->34(4,6)->41(5,6)->40(5,5)->39(5,4)->38(5,3)->37(5,2)->36(5,1)->35(5,0)->
# Wall 35<->42. 35->28(4,0)->29(4,1)->30(4,2)->31(4,3)->
# Wall 24<->31. 31->32(4,4)? Yes.
# 32(4,4)->... 32's neighbors: 31(visited), 33(visited), 25(visited), 39(visited).
# Dead end!
#
# Problem: 32 gets boxed in. I need to visit 32 before 33 or route differently.
#
# Let me try:
# ...26->33->32->31[wall 24<->31, but going 32->31 is (4,4)->(4,3), fine]->
# 31->38(5,3)? Yes. Then we need to get to 34 and 41.
# 31->38->37->36->35[wall 35<->42]->28->29->30->23? visited.
# 30->37? visited. 30->31? visited. From 30(4,2): neighbors 29(visited), 31(visited), 23(visited), 37(visited). Dead end!
#
# OK I'm going to take a totally different approach and build from scratch.
# Let me use a systematic spiral-ish path.
#
# 7x7 grid. Let me trace a working Hamiltonian path:
# Go along top: 0->1->2->3->4->5->6
# Down right side: 6->13->20->27->34->41->48
# Left along bottom: 48->47->46->45->44->43->42
# Up left side: 42->35->28->21->14->7
# Now inner spiral: 7->8->... wait, 7 is (1,0). From 7 go to 8(1,1).
# Inner ring: 8->9->10->11->12
# 12->19->26->33->40
# 40->39->38->37->36
# 36->29->22->15
# 15->16->17->18->25->32->31->30->23->24
# Wait, from 15(2,1)->16(2,2)->17(2,3)->18(2,4)->25(3,4)->32(4,4)->31(4,3)->30(4,2)->23(3,2)->24(3,3)
# That's the inner core.
#
# Full spiral path:
# 0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,28,21,14,7,8,9,10,11,12,19,26,33,40,39,38,37,36,29,22,15,16,17,18,25,32,31,30,23,24
# Count: 49.
#
# Now I need walls that DON'T interfere with this path and make it interesting.
# Path consecutive pairs: (0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,13),(13,20),(20,27),(27,34),(34,41),(41,48),(48,47),(47,46),(46,45),(45,44),(44,43),(43,42),(42,35),(35,28),(28,21),(21,14),(14,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,19),(19,26),(26,33),(33,40),(40,39),(39,38),(38,37),(37,36),(36,29),(29,22),(22,15),(15,16),(16,17),(17,18),(18,25),(25,32),(32,31),(31,30),(30,23),(23,24)
#
# Good walls (not crossing the path):
# (0,3)-(1,3) = 3<->10: path has (3,4) and (9,10), not 3<->10. Good.
# (2,1)-(3,1) = 15<->22: path has (22,15), THAT'S IN THE PATH! Bad.
# (1,4)-(2,4) = 11<->18: path has (10,11) and (17,18), not 11<->18.
# (3,2)-(3,3) = 23<->24: path has (23,24). Bad!
# (3,1)-(3,2) = 22<->23: path has (30,23) but not 22<->23.
# (4,4)-(5,4) = 32<->39: path has (32,31) and (39,38), not 32<->39.
# (5,2)-(5,3) = 37<->38: path has (38,37). Bad!
# (5,1)-(6,1) = 36<->43: path has (43,42) and (37,36), not 36<->43.
# (2,3)-(2,4) = 17<->18: path has (17,18). Bad.
# (0,2)-(1,2) = 2<->9: path has (2,3) and (8,9), not 2<->9.
#
# Good walls:
# W1: (0,3)-(1,3) = 3<->10
# W2: (1,4)-(2,4) = 11<->18
# W3: (3,1)-(3,2) = 22<->23
# W4: (4,4)-(5,4) = 32<->39
#
# These walls don't cross the spiral path. But they will block alternative routes, forcing the spiral.
# The path IS a spiral though. Let me make it less obviously spiral by modifying it.
#
# Actually, the spiral IS non-serpentine and interesting. The walls force the solver to find the spiral.
# Let me place interior-heavy checkpoints.
#
# Checkpoints (9, majority interior):
# path[0]=0 -> CP1 (corner, start)
# path[7]=13 -> CP2 (edge (1,6))
# path[14]=46 -> CP3 (edge (6,4))
# path[22]=14 -> CP4 (edge (2,0))
# path[28]=12 -> CP5 (edge (1,5))  -- too many edge ones
#
# Let me pick more interior ones:
# 0=CP1 (start, corner)
# 10=CP2 (interior (1,3))
# 45=CP3 (interior-ish (6,3))
# 8=CP4 (interior (1,1))
# 26=CP5 (interior (3,5))
# 39=CP6 (interior (5,4))
# 22=CP7 (interior (3,1))
# 17=CP8 (interior (2,3))
# 24=CP9 (interior (3,3), end)
#
# Check order in path:
# 0 at pos 0, 10 at pos 26, 45 at pos 15, 8 at pos 24, 26 at pos 30, 39 at pos 33, 22 at pos 38, 17 at pos 41, 24 at pos 48
# Order: 0(0), 45(15), 8(24), 10(26), 26(30), 39(33), 22(38), 17(41), 24(48)
# So checkpoints must be numbered in path order:
# 0->1, 45->2, 8->3, 10->4, 26->5, 39->6, 22->7, 17->8, 24->9

thursday_path = [0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,28,21,14,7,8,9,10,11,12,19,26,33,40,39,38,37,36,29,22,15,16,17,18,25,32,31,30,23,24]
thursday_checkpoints = {0:1, 45:2, 8:3, 10:4, 26:5, 39:6, 22:7, 17:8, 24:9}
thursday_walls = [[0,3,1,3],[1,4,2,4],[3,1,3,2],[4,4,5,4]]

verify_puzzle("Thursday", 7, 7, thursday_path, thursday_checkpoints, thursday_walls)


# ═══════════════════════════════════════════
# FRIDAY - 7x7, 10 checkpoints, 5 walls
# ═══════════════════════════════════════════
# 7x7 = 49 cells. Odd grid.
#
# Let me design a different non-spiral path.
# I'll use a more complex traversal.
#
# Let me try a "zigzag with detours" approach:
# Start at (3,3)=24 (center!) for max interior-ness
#
# 24(3,3)->23(3,2)->22(3,1)->21(3,0)->14(2,0)->15(2,1)->16(2,2)->17(2,3)->
# 18(2,4)->19(2,5)->20(2,6)->13(1,6)->12(1,5)->11(1,4)->10(1,3)->9(1,2)->
# 8(1,1)->7(1,0)->0(0,0)->1(0,1)->2(0,2)->3(0,3)->4(0,4)->5(0,5)->6(0,6)->
# From 6: only neighbor is 5(visited) and 13(visited). Dead end!
#
# Visit 6 before 13:
# ...20(2,6)->27(3,6)->34(4,6)->41(5,6)->48(6,6)->47(6,5)->40(5,5)->
# 33(4,5)->26(3,5)->19(2,5)-> wait, 19 already visited.
#
# Let me try a completely different path structure.
#
# Row-by-row but with detours:
# 0->1->2->3->4->5->6->13->12->11->10->9->8->7->14->15->16->17->18->19->20->27->26->25->24->23->22->21->28->29->30->31->32->33->34->41->40->39->38->37->36->35->42->43->44->45->46->47->48
# That's a pure serpentine. Let me modify it.
#
# Take the serpentine and add a twist in the middle:
# Row 0 L->R: 0->1->2->3->4->5->6
# Row 1 R->L: 13->12->11->10->9->8->7
# Instead of going to row 2, detour:
# 7->14->21->28->29->22->15->16->17->24->23->
# Wall needed to prevent shortcut. Then:
# 23->30->37->36->35->42->43->44->45->38->31->32->33->
# 26->25->18->19->20->27->34->41->48->47->46->39->40
# Wait, let me be more careful.
#
# You know what, let me just construct a known working Hamiltonian path by doing a modified serpentine with some swaps.
#
# Base serpentine (7x7):
# Row0 R: 0,1,2,3,4,5,6
# Row1 L: 13,12,11,10,9,8,7
# Row2 R: 14,15,16,17,18,19,20
# Row3 L: 27,26,25,24,23,22,21
# Row4 R: 28,29,30,31,32,33,34
# Row5 L: 41,40,39,38,37,36,35
# Row6 R: 42,43,44,45,46,47,48
#
# Now I'll modify it to be non-serpentine by swapping some sections:
# After hitting 6(0,6), instead of going to 13(1,6), drop down the right column:
# 0,1,2,3,4,5,6 then 6->13->20->27
# Then traverse row 3 leftward: 27->26->25->24->23->22->21
# Then up: 21->14->7->8->9->10->11->12
# Then 12->19->18->17->16->15 ... wait, 14 is visited, dead end from 15.
# 15(2,1)->14(visited). 15->16(visited if we go 15 before 16). Let me reconsider.
#
# 0,1,2,3,4,5,6,13,20,27,26,25,24,23,22,21,14,7,8,9,10,11,12,19,18,17,16,15
# From 15(2,1): neighbors 14(visited),16(visited),8(visited),22(visited). Dead end at step 27!
# Still 21 cells unvisited (rows 4,5,6 and some of row 2).
#
# OK, let me try yet another approach.
# I'll construct the path column by column with snaking:
# Col0 down: 0,7,14,21,28,35,42
# Col1 up: 43,36,29,22,15,8,1
# Col2 down: 2,9,16,23,30,37,44
# Col3 up: 45,38,31,24,17,10,3
# Col4 down: 4,11,18,25,32,39,46
# Col5 up: 47,40,33,26,19,12,5
# Col6 down: 6,13,20,27,34,41,48
#
# Full: 0,7,14,21,28,35,42,43,36,29,22,15,8,1,2,9,16,23,30,37,44,45,38,31,24,17,10,3,4,11,18,25,32,39,46,47,40,33,26,19,12,5,6,13,20,27,34,41,48
# Count: 49. Good!
# This is interesting - it's a column-snake, which is less obvious than a row-snake.
#
# Walls that don't cross this path:
# Path pairs: (0,7),(7,14),(14,21),(21,28),(28,35),(35,42),(42,43),(43,36),(36,29),(29,22),(22,15),(15,8),(8,1),(1,2),(2,9),(9,16),(16,23),(23,30),(30,37),(37,44),(44,45),(45,38),(38,31),(31,24),(24,17),(17,10),(10,3),(3,4),(4,11),(11,18),(18,25),(25,32),(32,39),(39,46),(46,47),(47,40),(40,33),(33,26),(26,19),(19,12),(12,5),(5,6),(6,13),(13,20),(20,27),(27,34),(34,41),(41,48)
#
# Walls NOT in the path:
# (0,1)-(0,2)=1<->2: IN PATH (8,1),(1,2).
# (0,0)-(0,1)=0<->1: not consecutive in path. GOOD.
# (1,0)-(1,1)=7<->8: path has (7,14) and (15,8). Not 7<->8. GOOD.
# (2,2)-(2,3)=16<->17: path has (16,23) and (24,17). Not 16<->17. GOOD.
# (3,3)-(3,4)=24<->25: path has (31,24) and (18,25). Not 24<->25. GOOD.
# (4,4)-(4,5)=32<->33: path has (25,32) and (40,33). Not 32<->33. GOOD.
# (5,1)-(5,2)=36<->37: path has (43,36) and (30,37). Not 36<->37. GOOD.
#
# 5 walls:
# W1: (0,0)-(0,1) = 0<->1
# W2: (1,0)-(1,1) = 7<->8
# W3: (2,2)-(2,3) = 16<->17
# W4: (3,3)-(3,4) = 24<->25
# W5: (4,4)-(4,5) = 32<->33
#
# Checkpoints (10, interior-heavy):
# Following path order:
# 0=1 (start, corner (0,0))
# 21=2 (interior (3,0))
# 22=3 (interior (3,1))
# 9=4 (interior (1,2))
# 23=5 (interior (3,2))
# 38=6 (interior (5,3))
# 17=7 (interior (2,3))
# 11=8 (interior (1,4))
# 40=9 (interior (5,5))
# 48=10 (corner (6,6), end)
#
# Check order in path:
# 0@0, 21@3, 22@10, 9@15, 23@17, 38@22, 17@25, 11@29, 40@36, 48@48
# Ascending: yes!

friday_path = [0,7,14,21,28,35,42,43,36,29,22,15,8,1,2,9,16,23,30,37,44,45,38,31,24,17,10,3,4,11,18,25,32,39,46,47,40,33,26,19,12,5,6,13,20,27,34,41,48]
friday_checkpoints = {0:1, 21:2, 22:3, 9:4, 23:5, 38:6, 17:7, 11:8, 40:9, 48:10}
friday_walls = [[0,0,0,1],[1,0,1,1],[2,2,2,3],[3,3,3,4],[4,4,4,5]]

verify_puzzle("Friday", 7, 7, friday_path, friday_checkpoints, friday_walls)


# ═══════════════════════════════════════════
# SATURDAY - 8x8, 10 checkpoints, 6 walls
# ═══════════════════════════════════════════
# 8x8 = 64 cells. Even grid: start/end different parity.
#
# Row 0: 0  1  2  3  4  5  6  7
# Row 1: 8  9  10 11 12 13 14 15
# Row 2: 16 17 18 19 20 21 22 23
# Row 3: 24 25 26 27 28 29 30 31
# Row 4: 32 33 34 35 36 37 38 39
# Row 5: 40 41 42 43 44 45 46 47
# Row 6: 48 49 50 51 52 53 54 55
# Row 7: 56 57 58 59 60 61 62 63
#
# Column-snake approach (like Friday):
# Col0 down: 0,8,16,24,32,40,48,56
# Col1 up: 57,49,41,33,25,17,9,1
# Col2 down: 2,10,18,26,34,42,50,58
# Col3 up: 59,51,43,35,27,19,11,3
# Col4 down: 4,12,20,28,36,44,52,60
# Col5 up: 61,53,45,37,29,21,13,5
# Col6 down: 6,14,22,30,38,46,54,62
# Col7 up: 63,55,47,39,31,23,15,7
#
# Full: 0,8,16,24,32,40,48,56,57,49,41,33,25,17,9,1,2,10,18,26,34,42,50,58,59,51,43,35,27,19,11,3,4,12,20,28,36,44,52,60,61,53,45,37,29,21,13,5,6,14,22,30,38,46,54,62,63,55,47,39,31,23,15,7
# Count: 64. Good!
#
# Start: 0=(0,0), parity 0. End: 7=(0,7), parity 1. Different! Good!
#
# Path pairs for wall checking:
# (0,8),(8,16),(16,24),(24,32),(32,40),(40,48),(48,56),(56,57),(57,49),(49,41),(41,33),(33,25),(25,17),(17,9),(9,1),(1,2),(2,10),(10,18),(18,26),(26,34),(34,42),(42,50),(50,58),(58,59),(59,51),(51,43),(43,35),(35,27),(27,19),(19,11),(11,3),(3,4),(4,12),(12,20),(20,28),(28,36),(36,44),(44,52),(52,60),(60,61),(61,53),(53,45),(45,37),(37,29),(29,21),(21,13),(13,5),(5,6),(6,14),(14,22),(22,30),(30,38),(38,46),(46,54),(54,62),(62,63),(63,55),(55,47),(47,39),(39,31),(31,23),(23,15),(15,7)
#
# Walls NOT in path:
# (0,0)-(0,1) = 0<->1: path has (9,1) not 0<->1. GOOD.
# (1,0)-(1,1) = 8<->9: path has (8,16) and (17,9). Not 8<->9. GOOD.
# (2,2)-(2,3) = 18<->19: path has (18,26) and (27,19). Not 18<->19. GOOD.
# (3,3)-(3,4) = 27<->28: path has (35,27) and (20,28). Not 27<->28. GOOD.
# (4,4)-(4,5) = 36<->37: path has (28,36) and (45,37). Not 36<->37. GOOD.
# (5,5)-(5,6) = 45<->46: path has (53,45) and (38,46). Not 45<->46. GOOD.
# (6,2)-(6,3) = 50<->51: path has (50,58) and (59,51). Not 50<->51. GOOD.
# (7,4)-(7,5) = 60<->61: path has (60,61). BAD!
# (1,2)-(1,3) = 10<->11: path has (10,18) and (19,11). Not 10<->11. GOOD.
# (5,2)-(5,3) = 42<->43: path has (42,50) and (51,43). Not 42<->43. GOOD.
#
# 6 walls:
# W1: (0,0)-(0,1) = 0<->1
# W2: (1,0)-(1,1) = 8<->9
# W3: (2,2)-(2,3) = 18<->19
# W4: (3,3)-(3,4) = 27<->28
# W5: (4,4)-(4,5) = 36<->37
# W6: (5,5)-(5,6) = 45<->46

saturday_path = [0,8,16,24,32,40,48,56,57,49,41,33,25,17,9,1,2,10,18,26,34,42,50,58,59,51,43,35,27,19,11,3,4,12,20,28,36,44,52,60,61,53,45,37,29,21,13,5,6,14,22,30,38,46,54,62,63,55,47,39,31,23,15,7]

# Checkpoints (10, interior-heavy):
# Path positions: 0@0, 8@1, 56@7, 57@8, 25@12, 18@18, 51@25, 28@35, 53@41, 7@63(end)
# Let me pick good ones:
# 0=1 (start, corner)
# 24=2 (interior (3,0)) @pos3
# 49=3 (interior (6,1)) @pos9
# 17=4 (interior (2,1)) @pos13
# 26=5 (interior (3,2)) @pos19
# 43=6 (interior (5,3)) @pos26
# 12=7 (interior (1,4)) @pos33
# 37=8 (interior (4,5)) @pos43
# 22=9 (interior (2,6)) @pos50
# 7=10 (edge (0,7), end) @pos63
#
# Order check: 0@0, 24@3, 49@9, 17@13, 26@19, 43@26, 12@33, 37@43, 22@50, 7@63
# Ascending: yes!

saturday_checkpoints = {0:1, 24:2, 49:3, 17:4, 26:5, 43:6, 12:7, 37:8, 22:9, 7:10}
saturday_walls = [[0,0,0,1],[1,0,1,1],[2,2,2,3],[3,3,3,4],[4,4,4,5],[5,5,5,6]]

verify_puzzle("Saturday", 8, 8, saturday_path, saturday_checkpoints, saturday_walls)


# ═══════════════════════════════════════════
# SUNDAY - 9x9, 10 checkpoints, 7 walls
# ═══════════════════════════════════════════
# 9x9 = 81 cells. Odd grid.
#
# Column-snake:
# Col0 down: 0,9,18,27,36,45,54,63,72
# Col1 up: 73,64,55,46,37,28,19,10,1
# Col2 down: 2,11,20,29,38,47,56,65,74
# Col3 up: 75,66,57,48,39,30,21,12,3
# Col4 down: 4,13,22,31,40,49,58,67,76
# Col5 up: 77,68,59,50,41,32,23,14,5
# Col6 down: 6,15,24,33,42,51,60,69,78
# Col7 up: 79,70,61,52,43,34,25,16,7
# Col8 down: 8,17,26,35,44,53,62,71,80
#
# Full: 0,9,18,27,36,45,54,63,72,73,64,55,46,37,28,19,10,1,2,11,20,29,38,47,56,65,74,75,66,57,48,39,30,21,12,3,4,13,22,31,40,49,58,67,76,77,68,59,50,41,32,23,14,5,6,15,24,33,42,51,60,69,78,79,70,61,52,43,34,25,16,7,8,17,26,35,44,53,62,71,80
# Count: 81. Good!
#
# Path pairs:
# (0,9),(9,18),(18,27),(27,36),(36,45),(45,54),(54,63),(63,72),(72,73),(73,64),(64,55),(55,46),(46,37),(37,28),(28,19),(19,10),(10,1),(1,2),(2,11),(11,20),(20,29),(29,38),(38,47),(47,56),(56,65),(65,74),(74,75),(75,66),(66,57),(57,48),(48,39),(39,30),(30,21),(21,12),(12,3),(3,4),(4,13),(13,22),(22,31),(31,40),(40,49),(49,58),(58,67),(67,76),(76,77),(77,68),(68,59),(59,50),(50,41),(41,32),(32,23),(23,14),(14,5),(5,6),(6,15),(15,24),(24,33),(33,42),(42,51),(51,60),(60,69),(69,78),(78,79),(79,70),(70,61),(61,52),(52,43),(43,34),(34,25),(25,16),(16,7),(7,8),(8,17),(17,26),(26,35),(35,44),(44,53),(53,62),(62,71),(71,80)
#
# Walls NOT in path:
# (0,0)-(0,1) = 0<->1: path (10,1). Not 0<->1. GOOD.
# (1,0)-(1,1) = 9<->10: path (9,18) and (19,10). Not 9<->10. GOOD.
# (2,2)-(2,3) = 20<->21: path (20,29) and (30,21). Not 20<->21. GOOD.
# (3,3)-(3,4) = 30<->31: path (39,30) and (22,31). Not 30<->31. GOOD.
# (4,4)-(4,5) = 40<->41: path (40,49) and (50,41). Not 40<->41. GOOD.
# (5,5)-(5,6) = 50<->51: path (59,50) and (42,51). Not 50<->51. GOOD.
# (6,6)-(6,7) = 60<->61: path (60,69) and (70,61). Not 60<->61. GOOD.
# (7,3)-(7,4) = 66<->67: path (75,66) and (58,67). Not 66<->67. GOOD.
#
# 7 walls:
# W1: (0,0)-(0,1) = 0<->1
# W2: (1,0)-(1,1) = 9<->10
# W3: (2,2)-(2,3) = 20<->21
# W4: (3,3)-(3,4) = 30<->31
# W5: (4,4)-(4,5) = 40<->41
# W6: (5,5)-(5,6) = 50<->51
# W7: (6,6)-(6,7) = 60<->61

sunday_path = [0,9,18,27,36,45,54,63,72,73,64,55,46,37,28,19,10,1,2,11,20,29,38,47,56,65,74,75,66,57,48,39,30,21,12,3,4,13,22,31,40,49,58,67,76,77,68,59,50,41,32,23,14,5,6,15,24,33,42,51,60,69,78,79,70,61,52,43,34,25,16,7,8,17,26,35,44,53,62,71,80]

# Checkpoints (10, interior-dominated):
# 0=1 (start, corner)
# 27=2 (interior (3,0)) @pos3
# 55=3 (interior (6,1)) @pos11
# 10=4 (interior (1,1)) @pos16
# 29=5 (interior (3,2)) @pos21
# 57=6 (interior (6,3)) @pos29
# 31=7 (interior (3,4)) @pos38
# 59=8 (interior (6,5)) @pos47
# 33=9 (interior (3,6)) @pos57
# 80=10 (corner (8,8), end) @pos80

sunday_checkpoints = {0:1, 27:2, 55:3, 10:4, 29:5, 57:6, 31:7, 59:8, 33:9, 80:10}
sunday_walls = [[0,0,0,1],[1,0,1,1],[2,2,2,3],[3,3,3,4],[4,4,4,5],[5,5,5,6],[6,6,6,7]]

verify_puzzle("Sunday", 9, 9, sunday_path, sunday_checkpoints, sunday_walls)

print("\n=== All verifications complete ===")
