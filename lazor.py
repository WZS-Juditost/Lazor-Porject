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