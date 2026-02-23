# Unified Game Layout Plan

## Goal
Standardize the layout across all games (Queens, Zip, Fjalëkryq) with a consistent structure.

## Standard Layout (Queens, Zip)

### Top Strip (always visible, same in playing & completed states):
- **Left:** Timer (`00:56`) — shows `--:--` in practice mode
- **Center:** Game Name (absolute positioned)
- **Right:** Reset button ("Pastro") — resets/replays the puzzle

### Board Area:
- Game board (fixed position, never shifts)

### Below Board — PLAYING state:
- Conflict/hint messages (contextual)
- Bottom controls: `Kthe` (undo) | `Kontrollo` (check) | `Ndihmë` (hint)

### Below Board — COMPLETED state:
- Completed card showing time (NO "Luaj përsëri" button — top-right "Pastro" serves as replay)

## Fjalëkryq Exception Layout

### Top Strip:
- **Left:** Timer
- **Center:** "Fjalëkryq" (absolute positioned)
- **Right:** Swap counter (shkëmbime)

### Below Board:
- Bottom controls: `Fillo përsëri` (reset) | `Ndihmë` (hint, 10s cooldown)

## Changes Per File

### 1. Queens (`queens.component.html`)
- Top-right "Pastro" button stays (already there) — make it always call `onReset()`
- Remove "Luaj përsëri" button from completed card
- Completed card just shows time, no button
- Bottom controls stay as-is (Kthe, Kontrollo, Ndihmë) — only shown when NOT completed

### 2. Zip (`zip.component.html`)
- Same as Queens — "Pastro" already in top-right
- Remove "Luaj përsëri" from completed card
- Bottom controls (Kthe, Ndihmë) — only shown when NOT completed

### 3. Fjalëkryq (`wordle7.component.html`)
- Top strip: Left=Timer, Center=Fjalëkryq, Right=Swap counter (already done)
- Remove the standalone "Fillo përsëri" button below board
- Add bottom controls: `Fillo përsëri` (reset) + `Ndihmë` (hint)
- Add hint system to `wordle7-game.service.ts` with 10s cooldown
  - Hint: find a wrong letter and swap it to correct position
  - Show hint message for 4s
  - 10s cooldown between hints

### 4. Fjalëkryq SCSS
- Keep layout stable (min-height on top-strip, visibility hidden for replay)
- Add bottom-controls styling (reuse existing pattern)

### 5. Fjalëkryq Game Service (`wordle7-game.service.ts`)
- Add hint signals: `hintMessage`, `hintCooldown`, `hintCooldownRemaining`, `canHint`
- Add `hint()` method: finds a wrongly-placed letter, swaps it to correct position
- 10s cooldown (not 5s like other games)
- Hint message visible for 4s
