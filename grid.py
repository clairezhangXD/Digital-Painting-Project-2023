from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import *

class Grid:
    """
    Complexity of class methods are O(1), unless otherwise specified
    """

    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style: str, x: int, y: int) -> None:
        """
        Description: Initialise the grid object.

        Args:
        - draw_style: Style with which colours will be drawn
        - x: x dimension of the grid
        - y: y dimension of the grid

        Time complexity:
        Best = Worst case:
            Ignoring O(1) assignments
            O(x)+O(x)*(O(y)+O(y)*(O(comp)+O(comp)+O(comp))
           =O(x)+O(x*y)+O(x*(y*3*comp))
            Ignore constant co-efficients and non-dominating terms
           =O(x*y*comp). Best = worst case because the run time of the method depends purely on the input sizes
            of x and y, which are not known, not on any specific favourable/unfavourable values of input

        """
        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

        # setting up 1 dimensional grid
        # O(x), since time complexity of an ArrayR(CAPACITY) is O(CAPACITY)
        self.grid = ArrayR(x)

        # setting up 2 dimensional grid
        # O(x), since len(grid) is same as capacity of the array, which is x.
        # Number of iterations depends on this input size, thus effects run time
        for i in range(len(self.grid)):

            # O(y), since time complexity of an ArrayR(CAPACITY) is O(CAPACITY)
            array_y = ArrayR(y)

            # each cell in array y stores a layer
            # O(y), since number of iterations depends on this input size, thus effects run time
            for j in range(len(array_y)):

                # O(comp)
                if self.draw_style == Grid.DRAW_STYLE_SET:
                    array_y[j] = SetLayerStore()

                # O(comp)
                elif self.draw_style == Grid.DRAW_STYLE_ADD:
                    array_y[j] = AdditiveLayerStore()

                # O(comp)
                elif self.draw_style == Grid.DRAW_STYLE_SEQUENCE:
                    array_y[j] = SequenceLayerStore()

            # each cell in the array x stores an array y
            self.grid[i] = array_y


    def __getitem__(self, index: int):
        """
        Description: return grid index

        Args:
        - index: integer value pointing to the position of item in array

        Returns:
        - item in array
        """
        return self.grid[index]

    def increase_brush_size(self):
        """
        Description: Increases the size of the brush by 1
        """
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1



    def decrease_brush_size(self):
        """
        Description: Decreases the size of the brush by 1
        """
        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1


    def special(self):
        """
        Description: Activate the special affect on all grid squares.

        Time complexity:
        Best case: O(x*y), and draw style is set to Set Layer store. Special() would take constant time
        Worst case:
        O(x*y*delete_at_index) if draw style set to Sequence Layer store.
        O(x*y*len(store)) if draw style set to Additive Layer store.
        Therefore, overall worst case is O({x*y*delete_at_index,x*y*len(store)})
        """
        for x_cell in range(self.x):
            for y_cell in range(self.y):
                self.grid[x_cell][y_cell].special()


