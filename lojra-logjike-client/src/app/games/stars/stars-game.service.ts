import { Injectable, signal, computed } from '@angular/core';
import { StarsPuzzle } from '../../core/models/stars-puzzle.model';

export const EMPTY = 0;
export const MARK_X = 1;
export const STAR = 2;
export const AUTO_X = 3;

@Injectable()
export class StarsGameService {
  private size = 0;
  private zones: number[][] = [];
  private solution: number[][] = []; // solution[row] = [col1, col2]

  readonly board = signal<number[][]>([]);
  readonly gameWon = signal(false);
  readonly timerSeconds = signal(0);
  readonly timerDisabled = signal(false);
  readonly isRestored = signal(false);
  readonly conflictCells = signal<{ row: number; col: number }[]>([]);
  readonly hintCells = signal<{ row: number; col: number }[]>([]);
  readonly hintMessage = signal('');
  readonly hintCooldown = signal(false);
  readonly hintCooldownRemaining = signal(0);

  private hintTimeout: ReturnType<typeof setTimeout> | null = null;
  private hintCooldownInterval: ReturnType<typeof setInterval> | null = null;
  private timerInterval: ReturnType<typeof setInterval> | null = null;

  private readonly zoneNames = [
    'e kuqe', 'portokalli', 'e verdhë', 'e gjelbër', 'mentë',
    'blu', 'indigo', 'vjollcë', 'rozë', 'pjeshkë', 'limoni', 'moçaliku'
  ];

  private history: number[][][] = [];
  private readonly historyLength = signal(0);

  readonly starsCount = computed(() => {
    let count = 0;
    for (const row of this.board()) for (const cell of row) if (cell === STAR) count++;
    return count;
  });

  readonly canUndo = computed(() => this.historyLength() > 0 && !this.gameWon());
  readonly canHint = computed(() => !this.gameWon() && !this.hintCooldown());

  getSize() { return this.size; }
  getZones() { return this.zones; }
  getSolution() { return this.solution; }

  initPuzzle(puzzle: StarsPuzzle): void {
    this.size = puzzle.size;
    this.zones = puzzle.zones;
    this.solution = puzzle.solution;
    this.gameWon.set(false);
    this.timerDisabled.set(false);
    this.isRestored.set(false);
    this.history = [];
    this.historyLength.set(0);
    this.clearHint();
    this.conflictCells.set([]);

    const b: number[][] = [];
    for (let r = 0; r < this.size; r++) b.push(new Array(this.size).fill(EMPTY));
    this.board.set(b);
    this.startTimer();
  }

  toggleCell(row: number, col: number): void {
    if (this.gameWon()) return;
    if (row < 0 || row >= this.size || col < 0 || col >= this.size) return;

    this.clearHint();
    const b = this.board().map(r => [...r]);
    const current = b[row][col];

    this.history.push(this.board().map(r => [...r]));
    this.historyLength.set(this.history.length);

    if (current === EMPTY) {
      b[row][col] = MARK_X;
    } else if (current === MARK_X || current === AUTO_X) {
      b[row][col] = STAR;
    } else {
      b[row][col] = EMPTY;
    }

    this.board.set(b);
    this.updateConflicts();

    if (b[row][col] === STAR) this.checkWin();
  }

  /**
   * When a star is placed at (row, col):
   * - Always X all 8 neighbors (no adjacency allowed, including diagonals)
   * - If this row now has 2 stars → X all remaining empty cells in row
   * - If this col now has 2 stars → X all remaining empty cells in col
   * - If this zone now has 2 stars → X all remaining empty cells in zone
   */
  private autoFillXAroundStar(b: number[][], qRow: number, qCol: number): void {
    const n = this.size;

    // All 8 neighbors always get X (no two stars can touch)
    for (const [dr, dc] of [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]) {
      const nr = qRow + dr, nc = qCol + dc;
      if (nr >= 0 && nr < n && nc >= 0 && nc < n && b[nr][nc] === EMPTY) {
        b[nr][nc] = AUTO_X;
      }
    }

    // Count stars in this row
    const rowStars = this.countStarsInRow(b, qRow);
    if (rowStars >= 2) {
      for (let c = 0; c < n; c++) {
        if (b[qRow][c] === EMPTY) b[qRow][c] = AUTO_X;
      }
    }

    // Count stars in this col
    const colStars = this.countStarsInCol(b, qCol);
    if (colStars >= 2) {
      for (let r = 0; r < n; r++) {
        if (b[r][qCol] === EMPTY) b[r][qCol] = AUTO_X;
      }
    }

    // Count stars in this zone
    const zone = this.zones[qRow][qCol];
    const zoneStars = this.countStarsInZone(b, zone);
    if (zoneStars >= 2) {
      for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
          if (this.zones[r][c] === zone && b[r][c] === EMPTY) {
            b[r][c] = AUTO_X;
          }
        }
      }
    }
  }

  private recalcAutoX(b: number[][]): void {
    const n = this.size;
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (b[r][c] === AUTO_X) b[r][c] = EMPTY;

    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (b[r][c] === STAR) this.autoFillXAroundStar(b, r, c);
  }

  private countStarsInRow(b: number[][], row: number): number {
    let count = 0;
    for (let c = 0; c < this.size; c++) if (b[row][c] === STAR) count++;
    return count;
  }

  private countStarsInCol(b: number[][], col: number): number {
    let count = 0;
    for (let r = 0; r < this.size; r++) if (b[r][col] === STAR) count++;
    return count;
  }

  private countStarsInZone(b: number[][], zone: number): number {
    let count = 0;
    for (let r = 0; r < this.size; r++)
      for (let c = 0; c < this.size; c++)
        if (this.zones[r][c] === zone && b[r][c] === STAR) count++;
    return count;
  }

  undo(): void {
    if (this.history.length === 0 || this.gameWon()) return;
    const prev = this.history.pop()!;
    this.historyLength.set(this.history.length);
    this.board.set(prev);
    this.updateConflicts();
  }

  hint(): void {
    if (!this.canHint()) return;
    this.clearHint();

    const n = this.size;
    const b = this.board();

    const corrections = this.correctMistakes(n, b);
    if (corrections) {
      this.history.push(b.map(r => [...r]));
      this.historyLength.set(this.history.length);
      this.board.set(corrections.board);
      this.updateConflicts();
      this.hintCells.set(corrections.cells);
      this.hintMessage.set(corrections.message);
      this.scheduleHintClear();
      this.startHintCooldown();
      return;
    }

    const solvedZones = new Set<number>();
    const solvedRows = new Set<number>();
    const solvedCols = new Set<number>();
    for (let r = 0; r < n; r++) {
      let rowStars = 0;
      for (let c = 0; c < n; c++) {
        if (b[r][c] === STAR) {
          rowStars++;
          solvedZones.add(this.zones[r][c]);
          solvedCols.add(c);
        }
      }
      if (rowStars >= 2) solvedRows.add(r);
    }

    const isAvailable = (r: number, c: number): boolean =>
      b[r][c] === EMPTY
      && !solvedRows.has(r)
      && !solvedCols.has(c)
      && this.countStarsInZone(b, this.zones[r][c]) < 2;

    let result = this.ruleZoneConfinedToRows(n, b, solvedZones, isAvailable);
    if (!result) result = this.ruleZoneConfinedToCols(n, b, solvedZones, isAvailable);
    if (!result) result = this.ruleRowHasOneZone(n, b, solvedZones, solvedRows, isAvailable);
    if (!result) result = this.ruleColHasOneZone(n, b, solvedZones, solvedCols, isAvailable);
    if (!result) result = this.ruleZoneTwoCells(n, b, solvedZones, isAvailable);

    if (!result || result.cells.length === 0) {
      this.hintMessage.set('Nuk gjeta ndihmë — provo të analizosh zonat me pak hapësirë.');
      this.hintTimeout = setTimeout(() => this.hintMessage.set(''), 4000);
      this.startHintCooldown();
      return;
    }

    this.history.push(this.board().map(r => [...r]));
    this.historyLength.set(this.history.length);
    const newBoard = b.map(r => [...r]);
    for (const cell of result.cells) {
      if (newBoard[cell.row][cell.col] === EMPTY) newBoard[cell.row][cell.col] = AUTO_X;
    }
    this.board.set(newBoard);
    this.hintCells.set(result.cells);
    this.hintMessage.set(result.message);
    this.scheduleHintClear();
    this.startHintCooldown();
  }

  private scheduleHintClear(): void {
    this.hintTimeout = setTimeout(() => {
      this.hintCells.set([]);
      this.hintMessage.set('');
      this.hintTimeout = null;
    }, 5000);
  }

  private correctMistakes(n: number, b: number[][]): {
    board: number[][];
    cells: { row: number; col: number }[];
    message: string;
  } | null {
    const newBoard = b.map(r => [...r]);
    for (let r = 0; r < n; r++) {
      const solCols = new Set(this.solution[r]);
      for (let c = 0; c < n; c++) {
        if (newBoard[r][c] === STAR && !solCols.has(c)) {
          newBoard[r][c] = EMPTY;
          this.recalcAutoX(newBoard);
          return { board: newBoard, cells: [{ row: r, col: c }], message: '1 yll i gabuar u hoq — tani provo përsëri!' };
        }
      }
      for (const sc of solCols) {
        if (newBoard[r][sc] === MARK_X || newBoard[r][sc] === AUTO_X) {
          newBoard[r][sc] = EMPTY;
          this.recalcAutoX(newBoard);
          return { board: newBoard, cells: [{ row: r, col: sc }], message: '1 X e gabuar u fshi — tani provo përsëri!' };
        }
      }
    }
    return null;
  }

  private zoneName(z: number): string {
    return this.zoneNames[z % this.zoneNames.length];
  }

  /** Rule: Zone's available cells all in ≤2 rows → X other zones' cells in those rows. */
  private ruleZoneConfinedToRows(
    n: number, b: number[][], solvedZones: Set<number>,
    isAvailable: (r: number, c: number) => boolean
  ): { cells: { row: number; col: number }[]; message: string } | null {
    for (let z = 0; z < n; z++) {
      if (this.countStarsInZone(b, z) >= 2) continue;
      const needed = 2 - this.countStarsInZone(b, z);
      const rows = new Set<number>();
      for (let r = 0; r < n; r++)
        for (let c = 0; c < n; c++)
          if (this.zones[r][c] === z && isAvailable(r, c)) rows.add(r);
      if (rows.size <= needed) {
        const cells: { row: number; col: number }[] = [];
        for (const row of rows) {
          for (let c = 0; c < n; c++) {
            if (this.zones[row][c] !== z && b[row][c] === EMPTY) cells.push({ row, col: c });
          }
        }
        if (cells.length > 0) return {
          cells,
          message: `Zona ${this.zoneName(z)} ka vend vetëm në ${needed === 2 ? 'ato rreshta' : 'atë rresht'} — X qelizat e tjera.`
        };
      }
    }
    return null;
  }

  /** Rule: Zone's available cells all in ≤2 cols → X other zones' cells in those cols. */
  private ruleZoneConfinedToCols(
    n: number, b: number[][], solvedZones: Set<number>,
    isAvailable: (r: number, c: number) => boolean
  ): { cells: { row: number; col: number }[]; message: string } | null {
    for (let z = 0; z < n; z++) {
      if (this.countStarsInZone(b, z) >= 2) continue;
      const needed = 2 - this.countStarsInZone(b, z);
      const cols = new Set<number>();
      for (let r = 0; r < n; r++)
        for (let c = 0; c < n; c++)
          if (this.zones[r][c] === z && isAvailable(r, c)) cols.add(c);
      if (cols.size <= needed) {
        const cells: { row: number; col: number }[] = [];
        for (const col of cols) {
          for (let r = 0; r < n; r++) {
            if (this.zones[r][col] !== z && b[r][col] === EMPTY) cells.push({ row: r, col });
          }
        }
        if (cells.length > 0) return {
          cells,
          message: `Zona ${this.zoneName(z)} ka vend vetëm në ato kolona — X qelizat e tjera.`
        };
      }
    }
    return null;
  }

  /** Rule: Row has only N unsolved zones → X those zones' cells in other rows. */
  private ruleRowHasOneZone(
    n: number, b: number[][], solvedZones: Set<number>, solvedRows: Set<number>,
    isAvailable: (r: number, c: number) => boolean
  ): { cells: { row: number; col: number }[]; message: string } | null {
    for (let r = 0; r < n; r++) {
      if (solvedRows.has(r)) continue;
      const zonesInRow = new Set<number>();
      for (let c = 0; c < n; c++) if (isAvailable(r, c)) zonesInRow.add(this.zones[r][c]);
      if (zonesInRow.size === 1) {
        const zone = zonesInRow.values().next().value!;
        const cells: { row: number; col: number }[] = [];
        for (let r2 = 0; r2 < n; r2++) {
          if (r2 === r) continue;
          for (let c = 0; c < n; c++) {
            if (this.zones[r2][c] === zone && b[r2][c] === EMPTY) cells.push({ row: r2, col: c });
          }
        }
        if (cells.length > 0) return {
          cells,
          message: `Rreshti ${r + 1} ka vetëm zonën ${this.zoneName(zone)} — X pjesën tjetër.`
        };
      }
    }
    return null;
  }

  /** Rule: Col has only N unsolved zones → X those zones' cells in other cols. */
  private ruleColHasOneZone(
    n: number, b: number[][], solvedZones: Set<number>, solvedCols: Set<number>,
    isAvailable: (r: number, c: number) => boolean
  ): { cells: { row: number; col: number }[]; message: string } | null {
    for (let c = 0; c < n; c++) {
      if (solvedCols.has(c)) continue;
      const zonesInCol = new Set<number>();
      for (let r = 0; r < n; r++) if (isAvailable(r, c)) zonesInCol.add(this.zones[r][c]);
      if (zonesInCol.size === 1) {
        const zone = zonesInCol.values().next().value!;
        const cells: { row: number; col: number }[] = [];
        for (let c2 = 0; c2 < n; c2++) {
          if (c2 === c) continue;
          for (let r = 0; r < n; r++) {
            if (this.zones[r][c2] === zone && b[r][c2] === EMPTY) cells.push({ row: r, col: c2 });
          }
        }
        if (cells.length > 0) return {
          cells,
          message: `Kolona ${c + 1} ka vetëm zonën ${this.zoneName(zone)} — X pjesën tjetër.`
        };
      }
    }
    return null;
  }

  /** Rule: Zone has only 2 available cells → mark conflicting cells. */
  private ruleZoneTwoCells(
    n: number, b: number[][], solvedZones: Set<number>,
    isAvailable: (r: number, c: number) => boolean
  ): { cells: { row: number; col: number }[]; message: string } | null {
    for (let z = 0; z < n; z++) {
      if (this.countStarsInZone(b, z) >= 2) continue;
      const needed = 2 - this.countStarsInZone(b, z);
      const available: { row: number; col: number }[] = [];
      for (let r = 0; r < n; r++)
        for (let c = 0; c < n; c++)
          if (this.zones[r][c] === z && isAvailable(r, c)) available.push({ row: r, col: c });

      if (available.length === needed && needed > 0) {
        const cells: { row: number; col: number }[] = [];
        for (const { row: qr, col: qc } of available) {
          for (const [dr, dc] of [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]) {
            const nr = qr + dr, nc = qc + dc;
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && b[nr][nc] === EMPTY
              && !available.some(a => a.row === nr && a.col === nc)) {
              cells.push({ row: nr, col: nc });
            }
          }
        }
        if (cells.length > 0) return {
          cells,
          message: `Zona ${this.zoneName(z)} ka vetëm ${needed === 1 ? '1 qelizë' : '2 qeliza'} — X rreth tyre.`
        };
      }
    }
    return null;
  }

  private detectConflicts(b: number[][]): { row: number; col: number }[] {
    const n = this.size;
    const stars: { row: number; col: number }[] = [];
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (b[r][c] === STAR) stars.push({ row: r, col: c });

    if (stars.length < 2) return [];

    const conflictSet = new Set<string>();
    for (let i = 0; i < stars.length; i++) {
      for (let j = i + 1; j < stars.length; j++) {
        const a = stars[i], bq = stars[j];
        // Adjacency: any two stars touching (including diagonals) is a conflict
        const touching = Math.abs(a.row - bq.row) <= 1 && Math.abs(a.col - bq.col) <= 1;
        if (touching) {
          conflictSet.add(`${a.row},${a.col}`);
          conflictSet.add(`${bq.row},${bq.col}`);
        }
      }
    }

    // Also flag rows/cols/zones with >2 stars
    const rowCounts = new Map<number, number>();
    const colCounts = new Map<number, number>();
    const zoneCounts = new Map<number, number>();
    for (const { row, col } of stars) {
      rowCounts.set(row, (rowCounts.get(row) ?? 0) + 1);
      colCounts.set(col, (colCounts.get(col) ?? 0) + 1);
      const z = this.zones[row][col];
      zoneCounts.set(z, (zoneCounts.get(z) ?? 0) + 1);
    }
    for (const { row, col } of stars) {
      if ((rowCounts.get(row) ?? 0) > 2 || (colCounts.get(col) ?? 0) > 2
        || (zoneCounts.get(this.zones[row][col]) ?? 0) > 2) {
        conflictSet.add(`${row},${col}`);
      }
    }

    return Array.from(conflictSet).map(key => {
      const [r, c] = key.split(',').map(Number);
      return { row: r, col: c };
    });
  }

  private updateConflicts(): void {
    this.conflictCells.set(this.detectConflicts(this.board()));
  }

  private checkWin(): void {
    const b = this.board();
    const n = this.size;

    const stars: [number, number][] = [];
    for (let r = 0; r < n; r++)
      for (let c = 0; c < n; c++)
        if (b[r][c] === STAR) stars.push([r, c]);

    if (stars.length !== 2 * n) return;

    // 2 per row
    const rowCounts = new Array(n).fill(0);
    const colCounts = new Array(n).fill(0);
    const zoneCounts = new Array(n).fill(0);
    for (const [r, c] of stars) {
      rowCounts[r]++;
      colCounts[c]++;
      zoneCounts[this.zones[r][c]]++;
    }
    for (let i = 0; i < n; i++) {
      if (rowCounts[i] !== 2 || colCounts[i] !== 2 || zoneCounts[i] !== 2) return;
    }

    // No two stars touching (including diagonal)
    for (let i = 0; i < stars.length; i++) {
      for (let j = i + 1; j < stars.length; j++) {
        const [r1, c1] = stars[i], [r2, c2] = stars[j];
        if (Math.abs(r1 - r2) <= 1 && Math.abs(c1 - c2) <= 1) return;
      }
    }

    this.gameWon.set(true);
    this.stopTimer();
  }

  checkCorrect(): boolean {
    const n = this.size;
    const b = this.board();
    for (let r = 0; r < n; r++) {
      const solCols = new Set(this.solution[r]);
      for (let c = 0; c < n; c++) {
        if (b[r][c] === STAR && !solCols.has(c)) return false;
      }
      for (const sc of solCols) {
        if (b[r][sc] === MARK_X) return false;
      }
    }
    return true;
  }

  reset(): void {
    const b: number[][] = [];
    for (let r = 0; r < this.size; r++) b.push(new Array(this.size).fill(EMPTY));
    this.board.set(b);
    this.gameWon.set(false);
    this.timerDisabled.set(false);
    this.isRestored.set(false);
    this.history = [];
    this.historyLength.set(0);
    this.clearHint();
    this.conflictCells.set([]);
    this.startTimer();
  }

  resetPractice(): void {
    const b: number[][] = [];
    for (let r = 0; r < this.size; r++) b.push(new Array(this.size).fill(EMPTY));
    this.board.set(b);
    this.gameWon.set(false);
    this.timerDisabled.set(true);
    this.isRestored.set(false);
    this.history = [];
    this.historyLength.set(0);
    this.clearHint();
    this.conflictCells.set([]);
    this.stopTimer();
    this.timerSeconds.set(0);
  }

  restoreCompleted(savedBoard: number[][]): void {
    this.isRestored.set(true);
    this.board.set(savedBoard);
    this.gameWon.set(true);
    this.timerDisabled.set(true);
    this.history = [];
    this.historyLength.set(0);
    this.stopTimer();
  }

  restorePaused(savedBoard: number[][], savedTimer: number): void {
    this.board.set(savedBoard);
    this.timerSeconds.set(savedTimer);
    this.gameWon.set(false);
    this.timerDisabled.set(false);
    this.isRestored.set(false);
    this.history = [];
    this.historyLength.set(0);
    this.stopTimer();
  }

  getProgressSnapshot(): { board: number[][]; timerSeconds: number } | null {
    if (this.gameWon() || this.isRestored() || this.timerDisabled()) return null;
    const b = this.board();
    let hasMove = false;
    for (const row of b) { for (const cell of row) { if (cell !== EMPTY) { hasMove = true; break; } } if (hasMove) break; }
    if (!hasMove) return null;
    return { board: b.map(r => [...r]), timerSeconds: this.timerSeconds() };
  }

  pauseTimer(): void { this.stopTimer(); }
  resumeTimer(): void {
    if (this.gameWon() || this.timerDisabled()) return;
    this.stopTimer();
    this.timerInterval = setInterval(() => this.timerSeconds.update(v => v + 1), 1000);
  }

  private startTimer(): void {
    this.stopTimer();
    this.timerSeconds.set(0);
    this.timerInterval = setInterval(() => this.timerSeconds.update(v => v + 1), 1000);
  }

  private stopTimer(): void {
    if (this.timerInterval) { clearInterval(this.timerInterval); this.timerInterval = null; }
  }

  formatTime(seconds: number): string {
    const m = String(Math.floor(seconds / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    return `${m}:${s}`;
  }

  private startHintCooldown(): void {
    this.hintCooldown.set(true);
    this.hintCooldownRemaining.set(5);
    this.hintCooldownInterval = setInterval(() => {
      const r = this.hintCooldownRemaining() - 1;
      this.hintCooldownRemaining.set(r);
      if (r <= 0) {
        this.hintCooldown.set(false);
        this.hintCooldownRemaining.set(0);
        if (this.hintCooldownInterval) { clearInterval(this.hintCooldownInterval); this.hintCooldownInterval = null; }
      }
    }, 1000);
  }

  private clearHint(): void {
    if (this.hintTimeout) { clearTimeout(this.hintTimeout); this.hintTimeout = null; }
    this.hintCells.set([]);
    this.hintMessage.set('');
    this.hintCooldown.set(false);
    this.hintCooldownRemaining.set(0);
    if (this.hintCooldownInterval) { clearInterval(this.hintCooldownInterval); this.hintCooldownInterval = null; }
  }

  destroy(): void {
    this.stopTimer();
    this.clearHint();
  }
}
