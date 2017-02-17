import pygame
import time
import importlib
import os
import glob

# pygame fundamentals
pygame.init()

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)
screen = pygame.display.get_surface()

pygame.display.set_caption('Gravity Guy!')

size = 50

# bob
player_img = pygame.image.load('img/aldrin.jpg')
player = pygame.transform.scale(player_img, (size, size))

# alert
def alert(msg, size, pos, color):
    font = pygame.font.SysFont(None, size)

    cont = font.render(msg, True, color)

    disp.blit(cont, pos)

def get_txt_center(msg):
    font = pygame.font.SysFont(None, size)

    cont = font.render(msg, True, (000, 000, 000))

    return cont.get_rect()

# lvl
lvl = 0
lvls = range(len(glob.glob('lvl/*.py')))

def select_lvl(i):
    global lvl

    if lvl + i in lvls:
        lvl += i

module = importlib.import_module('lvl.%d' % lvl)

prop = module.prop

def splash():
    global lvl, prop

    splash = True

    while splash:
        disp.fill((255, 255, 255))

        alert('Gravity Guy!', 100, [bounds[0] / 2 - get_txt_center('Gravity Guy!')[2], bounds[1] / 2 - 100], (000, 000, 000))

        margin = [0, 0]

        for i in lvls:
            margin[0] += size

            if i % 6 == 0:
                margin[0] = bounds[0] / 2 - 6 * size / 2
                margin[1] += size

            if i == lvl:
                pygame.draw.rect(disp, (000, 000, 000), [margin[0], bounds[1] / 2 + margin[1], size, size])

                color = (255, 255, 255)

            else:
                color = (000, 000, 000)

            alert(str(i), 30, [margin[0] + size / 2 - get_txt_center(str(i))[2] / 2, bounds[1] / 2 - 10 + size / 2 + margin[1]], color)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    select_lvl(1)

                if event.key == pygame.K_LEFT:
                    select_lvl(-1)

                if event.key == pygame.K_DOWN:
                    select_lvl(6)

                if event.key == pygame.K_UP:
                    select_lvl(-6)

                if event.key == pygame.K_RETURN:
                    module = importlib.import_module('lvl.%d' % lvl)

                    prop = module.prop

                    play('restart')

        pygame.display.update()

prev_rot = 0

target_candidates = []

def rotate(deg):
    global player, prev_rot

    player = pygame.transform.rotate(player, -prev_rot + deg)

    prev_rot = deg

pos = prop['start']['pos'][:]

def find_target(dir):
    global target, target_candidates

    if dir == 'up':
        for box in prop['boxes']:
            if box[0] == pos[0] and box[1] < pos[1]:
                target_candidates.append(box)

        sorted(target_candidates)

        if target_candidates:
            target = target_candidates[-1]

        else:
            end = True
            success = False
            menu()

    if dir == 'down':
        for box in prop['boxes']:
            if box[0] == pos[0] and box[1] > pos[1]:
                target_candidates.append(box)

        sorted(target_candidates)

        if target_candidates:
            target = target_candidates[0]

        else:
            end = True
            success = False
            menu()

    if dir == 'left':
        for box in prop['boxes']:
            if box[1] == pos[1] and box[0] < pos[0]:
                target_candidates.append(box)

        sorted(target_candidates)

        if target_candidates:
            target = target_candidates[0]

        else:
            end = True
            success = False
            menu()

    if dir == 'right':
        for box in prop['boxes']:
            if box[1] == pos[1] and box[0] > pos[0]:
                target_candidates.append(box)

        sorted(target_candidates)

        if target_candidates:
            target = target_candidates[-1]

        else:
            end = True
            success = False
            menu()

def play(status):
    global prev_rot, success, end, pos

    running = True
    end = False

    if status == 'restart':
        rotate(prop['start']['rot'])
        pos = prop['start']['pos'][:]

    while running:
        disp.fill((255, 255, 255))

        # prop
        screen.blit(player, (pos[0] * size, pos[1] * size))

        for box in prop['boxes']:
            pygame.draw.rect(disp, (000, 000, 000), [box[0] * size, box[1] * size, size, size])

        for star in prop['stars']:
            pygame.draw.rect(disp, (255, 215, 000), [star[0] * size, star[1] * size, size, size])

        pygame.draw.rect(disp, (255, 000, 000), [prop['goal'][0] * size, prop['goal'][1] * size, size, size])

        # input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                del target_candidates[:]

                if event.key == pygame.K_RIGHT:
                    find_target('right')

                    rotate(90)

                    if pos[1] == target[1] and pos[0] < target[0]:
                        v = 0

                        while pos[0] < target[0] - 1:
                            v += .0981

                            if pos[0] < target[0] - 1 - v:
                                pos[0] += v

                                disp.fill((255, 255, 255))
                                screen.blit(player, (pos[0] * size, pos[1] * size))

                                pygame.display.update()

                                time.sleep(.01)

                            else:
                                pos[0] = target[0] - 1

                    else:
                        pos[0] = bounds[0] + 1

                if event.key == pygame.K_LEFT:
                    find_target('left')

                    rotate(270)

                    if pos[1] == target[1] and pos[0] > target[0]:
                        v = 0

                        while pos[0] > target[0] + 1:
                            v += .0981

                            if pos[0] > target[0] + 1 + v:
                                pos[0] -= v

                                disp.fill((255, 255, 255))
                                screen.blit(player, (pos[0] * size, pos[1] * size))

                                pygame.display.update()

                                time.sleep(.01)

                            else:
                                pos[0] = target[0] + 1

                    else:
                        pos[0] = -1

                if event.key == pygame.K_UP:
                    find_target('up')

                    rotate(180)

                    if pos[0] == target[0] and pos[1] > target[1]:
                        v = 0

                        while pos[1] > target[1] + 1:
                            v += .0981

                            if pos[1] > target[1] + 1 + v:
                                pos[1] -= v

                                disp.fill((255, 255, 255))
                                screen.blit(player, (pos[0] * size, pos[1] * size))

                                pygame.display.update()

                                time.sleep(.01)

                            else:
                                pos[1] = target[1] + 1

                    else:
                        pos[1] = -1

                if event.key == pygame.K_DOWN:
                    find_target('down')

                    rotate(0)

                    if pos[0] == target[0] and pos[1] < target[1]:
                        v = 0

                        while pos[1] < target[1] - 1:
                            v += .0981

                            if pos[1] < target[1] - 1 - v:
                                pos[1] += v

                                disp.fill((255, 255, 255))
                                screen.blit(player, (pos[0] * size, pos[1] * size))

                                pygame.display.update()

                                time.sleep(.01)

                            else:
                                pos[1] = target[1] - 1

                    else:
                        pos[1] = bounds[1] + 1

                if event.key == pygame.K_ESCAPE:
                    menu()

            # fail
            if pos[0] < 0 or pos[0] > bounds[0] or pos[1] < 0 or pos[1] > bounds[1]:
                end = True
                success = False
                menu()

            # success
            if pos == prop['goal']:
                end = True
                success = True
                menu()

        pygame.display.update()

def menu():
    global lvl, success, prop, pos

    running = False
    show_menu = True

    while show_menu:
        pygame.draw.rect(disp, (200, 200, 200), [size / 2, size / 2, bounds[0] - size, bounds[1] - size])

        alert(str(lvl), 40, [40, 40], (255, 255, 255))
        alert('r - Restart', 40, [40, bounds[1] - 105], (255, 255, 255))
        alert('m - Menu', 40, [40, bounds[1] - 65], (255, 255, 255))

        if end:
            if success:
                alert('Well done!', 60, [bounds[0] / 2 - get_txt_center('Well done!')[2] / 2, bounds[1] / 2], (255, 255, 255))
                alert('Next level', 60, [bounds[0] / 2 - get_txt_center('Next level')[2] / 2, bounds[1] / 2 + 40], (255, 255, 255))

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            select_lvl(1)

                            module = importlib.import_module('lvl.%d' % lvl)

                            prop = module.prop

                            play('restart')

                    if event.key == pygame.K_r:
                        pos = prop['start']['pos'][:]
                        rotate(0)

                        play('restart')

                    if event.key == pygame.K_m:
                        splash()

                    pygame.display.update()

            else:
                alert('Fail :(', 60, [bounds[0] / 2 - get_txt_center('Fail :(')[2] / 2, bounds[1] / 2], (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play('resume')

                if event.key == pygame.K_r:
                    pos = prop['start']['pos'][:]
                    rotate(0)

                    play('restart')

                if event.key == pygame.K_m:
                    splash()

            pygame.display.update()

splash()

# quit
if event.type == pygame.QUIT:
    running = False
