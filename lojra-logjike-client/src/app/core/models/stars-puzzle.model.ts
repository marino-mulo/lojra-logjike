export interface StarsPuzzle {
  size: number;
  zones: number[][];
  solution: number[][]; // solution[row] = [col1, col2] sorted ascending
  dayIndex: number;
  dayName: string;
}
