import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
from vector import Vector
from ghosts1 import Haunt
from timer import Timer
from imagerect import ImageRect
from portal import Portal
from menurun import Display


class Wall(object):
    def __init__(self, pos):
        # walls.append(self)
        # self.rect = self.screen.rect
        self.rect = pg.Rect(pos[0], pos[1], 12, 12)


class Node:
    # def __init__(self, xNode, yNode, x, y):
    def __init__(self, x, y):
        # self.node = node  # string wall or node
        # self.xNode = xNode
        # self.yNode = yNode
        self.x = x
        self.y = y


class Fruit:
    def __init__(self, game, x, y):
        self.image = pg.image.load('images/fruit.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.game = game

    def update(self):
        self.game.screen.blit(self.image, self.rect)


class Laser(Sprite):
    # change to portals
    SPEED = 2
    WIDTH = 20
    HEIGHT = 20
    COLOR = (200, 0, 0)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.color = Laser.COLOR
        self.rect = pg.Rect(0, 0, Laser.WIDTH, Laser.HEIGHT)
        self.rect.midtop = self.game.pacman.rect.midtop
        self.velocity = Laser.SPEED * self.game.pacman.velocity
        # self.veolocity = Vector(0, -Laser.SPEED)
        self.y = float(self.rect.y)

    def move(self):
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.move()
        self.draw()


class Food(Sprite):
    WIDTH = 5
    HEIGHT = 5
    COLOR = (255, 255, 255)
    eaten = False
    food_type = {'dot': 5, 'power': 15}

    def __init__(self, game, t):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.color = Food.COLOR
        self.rect = pg.Rect(0, 0, self.food_type[t], self.food_type[t])
        self.rect.midtop = self.game.pacman.rect.midtop
        self.type = t

    def width(self): return self.rect.width

    def height(self): return self.rect.height

    def check_edges(self):
        r = self.rect
        s_r = self.screen.get_rect()
        return r.right >= s_r.right or r.left <= 0

    def move(self):
        pass
        # self.rect.left += self.velocity.x
        # self.rect.top += self.velocity.y

    def draw(self):
        if not self.eaten:
            pg.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        self.move()
        self.draw()


class AllFood:
    SPEED = 0

    def __init__(self, game, t='dot'):
        self.foods = pg.sprite.Group()
        self.game = game
        self.type = t
        self.pacman_eat = pg.mixer.Sound("sounds/pacman_chomp.wav")

        for dot in self.game.food_list:
            self.create_food(dot[0], dot[1])
        for power in self.game.power_list:
            self.create_power(power[0], power[1])

    def create_food(self, xpos, ypos):
        food = Food(game=self.game, t=self.type)
        rect = food.rect
        food.x = xpos
        food.y = ypos
        rect.x = food.x
        rect.y = food.y
        self.foods.add(food)

    def create_power(self, xpos, ypos):
        power = Food(game=self.game, t='power')
        rect = power.rect
        power.x = xpos
        power.y = ypos
        rect.x = power.x
        rect.y = power.y
        self.foods.add(power)

    def check_pacman_hit(self):
        temp = pg.sprite.spritecollideany(self.game.pacman, self.foods)
        if temp:
            pg.mixer.Sound.play(self.pacman_eat)
            if temp.type == 'power':
                self.game.reverse_game_play()
                self.game.score += 40
                self.game.reverse_game = True
            self.foods.remove(temp)
            self.game.score += 10
            return

    # currently doesn't work
    def check_empty(self):
        if len(self.foods) == 0:
            # reload dots and increase speed
            self.game.nextlevel()

    def update(self):
        self.check_pacman_hit()
        self.foods.update()
        # if self.game.score > 2000:
        self.check_empty()


class Pacman:
    def __init__(self, game, vector=Vector()):
        self.game = game
        self.screen = game.screen
        self.velocity = vector
        self.next = self.velocity
        self.alive = True
        self.death_animation = 1
        self.screen_rect = game.screen.get_rect()
        # self.image = pg.image.load('/images/pacman_solid.png')
        self.image = (ImageRect(self.screen, 'pacman_solid', height=25, width=25))
        self.x = self.game.pacman_start[0]
        self.y = self.game.pacman_start[1]
        self.rect = self.image.image.get_rect()
        # self.rect.center = (self.x, self.y)
        self.rect.x = self.x
        self.rect.y = self.y
        # self.rect.midbottom = self.screen_rect.midbottom
        self.current_direction = 'right'  # up, down, left, right, none
        self.current_node = game.start_node
        self.next_node = game.start_node
        self.animation_num = 1  # 4 different animations
        self.pacman_animations = {
            1: 'pacman1.png', 2: 'pacman2.png', 3: 'pacman3.png', 4: 'pacman4.png'
        }
        self.p_animations = ['pacman1', 'pacman2', 'pacman3', 'pacman4']
        self.pacman_direction = {
            'left': 0, 'down': 90, 'right': 180, 'up': 270
        }
        # self.next_direction =
        self.animation_time = 0
        self.d_images = {
            1: 'pacman_solid.png', 2: 'pd2.png', 3: 'pacman1.png', 4: 'pd4.png', 5: 'pacman2.png', 6: 'pd6.png',
            7: 'pacman3.png',
            8: 'pacman4.png', 9: 'pd9.png', 10: 'pd10.png', 11: 'pd11.png', 12: 'pd12.png', 13: 'pd13.png',
            14: 'pd14.png',
            15: 'pd15.png', 16: 'pd16.png'
        }
        self.pacman_death_animation = ['pacman_solid', 'pd2', 'pacman1', 'pd4', 'pacman2', 'pd6', 'pacman3',
                                       'pacman4', 'pd9', 'pd10', 'pd11', 'pd12', 'pd13', 'pd14', 'pd15', 'pd16']
        # print(self.rect)
        self.center()
        self.wait = 100
        self.timerPacman = Timer(game=self.game, images=self.p_animations, wait=self.wait, frameindex=0, step=1,
                                 looponce=False)
        self.timerPacmanDeath = Timer(game=self.game, images=self.pacman_death_animation, wait=self.wait, frameindex=0,
                                      step=1, looponce=True)
        self.pacman_dies = pg.mixer.Sound("sounds/pacman_death.wav")
        self.timer = self.timerPacman
        # self.lasers = pg.sprite.Group()
        self.laser = None

    def __repr__(self):
        r = self.rect
        return 'Pacman({},{}),v={}'.format(r.x, r.y, self.velocity)

    # fire to create portal
    def fire(self):
        if len(self.game.portals) > 1 and not self.game.portals[0].isclosed:
            self.game.pacman.close_portals()
        elif self.laser is None:
            self.laser = Laser(game=self.game)
        else:
            self.laser = None

    # def remove_foods(self):
    #     self.allfoods.remove()

    # puts pacman at his starting position
    def center(self):
        self.rect.centerx = self.game.pacman_start[0]
        self.rect.centery = self.game.pacman_start[1] + 10

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    def draw(self):
        temp_image = self.timer.imagerect()
        temp_image = pg.transform.rotate(temp_image.image, self.pacman_direction[self.current_direction])
        self.screen.blit(temp_image, self.rect)

    def move(self):
        if self.next == Vector():
            # or self.check_node():
            return

        bridge = pg.sprite.spritecollide(self, self.game.bridge, False)
        if bridge:
            if self.rect.x < 100:
                other = self.game.bridge[1]
                self.rect.center = (other.rect.centerx - 26, other.rect.centery)
            else:
                other = self.game.bridge[0]
                self.rect.center = (other.rect.centerx + 26, other.rect.centery)

        self.rect.left += self.next.x
        self.rect.top += self.next.y
        self.game.limit_on_screen(self.rect)

        # Did this update cause us to hit a wall?
        # FIX THIS LATER
        wall_hit_list = pg.sprite.spritecollide(self, self.game.walls, False)

        if len(wall_hit_list) > 0:
            # print("collision")
            self.rect.left -= self.next.x
            self.rect.top -= self.next.y

            self.rect.left += self.velocity.x
            self.rect.top += self.velocity.y
            self.game.limit_on_screen(self.rect)
            wall_hit_list = pg.sprite.spritecollide(self, self.game.walls, False)
            if len(wall_hit_list) > 0:
                # print("collision")
                self.rect.left -= self.velocity.x
                self.rect.top -= self.velocity.y
        elif self.velocity != self.next:
            self.velocity = self.next

        if self.velocity.x != 0:
            if self.velocity.x > 0:
                self.current_direction = 'right'
            else:
                self.current_direction = 'left'
        elif self.velocity.y != 0:
            if self.velocity.y > 0:
                self.current_direction = 'down'
            else:
                self.current_direction = 'up'

    def death(self):
        if self.timerPacmanDeath.frameindex == self.timerPacmanDeath.lastframe:
            self.game.restart()
            return
        temp_image = self.timer.imagerect()
        temp_image = pg.transform.rotate(temp_image.image, self.pacman_direction[self.current_direction])
        self.screen.blit(temp_image, self.rect)
        # pg.mixer.Sound.play(self.pacman_dies)

    def restart(self):
        self.center()
        self.alive = True
        self.timer = self.timerPacman
        self.timerPacmanDeath.reset()

    def update(self):

        if not self.alive:
            self.death()
        else:
            self.move()
            self.draw()
            if self.laser is not None:
                self.laser.update()
                self.check_hit()
            if len(self.game.portals) > 1 and not (self.game.portals[0].isclosed and
                                                   self.game.portals[0].timerclosing.frame_index() == 0):
                self.game.portals[0].draw()
                self.game.portals[1].draw()
                portal = pg.sprite.spritecollideany(self, self.game.portals)
                if portal:
                    if portal.attempt_transport(self, self.game):
                        self.close_portals()

    def check_hit(self):
        wall = pg.sprite.spritecollideany(self.laser, self.game.walls)
        if wall:
            self.create_portals()
            # remove laser
            self.laser = None

    def create_portals(self):
        x1 = self.laser.rect.centerx - (self.laser.velocity.x * 13)
        y1 = self.laser.rect.centery - (self.laser.velocity.y * 13)
        x2, y2 = self.game.WIDTH - x1 - 2, y1 + 2
        # create portals and open
        self.game.portals = [Portal(self.game, x1, y1, ['g5452', 'g5520', 'g5627', 'g5402-4']),
                             Portal(self.game, x2, y2, ['g5452', 'g5520', 'g5627', 'g5402-4'])]
        for p in self.game.portals:
            if not p.isopen:
                p.open(self.game)
        self.game.portals[0].draw()
        self.game.portals[1].draw()

    def close_portals(self):
        for p in self.game.portals:
            if p.isopen:
                p.close()

    def nearest_node(self):
        temp = pg.sprite.spritecollideany(self, self.game.allfoods.foods)
        if temp:
            self.rect.x = temp.x
            self.rect.y = temp.y


class Game:
    SHIP_SPEED = 5
    PACMAN_SPEED = 1
    WIDTH = 598
    HEIGHT = 705
    SHIPS = 3
    GHOST_DROP = 10

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Game.WIDTH, Game.HEIGHT))
        pg.display.set_caption('Pacman')
        self.back_music = pg.mixer.Sound("sounds/pacman_beginning.wav")
        self.menu = Display(self)

        self.nodes = []  # nodes for game (node/wall, x, y)
        self.walls = []
        self.food_list = []
        self.power_list = []
        self.ghost_start = []
        self.pacman_start = (0, 0)
        self.start_node = ()
        self.bridge = []
        self.fruit = None
        self.create_walls()

        self.bg_color = (40, 40, 40)  # dark grey
        self.finished: bool = False
        self.pacmans_left = 3
        self.pacman = Pacman(self)
        self.reverse_game = False  # used when pacman eats power, ghosts flash

        self.allfoods = AllFood(self, t='dot')
        self.score = 0
        self.haunt = Haunt(self)
        self.portals = []

        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.score_text = self.font.render('Score: ', True, (255, 255, 255), (40, 40, 40))
        self.textRect1 = self.score_text.get_rect()
        self.textRect1.midleft = (10, 20)
        self.score_text2 = self.font.render('0', True, (255, 255, 255), (40, 40, 40))
        self.textRect2 = self.score_text2.get_rect()
        self.textRect2.midleft = (150, 20)
        self.lives_text = self.font.render('Lives: ', True, (255, 255, 255), (40, 40, 40))
        self.textRect3 = self.score_text.get_rect()
        self.textRect3.midleft = (400, 20)
        self.lives_text2 = self.font.render('3', True, (255, 255, 255), (40, 40, 40))
        self.textRect4 = self.score_text2.get_rect()
        self.textRect4.midleft = (540, 20)
        self.font2 = pg.font.Font('freesansbold.ttf', 75)
        self.gameover_text = self.font2.render('GAME OVER', True, (255, 255, 255), (40, 40, 40))
        self.gameoverRect = self.gameover_text.get_rect()
        self.gameoverRect.midleft = (75, 400)

        self.start_time = pg.time.get_ticks()

    def limit_on_screen(self, rect):
        rect.left = max(0, rect.left)
        rect.right = min(rect.right, self.WIDTH)
        rect.top = max(0, rect.top)
        rect.bottom = min(rect.bottom, self.HEIGHT)

    def process_events(self):
        key_up_down = [pg.KEYDOWN, pg.KEYUP]
        movement = {K_RIGHT: Vector(1, 0), K_LEFT: Vector(-1, 0), K_UP: Vector(0, -1), K_DOWN: Vector(0, 1)}
        translate = {K_d: K_RIGHT, K_a: K_LEFT, K_w: K_UP, K_s: K_DOWN}
        for event in pg.event.get():
            e_type = event.type
            if e_type in key_up_down:
                k = event.key
                if k in translate.keys() or k in translate.values():  # movement
                    if k in translate.keys():
                        k = translate[k]
                    # self.ship.velocity = Game.SHIP_SPEED * movement[k]
                    self.pacman.next = Game.PACMAN_SPEED * movement[k]
                elif k == pg.K_SPACE and e_type == pg.KEYDOWN:  # shoot laser
                    # self.pacman.portal()
                    self.pacman.fire()
                    # for p in self.portals:
                    # p.open(self) if p.isclosed else p.close()
                    # return
            elif e_type == QUIT:  # quit
                self.finished = True

    def process_intro_events(self):
        for event in pg.event.get():
            e_type = event.type
            if e_type == QUIT:  # quit
                self.finished = True
            elif e_type == pg.MOUSEBUTTONDOWN:
                self.menu.button_clicks()

    def create_walls(self):
        size = 13
        # self.walls = []  # List to hold the walls
        # Holds the level layout in a list of strings.
        level = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X                     XX                     X",
            "X N N N N N N N N N N XX N N N N N N N N N N X",
            "X                     XX                     X",
            "X N XXXXX N XXXXXXX N XX N XXXXXXX N XXXXX N X",
            "X   XXXXX   XXXXXXX   XX   XXXXXXX   XXXXX   X",
            "X P XXXXX N XXXXXXX N XX N XXXXXXX N XXXXX P X",
            "X                     XX                     X",
            "X N N N N N N N N N N XX N N N N N N N N N N X",
            "X                     XX                     X",
            "X N XXXXX N XX N XXXXXXXXXXXX N XX N XXXXX N X",
            "X   XXXXX   XX   XXXXXXXXXXXX   XX   XXXXX   X",
            "X N XXXXX N XX N XXXXXXXXXXXX N XX N XXXXX N X",
            "X           XX        XX        XX           X",
            "X N N N N N XX N N N  XX  N N N XX N N N N N X",
            "X           XX        XX        XX           X",
            "XXXXXXXXX N XXXXXXX   XX   XXXXXXX N XXXXXXXXX",
            "        X   XXXXXXX   XX   XXXXXXX   X        ",
            "        X   XX                  XX   X        ",
            "        X N XX n n n n  n n n n XX N X        ",
            "        X   XX                  XX   X        ",
            "        X N XX n XXXX G  XXXX n XX N X        ",
            "XXXXXXXXX   XX   X          X   XX   XXXXXXXXX",
            "          N    n X          X n    N          ",
            "B      F         X G  G  G  X                B",
            "          N    n X          X n    N          ",
            "XXXXXXXXX   XX   X          X   XX   XXXXXXXXX",
            "        X N XX n XXXXXXXXXXXX n XX N X        ",
            "        X   XX                  XX   X        ",
            "        X N XX n n n n Sn n n n XX N X        ",
            "        X   XX                  XX   X        ",
            "        X N XX n XXXXXXXXXXXX n XX N X        ",
            "XXXXXXXXX   XX   XXXXXXXXXXXX   XX   XXXXXXXXX",
            "X                     XX                     X",
            "X N N N N N N N N N N XX N N N N N N N N N N X",
            "X                     XX                     X",
            "X N XXXXX N XXXXXXX N XX N XXXXXXX N XXXXX N X",
            "X   XXXXX   XXXXXXX   XX   XXXXXXX   XXXXX   X",
            "X      XX                            XX      X",
            "X P N  XX N N N N N N N  N N N N N N XX  N P X",
            "X      XX                            XX      X",
            "XXXX N XX N XX N XXXXXXXXXXXX N XX N XX N XXXX",
            "XXXX   XX   XX   XXXXXXXXXXXX   XX   XX   XXXX",
            "X           XX        XX        XX           X",
            "X N N N N N XX N N N  XX  N N N XX N N N N N X",
            "X           XX        XX        XX           X",
            "X N XXXXXXXXXXXXXXX N XX N XXXXXXXXXXXXXXX N X",
            "X                                            X",
            "X N N N N N N N N N N N  N N N N N N N N N N X",
            "X                                            X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]

        # Parse the level string above. X = wall, space = exit
        nodesrow = {}
        r, c = 0, 0
        x, y = 0, 40
        for row in level:
            for col in row:
                if col == "X":
                    # Wall(x, y)
                    temp = Wall((x, y))
                    self.walls.append(temp)
                    # nodesrow[c] = Node(r, c, x, y)
                elif col == "N":  # node/food
                    self.food_list.append((x, y))
                    # nodesrow[c] = Node(r, c, x, y)
                    # c += 1
                    self.nodes.append(Node(x, y))
                    # end_rect = pg.Rect(x, y, 16, 16)
                elif col == "G":  # ghost start
                    self.ghost_start.append((x, y))
                    # nodesrow[c] = Node(r, c, x, y)
                    self.nodes.append(Node(x, y))
                    # c += 1
                elif col == "P":  # node/power
                    # self.food_list.append((x, y))
                    self.power_list.append((x, y))
                    # nodesrow[c] = Node(r, c, x, y)
                    # c += 1
                elif col == "S":  # pacman start spot
                    self.pacman_start = (x, y)
                    self.start_node = Node(x, y)
                    self.nodes.append(Node(x, y))
                    # self.start_node = Node(r, c, x, y)
                    # nodesrow[c] = Node(r, c, x, y)
                    # c += 1
                elif col == "n":  # node
                    self.nodes.append(Node(x, y))
                    # nodesrow[c] = Node(r, c, x, y)
                    # c += 1
                elif col == "B":  # bridge to other side
                    self.bridge.append(Wall((x, y)))
                elif col == "F":  # fruit
                    self.fruit = Fruit(self, x, y)
                    # self.fruit = ImageRect(self.screen, 'fruit', height=size, width=size)
                    # self.fruit.x = x
                    # self.fruit.y = y
                x += size
                # c += 1
            y += size
            x = 0
            if nodesrow != {}:
                self.nodes[r] = nodesrow
                r += 1
            nodesrow = {}
            # c = 0

    def restart(self):

        self.pacmans_left -= 1
        # 2 lives left, 1 life left
        # print('{} li{} left'.format(self.pacmans_left, "ves" if self.pacmans_left > 1 else "fe"))
        if self.pacmans_left == 0:
            self.game_over()

        # self.pacman.center()
        # self.pacman.alive = True
        self.pacman.restart()
        self.portals = []
        self.pacman.laser = None

        self.haunt = Haunt(self)
        # NEED TO RESTART GHOSTS

    def reverse_game_play(self):
        self.reverse_game = True
        self.haunt.reverse()

    def game_over(self):
        # print("GAME OVER.")
        # quit()
        self.finished = True
        self.screen.blit(self.gameover_text, self.gameoverRect)

    def nextlevel(self):
        self.allfoods = AllFood(self, t='dot')
        self.pacman.restart()
        self.portals = []
        self.pacman.laser = None
        self.haunt = Haunt(self)
        for ghost in self.haunt.ghosts.sprites():
            ghost.SPEED = 1.5

    def update(self):
        self.screen.fill(self.bg_color)

        for wall in self.walls:
            pg.draw.rect(self.screen, (0, 0, 255), wall.rect)

        self.pacman.update()
        self.allfoods.update()
        self.haunt.update()
        self.update_values()

        # if pg.time.get_ticks() - self.start_time > 10:
        # self.fruit.update()

    def update_values(self):
        self.screen.blit(self.score_text, self.textRect1)
        self.score_text2 = self.font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(self.score_text2, self.textRect2)
        self.screen.blit(self.lives_text, self.textRect3)
        self.lives_text2 = self.font.render(str(self.pacmans_left), True, (255, 255, 255))
        self.screen.blit(self.lives_text2, self.textRect4)

    def play(self):
        pg.mixer.Sound.play(self.back_music)
        while self.menu.viewMenu:
            self.menu.draw()
            self.process_intro_events()
            pg.display.update()
        while not self.finished:
            self.process_events()
            self.update()
            pg.display.update()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
