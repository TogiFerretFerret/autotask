import pytest
from unittest.mock import MagicMock, patch
from aguiwayland.virtinput import VirtInput

@pytest.fixture
def virtinput():
    with patch('aguiwayland.virtinput.libvirtinput') as mock_libvirtinput:
        mock_libvirtinput.VirtInput = MagicMock()
        yield VirtInput()

def test_type(virtinput):
    virtinput.type("Hello World")
    virtinput.virtinput.type.assert_called_once_with("Hello World")

def test_press(virtinput):
    virtinput.press(42)
    virtinput.virtinput.press.assert_called_once_with(42)

def test_moveRel(virtinput):
    virtinput.moveRel(10, 20)
    virtinput.virtinput.moveRel.assert_called_once_with(10, 20)

def test_moveAbs(virtinput):
    virtinput.moveAbs(100, 200)
    virtinput.virtinput.moveAbs.assert_called_once_with(100, 200)

def test_scroll(virtinput):
    virtinput.scroll(5)
    virtinput.virtinput.scroll.assert_called_once_with(5)

def test_click(virtinput):
    virtinput.click(1)
    virtinput.virtinput.click.assert_called_once_with(1)

def test_startMouseTracking(virtinput):
    virtinput.startMouseTracking()
    virtinput.virtinput.startMouseTracking.assert_called_once()

def test_stopMouseTracking(virtinput):
    virtinput.stopMouseTracking()
    virtinput.virtinput.stopMouseTracking.assert_called_once()

def test_getMousePos(virtinput):
    virtinput.virtinput.getMousePos.return_value = (50, 50)
    assert virtinput.getMousePos() == (50, 50)
    virtinput.virtinput.getMousePos.assert_called_once()
