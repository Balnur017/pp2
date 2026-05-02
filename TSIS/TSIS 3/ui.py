import pygame
import sys


def draw_text(surface, text, size, x, y, color=(0, 0, 0)):
    font = pygame.font.SysFont("Verdana", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200)):
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = text
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        draw_text(surface, self.text, 25, self.rect.centerx, self.rect.centery)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def input_name_screen(screen, width, height):
    name = ""

    while True:
        screen.fill((255, 255, 255))

        draw_text(screen, "ENTER YOUR NAME:", 30, width//2, height//2 - 60)
        draw_text(screen, name + "|", 40, width//2, height//2, (0, 0, 255))
        draw_text(screen, "Press ENTER to Start", 18, width//2, height//2 + 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                # ✅ ENTER — запуск игры
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        return name.strip()

                # ⬅️ Backspace
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                # ❌ игнорируем Enter и странные символы
                else:
                    if event.unicode.isprintable() and event.unicode not in ["\r", "\n"]:
                        if len(name) < 12:
                            name += event.unicode

        pygame.display.update()