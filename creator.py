import pygame
import glob

# pygame fundamentals
pygame.init()

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)
screen = pygame.display.get_surface()

pygame.display.set_caption('Gravity Guy Level Creator')

size = 50

# bob
player_img = pygame.image.load('img/aldrin.jpg')
player = pygame.transform.scale(player_img, (size, size))

# alert
def alert(msg, size, pos, color):
    font = pygame.font.SysFont(None, size)

    cont = font.render(str(msg), True, color)

    disp.blit(cont, pos)

prop = {
        'start': {
            'pos': [
                -1,
                -1
                ],
            'rot': 0
            },
        'boxes': [],
        'stars': [],
        'goal': [-1, -1]
        }

pos = prop['start']['pos']

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
                lvls = len(glob.glob('lvl/*.py')) + 1

                f = open('lvl/%d.py' % lvls, 'a+')

                f.write('prop = ' + str(prop))

                f.close()

        disp.fill((255, 255, 255))

        for n in range(2):
            margin = [0, 0]

            for i in range(bounds[n] / size):
                alert(i, 20, margin, (255, 000, 000))

                margin[n] += 50

        screen.blit(player, (prop['start']['pos'][0] * size, prop['start']['pos'][1] * size))

        for box in prop['boxes']:
            pygame.draw.rect(disp, (000, 000, 000), [box[0] * size, box[1] * size, size, size])

        for star in prop['stars']:
            pygame.draw.rect(disp, (255, 215, 000), [star[0] * size, star[1] * size, size, size])

        pygame.draw.rect(disp, (255, 000, 000), [prop['goal'][0] * size, prop['goal'][1] * size, size, size])

        # cursor
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size, pos[1] * size, 10, 10])
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size + 40, pos[1] * size, 10, 10])
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size, pos[1] * size + 40, 10, 10])
        pygame.draw.rect(disp, (000, 000, 255), [pos[0] * size + 40, pos[1] * size + 40, 10, 10])

        alert(pos, 20, [pos[0] * 50, pos[1] * 50 + 10], (000, 000, 000))

        pygame.display.update()
