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

class Board:
    def __init__(self, grid, lasers, targets):
        self.grid = grid
        self.lasers = lasers
        self.targets = targets # List of target points
    
    def place_block(self, block, x, y):
        if not self.grid[y][x].fixed:
            self.grid[y][x] = block

    def remove_block(self, x, y):
        if not self.grid[y][x].fixed:
            self.grid[y][x] = Block('empty')

    def is_within_bounds(self, x, y):
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

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
                        row.append(Block('none', fixed=True))  # No block allowed
                    elif char == 'o':
                        row.append(Block('empty'))  # Block allowed
                    elif char == 'A':
                        row.append(Block('reflect', fixed=True))  # Fixed reflect block
                    elif char == 'B':
                        row.append(Block('opaque', fixed=True))  # Fixed opaque block
                    elif char == 'C':
                        row.append(Block('refract', fixed=True))  # Fixed refract block
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

    return data
