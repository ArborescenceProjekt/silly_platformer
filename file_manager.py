import sys, os, pygame, random

pygame.mixer.init()

def ressource_path(relative_path):
        try:
            base_path = sys.MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class Sound_Manager:

    def __init__(self):
        self.sounds = {
            "sfx_collision": [
                pygame.mixer.Sound(ressource_path("SFX/sfx1.wav")),
                pygame.mixer.Sound(ressource_path("SFX/sfx3.wav"))
                ],
            "sfx_big_collision": pygame.mixer.Sound(ressource_path("SFX/sfx2.wav")),
            "sfx_jump": [pygame.mixer.Sound(ressource_path("SFX/sfx_jump.wav")),
                         pygame.mixer.Sound(ressource_path("SFX/sfx_jump2.wav"))]
            }
        self.sounds_raw = {
            "sfx_explosion": "Sounds/explosion.wav",
            "sfx_point": "Sounds/point.wav",
            "sfx_ball": [
                "Sounds/blipSelect.wav",
                "Sounds/blipSelect2.wav",
                "Sounds/blipSelect3.wav"
                ]
            }

    def play(self, name):
        sfx = self.sounds.get(name)
        if isinstance(sfx, list):
            random.choice(sfx).play()
        else:
            sfx.play()

    '''def volume_global(self, volume):
        for sound in self.sounds.values():
            if isinstance(sound, list):
                for s in sound:
                    s.set_volume(volume)
            else:
                sound.set_volume(volume)'''
