export interface TangoConstraint {
  r1: number;
  c1: number;
  r2: number;
  c2: number;
  type: 'same' | 'diff';
}

export interface TangoPuzzle {
  solution: number[][];
  prefilled: number[][];
  constraints: TangoConstraint[];
  dayIndex: number;
  dayName: string;
}
