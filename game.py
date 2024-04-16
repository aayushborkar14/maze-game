import pygame

from level_config import LevelConfig
from powerup import PowerUp
from tiles import Tileset

pygame.init()

size = width, height = 960, 720
screen = pygame.display.set_mode(size)
running = True
score_rect = pygame.Rect(0, 640, 960, 80)
clock = pygame.time.Clock()
selected_level = 1
player_sprite = Tileset("assets/sprites.png", size=(16, 16))
player_sprite.load()
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))


def font_with_size(size):
    return pygame.font.Font("assets/Teko-Regular.ttf", size)


def render_text(text, size, color, x, y):
    text = font_with_size(size).render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return text, text_rect


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def maze(level):
    global running, player_sprite
    player_pos = (20, 20)
    s_off = 0
    config = LevelConfig()
    map, maze, powerup_map, time = config.get_level_config(level)
    gamestart = 20
    gameend = 89
    man_score = 0
    collect_score = 0
    if level == 1:
        s_off = 1
    elif level == "cave":
        gameend = 49
    sprite = s_off
    assert map is not None
    map.process_layers()
    pygame.key.set_repeat(150, 150)
    rflip = False
    sprite_facing = (0, 1)
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
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
            pygame.transform.flip(player_sprite.tiles[sprite], rflip, False),
            (14 * 32, 9 * 32),
        )
        move_offset = None
        sprite1 = 0
        sprite2 = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if isinstance(time, int):
                    time -= 1
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
                    sprite_facing = (0, -1)
                if event.key == pygame.K_DOWN:
                    sprite = 0 + s_off
                    sprite1 = 9 + s_off
                    sprite2 = 18 + s_off
                    rflip = False
                    move_offset = (0, 1)
                    sprite_facing = (0, 1)
                if event.key == pygame.K_LEFT:
                    sprite = 3 + s_off
                    sprite1 = 12 + s_off
                    sprite2 = 21 + s_off
                    rflip = False
                    move_offset = (-1, 0)
                    sprite_facing = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    sprite = 3 + s_off
                    sprite1 = 12 + s_off
                    sprite2 = 21 + s_off
                    rflip = True
                    move_offset = (1, 0)
                    sprite_facing = (1, 0)
                if event.key == pygame.K_SPACE:
                    for dx, dy in dirs:
                        if (
                            player_pos[0] - gamestart + dx < gameend
                            and player_pos[1] - gamestart + dy < gameend
                            and powerup_map.map[
                                player_pos[1] - gamestart + dx,
                                player_pos[0] - gamestart + dy,
                            ]
                            not in (0, PowerUp.EMPTY)
                            and (dy, dx) == sprite_facing
                        ):
                            map.remove_powerup(
                                player_pos[1] + dx,
                                player_pos[0] + dy,
                            )
                            powerup_map.map[
                                player_pos[1] - gamestart + dx,
                                player_pos[0] - gamestart + dy,
                            ] = PowerUp.EMPTY
                            break
        if (
            move_offset is not None
            and player_pos[0] + move_offset[0] >= gamestart
            and player_pos[0] + move_offset[0] < gameend
            and player_pos[1] + move_offset[1] >= gamestart
            and player_pos[1] + move_offset[1] < gameend
            and not maze.cells[
                player_pos[1] + move_offset[1] - gamestart,
                player_pos[0] + move_offset[0] - gamestart,
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
                        pygame.transform.flip(
                            player_sprite.tiles[sprite1], rflip, False
                        ),
                        (14 * 32, 9 * 32),
                    )
                else:
                    screen.blit(
                        pygame.transform.flip(
                            player_sprite.tiles[sprite2], rflip, False
                        ),
                        (14 * 32, 9 * 32),
                    )
                pygame.draw.rect(screen, (0, 0, 0), score_rect)
                score = man_score + collect_score
                render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
                render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
                pygame.display.update()
                clock.tick(60)  # limit the frame rate to 60 FPS
            player_pos = (player_pos[0] + dx, player_pos[1] + dy)
        pygame.draw.rect(screen, (0, 0, 0), score_rect)
        man_score = max(136 - manhattan_distance(player_pos, (88, 88)), man_score)
        score = man_score + collect_score
        render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
        render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
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
