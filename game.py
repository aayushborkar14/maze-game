import os

import pygame

from level_config import LevelConfig
from powerup import PowerUp
from tiles import Tileset
from trap import Trap

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/maze.mp3")

if not os.path.exists("leaderboard"):
    os.makedirs("leaderboard")

size = width, height = 960, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Game")
running = True
score_rect = pygame.Rect(0, 640, 960, 80)
pause_rect = pygame.Rect(320, 200, 320, 180)
clock = pygame.time.Clock()
selected_level = 1
player_sprite = Tileset("assets/sprites.png", size=(16, 16))
player_sprite.load()
reduced_vision_screen = pygame.image.load("assets/reduced_vision.png")
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
gamestate = None
gamelevel = 1


def font_with_size(size):
    """
    Get pygame font object with the specified size
    Args:
        size: int, Font size
    Returns:
        pygame.font.Font object
    """
    return pygame.font.Font("assets/Teko-Regular.ttf", size)


def render_text(text, size, color, x, y):
    """
    Render text on the screen
    Args:
        text: str, Text to render
        size: int, Font size
        color: pygame.Color object, Text color
        x: int, X coordinate
        y: int, Y coordinate
    Returns:
        Tuple of pygame.Surface, pygame.Rect, Text surface and its rectangle
    """
    text = font_with_size(size).render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return text, text_rect


def manhattan_distance(a, b):
    """
    Calculate Manhattan distance between two points
    Args:
        a: Tuple of int, Point 1
        b: Tuple of int, Point 2
    Returns:
        int, Manhattan distance between the two points
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def maze_game(level, maze_state=None):
    """
    Main game loop for the maze game's gameplay
    Args:
        level: int, Level number
        maze_state: dict, Maze state to resume the game from (optional)
    """
    global running, player_sprite, gamestate, gamelevel
    pygame.mixer.music.play(-1)
    # Resume game from the saved state
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
            if "trap_map" in maze_state:
                trap_map = maze_state["trap_map"]
        else:
            map, maze, powerup_map, trap_map, time = LevelConfig().get_level_config(
                level
            )
        if "time" in maze_state:
            time = maze_state["time"]
    else:
        player_pos = (20, 20)
        man_score = 0
        collect_score = 0
        map, maze, powerup_map, trap_map, time = LevelConfig().get_level_config(level)
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
    rflip = False
    sprite_facing = (0, 1)
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    score_plus_left = 0
    time_plus_left = 0
    black_surface = pygame.Surface((screen.get_width(), screen.get_height())).convert()
    black_surface.fill((0, 0, 0))
    freeze_time = 0
    reduced_time = 0
    powerup_used = False
    jump_skips = 0
    paused = False
    pause_selection = 0
    pause_cooldown = 0
    # Black screen fade in effect
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
    # Main game loop
    while running:
        if paused:
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
            translucent_black_surface = pygame.Surface(
                (
                    screen.get_width(),
                    screen.get_height(),
                )
            ).convert()
            translucent_black_surface.fill((0, 0, 0))
            translucent_black_surface.set_alpha(128)
            screen.blit(translucent_black_surface, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), pause_rect)
            render_text("Paused", 60, "#ffffff", width / 2, 250)
            resume_color = "#ffffff"
            quit_color = "#ffffff"
            if pause_selection == 0:
                resume_color = "#ff0000"
            else:
                quit_color = "#ff0000"
            render_text("Resume", 40, resume_color, width / 2 - 80, 330)
            render_text("Quit", 40, quit_color, width / 2 + 80, 330)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        pause_selection = 1
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        pause_selection = 0
                    if event.key == pygame.K_RETURN:
                        if pause_selection == 0:
                            paused = False
                            pygame.mixer.music.unpause()
                            pause_cooldown = 8
                        else:
                            if level == "cave":
                                return game_end(score, False, gamelevel)
                            else:
                                return game_end(score, False, level)
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        pygame.mixer.music.unpause()
                        pause_cooldown = 8
            pygame.display.update()
        else:
            # If player reaches the end of the game
            if player_pos == (gameend - 1, gameend - 1):
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
                if level == "cave":
                    assert gamestate is not None
                    gamestate["time"] = time
                    return maze_game(gamelevel, gamestate)
                man_score = max(
                    int((136 - manhattan_distance(player_pos, (88, 88))) ** 2),
                    man_score,
                )
                assert time is not None
                score = man_score + collect_score + time * 100
                if level == "cave":
                    return game_end(score, True, gamelevel)
                else:
                    return game_end(score, True, level)
            if powerup_used:
                if jump_skips < 8:
                    jump_skips += 1
                else:
                    jump_skips = 0
                    powerup_used = False
            if pause_cooldown:
                pause_cooldown -= 1
            image_blitted = False
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
            if freeze_time:
                pygame.draw.rect(screen, (0, 0, 0), score_rect)
                man_score = max(
                    int((136 - manhattan_distance(player_pos, (88, 88))) ** 2),
                    man_score,
                )
                score = man_score + collect_score
                render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
                render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
                if score_plus_left:
                    render_text("+500", 30, "#00ff00", 3 * width / 8, 680)
                if time_plus_left:
                    render_text("+10", 30, "#00ff00", 7 * width / 8, 680)
                freeze_screen = pygame.Surface(
                    (screen.get_width(), screen.get_height())
                ).convert_alpha()
                freeze_screen.fill((0, 0, 0, 128))
                screen.blit(freeze_screen, (0, 0))
                render_text(
                    f"Frozen for {freeze_time} seconds",
                    100,
                    "#ffffff",
                    width / 2,
                    height / 2,
                )
            if (
                trap_map is not None
                and 0 <= player_pos[0] - gamestart < gameend - gamestart
                and 0 <= player_pos[1] - gamestart < gameend - gamestart
                and trap_map.map[
                    player_pos[1] - gamestart,
                    player_pos[0] - gamestart,
                ]
                not in (0, Trap.EMPTY)
            ):
                if not (freeze_time or reduced_time):
                    music_pos = pygame.mixer.music.get_pos()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("assets/lowpassmaze.mp3")
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_pos(music_pos)
                if (
                    (
                        trap_map.map[
                            player_pos[1] - gamestart,
                            player_pos[0] - gamestart,
                        ]
                    )
                    == Trap.SPRITE_FREEZE
                ):
                    freeze_time = 5
                    reduced_time = 0
                elif (
                    (
                        trap_map.map[
                            player_pos[1] - gamestart,
                            player_pos[0] - gamestart,
                        ]
                    )
                    == Trap.REDUCED_VISION
                ):
                    reduced_time = 10
                map.reset_tile(
                    player_pos[1],
                    player_pos[0],
                )
                trap_map.map[
                    player_pos[1] - gamestart,
                    player_pos[0] - gamestart,
                ] = PowerUp.EMPTY
            move_offset = None
            sprite1 = 0
            sprite2 = 0
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT:
                    if isinstance(time, int):
                        time -= 1
                        if time < 0:
                            if level == "cave":
                                return game_end(score, False, gamelevel)
                            else:
                                return game_end(score, False, level)
                        if score_plus_left:
                            score_plus_left -= 1
                        if time_plus_left:
                            time_plus_left -= 1
                        if freeze_time:
                            freeze_time -= 1
                            if not freeze_time:
                                music_pos = pygame.mixer.music.get_pos()
                                pygame.mixer.music.stop()
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load("assets/maze.mp3")
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_pos(music_pos)
                        if reduced_time:
                            reduced_time -= 1
                            if not reduced_time:
                                music_pos = pygame.mixer.music.get_pos()
                                pygame.mixer.music.stop()
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load("assets/maze.mp3")
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_pos(music_pos)
            # key handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                if not pause_cooldown:
                    paused = True
                    pygame.mixer.music.pause()
            if freeze_time:
                pygame.display.update()
                clock.tick(60)  # limit the frame rate to 60 FPS
                continue
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                sprite = 6 + s_off
                sprite1 = 15 + s_off
                sprite2 = 24 + s_off
                rflip = False
                move_offset = (0, -1)
                sprite_facing = (0, -1)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                sprite = 0 + s_off
                sprite1 = 9 + s_off
                sprite2 = 18 + s_off
                rflip = False
                move_offset = (0, 1)
                sprite_facing = (0, 1)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                sprite = 3 + s_off
                sprite1 = 12 + s_off
                sprite2 = 21 + s_off
                rflip = False
                move_offset = (-1, 0)
                sprite_facing = (-1, 0)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                sprite = 3 + s_off
                sprite1 = 12 + s_off
                sprite2 = 21 + s_off
                rflip = True
                move_offset = (1, 0)
                sprite_facing = (1, 0)
            # powerup handling
            if keys[pygame.K_SPACE] and powerup_map is not None:
                for dx, dy in dirs:
                    if (
                        0 <= player_pos[0] - gamestart + dx < gameend - gamestart
                        and 0 <= player_pos[1] - gamestart + dy < gameend - gamestart
                        and powerup_map.map[
                            player_pos[1] - gamestart + dx,
                            player_pos[0] - gamestart + dy,
                        ]
                        not in (0, PowerUp.EMPTY)
                        and (dy, dx) == sprite_facing
                    ):
                        powerup_used = True
                        if (
                            powerup_map.map[
                                player_pos[1] - gamestart + dx,
                                player_pos[0] - gamestart + dy,
                            ]
                            == PowerUp.SCORE_GAIN
                        ):
                            collect_score += 500
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
                            == PowerUp.CAVE_VENT
                        ):
                            gamelevel = level
                            md0 = manhattan_distance(player_pos, (gamestart, gamestart))
                            md_exit = min(md0 + 56, 130)
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
                                "trap_map": trap_map,
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
                                if reduced_time:
                                    screen.convert_alpha()
                                    screen.blit(reduced_vision_screen, (0, 0))
                                    render_text(
                                        f"Reduced vision for {reduced_time} seconds",
                                        30,
                                        "#ffffff",
                                        160,
                                        60,
                                    )
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
                        map.reset_tile(
                            player_pos[1] + dx,
                            player_pos[0] + dy,
                        )
                        powerup_map.map[
                            player_pos[1] - gamestart + dx,
                            player_pos[0] - gamestart + dy,
                        ] = PowerUp.EMPTY
                        break
            # jump handling
            if keys[pygame.K_SPACE] and not powerup_used:
                jx, jy = 0, -1
                dx, dy = sprite_facing
                j = 0
                jumps = [7, 13, 18, 22, 26, 29, 31, 32]
                if dx != 0:
                    jx, jy = 0, -1
                elif dy != 0:
                    jx, jy = -1, 0
                jfactor = 0
                if (
                    0 <= player_pos[0] + dx - gamestart < gameend - gamestart
                    and 0 <= player_pos[1] + dy - gamestart < gameend - gamestart
                    and not maze.cells[
                        player_pos[1] + dy - gamestart,
                        player_pos[0] + dx - gamestart,
                    ]
                ):
                    jfactor = 2
                    if (
                        0 <= player_pos[0] + 2 * dx - gamestart < gameend - gamestart
                        and 0
                        <= player_pos[1] + 2 * dy - gamestart
                        < gameend - gamestart
                        and not maze.cells[
                            player_pos[1] + 2 * dy - gamestart,
                            player_pos[0] + 2 * dx - gamestart,
                        ]
                    ):
                        jfactor = 4
                for i, jump in enumerate(jumps):
                    screen.blit(
                        map.image,
                        map.rect,
                        (
                            32 * (player_pos[0] - 14)
                            + jump * jx
                            + (i + 1) * jfactor * dx,
                            32 * (player_pos[1] - 9)
                            + jump * jy
                            + (i + 1) * jfactor * dy,
                            32 * (player_pos[0] + 15)
                            + jump * jx
                            + (i + 1) * jfactor * dx,
                            32 * (player_pos[1] + 10)
                            + jump * jy
                            + (i + 1) * jfactor * dy,
                        ),
                    )
                    screen.blit(
                        pygame.transform.flip(
                            player_sprite.tiles[sprite], rflip, False
                        ),
                        (14 * 32, 9 * 32),
                    )
                    image_blitted = False
                    pygame.draw.rect(screen, (0, 0, 0), score_rect)
                    man_score = max(
                        int((136 - manhattan_distance(player_pos, (88, 88))) ** 2),
                        man_score,
                    )
                    score = man_score + collect_score
                    render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
                    render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
                    if reduced_time:
                        screen.convert_alpha()
                        screen.blit(reduced_vision_screen, (0, 0))
                        render_text(
                            f"Reduced vision for {reduced_time} seconds",
                            30,
                            "#ffffff",
                            160,
                            60,
                        )
                        image_blitted = True
                    pygame.display.update()
                    clock.tick(60)
                for i, jump in enumerate(reversed(jumps)):
                    screen.blit(
                        map.image,
                        map.rect,
                        (
                            32 * (player_pos[0] - 14)
                            + jump * jx
                            + (i + 1 + len(jumps)) * jfactor * dx,
                            32 * (player_pos[1] - 9)
                            + jump * jy
                            + (i + 1 + len(jumps)) * jfactor * dy,
                            32 * (player_pos[0] + 15)
                            + jump * jx
                            + (i + 1 + len(jumps)) * jfactor * dx,
                            32 * (player_pos[1] + 10)
                            + jump * jy
                            + (i + 1 + len(jumps)) * jfactor * dy,
                        ),
                    )
                    screen.blit(
                        pygame.transform.flip(
                            player_sprite.tiles[sprite], rflip, False
                        ),
                        (14 * 32, 9 * 32),
                    )
                    image_blitted = False
                    pygame.draw.rect(screen, (0, 0, 0), score_rect)
                    man_score = max(
                        int((136 - manhattan_distance(player_pos, (88, 88))) ** 2),
                        man_score,
                    )
                    score = man_score + collect_score
                    render_text(f"Score: {score}", 30, "#ffffff", width / 4, 680)
                    render_text(f"Time: {time}", 30, "#ffffff", 3 * width / 4, 680)
                    if reduced_time:
                        screen.convert_alpha()
                        screen.blit(reduced_vision_screen, (0, 0))
                        render_text(
                            f"Reduced vision for {reduced_time} seconds",
                            30,
                            "#ffffff",
                            160,
                            60,
                        )
                        image_blitted = True
                    pygame.display.update()
                    clock.tick(60)
                player_pos = (
                    player_pos[0] + (jfactor // 2) * dx,
                    player_pos[1] + (jfactor // 2) * dy,
                )
            # smooth movement handling
            elif (
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
                    image_blitted = False
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
                        render_text("+500", 30, "#00ff00", 3 * width / 8, 680)
                    if time_plus_left:
                        render_text("+10", 30, "#00ff00", 7 * width / 8, 680)
                    if reduced_time:
                        screen.convert_alpha()
                        screen.blit(reduced_vision_screen, (0, 0))
                        render_text(
                            f"Reduced vision for {reduced_time} seconds",
                            30,
                            "#ffffff",
                            160,
                            60,
                        )
                        image_blitted = True
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
                render_text("+500", 30, "#00ff00", 3 * width / 8, 680)
            if time_plus_left:
                render_text("+10", 30, "#00ff00", 7 * width / 8, 680)
            if reduced_time and not image_blitted:
                screen.convert_alpha()
                screen.blit(reduced_vision_screen, (0, 0))
                render_text(
                    f"Reduced vision for {reduced_time} seconds",
                    30,
                    "#ffffff",
                    160,
                    60,
                )
            pygame.display.update()
            clock.tick(60)  # limit the frame rate to 60 FPS


def game_end(score, completed, level):
    """
    Game end screen
    Args:
        score: int, game score
        completed: bool, level completed or not
        level: int, level
    Returns to menu if user presses escape or selects exit
    """
    pygame.mixer.music.stop()
    global running
    scores = []
    if os.path.isfile(f"leaderboard/highscores{level}.txt"):
        with open(f"leaderboard/highscores{level}.txt", "r") as f:
            for line in f:
                if line.strip().isdigit():
                    scores.append(int(line.strip()))
        scores.append(score)
        with open(f"leaderboard/highscores{level}.txt", "w") as f:
            for i, s in enumerate(sorted(scores, reverse=True)):
                if i >= 8:
                    break
                f.write(f"{s}\n")
    else:
        scores.append(score)
        with open(f"leaderboard/highscores{level}.txt", "w") as f:
            f.write(f"{score}\n")
    selected_option = 0
    score_count = 0
    for s in scores:
        if s == score:
            score_count += 1
    while running:
        screen.fill((0, 0, 0))
        if completed:
            render_text("Level Completed", 100, "#ffffff", width / 2, 100)
        else:
            render_text("Game Over", 100, "#ffffff", width / 2, 100)
        render_text(f"Score: {score}", 50, "#ffffff", width / 2, 200)
        if score == max(scores) and score_count == 1:
            render_text("New High Score!", 50, "#ffff00", width / 2, 250)
        leaderboard_color = home_color = "#ffffff"
        if selected_option == 0:
            leaderboard_color = "#ff0000"
        else:
            home_color = "#ff0000"
        render_text("View Leaderboard", 50, leaderboard_color, width / 2, 400)
        render_text("Go back home", 50, home_color, width / 2, 500)
        render_text("Press Esc to go back", 30, "#ffffff", width / 2, 600)
        render_text("Press Enter to continue", 30, "#ffffff", width / 2, 650)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_option == 1:
                        return menu()
                    else:
                        leaderboard(level)
                if event.key == pygame.K_UP:
                    selected_option = 0
                if event.key == pygame.K_DOWN:
                    selected_option = 1
                if event.key == pygame.K_ESCAPE:
                    return menu()


def leaderboard_selector():
    """
    Select the level for which leaderboard is to be displayed
    Returns to menu if user presses escape
    Returns the leaderboard for the selected level otherwise
    """
    global running, selected_level
    selected_level = 1
    while running:
        easy_color = medium_color = hard_color = "#ffffff"
        if selected_level == 1:
            easy_color = "#ff0000"
        elif selected_level == 2:
            medium_color = "#ff0000"
        elif selected_level == 3:
            hard_color = "#ff0000"
        screen.fill((0, 0, 0))
        render_text("Select a level", 100, "#ffffff", width / 2, 100)
        render_text("Easy", 50, easy_color, width / 2, 250)
        render_text("Medium", 50, medium_color, width / 2, 325)
        render_text("Hard", 50, hard_color, width / 2, 400)
        render_text("Press Esc to go back", 30, "#ffffff", width / 2, 600)
        render_text("Press Enter to continue", 30, "#ffffff", width / 2, 650)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    leaderboard(selected_level)
                if event.key == pygame.K_UP:
                    selected_level = max(selected_level - 1, 1)
                if event.key == pygame.K_DOWN:
                    selected_level = min(selected_level + 1, 3)
                if event.key == pygame.K_ESCAPE:
                    return menu()
        pygame.display.update()
        clock.tick(60)


def leaderboard(level):
    """
    Display the leaderboard for the selected level
    Args:
        level: int, selected level
    """
    global running
    scores = []
    if os.path.isfile(f"leaderboard/highscores{level}.txt"):
        with open(f"leaderboard/highscores{level}.txt", "r") as f:
            for line in f:
                if line.strip().isdigit():
                    scores.append(int(line.strip()))
    scores = scores[:8]
    while running:
        screen.fill((0, 0, 0))
        render_text("Leaderboard", 100, "#ffffff", width / 2, 100)
        if scores:
            for i, score in enumerate(sorted(scores, reverse=True)):
                if i >= 10:
                    break
                render_text(f"{i + 1}. {score}", 50, "#ffffff", width / 2, 200 + i * 50)
        else:
            render_text("No scores yet", 50, "#ffffff", width / 2, 200)
        render_text("Press Esc to go back", 30, "#ffffff", width / 2, 600)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.update()
        clock.tick(60)


def menu():
    """
    The main menu of the game
    Exits the game if user presses escape
    """
    global running, selected_level

    while running:
        screen.fill((0, 0, 0))
        menu_title = font_with_size(100).render("Choose a Level", True, "#ffffff")
        menu_rect = menu_title.get_rect(center=(width / 2, 100))
        screen.blit(menu_title, menu_rect)
        easy_color = medium_color = hard_color = leaderboard_color = "#ffffff"
        if selected_level == 1:
            easy_color = "#ff0000"
        elif selected_level == 2:
            medium_color = "#ff0000"
        elif selected_level == 3:
            hard_color = "#ff0000"
        elif selected_level == 4:
            leaderboard_color = "#ff0000"

        _, easy_rect = render_text("Easy", 50, easy_color, width / 2, 250)
        _, medium_rect = render_text("Medium", 50, medium_color, width / 2, 325)
        _, hard_rect = render_text("Hard", 50, hard_color, width / 2, 400)
        _, leaderboard_rect = render_text(
            "Leaderboard", 50, leaderboard_color, width / 2, 475
        )

        render_text("Press Esc to exit", 30, "#ffffff", width / 2, 600)
        render_text("Press Enter to continue", 30, "#ffffff", width / 2, 650)

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
        if leaderboard_rect.collidepoint(pygame.mouse.get_pos()):
            selected_level = 4
            if pygame.mouse.get_pressed()[0]:
                return leaderboard_selector()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_level == 4:
                        return leaderboard_selector()
                    return maze_game(selected_level)
                if event.key == pygame.K_UP:
                    selected_level = max(1, selected_level - 1)
                if event.key == pygame.K_DOWN:
                    selected_level = min(4, selected_level + 1)
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)  # limit the frame rate to 60 FPS


menu()
pygame.quit()
