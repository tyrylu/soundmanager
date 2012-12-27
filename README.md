soundmanager
============
An abstraction on top of pyfmodex providing simple audio playback capability.

System requirements
-------------------
To use soundmanager, you must have pyfmodex installed and working. For details, see tyrylu/pyfmodex.

Usage example
-------------
Using soundmanager is very simple thing to do. For example, this is a way how to play a sound file.
```python
import soundmanager
sndmgr = soundmanager.SoundManager()
sndmgr.play("file_without_extension")
```

Now some notes to the above example. First, the file must be located in a directory which is known to soundmanager. The default is directory with name sounds. Of course, you can change that. And another thing, it must have a recognized file extension (mp3 and wav are examples of the default set). Yes, another configurable thing. You can also pass arguments to the fmod ex initialization.

soundmanager.sndmgr global
--------------------------
Upon calling the constructor a module global variable is initializet. It's useful when using soundmanager from different modules of your application, so you can do something like this:
```python
from soundmanager import sndmgr
```
I am not sure if this is the best way of achieving the goal, but it's the current implementation.