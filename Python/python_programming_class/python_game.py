import pygame, sys




def main():
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)

    pygame.init()
    pygame.display.set_caption("Shapes")

    screen = pygame.display.set_mode((400, 300))
    background_color = (127,127,127)
    screen.fill(background_color)

    pygame.draw.circle(screen, red, (200,150), 60, 1)
    pygame.draw.circle(screen, green, (200,150), 80, 2)
    pygame.draw.circle(screen, blue, (200,150), 100, 3)
    pygame.draw.circle(screen, white, (200,150), 120, 4)

    pygame.display.update()
    pygame.image.save(screen, "circles.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                print(key, "Key is pressed")

            if event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                print(key, "Key is released")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                btn = pygame.mouse
                print("x = {}, y = {}".format(pos[0], pos[1]))

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                btn = pygame.mouse
                print("x = {}, y = {}".format(pos[0], pos[1]))


if __name__ == '__main__':
    main()