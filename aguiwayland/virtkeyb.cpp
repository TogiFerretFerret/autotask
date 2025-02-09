#include <fcntl.h>
#include <linux/input.h>
#include <stdio.h>
#include <unistd.h>
#include <libevdev/libevdev-uinput.h>
#include <signal.h>
#include <stdlib.h>
#include <grp.h>
#include <iostream>
#include <string>
#include <unistd.h>
#include <fcntl.h>

typedef struct libevdev_uinput *uinput;

typedef struct
{
    int evdev;
    char ascii;
    int shift;
} keyMapEntry;

typedef enum
{
    LEFT = 0,
    RIGHT = 2,
    MIDDLE = 1
} MouseButton;
keyMapEntry keyMap[] = {
    {KEY_A, 'a', 0},
    {KEY_B, 'b', 0},
    {KEY_C, 'c', 0},
    {KEY_D, 'd', 0},
    {KEY_E, 'e', 0},
    {KEY_F, 'f', 0},
    {KEY_G, 'g', 0},
    {KEY_H, 'h', 0},
    {KEY_I, 'i', 0},
    {KEY_J, 'j', 0},
    {KEY_K, 'k', 0},
    {KEY_L, 'l', 0},
    {KEY_M, 'm', 0},
    {KEY_N, 'n', 0},
    {KEY_O, 'o', 0},
    {KEY_P, 'p', 0},
    {KEY_Q, 'q', 0},
    {KEY_R, 'r', 0},
    {KEY_S, 's', 0},
    {KEY_T, 't', 0},
    {KEY_U, 'u', 0},
    {KEY_V, 'v', 0},
    {KEY_W, 'w', 0},
    {KEY_X, 'x', 0},
    {KEY_Y, 'y', 0},
    {KEY_Z, 'z', 0},
    {KEY_A, 'A', 1},
    {KEY_B, 'B', 1},
    {KEY_C, 'C', 1},
    {KEY_D, 'D', 1},
    {KEY_E, 'E', 1},
    {KEY_F, 'F', 1},
    {KEY_G, 'G', 1},
    {KEY_H, 'H', 1},
    {KEY_I, 'I', 1},
    {KEY_J, 'J', 1},
    {KEY_K, 'K', 1},
    {KEY_L, 'L', 1},
    {KEY_M, 'M', 1},
    {KEY_N, 'N', 1},
    {KEY_O, 'O', 1},
    {KEY_P, 'P', 1},
    {KEY_Q, 'Q', 1},
    {KEY_R, 'R', 1},
    {KEY_S, 'S', 1},
    {KEY_T, 'T', 1},
    {KEY_U, 'U', 1},
    {KEY_V, 'V', 1},
    {KEY_W, 'W', 1},
    {KEY_X, 'X', 1},
    {KEY_Y, 'Y', 1},
    {KEY_Z, 'Z', 1},
    {KEY_1, '1', 0},
    {KEY_2, '2', 0},
    {KEY_3, '3', 0},
    {KEY_4, '4', 0},
    {KEY_5, '5', 0},
    {KEY_6, '6', 0},
    {KEY_7, '7', 0},
    {KEY_8, '8', 0},
    {KEY_9, '9', 0},
    {KEY_0, '0', 0},
    {KEY_SPACE, ' ', 0},
    {KEY_MINUS, '-', 0},
    {KEY_EQUAL, '=', 0},
    {KEY_COMMA, ',', 0},
    {KEY_DOT, '.', 0},
    {KEY_SLASH, '/', 0},
    {KEY_SEMICOLON, ';', 0},
    {KEY_APOSTROPHE, '\'', 0},
    {KEY_GRAVE, '`', 0},
    {KEY_LEFTBRACE, '[', 0},
    {KEY_RIGHTBRACE, ']', 0},
    {KEY_BACKSLASH, '\\', 0},
    {KEY_1, '!', 1},
    {KEY_2, '@', 1},
    {KEY_3, '#', 1},
    {KEY_4, '$', 1},
    {KEY_5, '%', 1},
    {KEY_6, '^', 1},
    {KEY_7, '&', 1},
    {KEY_8, '*', 1},
    {KEY_9, '(', 1},
    {KEY_0, ')', 1},
    {KEY_MINUS, '_', 1},
    {KEY_EQUAL, '+', 1},
    {KEY_LEFTBRACE, '{', 1},
    {KEY_RIGHTBRACE, '}', 1},
    {KEY_SEMICOLON, ':', 1},
    {KEY_APOSTROPHE, '"', 1},
    {KEY_GRAVE, '~', 1},
    {KEY_BACKSLASH, '|', 1},
    {KEY_COMMA, '<', 1},
    {KEY_DOT, '>', 1},
    {KEY_SLASH, '?', 1}};
keyMapEntry convToEvdev(char c)
{
    for (int i = 0; i < (int)(sizeof(keyMap) / sizeof(keyMapEntry)); i++)
    {
        if (keyMap[i].ascii == c)
        {
            return keyMap[i];
        }
    }
    keyMapEntry invalidEntry = {-1, '\0', 0};
    return invalidEntry;
}
void virt_press(int code, uinput dev)
{
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
    libevdev_uinput_write_event(dev, EV_KEY, code, 1);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
    libevdev_uinput_write_event(dev, EV_KEY, code, 0);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
}
void virt_type(char *str, uinput dev)
{
    for (int i = 0; *(str + i) != 0; i++)
    {
        keyMapEntry c = convToEvdev((char)(*(str + i)));
        if (c.evdev == -1)
            continue;
        if (c.shift)
        {
            libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
            libevdev_uinput_write_event(dev, EV_KEY, KEY_LEFTSHIFT, 1);
            libevdev_uinput_write_event(dev, EV_KEY, c.evdev, 1);
            libevdev_uinput_write_event(dev, EV_KEY, c.evdev, 0);
            libevdev_uinput_write_event(dev, EV_KEY, KEY_LEFTSHIFT, 0);
            libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
        }
        else
        {
            virt_press(c.evdev, dev);
        }
    }
}
void virt_mouse_move(int x, int y, uinput dev)
{
    libevdev_uinput_write_event(dev, EV_KEY, BTN_TOOL_PEN, 0);
    libevdev_uinput_write_event(dev, EV_REL, REL_X, x);
    libevdev_uinput_write_event(dev, EV_REL, REL_Y, y);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
}
void virt_mouse_scroll(int s, uinput dev)
{
    libevdev_uinput_write_event(dev, EV_REL, REL_WHEEL, s);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
}
void virt_mouse_click(MouseButton m, uinput dev)
{
    int convButton;
    switch (m)
    {
    case LEFT:
        convButton = BTN_LEFT;
        break;
    case RIGHT:
        convButton = BTN_RIGHT;
        break;
    case MIDDLE:
        convButton = BTN_MIDDLE;
        break;
    default:
        convButton = BTN_LEFT;
        break;
    }
    libevdev_uinput_write_event(dev, EV_KEY, convButton, 1);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
    libevdev_uinput_write_event(dev, EV_KEY, convButton, 0);
    libevdev_uinput_write_event(dev, EV_SYN, SYN_REPORT, 0);
}
uinput virt_create()
{
    struct libevdev *dev;
    uinput virtkbd_dev;
    dev = libevdev_new();
    libevdev_set_name(dev, "Virtual Keyboard");
    libevdev_enable_property(dev, INPUT_PROP_DIRECT);

    libevdev_enable_event_type(dev, EV_REL);
    libevdev_enable_event_code(dev, EV_REL, REL_X, NULL);
    libevdev_enable_event_code(dev, EV_REL, REL_Y, NULL);
    libevdev_enable_event_code(dev, EV_REL, REL_WHEEL, NULL);
    libevdev_enable_event_type(dev, EV_ABS);
    libevdev_enable_event_code(dev, EV_ABS, ABS_X, NULL);
    libevdev_enable_event_code(dev, EV_ABS, ABS_Y, NULL);

    libevdev_enable_event_type(dev, EV_KEY);
    libevdev_enable_event_code(dev, EV_KEY, BTN_LEFT, NULL);
    libevdev_enable_event_code(dev, EV_KEY, BTN_RIGHT, NULL);
    libevdev_enable_event_code(dev, EV_KEY, BTN_MIDDLE, NULL);
    libevdev_enable_event_type(dev, EV_KEY);
    libevdev_enable_event_type(dev, EV_SYN);
    libevdev_enable_event_type(dev, EV_REP);
    libevdev_enable_event_type(dev, EV_REL);
    for (int i = 0; i < (int)(sizeof(keyMap) / sizeof(keyMapEntry)); i++)
    {
        libevdev_enable_event_code(dev, EV_KEY, keyMap[i].evdev, NULL);
    }
    libevdev_enable_event_code(dev, EV_KEY, KEY_LEFTSHIFT, NULL);
    libevdev_enable_event_code(dev, EV_KEY, KEY_RIGHTSHIFT, NULL);
    libevdev_enable_event_code(dev, EV_KEY, KEY_LEFTCTRL, NULL);
    libevdev_enable_event_code(dev, EV_KEY, KEY_RIGHTCTRL, NULL);
    libevdev_enable_event_code(dev, EV_KEY, KEY_LEFTALT, NULL);
    libevdev_enable_event_code(dev, EV_KEY, KEY_RIGHTALT, NULL);
    libevdev_enable_event_code(dev, EV_KEY, BTN_TOOL_PEN, NULL);
    libevdev_uinput_create_from_device(dev, LIBEVDEV_UINPUT_OPEN_MANAGED, &virtkbd_dev);
    libevdev_free(dev);
    sleep(1);
    return virtkbd_dev;
}
void virt_destroy(uinput kbd)
{
    libevdev_uinput_destroy(kbd);
}
class VirtInput
{
    uinput dev;
public:
    VirtInput()
    {
        /*auto grp = getgrnam("input");
        if (grp == nullptr)
        {
            std::cerr << "getgrnam(\"input\") failed" << std::endl;
        }
        if (setgid(grp->gr_gid) < 0)
        {
            std::cerr << "couldn't change group to input!" << std::endl;
        }*/
        dev = virt_create();
    };
    void click(int m)
    {
        virt_mouse_click((MouseButton)m, dev);
    };
    void move(int x, int y)
    {
        virt_mouse_move(x, y, dev);
    };
    void scroll(int s)
    {
        virt_mouse_scroll(s, dev);
    };
    void type(char *str)
    {
        virt_type(str, dev);
    };
    void press(int code)
    {
        virt_press(code, dev);
    };
    ~VirtInput()
    {
        virt_destroy(dev);
        
    };
};