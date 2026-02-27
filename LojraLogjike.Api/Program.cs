// TEMP TEST: Test snake solver directly with a known path
using LojraLogjike.Api.Services;

Console.WriteLine("=== Snake Solver Test ===");

// Manually create a known 5x5 path:
// (0,0) -> (0,1) -> (1,1) -> (2,1) -> (2,0) -> (3,0) -> (4,0) -> (4,1) -> (4,2)
// Path length: 9, head at (0,0), tail at (4,2)
var testPath = new (int r, int c)[] { (0,0), (0,1), (1,1), (2,1), (2,0), (3,0), (4,0), (4,1), (4,2) };
int testSize = 5;
var rowClues = new int[testSize];
var colClues = new int[testSize];
for (int i = 0; i < testPath.Length; i++)
{
    rowClues[testPath[i].r]++;
    colClues[testPath[i].c]++;
}
Console.WriteLine($"RowClues: [{string.Join(",", rowClues)}], ColClues: [{string.Join(",", colClues)}]");
Console.WriteLine($"Head: (0,0), Tail: (4,2), Length: 9");

// Test with 0 givens
int sol0 = SnakeSolver.CountSolutions(rowClues, colClues, 0, 0, 4, 2, testSize, 9, [], 3);
Console.WriteLine($"0 givens: {sol0}");

// Test with 1 given: step 5 at (2,0)
int sol1 = SnakeSolver.CountSolutions(rowClues, colClues, 0, 0, 4, 2, testSize, 9, [[2, 0, 5]], 3);
Console.WriteLine($"1 given (step5@2,0): {sol1}");

// Test with 2 givens: step 3 at (1,1), step 7 at (4,0)
int sol2 = SnakeSolver.CountSolutions(rowClues, colClues, 0, 0, 4, 2, testSize, 9, [[1, 1, 3], [4, 0, 7]], 3);
Console.WriteLine($"2 givens (step3@1,1 step7@4,0): {sol2}");

// Now test the generator directly
Console.WriteLine("\n=== Generator Test ===");
try
{
    var puzzle = SnakeGenerator.Generate(12345, 0, "Test");
    Console.WriteLine($"SUCCESS! Size={puzzle.Size} Len={puzzle.SnakeLength} Givens={puzzle.Givens.Length}");
    Console.WriteLine($"RowClues: [{string.Join(",", puzzle.RowClues)}]");
    Console.WriteLine($"ColClues: [{string.Join(",", puzzle.ColClues)}]");
}
catch (Exception ex)
{
    Console.WriteLine($"FAILED: {ex.Message}");
}

Console.WriteLine("=== Test Complete ===");
Environment.Exit(0);

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("http://localhost:4200")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseCors();
app.MapControllers();

app.Run();
