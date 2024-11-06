# Lazor-Porject
The Lazor Game Solver is a Python program designed to solve puzzles in the Lazor game. In Lazor, players arrange blocks on a grid to direct laser beams to specific target points. The game configuration is provided in `.bff` files, which specify the grid layout, available blocks, laser starting positions, directions, and target points. This program automates the solving process, saving the solution as both text and an image representation.

## Features

- Reads `.bff` configuration files to set up the Lazor game grid, blocks, and lasers.
- Attempts to solve the puzzle by trying all possible block placements on the grid.
- Visualizes the solution by saving an image showing the grid layout, blocks, laser paths, start points, and target points.
- Supports solving multiple puzzles from a folder of `.bff` files.

## Game Logic

1. **Grid Setup**: The grid consists of cells that may contain blocks or empty spaces.
2. **Block Types**:
   - **Reflect ('A')**: Reflects the laser by 90 degrees.
   - **Opaque ('B')**: Absorbs the laser, stopping its movement.
   - **Refract ('C')**: Allows the laser to pass through while also creating a reflected beam.
3. **Lasers**: Start at specified grid positions with defined directions.
4. **Goal**: Place blocks on the grid so that all lasers intersect each specified target point.

## File Structure

- `bff_files/`: Contains `.bff` files defining Lazor puzzles.
- `solution/`: Stores image files of solved puzzles.
- `LazorGame.py`: Main program file containing classes and logic for solving puzzles.

## Classes Overview

### `Block`

Represents a block in the grid. Each block has a type (`reflect`, `opaque`, `refract`, or `empty`) and a fixed status.

### `Laser`

Represents a laser beam with initial coordinates and direction. Lasers move across the grid and interact with blocks.

### `Grid`

Manages the game grid, supports block placement, and contains methods for retrieving and updating cell contents.

### `LazorGame`

Handles the core game logic, solving process, solution validation, and saving solutions. Reads `.bff` files to configure the game, simulates laser paths based on block placements, and generates a solution if all target points are hit.

## Requirements

- Python 3.x
- `Pillow` library (for image generation)

To install `Pillow`, run:
```bash
pip install pillow
