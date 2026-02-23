// Generate valid Queens puzzles with connected zones
// Each queen must be in its own zone, zones must be connected

// Valid queen placements (no two touching, 1/row, 1/col)
const solutions = [
  { name: "Monday 6x6",    size: 6, sol: [1, 3, 5, 0, 2, 4] },
  { name: "Tuesday 6x6",   size: 6, sol: [2, 5, 3, 0, 4, 1] },
  { name: "Wednesday 7x7", size: 7, sol: [3, 6, 4, 1, 5, 2, 0] },
  { name: "Thursday 7x7",  size: 7, sol: [5, 2, 0, 3, 6, 4, 1] },
  { name: "Friday 8x8",    size: 8, sol: [3, 6, 4, 1, 5, 0, 2, 7] },
  { name: "Saturday 8x8",  size: 8, sol: [4, 7, 5, 2, 0, 6, 3, 1] },
  { name: "Sunday 9x9",    size: 9, sol: [5, 8, 0, 3, 6, 1, 4, 7, 2] },
];

// Verify no-touching constraint
function verifyNoTouching(sol) {
  const n = sol.length;
  for (let r1 = 0; r1 < n; r1++) {
    for (let r2 = r1 + 1; r2 < n; r2++) {
      if (Math.abs(r1 - r2) <= 1 && Math.abs(sol[r1] - sol[r2]) <= 1) {
        return false;
      }
    }
  }
  return true;
}

// Generate zones using BFS expansion from queen positions
function generateZones(n, sol) {
  const zones = Array.from({length: n}, () => Array(n).fill(-1));

  // Place each queen as the seed for its zone
  for (let r = 0; r < n; r++) {
    zones[r][sol[r]] = r; // zone ID = row index of queen
  }

  // BFS expand zones - each zone grows from its queen position
  // Use a round-robin approach so zones grow evenly
  const queues = [];
  for (let r = 0; r < n; r++) {
    queues.push([[r, sol[r]]]);
  }

  let unassigned = n * n - n; // all cells minus queen cells
  const dirs = [[0,1],[0,-1],[1,0],[-1,0]];

  while (unassigned > 0) {
    let progress = false;
    for (let z = 0; z < n; z++) {
      if (queues[z].length === 0) continue;

      // Try to expand this zone by one cell
      let expanded = false;
      const nextQueue = [];

      while (queues[z].length > 0 && !expanded) {
        const [cr, cc] = queues[z].shift();

        // Shuffle directions for variety
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
        if (!expanded) {
          // This frontier cell is surrounded, try next
          nextQueue.push([cr, cc]); // keep for later
        }
      }

      // Merge remaining + new frontier
      queues[z] = [...nextQueue, ...queues[z]];
      if (expanded) progress = true;
    }

    if (!progress) {
      // Fallback: assign remaining cells to nearest zone
      for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
          if (zones[r][c] === -1) {
            // Find adjacent assigned cell
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

// Check zones are connected
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
        const nr = cr + dr, nc = cc + dc;
        const key = `${nr},${nc}`;
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

console.log("Generating Queens puzzles...\n");

for (const p of solutions) {
  if (!verifyNoTouching(p.sol)) {
    console.log(`ERROR: ${p.name} solution has touching queens!`);
    continue;
  }

  // Try until we get connected zones
  let zones;
  let attempts = 0;
  do {
    zones = generateZones(p.size, p.sol);
    attempts++;
  } while (!zonesConnected(zones, p.size) && attempts < 1000);

  if (!zonesConnected(zones, p.size)) {
    console.log(`ERROR: ${p.name} could not generate connected zones after ${attempts} attempts`);
    continue;
  }

  console.log(`// ${p.name} (${p.size}x${p.size}) — attempts: ${attempts}`);
  console.log(`// Solution: [${p.sol.join(', ')}]`);
  console.log(`Size = ${p.size},`);
  console.log(`Zones = [`);
  for (let r = 0; r < p.size; r++) {
    console.log(`    [${zones[r].join(',')}]${r < p.size - 1 ? ',' : ''}`);
  }
  console.log(`],`);
  console.log(`Solution = [${p.sol.join(', ')}]`);
  console.log();
}
