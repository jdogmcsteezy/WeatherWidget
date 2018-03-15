from WeatherWidget import WeatherWidget
import pygame
import os
def main():
    pygame.init()
    clock = pygame.time.Clock()
    testScreen = pygame.display.set_mode((500,500))
    testScreen.fill((200, 255, 230))
    weather = WeatherWidget(500,500)
    testScreen.blit(weather,(0,0))
    pygame.display.update()
    run = True
    while(run):
        clock.tick(26)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    run = False
            elif event.type == pygame.QUIT:
                run = False

    pygame.quit()
    os.abort()

if __name__ == "__main__":
    main()
