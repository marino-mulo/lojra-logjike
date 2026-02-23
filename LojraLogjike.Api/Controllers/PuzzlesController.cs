using LojraLogjike.Api.Data;
using Microsoft.AspNetCore.Mvc;

namespace LojraLogjike.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PuzzlesController : ControllerBase
{
    [HttpGet("zip/today")]
    public IActionResult GetTodayZip()
    {
        var puzzle = ZipPuzzleData.GetTodayPuzzle();
        return Ok(puzzle);
    }

    [HttpGet("zip/{dayIndex:int}")]
    public IActionResult GetZipByDay(int dayIndex)
    {
        var puzzle = ZipPuzzleData.GetPuzzleByDay(dayIndex);
        return Ok(puzzle);
    }

    [HttpGet("queens/today")]
    public IActionResult GetTodayQueens()
    {
        var puzzle = QueensPuzzleData.GetTodayPuzzle();
        return Ok(puzzle);
    }

    [HttpGet("queens/{dayIndex:int}")]
    public IActionResult GetQueensByDay(int dayIndex)
    {
        var puzzle = QueensPuzzleData.GetPuzzleByDay(dayIndex);
        return Ok(puzzle);
    }

    [HttpGet("wordle7/today")]
    public IActionResult GetTodayWordle7()
    {
        var puzzle = Wordle7PuzzleData.GetTodayPuzzle();
        return Ok(puzzle);
    }

    [HttpGet("wordle7/{dayIndex:int}")]
    public IActionResult GetWordle7ByDay(int dayIndex)
    {
        var puzzle = Wordle7PuzzleData.GetPuzzleByDay(dayIndex);
        return Ok(puzzle);
    }
}
