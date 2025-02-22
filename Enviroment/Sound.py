from Enviroment.TextureID import *
from Settings import *

class Sound:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(MAX_SOUND_CHANNELS)
        self.Channel = 0
        self.Path = 'Resources/Assets/Sounds/'
        
        self.PlayerAttack = {
            ID.KNIFE_0: self.Load('w_knife.ogg', Volume=0.2),
            ID.PISTOL_0: self.Load('w_pistol.wav', Volume=0.2),
            ID.RIFLE_0: self.Load('w_rifle.ogg', Volume=0.2)
        }
        
        self.PlayerHurt = self.Load('p_hurt.ogg')
        self.PlayerDeath = self.Load('p_death.ogg')
        self.PlayerMissed = self.Load('p_missed.wav')
        self.OpenDoor = self.Load('p_open_door.wav', Volume=1.0)
        
        self.PickUp = {
            ID.AMMO: self.Load('p_ammo.ogg'),
            ID.MED_KIT: self.Load('p_med_kit.mp3'),
            ID.KEY: self.Load('p_key.wav'),
        }
        self.PickUp[ID.PISTOL_ICON] = self.PickUp[ID.AMMO]
        self.PickUp[ID.RIFLE_ICON] = self.PickUp[ID.AMMO]
        
        self.EnemyAttack = {
            ID.SOLDIER_BLUE_0: self.Load('n_soldier_attack.mp3', Volume=0.8),
            ID.SOLDIER_BROWN_0: self.Load('n_soldier_attack.mp3', Volume=0.8),
            ID.RAT_0: self.Load('n_rat_attack.ogg', Volume=0.2),
        }
        
        self.Spotted = {
            ID.SOLDIER_BLUE_0: self.Load('n_soldier_spotted.ogg', Volume=1.0),
            ID.SOLDIER_BROWN_0: self.Load('n_brown_spotted.ogg', Volume=0.8),
            ID.RAT_0: self.Load('n_rat_spotted.ogg', Volume=0.5),
        }
        
        self.Death = {
            ID.SOLDIER_BLUE_0: self.Load('n_blue_death.ogg', Volume=0.8),
            ID.SOLDIER_BROWN_0: self.Load('n_brown_death.ogg', Volume=0.8),
            ID.RAT_0: self.Load('no_sound.mp3', Volume=0.0),
        }

        pygame.mixer.music.load(self.Path+'w_spaceambience.ogg')
        pygame.mixer.music.set_volume(0.2)
        

    def Load(self,File,Volume=0.5):
        Sound = pygame.mixer.Sound(self.Path+File)
        Sound.set_volume(Volume)
        return Sound

    def Play(self,Sound):
        pygame.mixer.Channel(self.Channel).play(Sound)
        self.Channel += 1
        if self.Channel == MAX_SOUND_CHANNELS:
            self.Channel = 0
