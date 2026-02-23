// Re-verify Wednesday and Thursday with correct walls from solver configs

function verify(name, rows, cols, path, numbers, walls) {
  const total = rows * cols;
  const rc = (i) => [Math.floor(i / cols), i % cols];
  const wallSet = new Set();
  for (const [r1,c1,r2,c2] of walls) {
    wallSet.add(`${r1},${c1}>${r2},${c2}`);
    wallSet.add(`${r2},${c2}>${r1},${c1}`);
  }
  if (path.length !== total) { console.log(`FAIL ${name}: len ${path.length} != ${total}`); return false; }
  if (new Set(path).size !== total) { console.log(`FAIL ${name}: dupes`); return false; }
  for (let i = 1; i < path.length; i++) {
    const [r1,c1] = rc(path[i-1]); const [r2,c2] = rc(path[i]);
    if (Math.abs(r1-r2)+Math.abs(c1-c2) !== 1) { console.log(`FAIL ${name}: adj step ${i}: (${r1},${c1})->(${r2},${c2})`); return false; }
    if (wallSet.has(`${r1},${c1}>${r2},${c2}`)) { console.log(`FAIL ${name}: wall step ${i}: (${r1},${c1})->(${r2},${c2})`); return false; }
  }
  const numEntries = Object.entries(numbers).sort((a,b) => a[1]-b[1]);
  let cpI = 0;
  for (const cell of path) { if (cpI < numEntries.length && cell === Number(numEntries[cpI][0])) cpI++; }
  if (cpI < numEntries.length) { console.log(`FAIL ${name}: cp order ${cpI}/${numEntries.length}`); return false; }
  if (path[0] !== Number(numEntries[0][0])) { console.log(`FAIL ${name}: start`); return false; }
  if (path[path.length-1] !== Number(numEntries[numEntries.length-1][0])) { console.log(`FAIL ${name}: end`); return false; }
  let interior = 0;
  for (const [idx] of numEntries) { const [r,c] = rc(Number(idx)); if (r>0&&r<rows-1&&c>0&&c<cols-1) interior++; }
  console.log(`✅ ${name}: ${rows}x${cols}, ${numEntries.length}cp (${interior} interior), ${walls.length}w`);
  return true;
}

// Wednesday path from solver: 14,13,7,8,9,3,2,1,0,6,12,18,19,20,26,25,24,30,31,32,33,27,21,15,16,10,4,5,11,17,23,22,28,34,35,29
// Solver config line 180: walls [[0,2,1,2],[2,4,3,4],[4,1,5,1]]
console.log("=== WEDNESDAY ===");
console.log("Testing with walls from solver config (line 180):");
verify("Wed-correct", 6, 6,
  [14,13,7,8,9,3,2,1,0,6,12,18,19,20,26,25,24,30,31,32,33,27,21,15,16,10,4,5,11,17,23,22,28,34,35,29],
  {14:1, 7:2, 9:3, 12:4, 20:5, 25:6, 27:7, 10:8, 29:9},
  [[0,2,1,2],[2,4,3,4],[4,1,5,1]]
);

// Thursday path from solver: 24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46
// Which config produced this? Let me check all Thursday configs:
console.log("\n=== THURSDAY ===");

// Config 1: walls [[1,5,2,5],[3,2,3,3],[5,0,5,1],[6,4,6,5]]
console.log("Testing Thursday config 1:");
verify("Thu-cfg1", 7, 7,
  [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46],
  {24:1, 16:2, 27:3, 19:4, 6:5, 0:6, 42:7, 23:8, 46:9},
  [[1,5,2,5],[3,2,3,3],[5,0,5,1],[6,4,6,5]]
);

// Config 2: walls [[0,3,1,3],[3,5,4,5],[5,1,5,2],[6,3,6,4]]
console.log("Testing Thursday config 2:");
verify("Thu-cfg2", 7, 7,
  [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46],
  {24:1, 16:2, 27:3, 19:4, 6:5, 0:6, 42:7, 23:8, 46:9},
  [[0,3,1,3],[3,5,4,5],[5,1,5,2],[6,3,6,4]]
);

// Config 3: walls [[0,4,1,4],[2,1,3,1],[4,5,5,5],[6,2,6,3]]
console.log("Testing Thursday config 3:");
verify("Thu-cfg3", 7, 7,
  [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46],
  {24:1, 16:2, 27:3, 19:4, 6:5, 0:6, 42:7, 23:8, 46:9},
  [[0,4,1,4],[2,1,3,1],[4,5,5,5],[6,2,6,3]]
);

// Config 4: walls [[1,2,1,3],[3,5,4,5],[5,0,5,1],[6,3,6,4]]
console.log("Testing Thursday config 4:");
verify("Thu-cfg4", 7, 7,
  [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46],
  {24:1, 16:2, 27:3, 19:4, 6:5, 0:6, 42:7, 23:8, 46:9},
  [[1,2,1,3],[3,5,4,5],[5,0,5,1],[6,3,6,4]]
);

// Also try with NO walls to see if the path actually needs walls
console.log("Testing Thursday with NO walls:");
verify("Thu-nowalls", 7, 7,
  [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46],
  {24:1, 16:2, 27:3, 19:4, 6:5, 0:6, 42:7, 23:8, 46:9},
  []
);
