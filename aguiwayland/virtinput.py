import libvirtinput
class VirtInput:
    def __init__(self):
        self.virtinput = libvirtinput.VirtInput()
    def type(self, text):
        self.virtinput.type(text)
    def press(self, key):
        self.virtinput.press(key)
    def moveRel(self, x, y):
        self.virtinput.move(x, y)
    def scroll(self, s):
        self.virtinput.scroll(s)
    def getMousePos(self):
        sessionType=os.environ.get('XDG_SESSION_TYPE')
        if sessionType=="wayland":
            
        else if sessionType=="x11":
            