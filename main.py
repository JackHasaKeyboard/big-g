import pygame

# pygame fundamentals
pygame.init()

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)
screen = pygame.display.get_surface()

pygame.display.set_caption('Gravity Guy!')

size = 50

# player
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
i = 0

def select_lvl(i):
    global lvl

    if lvl + i >= 0 and lvl + i < lvls:
        lvl += i

# prop
prop = [
        {
            'start': {
                'x': 5,
                'y': 4
                },
            'boxes': [
                {
                    'x': 9,
                    'y': 4
                    },
                {
                    'x': 8,
                    'y': 7
                    },
                {
                    'x': 6,
                    'y': 6
                    }
                ],
            'stars': [
                ],
            'goal': {
                'x': 8,
                'y': 6
                }
            }, {
                'start': {
                    'x': 7,
                    'y': 4
                    },
                'boxes': [
                    {
                        'x': 7,
                        'y': 5
                        },
                    {
                            'x': 7,
                            'y': 1
                            },
                    {
                                'x': 10,
                                'y': 2
                                },
                    {
                                    'x': 9,
                                    'y': 6
                                    },
                    {
                                        'x': 2,
                                        'y': 4
                                        },
                    {
                                            'x': 2,
                                            'y': 4
                                            },
                    {
                                                'x': 3,
                                                'y': 7
                                                }
                                            ],
                'stars': [
                    {
                        'x': 3,
                        'y': 4
                        }
                    ],
                'goal': {
                    'x': 8,
                    'y': 5
                    }
                }, {
                        'start': {
                            'x': 7,
                            'y': 3
                            },
                        'boxes': [
                            {
                                'x': 1,
                                'y': 4
                                },
                            {
                                    'x': 4,
                                    'y': 7
                                    }
                                ],
                        'stars': [
                            {
                                'x': 1,
                                'y': 4
                                }
                            ],
                        'goal': {
                            'x': 4,
                            'y': 2
                            }
                        }

                ]

lvl = 0
lvls = len(prop)

margin = 0

def splash():
    global lvl, margin

    splash = True

    while splash:
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
                    play()

        margin = 0

        disp.fill((255, 255, 255))

        alert('Gravity Guy!', 100, [bounds[0] / 2 - get_txt_center('Gravity Guy!')[2], bounds[1] / 2 - 100], (000, 000, 000))

        for i in range(len(prop)):
            margin += 80

            if i == lvl:
                pygame.draw.rect(disp, (000, 000, 000), [margin, bounds[1] / 2, size, size])

                color = (255, 255, 255)

            else:
                color = (000, 000, 000)

            alert(str(i), 30, [size / 2 + margin - 5, bounds[1] / 2 - 10 + size / 2], color)

        pygame.display.update()

prev_rot = 0

target_candidates = []

def rotate(deg):
    global player, prev_rot

    player = pygame.transform.rotate(player, -prev_rot + deg)

    prev_rot = deg

def play():
    global player, running, prev_rot, success

    splash = False
    show_menu = False
    success = False
    running = True

    pos = prop[lvl]['start']

    while running:
        disp.fill((255, 255, 255))

        # prop
        screen.blit(player, (pos['x'] * size, pos['y'] * size))

        for box in prop[lvl]['boxes']:
            pygame.draw.rect(disp, (000, 000, 000), [box['x'] * size, box['y'] * size, size, size])

        for star in prop[lvl]['stars']:
            pygame.draw.rect(disp, (255, 215, 000), [star['x'] * size, star['y'] * size, size, size])

        pygame.draw.rect(disp, (255, 000, 000), [prop[lvl]['goal']['x'] * size, prop[lvl]['goal']['y'] * size, size, size])

        # input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                del target_candidates[:]

                if event.key == pygame.K_RIGHT:
                    for box in prop[lvl]['boxes']:
                        if box['y'] == pos['y']:
                            target_candidates.append(box)

                    if target_candidates[0] != None:
                        target = target_candidates[0]
                        rotate(90)

                        if pos['y'] == target['y'] and pos['x'] < target['x']:
                            pos['x'] = target['x'] - 1

                        else:
                            pos['x'] = bounds[0] + 1

                    else:
                        menu()

                if event.key == pygame.K_LEFT:
                    for box in prop[lvl]['boxes']:
                        if box['y'] == pos['y']:
                            target_candidates.append(box)

                    if target_candidates[0] != None:
                        target = target_candidates[0]
                        rotate(270)

                        if pos['y'] == target['y'] and pos['x'] > target['x']:
                            pos['x'] = target['x'] + 1

                        else:
                            pos['x'] = -1

                    else:
                        menu()

                if event.key == pygame.K_UP:
                    for box in prop[lvl]['boxes']:
                        if box['x'] == pos['x']:
                            target_candidates.append(box)

                    if target_candidates[0] != None:
                        target = target_candidates[0]
                        rotate(180)

                        if pos['x'] == target['x'] and pos['y'] > target['y']:
                            pos['y'] = target['y'] + 1

                        else:
                            pos['y'] = bounds[0] - 1

                    else:
                        menu()

                if event.key == pygame.K_DOWN:
                    for box in prop[lvl]['boxes']:
                        if box['x'] == pos['x']:
                            target_candidates.append(box)

                    if target_candidates[0] != None:
                        target = target_candidates[0]
                        rotate(0)

                        if pos['x'] == target['x'] and pos['y'] < target['y']:
                            pos['y'] = target['y'] - 1

                        else:
                            pos['y'] = bounds[0] + 1

                    else:
                        menu()

                if event.key == pygame.K_ESCAPE:
                    menu()

            # fail
            if pos['x'] < 0 or pos['x'] > bounds[0] or pos['y'] < 0 or pos['y'] > bounds[1]:
                success = False
                menu()

            # success
            if pos == prop[lvl]['goal']:
                success = True
                menu()

        pygame.display.update()

success = False

def menu():
    global lvl, success

    running = False
    show_menu = True

    pygame.display.update()

    while show_menu:
        pygame.draw.rect(disp, (200, 200, 200), [size / 2, size / 2, bounds[0] - size, bounds[1] - size])

        if success:
            alert('Well done!', 60, [bounds[0] / 2 - get_txt_center('Well done!')[2] / 2, bounds[1] / 2], (255, 255, 255))
            alert('Next level', 60, [bounds[0] / 2 - get_txt_center('Next level')[2] / 2, bounds[1] / 2 + 40], (255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        select_lvl(1)

                        play()

                pygame.display.update()

        else:
            alert('Fail :(', 60, [bounds[0] / 2 - get_txt_center('Well done!')[2] / 2, bounds[1] / 2], (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play()

                if event.key == pygame.K_r:
                    pos = prop[lvl]['start']

                    play()

                if event.key == pygame.K_m:
                    splash()

            pygame.display.update()

        alert('Menu', 40, [40, bounds[1] - 70], (255, 255, 255))
        alert('Restart', 40, [40, bounds[1] - 110], (255, 255, 255))

splash()

# quit
if event.type == pygame.QUIT:
    running = False
