// Hamiltonian path solver for Zip puzzles
// Finds a path visiting all cells from start to end, respecting walls and checkpoint order

function solve(rows, cols, start, end, walls, checkpointCells) {
  const total = rows * cols;
  const rc = (i) => [Math.floor(i / cols), i % cols];
  const idx = (r, c) => r * cols + c;

  // Build wall set
  const wallSet = new Set();
  for (const [r1,c1,r2,c2] of walls) {
    wallSet.add(`${r1},${c1}>${r2},${c2}`);
    wallSet.add(`${r2},${c2}>${r1},${c1}`);
  }

  // Build adjacency list
  const adj = new Array(total).fill(null).map(() => []);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i = idx(r, c);
      const dirs = [[r-1,c],[r+1,c],[r,c-1],[r,c+1]];
      for (const [nr, nc] of dirs) {
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
        if (wallSet.has(`${r},${c}>${nr},${nc}`)) continue;
        adj[i].push(idx(nr, nc));
      }
    }
  }

  // Checkpoint cells in order (indices into path that must appear in sequence)
  const cpSet = new Set(checkpointCells);

  const visited = new Uint8Array(total);
  const path = [start];
  visited[start] = 1;
  let found = null;
  let attempts = 0;

  function dfs() {
    attempts++;
    if (attempts > 50000000) return; // safety limit

    if (path.length === total) {
      if (path[path.length - 1] === end) {
        // Verify checkpoints are in order
        let cpIdx = 0;
        for (const cell of path) {
          if (cpIdx < checkpointCells.length && cell === checkpointCells[cpIdx]) {
            cpIdx++;
          }
        }
        if (cpIdx === checkpointCells.length) {
          found = [...path];
        }
      }
      return;
    }

    if (found) return;

    const cur = path[path.length - 1];

    // Pruning: check if we can still reach the end cell
    // Simple: if only 1 cell left and it's not adjacent to current, skip
    if (path.length === total - 1) {
      if (!adj[cur].includes(end) || visited[end]) return;
    }

    for (const next of adj[cur]) {
      if (visited[next]) continue;

      // Check checkpoint ordering: if next is a checkpoint, it must be the next expected one
      if (cpSet.has(next)) {
        // Find which checkpoint index this is
        const cpPos = checkpointCells.indexOf(next);
        // Count how many checkpoints we've visited so far
        let visitedCps = 0;
        for (const cell of path) {
          if (cpSet.has(cell) && checkpointCells.indexOf(cell) === visitedCps) {
            visitedCps++;
          }
        }
        if (cpPos !== visitedCps) continue; // wrong order
      }

      visited[next] = 1;
      path.push(next);
      dfs();
      if (found) return;
      path.pop();
      visited[next] = 0;
    }
  }

  dfs();
  return found;
}

function verify(name, rows, cols, path, numbers, walls) {
  const total = rows * cols;
  const rc = (i) => [Math.floor(i / cols), i % cols];
  const wallSet = new Set();
  for (const [r1,c1,r2,c2] of walls) {
    wallSet.add(`${r1},${c1}>${r2},${c2}`);
    wallSet.add(`${r2},${c2}>${r1},${c1}`);
  }
  if (path.length !== total) { console.log(`FAIL ${name}: len ${path.length}!=${total}`); return false; }
  const visited = new Set(path);
  if (visited.size !== total) { console.log(`FAIL ${name}: dupes`); return false; }
  for (let i = 1; i < path.length; i++) {
    const [r1,c1] = rc(path[i-1]);
    const [r2,c2] = rc(path[i]);
    if (Math.abs(r1-r2)+Math.abs(c1-c2) !== 1) { console.log(`FAIL ${name}: step ${i}`); return false; }
    if (wallSet.has(`${r1},${c1}>${r2},${c2}`)) { console.log(`FAIL ${name}: wall at step ${i}`); return false; }
  }
  const numEntries = Object.entries(numbers).sort((a,b) => a[1]-b[1]);
  let cpIdx = 0;
  for (const cell of path) {
    if (cpIdx < numEntries.length && cell === Number(numEntries[cpIdx][0])) cpIdx++;
  }
  if (cpIdx < numEntries.length) { console.log(`FAIL ${name}: cp order`); return false; }
  if (path[0] !== Number(numEntries[0][0])) { console.log(`FAIL ${name}: wrong start`); return false; }
  if (path[path.length-1] !== Number(numEntries[numEntries.length-1][0])) { console.log(`FAIL ${name}: wrong end`); return false; }

  let interior = 0;
  for (const [idx] of numEntries) {
    const [r,c] = rc(Number(idx));
    if (r > 0 && r < rows-1 && c > 0 && c < cols-1) interior++;
  }
  console.log(`OK ${name}: ${rows}x${cols}, ${numEntries.length}cp (${interior} interior), ${walls.length}w`);

  // Print grid with path order
  const grid = [];
  for (let r = 0; r < rows; r++) {
    const row = [];
    for (let c = 0; c < cols; c++) {
      const cell = r * cols + c;
      const pos = path.indexOf(cell);
      const num = numbers[cell];
      if (num !== undefined) row.push(`[${String(num).padStart(2)}]`);
      else row.push(` ${String(pos+1).padStart(2)} `);
    }
    grid.push(row.join(' '));
  }
  console.log(grid.join('\n'));
  console.log('');
  return true;
}

// ═══════════════════════════════════════════
// MONDAY 5x5 (easy, 0 walls, 7 checkpoints)
// Start at 12(2,2) center, checkpoints in middle
// ═══════════════════════════════════════════
console.log("Solving Monday 5x5...");
const monCps = [12, 7, 3, 16, 21, 9, 23]; // interior-heavy
const monPath = solve(5, 5, 12, 23, [], monCps);
if (monPath) {
  const monNums = {}; monCps.forEach((c,i) => monNums[c] = i+1);
  verify("Monday", 5, 5, monPath, monNums, []);
} else {
  console.log("Monday: no solution found, trying alt...");
  const monCps2 = [12, 8, 2, 16, 22, 19];
  const monPath2 = solve(5, 5, 12, 19, [], monCps2);
  if (monPath2) {
    const monNums2 = {}; monCps2.forEach((c,i) => monNums2[c] = i+1);
    verify("Monday-alt", 5, 5, monPath2, monNums2, []);
  } else {
    console.log("Monday: no alt solution either");
  }
}

// ═══════════════════════════════════════════
// TUESDAY 6x6 (easy-medium, 2 walls, 8 checkpoints)
// For 6x6 even grid: start/end must have different parity
// 8(1,2) parity=1(odd), end at 21(3,3) parity=0(even) -> different ✓
// ═══════════════════════════════════════════
console.log("Solving Tuesday 6x6...");
const tueWalls = [[1,4,2,4],[3,2,4,2]];
const tueCps = [8, 15, 20, 3, 10, 25, 33, 21]; // mix of interior and edge
const tuePath = solve(6, 6, 8, 21, tueWalls, tueCps);
if (tuePath) {
  const tueNums = {}; tueCps.forEach((c,i) => tueNums[c] = i+1);
  verify("Tuesday", 6, 6, tuePath, tueNums, tueWalls);
} else {
  console.log("Tuesday: no solution, trying alt checkpoints...");
  const tueCps2 = [8, 14, 3, 20, 31, 27, 22, 35];
  const tuePath2 = solve(6, 6, 8, 35, tueWalls, tueCps2);
  if (tuePath2) {
    const tueNums2 = {}; tueCps2.forEach((c,i) => tueNums2[c] = i+1);
    verify("Tuesday-alt", 6, 6, tuePath2, tueNums2, tueWalls);
  } else {
    console.log("Tuesday: no alt solution either");
  }
}

// ═══════════════════════════════════════════
// WEDNESDAY 6x6 (medium, 3 walls, 9 checkpoints)
// Start 14(2,2) parity=0, end 21(3,3) parity=0 -> same! Bad.
// Start 14(2,2) parity=0, end 25(4,1) parity=1 -> different ✓
// ═══════════════════════════════════════════
console.log("Solving Wednesday 6x6...");
const wedWalls = [[0,2,1,2],[2,4,3,4],[4,1,5,1]];
const wedCps = [14, 9, 1, 19, 26, 33, 16, 11, 25];
const wedPath = solve(6, 6, 14, 25, wedWalls, wedCps);
if (wedPath) {
  const wedNums = {}; wedCps.forEach((c,i) => wedNums[c] = i+1);
  verify("Wednesday", 6, 6, wedPath, wedNums, wedWalls);
} else {
  console.log("Wednesday: no solution, trying alt...");
  const wedCps2 = [14, 7, 3, 20, 31, 27, 16, 5, 29];
  const wedPath2 = solve(6, 6, 14, 29, wedWalls, wedCps2);
  if (wedPath2) {
    const wedNums2 = {}; wedCps2.forEach((c,i) => wedNums2[c] = i+1);
    verify("Wednesday-alt", 6, 6, wedPath2, wedNums2, wedWalls);
  } else {
    console.log("Wednesday: no alt solution either");
  }
}

// ═══════════════════════════════════════════
// THURSDAY 7x7 (medium, 4 walls, 9 checkpoints)
// 7x7 odd grid, no parity constraint
// Start 24(3,3) dead center, end 40(5,5) interior
// ═══════════════════════════════════════════
console.log("Solving Thursday 7x7...");
const thuWalls = [[0,3,0,4],[2,5,3,5],[4,2,4,3],[5,0,6,0]];
const thuCps = [24, 10, 2, 19, 30, 43, 38, 33, 40];
const thuPath = solve(7, 7, 24, 40, thuWalls, thuCps);
if (thuPath) {
  const thuNums = {}; thuCps.forEach((c,i) => thuNums[c] = i+1);
  verify("Thursday", 7, 7, thuPath, thuNums, thuWalls);
} else {
  console.log("Thursday: no solution (may need more time for 7x7)");
}
