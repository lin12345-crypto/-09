import pygame


class BallGame:
    """Here is a game where arrow keys move a ball inside the window."""

    WIDTH = 800
    HEIGHT = 600
    RADIUS = 25
    STEP = 20

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Moving Ball")
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)

        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2

    def move_ball(self, change_x, change_y):
        """Here is boundary checking before the ball position is changed."""
        new_x = self.ball_x + change_x
        new_y = self.ball_y + change_y

        if self.RADIUS <= new_x <= self.WIDTH - self.RADIUS:
            self.ball_x = new_x

        if self.RADIUS <= new_y <= self.HEIGHT - self.RADIUS:
            self.ball_y = new_y

    def handle_key(self, key):
        """Here is the arrow-key input handler."""
        if key == pygame.K_UP:
            self.move_ball(0, -self.STEP)
        elif key == pygame.K_DOWN:
            self.move_ball(0, self.STEP)
        elif key == pygame.K_LEFT:
            self.move_ball(-self.STEP, 0)
        elif key == pygame.K_RIGHT:
            self.move_ball(self.STEP, 0)

    def draw(self):
        """Here is the white background and the 50 by 50 pixel red ball."""
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (220, 45, 55), (self.ball_x, self.ball_y), self.RADIUS)

        instructions = self.font.render("Use arrow keys to move by 20 pixels", True, (40, 40, 50))
        self.screen.blit(instructions, (20, 20))

        position = self.font.render(f"Position: ({self.ball_x}, {self.ball_y})", True, (80, 80, 90))
        self.screen.blit(position, (20, 52))

    def run(self):
        """Here is the main game loop."""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.handle_key(event.key)

            self.draw()
            pygame.display.flip()
            self.timer.tick(60)

        pygame.quit()

