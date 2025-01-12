from BamUI import *
import pygame

def main():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    window = Window(100, 100, 800, 600, "My First Window")
    toggle1 = ToggleWidget(10, 250, 100, 30, "My First Toggle")

    window.children.append(toggle1)

    running = True
    while running:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if toggle1.is_hovered(event.pos[0], event.pos[1], window.x, window.y):
                    toggle1.toggle()
            elif event.type == pygame.VIDEORESIZE:
                screen = handle_videoresize(event, screen)
            window.handle_event(event)

        screen.fill(GREEN)
        window.draw(screen)

        pygame.display.flip()
        clock.tick(90)

    pygame.quit()
    sys.exit()  

if __name__ == "__main__":
    main()
