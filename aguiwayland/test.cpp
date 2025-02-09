#include "virtkeyb.cpp"
#include <stdlib.h>
#include <stdio.h>
int main(int argc, char **argv)
{
    uinput virtkbd_dev = virt_create();
    virt_type("hello", virtkbd_dev);
    virt_mouse_move(-10000, -10000, virtkbd_dev);
    virt_mouse_click(LEFT, virtkbd_dev);
    virt_mouse_scroll(1, virtkbd_dev);
    virt_destroy(virtkbd_dev);
    return 0;
}