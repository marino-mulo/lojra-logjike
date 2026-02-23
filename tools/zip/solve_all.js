// Optimized Hamiltonian path solver with better pruning
function solve(rows, cols, start, end, walls, checkpointCells, maxAttempts = 20000000) {
  const total = rows * cols;
  const idx = (r, c) => r * cols + c;
  const rc = (i) => [Math.floor(i / cols), i % cols];

  const wallSet = new Set();
  for (const [r1,c1,r2,c2] of walls) {
    wallSet.add(`${r1},${c1}>${r2},${c2}`);
    wallSet.add(`${r2},${c2}>${r1},${c1}`);
  }

  const adj = new Array(total).fill(null).map(() => []);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i = idx(r, c);
      for (const [nr, nc] of [[r-1,c],[r+1,c],[r,c-1],[r,c+1]]) {
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
        if (wallSet.has(`${r},${c}>${nr},${nc}`)) continue;
        adj[i].push(idx(nr, nc));
      }
    }
  }

  const cpMap = new Map();
  checkpointCells.forEach((c, i) => cpMap.set(c, i));

  const visited = new Uint8Array(total);
  const path = [start];
  visited[start] = 1;
  let found = null;
  let attempts = 0;
  let nextCpIdx = cpMap.has(start) ? 1 : 0;

  function countUnvisitedNeighbors(cell) {
    let count = 0;
    for (const n of adj[cell]) if (!visited[n]) count++;
    return count;
  }

  function dfs(cpProgress) {
    attempts++;
    if (attempts > maxAttempts) return;
    if (found) return;

    if (path.length === total) {
      if (path[path.length-1] === end && cpProgress === checkpointCells.length) {
        found = [...path];
      }
      return;
    }

    const cur = path[path.length-1];
    const remaining = total - path.length;

    // If only one cell left, it must be the end
    if (remaining === 1) {
      if (!visited[end] && adj[cur].includes(end)) {
        visited[end] = 1;
        path.push(end);
        dfs(cpMap.has(end) && cpMap.get(end) === cpProgress ? cpProgress + 1 : cpProgress);
        path.pop();
        visited[end] = 0;
      }
      return;
    }

    // Articulation point check: don't create disconnected unvisited regions
    // Quick check: if end is unvisited, make sure it's still reachable

    for (const next of adj[cur]) {
      if (visited[next]) continue;
      if (next === end && remaining > 1) continue; // don't go to end too early

      // Checkpoint ordering
      if (cpMap.has(next)) {
        if (cpMap.get(next) !== cpProgress) continue;
        visited[next] = 1;
        path.push(next);
        dfs(cpProgress + 1);
        path.pop();
        visited[next] = 0;
      } else {
        visited[next] = 1;
        path.push(next);
        dfs(cpProgress);
        path.pop();
        visited[next] = 0;
      }

      if (found) return;
    }
  }

  dfs(cpMap.has(start) ? 1 : 0);
  console.log(`  (${attempts.toLocaleString()} attempts)`);
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
  if (path.length !== total) { console.log(`FAIL ${name}: len`); return; }
  if (new Set(path).size !== total) { console.log(`FAIL ${name}: dupes`); return; }
  for (let i = 1; i < path.length; i++) {
    const [r1,c1] = rc(path[i-1]); const [r2,c2] = rc(path[i]);
    if (Math.abs(r1-r2)+Math.abs(c1-c2) !== 1) { console.log(`FAIL ${name}: adj step ${i}`); return; }
    if (wallSet.has(`${r1},${c1}>${r2},${c2}`)) { console.log(`FAIL ${name}: wall step ${i}`); return; }
  }
  const numEntries = Object.entries(numbers).sort((a,b) => a[1]-b[1]);
  let cpI = 0;
  for (const cell of path) { if (cpI < numEntries.length && cell === Number(numEntries[cpI][0])) cpI++; }
  if (cpI < numEntries.length) { console.log(`FAIL ${name}: cp order`); return; }
  let interior = 0;
  for (const [idx] of numEntries) { const [r,c] = rc(Number(idx)); if (r>0&&r<rows-1&&c>0&&c<cols-1) interior++; }
  console.log(`OK ${name}: ${rows}x${cols}, ${numEntries.length}cp (${interior} interior), ${walls.length}w`);

  // Print C# format
  console.log(`Numbers = new() {`);
  for (const [idx, val] of numEntries) {
    const [r,c] = rc(Number(idx));
    console.log(`    [${idx}] = ${val},   // (${r},${c})`);
  }
  console.log(`},`);
  console.log(`Walls = [${walls.map(w => `[${w}]`).join(',')}]`);
  console.log(`// Path: ${path.join(',')}`);
  console.log('');
}

function tryConfigs(name, rows, cols, configs) {
  for (const [start, end, walls, cps] of configs) {
    console.log(`${name}: trying start=${start} end=${end}...`);
    const path = solve(rows, cols, start, end, walls, cps);
    if (path) {
      const nums = {}; cps.forEach((c,i) => nums[c] = i+1);
      verify(name, rows, cols, path, nums, walls);
      return path;
    }
  }
  console.log(`${name}: ALL CONFIGS FAILED`);
  return null;
}

// ═══════════════════════════════════════════
// MONDAY 5x5 (7 checkpoints, 0 walls)
// ═══════════════════════════════════════════
tryConfigs("Monday", 5, 5, [
  [12, 18, [], [12, 7, 3, 16, 21, 9, 18]],  // center to interior
  [12, 23, [], [12, 7, 3, 16, 21, 9, 23]],  // center to corner-ish
  [12, 22, [], [12, 8, 1, 16, 22]],          // simpler
  [12, 4,  [], [12, 8, 1, 16, 21, 9, 4]],   // center to corner
  [6,  18, [], [6, 12, 3, 22, 9, 16, 18]],   // interior to interior
  [7,  17, [], [7, 11, 3, 22, 9, 16, 17]],
  [8,  16, [], [8, 12, 0, 21, 14, 23, 16]],
  [12, 8,  [], [12, 6, 2, 23, 15, 9, 8]],
]);

// ═══════════════════════════════════════════
// TUESDAY 6x6 (8 checkpoints, 2 walls)
// Parity: start and end must differ for 6x6
// ═══════════════════════════════════════════
tryConfigs("Tuesday", 6, 6, [
  [14, 21, [[1,3,2,3],[4,1,4,2]], [14, 7, 3, 20, 31, 27, 22, 21]],
  [14, 9,  [[1,3,2,3],[3,4,4,4]], [14, 7, 4, 19, 32, 27, 16, 9]],
  [8,  21, [[0,4,1,4],[3,2,4,2]], [8, 14, 3, 20, 31, 27, 22, 21]],
  [8,  27, [[1,3,2,3],[4,1,4,2]], [8, 13, 2, 20, 31, 16, 22, 27]],
  [7,  22, [[1,4,2,4],[3,1,4,1]], [7, 14, 3, 9, 32, 27, 16, 22]],
  [13, 22, [[0,3,1,3],[4,2,4,3]], [13, 8, 4, 20, 25, 34, 16, 22]],
]);

// ═══════════════════════════════════════════
// WEDNESDAY 6x6 (9 checkpoints, 3 walls)
// ═══════════════════════════════════════════
tryConfigs("Wednesday", 6, 6, [
  [14, 29, [[0,2,1,2],[2,4,3,4],[4,1,5,1]], [14, 7, 3, 20, 31, 27, 16, 5, 29]],
  [14, 21, [[0,3,1,3],[2,1,3,1],[4,4,5,4]], [14, 9, 1, 19, 26, 33, 16, 11, 21]],
  [20, 15, [[0,2,1,2],[3,4,3,5],[4,1,5,1]], [20, 8, 4, 12, 25, 34, 22, 1, 15]],
]);

// ═══════════════════════════════════════════
// THURSDAY 7x7 (9 checkpoints, 4 walls)
// 7x7 odd, no parity constraint
// Use fewer interior constraints for speed
// ═══════════════════════════════════════════
tryConfigs("Thursday", 7, 7, [
  [24, 40, [[1,5,2,5],[3,2,3,3],[5,0,5,1],[6,4,6,5]], [24, 16, 5, 22, 37, 33, 47, 13, 40]],
  [24, 46, [[0,3,1,3],[3,5,4,5],[5,1,5,2],[6,3,6,4]], [24, 9, 3, 22, 30, 44, 34, 47, 46]],
  [17, 31, [[0,4,1,4],[2,1,3,1],[4,5,5,5],[6,2,6,3]], [17, 10, 0, 22, 36, 44, 33, 26, 31]],
  [24, 38, [[1,2,1,3],[3,5,4,5],[5,0,5,1],[6,3,6,4]], [24, 16, 2, 20, 42, 46, 33, 11, 38]],
]);

// ═══════════════════════════════════════════
// FRIDAY 7x7 (10 checkpoints, 5 walls)
// ═══════════════════════════════════════════
tryConfigs("Friday", 7, 7, [
  [24, 38, [[0,2,0,3],[2,4,3,4],[3,1,4,1],[5,3,5,4],[6,0,6,1]], [24, 17, 9, 1, 21, 29, 44, 46, 33, 38]],
  [24, 46, [[0,5,1,5],[2,2,3,2],[3,0,4,0],[5,4,5,5],[6,1,6,2]], [24, 10, 4, 14, 28, 36, 45, 40, 34, 46]],
  [17, 31, [[0,3,0,4],[2,1,3,1],[3,5,4,5],[5,2,5,3],[6,0,6,1]], [17, 9, 0, 22, 35, 43, 46, 33, 26, 31]],
]);

// ═══════════════════════════════════════════
// SATURDAY 8x8 (10 checkpoints, 6 walls)
// 8x8 even: start/end different parity
// 27(3,3) parity=0, 36(4,4) parity=0 -> SAME, bad
// 27(3,3) parity=0, 37(4,5) parity=1 -> different ✓
// ═══════════════════════════════════════════
tryConfigs("Saturday", 8, 8, [
  [27, 37, [[0,3,1,3],[2,5,3,5],[3,1,4,1],[5,3,5,4],[6,0,6,1],[7,5,7,6]],
    [27, 18, 10, 3, 44, 57, 48, 39, 62, 37]],
  [27, 36, [[1,3,1,4],[2,6,3,6],[4,1,4,2],[5,4,6,4],[6,0,7,0],[7,6,7,7]],
    [27, 20, 9, 2, 44, 49, 58, 39, 62, 36]],
]);

// ═══════════════════════════════════════════
// SUNDAY 9x9 (10 checkpoints, 7 walls)
// 9x9 odd, no parity constraint
// ═══════════════════════════════════════════
tryConfigs("Sunday", 9, 9, [
  [40, 50, [[0,4,1,4],[2,2,2,3],[3,6,4,6],[4,1,5,1],[5,4,6,4],[6,7,7,7],[7,2,8,2]],
    [40, 30, 20, 10, 5, 56, 72, 60, 48, 50]],
  [40, 32, [[1,3,1,4],[2,7,3,7],[4,1,4,2],[5,5,6,5],[6,0,7,0],[7,3,7,4],[8,7,8,8]],
    [40, 29, 11, 6, 45, 63, 72, 58, 78, 32]],
]);
