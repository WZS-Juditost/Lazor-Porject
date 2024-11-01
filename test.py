import unittest
from lazor import*

class TestBlock(unittest.TestCase):
    def test_block_initialization(self):
        block = Block('reflect', fixed=True)
        self.assertEqual(block.block_type, 'reflect')
        self.assertTrue(block.fixed)
        print("TestBlock.test_block_initialization passed")

    def test_is_empty(self):
        empty_block = Block('empty', fixed=False)
        fixed_block = Block('reflect', fixed=True)
        self.assertTrue(empty_block.is_empty())
        self.assertFalse(fixed_block.is_empty())
        print("TestBlock.test_is_empty passed")

    def test_can_interact_with_laser(self):
        reflect_block = Block('reflect')
        opaque_block = Block('opaque')
        refract_block = Block('refract')
        empty_block = Block('empty')
        self.assertTrue(reflect_block.can_interact_with_laser())
        self.assertTrue(opaque_block.can_interact_with_laser())
        self.assertTrue(refract_block.can_interact_with_laser())
        self.assertFalse(empty_block.can_interact_with_laser())
        print("TestBlock.test_can_interact_with_laser passed")


class TestLaser(unittest.TestCase):
    def test_laser_initialization(self):
        laser = Laser(1, 1, 1, 0)
        self.assertEqual(laser.x, 1)
        self.assertEqual(laser.y, 1)
        self.assertEqual(laser.vx, 1)
        self.assertEqual(laser.vy, 0)
        print("TestLaser.test_laser_initialization passed")

    def test_move(self):
        laser = Laser(1, 1, 1, 1)
        laser.move()
        self.assertEqual((laser.x, laser.y), (2, 2))
        print("TestLaser.test_move passed")

    def test_reflect_x(self):
        laser = Laser(1, 1, 1, 1)
        laser.reflect_x()
        self.assertEqual(laser.vx, -1)
        print("TestLaser.test_reflect_x passed")

    def test_reflect_y(self):
        laser = Laser(1, 1, 1, 1)
        laser.reflect_y()
        self.assertEqual(laser.vy, -1)
        print("TestLaser.test_reflect_y passed")

    def test_refract_x(self):
        laser = Laser(1, 1, 1, 1)
        refracted_laser = laser.refract_x()
        self.assertEqual(refracted_laser.vx, -1)
        self.assertEqual(refracted_laser.vy, 1)
        print("TestLaser.test_refract_x passed")

    def test_refract_y(self):
        laser = Laser(1, 1, 1, 1)
        refracted_laser = laser.refract_y()
        self.assertEqual(refracted_laser.vx, 1)
        self.assertEqual(refracted_laser.vy, -1)
        print("TestLaser.test_refract_y passed")

    def test_absorb(self):
        laser = Laser(1, 1, 1, 1)
        laser.absorb()
        self.assertEqual((laser.vx, laser.vy), (0, 0))
        print("TestLaser.test_absorb passed")

    def test_current_position(self):
        laser = Laser(1, 1, 1, 1)
        self.assertEqual(laser.current_position(), (1, 1))
        print("TestLaser.test_current_position passed")

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [Block('none', fixed=True), Block('empty'), Block('reflect', fixed=True)],
            [Block('opaque', fixed=True), Block('empty'), Block('refract', fixed=True)],
        ]
        self.grid_obj = Grid(self.grid)

    def test_get_block(self):
        block = self.grid_obj.get_block(1, 0)
        self.assertEqual(block.block_type, 'empty')
        print("TestGrid.test_get_block passed")

    def test_set_block(self):
        new_block = Block('opaque')
        self.grid_obj.set_block(1, 1, new_block)
        self.assertEqual(self.grid_obj.get_block(1, 1).block_type, 'opaque')
        print("TestGrid.test_set_block passed")

    def test_is_within_bounds(self):
        self.assertTrue(self.grid_obj.is_within_bounds(0, 1))
        self.assertFalse(self.grid_obj.is_within_bounds(3, 1))
        print("TestGrid.test_is_within_bounds passed")

    def test_find_empty_positions(self):
        empty_positions = self.grid_obj.find_empty_positions()
        self.assertIn((1, 0), empty_positions)
        self.assertIn((1, 1), empty_positions)
        self.assertEqual(len(empty_positions), 2)
        print("TestGrid.test_find_empty_positions passed")

    def test_place_block_successful(self):
        result = self.grid_obj.place_block(1, 1, 'reflect')
        self.assertTrue(result)
        self.assertEqual(self.grid_obj.get_block(1, 1).block_type, 'reflect')
        print("TestGrid.test_place_block_successful passed")

    def test_place_block_failed_on_fixed_block(self):
        result = self.grid_obj.place_block(0, 0, 'opaque')
        self.assertFalse(result)
        self.assertEqual(self.grid_obj.get_block(0, 0).block_type, 'none')
        print("TestGrid.test_place_block_failed_on_fixed_block passed")

class TestGridComplex(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [Block('none', fixed=True), Block('empty'), Block('reflect', fixed=True), Block('empty')],
            [Block('opaque', fixed=True), Block('empty'), Block('empty'), Block('refract', fixed=True)],
            [Block('none', fixed=True), Block('empty'), Block('opaque', fixed=True), Block('empty')],
            [Block('empty'), Block('empty'), Block('reflect', fixed=True), Block('empty')]
        ]
        self.grid_obj = Grid(self.grid)

    def test_find_empty_positions_complex(self):
        expected_empty_positions = [(1, 0), (3, 0), (1, 1), (2, 1), (1, 2), (3, 2), (0, 3), (1, 3), (3, 3)]
        empty_positions = self.grid_obj.find_empty_positions()
        for pos in expected_empty_positions:
            self.assertIn(pos, empty_positions)
        self.assertEqual(len(empty_positions), len(expected_empty_positions))
        print("TestGridComplex.test_find_empty_positions_complex passed")

class TestReadBFFFile(unittest.TestCase):
    def test_read_bff_file_complex(self):
        file_content = """
        # Complex BFF file for testing
        GRID START
        x o o A o x
        B o o o o C
        x x o o x x
        x o o B o x
        A o o o o B
        GRID STOP
        A 2
        B 1
        C 3
        L 0 1 1 0
        L 5 2 -1 1
        L 2 4 1 -1
        P 3 3
        P 4 1
        P 1 4
        """
        with open("test_file_complex.bff", "w") as f:
            f.write(file_content.strip())

        data = read_bff_file("test_file_complex.bff")
        
        self.assertEqual(len(data['grid']), 5)
        self.assertEqual(len(data['grid'][0]), 6)
        self.assertEqual(data['grid'][0][3].block_type, 'reflect')
        self.assertEqual(data['grid'][1][0].block_type, 'opaque')
        self.assertEqual(data['grid'][1][5].block_type, 'refract')

        self.assertEqual(data['avaliable_blocks']['A'], 2)
        self.assertEqual(data['avaliable_blocks']['B'], 1)
        self.assertEqual(data['avaliable_blocks']['C'], 3)

        self.assertEqual(len(data['lasers']), 3)
        self.assertEqual(data['lasers'][0].current_position(), (0, 1))
        self.assertEqual(data['lasers'][1].vx, -1)
        self.assertEqual(data['lasers'][2].vy, -1)

        self.assertEqual(len(data['points']), 3)
        self.assertIn((3, 3), data['points'])
        self.assertIn((4, 1), data['points'])
        self.assertIn((1, 4), data['points'])
        
        print("TestReadBFFFile.test_read_bff_file_complex passed")


class TestGridEdgeCases(unittest.TestCase):
    def test_empty_grid(self):
        grid = [[Block('empty') for _ in range(5)] for _ in range(5)]
        grid_obj = Grid(grid)
        empty_positions = grid_obj.find_empty_positions()

        expected_empty_positions = [(x, y) for x in range(5) for y in range(5)]
        self.assertEqual(set(empty_positions), set(expected_empty_positions))
        print("TestGridEdgeCases.test_empty_grid passed")

    def test_full_grid(self):
        grid = [[Block('reflect', fixed=True) for _ in range(4)] for _ in range(4)]
        grid_obj = Grid(grid)
        empty_positions = grid_obj.find_empty_positions()
        self.assertEqual(empty_positions, [])
        print("TestGridEdgeCases.test_full_grid passed")


if __name__ == "__main__":
    unittest.main()

