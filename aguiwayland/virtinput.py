import libvirtinput

class VirtInput:
    def __init__(self):
        self.virtinput = libvirtinput.VirtInput()

    def type(self, text):
        """
        Simulate typing a string.
        
        Args:
            text (str): The text to type.
        """
        self.virtinput.type(text)

    def press(self, key):
        """
        Simulate pressing a key.
        
        Args:
            key (int): The key code to press.
        """
        self.virtinput.press(key)

    def moveRel(self, x, y):
        """
        Simulate relative mouse movement.
        
        Args:
            x (int): The relative x-coordinate to move.
            y (int): The relative y-coordinate to move.
        """
        self.virtinput.moveRel(x, y)

    def moveAbs(self, x, y):
        """
        Simulate absolute mouse movement.
        
        Args:
            x (int): The absolute x-coordinate to move.
            y (int): The absolute y-coordinate to move.
        """
        self.virtinput.moveAbs(x, y)

    def scroll(self, s):
        """
        Simulate mouse scroll.
        
        Args:
            s (int): The scroll amount.
        """
        self.virtinput.scroll(s)

    def click(self, button):
        """
        Simulate mouse click.
        
        Args:
            button (int): The mouse button to click.
        """
        self.virtinput.click(button)

    def startMouseTracking(self):
        """
        Start tracking mouse position.
        """
        self.virtinput.startMouseTracking()

    def stopMouseTracking(self):
        """
        Stop tracking mouse position.
        """
        self.virtinput.stopMouseTracking()

    def getMousePos(self):
        """
        Get the current mouse position.
        
        Returns:
            tuple: The current mouse position (x, y).
        """
        return self.virtinput.getMousePos()
