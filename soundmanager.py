import pyfmodex as pf
import os
non_3d_args = pf.constants.FMOD_SOFTWARE|pf.constants.FMOD_2D
sndmgr = None
class SoundManager(object):
    def __init__(self, sounds_dir="sounds", sound_extensions=["wav", "mp3", "ogg"], recursive_search=True, **system_init_args):
        global sndmgr
        self._sounds = {}
        self._sound_files = {}
        self._exts = sound_extensions
        self.fmodex_system = pf.System()
        self.fmodex_system.init(**system_init_args)
        self._recursive = recursive_search
        self._index_dir(sounds_dir)
        sndmgr = self

    def _index_dir(self, path):
        for name in os.listdir(path):
            full_subdir_path = os.path.join(path, name)
            if os.path.isdir(full_subdir_path) and self._recursive: self._index_dir(full_subdir_path)
            name_split = os.path.splitext(full_subdir_path)
            if not len(name_split) == 2: continue
            if name_split[1][1:] in self._exts:
                name =             os.path.basename(name_split[0])
                if len(name.split(".")) == 2: name = name.split(".")[0]
                self._sound_files[name] = full_subdir_path

    def get(self, name, **sound_create_args):
        fname = self._sound_files[name]
        name_splt = fname.split(".")
        if len(name_splt) == 2:
            if "mode" in sound_create_args: sound_create_args["mode"] |= non_3d_args
            else: sound_create_args["mode"] = non_3d_args
            return self._get(name, **sound_create_args)[0]
        else:
            snd, from_cache = self._get(name, **sound_create_args)
            if from_cache: return snd
            snd.min_distance = int(name_splt[1][2:])
            return snd

    def _get(self, name, **sound_create_args):
        if name in self._sounds: return [self._sounds[name], True]
        snd = self.fmodex_system.create_sound(self._sound_files[name], **sound_create_args)
        self._sounds[name] = snd
        return [snd, False]


    def get_channel(self, name, set_loop=False, x=None, y=None, z=None):
        ch = self.get(name).play(paused=True)
        if set_loop: ch.mode = 2
        if x is not None:
            ch.position = [x, y, z]
        return ch

    def play(self, name, set_loop=False, x=None, y=None, z=None):
        ch = self.get_channel(name, set_loop, x, y, z)
        ch.paused = False
        self.fmodex_system.update() #Avoid out of channels error.
        return ch
