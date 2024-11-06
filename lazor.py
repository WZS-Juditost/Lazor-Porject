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
    A class for handling grid setup, laser movement, block placement, and solution validation.
    '''

    def __init__(self, file_path):
        '''
        Initializes the LazorGame with a parsed .bff file configuration.
        '''
        data = read_bff_file(file_path)
        self.grid = Grid(data['grid'])
        self.initial_lasers = data['lasers']  # Store original lasers to reset as needed
        self.points = set(data['points'])
        self.available_blocks = data['avaliable_blocks']
        self.solution_found = False

    def run_laser(self, laser):
        '''
        Traces the path of a laser, recording positions it intersects.
        '''
        laser_path = set()
        additional_lasers = []

        while laser.vx != 0 or laser.vy != 0:
            x, y = laser.move()
            if not self.grid.is_within_bounds(x, y):
                break

            block = self.grid.get_block(x, y)
            laser_path.add((x, y))

            if block.can_interact_with_laser():
                if block.block_type == 'reflect':
                    # Reflect based on the direction of the laser
                    if laser.vx != 0:
                        laser.reflect_x()
                    if laser.vy != 0:
                        laser.reflect_y()
                    print(f"Laser reflected at ({x}, {y})")
                elif block.block_type == 'opaque':
                    laser.absorb()
                    print(f"Laser absorbed at ({x}, {y})")
                    break
                elif block.block_type == 'refract':
                    # Add two new lasers for refracted paths
                    additional_lasers.append(laser.refract_x())
                    additional_lasers.append(laser.refract_y())
                    print(f"Laser refracted at ({x}, {y})")

        # Process any additional refracted lasers
        for new_laser in additional_lasers:
            laser_path.update(self.run_laser(new_laser))

        return laser_path

    def validate_solution(self):
        '''
        Checks whether all the target points are intersected by lasers.
        '''
        hit_points = set()
        # Reset lasers to their initial state for each validation
        lasers = [Laser(l.x, l.y, l.vx, l.vy) for l in self.initial_lasers]

        for laser in lasers:
            hit_points.update(self.run_laser(laser))

        print(f"Hit Points: {hit_points}")  # Debug output
        print(f"Required Points: {self.points}")  # Debug output
        return self.points.issubset(hit_points)

    def attempt_block_placements(self):
        '''
        Recursively places blocks on the grid to find a configuration that hits all target points.
        Uses a set to track visited configurations to avoid repeated attempts.
        '''
        empty_positions = self.grid.find_empty_positions()
        block_types = {bt: count for bt, count in self.available_blocks.items() if count > 0}
        visited = set()  # Track visited configurations based on placements

        def place_blocks(index, current_placement):
            '''
            Recursively tries each block in each position to find a solution.

            Args:
                index (int): The index of the empty position being tried.
                current_placement (tuple): Current sequence of block placements.

            Returns:
                bool: True if a solution is found; False otherwise.
            '''
            # Base case: If all positions are filled or a solution is found
            if index == len(empty_positions):
                # Convert current placement to a hashable form and check if visited
                placement_key = tuple(sorted(current_placement))
                if placement_key in visited:
                    return False
                visited.add(placement_key)  # Mark this placement as visited

                # Validate the solution
                if self.validate_solution():
                    self.solution_found = True
                    self.output_solution()
                    return True

                return False

            # Recursive case: Try each block type at the current position
            x, y = empty_positions[index]

            for block_type in list(block_types.keys()):
                if block_types[block_type] > 0:
                    # Place the block, decrement its count, and add it to the current configuration
                    self.grid.place_block(x, y, block_type)
                    block_types[block_type] -= 1  # Decrement the count of available blocks
                    print(f"Placing {block_type} block at ({x}, {y})")  # Debug output

                    # Include the new placement in the current sequence
                    new_placement = current_placement + ((x, y, block_type),)

                    # Recurse to place the next block
                    if place_blocks(index + 1, new_placement):
                        return True  # Stop further recursion if a solution is found

                    # Backtrack by removing the block and restoring the count
                    self.grid.set_block(x, y, Block('empty'))
                    block_types[block_type] += 1  # Restore the count of the block type
                    print(f"Removing {block_type} block from ({x}, {y})")  # Debug output

            return False

        # Start the recursive placement from the first empty position with an empty configuration
        if not place_blocks(0, ()):
            print("No solution found.")

def main():
    game = LazorGame('numbered_6.bff')
    game.attempt_block_placements()
    if not game.solution_found:
        print("No solution found.")


if __name__ == '__main__':
    main()
