// Solver for Saturday 8x8 - find 10-checkpoint version with interior checkpoints
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
    console.log(`${name}: trying start=${start} end=${end} walls=${walls.length} cps=${cps.length}...`);
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

// Already found that diagonal 8cp works. Now try adding 2 more interior checkpoints.
// Known working path: 0,8,16,24,32,40,48,56,57,49,41,33,25,17,9,1,2,10,18,26,34,42,50,58,59,51,43,35,27,19,11,3,4,12,20,28,36,44,52,60,61,53,45,37,29,21,13,5,6,7,15,14,22,23,31,30,38,39,47,46,54,55,63,62
// Try adding checkpoints that this path already visits in order

// Let me look at the path and pick interior cells that are visited in order between existing checkpoints
// Path order: 0(cp1), ..., 9(cp2), ..., 18(cp3), ..., 27(cp4), ..., 36(cp5), ..., 45(cp6), ..., 54(cp7), ..., 62(cp8)
// Between cp1(0) and cp2(9): visits 8,16,24,32,40,48,56,57,49,41,33,25,17,9
// Could add cp at 17(2,1) interior? or 33(4,1) interior? or 41(5,1)?
// Between cp6(45) and cp7(54): visits 37,29,21,13,5,6,7,15,14,22,23,31,30,38,39,47,46,54
// Could add cp at 37(4,5) interior, 29(3,5) interior, etc.

// Strategy: use the known diagonal pattern but add extra interior checkpoints between existing ones
// that the path naturally passes through. This constrains the solver more.

tryConfigs("Saturday-10cp", 8, 8, [
  // 10 cp: diagonal + 2 extra interior points
  // Add 41(5,1) between cp1-cp2, and 37(4,5) between cp6-cp7
  [0, 62, [], [0, 41, 9, 18, 27, 36, 45, 37, 54, 62]],

  // Add 33(4,1) between cp1-cp2, and 29(3,5) between cp6-cp7
  [0, 62, [], [0, 33, 9, 18, 27, 36, 45, 29, 54, 62]],

  // Scatter more: keep diagonal but insert mid-grid points
  [0, 62, [], [0, 9, 25, 18, 27, 36, 45, 38, 54, 62]],

  // Try with walls to make it more interesting
  [0, 62, [[3,3,3,4]], [0, 9, 18, 27, 36, 45, 38, 54, 46, 62]],
  [0, 62, [[2,5,3,5]], [0, 9, 18, 27, 36, 45, 38, 54, 46, 62]],

  // Different approach: zigzag checkpoints across grid
  [0, 62, [], [0, 10, 17, 26, 35, 44, 53, 36, 27, 62]],

  // Simple: go down-right diagonal then back
  [0, 62, [], [0, 9, 18, 27, 36, 45, 54, 46, 38, 62]],

  // With 1 wall
  [0, 62, [[3,4,4,4]], [0, 9, 18, 27, 36, 45, 54, 46, 38, 62]],
  [0, 62, [[4,3,5,3]], [0, 9, 18, 27, 36, 45, 54, 46, 38, 62]],
]);
