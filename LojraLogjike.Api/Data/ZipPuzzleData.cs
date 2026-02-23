using LojraLogjike.Api.Models;

namespace LojraLogjike.Api.Data;

public static class ZipPuzzleData
{
    private static readonly string[] DayNames =
        ["E Hënë", "E Martë", "E Mërkurë", "E Enjte", "E Premte", "E Shtunë", "E Diel"];

    // All puzzles are verified Hamiltonian paths with interior checkpoints.
    // Path goes checkpoint 1 → 2 → 3 → ... → last, visiting every cell exactly once.
    // The path MUST end on the last numbered checkpoint.
    private static readonly List<ZipPuzzle> Puzzles =
    [
        // ═══════════════════════════════════════════
        // Day 0 — Monday 5×5 (easy, no walls, 5 checkpoints, 3 interior)
        // Path: 12,7,8,13,18,23,24,19,14,9,4,3,2,1,0,5,6,11,10,15,20,21,16,17,22
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 5, Cols = 5,
            Numbers = new() {
                [12] = 1,   // (2,2) start — interior
                [18] = 2,   // (3,3) interior
                [4] = 3,    // (0,4) edge
                [6] = 4,    // (1,1) interior
                [22] = 5    // (4,2) end — edge
            },
            Walls = [],
            SolutionPath = [12,7,8,13,18,23,24,19,14,9,4,3,2,1,0,5,6,11,10,15,20,21,16,17,22]
        },
        // ═══════════════════════════════════════════
        // Day 1 — Tuesday 6×6 (easy-medium, 2 walls, 8 checkpoints, 6 interior)
        // Path: 7,1,0,6,12,18,19,13,14,8,2,3,4,5,11,10,9,15,21,20,26,25,24,30,31,32,33,27,28,34,35,29,23,17,16,22
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 6, Cols = 6,
            Numbers = new() {
                [7] = 1,    // (1,1) start — interior
                [19] = 2,   // (3,1) interior
                [8] = 3,    // (1,2) interior
                [9] = 4,    // (1,3) interior
                [20] = 5,   // (3,2) interior
                [33] = 6,   // (5,3) edge
                [17] = 7,   // (2,5) edge
                [22] = 8    // (3,4) end — interior
            },
            Walls = [[0,3,1,3],[3,4,4,4]],
            SolutionPath = [7,1,0,6,12,18,19,13,14,8,2,3,4,5,11,10,9,15,21,20,26,25,24,30,31,32,33,27,28,34,35,29,23,17,16,22]
        },
        // ═══════════════════════════════════════════
        // Day 2 — Wednesday 6×6 (medium, 3 walls, 9 checkpoints, 5 interior)
        // Path: 14,13,7,8,9,3,2,1,0,6,12,18,19,20,26,25,24,30,31,32,33,27,21,15,16,10,4,5,11,17,23,22,28,34,35,29
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 6, Cols = 6,
            Numbers = new() {
                [14] = 1,   // (2,2) start — interior
                [7] = 2,    // (1,1) interior
                [9] = 3,    // (1,3) interior
                [12] = 4,   // (2,0) edge
                [20] = 5,   // (3,2) interior
                [25] = 6,   // (4,1) interior
                [27] = 7,   // (4,3) interior
                [10] = 8,   // (1,4) edge
                [29] = 9    // (4,5) end — edge
            },
            Walls = [[0,2,1,2],[2,4,3,4],[4,1,5,1]],
            SolutionPath = [14,13,7,8,9,3,2,1,0,6,12,18,19,20,26,25,24,30,31,32,33,27,21,15,16,10,4,5,11,17,23,22,28,34,35,29]
        },
        // ═══════════════════════════════════════════
        // Day 3 — Thursday 7×7 (medium, 4 walls, 9 checkpoints, 4 interior)
        // Path: 24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 7, Cols = 7,
            Numbers = new() {
                [24] = 1,   // (3,3) start — interior
                [16] = 2,   // (2,2) interior
                [27] = 3,   // (3,6) edge
                [19] = 4,   // (2,5) interior
                [6] = 5,    // (0,6) corner
                [0] = 6,    // (0,0) corner
                [42] = 7,   // (6,0) corner
                [23] = 8,   // (3,2) interior
                [46] = 9    // (6,4) end — edge
            },
            Walls = [[0,3,1,3],[3,5,4,5],[5,1,5,2],[6,3,6,4]],
            SolutionPath = [24,17,16,9,10,11,18,25,26,27,20,19,12,13,6,5,4,3,2,1,0,7,8,15,14,21,28,35,42,43,36,29,22,23,30,37,44,45,38,31,32,39,40,33,34,41,48,47,46]
        },
        // ═══════════════════════════════════════════
        // Day 4 — Friday 7×7 (medium-hard, 2 walls, 10 checkpoints, 7 interior)
        // Path: 0,7,14,21,28,35,42,43,36,29,22,15,8,1,2,9,16,23,30,37,44,45,38,39,46,47,40,33,32,31,24,25,18,17,10,3,4,11,12,5,6,13,20,19,26,27,34,41,48
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 7, Cols = 7,
            Numbers = new() {
                [0] = 1,    // (0,0) start — corner
                [9] = 2,    // (1,2) interior
                [16] = 3,   // (2,2) interior
                [23] = 4,   // (3,2) interior
                [30] = 5,   // (4,2) interior
                [38] = 6,   // (5,3) interior
                [46] = 7,   // (6,4) edge
                [32] = 8,   // (4,4) interior
                [19] = 9,   // (2,5) interior
                [48] = 10   // (6,6) end — corner
            },
            Walls = [[2,3,3,3],[4,1,4,2]],
            SolutionPath = [0,7,14,21,28,35,42,43,36,29,22,15,8,1,2,9,16,23,30,37,44,45,38,39,46,47,40,33,32,31,24,25,18,17,10,3,4,11,12,5,6,13,20,19,26,27,34,41,48]
        },
        // ═══════════════════════════════════════════
        // Day 5 — Saturday 8×8 (hard, no walls, 10 checkpoints, 8 interior)
        // Path: 0,8,16,24,32,40,48,56,57,49,41,33,25,17,9,1,2,10,18,26,34,42,50,58,59,51,43,35,27,19,11,3,4,12,20,28,36,44,52,60,61,53,45,37,29,21,13,5,6,7,15,14,22,23,31,30,38,39,47,46,54,55,63,62
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 8, Cols = 8,
            Numbers = new() {
                [0] = 1,    // (0,0) start — corner
                [41] = 2,   // (5,1) interior
                [9] = 3,    // (1,1) interior
                [18] = 4,   // (2,2) interior
                [27] = 5,   // (3,3) interior
                [36] = 6,   // (4,4) interior
                [45] = 7,   // (5,5) interior
                [37] = 8,   // (4,5) interior
                [54] = 9,   // (6,6) interior
                [62] = 10   // (7,6) end — edge
            },
            Walls = [],
            SolutionPath = [0,8,16,24,32,40,48,56,57,49,41,33,25,17,9,1,2,10,18,26,34,42,50,58,59,51,43,35,27,19,11,3,4,12,20,28,36,44,52,60,61,53,45,37,29,21,13,5,6,7,15,14,22,23,31,30,38,39,47,46,54,55,63,62]
        },
        // ═══════════════════════════════════════════
        // Day 6 — Sunday 9×9 (hardest, 2 walls, 10 checkpoints, 8 interior)
        // Path: 0,9,18,27,36,45,54,63,72,73,64,55,46,37,28,19,10,1,2,11,20,29,38,39,30,21,12,3,4,13,22,23,14,5,6,15,24,33,42,41,32,31,40,49,58,59,50,51,60,61,52,43,34,25,16,7,8,17,26,35,44,53,62,71,70,69,68,67,66,57,48,47,56,65,74,75,76,77,78,79,80
        // ═══════════════════════════════════════════
        new()
        {
            Rows = 9, Cols = 9,
            Numbers = new() {
                [0] = 1,    // (0,0) start — corner
                [10] = 2,   // (1,1) interior
                [20] = 3,   // (2,2) interior
                [30] = 4,   // (3,3) interior
                [40] = 5,   // (4,4) interior
                [50] = 6,   // (5,5) interior
                [60] = 7,   // (6,6) interior
                [70] = 8,   // (7,7) interior
                [48] = 9,   // (5,3) interior
                [80] = 10   // (8,8) end — corner
            },
            Walls = [[2,4,3,4],[5,3,5,4]],
            SolutionPath = [0,9,18,27,36,45,54,63,72,73,64,55,46,37,28,19,10,1,2,11,20,29,38,39,30,21,12,3,4,13,22,23,14,5,6,15,24,33,42,41,32,31,40,49,58,59,50,51,60,61,52,43,34,25,16,7,8,17,26,35,44,53,62,71,70,69,68,67,66,57,48,47,56,65,74,75,76,77,78,79,80]
        }
    ];

    public static ZipPuzzle GetTodayPuzzle()
    {
        var dayOfWeek = (int)DateTime.Now.DayOfWeek;
        // Map: Sun=0→6, Mon=1→0, Tue=2→1, ...
        var index = dayOfWeek == 0 ? 6 : dayOfWeek - 1;
        var puzzle = Puzzles[index];
        puzzle.DayIndex = index;
        puzzle.DayName = DayNames[index];
        return puzzle;
    }

    public static ZipPuzzle GetPuzzleByDay(int dayIndex)
    {
        if (dayIndex < 0 || dayIndex >= Puzzles.Count)
            dayIndex = 0;
        var puzzle = Puzzles[dayIndex];
        puzzle.DayIndex = dayIndex;
        puzzle.DayName = DayNames[dayIndex];
        return puzzle;
    }
}
