import pygame as pg
import random
from pygame.sprite import Sprite
from vector import Vector
from timer import Timer, TimerDual
from imagerect import ImageRect


class Ghost(Sprite):
    SPEED = 0

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.velocity = Ghost.SPEED * Vector(1, 0)

        self.image = pg.image.load('images/red_ghost4r.png')
        self.rect = self.image.get_rect()

        self.rect.left = self.rect.width
        self.rect.top = self.rect.height
        self.x = float(self.rect.x)
        self.alive = True
        self.rev = False
        self.timer = None
        self.timerR = None
        self.timerL = None
        self.timerU = None
        self.timerD = None
        self.timer = self.timerU
        self.current_direction = 'up'
        self.moveD = 'u'
        self.speed = 1
        self.directions_remain = []
        self.eyes_animations = {
            'left': 'eyes_left', 'down': 'eyes_down', 'right': 'eyes_right', 'up': 'eyes_up'
        }
        self.timerBlueGhost = TimerDual(game=self.game, images1=['g3762', 'g3770'], images2=['g3512', 'g3520'],
                                        wait1=200, wait2=200, wait_switch_timers=6000, frameindex1=0, frameindex2=0,
                                        step1=1, step2=1, looponce=False)

    def width(self): return self.rect.width

    def height(self): return self.rect.height

    def check_edges(self):
        r = self.rect
        s_r = self.screen.get_rect()
        return r.right >= s_r.right or r.left <= 0

    def draw(self):
        temp_image = self.timer.imagerect()
        self.screen.blit(temp_image.image, self.rect)

    def move(self):
        if self.ball_stop(self.moveD) is False:
            if self.alive and not self.rev:
                if self.moveD == 'r':
                    self.timer = self.timerR
                    self.rect.x += self.speed
                elif self.moveD == 'l':
                    self.timer = self.timerL
                    self.rect.x -= self.speed
                elif self.moveD == 'd':
                    self.timer = self.timerD
                    self.rect.y += self.speed
                else:
                    self.timer = self.timerU
                    self.rect.y -= self.speed
                    self.moveD = 'u'
            else:
                if self.moveD == 'r':
                    self.rect.x += self.speed
                elif self.moveD == 'l':
                    self.rect.x -= self.speed
                elif self.moveD == 'd':
                    self.rect.y += self.speed
                else:
                    self.rect.y -= self.speed
                    self.moveD = 'u'
        self.ai()

    def reverse_draw(self):
        # self.timer = self.timerBlueGhost
        if not self.alive:
            # eyes
            # temp_image = self.eyes_animations[self.current_direction]
            temp_image = (ImageRect(self.screen, self.eyes_animations[self.current_direction], height=25, width=25))
            self.screen.blit(temp_image.image, self.rect)
            return
        if self.timerBlueGhost.counter >= 2:
            self.reanimate()
        temp_image = self.timer.imagerect()
        self.screen.blit(temp_image.image, self.rect)

    def reverse(self):
        self.rev = True
        self.timer = self.timerBlueGhost
        self.timerBlueGhost.reset()

    def reanimate(self):
        self.rev = False
        self.alive = True
        self.timer = self.timerU
        self.draw()

    def reverse_update(self):
        self.move()
        self.reverse_draw()

    def reset(self):
        self.timer = self.timerD
        self.rev = False
        self.alive = True

    def update(self):
        if self.rev:
            self.reverse_update()
            return
        self.move()
        self.draw()

    def ai(self):
        if self.moveD == "u" and self.rect == (286, 300, 30, 30):
            self.moveD = "l"
        elif 280 < self.rect.x < 301 and 300 < self.rect.y < 360:
            self.moveD = "u"

        if self.ball_stop(self.moveD) is True and self.alive is True:
            self.check_directions()
            if len(self.directions_remain) == 0:
                self.moveD = "l"
                self.moveD = "r"
                self.moveD = "u"
                self.moveD = "d"
            else:
                rand = random.choice(self.directions_remain)
                self.moveD = rand

        if self.alive is False:
            self.check_directions()

            if self.rect.x < 190 and self.rect.y is not 300:
                if "r" in self.directions_remain:
                    self.moveD = "r"
                elif self.ball_stop(self.moveD):
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.x > 400 and self.rect.y is not 300:
                if "l" in self.directions_remain:
                    self.moveD = "l"
                elif self.ball_stop(self.moveD):
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.y < 300 and self.rect.x is not 286:
                if "d" in self.directions_remain:
                    self.moveD = "d"
                elif self.ball_stop(self.moveD):
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.y > 300 and self.rect.x is not 286:
                if "u" in self.directions_remain:
                    self.moveD = "u"
                elif self.ball_stop(self.moveD):
                    rand = random.choice(self.directions_remain)
                    self.moveD = rand

            elif self.rect.y is 300 and 190 < self.rect.x < 400:
                self.reanimate()
                if 280 < self.rect.x < 301:
                    self.moveD = "d"
                elif self.rect.x < 280:
                    self.moveD = "r"
                    # self.reanimate()
                elif self.rect.x > 301:
                    self.moveD = "l"
                    # self.reanimate()

            else:
                rand = random.choice(self.directions_remain)
                self.moveD = rand

    def ball_stop(self, m):
        if m == "l":
            temp = self.rect.move(-10, 0)
        elif m == "r":
            temp = self.rect.move(10, 0)
        elif m == "u":
            temp = self.rect.move(0, -10)
        elif m == "d":
            temp = self.rect.move(0, 10)
        else:
            temp = self.rect.move(0, 0)
        for wall in self.game.walls:
            if wall.rect.colliderect(temp):
                return True
        return False

    def check_dir(self, m):
        if m == "left":
            temp = self.rect.move(-10, 0)
        elif m == "right":
            temp = self.rect.move(10, 0)
        elif m == "up":
            temp = self.rect.move(0, -10)
        elif m == "down":
            temp = self.rect.move(0, 10)
        else:
            temp = self.rect.move(0, 0)
        for wall in self.game.walls:
            if wall.rect.colliderect(temp):
                return True
        return False

    def check_directions(self):
        self.directions_remain.clear()
        self.current_direction = "up"
        if self.check_dir(self.current_direction) is False:
            if self.moveD is not "d":
                self.directions_remain.append("u")

        self.current_direction = "down"
        if self.check_dir(self.current_direction) is False:
            if self.moveD is not "u":
                self.directions_remain.append("d")

        self.current_direction = "left"
        if self.check_dir(self.current_direction) is False:
            if self.moveD is not "r":
                self.directions_remain.append("l")

        self.current_direction = "right"
        if self.check_dir(self.current_direction) is False:
            if self.moveD is not "l":
                self.directions_remain.append("r")


class RedGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['red_ghost3r', 'red_ghost4r'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timerD = Timer(game=self.game, images=['red_ghost3d', 'red_ghost4d'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timerL = Timer(game=self.game, images=['red_ghost3l', 'red_ghost4l'], wait=wait, frameindex=0, step=1,
                            looponce=False)
        self.timerU = Timer(game=self.game, images=['red_ghost3u', 'red_ghost4u'], wait=wait, frameindex=0, step=1,
                            looponce=False)


class PinkGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['g8200', 'g3168'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerD = Timer(game=self.game, images=['g8191', 'g3139'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerL = Timer(game=self.game, images=['g8269', 'g3159'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerU = Timer(game=self.game, images=['g2727', 'g3284'], wait=wait, frameindex=0, step=1, looponce=False)


class BlueGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['g8230', 'g8357'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerD = Timer(game=self.game, images=['g8162', 'g3112'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerL = Timer(game=self.game, images=['g8240', 'g3222'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerU = Timer(game=self.game, images=['g3040', 'g6234'], wait=wait, frameindex=0, step=1, looponce=False)


class OrangeGhost(Ghost):
    def __init__(self, game, wait=100):
        super().__init__(game)

        self.timerR = Timer(game=self.game, images=['g8220', 'g8348'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerD = Timer(game=self.game, images=['g8172', 'g3121'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerL = Timer(game=self.game, images=['g8250', 'g3195'], wait=wait, frameindex=0, step=1, looponce=False)
        self.timerU = Timer(game=self.game, images=['g3027', 'g6119'], wait=wait, frameindex=0, step=1, looponce=False)


class Haunt:
    SPEED = 0

    def __init__(self, game):
        self.ghosts = pg.sprite.Group()
        self.game = game
        self.ghost_dies = pg.mixer.Sound("sounds/pacman_eatghost.wav")
        self.velocity = Haunt.SPEED * Vector(1, 0)

        self.g_color = {
            'r': RedGhost, 'p': PinkGhost, 'b': BlueGhost, 'o': OrangeGhost
        }

        self.create_ghost(self.game.ghost_start[0], 'r')
        self.create_ghost(self.game.ghost_start[2], 'p')
        self.create_ghost(self.game.ghost_start[1], 'b')
        self.create_ghost(self.game.ghost_start[3], 'o')

    def create_ghost(self, n, r):
        ghost = self.g_color[r](game=self.game)

        rect = ghost.rect
        # ghost.x = width + 2 * n * width  # controls location
        ghost.x = n[0]
        ghost.y = n[1]
        rect.x = ghost.x
        rect.y = ghost.y
        # rect.y = rect.height + 2 * height * row
        self.ghosts.add(ghost)

    def check_sides(self):
        for ghost in self.ghosts.sprites():
            if ghost.check_edges():
                self.change_ghost_direction()
                break

    def check_bottom(self):
        for ghost in self.ghosts.sprites():
            if ghost.rect.bottom > self.game.HEIGHT:
                pass
                # self.game.restart()

    def check_pacman_hit(self):
        temp = pg.sprite.spritecollideany(self.game.pacman, self.ghosts)
        if temp:
            # self.game.restart()
            if temp.rev and temp.alive:
                temp.alive = False
                pg.mixer.Sound.play(self.ghost_dies)
                temp.animation_num = 'eyes'
                self.game.score += 20  # CHANGE THIS NUMBER LATER
            elif not temp.rev:
                pg.mixer.Sound.play(self.game.pacman.pacman_dies)
                self.frozen()
                self.game.pacman.alive = False
                self.game.pacman.timer = self.game.pacman.timerPacmanDeath
                self.game.pacman.timerPacmanDeath.reset()
            return

    def change_ghost_direction(self):
        for ghost in self.ghosts.sprites():
            ghost.rect.y += self.game.GHOST_DROP
            ghost.velocity.x *= -1.1

    def frozen(self):
        for ghost in self.ghosts.sprites():
            ghost.velocity.x = 0
            ghost.velocity.y = 0

    def update(self):
        self.check_sides()
        self.check_bottom()

        if self.game.pacman.alive:
            self.check_pacman_hit()
        self.ghosts.update()

    def reverse(self):
        for ghost in self.ghosts:
            ghost.reverse()
