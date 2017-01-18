import pygame

pygame.init()

pygame.display.set_caption('Gravity Guy!')

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)

pygame.display.flip()
pygame.display.update()

running = True

screen = pygame.display.get_surface()

start = {
        'x': 0,
        'y': 0
        }

boxes = [
        {
            'x': 200,
            'y': 300
            }, {
                'x': 350,
                'y': 300
                }, {
                'x': 400,
                'y': 0
                }, {
                'x': 600,
                'y': 0
                }, {
                'x': 50,
                'y': 250
                }, {
                'x': 100,
                'y': 100
                }
            ]

stars = [
        {
            'x': 250,
            'y': 350
            }, {
                'x': 450,
                'y': 350
                }
            ]

pos = start

size = 50

target_candidates = []

# player
player = pygame.image.load('img/aldrin.jpg')
player = pygame.transform.scale(player, (size, size))

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # print(pos)

            del target_candidates[:]

            if event.key == pygame.K_LEFT:
                for box in boxes:
                    if box['y'] == pos['y']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['y'] == target['y'] and pos['x'] > target['x']:
                    pos['x'] = target['x'] + size

                else:
                    pos['x'] = -size

            if event.key == pygame.K_RIGHT:
                for box in boxes:
                    if box['y'] == pos['y']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['y'] == target['y'] and pos['x'] < target['x']:
                    pos['x'] = target['x'] - size

                else:
                    pos['x'] = bounds[0] + size

            if event.key == pygame.K_UP:
                for box in boxes:
                    if box['x'] == pos['x']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['x'] == target['x'] and pos['y'] > target['y']:
                    pos['y'] = target['y'] + size

                else:
                    pos['y'] = bounds[0] - size

            if event.key == pygame.K_DOWN:
                for box in boxes:
                    if box['x'] == pos['x']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['x'] == target['x'] and pos['y'] < target['y']:
                    pos['y'] = target['y'] - size

                else:
                    pos['y'] = bounds[0] + size

        if event.type == pygame.QUIT: # quit
            running = False

    disp.fill((255, 255, 255))

    screen.blit(player, (start['x'], start['y']))

    for box in boxes:
        pygame.draw.rect(disp, (000, 000, 000), [box['x'], box['y'], size, size])

    pygame.display.update()

pygame.quit()
quit()
