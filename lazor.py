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