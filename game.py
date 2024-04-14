import pygame

from maze import Maze
from tiles import Tilemap, Tileset

pygame.init()

size = width, height = 960, 640
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
selected_level = 1
ts2 = Tileset("assets/gen5.png")
ts11 = Tileset("assets/underwater1.png", size=(16, 16))
ts12 = Tileset("assets/underwater2.png", size=(16, 16))
ts3 = Tileset("assets/swampy.png")
ss = Tileset("assets/sprites.png", size=(16, 16))
ts2.load()
ts11.load()
ts12.load()
ts3.load()
ss.load()


def font_with_size(size):
    return pygame.font.Font("assets/Teko-Regular.ttf", size)


def render_text(text, size, color, x, y):
    text = font_with_size(size).render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return text, text_rect


def maze(level):
    global running, ss, map
    player_pos = (20, 20)
    s_off = 0
    m = Maze(level, 70)
    map = None
    if level == 1:
        map = Tilemap(
            ts11,
            ts11,
            ts12,
            "assets/BaseLayer1.npy",
            "assets/TerrainLayer1.npy",
            "assets/TopLayer1.npy",
            m.cells,
            m.sol_cells,
            434,
            90,
            size=(110, 110),
        )
        s_off = 1
    elif level == 2:
        map = Tilemap(
            ts2,
            ts2,
            ts2,
            "assets/BaseLayer2.npy",
            "assets/TerrainLayer2.npy",
            "assets/TopLayer2.npy",
            m.cells,
            m.sol_cells,
            4109,
            4378,
            size=(110, 110),
        )
        s_off = 0
    elif level == 3:
        map = Tilemap(
            ts3,
            ts3,
            ts3,
            "assets/BaseLayer3.npy",
            "assets/TerrainLayer3.npy",
            None,
            m.cells,
            m.sol_cells,
            0,
            3,
            size=(110, 110),
        )
        s_off = 0
    sprite = s_off
    assert map is not None
    map.process_layers()
    pygame.key.set_repeat(150, 150)
    rflip = False
    while running:
        screen.blit(
            map.image,
            map.rect,
            (
                32 * (player_pos[0] - 14),
                32 * (player_pos[1] - 9),
                32 * (player_pos[0] + 15),
                32 * (player_pos[1] + 10),
            ),
        )
        screen.blit(
            pygame.transform.flip(ss.tiles[sprite], rflip, False), (14 * 32, 9 * 32)
        )
        move_offset = None
        sprite1 = 0
        sprite2 = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.key.set_repeat(0, 0)
                    return menu()
                if event.key == pygame.K_UP:
                    sprite = 6 + s_off
                    sprite1 = 15 + s_off
                    sprite2 = 24 + s_off
                    rflip = False
                    move_offset = (0, -1)
                if event.key == pygame.K_DOWN:
                    sprite = 0 + s_off
                    sprite1 = 9 + s_off
                    sprite2 = 18 + s_off
                    rflip = False
                    move_offset = (0, 1)
                if event.key == pygame.K_LEFT:
                    sprite = 3 + s_off
                    sprite1 = 12 + s_off
                    sprite2 = 21 + s_off
                    rflip = False
                    move_offset = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    sprite = 3 + s_off
                    sprite1 = 12 + s_off
                    sprite2 = 21 + s_off
                    rflip = True
                    move_offset = (1, 0)
        if (
            move_offset is not None
            and player_pos[0] + move_offset[0] >= 20
            and player_pos[0] + move_offset[0] < 89
            and player_pos[1] + move_offset[1] >= 20
            and player_pos[1] + move_offset[1] < 89
            and not m.cells[
                player_pos[1] + move_offset[1] - 20, player_pos[0] + move_offset[0] - 20
            ]
        ):
            dx, dy = move_offset
            for i in range(4, 32, 4):
                screen.blit(
                    map.image,
                    map.rect,
                    (
                        32 * (player_pos[0] - 14) + i * dx,
                        32 * (player_pos[1] - 9) + i * dy,
                        32 * (player_pos[0] + 15) + i * dx,
                        32 * (player_pos[1] + 10) + i * dy,
                    ),
                )
                if i % 8:
                    screen.blit(
                        pygame.transform.flip(ss.tiles[sprite1], rflip, False),
                        (14 * 32, 9 * 32),
                    )
                else:
                    screen.blit(
                        pygame.transform.flip(ss.tiles[sprite2], rflip, False),
                        (14 * 32, 9 * 32),
                    )
                pygame.display.update()
                clock.tick(60)  # limit the frame rate to 60 FPS
            player_pos = (player_pos[0] + dx, player_pos[1] + dy)
        pygame.display.update()
        clock.tick(60)  # limit the frame rate to 60 FPS


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
