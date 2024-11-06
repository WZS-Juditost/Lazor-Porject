import os
import time
import copy
import itertools
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
                True if the block is 'reflect', 'opaque', or 'refract', False otherwise.
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
            The x-component of the laser's direction vector (can be 0, 1 or -1).
        vy (int):
            The y-component of the laser's direction vector (can be 0, 1 or -1).
    '''

    def __init__(self, x, y, vx, vy):
        '''
        Initializes a Laser instance with a starting position and direction vector.

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
        Generates a new Laser object with the x-component of the direction vector reversed.

        Returns:
            Laser:
                A new laser with the same position and
                the x-component of the direction vector reversed.
        '''
        return Laser(self.x, self.y, -self.vx, self.vy)

    def refract_y(self):
        '''
        Generates a new Laser object with the y-component of the direction vector reversed.

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
            grid (list): A 2D list containing Block objects that define the initial grid layout.
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
                True if the block was placed successfully, False if the position was not empty.
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
            A dictionary containing the padded grid, blocks, lasers, and points.
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
                row = [Block('none', fixed=True)]  # Start with a 'none' fixed block for padding
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
            elif line.startswith('A') or line.startswith('B') or line.startswith('C'):
                block_type, count = line.split()
                avaliable_blocks[block_type] = int(count)
            elif line.startswith('L'):
                _, x, y, vx, vy = line.split()
                lasers.append(Laser(int(x), int(y), int(vx), int(vy)))
            elif line.startswith('P'):
                _, x, y = line.split()
                points.append((int(x), int(y)))

    # Adding rows of 'none' fixed blocks above, between, and below the main grid
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
        data = read_bff_file(file_path)
        
        # Initialize grid, lasers, points, and available blocks
        self.grid = Grid(data['grid'])
        self.lasers = data['lasers']
        self.points = set(data['points'])
        self.available_blocks = data['avaliable_blocks']
        self.solution_found = False
        self.initial_lasers = [Laser(laser.x, laser.y, laser.vx, laser.vy) for laser in data['lasers']]

    def process_laser_paths(self, lasers):
        '''
        Calls laser_path for each laser and updates the grid with laser paths,
        handling any new lasers generated by refraction. Additionally, checks
        if all target points are intersected by lasers to validate the solution.

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

            laser_queue.extend(laser_data['new_lasers'])

        return self.points.issubset(hit_points)

    def print_grid(self, grid):
        '''
        Prints the grid in a readable format, marking blocks and lasers appropriately.

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
        Traces the paths of lasers in the grid, updating positions based on interactions.

        Args:
            grid_obj (Grid): 
                An instance of the Grid class, representing the current state of the game grid.
            laser_objs (list of Laser): 
                A list of Laser instances, each representing a laser with a starting position and direction.

        Returns:
            dict: 
                A dictionary with positions and new_lasers:
                    positions (list of list of tuple): 
                        Each sublist represents the path taken by a laser in the grid.
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
                elif x_block.block_type == 'opaque' or y_block.block_type == 'opaque':
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
                elif x_block.block_type == 'empty' or y_block.block_type == 'empty':
                    new_pos = laser.move()
                    current_positions.append(new_pos)
                elif x_block.block_type == 'none' or y_block.block_type == 'none':
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
                Each inner list contains tuples representing possible positions for each block.
        '''
        block_list = [Block(block_type) for block_type, count in block_dict.items() for _ in range(count)]
        available_positions = grid_obj.find_empty_positions()
        all_same_type = all(block.block_type == block_list[0].block_type for block in block_list)
        if all_same_type:
            # Use combinations if all blocks are of the same type
            block_configs = [
                list(positions)
                for positions in itertools.combinations(available_positions, len(block_list))
            ]
        else:
            # Use permutations if blocks are of different types
            block_configs = [
                list(positions)
                for positions in itertools.permutations(available_positions, len(block_list))
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
        block_configurations = self.all_possible_configs(self.grid, self.available_blocks)

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
        # Map available blocks to their types and place them in specified positions
        block_list = []
        for block_letter, count in self.available_blocks.items():
            actual_type = block_type_mapping.get(block_letter, 'empty')
            block_list.extend([actual_type] * count)
        for position, block_type in zip(config, block_list):
            x, y = position
            self.grid.set_block(x, y, Block(block_type))

    def reset_lasers(self):
        '''
        Resets the lasers to only the original lasers with their initial states.
        '''
        self.lasers = [Laser(laser.x, laser.y, laser.vx, laser.vy) for laser in self.initial_lasers]


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
        Outputs the final solution with blocks and laser paths in the grid.
        '''
        print("\nFinal Solution:")
        self.print_grid(self.grid.grid)
        print("\nTarget points have been successfully intersected by lasers.")

def main():
    print("Welcome to the Lazor Game Solver!")
    print("=================================")
    print("This tool attempts to find solutions for Lazor game puzzles defined in .bff files.")
    print("You can either solve a single puzzle by specifying its file path or solve all puzzles in the 'bff_files' folder.")
    print("Let's get started!\n")

    user_input = input("Enter the path to the .bff file you want to solve, or press Enter to solve all examples in 'bff_files': ").strip()
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
                print(f"Time taken for {user_input}: {elapsed_time:.2f} seconds\n")
            else:
                print(f"Failed to solve {user_input}.")
        else:
            print("Invalid file path or file type. Please provide a valid .bff file.")
            return
    else:
        # Run solver on all example files in the 'bff_files' directory
        folder_path = 'bff_files'
        print("Solving all puzzles in the 'bff_files' folder...")
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.bff'):
                file_path = os.path.join(folder_path, file_name)
                print(f"\nProcessing puzzle: {file_name}...")

                start_time = time.time()
                
                game = LazorGame(file_path)
                solved = game.solve()

                elapsed_time = time.time() - start_time
                if solved:
                    total_time += elapsed_time
                    solved_files += 1
                    print(f"Time taken for {file_name}: {elapsed_time:.2f} seconds")
                else:
                    print(f"Failed to solve {file_name}.")

    # Final summary
    print("\n=================================")
    if solved_files > 0:
        print(f"\nAll puzzles processed! Total puzzles solved: {solved_files}")
        print(f"Total time taken to solve puzzles: {total_time:.2f} seconds")
    else:
        print("No puzzles were solved. Please ensure .bff files are available in the 'bff_files' folder.")
    print("Thank you for using the Lazor Game Solver!")
    print("=================================")

if __name__ == '__main__':
    main()