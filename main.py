import pygame

# pygame fundamentals
pygame.init()

pygame.display.set_caption('Gravity Guy!')

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)
screen = pygame.display.get_surface()

lvls = [range(5)]
lvl = 0

size = 50

margin = 0

# player
player_img = pygame.image.load('img/aldrin.jpg')
player = pygame.transform.scale(player_img, (size, size))

# alert
def alert(msg, size, pos):
    font = pygame.font.SysFont(None, size)

    cont = font.render(msg, True, (000, 000, 000))

    disp.blit(cont, pos)

# prop
start = {
        'x': 100,
        'y': 50
        }

boxes = [
        [
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

def splash():
    global lvl

    splash = True
    running = False

    while splash:
        disp.fill((255, 255, 255))

        alert('Gravity Guy!', 100, [bounds[0] / 2, bounds[1] / 2 - 100])

        for alvl in lvls:
            alert(str(alvl), 60, [bounds[0] / 2, bounds[1] / 2])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    lvl += 1

                    if lvl > len(lvls):
                        lvl = len(lvls)

                if event.key == pygame.K_LEFT:
                    lvl -= 1

                    if lvl < 0:
                        lvl = 0

                if event.key == pygame.K_DOWN:
                    lvl += 4

                    if lvl > len(lvls):
                        lvl = len(lvls)

                if event.key == pygame.K_UP:
                    lvl -= 4

                    if lvl < 0:
                        lvl = 0

                if event.key == pygame.K_RETURN:
                    play()

                alert(str(lvl), 40, [0, 0])

        pygame.display.update()

prev_rot = 0

target_candidates = []

success = False

def play():
    global player, running, prev_rot, success

    splash = False
    running = True

    while running:
        # background
        disp.fill((255, 255, 255))

        for event in pygame.event.get():
            #input
            if event.type == pygame.KEYDOWN:
                del target_candidates[:]

                if event.key == pygame.K_LEFT:
                    deg = 270

                    for box in boxes[lvl]:
                        if box['y'] == pos['y']:
                            target_candidates.append(box)

                    target = target_candidates[0]

                    if pos['y'] == target['y'] and pos['x'] > target['x']:
                        pos['x'] = target['x'] + size

                    else:
                        pos['x'] = -size

                if event.key == pygame.K_RIGHT:
                    deg = 90

                    for box in boxes[lvl]:
                        if box['y'] == pos['y']:
                            target_candidates.append(box)

                    target = target_candidates[0]

                    if pos['y'] == target['y'] and pos['x'] < target['x']:
                        pos['x'] = target['x'] - size

                    else:
                        pos['x'] = bounds[0] + size

                if event.key == pygame.K_UP:
                    deg = 180

                    for box in boxes[lvl]:
                        if box['x'] == pos['x']:
                            target_candidates.append(box)

                    target = target_candidates[0]

                    if pos['x'] == target['x'] and pos['y'] > target['y']:
                        pos['y'] = target['y'] + size

                    else:
                        pos['y'] = bounds[0] - size

                if event.key == pygame.K_DOWN:
                    deg = 0

                    for box in boxes[lvl]:
                        if box['x'] == pos['x']:
                            target_candidates.append(box)

                    target = target_candidates[0]

                    if pos['x'] == target['x'] and pos['y'] < target['y']:
                        pos['y'] = target['y'] - size

                    else:
                        pos['y'] = bounds[0] + size

                if event.key == pygame.K_ESCAPE:
                    alert('Menu', 20, [0, 0])

                player = pygame.transform.rotate(player, -prev_rot + deg)

                prev_rot = deg
            
            # fail
            if pos['x'] < 0 or pos['x'] > bounds[0] or pos['y'] < 0 or pos['y'] > bounds[1]:
                success = False
                menu()

            # success
            if pos == goal:
                success = True
                menu()

        # prop
        screen.blit(player, (start['x'], start['y']))

        for box in boxes[lvl]:
            pygame.draw.rect(disp, (000, 000, 000), [box['x'], box['y'], size, size])

        for star in stars:
            pygame.draw.rect(disp, (255, 215, 000), [star['x'], star['y'], size, size])

        pygame.draw.rect(disp, (255, 0, 0), [goal['x'], goal['y'], size, size])

        pygame.display.update()

def menu():
    global success, lvl

    running = False
    menu = True

    while menu:
        disp.fill((255, 255, 255))

        if success == True:
            msg = 'Well done!'
            alert('Next level', 60, [bounds[0] / 2, bounds[1] / 2 + 40])

        else:
            msg = 'Fail :('
            alert('Menu', 40, [16, bounds[1] - 40])
            alert('Restart', 40, [16, bounds[1]])

        alert(msg, 60, [bounds[0] / 2, bounds[1] / 2])

        pygame.display.update()

        for event in pygame.event.get():
            #input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    lvl += 1

splash()

# quit
if event.type == pygame.QUIT:
    running = False
