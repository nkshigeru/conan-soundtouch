#include <stdio.h>
#ifdef SOUNDTOUCHDLL
#include "SoundTouchDLL.h"
#else

#include "soundtouch/SoundTouch.h"

static inline const char *soundtouch_getVersionString()
{
	return soundtouch::SoundTouch::getVersionString();
}

#endif

int main() {
    printf("SoundTouch %s\n", soundtouch_getVersionString());
    return 0;
}
