class Block:
    def __init__(self, block_type, fixed=False):
        self.block_type = block_type  # 'reflect', 'opaque', 'refract', 'empty'
        self.fixed = fixed

class Laser:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

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

    def withIn_bounds(self, x, y):
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

def parse_file(file_path):
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

    return Board(grid, lasers, points), avaliable_blocks