import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SILVER = (192,192,192)
TEAL = (0,128,128)
ORANGE = (255, 172, 28)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
FONT = pygame.font.SysFont("Arial", 18)

class Window:
    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.children = []
        self.dragging = False
        self.resizing = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height), border_radius=10)
        text = FONT.render(self.title, True, BLACK)
        screen.blit(text, (self.x + 10, self.y + 10))
        for child in self.children:
            child.draw(screen, self.x, self.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.x <= event.pos[0] <= self.x + self.width and
                    self.y <= event.pos[1] <= self.y + 20):
                self.dragging = True
                self.offset_x = self.x - event.pos[0]
                self.offset_y = self.y - event.pos[1]
            elif (self.x + self.width - 10 <= event.pos[0] <= self.x + self.width and
                  self.y + self.height - 10 <= event.pos[1] <= self.y + self.height):
                self.resizing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.resizing = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.x = event.pos[0] + self.offset_x
                self.y = event.pos[1] + self.offset_y
            elif self.resizing:
                self.width = event.pos[0] - self.x
                self.height = event.pos[1] - self.y

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, window_x, window_y):
        pygame.draw.rect(screen, (200, 200, 200), (window_x + self.x, window_y + self.y, self.width, self.height), border_radius=5)
        text = FONT.render(self.text, True, BLACK)
        screen.blit(text, (window_x + self.x + 10, window_y + self.y + 10))

    def is_hovered(self, mouse_x, mouse_y, window_x, window_y):
        return (window_x + self.x <= mouse_x <= window_x + self.x + self.width and
                window_y + self.y <= mouse_y <= window_y + self.y + self.height)

class Tab:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def draw(self, screen, window_x, window_y):
        if self.selected:
            pygame.draw.rect(screen, GREEN, (window_x + self.x, window_y + self.y, self.width, self.height), border_radius=5)
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, (window_x + self.x, window_y + self.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, (window_x + self.x, window_y + self.y, self.width, self.height), border_radius=5, width=1)
        text = FONT.render(self.text, True, BLACK)
        screen.blit(text, (window_x + self.x + 10, window_y + self.y + 10))
        if self.selected:
            for i, child in enumerate(self.children):
                child.draw(screen, window_x, window_y + 40 + i * 30)

    def is_hovered(self, mouse_x, mouse_y, window_x, window_y):
        return (window_x + self.x <= mouse_x <= window_x + self.x + self.width and
                window_y + self.y <= mouse_y <= window_y + self.y + self.height)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    @classmethod
    def select_tab(cls, tabs, tab_index):
        for i, tab in enumerate(tabs):
            if i == tab_index:
                tab.select()
            else:
                tab.deselect()

    @classmethod
    def handle_tab_event(cls, tabs, event, window_x, window_y):
        if hasattr(event, 'pos'):
            for i, tab in enumerate(tabs):
                if tab.is_hovered(event.pos[0], event.pos[1], window_x, window_y):
                    cls.select_tab(tabs, i)
                    break

class ToggleWidget:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.toggled = False

    def draw(self, screen, window_x, window_y):
        if self.toggled:
            pygame.draw.rect(screen, GREEN, (window_x + self.x, window_y + self.y, self.width, self.height), border_radius=10)
            pygame.draw.rect(screen, WHITE, (window_x + self.x + self.width - 20, window_y + self.y + 5, 10, self.height - 10), border_radius=10)
        else:
            pygame.draw.rect(screen, RED, (window_x + self.x, window_y + self.y, self.width, self.height), border_radius=10)
            pygame.draw.rect(screen, WHITE, (window_x + self.x + 10, window_y + self.y + 5, 10, self.height - 10), border_radius=10)
        text = FONT.render(self.text, True, BLACK)
        screen.blit(text, (window_x + self.x + self.width + 10, window_y + self.y + 10))

    def is_hovered(self, mouse_x, mouse_y, window_x, window_y):
        return (window_x + self.x <= mouse_x <= window_x + self.x + self.width and
                window_y + self.y <= mouse_y <= window_y + self.y + self.height)

    def toggle(self):
        self.toggled = not self.toggled
        
class ColorPicker:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (128, 128, 128),  # Gray
            (0, 0, 0),  # Black
            (255, 255, 255),  # White
        ]
        self.selected_color = self.colors[0]

    def draw(self, screen, window_x, window_y):
        for i, color in enumerate(self.colors):
            pygame.draw.rect(screen, color, (window_x + self.x + i * 30, window_y + self.y, 30, 30))
            if self.colors[i] == self.selected_color:
                pygame.draw.rect(screen, (0, 0, 0), (window_x + self.x + i * 30, window_y + self.y, 30, 30), 2)

    def is_hovered(self, mouse_x, mouse_y, window_x, window_y):
        return (window_x + self.x <= mouse_x <= window_x + self.x + self.width and
                window_y + self.y <= mouse_y <= window_y + self.y + self.height)

    def select_color(self, color):
        self.selected_color = color

    def handle_event(self, event, window_x, window_y):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered(event.pos[0], event.pos[1], window_x, window_y):
                for i, color in enumerate(self.colors):
                    if (window_x + self.x + i * 30 <= event.pos[0] <= window_x + self.x + i * 30 + 30 and
                            window_y + self.y <= event.pos[1] <= window_y + self.y + 30):
                        self.select_color(color)

def handle_videoresize(event, screen):
    screen = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)
    return screen
