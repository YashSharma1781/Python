from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Tuple

import pygame


WIDTH, HEIGHT = 900, 600
FPS = 60

WHITE = (240, 240, 240)
BLACK = (10, 10, 14)
ACCENT = (90, 200, 255)
ACCENT_2 = (255, 110, 110)
GRAY = (90, 90, 100)

PADDLE_W, PADDLE_H = 14, 100
PADDLE_SPEED = 7
BALL_SIZE = 14
BALL_START_SPEED = 6.0
BALL_MAX_SPEED = 16.0
BALL_SPEED_INCREASE = 0.35
WIN_SCORE = 7


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Difficulty(Enum):
    EASY = ("Easy", 0.05, 5)
    MEDIUM = ("Medium", 0.09, 7)
    HARD = ("Hard", 0.14, 9)

    def __init__(self, label: str, reaction: float, speed: int):
        self.label = label
        self.reaction = reaction   
        self.speed = speed         



class Paddle:
    """A player- or AI-controlled paddle."""

    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)
        self.color = color
        self.speed = PADDLE_SPEED
        self.score = 0
        self.vy = 0.0 
    def move(self, dy: int) -> None:
        prev_y = self.rect.y
        self.rect.y += dy
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))
        self.vy = self.rect.y - prev_y

    def move_towards(self, target_y: float, lerp: float, max_speed: float) -> None:
        """AI movement: smoothly chase a target y position."""
        # hello world i am
        center = self.rect.centery
        delta = (target_y - center) * lerp
        delta = max(-max_speed, min(max_speed, delta))
        prev_y = self.rect.y
        self.rect.y += int(delta)
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))
        self.vy = self.rect.y - prev_y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
    # 
class Particle:
    """Small dissipating particle used for hit / score effects."""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 5.5)
        self.x, self.y = x, y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.color = color 
        self.radius = random.uniform(2, 4)
    
    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= self.decay

    @property
    def alive(self) -> bool:
        return self.life > 0

    def draw(self, surface: pygame.Surface) -> None:
        if self.life <= 0:
            return
        alpha_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        alpha = max(0, min(255, int(255 * self.life)))
        pygame.draw.circle(
            alpha_surf, (*self.color, alpha), (self.radius, self.radius), self.radius
        )
        surface.blit(alpha_surf, (self.x - self.radius, self.y - self.radius))


class Ball:
    """The ball, including trail rendering and physics."""

    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.trail: List[Tuple[float, float]] = []
        self.reset(direction=random.choice([-1, 1]))

    def reset(self, direction: int) -> None:
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        angle = random.uniform(-0.35, 0.35)  # radians, avoids near-horizontal boring shots
        self.speed = BALL_START_SPEED
        self.vx = math.cos(angle) * self.speed * direction
        self.vy = math.sin(angle) * self.speed
        self.trail.clear()

    def update(self) -> List[Tuple[str, float, float]]:
        """Move the ball, bounce off top/bottom walls. Returns list of events for effects."""
        events = []
        self.trail.append(self.rect.center)
        if len(self.trail) > 12:
            self.trail.pop(0)

        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
            events.append(("wall", self.rect.centerx, self.rect.centery))
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy *= -1
            events.append(("wall", self.rect.centerx, self.rect.centery))

        return events

    def bounce_off_paddle(self, paddle: Paddle) -> None:
        """Reflect the ball off a paddle, adding spin based on paddle movement
        and hit offset (classic Pong 'English')."""
        offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        offset = max(-1, min(1, offset))

        self.speed = min(BALL_MAX_SPEED, self.speed + BALL_SPEED_INCREASE)
        direction = 1 if self.vx < 0 else -1
        max_bounce_angle = math.radians(60)
        angle = offset * max_bounce_angle

        self.vx = math.cos(angle) * self.speed * direction
        self.vy = math.sin(angle) * self.speed + paddle.vy * 0.12

    def draw(self, surface: pygame.Surface) -> None:
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(180 * (i / len(self.trail))) if self.trail else 0
            radius = int(BALL_SIZE / 2 * (i / max(1, len(self.trail))))
            trail_surf = pygame.Surface((radius * 2 + 1, radius * 2 + 1), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (*WHITE, alpha), (radius, radius), radius)
            surface.blit(trail_surf, (tx - radius, ty - radius))
        pygame.draw.ellipse(surface, WHITE, self.rect)




@dataclass
class ScreenShake:
    magnitude: float = 0.0
    decay: float = 0.85

    def kick(self, amount: float) -> None:
        self.magnitude = max(self.magnitude, amount)

    def update(self) -> Tuple[int, int]:
        if self.magnitude < 0.1:
            self.magnitude = 0.0
            return 0, 0
        offset = (
            random.uniform(-self.magnitude, self.magnitude),
            random.uniform(-self.magnitude, self.magnitude),
        )
        self.magnitude *= self.decay
        return int(offset[0]), int(offset[1])


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Advanced Pong")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("consolas", 64, bold=True)
        self.font_mid = pygame.font.SysFont("consolas", 32, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 20)

        self.state = GameState.MENU
        self.difficulty_index = 1  # default: Medium
        self.difficulty = list(Difficulty)[self.difficulty_index]
        self.player = Paddle(30, HEIGHT // 2 - PADDLE_H // 2, ACCENT)
        self.ai = Paddle(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, ACCENT_2)
        self.ball = Ball()
        self.particles: List[Particle] = []
        self.shake = ScreenShake()

        self.menu_options = ["Play", "Difficulty: ", "Quit"]
        self.menu_index = 0
            
        self.winner: str | None = None

    # ----------------------------- helpers -------------------------------- #

    def spawn_particles(self, x: float, y: float, color, count: int = 14) -> None:
        self.particles.extend(Particle(x, y, color) for _ in range(count))

    def update_particles(self) -> None:
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def reset_match(self) -> None:
        self.player.score = 0
        self.ai.score = 0
        self.player.rect.centery = HEIGHT // 2
        self.ai.rect.centery = HEIGHT // 2
        self.ball.reset(direction=random.choice([-1, 1]))
        self.winner = None

    # ------------------------------ input ---------------------------------- #

    def handle_menu_input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.menu_index = (self.menu_index - 1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN:
            self.menu_index = (self.menu_index + 1) % len(self.menu_options)
        elif event.key == pygame.K_LEFT and self.menu_index == 1:
            self.difficulty_index = (self.difficulty_index - 1) % len(Difficulty)
            self.difficulty = list(Difficulty)[self.difficulty_index]
        elif event.key == pygame.K_RIGHT and self.menu_index == 1:
            self.difficulty_index = (self.difficulty_index + 1) % len(Difficulty)
            self.difficulty = list(Difficulty)[self.difficulty_index]
        elif event.key == pygame.K_RETURN:
            if self.menu_index == 0:
                self.reset_match()
                self.state = GameState.PLAYING
            elif self.menu_index == 2:
                pygame.quit()
                sys.exit()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def handle_playing_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.state = GameState.PAUSED

    def handle_paused_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.state = GameState.PLAYING
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.state = GameState.MENU

    def handle_game_over_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.reset_match()
            self.state = GameState.PLAYING
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.state = GameState.MENU

    # ------------------------------ update ---------------------------------- #

    def update_player(self) -> None:
        keys = pygame.key.get_pressed()
        dy = 0
        if keys[pygame.K_w]:
            dy = -self.player.speed
        elif keys[pygame.K_s]:
            dy = self.player.speed
        self.player.move(dy)

    def update_ai(self) -> None:
        # Only react once the ball is heading towards the AI, for a touch of realism
        if self.ball.vx > 0:
            target = self.ball.rect.centery
        else:
            target = HEIGHT // 2  # drift back to center
        self.ai.move_towards(target, self.difficulty.reaction, self.difficulty.speed)

    def update_ball(self) -> None:
        events = self.ball.update()
        for kind, x, y in events:
            self.spawn_particles(x, y, WHITE, count=8)
            self.shake.kick(4)

        # Paddle collisions
        if self.ball.vx < 0 and self.ball.rect.colliderect(self.player.rect):
            self.ball.rect.left = self.player.rect.right
            self.ball.bounce_off_paddle(self.player)
            self.spawn_particles(self.ball.rect.centerx, self.ball.rect.centery, ACCENT)
            self.shake.kick(6)
        elif self.ball.vx > 0 and self.ball.rect.colliderect(self.ai.rect):
            self.ball.rect.right = self.ai.rect.left
            self.ball.bounce_off_paddle(self.ai)
            self.spawn_particles(self.ball.rect.centerx, self.ball.rect.centery, ACCENT_2)
            self.shake.kick(6)

        # Scoring
        if self.ball.rect.right < 0:
            self.ai.score += 1
            self.spawn_particles(0, self.ball.rect.centery, ACCENT_2, count=30)
            self.shake.kick(14)
            self.ball.reset(direction=1)
        elif self.ball.rect.left > WIDTH:
            self.player.score += 1
            self.spawn_particles(WIDTH, self.ball.rect.centery, ACCENT, count=30)
            self.shake.kick(14)
            self.ball.reset(direction=-1)

        if self.player.score >= WIN_SCORE or self.ai.score >= WIN_SCORE:
            self.winner = "Player" if self.player.score > self.ai.score else "AI"
            self.state = GameState.GAME_OVER

    def update(self) -> None:
        if self.state == GameState.PLAYING:
            self.update_player()
            self.update_ai()
            self.update_ball()
        self.update_particles()

    # ------------------------------ drawing ---------------------------------- #

    def draw_center_line(self, offset: Tuple[int, int]) -> None:
        ox, oy = offset
        x = WIDTH // 2 + ox
        dash_h = 14
        gap = 10
        y = 0
        while y < HEIGHT:
            pygame.draw.rect(self.screen, GRAY, (x - 2, y + oy, 4, dash_h))
            y += dash_h + gap

    def draw_playing(self) -> None:
        ox, oy = self.shake.update()
        self.screen.fill(BLACK)
        self.draw_center_line((ox, oy))

        for p in self.particles:
            p.draw(self.screen)

        player_rect = self.player.rect.move(ox, oy)
        ai_rect = self.ai.rect.move(ox, oy)
        pygame.draw.rect(self.screen, self.player.color, player_rect, border_radius=6)
        pygame.draw.rect(self.screen, self.ai.color, ai_rect, border_radius=6)

        ball_copy = Ball.__new__(Ball)
        ball_copy.rect = self.ball.rect.move(ox, oy)
        ball_copy.trail = [(tx + ox, ty + oy) for tx, ty in self.ball.trail]
        ball_copy.draw(self.screen)

        score_l = self.font_big.render(str(self.player.score), True, WHITE)
        score_r = self.font_big.render(str(self.ai.score), True, WHITE)
        self.screen.blit(score_l, (WIDTH // 2 - 80 - score_l.get_width() // 2, 30))
        self.screen.blit(score_r, (WIDTH // 2 + 80 - score_r.get_width() // 2, 30))

        hint = self.font_small.render("W/S to move   |   P to pause", True, GRAY)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 30))

    def draw_menu(self) -> None:
        self.screen.fill(BLACK)
        title = self.font_big.render("ADVANCED PONG", True, ACCENT)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.menu_options):
            label = option
            if i == 1:
                label += self.difficulty.label
            color = ACCENT if i == self.menu_index else WHITE
            text = self.font_mid.render(label, True, color)
            y = 260 + i * 60
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            if i == self.menu_index:
                pygame.draw.polygon(
                    self.screen, ACCENT,
                    [(WIDTH // 2 - text.get_width() // 2 - 30, y + 15),
                     (WIDTH // 2 - text.get_width() // 2 - 15, y + 8),
                     (WIDTH // 2 - text.get_width() // 2 - 15, y + 22)]
                )

        hint = self.font_small.render(
            "UP/DOWN select   |   LEFT/RIGHT change difficulty   |   ENTER confirm",
            True, GRAY
        )
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 60))

    def draw_paused(self) -> None:
        self.draw_playing()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        text = self.font_big.render("PAUSED", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
        hint = self.font_small.render("P/ESC to resume   |   M for menu", True, GRAY)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))

    def draw_game_over(self) -> None:
        self.screen.fill(BLACK)
        for p in self.particles:
            p.draw(self.screen)

            p.draw(self.screen) 
        color = ACCENT if self.winner == "Player" else ACCENT_2
        text = self.font_big.render(f"{self.winner} wins!", True,   color)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
        score = self.font_mid.render(
            f"{self.player.score}  -  {self.ai.score}", True, WHITE
        )
        self.screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2))
        hint = self.font_small.render(
            "ENTER to play again   |   M for menu", True, GRAY
        )
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 70))

    def draw(self) -> None:
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.PAUSED:
            self.draw_paused()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        pygame.display.flip()
       

    # ------------------------------main loop ---------------------------------- #

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.state == GameState.MENU:
                    self.handle_menu_input(event)
                elif self.state == GameState.PLAYING:
                    self.handle_playing_input(event)
                elif self.state == GameState.PAUSED:
                    self.handle_paused_input(event)
                elif self.state == GameState.GAME_OVER:
                    self.handle_game_over_input(event)
              
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()