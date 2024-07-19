from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    """
    Complexity of class methods are O(1), unless otherwise specified
    """

    CAPACITY = 10000

    def __init__(self) -> None:
        """
        Description: Initialise stacks that store undo and redo actions
        """

        # Worst case time complexity: O(1), since CAPACITY is a fixed integer class variable,
        # so we know CAPACITY is not asymptotic
        self.tree = ArrayStack(UndoTracker.CAPACITY)
        self.branch = ArrayStack(UndoTracker.CAPACITY)

    def add_action(self, action: PaintAction) -> None:
        """
        Description: Adds an action to the undo tracker. When collection full, exit early

        Args:
        - action: list of paint steps
        """
        if self.tree.is_full():
            return  # exit early
        self.tree.push(action)
        self.branch.clear()  # new action clears redo branch

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Description: Undo an operation and apply action to grid. Do nothing if no actions

        Args:
        - grid: grid to apply action to

        Returns: The action that was undone, or None.

        Time complexity:
        Best case: O(1), when the stack is empty, then undo_apply is not called
        Worst case: O(undo_apply), the rest is O(1)
        """
        if self.tree.is_empty():
            return None
        else:
            undo_action = self.tree.pop()
            self.branch.push(undo_action)

            # O(undo_apply)
            undo_action.undo_apply(grid)
            return undo_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Description: Redo an operation that was previously undone. Do nothing if no actions

        Args:
        - grid: grid to apply action to

        Returns: The action that was redone, or None.

        Time complexity:
        Best case: O(1), when the stack is empty, then redo_apply is not called
        Worst case: O(redo_apply), the rest is O(1)
        """
        if self.branch.is_empty():
            return None
        else:
            redo_action = self.branch.pop()
            self.tree.push(redo_action)

            # O(redo_apply)
            redo_action.redo_apply(grid)
            return redo_action

