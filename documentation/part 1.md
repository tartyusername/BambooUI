# BambooUI Documentation.
Hello! Welcome to BambooUI documentation, in this part i will tell you how to create a window with one toggle. 

# Setup🚀
1. Download BamUI.py
2. Create a file named "main.py"
3. at the start type "from BamUI import *"
4. then "import pygame"
# Coding💻
At the start add:
```
from BamUI import *
import pygame

def main():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
```
then:
```
window = Window(100, 100, 800, 600, "My First Window")
toggle1 = ToggleWidget(10, 250, 100, 30, "My First Toggle")
```
Now we need a while running loop:
```
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
```
Final touches are:
```
        screen.fill(GREEN)
        window.draw(screen)

        pygame.display.flip()
        clock.tick(90)

    pygame.quit()
    sys.exit()  

if __name__ == "__main__":
    main()
```
# Final
You successfully created a window with a toggle!
This example will be in examples folder
