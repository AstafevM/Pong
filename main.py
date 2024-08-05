import pygame as pg
import sys
from random import randint
pg.font.init()

class Player1(pg.sprite.Sprite):  # LEFT PLAYER
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pg.image.load('player.png')
        self.rect = self.image.get_rect(left=self.screen_rect.left + 20, centery=self.screen_rect.centery)
        self.moveUp = self.moveDown = False

    def output(self):
        if self.moveUp and self.rect.top > self.screen_rect.top:
            self.rect.y -= 15
        elif self.moveDown and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 15
        self.screen.blit(self.image, self.rect)


class Player2(Player1):  # RIGHT PLAYER
    def __init__(self, screen):
        super().__init__(screen)
        self.rect.right = self.screen_rect.right - 20


class Ball(pg.sprite.Sprite):
    def __init__(self, screen, player1_rect: pg.Rect, player2_rect: pg.Rect):
        super().__init__()
        self.directions = -5, 5
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.player1_rect = player1_rect
        self.player2_rect = player2_rect
        self.image = pg.image.load('ball.png')
        self.rect = self.image.get_rect(center=self.screen_rect.center)
        self.vx = self.directions[randint(0, 1)]
        self.vy = self.directions[randint(0, 1)]

    @staticmethod
    def increasing_speed(speed):
        if speed >= 15 or speed <= -15: return speed + 0
        elif speed < 0: return speed - 1
        elif speed > 0: return speed + 1

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top < self.screen_rect.top:
            self.vy = -self.vy
        elif self.rect.bottom > self.screen_rect.bottom:
            self.vy = -self.vy

        if (self.rect.left < self.player1_rect.right and self.player1_rect.centery - 8 < self.rect.centery < self.player1_rect.centery + 8) or \
           (self.rect.right > self.player2_rect.left and self.player2_rect.centery - 8 < self.rect.centery < self.player2_rect.centery + 8):
            self.vx = self.increasing_speed(-self.vx)
            self.vy = 0

        if (self.rect.left < self.player1_rect.right and (self.player1_rect.top + 16 < self.rect.centery < self.player1_rect.centery - 8 or self.player1_rect.centery + 8 < self.rect.centery < self.player1_rect.bottom - 16)) or \
           (self.rect.right > self.player2_rect.left and (self.player2_rect.top + 16 < self.rect.centery < self.player2_rect.centery - 8 or self.player2_rect.centery + 8 < self.rect.centery < self.player2_rect.bottom - 16)):
            self.vx = self.increasing_speed(-self.vx)
            if self.vy == 0:
                if self.player1_rect.top + 16 < self.rect.centery < self.player1_rect.centery - 8 or self.player2_rect.top + 16 < self.rect.centery < self.player2_rect.centery - 8:
                    self.vy = -5
                elif self.player1_rect.centery + 8 < self.rect.centery < self.player1_rect.bottom - 16 or self.player2_rect.centery + 8 < self.rect.centery < self.player2_rect.bottom - 16:
                    self.vy = 5

        if (self.rect.left < self.player1_rect.right and (self.player1_rect.top < self.rect.centery < self.player1_rect.top + 16 or self.player1_rect.bottom - 16 < self.rect.centery < self.player1_rect.bottom)) or \
           (self.rect.right > self.player2_rect.left and (self.player2_rect.top < self.rect.centery < self.player2_rect.top + 16 or self.player2_rect.bottom - 16 < self.rect.centery < self.player2_rect.bottom)):
            self.vx = self.increasing_speed(-self.vx)
            if self.vy == 0:
                if self.player1_rect.top < self.rect.centery < self.player1_rect.top + 16 or self.player2_rect.top < self.rect.centery < self.player2_rect.top + 16:
                    self.vy = -5
                elif self.player1_rect.bottom - 16 < self.rect.centery < self.player1_rect.bottom or self.player2_rect.bottom - 16 < self.rect.centery < self.player2_rect.bottom:
                    self.vy = 5

            elif self.vy < 0:
                if self.player1_rect.top < self.rect.centery < self.player1_rect.top + 16 or self.player2_rect.top < self.rect.centery < self.player2_rect.top + 16:
                    self.vy = -self.vy
                elif self.player1_rect.bottom - 16 < self.rect.centery < self.player1_rect.bottom or self.player2_rect.bottom - 16 < self.rect.centery < self.player2_rect.bottom:
                    self.vy = -5

            elif self.vy > 0:
                if self.player1_rect.top < self.rect.centery < self.player1_rect.top + 16 or self.player2_rect.top < self.rect.centery < self.player2_rect.top + 16:
                    self.vy = 5
                elif self.player1_rect.bottom - 16 < self.rect.centery < self.player1_rect.bottom or self.player2_rect.bottom - 16 < self.rect.centery < self.player2_rect.bottom:
                    self.vy = -self.vy

        self.screen.blit(self.image, self.rect)


class Main:
    def __init__(self):
        pg.display.set_caption('Pong')
        self.screen = pg.display.set_mode(size=(1100, 800))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.player1 = Player1(self.screen)
        self.player2 = Player2(self.screen)
        self.ball = Ball(self.screen, self.player1.rect, self.player2.rect)
        self.point1 = self.point2 = 0
        self.font = pg.font.Font('VCR_OSD_MONO_1.001.ttf', 30)
        self.text1 = self.font.render(str(self.point1), False, 'white')
        self.text1_rect = self.text1.get_rect(y=10, centerx=self.screen_rect.centerx-30)
        self.text2 = self.font.render(str(self.point2), False, 'white')
        self.text2_rect = self.text2.get_rect(y=10, centerx=self.screen_rect.centerx+30)

    def check_ball_pos(self):
        if self.ball.rect.left > self.player1.rect.right - 11 and self.ball.rect.right < self.player2.rect.left + 11:
            self.ball.update()
        elif self.ball.rect.right > self.player2.rect.left + 11:
            self.point1 += 1
            self.text1 = self.font.render(str(self.point1), False, 'white')
            self.ball.rect = self.ball.image.get_rect(center=self.screen_rect.center)
            self.ball.vx = self.ball.directions[randint(0, 1)]
            self.ball.vy = self.ball.directions[randint(0, 1)]
            self.ball.update()
        elif self.ball.rect.left < self.player1.rect.right - 11:
            self.point2 += 1
            self.text2 = self.font.render(str(self.point2), False, 'white')
            self.ball.rect = self.ball.image.get_rect(center=self.screen_rect.center)
            self.ball.vx = self.ball.directions[randint(0, 1)]
            self.ball.vy = self.ball.directions[randint(0, 1)]
            self.ball.update()

    def field_update(self):
        self.screen.fill('black')
        for y in range(10, 800, 40):
            pg.draw.rect(color='white', surface=self.screen, rect=(547, y, 6, 15))
        self.screen.blit(self.text1, self.text1_rect)
        self.screen.blit(self.text2, self.text2_rect)

    def check_event(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()
            elif e.type == pg.KEYDOWN and e.key == pg.K_w:
                self.player1.moveUp = True
            elif e.type == pg.KEYDOWN and e.key == pg.K_s:
                self.player1.moveDown = True
            elif e.type == pg.KEYDOWN and e.key == pg.K_UP:
                self.player2.moveUp = True
            elif e.type == pg.KEYDOWN and e.key == pg.K_DOWN:
                self.player2.moveDown = True
            elif e.type == pg.KEYUP and (e.key == pg.K_w or e.key == pg.K_s):
                self.player1.moveUp = self.player1.moveDown = False
            elif e.type == pg.KEYUP and (e.key == pg.K_UP or e.key == pg.K_DOWN):
                self.player2.moveUp = self.player2.moveDown = False

    def run(self):
        while True:
            self.clock.tick(60)
            self.check_event()
            self.field_update()
            self.player1.output()
            self.player2.output()
            self.check_ball_pos()
            pg.display.update()

game = Main()
game.run()