import pygame


file = "MorrilD.wav"
#my_name = 'Derrian'
print(file)
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
	continue
print "Derrian"

pygame.mixer.music.load("Batman.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
	continue
print "Derrian"
