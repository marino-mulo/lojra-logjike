export interface ZipPuzzle {
  rows: number;
  cols: number;
  numbers: Record<string, number>;
  walls: number[][];
  solutionPath: number[];
  dayIndex: number;
  dayName: string;
}
