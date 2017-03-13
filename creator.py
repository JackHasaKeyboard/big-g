import pygame
import glob
import re

import importlib
from glob import glob as glob
import os

import sys

# pygame fundamentals
pygame.init()

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)
screen = pygame.display.get_surface()

pygame.display.set_caption('Gravity Guy Level Creator')

size = 50

# img
img = {}

for path in glob('img/*'):
    rel = os.path.splitext(os.path.basename(path))[0]

    img[str(rel)] = pygame.transform.scale(pygame.image.load(path), (size, size))

# alert
def alert(msg, font, size, pos, color):
    font = pygame.font.SysFont(None, size)

    cont = font.render(str(msg), True, color)

    disp.blit(cont, pos)

# lvl
if len(sys.argv) > 1:
    lvl = int(sys.argv[1])

    module = importlib.import_module('lvl.%d' % lvl)
    prop = module.prop

else:
    lvl = len(re.findall('\d+\.py', str(glob('lvl/*'))))

    prop = {
            'start': {
                'pos': [
                    0,
                    0
                    ],
                'rot': 0
                },
            'boxes': [],
            'stars': [],
            'goal': [
                0, 
                0
                ]
            }

pos = prop['start']['pos'][:]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pos[0] += 1

            if event.key == pygame.K_LEFT:
                pos[0] -= 1

            if event.key == pygame.K_UP:
                pos[1] -= 1

            if event.key == pygame.K_DOWN:
                pos[1] += 1

            if event.key == pygame.K_p:
                prop['start']['pos'] = pos[:]

            if event.key == pygame.K_b:
                prop['boxes'].append(pos[:])

            if event.key == pygame.K_s:
                prop['stars'].append(pos[:])

            if event.key == pygame.K_g:
                prop['goal'] = pos[:]

            # clear
            if event.key == pygame.K_c:
                for prop_type in prop:
                    for item in prop[prop_type]:
                        if pos == item:
                            prop[prop_type].remove(item)

            # write
            if event.key == pygame.K_w:
                f = open('lvl/%d.py' % lvl, 'w+')

                f.write('prop = ' + str(prop))

                f.close()

        disp.fill((255, 255, 255))

        alert(str(lvl), pygame.font.SysFont("AG Stencil", size), 160, [size, size], (225, 225, 225))

        for n in range(2):
            margin = [0, 0]

            for i in range(bounds[n] / size):
                alert(i, pygame.font.SysFont(None, size), 20, margin, (255, 000, 000))

                margin[n] += 50

        screen.blit(img['bob'], (prop['start']['pos'][0] * size, prop['start']['pos'][1] * size))

        for box in prop['boxes']:
            screen.blit(img['box'], (box[0] * size, box[1] * size))

        for star in prop['stars']:
            screen.blit(img['star'], (star[0] * size, star[1] * size))

        screen.blit(img['goal'], (prop['goal'][0] * size, prop['goal'][1] * size))

        # cursor
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size, pos[1] * size, 10, 10])
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size + 40, pos[1] * size, 10, 10])
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size, pos[1] * size + 40, 10, 10])
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size + 40, pos[1] * size + 40, 10, 10])

        alert(pos, pygame.font.SysFont(None, size), 20, [pos[0] * 50, pos[1] * 50 + 10], (000, 000, 000))

        pygame.display.update()
