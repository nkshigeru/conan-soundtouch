#include <stdio.h>
#include "SoundTouchDLL.h"

int main() {
    printf("SoundTouch %s\n", soundtouch_getVersionString());
    return 0;
}
