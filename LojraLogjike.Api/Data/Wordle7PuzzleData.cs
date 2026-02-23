using LojraLogjike.Api.Models;

namespace LojraLogjike.Api.Data;

public static class Wordle7PuzzleData
{
    private static readonly string[] DayNames =
        ["E Hënë", "E Martë", "E Mërkurë", "E Enjte", "E Premte", "E Shtunë", "E Diel"];

    private static readonly List<Wordle7Puzzle> Puzzles =
    [
        // Day 0 (7x7): TRE, VEL, VET, DET, DRITË, SHI, NJË, DIM, NUK, KUQ, LOT, ORA, MOS, PAK
        new()
        {
            GridSize = 7,
            Solution = [
                ["M", "X", "D", "I", "M", "X", "D"],
                ["O", "X", "R", "X", "X", "X", "E"],
                ["S", "H", "I", "X", "V", "E", "T"],
                ["X", "X", "T", "R", "E", "X", "X"],
                ["N", "J", "Ë", "X", "L", "O", "T"],
                ["U", "X", "X", "X", "X", "R", "X"],
                ["K", "U", "Q", "X", "P", "A", "K"],
            ],
            Words = [
                new() { Word = "TRE", Row = 3, Col = 2, Direction = "horizontal" },
                new() { Word = "VEL", Row = 2, Col = 4, Direction = "vertical" },
                new() { Word = "VET", Row = 2, Col = 4, Direction = "horizontal" },
                new() { Word = "DET", Row = 0, Col = 6, Direction = "vertical" },
                new() { Word = "DRITË", Row = 0, Col = 2, Direction = "vertical" },
                new() { Word = "SHI", Row = 2, Col = 0, Direction = "horizontal" },
                new() { Word = "NJË", Row = 4, Col = 0, Direction = "horizontal" },
                new() { Word = "DIM", Row = 0, Col = 2, Direction = "horizontal" },
                new() { Word = "NUK", Row = 4, Col = 0, Direction = "vertical" },
                new() { Word = "KUQ", Row = 6, Col = 0, Direction = "horizontal" },
                new() { Word = "LOT", Row = 4, Col = 4, Direction = "horizontal" },
                new() { Word = "ORA", Row = 4, Col = 5, Direction = "vertical" },
                new() { Word = "MOS", Row = 0, Col = 0, Direction = "vertical" },
                new() { Word = "PAK", Row = 6, Col = 4, Direction = "horizontal" },
            ]
        },
        // Day 1 (7x7): VËRË, DIMË, JETË, VEL, MAL, VAJ, PLAKË, VIT, FLETË
        new()
        {
            GridSize = 7,
            Solution = [
                ["V", "A", "J", "X", "D", "X", "X"],
                ["I", "X", "E", "X", "I", "X", "F"],
                ["T", "X", "T", "X", "M", "A", "L"],
                ["X", "V", "Ë", "R", "Ë", "X", "E"],
                ["X", "E", "X", "X", "X", "X", "T"],
                ["P", "L", "A", "K", "Ë", "X", "Ë"],
                ["X", "X", "X", "X", "X", "X", "X"],
            ],
            Words = [
                new() { Word = "VËRË", Row = 3, Col = 1, Direction = "horizontal" },
                new() { Word = "DIMË", Row = 0, Col = 4, Direction = "vertical" },
                new() { Word = "JETË", Row = 0, Col = 2, Direction = "vertical" },
                new() { Word = "VEL", Row = 3, Col = 1, Direction = "vertical" },
                new() { Word = "MAL", Row = 2, Col = 4, Direction = "horizontal" },
                new() { Word = "VAJ", Row = 0, Col = 0, Direction = "horizontal" },
                new() { Word = "PLAKË", Row = 5, Col = 0, Direction = "horizontal" },
                new() { Word = "VIT", Row = 0, Col = 0, Direction = "vertical" },
                new() { Word = "FLETË", Row = 1, Col = 6, Direction = "vertical" },
            ]
        },
        // Day 2 (8x8): DUA, DJALI, LUMË, DIKU, BABAI, HËNË, FUND, MAL, PIKË, QEN, NJË, KAFË, KUQ
        new()
        {
            GridSize = 8,
            Solution = [
                ["X", "X", "X", "X", "X", "X", "P", "X"],
                ["K", "A", "F", "Ë", "X", "X", "I", "X"],
                ["U", "X", "U", "X", "D", "I", "K", "U"],
                ["Q", "E", "N", "X", "J", "X", "Ë", "X"],
                ["X", "X", "D", "U", "A", "X", "X", "H"],
                ["X", "M", "X", "X", "L", "U", "M", "Ë"],
                ["B", "A", "B", "A", "I", "X", "X", "N"],
                ["X", "L", "X", "X", "X", "N", "J", "Ë"],
            ],
            Words = [
                new() { Word = "DUA", Row = 4, Col = 2, Direction = "horizontal" },
                new() { Word = "DJALI", Row = 2, Col = 4, Direction = "vertical" },
                new() { Word = "LUMË", Row = 5, Col = 4, Direction = "horizontal" },
                new() { Word = "DIKU", Row = 2, Col = 4, Direction = "horizontal" },
                new() { Word = "BABAI", Row = 6, Col = 0, Direction = "horizontal" },
                new() { Word = "HËNË", Row = 4, Col = 7, Direction = "vertical" },
                new() { Word = "FUND", Row = 1, Col = 2, Direction = "vertical" },
                new() { Word = "MAL", Row = 5, Col = 1, Direction = "vertical" },
                new() { Word = "PIKË", Row = 0, Col = 6, Direction = "vertical" },
                new() { Word = "QEN", Row = 3, Col = 0, Direction = "horizontal" },
                new() { Word = "NJË", Row = 7, Col = 5, Direction = "horizontal" },
                new() { Word = "KAFË", Row = 1, Col = 0, Direction = "horizontal" },
                new() { Word = "KUQ", Row = 1, Col = 0, Direction = "vertical" },
            ]
        },
        // Day 3 (8x8): BLETË, DARKË, MIZËR, KOT, NATË, TOKA, VAJZË, ARI, INAT, LOT, BUZ, JET, KJO
        new()
        {
            GridSize = 8,
            Solution = [
                ["I", "N", "A", "T", "X", "D", "X", "X"],
                ["X", "X", "R", "X", "X", "A", "X", "N"],
                ["X", "M", "I", "Z", "Ë", "R", "X", "A"],
                ["X", "X", "X", "X", "X", "K", "O", "T"],
                ["X", "B", "L", "E", "T", "Ë", "X", "Ë"],
                ["K", "X", "O", "X", "O", "X", "B", "X"],
                ["J", "E", "T", "X", "K", "X", "U", "X"],
                ["O", "X", "X", "V", "A", "J", "Z", "Ë"],
            ],
            Words = [
                new() { Word = "BLETË", Row = 4, Col = 1, Direction = "horizontal" },
                new() { Word = "DARKË", Row = 0, Col = 5, Direction = "vertical" },
                new() { Word = "MIZËR", Row = 2, Col = 1, Direction = "horizontal" },
                new() { Word = "KOT", Row = 3, Col = 5, Direction = "horizontal" },
                new() { Word = "NATË", Row = 1, Col = 7, Direction = "vertical" },
                new() { Word = "TOKA", Row = 4, Col = 4, Direction = "vertical" },
                new() { Word = "VAJZË", Row = 7, Col = 3, Direction = "horizontal" },
                new() { Word = "ARI", Row = 0, Col = 2, Direction = "vertical" },
                new() { Word = "INAT", Row = 0, Col = 0, Direction = "horizontal" },
                new() { Word = "LOT", Row = 4, Col = 2, Direction = "vertical" },
                new() { Word = "BUZ", Row = 5, Col = 6, Direction = "vertical" },
                new() { Word = "JET", Row = 6, Col = 0, Direction = "horizontal" },
                new() { Word = "KJO", Row = 5, Col = 0, Direction = "vertical" },
            ]
        },
        // Day 4 (9x9): UJKUJ, VAJ, TIJ, KISHA, ZANË, QUMËS, PULË, UJË, JAVË, ERA, QEN, TRE, JET, DHE, INAT, FUND
        new()
        {
            GridSize = 9,
            Solution = [
                ["X", "Q", "E", "N", "X", "F", "U", "N", "D"],
                ["X", "X", "R", "X", "X", "X", "X", "X", "H"],
                ["X", "J", "A", "V", "Ë", "X", "T", "R", "E"],
                ["X", "X", "X", "A", "X", "X", "I", "X", "X"],
                ["X", "X", "U", "J", "K", "U", "J", "X", "I"],
                ["X", "P", "X", "X", "I", "X", "X", "X", "N"],
                ["Q", "U", "M", "Ë", "S", "X", "U", "X", "A"],
                ["X", "L", "X", "X", "H", "X", "J", "E", "T"],
                ["X", "Ë", "X", "Z", "A", "N", "Ë", "X", "X"],
            ],
            Words = [
                new() { Word = "UJKUJ", Row = 4, Col = 2, Direction = "horizontal" },
                new() { Word = "VAJ", Row = 2, Col = 3, Direction = "vertical" },
                new() { Word = "TIJ", Row = 2, Col = 6, Direction = "vertical" },
                new() { Word = "KISHA", Row = 4, Col = 4, Direction = "vertical" },
                new() { Word = "ZANË", Row = 8, Col = 3, Direction = "horizontal" },
                new() { Word = "QUMËS", Row = 6, Col = 0, Direction = "horizontal" },
                new() { Word = "PULË", Row = 5, Col = 1, Direction = "vertical" },
                new() { Word = "UJË", Row = 6, Col = 6, Direction = "vertical" },
                new() { Word = "JAVË", Row = 2, Col = 1, Direction = "horizontal" },
                new() { Word = "ERA", Row = 0, Col = 2, Direction = "vertical" },
                new() { Word = "QEN", Row = 0, Col = 1, Direction = "horizontal" },
                new() { Word = "TRE", Row = 2, Col = 6, Direction = "horizontal" },
                new() { Word = "JET", Row = 7, Col = 6, Direction = "horizontal" },
                new() { Word = "DHE", Row = 0, Col = 8, Direction = "vertical" },
                new() { Word = "INAT", Row = 4, Col = 8, Direction = "vertical" },
                new() { Word = "FUND", Row = 0, Col = 5, Direction = "horizontal" },
            ]
        },
        // Day 5 (9x9): RËRË, ARTH, PLAKË, DHE, ERA, SHTËPI, KAFË, JAVË, END, DIMË, FLETË, DUA, ORA, LOT, JET, DIM, TRE
        new()
        {
            GridSize = 9,
            Solution = [
                ["X", "S", "H", "T", "Ë", "P", "I", "X", "J"],
                ["X", "X", "X", "R", "X", "L", "X", "X", "A"],
                ["L", "X", "X", "E", "R", "A", "X", "X", "V"],
                ["O", "R", "A", "X", "X", "K", "A", "F", "Ë"],
                ["T", "X", "R", "Ë", "R", "Ë", "X", "L", "X"],
                ["X", "X", "T", "X", "X", "X", "J", "E", "T"],
                ["X", "D", "H", "E", "X", "D", "X", "T", "X"],
                ["X", "U", "X", "N", "X", "I", "X", "Ë", "X"],
                ["X", "A", "X", "D", "I", "M", "Ë", "X", "X"],
            ],
            Words = [
                new() { Word = "RËRË", Row = 4, Col = 2, Direction = "horizontal" },
                new() { Word = "ARTH", Row = 3, Col = 2, Direction = "vertical" },
                new() { Word = "PLAKË", Row = 0, Col = 5, Direction = "vertical" },
                new() { Word = "DHE", Row = 6, Col = 1, Direction = "horizontal" },
                new() { Word = "ERA", Row = 2, Col = 3, Direction = "horizontal" },
                new() { Word = "SHTËPI", Row = 0, Col = 1, Direction = "horizontal" },
                new() { Word = "KAFË", Row = 3, Col = 5, Direction = "horizontal" },
                new() { Word = "JAVË", Row = 0, Col = 8, Direction = "vertical" },
                new() { Word = "END", Row = 6, Col = 3, Direction = "vertical" },
                new() { Word = "DIMË", Row = 8, Col = 3, Direction = "horizontal" },
                new() { Word = "FLETË", Row = 3, Col = 7, Direction = "vertical" },
                new() { Word = "DUA", Row = 6, Col = 1, Direction = "vertical" },
                new() { Word = "ORA", Row = 3, Col = 0, Direction = "horizontal" },
                new() { Word = "LOT", Row = 2, Col = 0, Direction = "vertical" },
                new() { Word = "JET", Row = 5, Col = 6, Direction = "horizontal" },
                new() { Word = "DIM", Row = 6, Col = 5, Direction = "vertical" },
                new() { Word = "TRE", Row = 0, Col = 3, Direction = "vertical" },
            ]
        },
        // Day 6 (10x10): DERË, VEL, GJËNDË, PIKTURË, PUNË, GJEL, DIKU, BUKUR, ZOT, KUQ, BUZ, LIBËR, END, LOT, SAJ, JETË, ORA, KJO
        new()
        {
            GridSize = 10,
            Solution = [
                ["X", "B", "U", "Z", "X", "X", "G", "J", "E", "L"],
                ["X", "X", "X", "O", "X", "X", "J", "X", "N", "X"],
                ["P", "I", "K", "T", "U", "R", "Ë", "X", "D", "X"],
                ["U", "X", "U", "X", "X", "X", "N", "X", "X", "B"],
                ["N", "X", "Q", "X", "V", "X", "D", "I", "K", "U"],
                ["Ë", "X", "X", "D", "E", "R", "Ë", "X", "X", "K"],
                ["X", "K", "X", "X", "L", "X", "X", "X", "X", "U"],
                ["X", "J", "X", "S", "X", "L", "I", "B", "Ë", "R"],
                ["X", "O", "R", "A", "X", "O", "X", "X", "X", "X"],
                ["X", "X", "X", "J", "E", "T", "Ë", "X", "X", "X"],
            ],
            Words = [
                new() { Word = "DERË", Row = 5, Col = 3, Direction = "horizontal" },
                new() { Word = "VEL", Row = 4, Col = 4, Direction = "vertical" },
                new() { Word = "GJËNDË", Row = 0, Col = 6, Direction = "vertical" },
                new() { Word = "PIKTURË", Row = 2, Col = 0, Direction = "horizontal" },
                new() { Word = "PUNË", Row = 2, Col = 0, Direction = "vertical" },
                new() { Word = "GJEL", Row = 0, Col = 6, Direction = "horizontal" },
                new() { Word = "DIKU", Row = 4, Col = 6, Direction = "horizontal" },
                new() { Word = "BUKUR", Row = 3, Col = 9, Direction = "vertical" },
                new() { Word = "ZOT", Row = 0, Col = 3, Direction = "vertical" },
                new() { Word = "KUQ", Row = 2, Col = 2, Direction = "vertical" },
                new() { Word = "BUZ", Row = 0, Col = 1, Direction = "horizontal" },
                new() { Word = "LIBËR", Row = 7, Col = 5, Direction = "horizontal" },
                new() { Word = "END", Row = 0, Col = 8, Direction = "vertical" },
                new() { Word = "LOT", Row = 7, Col = 5, Direction = "vertical" },
                new() { Word = "SAJ", Row = 7, Col = 3, Direction = "vertical" },
                new() { Word = "JETË", Row = 9, Col = 3, Direction = "horizontal" },
                new() { Word = "ORA", Row = 8, Col = 1, Direction = "horizontal" },
                new() { Word = "KJO", Row = 6, Col = 1, Direction = "vertical" },
            ]
        },
    ];

    public static Wordle7Puzzle GetTodayPuzzle()
    {
        var jsDay = (int)DateTime.Now.DayOfWeek;
        var dayIndex = jsDay == 0 ? 6 : jsDay - 1;
        return GetPuzzleByDay(dayIndex);
    }

    public static Wordle7Puzzle GetPuzzleByDay(int dayIndex)
    {
        if (dayIndex < 0 || dayIndex >= Puzzles.Count)
            dayIndex = 0;

        var puzzle = Puzzles[dayIndex];
        puzzle.DayIndex = dayIndex;
        puzzle.DayName = DayNames[dayIndex];
        return puzzle;
    }
}
