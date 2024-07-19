from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue


class ReplayTracker:
    """
    Complexity of class methods are O(1), unless otherwise specified
    """

    CAPACITY = 100000

    def __init__(self) -> None:
        """
        Description: Initialise queue that store replay actions
        """

        # Worst case time complexity: O(1), since CAPACITY is a fixed integer class variable,
        # so we know CAPACITY is not asymptotic
        self.replay_queue = CircularQueue(ReplayTracker.CAPACITY)

        self.replay_on = False

    def start_replay(self) -> None:
        """
        Description: Called whenever we should stop taking actions, and start playing them back.
        """
        self.replay_on = True

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Description: Adds an action to the replay.

        Args:
        - action: list of paint steps
        - is_undo: specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        """
        if not self.replay_on:
            self.replay_queue.append((action, is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Description: Plays the next replay action on the grid.

        Args:
        - grid: grid to apply action to

        Returns:
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Time complexity:
        Best case: O(1), when the queue is empty, then undo_apply or redo_apply do not get called
        Worst case: O(Max{undo_apply,redo_apply}), not sure which has longer run time, so the greater run time of the
        two is the overall worst case time complexity of this method
        """
        if self.replay_queue.is_empty():
            self.replay_on = False
            return True
        else:
            action, is_undo = self.replay_queue.serve()
            if is_undo:

                # O(undo_apply)
                action.undo_apply(grid)
            else:

                # O(redo_apply)
                action.redo_apply(grid)
            return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

