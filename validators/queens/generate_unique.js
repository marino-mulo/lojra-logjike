// Generate Queens puzzles with UNIQUE solutions
// Sizes: Mon=7, Tue=8, Wed=9, Thu=9, Fri=10, Sat=10, Sun=11

const targets = [
  { name: "Monday",    size: 7 },
  { name: "Tuesday",   size: 8 },
  { name: "Wednesday", size: 9 },
  { name: "Thursday",  size: 9 },
  { name: "Friday",    size: 10 },
  { name: "Saturday",  size: 10 },
  { name: "Sunday",    size: 11 },
];

// Find ALL valid queen placements for a given zone layout
// solution[r] = column of queen in row r
// Constraints: 1/row (implicit), 1/col, 1/zone, no adjacent touching
function findAllSolutions(zones, n) {
  const solutions = [];
  const colUsed = new Set();
  const zoneUsed = new Set();
  const placement = new Array(n).fill(-1);

  function backtrack(row) {
    if (row === n) {
      solutions.push([...placement]);
      return;
    }
    for (let col = 0; col < n; col++) {
      if (colUsed.has(col)) continue;
      const zone = zones[row][col];
      if (zoneUsed.has(zone)) continue;
      // Check no touching with previous row's queen
      if (row > 0) {
        const prevCol = placement[row - 1];
        if (Math.abs(col - prevCol) <= 1) continue;
      }
      placement[row] = col;
      colUsed.add(col);
      zoneUsed.add(zone);
      backtrack(row + 1);
      colUsed.delete(col);
      zoneUsed.delete(zone);
      placement[row] = -1;
      // Early exit if we found 2+ solutions (we only need to know if unique)
      if (solutions.length > 1) return;
    }
  }

  backtrack(0);
  return solutions;
}

// Count solutions (stop at 2)
function countSolutions(zones, n) {
  return findAllSolutions(zones, n).length;
}

// Generate a random valid queen placement (1/row, 1/col, no adjacent touching)
function randomQueenPlacement(n) {
  const colUsed = new Set();
  const placement = new Array(n).fill(-1);

  function backtrack(row) {
    const cols = Array.from({length: n}, (_, i) => i).sort(() => Math.random() - 0.5);
    for (const col of cols) {
      if (colUsed.has(col)) continue;
      if (row > 0 && Math.abs(col - placement[row - 1]) <= 1) continue;
      placement[row] = col;
      colUsed.add(col);
      if (row === n - 1) return true;
      if (backtrack(row + 1)) return true;
      colUsed.delete(col);
      placement[row] = -1;
    }
    return false;
  }

  if (backtrack(0)) return placement;
  return null;
}

// Generate zones using BFS expansion from queen positions
function generateZones(n, sol) {
  const zones = Array.from({length: n}, () => Array(n).fill(-1));
  for (let r = 0; r < n; r++) zones[r][sol[r]] = r;

  const queues = [];
  for (let r = 0; r < n; r++) queues.push([[r, sol[r]]]);

  let unassigned = n * n - n;
  const dirs = [[0,1],[0,-1],[1,0],[-1,0]];

  while (unassigned > 0) {
    let progress = false;
    for (let z = 0; z < n; z++) {
      if (queues[z].length === 0) continue;
      let expanded = false;
      const nextQueue = [];
      while (queues[z].length > 0 && !expanded) {
        const [cr, cc] = queues[z].shift();
        const shuffled = [...dirs].sort(() => Math.random() - 0.5);
        for (const [dr, dc] of shuffled) {
          const nr = cr + dr, nc = cc + dc;
          if (nr >= 0 && nr < n && nc >= 0 && nc < n && zones[nr][nc] === -1) {
            zones[nr][nc] = z;
            nextQueue.push([nr, nc]);
            unassigned--;
            expanded = true;
            break;
          }
        }
        if (!expanded) nextQueue.push([cr, cc]);
      }
      queues[z] = [...nextQueue, ...queues[z]];
      if (expanded) progress = true;
    }
    if (!progress) {
      for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
          if (zones[r][c] === -1) {
            for (const [dr, dc] of dirs) {
              const nr = r + dr, nc = c + dc;
              if (nr >= 0 && nr < n && nc >= 0 && nc < n && zones[nr][nc] !== -1) {
                zones[r][c] = zones[nr][nc];
                unassigned--;
                break;
              }
            }
          }
        }
      }
      if (unassigned <= 0) break;
    }
  }
  return zones;
}

// Check all zones are connected
function zonesConnected(zones, n) {
  for (let z = 0; z < n; z++) {
    const cells = [];
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (zones[r][c] === z) cells.push([r, c]);
    if (cells.length === 0) return false;
    const visited = new Set();
    const queue = [cells[0]];
    visited.add(`${cells[0][0]},${cells[0][1]}`);
    while (queue.length > 0) {
      const [cr, cc] = queue.shift();
      for (const [dr, dc] of [[0,1],[0,-1],[1,0],[-1,0]]) {
        const nr = cr + dr, nc = cc + dc, key = `${nr},${nc}`;
        if (nr >= 0 && nr < n && nc >= 0 && nc < n && zones[nr][nc] === z && !visited.has(key)) {
          visited.add(key);
          queue.push([nr, nc]);
        }
      }
    }
    if (visited.size !== cells.length) return false;
  }
  return true;
}

// Check all N zones exist
function hasAllZones(zones, n) {
  const found = new Set();
  for (let r = 0; r < n; r++)
    for (let c = 0; c < n; c++)
      found.add(zones[r][c]);
  return found.size === n;
}

console.log("Generating Queens puzzles with UNIQUE solutions...\n");
console.log("This may take a while for larger sizes...\n");

for (const target of targets) {
  const n = target.size;
  let found = false;
  let attempts = 0;

  while (!found) {
    attempts++;
    if (attempts % 100 === 0) {
      process.stdout.write(`  ${target.name} ${n}x${n}: attempt ${attempts}...\r`);
    }

    // Generate random queen placement
    const sol = randomQueenPlacement(n);
    if (!sol) continue;

    // Generate zones from this placement
    const zones = generateZones(n, sol);
    if (!zonesConnected(zones, n)) continue;
    if (!hasAllZones(zones, n)) continue;

    // Check uniqueness — this is the key step!
    const solCount = countSolutions(zones, n);
    if (solCount !== 1) continue;

    // Found a unique-solution puzzle!
    found = true;
    console.log(`// ${target.name} ${n}x${n} — unique solution (found in ${attempts} attempts)`);
    console.log(`// Solution: [${sol.join(', ')}]`);
    console.log(`new()`);
    console.log(`{`);
    console.log(`    Size = ${n},`);
    console.log(`    Zones = [`);
    for (let r = 0; r < n; r++) {
      console.log(`        [${zones[r].join(',')}]${r < n - 1 ? ',' : ''}`);
    }
    console.log(`    ],`);
    console.log(`    Solution = [${sol.join(', ')}]`);
    console.log(`},`);
    console.log();
  }
}

console.log("Done! All puzzles have unique solutions.");
