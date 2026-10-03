
# NY Islanders Player Performance Analysis

A self-directed project exploring year-over-year player performance using 
real NHL data, built to practice SQL, Python, and data analysis.

## What this does

- Pulls live Islanders roster and player statistics from the NHL's public API
- Loads the data into a SQLite database
- Uses SQL to compare player performance across the 2023-24 and 2024-25 seasons

## Tools used
- Python 
- SQLite / DB Browser for SQLite 
- SQL

## Key finding

Initial analysis using raw point totals suggested Mathew Barzal had the 
largest year-over-year decline. However, after noticing a significant 
difference in games played between seasons, I corrected the analysis to 
use points-per-game instead of raw totals. This revealed a different, 
more accurate result; Noah Dobson actually had the largest per-game 
decline (-0.34 points/game), while Simon Holmström had the largest 
per-game improvement (+0.27 points/game).

This correction mattered because raw totals were biased by how many games 
each player had played, not just how well they performed.

## What I'd do next
- Incorporate the current season's data once enough games have been played 
  for points-per-game to be meaningful
- Expand to the full roster's underlying skaters/goalies separately
- Visualize the results 