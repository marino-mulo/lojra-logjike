// Puzzle verifier
function verify(name, rows, cols, path, numbers, walls) {
  const total = rows * cols;
  const rc = (i) => [Math.floor(i / cols), i % cols];
  const wallSet = new Set();
  for (const [r1,c1,r2,c2] of walls) {
    wallSet.add(`${r1},${c1}>${r2},${c2}`);
    wallSet.add(`${r2},${c2}>${r1},${c1}`);
  }

  if (path.length !== total) {
    console.log(`FAIL ${name}: path length ${path.length} != ${total} cells`);
    return false;
  }

  const visited = new Set(path);
  if (visited.size !== total) {
    console.log(`FAIL ${name}: ${visited.size} unique cells != ${total}`);
    return false;
  }

  for (let i = 1; i < path.length; i++) {
    const [r1,c1] = rc(path[i-1]);
    const [r2,c2] = rc(path[i]);
    const dist = Math.abs(r1-r2) + Math.abs(c1-c2);
    if (dist !== 1) {
      console.log(`FAIL ${name}: step ${i-1}->${i} (cell ${path[i-1]}(${r1},${c1})->${path[i]}(${r2},${c2})) dist=${dist}`);
      return false;
    }
    if (wallSet.has(`${r1},${c1}>${r2},${c2}`)) {
      console.log(`FAIL ${name}: step ${i} crosses wall (${r1},${c1})->(${r2},${c2})`);
      return false;
    }
  }

  const numEntries = Object.entries(numbers).sort((a,b) => a[1] - b[1]);
  let cpIdx = 0;
  for (let i = 0; i < path.length; i++) {
    if (cpIdx < numEntries.length && path[i] === Number(numEntries[cpIdx][0])) {
      cpIdx++;
    }
  }
  if (cpIdx < numEntries.length) {
    console.log(`FAIL ${name}: checkpoints not visited in order (got ${cpIdx}/${numEntries.length})`);
    return false;
  }

  const cp1 = numEntries[0];
  if (path[0] !== Number(cp1[0])) {
    console.log(`FAIL ${name}: path starts at ${path[0]} but checkpoint 1 is at ${cp1[0]}`);
    return false;
  }

  const cpLast = numEntries[numEntries.length - 1];
  if (path[path.length-1] !== Number(cpLast[0])) {
    console.log(`FAIL ${name}: path ends at ${path[path.length-1]} but last checkpoint is at ${cpLast[0]}`);
    return false;
  }

  // Check parity for even grids
  if (rows % 2 === 0 && cols % 2 === 0) {
    const [sr,sc] = rc(path[0]);
    const [er,ec] = rc(path[path.length-1]);
    const sp = (sr+sc) % 2;
    const ep = (er+ec) % 2;
    if (sp === ep) {
      console.log(`WARN ${name}: even grid ${rows}x${cols} but start/end same parity (${sp}). This is impossible!`);
    }
  }

  let interior = 0, edge = 0;
  for (const [idx, val] of numEntries) {
    const [r,c] = rc(Number(idx));
    if (r > 0 && r < rows-1 && c > 0 && c < cols-1) interior++;
    else edge++;
  }

  console.log(`OK ${name}: ${rows}x${cols}, ${numEntries.length} checkpoints (${interior} interior, ${edge} edge), ${walls.length} walls`);
  return true;
}

// ═══════════════════════════════════════════
// MONDAY 5x5 (25 cells, 7 checkpoints, 0 walls)
// Start at 12(2,2) center, end at 19(3,4) interior
// ═══════════════════════════════════════════
//  0  1  2  3  4
//  5  6  7  8  9
// 10 11 12 13 14
// 15 16 17 18 19
// 20 21 22 23 24
const monPath = [
  12, 11, 10, 5, 0, 1, 6, 7, 8, 3, 2,
  13, 14, 9, 4,
  18, 17, 16, 15, 20, 21, 22, 23, 24, 19
];
verify("Monday", 5, 5, monPath, {12:1, 5:2, 8:3, 14:4, 17:5, 21:6, 19:7}, []);

// ═══════════════════════════════════════════
// TUESDAY 6x6 (36 cells, 8 checkpoints, 2 walls)
// Start at 8(1,2) interior, end at 29(4,5)
// ═══════════════════════════════════════════
//  0  1  2  3  4  5
//  6  7  8  9 10 11
// 12 13 14 15 16 17
// 18 19 20 21 22 23
// 24 25 26 27 28 29
// 30 31 32 33 34 35
const tuePath = [
  8, 7, 6, 0, 1, 2, 3, 9, 15, 14, 13, 19, 18, 12,
  16, 10, 4, 5, 11, 17, 23, 22, 21, 20, 26, 25, 24, 30, 31, 32, 33, 27, 28, 34, 35, 29
];
verify("Tuesday", 6, 6, tuePath, {8:1, 2:2, 15:3, 12:4, 10:5, 23:6, 26:7, 29:8}, [[3,3,3,4],[4,3,5,3]]);

// ═══════════════════════════════════════════
// WEDNESDAY 6x6 (36 cells, 9 checkpoints, 3 walls)
// Start at 14(2,2) interior, end at 23(3,5) edge
// 14 parity = (2+2)%2 = 0, 23 parity = (3+5)%2 = 0... same! Bad for 6x6
// Try: start 14(2,2) parity=0, end 29(4,5) parity=1 ✓
// ═══════════════════════════════════════════
const wedPath = [
  14, 8, 2, 1, 0, 6, 7, 13, 12, 18, 19, 25, 24, 30, 31, 32, 26, 20, 21, 15, 9, 3, 4, 10, 16, 22, 23, 17, 11, 5, 27, 33, 34, 28, 35, 29
];
// step 5->27: 5(0,5)->27(4,3) FAIL. Let me fix.
// After 11->5: 5 is (0,5). Need to get to 27 somehow. Not adjacent.
// Redesign ending:
// ...17, 11, 5, 4, 10, 16, 22, 28, 34, 33, 27, 21, 15, 9, 3
// but 15 and 21 already visited...

// Let me try a completely different path for Wednesday
const wedPath2 = [
  14, 13, 7, 1, 0, 6, 12, 18, 19, 25, 24, 30, 31, 32, 26, 20, 21, 27, 33, 34, 28, 22, 16, 10, 4, 3, 9, 15, 8, 2,
  11, 5, 17, 23, 29, 35
];
// step 15->8: (2,3)->(1,2) dist=2 FAIL
// step 8->2: (1,2)->(0,2) OK

// Try again more carefully:
const wedPath3 = [
  14, 13, 7, 1, 0, 6, 12, 18, 19, 25, 24, 30, 31, 32, 26, 20, 21, 27, 33, 34, 28, 22, 16, 10, 9, 3, 4, 5, 11, 17, 23, 29, 35,
  15, 8, 2
];
// step 35->15: (5,5)->(2,3) FAIL
// I need 35 to connect to something unvisited. After 35, remaining: 2, 8, 15
// 35(5,5)->29 visited. Dead end.

// Complete redesign for Wednesday:
const wedPath4 = [
  14, 15, 9, 3, 2, 8, 7, 1, 0, 6, 12, 13, 19, 18, 24, 25, 31, 30,
  32, 33, 27, 26, 20, 21, 22, 16, 10, 4, 5, 11, 17, 23, 29, 28, 34, 35
];
verify("Wednesday", 6, 6, wedPath4, {14:1, 3:2, 7:3, 13:4, 24:5, 32:6, 20:7, 10:8, 35:9}, [[1,3,1,4],[3,2,3,3],[4,4,5,4]]);

// ═══════════════════════════════════════════
// THURSDAY 7x7 (49 cells, 9 checkpoints, 4 walls)
// Start at 17(2,3) interior center, end at 31(4,3) interior center
// ═══════════════════════════════════════════
//  0  1  2  3  4  5  6
//  7  8  9 10 11 12 13
// 14 15 16 17 18 19 20
// 21 22 23 24 25 26 27
// 28 29 30 31 32 33 34
// 35 36 37 38 39 40 41
// 42 43 44 45 46 47 48
const thuPath = [
  17, 16, 15, 14, 7, 8, 9, 10, 3, 2, 1, 0,
  11, 4, 5, 6, 13, 12, 19, 18,
  24, 23, 22, 21, 28, 29, 30, 37, 36, 35, 42, 43, 44, 45, 38, 39, 32, 33,
  26, 25,
  46, 47, 40, 41, 34, 27, 20, 48, 31
];
// step 25->46: (3,4)->(6,4) dist=3 FAIL

// Redesign Thursday:
const thuPath2 = [
  17, 16, 15, 14, 7, 0, 1, 2, 3, 10, 9, 8,
  11, 4, 5, 6, 13, 12, 19, 18,
  25, 24, 23, 22, 21, 28, 29, 30, 37, 36, 35, 42, 43, 44, 45, 46, 39, 38, 31, 32, 33,
  26, 27, 20,
  34, 41, 48, 47, 40
];
// step 7->0: (1,0)->(0,0) ✓
// step 33->26: (4,5)->(3,5) ✓
// step 20->34: (2,6)->(4,6) dist=2 FAIL

const thuPath3 = [
  17, 16, 15, 14, 7, 0, 1, 2, 3, 10, 9, 8,
  11, 4, 5, 6, 13, 12, 19, 18,
  25, 24, 23, 22, 21, 28, 29, 30, 37, 36, 35, 42, 43, 44, 45, 46, 39, 38, 31, 32, 33,
  26, 27, 34, 41, 48, 47, 40, 20
];
// step 40->20: (5,5)->(2,6) dist=4 FAIL

const thuPath4 = [
  17, 16, 15, 14, 7, 0, 1, 2, 3, 10, 9, 8,
  11, 4, 5, 6, 13, 20, 19, 12,
  18, 25, 24, 23, 22, 21, 28, 29, 30, 37, 36, 35, 42, 43, 44, 45, 38, 31, 32, 39, 46, 47, 48, 41, 34, 33,
  26, 27, 40
];
verify("Thursday", 7, 7, thuPath4, {17:1, 0:2, 10:3, 11:4, 20:5, 22:6, 42:7, 38:8, 40:9}, [[0,3,0,4],[2,4,3,4],[4,1,4,2],[5,5,6,5]]);

// ═══════════════════════════════════════════
// FRIDAY 7x7 (49 cells, 10 checkpoints, 5 walls)
// Start at 24(3,3) dead center, end at 40(5,5) interior
// ═══════════════════════════════════════════
const friPath = [
  24, 23, 16, 15, 8, 9, 10, 3, 2, 1, 0, 7, 14, 21, 22, 29, 28,
  35, 36, 43, 42,
  30, 37, 44, 45, 38, 31, 32, 25, 18, 11, 4, 5, 6, 13, 20, 27,
  26, 19, 12,
  17, 39, 46, 47, 48, 41, 34, 33,
  46
];
// step 12->17: (1,5)->(2,3) dist=3 FAIL. Too messy.

// Friday - completely fresh
const friPath2 = [
  24, 17, 18, 11, 4, 3, 10, 9, 2, 1, 0, 7, 8, 15, 16, 23, 22, 21, 14,
  5, 6, 13, 20, 19, 12,
  25, 26, 27, 34, 33, 32, 31, 30, 37, 38, 39, 46, 45, 44, 43, 42, 35, 36,
  29, 28,
  40, 41, 48, 47,
];
// 24->17: (3,3)->(2,3) ✓
// 14->5: (2,0)->(0,5) FAIL

// I need to slow down and be systematic. Let me use a helper to build paths.
console.log("\n--- Building paths step by step ---");

// For Friday, let me trace more carefully:
// Start 24(3,3)
// 24->23(3,2)->22(3,1)->21(3,0)->14(2,0)->15(2,1)->16(2,2)->
// 17(2,3)->18(2,4)->19(2,5)->20(2,6)->13(1,6)->6(0,6)->5(0,5)->
// 4(0,4)->11(1,4)->10(1,3)->9(1,2)->8(1,1)->7(1,0)->0(0,0)->
// 1(0,1)->2(0,2)->3(0,3)->12(1,5)->
// wait 3(0,3)->12(1,5) dist=3 FAIL
// 3(0,3) neighbors: 2(0,2) visited, 4(0,4) visited, 10(1,3) visited
// Dead end! Need to rethink.

// Let me try:
// 24->25->26->27->20->13->6->5->4->3->10->11->18->19->12->7->0->1->2->9->8->15->16->23->22->21->14->
// 28->29->30->37->36->35->42->43->44->45->38->31->32->33->34->41->48->47->46->39->17
// check: 14->28: (2,0)->(4,0) dist=2 FAIL

// OK let me try the simplest valid approach:
// 24->25->26->27->34->33->32->31->30->29->28->21->22->23->16->15->14->7->0->1->2->9->8->
// 17->18->11->4->3->10->
// check 23->16: (3,2)->(2,2) ✓
// check 8->17: (1,1)->(2,3) dist=3 FAIL

// I clearly need to be more methodical. Let me write a brute force solver.
console.log("Skipping Friday+ for now, will use solver");
