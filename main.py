import pygame

# pygame fundamentals
pygame.init()

bounds = [800, 600]
disp = pygame.display.set_mode(bounds)
screen = pygame.display.get_surface()

pygame.display.set_caption('Gravity Guy!')

lvls = range(12)
lvl = 0

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

    return cont.get_rect()[2]

# lvl
i = 0

def select_lvl(i):
    global lvl

    if lvl + i >= 0 and lvl + i < len(lvls):
        lvl += i

# prop
start = {
        'x': 2,
        'y': 1
        }

boxes = [
        [
            {
                'x': 1,
                'y': 6
                }, {
                    'x': 7,
                    'y': 6
                    }, {
                        'x': 8,
                        'y': 1
                        }, {
                            'x': 12,
                            'y': 0
                            }, {
                                'x': 1,
                                'y': 5
                                }, {
                                    'x': 2,
                                    'y': 2
                                    }
                                ], [
                                    {
                                        'x': 4,
                                        'y': 8
                                        }, {
                                            'x': 5,
                                            'y': 6
                                            }, {
                                                'x': 12,
                                                'y': 4
                                                }, {
                                                    'x': 4,
                                                    'y': 2
                                                    }, {
                                                        'x': 1,
                                                        'y': 5
                                                        }, {
                                                            'x': 2,
                                                            'y': 2
                                                            }
                                                        ]
                                ]

stars = [
        {
            'x': 8,
            'y': 8
            }, {
                'x': 10,
                'y': 10
                }
            ]

goal = {
        'x': 2,
        'y': 3
        }

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

        alert('Gravity Guy!', 100, [bounds[0] / 2 - get_txt_center('Gravity Guy!'), bounds[1] / 2 - 100], (000, 000, 000))

        for i in lvls:
            margin += 40

            if i == lvl:
		pygame.draw.rect(disp, (000, 000, 000), [margin, bounds[1] / 2, size, size])
                color = (255, 255, 255)

            else:
                color = (000, 000, 000)

	    alert(str(i), 30, [margin + size / 2, bounds[1] / 2 - 15 + size / 2], color)

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
    running = True

    pos = start

    while running:
        disp.fill((255, 255, 255))

        # prop
        screen.blit(player, (pos['x'] * size, pos['y'] * size))

        for box in boxes[lvl]:
            pygame.draw.rect(disp, (000, 000, 000), [box['x'] * size, box['y'] * size, size, size])

        for star in stars:
            pygame.draw.rect(disp, (255, 215, 000), [star['x'] * size, star['y'] * size, size, size])

        pygame.draw.rect(disp, (255, 0, 0), [goal['x'] * size, goal['y'] * size, size, size])

        # input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                del target_candidates[:]

                if event.key == pygame.K_RIGHT:
                    for box in boxes[lvl]:
                        if box['y'] == pos['y']:
                            target_candidates.append(box)

                    target = target_candidates[0]
                    rotate(90)

                    if pos['y'] == target['y'] and pos['x'] < target['x']:
                        pos['x'] = target['x'] - 1

                    else:
                        pos['x'] = bounds[0] + 1

                if event.key == pygame.K_LEFT:
                    for box in boxes[lvl]:
                        if box['y'] == pos['y']:
                            target_candidates.append(box)

                    target = target_candidates[0]
                    rotate(270)

                    if pos['y'] == target['y'] and pos['x'] > target['x']:
                        pos['x'] = target['x'] + 1

                    else:
                        pos['x'] = -1

                if event.key == pygame.K_UP:
                    for box in boxes[lvl]:
                        if box['x'] == pos['x']:
                            target_candidates.append(box)

                    target = target_candidates[0]
                    rotate(180)

                    if pos['x'] == target['x'] and pos['y'] > target['y']:
                        pos['y'] = target['y'] + 1

                    else:
                        pos['y'] = bounds[0] - 1

                if event.key == pygame.K_DOWN:
                    for box in boxes[lvl]:
                        if box['x'] == pos['x']:
                            target_candidates.append(box)

                    target = target_candidates[0]
                    rotate(0)

                    if pos['x'] == target['x'] and pos['y'] < target['y']:
                        pos['y'] = target['y'] - size

                    else:
                        pos['y'] = bounds[0] + size

                if event.key == pygame.K_ESCAPE:
                    menu()

            # fail
            if pos['x'] < 0 or pos['x'] > bounds[0] or pos['y'] < 0 or pos['y'] > bounds[1]:
                success = False
                menu()

            # success
            if pos == goal:
                success = True
                menu()

        pygame.display.update()

success = False

def menu():
    global lvl, success

    running = False
    show_menu = True

    while show_menu:
        pygame.draw.rect(disp, (200, 200, 200), [size / 2, size / 2, bounds[0] - size, bounds[1] - size])

        if success:
            alert('Well done!', 60, [bounds[0] / 2, bounds[1] / 2], (255, 255, 255))
            alert('Next level', 60, [bounds[0] / 2, bounds[1] / 2 + 40], (255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        select_lvl(1)
                        
                        play()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play()

                if event.key == pygame.K_r:
                    pos = start

                    play()

                if event.key == pygame.K_m:
                    splash()
                    
        alert('Menu', 40, [40, bounds[1] - 70], (255, 255, 255))
        alert('Restart', 40, [40, bounds[1] - 110], (255, 255, 255))

        pygame.display.update()

splash()

# quit
if event.type == pygame.QUIT:
    running = False
