"""
Lazor Game Solver

This program is a solver for the Lazor game. Lazor is a puzzle game in which
the player must arrange blocks on a grid to direct laser beams to specific
target points. Each puzzle is defined in a .bff file, which specifies the grid
layout, available blocks, laser starting positions, directions, and target
points. The goal is to place blocks in the correct positions to ensure that
all laser beams intersect the target points.

Game Logic:
-----------
1. The game grid consists of cells that can contain different types of blocks.
   The lasers start from specific grid cells with given directions.

2. The player places blocks of various types in empty grid cells. Each block
   type interacts with the lasers differently, either reflecting, absorbing,
   or allowing the laser to pass through and split.

3. The solver tries different configurations of block placements until it
   finds a solution where all lasers intersect the specified target points.

4. The solution is saved as a visual representation in an image file,
   displaying the grid layout, blocks, laser paths, start points,
   and target points.

Block Types:
------------
The game includes several block types, each represented by a specific symbol:
'reflect' (Symbol: 'A'):
    Reflects the laser, change its direction by 90 degrees.
'opaque' (Symbol: 'B'):
    Blocks and absorbs the laser beam, preventing it from passing through.
'refract' (Symbol: 'C'):
    Allows the laser to pass through while also creating a reflected beam.
'empty' (Symbol: 'o'):
    An empty space where a block can be placed .
'none' (Symbol: 'x'):
    Represents unavaible. No block can be place on this cell.
'laser' (Symbol: 'L'):
    Represents a laser intersects this cell, used for displaying solution only.

Laser:
------
The `Laser` class represents a laser beam in the Lazor game. Each laser has:
`x` and `y`:
    The initial coordinates of the laser's starting position on the grid.
`vx` and `vy`:
    The direction of the laser beam along the x and y axis.

Attributes:
-----------
`self.grid`:
    The grid object containing all the blocks in the puzzle.
`self.lasers`:
    A list of `Laser` objects, each representing a laser's
    starting position and direction.
`self.points`:
    A set of target points that lasers must intersect to solve the puzzle.
`self.available_blocks`:
    A dictionary of block types and their available counts.
`self.solution_found`:
    A boolean flag indicating whether a solution has been found.
`self.initial_lasers`:
    A copy of the initial laser positions and directions for reset purposes.

Main Solver Flow:
-----------------
1. The solver reads the grid configuration and laser setup
   from the specified .bff file.
2. It generates all possible placements for the blocks
   based on their availability and tries each configuration.
3. For each configuration, it simulates the laser paths
   based on block interactions.
4. If all target points are hit by lasers, the solution is considered found.
5. The final solution is saved as an image.

Classes:
--------
`Block`:
    Represents a block in the grid with a specified type and fixed status.
`Laser`:
    Represents a laser beam with initial coordinates and direction.
`Grid`:
    Manages the game grid and contains methods for managing blocks.
`LazorGame`:
    Handles the game logic, solving process, and saving solutions.

"""

import os
import time
import copy
import itertools
from PIL import Image, ImageDraw, ImageFont
import math


class Block:
    '''
    A class representing a block in the Lazors game grid.

    Attributes:
        block_type (str):
            The type of the block ('reflect', 'opaque', 'refract', 'empty').
        fixed (bool):
            Whether the block is fixed in position (True) or movable (False).
    '''

    def __init__(self, block_type, fixed=False):
        '''
        Initializes a Block instance with a specified type and fixed status.

        Args:
            block_type (str):
                Type of the block ('reflect', 'opaque', 'refract', 'empty').
            fixed (bool, optional):
                If True, the block is fixed in place. Otherwise, it is movable.
                Default is False.
        '''
        self.block_type = block_type  # 'reflect', 'opaque', 'refract', 'empty'
        self.fixed = fixed

    def is_empty(self):
        '''
        Checks if the block is an empty, movable position.

        Returns:
            bool:
                True if the block is empty and movable, False otherwise.
        '''
        return self.block_type == 'empty' and not self.fixed

    def can_interact_with_laser(self):
        '''
        Determines if the block can interact with a laser.

        Returns:
            bool:
                True if the block is 'reflect', 'opaque', or 'refract'.
                False otherwise.
        '''
        return self.block_type in ('reflect', 'opaque', 'refract')


class Laser:
    '''
    A class representing a laser in the Lazors game.

    Attributes:
        x (int):
            The x-coordinate of the laser's starting position.
        y (int):
            The y-coordinate of the laser's starting position.
        vx (int):
            The x-component of the laser's direction vector.
        vy (int):
            The y-component of the laser's direction vector.
    '''

    def __init__(self, x, y, vx, vy):
        '''
        Initializes a Laser instance with a starting position and direction.

        Args:
            x (int):
                The x-coordinate of the laser's starting position.
            y (int):
                The y-coordinate of the laser's starting position.
            vx (int):
                The x-component of the laser's direction vector (0, 1 or -1).
            vy (int):
                The y-component of the laser's direction vector (0,1 or -1).
        '''
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        '''
        Updates the laser's position based on its current direction.

        Returns:
            tuple: The new (x, y) position after moving.
        '''
        self.x += self.vx
        self.y += self.vy
        return (self.x, self.y)

    def reflect_x(self):
        '''
        Reflects the laser along the x-axis by reversing
        the x-component of the direction vector.
        '''
        self.vx = -self.vx

    def reflect_y(self):
        '''
        Reflects the laser along the y-axis by reversing
        the y-component of the direction vector.
        '''
        self.vy = -self.vy

    def refract_x(self):
        '''
        Generates new Laser with x-component of the direction vector reversed.

        Returns:
            Laser:
                A new laser with the same position and
                the x-component of the direction vector reversed.
        '''
        return Laser(self.x, self.y, -self.vx, self.vy)

    def refract_y(self):
        '''
        Generates new Laser with y-component of the direction vector reversed.

        Returns:
            Laser:
                A new laser with the same position and
                the y-component of the direction vector reversed.
        '''
        return Laser(self.x, self.y, self.vx, -self.vy)

    def absorb(self):
        '''
        Terminates the laser's movement by setting its direction to (0, 0).
        '''
        self.vx, self.vy = 0, 0

    def current_position(self):
        '''
        Returns the current position of the laser.

        Returns:
            tuple: The (x, y) position of the laser.
        '''
        return (self.x, self.y)


class Grid:
    '''
    A class representing the game grid in the Lazors game.

    Attributes:
        grid (list):
            A 2D list of Block objects representing the grid layout.
    '''

    def __init__(self, grid):
        '''
        Initializes a Grid instance with a specified grid layout.

        Args:
            grid (list):
               Containing Block objects that define the initial grid layout.
        '''
        self.grid = grid
        self.initial_grid = copy.deepcopy(grid)

    def set_block(self, x, y, block):
        '''
        Places a block at a specific position in the grid.

        Args:
            x (int): The x-coordinate of the block position.
            y (int): The y-coordinate of the block position.
            block (Block): The block object to place at the specified position.
        '''
        self.grid[y][x] = block

    def get_block(self, x, y):
        '''
        Retrieves the block at a specific position in the grid.

        Args:
            x (int): The x-coordinate of the block position.
            y (int): The y-coordinate of the block position.

        Returns:
            Block: The block at the specified position.
        '''
        return self.grid[y][x]

    def is_within_bounds(self, x, y):
        '''
        Checks if the specified position is within the grid boundaries.

        Args:
            x (int):
                The x-coordinate to check.
            y (int):
                The y-coordinate to check.

        Returns:
            bool:
                True if the position is within bounds, False otherwise.
        '''
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def reset_to_initial(self):
        '''
        Resets the grid back to its initial configuration.
        '''
        self.grid = copy.deepcopy(self.initial_grid)

    def find_empty_positions(self):
        '''
        Finds all empty, movable positions in the grid.

        Returns:
            empty_positions (list):
                List of (x, y) positions that are empty and can hold a block.
        '''
        empty_positions = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.get_block(x, y).is_empty():
                    empty_positions.append((x, y))
        return empty_positions

    def place_block(self, x, y, block_type):
        '''
        Places a new block of a specified type at a given position.

        Args:
            x (int):
                The x-coordinate where the block will be placed.
            y (int):
                The y-coordinate where the block will be placed.
            block_type (str):
                Type of the block to place.

        Returns:
            bool:
                True if the block was placed successfully.
                False if the position was not empty.
        '''
        if self.is_within_bounds(x, y) and self.get_block(x, y).is_empty():
            self.set_block(x, y, Block(block_type))
            return True
        return False


def read_bff_file(file_path):
    '''
    This function opens and parses a .bff file line by line,
    getting all the information and storing them in a dictionary.
    It adds 'none' fixed blocks around each row, between elements,
    and rows between each line in the grid.

    Args:
        file_path (string):
            The path to the .bff file to be read

    Returns:
        data (dictionary):
            A dictionary containing the grid, blocks, lasers, and points.
    '''
    grid = []
    lasers = []
    points = []
    avaliable_blocks = {'A': 0, 'B': 0, 'C': 0}

    with open(file_path, 'r') as file:
        grid_section = False
        for line in file:
            line = line.strip()

            # Skip all the comments
            if line.startswith('#') or not line:
                continue

            if line == 'GRID START':
                grid_section = True
                continue
            if line == 'GRID STOP':
                grid_section = False
                continue
            if grid_section:
                # Start with a 'none' fixed block for padding
                row = [Block('none', fixed=True)]
                for char in line:
                    if char == 'x':
                        row.append(Block('none', fixed=True))
                        row.append(Block('none', fixed=True))
                    elif char == 'o':
                        row.append(Block('empty'))
                        row.append(Block('none', fixed=True))
                    elif char == 'A':
                        row.append(Block('reflect', fixed=True))
                        row.append(Block('none', fixed=True))
                    elif char == 'B':
                        row.append(Block('opaque', fixed=True))
                        row.append(Block('none', fixed=True))
                    elif char == 'C':
                        row.append(Block('refract', fixed=True))
                        row.append(Block('none', fixed=True))
                grid.append(row)
            elif (line.startswith('A') or
                  line.startswith('B') or
                  line.startswith('C')):
                block_type, count = line.split()
                avaliable_blocks[block_type] = int(count)
            elif line.startswith('L'):
                _, x, y, vx, vy = line.split()
                lasers.append(Laser(int(x), int(y), int(vx), int(vy)))
            elif line.startswith('P'):
                _, x, y = line.split()
                points.append((int(x), int(y)))

    # Adding rows of 'none' fixed blocks above, between, and below the main
    # grid
    padded_grid = [[Block('none', fixed=True)] * len(grid[0])]
    for row in grid:
        padded_grid.append(row)
        padded_grid.append([Block('none', fixed=True)] * len(row))

    # Create a data dictionary to store all the parsed information
    data = {
        'grid': padded_grid,
        'lasers': lasers,
        'points': points,
        'avaliable_blocks': avaliable_blocks
    }

    return data


class LazorGame:
    '''
    A class representing the Lazor Game, handling grid setup,
    laser movement, block placement, and solution validation.
    '''

    def __init__(self, file_path):
        '''
        Initializes the LazorGame with a parsed .bff file configuration.

        Args:
            file_path (str):
                Path to the .bff file with game setup.
        '''
        # Read and parse data from the .bff file
        self.file_path = file_path
        data = read_bff_file(file_path)

        # Initialize grid, lasers, points, and available blocks
        self.grid = Grid(data['grid'])
        self.lasers = data['lasers']
        self.points = set(data['points'])
        self.available_blocks = data['avaliable_blocks']
        self.solution_found = False
        self.initial_lasers = [
            Laser(
                laser.x,
                laser.y,
                laser.vx,
                laser.vy) for laser in data['lasers']]

    def process_laser_paths(self, lasers):
        '''
        Calls laser_path for each laser and updates the grid with laser paths,
        handling any new lasers generated by refraction. Additionally, checks
        if all target points are intersected by lasers to validate solution.

        Returns:
            bool:
                True if the solution is valid, False otherwise.
        '''
        laser_queue = list(lasers)
        hit_points = set()

        while laser_queue:
            current_laser = laser_queue.pop(0)  # Get the next laser to process
            laser_data = self.calculate_laser_path(self.grid, [current_laser])

            for path in laser_data['positions']:
                for (x, y) in path:
                    if self.grid.is_within_bounds(x, y):
                        # Add to hit points set
                        hit_points.add((x, y))
                        block_type = self.grid.get_block(x, y).block_type
                        if block_type == 'empty' or block_type == 'none':
                            self.grid.grid[y][x] = Block('laser', fixed=True)

            laser_queue.extend(laser_data['new_lasers'])

        return self.points.issubset(hit_points)

    def print_grid(self, grid):
        '''
        Prints the grid in a readable format,
        marking blocks and lasers appropriately.

        Args:
            grid (list of list of Block):
                A 2D list representing the game grid.
        '''
        for row in grid:
            row_repr = []
            for block in row:
                if block.block_type == 'laser':
                    row_repr.append('L')
                elif block.block_type == 'reflect':
                    row_repr.append('A')
                elif block.block_type == 'opaque':
                    row_repr.append('B')
                elif block.block_type == 'refract':
                    row_repr.append('C')
                else:
                    row_repr.append('.')
            print(' '.join(row_repr))

    def calculate_laser_path(self, grid_obj, laser_objs):
        '''
        Traces the paths of lasers in the grid,
        updating positions based on interactions.

        Args:
            grid_obj (Grid):
                An instance of the Grid class,
                representing the current state of the game grid.
            laser_objs (list of Laser):
                A list of Laser instances, each representing
                a laser with a starting position and direction.

        Returns:
            dict:
                A dictionary with positions and new_lasers:
                    positions (list of list of tuple):
                        Each sublist represents the path taken by a laser.
                    new_lasers (list of Laser):
                        A list of new Laser instances created by refraction.
        '''
        MAX_STEPS = 500
        positions = []
        new_lasers = []

        for laser in laser_objs:
            current_positions = []
            current_positions.append(laser.current_position())

            steps = 0

            while steps < MAX_STEPS:  # Stop if steps exceed MAX_STEPS
                steps += 1
                new_pos = laser.current_position()
                x_new = (new_pos[0] + laser.vx, new_pos[1])
                y_new = (new_pos[0], new_pos[1] + laser.vy)

                # Check if the new position is within the grid bounds
                if not grid_obj.is_within_bounds(x_new[0], x_new[1]):
                    break
                elif not grid_obj.is_within_bounds(y_new[0], y_new[1]):
                    break

                x_block = grid_obj.get_block(x_new[0], x_new[1])
                y_block = grid_obj.get_block(y_new[0], y_new[1])

                if x_block.block_type == 'reflect':
                    laser.reflect_x()
                    new_pos = laser.move()
                    current_positions.append(new_pos)
                elif y_block.block_type == 'reflect':
                    laser.reflect_y()
                    new_pos = laser.move()
                    current_positions.append(new_pos)
                elif (x_block.block_type == 'opaque' or
                      y_block.block_type == 'opaque'):
                    laser.absorb()
                    break
                elif x_block.block_type == 'refract':
                    new_laser = laser.refract_x()
                    new_pos = laser.move()
                    current_positions.append(new_pos)
                    new_lasers.append(new_laser)
                elif y_block.block_type == 'refract':
                    new_laser = laser.refract_y()
                    new_pos = laser.move()
                    current_positions.append(new_pos)
                    new_lasers.append(new_laser)
                elif (x_block.block_type == 'empty' or
                      y_block.block_type == 'empty'):
                    new_pos = laser.move()
                    current_positions.append(new_pos)
                elif (x_block.block_type == 'none' or
                      y_block.block_type == 'none'):
                    new_pos = laser.move()
                    current_positions.append(new_pos)

                # If the laser is absorbed or out of bounds, break the loop
                if laser.vx == 0 and laser.vy == 0:
                    break

            positions.append(current_positions)

        return {'positions': positions, 'new_lasers': new_lasers}

    def all_possible_configs(self, grid_obj, block_dict):
        '''
        Generates all possible configurations for placing blocks on the grid.

        Args:
            grid_obj (Grid):
                An instance of the Grid class.
            block_dict (dict):
                A dictionary with block types as keys and counts as values.

        Returns:
            block_configs (list of list of tuple):
                Each inner list contains tuples
                representing possible positions for each block.
        '''
        block_list = [Block(block_type) for block_type,
                      count in block_dict.items() for _ in range(count)]
        available_positions = grid_obj.find_empty_positions()
        all_same_type = all(
            block.block_type ==
            block_list[0].block_type for block in block_list)
        if all_same_type:
            # Use combinations if all blocks are of the same type
            block_configs = [
                list(positions)
                for positions in itertools.combinations(
                    available_positions, len(block_list))
            ]
        else:
            # Use permutations if blocks are of different types
            block_configs = [
                list(positions)
                for positions in itertools.permutations(
                    available_positions, len(block_list))
            ]

        return block_configs

    def solve(self):
        '''
        Attempts to solve the puzzle by trying different block placements.

        Returns:
            bool:
                True if a solution is found, False otherwise.
        '''
        # Generate all possible configurations of block placements
        block_configurations = self.all_possible_configs(
            self.grid, self.available_blocks)

        for config in block_configurations:
            self.place_blocks_in_grid(config)

            if self.process_laser_paths(self.lasers):
                self.solution_found = True
                print("Solution found!")
                self.output_solution()
                return True

            # Reset the game
            self.grid.reset_to_initial()
            self.reset_lasers()

        print("No solution found.")
        return False

    def place_blocks_in_grid(self, config):
        '''
        Places blocks on the grid based on the provided configuration.

        Args:
            config (list of tuples):
                List of positions where each block should be placed.
        '''
        block_type_mapping = {'A': 'reflect', 'B': 'opaque', 'C': 'refract'}
        # Map available blocks to their types and place them in specified
        # positions
        block_list = []
        for block_letter, count in self.available_blocks.items():
            actual_type = block_type_mapping.get(block_letter, 'empty')
            block_list.extend([actual_type] * count)
        for position, block_type in zip(config, block_list):
            x, y = position
            self.grid.set_block(x, y, Block(block_type))

    def reset_lasers(self):
        '''
        Resets the lasers to the original lasers with their initial states.
        '''
        self.lasers = [Laser(laser.x, laser.y, laser.vx, laser.vy)
                       for laser in self.initial_lasers]

    def validate_solution(self):
        '''
        Checks if all target points are intersected by lasers.

        Returns:
            bool:
                True if all points are intersected, False otherwise.
        '''
        hit_points = set()
        for laser in self.lasers:
            laser_data = self.calculate_laser_path(self.grid, [laser])
            for path in laser_data['positions']:
                hit_points.update(path)
        return self.points.issubset(hit_points)

    def output_solution(self):
        '''
        Outputs the final solution.
        '''
        print("\nFinal Solution:")

        # Create a set of laser starting points for easy lookup
        laser_start_points = {(laser.x, laser.y)
                              for laser in self.initial_lasers}

        # Print the grid with blocks, laser paths, laser start points, and
        # target points
        for y, row in enumerate(self.grid.grid):
            row_repr = []
            for x, block in enumerate(row):
                if (x, y) in laser_start_points:
                    # Mark laser starting points (using 'S' here)
                    row_repr.append('S')
                elif (x, y) in self.points:
                    # Mark target points (using 'T' here)
                    row_repr.append('T')
                elif block.block_type == 'laser':
                    row_repr.append('L')
                elif block.block_type == 'reflect':
                    row_repr.append('A')
                elif block.block_type == 'opaque':
                    row_repr.append('B')
                elif block.block_type == 'refract':
                    row_repr.append('C')
                elif block.block_type == 'empty':
                    row_repr.append('o')
                else:
                    row_repr.append('.')
            print(' '.join(row_repr))

        print(
            "\nAll target points successfully intersects by lasers.")

        # Print each block's position
        print("\nBlocks placed:")
        for y, row in enumerate(self.grid.grid):
            for x, block in enumerate(row):
                if block.block_type in ['reflect', 'opaque', 'refract']:
                    print(
                        f"Block '{block.block_type}' placed at position "
                        f"({x}, {y})"
                    )

        # Print laser start points
        print("\nLaser starting points:")
        for point in laser_start_points:
            print(f"Laser starts at position {point}")

    def save_solution_as_image(self, solve_time):
        '''
        Saves the solved grid as an image
        in the 'solution' folder with additional information.

        Args:
            solve_time (float):
                The time taken to solve the puzzle, in seconds.
        '''
        # Ensure the 'solution' folder exists
        solution_dir = "solution"
        os.makedirs(solution_dir, exist_ok=True)
        cell_size = 30
        grid_width = len(self.grid.grid[0]) * cell_size
        grid_height = len(self.grid.grid) * cell_size

        # Font setup
        font_size = 11
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        text_lines = [
            f"Game: {os.path.basename(self.file_path)}",
            f"Time to solve: {solve_time:.2f} seconds",
            "Blocks placed:",
            *[f"- {block.block_type.capitalize()} at ({x}, {y})"
              for y, row in enumerate(self.grid.grid)
              for x, block in enumerate(row)
              if block.block_type in ['reflect', 'opaque', 'refract']],
            "Laser starting points:",
            *[f"- Start at ({x}, {y}) with direction ({vx}, {vy})"
              for (x, y), (vx, vy) in {
                  (laser.x, laser.y): (laser.vx, laser.vy)
                  for laser in self.initial_lasers
              }.items()]
        ]

        text_space_height = sum(
            font.getbbox(line)[3] + 5 for line in text_lines) + 10
        image_height = grid_height + text_space_height
        image = Image.new('RGB', (grid_width, image_height), 'white')
        draw = ImageDraw.Draw(image)

        colors = {
            'reflect': 'blue',
            'opaque': 'orange',
            'refract': 'yellow',
            'empty': 'gray',
            'none': 'white'
        }
        labels = {
            'reflect': 'A',
            'opaque': 'B',
            'refract': 'C',
            'laser_start': 'S',
            'target': 'T'
        }

        laser_start_points = {(laser.x, laser.y): (laser.vx, laser.vy)
                              for laser in self.initial_lasers}
        for y, row in enumerate(self.grid.grid):
            for x, block in enumerate(row):
                top_left = (x * cell_size, y * cell_size)
                bottom_right = ((x + 1) * cell_size, (y + 1) * cell_size)

                if (x, y) in laser_start_points:
                    draw.rectangle([top_left, bottom_right], fill="red")
                    # Draw an arrow based on the laser's direction
                    vx, vy = laser_start_points[(x, y)]
                    center = (
                        top_left[0] + cell_size // 2,
                        top_left[1] + cell_size // 2)
                    arrow_length = cell_size // 2
                    arrow_end = (
                        center[0] + arrow_length * vx,
                        center[1] + arrow_length * vy
                    )
                    draw.line([center, arrow_end], fill="white", width=2)
                    # Draw arrowhead
                    arrowhead_length = 6
                    angle_offset = math.pi / 6
                    angle_main = math.atan2(vy, vx)
                    left_end = (
                        arrow_end[0] -
                        arrowhead_length *
                        math.cos(
                            angle_main +
                            angle_offset),
                        arrow_end[1] -
                        arrowhead_length *
                        math.sin(
                            angle_main +
                            angle_offset))
                    right_end = (
                        arrow_end[0] -
                        arrowhead_length *
                        math.cos(
                            angle_main -
                            angle_offset),
                        arrow_end[1] -
                        arrowhead_length *
                        math.sin(
                            angle_main -
                            angle_offset))
                    draw.line([arrow_end, left_end], fill="white", width=2)
                    draw.line([arrow_end, right_end], fill="white", width=2)
                    draw.text(
                        (top_left[0] + cell_size // 5,
                         top_left[1] + cell_size // 3),
                        labels['laser_start'],
                        fill="white",
                        font=font)

                elif (x, y) in self.points:
                    draw.rectangle([top_left, bottom_right],
                                   outline="green", width=3)
                    draw.text(
                        (top_left[0] + cell_size // 5,
                         top_left[1] + cell_size // 3),
                        labels['target'],
                        fill="green",
                        font=font)
                else:
                    color = colors.get(block.block_type, 'white')
                    draw.rectangle([top_left, bottom_right], fill=color)
                    if block.block_type in labels:
                        draw.text((top_left[0] + cell_size // 5,
                                   top_left[1] + cell_size // 3),
                                  labels[block.block_type],
                                  fill="black",
                                  font=font)

        # Draw grid lines
        for i in range(1, len(self.grid.grid[0])):
            x = i * cell_size
            draw.line([(x, 0), (x, grid_height)], fill="black", width=1)
        for i in range(1, len(self.grid.grid)):
            y = i * cell_size
            draw.line([(0, y), (grid_width, y)], fill="black", width=1)

        # Draw laser path dots for cells with laser path
        for y, row in enumerate(self.grid.grid):
            for x, block in enumerate(row):
                if block.block_type == 'laser' and (
                        x, y) not in laser_start_points:
                    center = (
                        x * cell_size + cell_size // 2,
                        y * cell_size + cell_size // 2)
                    draw.ellipse([center[0] - 2, center[1] - 2,
                                 center[0] + 2, center[1] + 2], fill="red")

        # Add text information at the bottom of the image
        text_y = grid_height + 10
        for line in text_lines:
            draw.text((10, text_y), line, fill="black", font=font)
            text_y += font.getbbox(line)[3] + 5

        # Save the image
        filename = os.path.basename(self.file_path)
        solution_filename = os.path.join(
            solution_dir, f"{os.path.splitext(filename)[0]}_solution.png")
        image.save(solution_filename)

        print(f"Solution saved as an image to {solution_filename}")


def main():
    print("Welcome to the Lazor Game Solver!")
    print("=================================")
    print(
        "This tool attempts to find solutions for Lazor game puzzles"
        "defined in .bff files."
    )
    print(
        "You can either solve a single puzzle by specifying its file path or "
        "solve all puzzles in the 'bff_files' folder."
    )

    print("Let's get started!\n")

    user_input = input(
        "Enter the path to the .bff file you want to solve,"
        "or press Enter to solve all examples in 'bff_files': "
    ).strip()
    total_time = 0
    solved_files = 0

    if user_input:
        # Run solver on a specific file
        if os.path.isfile(user_input) and user_input.endswith('.bff'):
            print(f"\nAttempting to solve puzzle: {user_input}...")
            start_time = time.time()

            game = LazorGame(user_input)
            solved = game.solve()  # Check if a solution was found

            elapsed_time = time.time() - start_time
            if solved:
                total_time += elapsed_time
                solved_files += 1
                # Pass solve_time to save_solution_as_image
                game.save_solution_as_image(elapsed_time)
                print(
                    f"Time taken for {user_input}: "
                    "{elapsed_time:.2f} seconds\n"
                )
            else:
                print(f"Failed to solve {user_input}.")
        else:
            print("Invalid file path or file type."
                  "Please provide a valid .bff file."
                  )
            return
    else:
        # Run solver on all example files in the 'bff_files' directory
        folder_path = 'bff_files'
        print("Solving all puzzles in the 'bff_files' folder...")
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.bff'):
                file_path = os.path.join(folder_path, file_name)
                print(f"\nSolving puzzle: {file_name}...")

                start_time = time.time()

                game = LazorGame(file_path)
                solved = game.solve()

                elapsed_time = time.time() - start_time
                if solved:
                    total_time += elapsed_time
                    solved_files += 1
                    # Pass solve_time to save_solution_as_image
                    game.save_solution_as_image(elapsed_time)
                    print(
                        f"Time taken for {file_name}: "
                        "{elapsed_time:.2f} seconds"
                    )
                else:
                    print(f"Failed to solve {file_name}.")

    # Final summary
    print("\n=================================")
    if solved_files > 0:
        print(f"\nAll puzzles processed! Total puzzles solved: {solved_files}")
        print(f"Total time taken to solve puzzles: {total_time:.2f} seconds")
    else:
        print("No puzzles were solved. Please ensure .bff files"
              "are available in the 'bff_files' folder."
              )
    print("Thank you for using the Lazor Game Solver!")
    print("=================================")


if __name__ == '__main__':
    main()
