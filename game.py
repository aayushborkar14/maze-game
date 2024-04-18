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
gamestate = None
gamelevel = 1


def font_with_size(size):
    return pygame.font.Font("assets/Teko-Regular.ttf", size)


def render_text(text, size, color, x, y):
    text = font_with_size(size).render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return text, text_rect


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def maze_game(level, maze_state=None):
    global running, player_sprite, gamestate, gamelevel
    if maze_state is not None:
        if "player_pos" in maze_state:
            player_pos = maze_state["player_pos"]
        else:
            player_pos = (20, 20)
        man_score = maze_state["man_score"]
        collect_score = maze_state["collect_score"]
        if "map" in maze_state:
            map = maze_state["map"]
            maze = maze_state["maze"]
            if "powerup_map" in maze_state:
                powerup_map = maze_state["powerup_map"]
            else:
                powerup_map = None
        else:
            map, maze, powerup_map, time = LevelConfig().get_level_config(level)
        if "time" in maze_state:
            time = maze_state["time"]
    else:
        player_pos = (20, 20)
        man_score = 0
        collect_score = 0
        map, maze, powerup_map, time = LevelConfig().get_level_config(level)
    s_off = 0
    gamestart = 20
    gameend = 89
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
    score_plus_left = 0
    time_plus_left = 0
    black_surface = pygame.Surface((screen.get_width(), screen.get_height())).convert()
    black_surface.fill((0, 0, 0))
    for i in range(31, 0, -1):
        black_surface.set_alpha(i * 8)
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
        pygame.draw.rect(screen, (0, 0, 0), score_rect)
        man_score = max(
            int((136 - manhattan_distance(player_pos, (88, 88))) ** 2), man_score
        )
        score = man_score + collect_score
        render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
        render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
        screen.blit(black_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)
    while running:
        if player_pos == (gameend - 1, gameend - 1):
            if level == "cave":
                assert gamestate is not None
                gamestate["time"] = time
                return maze_game(gamelevel, gamestate)
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
                    if score_plus_left:
                        score_plus_left -= 1
                    if time_plus_left:
                        time_plus_left -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.key.set_repeat(0, 0)
                    return menu()
                if event.key in (pygame.K_UP, pygame.K_w):
                    sprite = 6 + s_off
                    sprite1 = 15 + s_off
                    sprite2 = 24 + s_off
                    rflip = False
                    move_offset = (0, -1)
                    sprite_facing = (0, -1)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    sprite = 0 + s_off
                    sprite1 = 9 + s_off
                    sprite2 = 18 + s_off
                    rflip = False
                    move_offset = (0, 1)
                    sprite_facing = (0, 1)
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    sprite = 3 + s_off
                    sprite1 = 12 + s_off
                    sprite2 = 21 + s_off
                    rflip = False
                    move_offset = (-1, 0)
                    sprite_facing = (-1, 0)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    sprite = 3 + s_off
                    sprite1 = 12 + s_off
                    sprite2 = 21 + s_off
                    rflip = True
                    move_offset = (1, 0)
                    sprite_facing = (1, 0)
                if event.key == pygame.K_SPACE and powerup_map is not None:
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
                            if (
                                powerup_map.map[
                                    player_pos[1] - gamestart + dx,
                                    player_pos[0] - gamestart + dy,
                                ]
                                == PowerUp.SCORE_GAIN
                            ):
                                collect_score += 100
                                score_plus_left = 2
                            elif (
                                powerup_map.map[
                                    player_pos[1] - gamestart + dx,
                                    player_pos[0] - gamestart + dy,
                                ]
                                == PowerUp.TIME_GAIN
                            ):
                                if isinstance(time, int):
                                    time += 10
                                time_plus_left = 2
                            elif (
                                powerup_map.map[
                                    player_pos[1] - gamestart + dx,
                                    player_pos[0] - gamestart + dy,
                                ]
                                == PowerUp.JUMP
                            ):
                                pass
                            elif (
                                powerup_map.map[
                                    player_pos[1] - gamestart + dx,
                                    player_pos[0] - gamestart + dy,
                                ]
                                == PowerUp.CAVE_VENT
                            ):
                                gamelevel = level
                                md0 = manhattan_distance(
                                    player_pos, (gamestart, gamestart)
                                )
                                md_exit = md0 + 28
                                exit_pos = player_pos
                                for i in range(0, gameend - gamestart):
                                    for j in range(0, gameend - gamestart):
                                        if (
                                            not maze.sol_cells[i, j]
                                            and manhattan_distance((0, 0), (i, j))
                                            == md_exit
                                        ):
                                            exit_pos = (j + gamestart, i + gamestart)
                                gamestate = {
                                    "player_pos": exit_pos,
                                    "man_score": man_score,
                                    "collect_score": collect_score,
                                    "map": map,
                                    "maze": maze,
                                    "powerup_map": powerup_map,
                                    "time": time,
                                }
                                black_surface = pygame.Surface(
                                    (
                                        screen.get_width(),
                                        screen.get_height(),
                                    )
                                ).convert()
                                black_surface.fill((0, 0, 0))
                                for i in range(32):
                                    black_surface.set_alpha(i * 8)
                                    screen.blit(black_surface, (0, 0))
                                    pygame.display.update()
                                    clock.tick(60)
                                return maze_game(
                                    "cave",
                                    {
                                        "man_score": man_score,
                                        "collect_score": collect_score,
                                        "time": time,
                                    },
                                )
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
                if score_plus_left:
                    render_text("+100", 30, "#00ff00", 3 * width / 8, 680)
                if time_plus_left:
                    render_text("+10", 30, "#00ff00", 7 * width / 8, 680)
                pygame.display.update()
                clock.tick(60)  # limit the frame rate to 60 FPS
            player_pos = (player_pos[0] + dx, player_pos[1] + dy)
        pygame.draw.rect(screen, (0, 0, 0), score_rect)
        man_score = max(
            int((136 - manhattan_distance(player_pos, (88, 88))) ** 2), man_score
        )
        score = man_score + collect_score
        render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
        render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
        if score_plus_left:
            render_text("+100", 30, "#00ff00", 3 * width / 8, 680)
        if time_plus_left:
            render_text("+10", 30, "#00ff00", 7 * width / 8, 680)
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
                return maze_game(1)
        if medium_rect.collidepoint(pygame.mouse.get_pos()):
            selected_level = 2
            if pygame.mouse.get_pressed()[0]:
                return maze_game(2)
        if hard_rect.collidepoint(pygame.mouse.get_pos()):
            selected_level = 3
            if pygame.mouse.get_pressed()[0]:
                return maze_game(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return maze_game(selected_level)
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
