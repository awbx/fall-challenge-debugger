#!/usr/local/bin/python3

import pygame
import random

h, w = [int(x) for x in input().split()]


UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

GRASS = 1
NEATRAL = 2
RED = 4
BLUE = 8


map = []
for idx in range(h):
    line = input().split(' ')
    line = list(filter(lambda x: len(x), line))
    line.insert(0, "0000")
    line.append("0000")
    map.append(line)

line = ["0000" for x in range(len(map[0]))]
map.insert(0, line)
map.append(line)
h += 2
w += 2


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return "x -> %d, y -> %d" % (self.x, self.y)


iw, ih = (70, 70)

pygame.init()

screen = pygame.display.set_mode((w * iw, h * ih))

grass_images = pygame.image.load('./images/grass/grass.png').convert()

recycler_imgaes = [pygame.image.load('./images/recycler/blue.png').convert(),  pygame.image.load('./images/recycler/red.png').convert()]
tiles_images = [pygame.image.load(f'./images/tile/{x + 1}.png').convert() for x in range(5)]
robot_images = [pygame.image.load('./images/robot/blue.png').convert(),  pygame.image.load('./images/robot/red.png').convert()]


def get_number(char):
    if char.isdigit():
        return char
    return ord(char) - ord('A') + 10


def choice_tile(type, flag):
    img = random.choice(tiles_images).copy()
    font = pygame.font.SysFont("arial", 50)
    side = 0 # default is blue
    if type & GRASS:
        img = grass_images.copy()
    elif type & RED:
        img.fill((0xff, 0, 0, 0xff), None, pygame.BLEND_RGBA_MULT)
        side = 1
    elif type & BLUE:
        img.fill((0, 0, 0xff, 0xff), None, pygame.BLEND_RGBA_MULT)
    
    if flag[0] == 'r':
        img = recycler_imgaes[side].copy()
    elif flag[0] != '0':
        img = robot_images[side].copy()
    
    img = pygame.transform.scale(img, (iw, ih))

    if flag[0] != '0' and flag[0] != 'r':
        text = font.render(str(get_number(flag[0])), True, (0xff, 0xff, 0xff))
        img.blit(text, (0, 0))

    if flag[1] == 'X':
        pygame.draw.line(img, (0xff, 0xff, 0xff), (0, 0), (iw, ih), width=10)
        pygame.draw.line(img, (0xff, 0xff, 0xff), (iw, 0), (0, ih), width=10)
    
    return (flag[2], img)

def draw_arrow(pos, height, dir=UP):

    line_start: Pos = pos
    line_end = Pos(pos.x, pos.y - height)

    left_arrow = Pos(pos.x - 10, line_end.y + 30)
    right_arrow = Pos(pos.x + 10, line_end.y + 30)

    if dir == LEFT:
        line_end = Pos(pos.x - height, pos.y)
        left_arrow = Pos(line_end.x + 30, pos.y + 10)
        right_arrow = Pos(line_end.x + 30, pos.y - 10)
    elif dir == RIGHT:
        line_end = Pos(pos.x + height, pos.y)
        left_arrow = Pos(line_end.x - 30, pos.y - 10)
        right_arrow = Pos(line_end.x - 30, pos.y + 10)
    elif dir == DOWN:
        line_end = Pos(pos.x, pos.y + height)
        left_arrow = Pos(pos.x + 10, line_end.y - 30)
        right_arrow = Pos(pos.x - 10, line_end.y - 30)

    pygame.draw.line(screen, (0, 0, 0), line_start(), line_end(), width=5)
    pygame.draw.line(screen, (0, 0, 0), line_end(), left_arrow(), width=4)
    pygame.draw.line(screen, (0, 0, 0), line_end(), right_arrow(), width=4)

images = {
    '0': lambda flag: choice_tile(GRASS, flag),
    '1': lambda flag: choice_tile(NEATRAL, flag),
    'R': lambda flag: choice_tile(RED, flag),
    'B': lambda flag: choice_tile(BLUE, flag),
}

arrows = []

y = 0
while y < h:
    x = 0
    while x < w:
        cell = map[y][x]
        obj = images[cell[0]](cell[1:])

        screen.blit(obj[1], (x * iw, y * ih))
        if obj[0] != '0':
            arrows.append((Pos(x * iw + (iw // 2), y * ih + (ih // 2)), obj[0]))
        x += 1
    y += 1


for arrow in arrows:
    draw_arrow(arrow[0], ih - 2, arrow[1])


pygame.display.flip()
running = True

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
