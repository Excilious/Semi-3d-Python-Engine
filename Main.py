from Settings import *
from Enviroment.Engine import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, MAJOR_VERSION)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, MINOR_VERSION)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, DEPTH_SIZE)

        pygame.display.set_mode(RESOLUTION, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        self.Context = moderngl.create_context()

        self.Context.enable(flags=moderngl.DEPTH_TEST | moderngl.BLEND)
        self.Context.gc_mode = 'auto'

        self.Clock = pygame.time.Clock()
        self.DeltaTime = 0
        self.Time = 0

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.IsRunning = True
        self.FramesPerSecond = 0

        self.Engine = Engine(self)

        self.AnimationTrigger = False
        self.AnimationEvent = pygame.USEREVENT + 0
        pygame.time.set_timer(self.AnimationEvent, SYNC)

        self.SoundTrigger = False
        self.SoundEvent = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SoundEvent, 750)

    def Update(self):
        self.Engine.Update()
        self.DeltaTime = self.Clock.tick(MAXFPS)
        self.Time = pygame.time.get_ticks() * 0.001
        self.FramesPerSecond = int(self.Clock.get_fps())
        pygame.display.set_caption(f'{self.FramesPerSecond}')

    def Render(self):
        self.Context.clear(color=BACKGROUND)
        self.Engine.Render()
        pygame.display.flip()

    def Events(self):
        self.AnimationTrigger, self.SoundTrigger = False, False

        for Event in pygame.event.get():
            if (Event.type == pygame.QUIT or (Event.type == pygame.KEYDOWN and Event.key == pygame.K_ESCAPE)):
                self.IsRunning = False
            if (Event.type == self.AnimationEvent):
                self.AnimationTrigger = True
            if (Event.type == self.SoundEvent):
                self.SoundTrigger = True
    
            self.Engine.Events(Event=Event)

    def Run(self):
        while self.IsRunning:
            self.Events()
            self.Update()
            self.Render()
        pygame.quit()
        sys.exit()


if (__name__ == '__main__'):
    Game = Game()
    Game.Run()
