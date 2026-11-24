from datetime import datetime
from pathlib import Path

import pygame


class MickeyClock:
    """Here is a clock that uses Mickey-style hands for minutes and seconds."""

    WIDTH = 700
    HEIGHT = 700

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mickey's Clock")
        self.timer = pygame.time.Clock()

        self.center = (self.WIDTH // 2, self.HEIGHT // 2 + 25)
        self.large_font = pygame.font.Font(None, 58)
        self.small_font = pygame.font.Font(None, 30)

        image_path = Path(__file__).parent / "images" / "mickey_hand.png"
        original_hand = pygame.image.load(image_path).convert_alpha()
        self.minute_hand = pygame.transform.smoothscale(original_hand, (85, 245))
        self.second_hand = pygame.transform.smoothscale(original_hand, (62, 205))

    def draw_face(self):
        """Here is the clock face and its minute marks."""
        self.screen.fill((238, 246, 255))
        pygame.draw.circle(self.screen, (255, 255, 255), self.center, 285)
        pygame.draw.circle(self.screen, (30, 35, 45), self.center, 285, 8)

        for number in range(60):
            angle = number * 6
            direction = pygame.Vector2(0, -1).rotate(angle)
            outer_point = pygame.Vector2(self.center) + direction * 265
            line_length = 19 if number % 5 == 0 else 9
            inner_point = pygame.Vector2(self.center) + direction * (265 - line_length)
            line_width = 5 if number % 5 == 0 else 2
            pygame.draw.line(self.screen, (45, 50, 60), inner_point, outer_point, line_width)

        title = self.small_font.render("MINUTES AND SECONDS", True, (50, 60, 80))
        title_rect = title.get_rect(center=(self.center[0], 175))
        self.screen.blit(title, title_rect)

    def draw_rotated_hand(self, image, angle):
        """Here is a hand rotated around the center of the clock."""
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_rect = rotated_image.get_rect(center=self.center)
        self.screen.blit(rotated_image, rotated_rect)

    def draw_time(self):
        """Here is the current system time synchronized with the clock hands."""
        current_time = datetime.now()
        seconds = current_time.second + current_time.microsecond / 1_000_000
        minutes = current_time.minute + seconds / 60

        # Here is the angle calculation: zero degrees is the top of the clock.
        minute_angle = minutes * 6
        second_angle = seconds * 6

        # Here is Mickey's right hand for minutes and left hand for seconds.
        self.draw_rotated_hand(self.minute_hand, minute_angle)
        self.draw_rotated_hand(self.second_hand, second_angle)

        pygame.draw.circle(self.screen, (20, 20, 25), self.center, 14)
        pygame.draw.circle(self.screen, (240, 55, 55), self.center, 7)

        digital_text = current_time.strftime("%M:%S")
        time_surface = self.large_font.render(digital_text, True, (25, 30, 40))
        time_rect = time_surface.get_rect(center=(self.center[0], 575))
        self.screen.blit(time_surface, time_rect)

    def run(self):
        """Here is the main event and drawing loop."""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.draw_face()
            self.draw_time()
            pygame.display.flip()
            self.timer.tick(30)

        pygame.quit()

