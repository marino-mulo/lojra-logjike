using LojraLogjike.Api.Models;

namespace LojraLogjike.Api.Data;

public static class QueensPuzzleData
{
    private static readonly string[] DayNames =
        ["E Hënë", "E Martë", "E Mërkurë", "E Enjte", "E Premte", "E Shtunë", "E Diel"];

    private static readonly List<QueensPuzzle> Puzzles =
    [
        // Day 0 — Monday 7×7 (easy)
        new()
        {
            Size = 7,
            Zones = [
                [2,2,2,2,0,0,0],
                [3,3,3,2,1,1,1],
                [3,3,3,2,1,5,5],
                [3,3,4,4,4,5,5],
                [6,3,4,4,4,5,5],
                [6,6,6,6,4,5,5],
                [6,6,6,6,4,4,4]
            ],
            Solution = [4, 6, 3, 0, 2, 5, 1]
        },
        // Day 1 — Tuesday 8×8 (easy-medium)
        new()
        {
            Size = 8,
            Zones = [
                [0,0,0,1,1,1,1,1],
                [3,2,2,1,2,2,4,1],
                [3,2,2,2,2,2,4,4],
                [3,3,3,3,3,7,4,4],
                [6,6,6,7,7,7,4,4],
                [6,6,6,7,7,5,5,5],
                [6,6,6,7,7,7,7,7],
                [6,6,6,7,7,7,7,7]
            ],
            Solution = [0, 3, 1, 4, 7, 5, 2, 6]
        },
        // Day 2 — Wednesday 9×9 (medium)
        new()
        {
            Size = 9,
            Zones = [
                [0,0,0,0,1,1,1,1,1],
                [0,0,0,1,1,1,1,1,1],
                [0,0,2,2,2,2,1,1,1],
                [0,0,0,2,2,2,1,1,3],
                [4,0,0,2,2,2,3,3,3],
                [4,0,0,2,2,5,3,3,3],
                [4,4,4,2,2,5,5,6,6],
                [4,4,4,7,7,5,5,6,6],
                [7,7,7,7,7,8,8,6,6]
            ],
            Solution = [1, 4, 2, 8, 0, 5, 7, 3, 6]
        },
        // Day 3 — Thursday 9×9 (medium-hard)
        new()
        {
            Size = 9,
            Zones = [
                [3,3,5,5,0,0,1,1,1],
                [3,3,5,4,4,0,0,2,1],
                [3,3,5,4,4,4,2,2,2],
                [3,5,5,4,4,4,4,4,4],
                [5,5,6,6,6,7,7,4,4],
                [5,5,6,6,6,7,7,7,7],
                [8,8,6,6,6,7,7,7,7],
                [8,8,8,8,7,7,7,7,7],
                [8,8,8,8,8,8,8,8,8]
            ],
            Solution = [4, 8, 6, 0, 7, 1, 3, 5, 2]
        },
        // Day 4 — Friday 10×10 (hard)
        new()
        {
            Size = 10,
            Zones = [
                [2,2,8,8,8,0,0,0,0,0],
                [2,2,8,1,8,0,0,1,0,0],
                [2,8,8,1,8,8,1,1,0,0],
                [8,8,3,1,1,1,1,4,4,4],
                [8,8,3,3,3,3,4,4,4,4],
                [8,8,8,3,3,3,4,4,5,5],
                [8,8,8,3,3,3,3,6,5,5],
                [8,8,8,8,7,7,7,6,6,5],
                [8,8,8,8,8,7,7,9,6,5],
                [8,8,8,8,8,7,7,9,9,5]
            ],
            Solution = [5, 3, 0, 2, 6, 9, 7, 4, 1, 8]
        },
        // Day 5 — Saturday 10×10 (hard)
        new()
        {
            Size = 10,
            Zones = [
                [1,1,1,3,3,2,2,2,0,0],
                [1,1,1,3,3,2,6,2,2,2],
                [8,8,3,3,5,5,6,4,4,2],
                [8,3,3,5,5,5,6,4,4,4],
                [8,8,5,5,5,6,6,4,4,4],
                [8,8,5,6,6,6,7,7,7,7],
                [8,8,8,8,6,9,7,7,7,7],
                [8,8,8,8,9,9,7,7,7,7],
                [8,8,8,8,9,9,9,9,9,9],
                [8,8,8,9,9,9,9,9,9,9]
            ],
            Solution = [8, 0, 9, 1, 7, 2, 4, 6, 3, 5]
        },
        // Day 6 — Sunday 11×11 (hardest)
        new()
        {
            Size = 11,
            Zones = [
                [10,10,10,10,10,10,10,10,0,0,1],
                [10,10,10,10,10,10,2,2,2,0,1],
                [10,10,10,10,2,2,2,2,2,0,0],
                [10,10,10,4,4,4,3,3,3,0,0],
                [10,10,10,4,6,4,4,3,3,5,5],
                [10,10,10,6,6,4,4,3,3,5,5],
                [10,6,6,6,7,7,7,7,5,5,5],
                [10,10,9,9,9,7,7,7,8,8,8],
                [10,10,9,9,9,9,8,8,8,8,8],
                [10,9,9,9,9,9,9,9,9,8,8],
                [10,10,10,10,9,9,9,9,9,8,8]
            ],
            Solution = [8, 10, 4, 6, 3, 9, 1, 5, 7, 2, 0]
        }
    ];

    public static QueensPuzzle GetTodayPuzzle()
    {
        var dayOfWeek = (int)DateTime.Now.DayOfWeek;
        var index = dayOfWeek == 0 ? 6 : dayOfWeek - 1;
        return GetPuzzleByDay(index);
    }

    public static QueensPuzzle GetPuzzleByDay(int dayIndex)
    {
        if (dayIndex < 0 || dayIndex >= Puzzles.Count)
            dayIndex = 0;

        var puzzle = Puzzles[dayIndex];
        return new QueensPuzzle
        {
            Size = puzzle.Size,
            Zones = puzzle.Zones,
            Solution = puzzle.Solution,
            DayIndex = dayIndex,
            DayName = DayNames[dayIndex]
        };
    }
}
