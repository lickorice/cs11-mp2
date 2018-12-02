class Button():
    """
    This class is used in the interface to implement on-click and on-hover listeners.

    Attributes:
        hovering (bool): Automatically assigned by the interface in order to determine
            if mouse is currently hovering the button.
        x_range (tuple): A tuple of two `int`s, (a, b) where `a <= b`, in order to check
            if the mouse is currently in-between those two values in the x-axis.
        x_range (tuple): A tuple of two `int`s, (a, b) where `a <= b`, in order to check
            if the mouse is currently in-between those two values in the y-axis.
    """
    def __init__(self):
        self.hovering = False
        self.x_range = (0, 0)
        self.y_range = (0, 0)