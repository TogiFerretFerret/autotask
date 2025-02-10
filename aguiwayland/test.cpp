#include "virtkeyb.cpp"
#include <stdlib.h>
#include <stdio.h>
int main(int argc, char **argv)
{
    uinput virtkbd_dev = virt_create();
    virt_type("hello", virtkbd_dev);
    virt_mouse_moveabs(500, 50, virtkbd_dev);
    virt_mouse_click(LEFT, virtkbd_dev);
    virt_mouse_scroll(1, virtkbd_dev);
    sleep(10);
    virt_destroy(virtkbd_dev);
    return 0;
}