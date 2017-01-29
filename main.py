import pygame

# pygame fundamentals
pygame.init()

pygame.display.set_caption('Gravity Guy!')

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)

pygame.display.flip()
pygame.display.update()

running = True

screen = pygame.display.get_surface()

start = {
        'x': 100,
        'y': 50
        }

boxes = [
        {
            'x': 50,
            'y': 300
            }, {
                'x': 350,
                'y': 300
                }, {
                    'x': 400,
                    'y': 50
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
            'x': 400,
            'y': 400
            }, {
                'x': 500,
                'y': 500
                }
            ]

goal = {
        'x': 100,
        'y': 150
        }

pos = start

size = 50

target_candidates = []

# player
player = pygame.image.load('img/aldrin.jpg')
player = pygame.transform.scale(player, (size, size))

# alert
font = pygame.font.SysFont(None, 25)

def alert(msg):
    text = font.render(msg, True, (000, 000, 000))

    disp.blit(text, [bounds[0] / 2, bounds[1] / 2])

def rotate(deg):
    return(pygame.transform.rotate(player, deg))

while running:
    # background
    disp.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            del target_candidates[:]

            if event.key == pygame.K_LEFT:
                deg = 270

                for box in boxes:
                    if box['y'] == pos['y']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['y'] == target['y'] and pos['x'] > target['x']:
                    pos['x'] = target['x'] + size

                else:
                    pos['x'] = -size

            if event.key == pygame.K_RIGHT:
                deg = 90

                for box in boxes:
                    if box['y'] == pos['y']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['y'] == target['y'] and pos['x'] < target['x']:
                    pos['x'] = target['x'] - size

                else:
                    pos['x'] = bounds[0] + size

            if event.key == pygame.K_UP:
                deg = 180

                for box in boxes:
                    if box['x'] == pos['x']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['x'] == target['x'] and pos['y'] > target['y']:
                    pos['y'] = target['y'] + size

                else:
                    pos['y'] = bounds[0] - size

            if event.key == pygame.K_DOWN:
                deg = 0

                for box in boxes:
                    if box['x'] == pos['x']:
                        target_candidates.append(box)

                target = target_candidates[0]

                if pos['x'] == target['x'] and pos['y'] < target['y']:
                    pos['y'] = target['y'] - size

                else:
                    pos['y'] = bounds[0] + size

            player = rotate(deg)
        
        # out of bounds
        if pos['x'] < 0 or pos['x'] > bounds[0] or pos['y'] < 0 or pos['y'] > bounds[1]:
            running = False

        # success
        if pos == goal:
            alert('Well done!')
            alert('Next level')

        if event.type == pygame.QUIT: # quit
            running = False

    lvls = [0, 1, 2, 3]

    # prop
    if running == True:
        screen.blit(player, (start['x'], start['y']))

        for box in boxes:
            pygame.draw.rect(disp, (000, 000, 000), [box['x'], box['y'], size, size])

        for star in stars:
            pygame.draw.rect(disp, (255, 215, 000), [star['x'], star['y'], size, size])

        pygame.draw.rect(disp, (255, 0, 0), [goal['x'], goal['y'], size, size])

    else:
        alert("Gravity Guy!")

        # levels
        margin = 0

        for lvl in lvls:
            text = font.render(str(lvl), True, (000, 000, 000))
            disp.blit(text, [bounds[0] / 2 + margin, bounds[1] / 2 + 60])

            margin += 20

    pygame.display.update()

pygame.quit()
quit()
