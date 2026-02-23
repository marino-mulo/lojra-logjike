// Solver specifically for Saturday 8x8
function solve(rows, cols, start, end, walls, checkpointCells, maxAttempts = 80000000) {
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
    console.log(`${name}: trying start=${start} end=${end} walls=${walls.length}...`);
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

// 8x8 = 64 cells. Parity: 0(0,0)=even. Need start/end with different parity.
// Cell parity = (r+c) % 2. 0 = even. Need end with odd parity.
// Options: start=0(even), end=odd-parity cell

// Strategy: Use diagonal-ish checkpoints with fewer constraints
// Try with fewer interior checkpoints, more edge ones, minimal walls
tryConfigs("Saturday", 8, 8, [
  // Diagonal checkpoints: 0, 9, 18, 27, 36, 45, 54, 63 - but 63 is even!
  // 0(0,0)even → need end odd. 62(7,6)=odd ✓, 57(7,1)=odd ✓, 55(6,7)=odd ✓

  // Try: mostly diagonal, end at 55(6,7), no walls
  [0, 55, [], [0, 9, 18, 27, 36, 45, 54, 62, 41, 55]],

  // Try: serpentine-ish with interior, minimal walls
  [0, 55, [[3,3,3,4]], [0, 9, 18, 27, 36, 45, 54, 62, 41, 55]],

  // Start 0, end 7(0,7) odd. Simple top-right corner end.
  [0, 7, [], [0, 9, 18, 27, 36, 45, 54, 62, 41, 7]],

  // Start 0(even), end 1(0,1) odd. Adjacent end.
  [0, 1, [], [0, 17, 26, 35, 44, 53, 62, 48, 33, 1]],

  // Fewer checkpoints with interior ones
  [0, 63, [], [0, 9, 18, 27, 36, 45, 54, 63]], // 8 cp, diagonal, no walls
  // Wait, 0 and 63 both even. Bad.

  // 8 checkpoints diagonal, end 62
  [0, 62, [], [0, 9, 18, 27, 36, 45, 54, 62]], // only 8 cp

  // Try with 1 wall, more spread out checkpoints
  [0, 62, [[3,4,4,4]], [0, 10, 19, 28, 37, 46, 55, 34, 21, 62]],

  // Edge start, interior checkpoints, edge end, 1 wall
  [0, 62, [[4,3,4,4]], [0, 11, 18, 27, 36, 45, 54, 33, 22, 62]],

  // Very simple: start 0, end 62, checkpoints along edges + some interior
  [0, 62, [[3,3,4,3]], [0, 7, 15, 18, 27, 36, 45, 54, 41, 62]],

  // Minimal: 8 cp, 1 wall
  [0, 62, [[4,4,5,4]], [0, 9, 18, 27, 45, 54, 36, 62]],
]);
