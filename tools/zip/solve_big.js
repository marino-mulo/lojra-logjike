// Solver for Fri/Sat/Sun - use simpler checkpoint layouts
function solve(rows, cols, start, end, walls, checkpointCells, maxAttempts = 50000000) {
  const total = rows * cols;
  const idx = (r, c) => r * cols + c;
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

  function dfs(cpProgress) {
    attempts++;
    if (attempts > maxAttempts || found) return;
    if (path.length === total) {
      if (path[path.length-1] === end && cpProgress === checkpointCells.length) found = [...path];
      return;
    }
    const cur = path[path.length-1];
    const remaining = total - path.length;
    if (remaining === 1) {
      if (!visited[end] && adj[cur].includes(end)) {
        const newCp = cpMap.has(end) && cpMap.get(end) === cpProgress ? cpProgress+1 : cpProgress;
        if (newCp === checkpointCells.length) found = [... path, end];
      }
      return;
    }
    for (const next of adj[cur]) {
      if (visited[next] || found) continue;
      if (next === end && remaining > 1) continue;
      if (cpMap.has(next)) {
        if (cpMap.get(next) !== cpProgress) continue;
        visited[next] = 1; path.push(next);
        dfs(cpProgress + 1);
        path.pop(); visited[next] = 0;
      } else {
        visited[next] = 1; path.push(next);
        dfs(cpProgress);
        path.pop(); visited[next] = 0;
      }
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
  for (const [r1,c1,r2,c2] of walls) { wallSet.add(`${r1},${c1}>${r2},${c2}`); wallSet.add(`${r2},${c2}>${r1},${c1}`); }
  if (path.length !== total || new Set(path).size !== total) { console.log(`FAIL ${name}: len/dupes`); return; }
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
  console.log(`Numbers = new() {`);
  for (const [idx, val] of numEntries) { const [r,c] = rc(Number(idx)); console.log(`    [${idx}] = ${val},   // (${r},${c})`); }
  console.log(`},`);
  console.log(`Walls = [${walls.map(w => `[${w}]`).join(',')}]`);
  console.log(`// Path: ${path.join(',')}\n`);
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

// FRIDAY 7x7 - use start/end closer to edges with some interior checkpoints
// Mix: some edge, some interior. Keep constraints moderate.
tryConfigs("Friday", 7, 7, [
  // Start corner-ish, end interior, but pass through interior checkpoints
  [0, 24, [[1,3,2,3],[3,5,4,5],[4,1,5,1],[6,3,6,4]], [0, 10, 18, 15, 30, 38, 44, 33, 47, 24]],
  [0, 48, [[1,2,1,3],[3,0,4,0],[4,5,5,5],[6,2,6,3]], [0, 9, 17, 22, 30, 43, 38, 33, 47, 48]],
  [0, 48, [[1,4,2,4],[3,1,3,2],[5,3,5,4],[6,0,6,1]], [0, 10, 16, 22, 37, 44, 32, 26, 47, 48]],
  // Simpler: edge start, interior checkpoints, edge end
  [0, 48, [], [0, 8, 16, 24, 32, 38, 10, 17, 39, 48]],
  [0, 48, [[2,3,3,3],[4,1,4,2]], [0, 9, 16, 23, 30, 38, 46, 32, 19, 48]],
  // Even simpler walls
  [0, 48, [[2,3,3,3]], [0, 9, 16, 23, 30, 38, 46, 33, 19, 48]],
]);

// SATURDAY 8x8 - start/end different parity
// 0(0,0) parity=0, need end parity=1, e.g. 63(7,7) parity=0 BAD, 62(7,6) parity=1 ✓
tryConfigs("Saturday", 8, 8, [
  [0, 62, [[1,3,2,3],[3,5,4,5],[5,1,5,2],[6,6,7,6]], [0, 11, 19, 28, 37, 52, 44, 25, 57, 62]],
  [0, 62, [[2,3,3,3],[4,5,5,5],[6,1,6,2]], [0, 10, 19, 28, 44, 52, 37, 25, 57, 62]],
  [0, 62, [[2,4,3,4],[5,2,5,3]], [0, 10, 18, 28, 45, 53, 37, 27, 57, 62]],
  // Simpler
  [0, 63, [[1,3,1,4],[4,3,4,4]], [0, 9, 18, 27, 36, 45, 54, 62, 39, 63]],
  // 0 parity=0, 63 parity=0 SAME. Bad. Use 62.
  [1, 62, [[1,4,2,4],[4,2,4,3]], [1, 10, 19, 28, 37, 46, 55, 36, 27, 62]],
  [0, 15, [[2,3,2,4],[5,3,5,4]], [0, 9, 18, 27, 36, 45, 54, 39, 20, 15]],
]);

// SUNDAY 9x9 - large grid, use simple layout with some interior
tryConfigs("Sunday", 9, 9, [
  [0, 80, [], [0, 11, 20, 31, 40, 51, 60, 71, 38, 80]],
  [0, 80, [[2,4,3,4],[5,3,5,4]], [0, 10, 20, 30, 40, 50, 60, 70, 48, 80]],
  [0, 80, [[3,4,4,4]], [0, 10, 20, 30, 40, 50, 60, 70, 49, 80]],
  [0, 80, [], [0, 10, 20, 30, 50, 60, 70, 40, 49, 80]],
]);
