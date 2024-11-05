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
                row = []
                for char in line:
                    if char == 'x':
                        # No block allowed
                        row.append(Block('none', fixed=True))
                    elif char == 'o':
                        row.append(Block('empty'))  # Block allowed
                    elif char == 'A':
                        # Fixed reflect block
                        row.append(Block('reflect', fixed=True))
                    elif char == 'B':
                        # Fixed opaque block
                        row.append(Block('opaque', fixed=True))
                    elif char == 'C':
                        # Fixed refract block
                        row.append(Block('refract', fixed=True))
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

    # Create a data dictionary to store all the parsed information
    data = {
        'grid': grid,
        'lasers': lasers,
        'points': points,
        'avaliable_blocks': avaliable_blocks
    }
import itertools

class LazorGame:
    '''
    A class representing the overall Lazors game, handling grid setup,
    laser movement, block placement, and solution validation.
    '''

    def __init__(self, file_path):
        '''
        Initializes the LazorGame with a parsed .bff file configuration.

        Args:
            file_path (str): Path to the .bff file with game setup.
        '''
        data = read_bff_file(file_path)
        self.grid = Grid(data['grid'])
        self.lasers = data['lasers']
        self.points = set(data['points'])  # Convert to set for fast lookup
        self.available_blocks = data['avaliable_blocks']
        self.solution_found = False

    def run_laser(self, laser):
        '''
        Traces the path of a laser, recording positions it intersects.

        Args:
            laser (Laser): The laser instance to move along the grid.

        Returns:
            set: A set of (x, y) positions the laser intersects.
        '''
        laser_path = set()
        while laser.vx != 0 or laser.vy != 0:
            x, y = laser.move()
            if not self.grid.is_within_bounds(x, y):
                break

            block = self.grid.get_block(x, y)
            if block.can_interact_with_laser():
                if block.block_type == 'reflect':
                    laser.reflect_x() if laser.vx else laser.reflect_y()
                elif block.block_type == 'opaque':
                    laser.absorb()
                elif block.block_type == 'refract':
                    laser_path.add((x, y))
                    self.lasers.append(laser.refract_x())
                    self.lasers.append(laser.refract_y())
            laser_path.add((x, y))
        return laser_path

    def validate_solution(self):
        '''
        Checks if all target points are intersected by lasers.

        Returns:
            bool: True if all points are intersected, False otherwise.
        '''
        hit_points = set()
        for laser in self.lasers:
            hit_points.update(self.run_laser(laser))
        return self.points.issubset(hit_points)

    def attempt_block_placements(self):
        '''
        Attempts various placements of available blocks in empty positions
        to find a solution that intersects all target points.
        '''
        empty_positions = self.grid.find_empty_positions()
        block_types = [bt for bt, count in self.available_blocks.items() for _ in range(count)]

        for placement in itertools.permutations(block_types, len(empty_positions)):
            for pos, block_type in zip(empty_positions, placement):
                x, y = pos
                self.grid.place_block(x, y, block_type)
            
            if self.validate_solution():
                self.solution_found = True
                self.output_solution()
                return

            # Reset the grid for next configuration
            for x, y in empty_positions:
                self.grid.set_block(x, y, Block('empty'))

    def output_solution(self):
        '''
        Outputs the solution in a readable format, either as a text file or a visual representation.
        '''
        print("Solution Found!")
        for y, row in enumerate(self.grid.grid):
            for x, block in enumerate(row):
                if block.fixed:
                    print(block.block_type[0].upper(), end=" ")
                elif block.block_type != 'empty':
                    print(block.block_type[0].lower(), end=" ")
                else:
                    print(".", end=" ")
            print()
        print("Target points achieved.")

def main():
    # Initialize the Lazor game with the .bff file
    game = LazorGame('dark_1.bff')
    # Attempt block placements and output solution if found
    game.attempt_block_placements()
    if not game.solution_found:
        print("No solution found.")

if __name__ == '__main__':
    main()

    return data
