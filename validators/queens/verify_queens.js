// Verify all Queens puzzles are valid + unique solution
// Run: node validators/queens/verify_queens.js

const puzzles = [
  {
    name: "Monday 7x7", size: 7,
    zones: [[2,2,2,2,0,0,0],[3,3,3,2,1,1,1],[3,3,3,2,1,5,5],[3,3,4,4,4,5,5],[6,3,4,4,4,5,5],[6,6,6,6,4,5,5],[6,6,6,6,4,4,4]],
    solution: [4, 6, 3, 0, 2, 5, 1]
  },
  {
    name: "Tuesday 8x8", size: 8,
    zones: [[0,0,0,1,1,1,1,1],[3,2,2,1,2,2,4,1],[3,2,2,2,2,2,4,4],[3,3,3,3,3,7,4,4],[6,6,6,7,7,7,4,4],[6,6,6,7,7,5,5,5],[6,6,6,7,7,7,7,7],[6,6,6,7,7,7,7,7]],
    solution: [0, 3, 1, 4, 7, 5, 2, 6]
  },
  {
    name: "Wednesday 9x9", size: 9,
    zones: [[0,0,0,0,1,1,1,1,1],[0,0,0,1,1,1,1,1,1],[0,0,2,2,2,2,1,1,1],[0,0,0,2,2,2,1,1,3],[4,0,0,2,2,2,3,3,3],[4,0,0,2,2,5,3,3,3],[4,4,4,2,2,5,5,6,6],[4,4,4,7,7,5,5,6,6],[7,7,7,7,7,8,8,6,6]],
    solution: [1, 4, 2, 8, 0, 5, 7, 3, 6]
  },
  {
    name: "Thursday 9x9", size: 9,
    zones: [[3,3,5,5,0,0,1,1,1],[3,3,5,4,4,0,0,2,1],[3,3,5,4,4,4,2,2,2],[3,5,5,4,4,4,4,4,4],[5,5,6,6,6,7,7,4,4],[5,5,6,6,6,7,7,7,7],[8,8,6,6,6,7,7,7,7],[8,8,8,8,7,7,7,7,7],[8,8,8,8,8,8,8,8,8]],
    solution: [4, 8, 6, 0, 7, 1, 3, 5, 2]
  },
  {
    name: "Friday 10x10", size: 10,
    zones: [[2,2,8,8,8,0,0,0,0,0],[2,2,8,1,8,0,0,1,0,0],[2,8,8,1,8,8,1,1,0,0],[8,8,3,1,1,1,1,4,4,4],[8,8,3,3,3,3,4,4,4,4],[8,8,8,3,3,3,4,4,5,5],[8,8,8,3,3,3,3,6,5,5],[8,8,8,8,7,7,7,6,6,5],[8,8,8,8,8,7,7,9,6,5],[8,8,8,8,8,7,7,9,9,5]],
    solution: [5, 3, 0, 2, 6, 9, 7, 4, 1, 8]
  },
  {
    name: "Saturday 10x10", size: 10,
    zones: [[1,1,1,3,3,2,2,2,0,0],[1,1,1,3,3,2,6,2,2,2],[8,8,3,3,5,5,6,4,4,2],[8,3,3,5,5,5,6,4,4,4],[8,8,5,5,5,6,6,4,4,4],[8,8,5,6,6,6,7,7,7,7],[8,8,8,8,6,9,7,7,7,7],[8,8,8,8,9,9,7,7,7,7],[8,8,8,8,9,9,9,9,9,9],[8,8,8,9,9,9,9,9,9,9]],
    solution: [8, 0, 9, 1, 7, 2, 4, 6, 3, 5]
  },
  {
    name: "Sunday 11x11", size: 11,
    zones: [[10,10,10,10,10,10,10,10,0,0,1],[10,10,10,10,10,10,2,2,2,0,1],[10,10,10,10,2,2,2,2,2,0,0],[10,10,10,4,4,4,3,3,3,0,0],[10,10,10,4,6,4,4,3,3,5,5],[10,10,10,6,6,4,4,3,3,5,5],[10,6,6,6,7,7,7,7,5,5,5],[10,10,9,9,9,7,7,7,8,8,8],[10,10,9,9,9,9,8,8,8,8,8],[10,9,9,9,9,9,9,9,9,8,8],[10,10,10,10,9,9,9,9,9,8,8]],
    solution: [8, 10, 4, 6, 3, 9, 1, 5, 7, 2, 0]
  }
];

// Count all valid solutions for a puzzle (backtracking solver)
function countSolutions(zones, n, maxCount) {
  let count = 0;
  const colUsed = new Set();
  const zoneUsed = new Set();
  const placement = new Array(n).fill(-1);

  function backtrack(row) {
    if (row === n) { count++; return; }
    for (let col = 0; col < n; col++) {
      if (colUsed.has(col)) continue;
      const zone = zones[row][col];
      if (zoneUsed.has(zone)) continue;
      if (row > 0 && Math.abs(col - placement[row - 1]) <= 1) continue;
      placement[row] = col;
      colUsed.add(col);
      zoneUsed.add(zone);
      backtrack(row + 1);
      colUsed.delete(col);
      zoneUsed.delete(zone);
      placement[row] = -1;
      if (count >= maxCount) return;
    }
  }

  backtrack(0);
  return count;
}

let allPassed = true;

for (const p of puzzles) {
  const errors = [];
  const n = p.size;
  const sol = p.solution;

  if (sol.length !== n) errors.push(`Solution length ${sol.length} != size ${n}`);

  if (p.zones.length !== n) errors.push(`Zones has ${p.zones.length} rows, expected ${n}`);
  for (let r = 0; r < n; r++) {
    if (p.zones[r] && p.zones[r].length !== n) errors.push(`Zones row ${r} has ${p.zones[r].length} cols`);
  }

  const zoneCounts = new Map();
  for (let r = 0; r < n; r++)
    for (let c = 0; c < n; c++)
      zoneCounts.set(p.zones[r][c], (zoneCounts.get(p.zones[r][c]) || 0) + 1);

  for (let z = 0; z < n; z++) {
    if (!zoneCounts.has(z)) errors.push(`Zone ${z} has no cells`);
  }
  if (zoneCounts.size !== n) errors.push(`Expected ${n} zones, found ${zoneCounts.size}`);

  // Check zones connected
  for (let z = 0; z < n; z++) {
    const cells = [];
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (p.zones[r][c] === z) cells.push([r, c]);
    if (cells.length === 0) continue;
    const visited = new Set();
    const queue = [cells[0]];
    visited.add(`${cells[0][0]},${cells[0][1]}`);
    while (queue.length > 0) {
      const [cr, cc] = queue.shift();
      for (const [dr, dc] of [[0,1],[0,-1],[1,0],[-1,0]]) {
        const nr = cr + dr, nc = cc + dc, key = `${nr},${nc}`;
        if (nr >= 0 && nr < n && nc >= 0 && nc < n && p.zones[nr][nc] === z && !visited.has(key)) { visited.add(key); queue.push([nr, nc]); }
      }
    }
    if (visited.size !== cells.length) errors.push(`Zone ${z} NOT connected (${visited.size}/${cells.length})`);
  }

  // 1 queen per column
  if (new Set(sol).size !== n) errors.push(`Duplicate columns`);

  // 1 queen per zone
  const qz = new Set();
  for (let r = 0; r < n; r++) { const z = p.zones[r][sol[r]]; if (qz.has(z)) errors.push(`Zone ${z} has multiple queens`); qz.add(z); }
  if (qz.size !== n) errors.push(`Queens cover ${qz.size} zones, expected ${n}`);

  // No touching
  for (let r1 = 0; r1 < n; r1++) for (let r2 = r1+1; r2 < n; r2++) {
    if (Math.abs(r1-r2) <= 1 && Math.abs(sol[r1]-sol[r2]) <= 1) errors.push(`Queens (${r1},${sol[r1]}) and (${r2},${sol[r2]}) touching`);
  }

  // Check unique solution
  if (errors.length === 0) {
    const solCount = countSolutions(p.zones, n, 3);
    if (solCount === 0) errors.push(`No solutions found!`);
    else if (solCount > 1) errors.push(`NOT unique: ${solCount}+ solutions found`);
  }

  if (errors.length > 0) {
    console.log(`FAIL: ${p.name}`); errors.forEach(e => console.log(`  - ${e}`)); allPassed = false;
  } else {
    console.log(`PASS: ${p.name} (${n}x${n}, ${n} zones, all connected, UNIQUE solution)`);
  }
}

console.log(allPassed ? '\nAll puzzles PASSED!' : '\nSome puzzles FAILED!');
process.exit(allPassed ? 0 : 1);
