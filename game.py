import pygame

pygame.init()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
selected_level = 1


def font_with_size(size):
    return pygame.font.Font("assets/Teko-Regular.ttf", size)


def maze(level):
    global running
    while running:
        screen.fill((0, 0, 0))
        title = font_with_size(100).render(f"LEVEL {level}", True, "#ffffff")
        title_rect = title.get_rect(center=(width / 2, 100))
        screen.blit(title, title_rect)

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
    global running
    pygame.display.set_caption("Main Menu")

    while running:
        screen.fill((0, 0, 0))
        menu_title = font_with_size(100).render("Main Menu", True, "#ffffff")
        menu_rect = menu_title.get_rect(center=(width / 2, 100))
        screen.blit(menu_title, menu_rect)

        _, easy_rect = render_text("Easy", 50, "#ffffff", width / 2, 300)
        _, medium_rect = render_text("Medium", 50, "#ffffff", width / 2, 400)
        _, hard_rect = render_text("Hard", 50, "#ffffff", width / 2, 500)

        render_text("Press Enter to start", 30, "#ffffff", width / 2, 600)
        render_text("Press Esc to exit", 30, "#ffffff", width / 2, 650)

        if easy_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, "#ffffff", easy_rect, 2)
            if pygame.mouse.get_pressed()[0]:
                return maze(1)
        if medium_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, "#ffffff", medium_rect, 2)
            if pygame.mouse.get_pressed()[0]:
                return maze(2)
        if hard_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, "#ffffff", hard_rect, 2)
            if pygame.mouse.get_pressed()[0]:
                return maze(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)  # limit the frame rate to 60 FPS


menu()
pygame.quit()
