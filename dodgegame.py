import pygame, time, random

winwidth = 1600
winheight = 1000
playerx = 300
playery = 400
laserx = 800
lasery = -100
laserINDCx = 800
laserINDCy = 0
Vertlaserx = -100
Vertlasery = 500
VertlaserINDCx = 800
lasermove = 0
deathstate = 0
laseractivate = 0
difficulty = 1.2

class Player(pygame.sprite.Sprite):

    def __init__(self, speed, color):
        super().__init__()
        self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
        pygame.draw.rect(self.image, 'purple', self.image.get_rect())
        self.rect = self.image.get_rect()

        self.pos = pygame.Vector2(playerx, playery)
        self.target = pygame.Vector2(playerx, playery)
        self.speed = speed

    def update(self):
        move = self.target - self.pos
        move_length = move.length()

        if move_length != 0:
            move.normalize_ip()
            move = move * min(move_length, self.speed)
            self.pos += move

        self.rect.center = self.pos

class LaserINDC(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((winwidth, 100), pygame.SRCALPHA)
        self.image.fill(pygame.Color(255, 0, 0, 50))
        self.rect = self.image.get_rect(center=(laserINDCx, laserINDCy))

class Laser(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((winwidth, 100), pygame.SRCALPHA)
        self.image.fill(pygame.Color(255, 0, 0, 255))
        self.rect = self.image.get_rect(center=(laserx, lasery))

class VertLaserINDC(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, winheight), pygame.SRCALPHA)
        self.image.fill(pygame.Color(255, 0, 0, 50))
        self.rect = self.image.get_rect(center=(VertlaserINDCx, Vertlasery))

class VertLaser(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, winheight), pygame.SRCALPHA)
        self.image.fill(pygame.Color(255, 0, 0, 255))
        self.rect = self.image.get_rect(center=(Vertlaserx, Vertlasery))

def main():
    pygame.init()
    global lasery
    global laserINDCy
    global Vertlaserx
    global VertlaserINDCx
    global deathstate
    global lasermove
    global laseractivate
    global difficulty

    screen = pygame.display.set_mode((winwidth, winheight), pygame.SRCALPHA)
    pygame.display.set_caption("League Of Legends")

    clock = pygame.time.Clock()
    start_time = time.time()

    player = pygame.sprite.Group(Player(6, pygame.Color(255, 0, 0, 255)))

    laser = Laser()
    laser_group = pygame.sprite.Group()
    laser_group.add(laser)

    laserINDC = LaserINDC()
    laserINDC_group = pygame.sprite.Group()
    laserINDC_group.add(laserINDC)

    VertlaserINDC = VertLaserINDC()
    VertlaserINDC_group = pygame.sprite.Group()
    VertlaserINDC_group.add(VertlaserINDC)

    Vertlaser = VertLaser()
    Vertlaser_group = pygame.sprite.Group()
    Vertlaser_group.add(Vertlaser)

    running = True
    while running:

        time_alive = time.time()
        time_difference = time_alive - start_time
        # font = pygame.font.SysFont("Arial", 60, False, False)
        # font_image = font.render(str(round(time_difference, 2)), True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for movement in player.sprites():
                    movement.target = pygame.mouse.get_pos()

        if pygame.sprite.groupcollide(player, laser_group, True, True):
            player = pygame.sprite.Group(
                Player(6, pygame.Color(160, 32, 240, 255)))
            laser = Laser()
            laser_group = pygame.sprite.Group()
            laser_group.add(laser)
            start_time = time_alive
            deathstate += 1

        if pygame.sprite.groupcollide(player, Vertlaser_group, True, True):
            player = pygame.sprite.Group(
            Player(6, pygame.Color(160, 32, 240, 255)))
            Vertlaser = VertLaser()
            Vertlaser_group = pygame.sprite.Group()
            Vertlaser_group.add(Vertlaser)
            start_time = time_alive
            deathstate += 1

        if time_difference >= 0.5 and time_difference <= 0.55:
            lasermove = random.randint(1, 2)
            laseractivate = 1

        if time_difference >= difficulty:
            laseractivate = 2

        if lasermove == 1 and laseractivate == 1:
            laserINDCy = random.randint(0, 1000)
            laserINDC = LaserINDC()
            laserINDC_group = pygame.sprite.Group()
            laserINDC_group.add(laserINDC)
            lasery = laserINDCy
            lasermove = 0

        if lasermove == 1 and laseractivate == 2:
            lasery = laserINDCy
            laserINDC = LaserINDC()
            laserINDC_group = pygame.sprite.Group()
            laserINDC_group.add(laserINDC)
            lasery = laserINDCy
            start_time = time_alive
            lasermove = 0

        if laseractivate == 2:
            VertlaserINDCx = random.randint(0, 1000)
            laser = Laser()
            laser_group = pygame.sprite.Group()
            laser_group.add(laser)
            start_time = time_alive
            laseractivate = 0
            lasermove = 0

        if deathstate >= 3:
            deathstate -= 3
            lasery = random.randint(0, 1000)
            Vertlaserx = random.randint(0, 1000)
            start_time = time_alive
            laser = Laser()
            laser_group = pygame.sprite.Group()
            laser_group.add(laser)
            Vertlaser = VertLaser()
            Vertlaser_group = pygame.sprite.Group()
            Vertlaser_group.add(Vertlaser)

        player.update()
        screen.fill('dark green')
        player.draw(screen)
        laser_group.draw(screen)
        laserINDC_group.draw(screen)
        Vertlaser_group.draw(screen)
        VertlaserINDC_group.draw(screen)
        # screen.blit(font_image, [winwidth // 2 - 60, 100])
        pygame.display.flip()
        clock.tick(60)

        print(lasery)

    pygame.quit()


if __name__ == "__main__":
    main()
