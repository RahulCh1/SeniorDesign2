import pygame


file = "Batman.wav"
my_name = 'Derrian'
print(file)
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
	continue
