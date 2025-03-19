import os

if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
    import libvirtinput
else:
    libvirtinput = None

class VirtInput:
    def __init__(self):
        if libvirtinput:
            self.virtinput = libvirtinput.VirtInput()
        else:
            self.virtinput = None

    def type(self, text):
        """
        Simulate typing a string.
        
        Args:
            text (str): The text to type.
        """
        if self.virtinput:
            self.virtinput.type(text)

    def press(self, key):
        """
        Simulate pressing a key.
        
        Args:
            key (int): The key code to press.
        """
        if self.virtinput:
            self.virtinput.press(key)

    def moveRel(self, x, y):
        """
        Simulate relative mouse movement.
        
        Args:
            x (int): The relative x-coordinate to move.
            y (int): The relative y-coordinate to move.
        """
        if self.virtinput:
            self.virtinput.moveRel(x, y)

    def moveAbs(self, x, y):
        """
        Simulate absolute mouse movement.
        
        Args:
            x (int): The absolute x-coordinate to move.
            y (int): The absolute y-coordinate to move.
        """
        if self.virtinput:
            self.virtinput.moveAbs(x, y)

    def scroll(self, s):
        """
        Simulate mouse scroll.
        
        Args:
            s (int): The scroll amount.
        """
        if self.virtinput:
            self.virtinput.scroll(s)

    def click(self, button):
        """
        Simulate mouse click.
        
        Args:
            button (int): The mouse button to click.
        """
        if self.virtinput:
            self.virtinput.click(button)

    def startMouseTracking(self):
        """
        Start tracking mouse position.
        """
        if self.virtinput:
            self.virtinput.startMouseTracking()

    def stopMouseTracking(self):
        """
        Stop tracking mouse position.
        """
        if self.virtinput:
            self.virtinput.stopMouseTracking()

    def getMousePos(self):
        """
        Get the current mouse position.
        
        Returns:
            tuple: The current mouse position (x, y).
        """
        if self.virtinput:
            return self.virtinput.getMousePos()
        return (0, 0)
