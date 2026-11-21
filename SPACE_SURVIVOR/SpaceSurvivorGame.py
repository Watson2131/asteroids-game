import random
import pygame
import color
import consts
from Counters import Counters
from Player import Player
from Bullet import Bullet
from Asteroid import Asteroid
from RenderEngine import RenderEngine


class SpaceSurvivorGame:
    def __init__(self):
        pygame.init()
        self.render = RenderEngine()
        pygame.display.set_caption(consts.game_title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 64)
        self.counters = Counters()
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.is_running = True
        self.game_over = False
        self.paused = False
        self.shoot_delay = 0
        self.level = 1
        self.best_score = 0
        self.reset_round()

    def reset_round(self):
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.counters.score = 0
        self.level = 1
        self.shoot_delay = 0

        for _ in range(consts.starting_asteroids):
            self.asteroids.append(Asteroid())

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.is_running = False
                    else:
                        self.paused = not self.paused

                elif event.key == pygame.K_RETURN and self.game_over:
                    self.reset_round()
                    self.game_over = False

    def shoot(self):
        if self.shoot_delay <= 0:
            center_x = self.player.x + self.player.width / 2
            center_y = self.player.y + self.player.height / 2

            self.bullets.append(
                Bullet(center_x, center_y, self.player.angle)
            )

            self.shoot_delay = 12

    def player_hit(self):
        self.player.lives -= 1
        self.player.invulnerable = 100

        self.player.x = (
            consts.screen_width / 2 - self.player.width / 2
        )
        self.player.y = (
            consts.screen_height / 2 - self.player.height / 2
        )

        self.player.rect.topleft = (
            int(self.player.x),
            int(self.player.y)
        )

        if self.player.lives <= 0:
            self.game_over = True

    def game_logic(self):
        self.event_handler()

        if not self.is_running or self.paused or self.game_over:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move_forward()

        if keys[pygame.K_SPACE]:
            self.shoot()

        self.player.update()
        self.shoot_delay = max(0, self.shoot_delay - 1)

        for bullet in self.bullets:
            bullet.move()

        self.bullets = [
            bullet for bullet in self.bullets
            if bullet.life > 0
        ]

        for asteroid in self.asteroids:
            asteroid.move()

        new_asteroids = []

        for asteroid in self.asteroids:
            was_hit = False

            for bullet in self.bullets:
                if bullet.life > 0 and asteroid.collide(bullet):
                    bullet.life = 0
                    was_hit = True
                    break

            if was_hit:
                self.counters.score += 10 * asteroid.size
                new_asteroids.extend(asteroid.split())
            else:
                new_asteroids.append(asteroid)

        self.asteroids = new_asteroids

        self.bullets = [
            bullet for bullet in self.bullets
            if bullet.life > 0
        ]

        if self.player.invulnerable <= 0:
            for asteroid in self.asteroids:
                if self.player.collide(asteroid):
                    self.player_hit()
                    break

        if len(self.asteroids) == 0:
            self.level += 1

            for _ in range(
                consts.starting_asteroids + self.level - 1
            ):
                self.asteroids.append(Asteroid())

        self.clock.tick(consts.game_FPS)

    def draw_hud(self, surface):
        score_text = self.font.render(
            "СЧЁТ: " + str(self.counters.score),
            True,
            color.white
        )

        lives_text = self.font.render(
            "ЖИЗНИ: " + str(self.player.lives),
            True,
            color.green
        )

        level_text = self.font.render(
            "УРОВЕНЬ: " + str(self.level),
            True,
            color.yellow
        )

        surface.blit(score_text, (18, 15))
        surface.blit(lives_text, (220, 15))
        surface.blit(level_text, (410, 15))

        pygame.draw.line(
            surface,
            color.dark_gray,
            (15, 52),
            (consts.screen_width - 15, 52),
            2
        )

    def draw_message(self, title, subtitle):
        overlay = pygame.Surface(consts.screen_params)
        overlay.set_alpha(190)
        overlay.fill(color.black)

        self.render.surface.blit(overlay, (0, 0))

        title_image = self.big_font.render(
            title, True, color.white
        )

        subtitle_image = self.font.render(
            subtitle, True, color.green
        )

        self.render.surface.blit(
            title_image,
            title_image.get_rect(
                center=(
                    consts.screen_width // 2,
                    consts.screen_height // 2 - 30
                )
            )
        )

        self.render.surface.blit(
            subtitle_image,
            subtitle_image.get_rect(
                center=(
                    consts.screen_width // 2,
                    consts.screen_height // 2 + 25
                )
            )
        )

        pygame.display.update()

    def update_scene(self):
        self.render.add_render_object(
            *self.asteroids,
            *self.bullets,
            self.player
        )

        self.render.render()
        self.draw_hud(self.render.surface)

        if self.paused and not self.game_over:
            self.draw_message(
                "ПАУЗА",
                "Нажмите ESC, чтобы продолжить"
            )

        elif self.game_over:
            self.draw_message(
                "ИГРА ОКОНЧЕНА",
                "ENTER — начать заново    ESC — выход"
            )

        pygame.display.update()

    def game_loop(self):
        while self.is_running:
            self.game_logic()
            self.update_scene()

        pygame.quit()