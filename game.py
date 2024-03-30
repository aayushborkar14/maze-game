import pygame
from tiles import Tilemap, Tileset

pygame.init()

size = width, height = 960, 640
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
selected_level = 1
ts = Tileset("assets/gen5.png")
ts.load()
map = Tilemap(
    ts,
    "assets/BaseLayer.npy",
    "assets/TerrainLayer.npy",
    "assets/TopLayer.npy",
    size=(110, 110),
    rect=(0, 0, 960, 640),
)


def font_with_size(size):
    return pygame.font.Font("assets/Teko-Regular.ttf", size)


def maze(level):
    global running
    map.render_around(20, 20)
    while running:
        screen.blit(map.image, map.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        clock.tick(60)  # limit the frame rate to 60 FPS


def render_text(text, size, color, x, y):
    text = font_with_size(size).render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return text, text_rect


def menu():
    global running, selected_level
    pygame.display.set_caption("Main Menu")

    while running:
        screen.fill((0, 0, 0))
        menu_title = font_with_size(100).render("Choose a Level", True, "#ffffff")
        menu_rect = menu_title.get_rect(center=(width / 2, 100))
        screen.blit(menu_title, menu_rect)
        easy_color = medium_color = hard_color = "#ffffff"
        if selected_level == 1:
            easy_color = "#ff0000"
        elif selected_level == 2:
            medium_color = "#ff0000"
        elif selected_level == 3:
            hard_color = "#ff0000"

        _, easy_rect = render_text("Easy", 50, easy_color, width / 2, 250)
        _, medium_rect = render_text("Medium", 50, medium_color, width / 2, 325)
        _, hard_rect = render_text("Hard", 50, hard_color, width / 2, 400)

        render_text("Press Enter to start", 30, "#ffffff", width / 2, 500)
        render_text("Press Esc to exit", 30, "#ffffff", width / 2, 550)

        if easy_rect.collidepoint(pygame.mouse.get_pos()):
            selected_level = 1
            if pygame.mouse.get_pressed()[0]:
                return maze(1)
        if medium_rect.collidepoint(pygame.mouse.get_pos()):
            selected_level = 2
            if pygame.mouse.get_pressed()[0]:
                return maze(2)
        if hard_rect.collidepoint(pygame.mouse.get_pos()):
            selected_level = 3
            if pygame.mouse.get_pressed()[0]:
                return maze(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return maze(selected_level)
                if event.key == pygame.K_UP:
                    selected_level = max(1, selected_level - 1)
                if event.key == pygame.K_DOWN:
                    selected_level = min(3, selected_level + 1)
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)  # limit the frame rate to 60 FPS


menu()
pygame.quit()
