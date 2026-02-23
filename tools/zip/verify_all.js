// Verify ALL 7 puzzles match exactly what's in ZipPuzzleData.cs
function verify(name, rows, cols, path, numbers, walls) {
  const total = rows * cols;
  const rc = (i) => [Math.floor(i / cols), i % cols];
  const wallSet = new Set();
  for (const [r1,c1,r2,c2] of walls) {
    wallSet.add(`${r1},${c1}>${r2},${c2}`);
    wallSet.add(`${r2},${c2}>${r1},${c1}`);
  }

  // Check 1: path length = total cells
  if (path.length !== total) {
    console.log(`❌ ${name}: path length ${path.length} != ${total} cells`);
    return false;
  }

  // Check 2: all cells unique
  if (new Set(path).size !== total) {
    console.log(`❌ ${name}: duplicate cells in path`);
    return false;
  }

  // Check 3: every step is adjacent (horizontal/vertical)
  for (let i = 1; i < path.length; i++) {
    const [r1,c1] = rc(path[i-1]);
    const [r2,c2] = rc(path[i]);
    const dist = Math.abs(r1-r2) + Math.abs(c1-c2);
    if (dist !== 1) {
      console.log(`❌ ${name}: step ${i} not adjacent: cell ${path[i-1]}(${r1},${c1}) → ${path[i]}(${r2},${c2}), dist=${dist}`);
      return false;
    }
  }

  // Check 4: no step crosses a wall
  for (let i = 1; i < path.length; i++) {
    const [r1,c1] = rc(path[i-1]);
    const [r2,c2] = rc(path[i]);
    if (wallSet.has(`${r1},${c1}>${r2},${c2}`)) {
      console.log(`❌ ${name}: step ${i} crosses wall: (${r1},${c1}) → (${r2},${c2})`);
      return false;
    }
  }

  // Check 5: checkpoints visited in order
  const numEntries = Object.entries(numbers).sort((a,b) => a[1] - b[1]);
  let cpI = 0;
  for (const cell of path) {
    if (cpI < numEntries.length && cell === Number(numEntries[cpI][0])) {
      cpI++;
    }
  }
  if (cpI < numEntries.length) {
    console.log(`❌ ${name}: checkpoints not visited in order. Got through ${cpI}/${numEntries.length}`);
    // Show which checkpoint failed
    for (let j = 0; j < numEntries.length; j++) {
      const cellIdx = Number(numEntries[j][0]);
      const posInPath = path.indexOf(cellIdx);
      const [r,c] = rc(cellIdx);
      console.log(`   cp${numEntries[j][1]}: cell ${cellIdx} (${r},${c}) at path position ${posInPath}`);
    }
    return false;
  }

  // Check 6: path starts at checkpoint 1
  const startCell = Number(numEntries[0][0]);
  if (path[0] !== startCell) {
    console.log(`❌ ${name}: path starts at ${path[0]} but checkpoint 1 is at ${startCell}`);
    return false;
  }

  // Check 7: path ends at last checkpoint
  const endCell = Number(numEntries[numEntries.length-1][0]);
  if (path[path.length-1] !== endCell) {
    console.log(`❌ ${name}: path ends at ${path[path.length-1]} but last checkpoint is at ${endCell}`);
    return false;
  }

  // Count interior checkpoints
  let interior = 0;
  for (const [idx] of numEntries) {
    const [r,c] = rc(Number(idx));
    if (r > 0 && r < rows-1 && c > 0 && c < cols-1) interior++;
  }

  console.log(`✅ ${name}: ${rows}×${cols}, ${numEntries.length} checkpoints (${interior} interior), ${walls.length} walls — ALL CHECKS PASSED`);
  return true;
}

// ====== Monday 5×5 ======
verify("Day 0 — Monday", 5, 5,
  [12,7,8,13,18,23,24,19,14,9,4,3,2,1,0,5,6,11,10,15,20,21,16,17,22],
  {12:1, 18:2, 4:3, 6:4, 22:5},
  []
);

// ====== Tuesday 6×6 ======
verify("Day 1 — Tuesday", 6, 6,
  [7,1,0,6,12,18,19,13,14,8,2,3,4,5,11,10,9,15,21,20,26,25,24,30,31,32,33,27,28,34,35,29,23,17,16,22],
  {7:1, 19:2, 8:3, 9:4, 20:5, 33:6, 17:7, 22:8},
  [[0,3,1,3],[3,4,4,4]]
);

// ====== Wednesday 6×6 ======
verify("Day 2 — Wednesday", 6, 6,
  [14,13,7,8,9,3,2,1,0,6,12,18,19,20,26,25,24,30,31,32,33,27,21,15,16,10,4,5,11,17,23,22,28,34,35,29],
  {14:1, 7:2, 9:3, 12:4, 20:5, 25:6, 27:7, 10:8, 29:9},
  [[0,2,1,2],[2,4,3,4],[4,1,5,1]]
);

// ====== Thursday 7×7 ======
verify("Day 3 — Thursday", 7, 7,
  [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46],
  {24:1, 16:2, 27:3, 19:4, 6:5, 0:6, 42:7, 23:8, 46:9},
  [[0,3,1,3],[3,5,4,5],[5,1,5,2],[6,3,6,4]]
);

// ====== Friday 7×7 ======
verify("Day 4 — Friday", 7, 7,
  [0,7,14,21,28,35,42,43,36,29,22,15,8,1,2,9,16,23,30,37,44,45,38,39,46,47,40,33,32,31,24,25,18,17,10,3,4,11,12,5,6,13,20,19,26,27,34,41,48],
  {0:1, 9:2, 16:3, 23:4, 30:5, 38:6, 46:7, 32:8, 19:9, 48:10},
  [[2,3,3,3],[4,1,4,2]]
);

// ====== Saturday 8×8 ======
verify("Day 5 — Saturday", 8, 8,
  [0,8,16,24,32,40,48,56,57,49,41,33,25,17,9,1,2,10,18,26,34,42,50,58,59,51,43,35,27,19,11,3,4,12,20,28,36,44,52,60,61,53,45,37,29,21,13,5,6,7,15,14,22,23,31,30,38,39,47,46,54,55,63,62],
  {0:1, 41:2, 9:3, 18:4, 27:5, 36:6, 45:7, 37:8, 54:9, 62:10},
  []
);

// ====== Sunday 9×9 ======
verify("Day 6 — Sunday", 9, 9,
  [0,9,18,27,36,45,54,63,72,73,64,55,46,37,28,19,10,1,2,11,20,29,38,39,30,21,12,3,4,13,22,23,14,5,6,15,24,33,42,41,32,31,40,49,58,59,50,51,60,61,52,43,34,25,16,7,8,17,26,35,44,53,62,71,70,69,68,67,66,57,48,47,56,65,74,75,76,77,78,79,80],
  {0:1, 10:2, 20:3, 30:4, 40:5, 50:6, 60:7, 70:8, 48:9, 80:10},
  [[2,4,3,4],[5,3,5,4]]
);

console.log("\n=== VERIFICATION COMPLETE ===");
