# Snake Puzzle Game — Implementation Plan

## Game Overview
**Snake** (Gjarpëri) — a classic logic puzzle where the player draws a continuous snake path on a grid.

### Rules:
1. An NxN grid with a **head** (🟢) and **tail** (🔴) marked
2. Draw a continuous path from head to tail moving only horizontally/vertically
3. The snake **cannot touch itself** even diagonally (non-consecutive cells can't share a corner)
4. **Row clues** (left edge) and **column clues** (top edge) tell how many cells are part of the snake
5. Click to toggle: empty → snake → X (not-snake) → empty

### Difficulty (DaySizes):
- Monday/Tuesday: 5×5
- Wednesday/Thursday: 6×6
- Friday/Saturday: 7×7
- Sunday: 7×7

### Color: Teal/Emerald (#14B8A6) — distinct from existing green (Wordle7)

---

## Files to Create/Modify

### BACKEND (6 new files + 1 modified)

**1. `Models/SnakePuzzle.cs`** — Data model
- Size, RowClues[], ColClues[], HeadRow, HeadCol, TailRow, TailCol
- Solution[][] (0=empty, 1..N = path order where 1=head, N=tail)
- DayIndex, DayName

**2. `Services/SnakeSolver.cs`** — Backtracking solver
- `HasUniqueSolution(rowClues, colClues, headR, headC, tailR, tailC, size)` → bool
- `CountSolutions(..., maxCount)` → int
- Algorithm: build path from head, extending to adjacent unvisited cells, checking:
  - No diagonal touching with non-consecutive cells
  - Row/col counts not exceeded
  - Path must end at tail with all clues satisfied
- Forward checking: if remaining row/col capacity can't fit remaining path

**3. `Services/SnakeGenerator.cs`** — Puzzle generator
- `Generate(seed, dayIndex, dayName)` → SnakePuzzle
- DaySizes = [5, 5, 6, 6, 7, 7, 7]
- Algorithm:
  1. Random walk to build valid snake path (no diagonal self-touching)
  2. Compute row/col clues from path
  3. Verify unique solution via solver
  4. Try 60 seed offsets × multiple attempts

**4. `Data/SnakePuzzleData.cs`** — Cache + deterministic seed
- Same pattern as StarsPuzzleData: GetTodayPuzzle(), GetPuzzleByDay(), week-based caching

**5. `Controllers/PuzzlesController.cs`** — Add 2 endpoints
- `GET /api/puzzles/snake/today`
- `GET /api/puzzles/snake/{dayIndex}`

### FRONTEND (8 new files + 3 modified)

**6. `core/models/snake-puzzle.model.ts`** — TypeScript interface

**7. `core/services/puzzle.service.ts`** — Add getSnakeToday(), getSnakeByDay()

**8. `games/snake/snake-game.service.ts`** — Core game logic
- Cell states: EMPTY=0, MARK_X=1, SNAKE=2, AUTO_X=3
- Signal state: board, gameWon, timer, conflicts, hints, history
- toggleCell: empty → SNAKE → MARK_X → empty
- Auto-X: when row/col reaches its clue count, auto-X remaining empties
- Conflict detection: row/col over limit, diagonal touching of non-consecutive cells
- Win check: all clues matched, path continuous from head to tail, no violations
- Hint system: find cells that must be snake/empty based on clue constraints

**9. `games/snake/snake-board/snake-board.component.ts`** — SVG board
- Grid with row clue numbers on left, col clue numbers on top
- Head icon (circle with eyes/tongue), Tail icon (tapered circle)
- Snake cells: teal filled rounded squares
- X marks: small gray X
- Conflict overlay, hint highlight
- Win animation: snake path "slither" animation

**10. `games/snake/snake-board/snake-board.component.html`** — SVG template

**11. `games/snake/snake-board/snake-board.component.scss`** — Teal theme styles

**12. `games/snake/snake.component.ts`** — Main game component
- Day navigation, localStorage persistence, timer, modals
- Game color: #14B8A6

**13. `games/snake/snake.component.html`** — Template (top strip, board, messages, controls, modals)

**14. `games/snake/snake.component.scss`** — Teal color scheme

**15. `app.routes.ts`** — Add snake routes

**16. `home/home.component.html`** — Add Snake game card (teal theme, snake SVG icon)

---

## Implementation Order

### Phase 1 — Backend
1. Create `SnakePuzzle.cs` model
2. Create `SnakeSolver.cs` (backtracking path solver)
3. Create `SnakeGenerator.cs` (random walk + clue extraction + uniqueness check)
4. Create `SnakePuzzleData.cs` (cache layer)
5. Add controller endpoints
6. Test: `dotnet build` + verify endpoints return valid puzzles

### Phase 2 — Frontend
7. Create `snake-puzzle.model.ts`
8. Add methods to `puzzle.service.ts`
9. Create `snake-game.service.ts` (full game logic)
10. Create board component (ts + html + scss)
11. Create game component (ts + html + scss)
12. Add routes to `app.routes.ts`
13. Add game card to home page
14. Test: `ng build`
