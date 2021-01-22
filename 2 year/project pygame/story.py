from moviepy.editor import *
import os
import subprocess
import pygame


class Story:
    def video(self):  # загрузка видео
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        clip = VideoFileClip('images/shrek_story.avi')
        clip.preview()

    def load_image(self, name):  # загрузка изображений
        fullname = os.path.join('images', name)
        image = pygame.image.load(fullname)
        return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('shrek swamp')  # вставка названия окна
    pygame.display.set_icon(Story().load_image("icon.png"))  # вставка иконки
    running = True
    while running:
        Story().video()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.quit()
        subprocess.call('python start.py')  # вызов следующего окна
        running = False
    pygame.quit()
