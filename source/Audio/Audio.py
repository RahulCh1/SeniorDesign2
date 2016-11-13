import pygame

class Audio(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Setup pygame mixer
        '''
        pygame.mixer.init()
        self.audio = pygame.mixer.music

    def loadAudioFile(self, fileName):
        self.audio.load(fileName)

    def playAudioFile(self, fileName):
        self.loadAudioFile(fileName)

        self.audio.play()
        while self.audio.get_busy() == True:
            continue
