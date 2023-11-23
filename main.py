import random
import pygame

pygame.init()
pygame.mixer.init()
font = pygame.font.Font('droid-sans.regular.ttf', 64)
tiles = []
flipping_tiles = []
mouse_pressed = False
flippable = False

icon = pygame.image.load('icon.png')
timer = pygame.time.Clock()

pygame.display.set_icon(icon)
pygame.display.set_caption('Match Charm')

match1 = None
match2 = None

move1 = pygame.mixer.Sound('move1.wav')
move2 = pygame.mixer.Sound('move2.wav')
move3 = pygame.mixer.Sound('move3.wav')
moves = [move1, move2, move3]

shuffle_color = [True, True, False]
random.shuffle(shuffle_color)


def lerp(start, end, time):
    return start + (end - start) * time


def generate_color(tile):
    global shuffle_color
    color = [tile.color_off if i else 255 for i in shuffle_color]
    return color


def generate_grid(size):
    global grid
    grid_size = size
    available_matches = [x for x in range(int((grid_size ** 2) / 2))]
    available_matches += available_matches
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    for x, xam in enumerate(grid):
        for y, yam in enumerate(grid[0]):
            rand_choice = random.choice(available_matches)
            grid[x][y] = rand_choice
            available_matches.remove(rand_choice)
    return grid


class Tile:
    color_off = 0
    possible_colors = [color_off, color_off, 255]

    def __init__(self, pos, number):
        global color_offset, font
        self.color_off = (number * 255) / color_offset

        color = generate_color(self)

        self.pos = pos
        self.pos_real = [pos[0] * 100, pos[1] * 100]
        self.rect = pygame.Rect(self.pos_real, (100, 100))
        self.number = number
        self.color = color
        self.font_render_real = font.render(str(self.number), True, (255, 255, 255))
        self.rect_font_render_real = self.font_render_real.get_rect(center=self.rect.center)
        self.font_render = self.font_render_real.copy()
        self.rect_font_render = self.font_render_real.copy()
        self.rect_real = self.rect.copy()

        self.flip_time = 0
        self.flipping = False
        self.rect.w = 0
        self.solved = False

        tiles.append(self)

    def flip(self):
        if flippable:
            self.flipping = True

    def flip_back(self):
        if flippable:
            self.flipping = False

    def update(self):
        global mouse_pressed, match1, match2, flippable

        if self.rect_real.collidepoint(pygame.mouse.get_pos()) and mouse_pressed and not self.solved:
            if not self.flipping or not self.solved:
                random.choice(moves).play()
                self.flip()

        if self.flipping or self.solved:
            if self.flip_time < 1:
                self.flip_time += 0.05
        else:
            if self.flip_time > 0:
                self.flip_time -= 0.05

        if self.flip_time > 1:
            self.flip_time = 1

        if self.flip_time < 0:
            self.flip_time = 0

        if self.flipping or self.solved:
            self.rect.w = lerp(self.rect.w, 100, self.flip_time)
        else:
            self.rect.w = lerp(0, self.rect.w, self.flip_time)

        self.rect.center = self.rect_real.center
        self.font_render = pygame.transform.scale_by(self.font_render_real, (self.rect.w / 100, 1))

        self.draw()

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.font_render, self.rect_font_render_real)


grid_size = 4
color_offset = int((grid_size ** 2) / 2)
grid = generate_grid(grid_size)
display_size = [len(grid) * 100, len(grid) * 100]
screen = pygame.display.set_mode(display_size)


def regen_tiles():
    global grid, grid_size, tiles, shuffle_color
    generate_grid(grid_size)

    tiles.clear()
    random.shuffle(shuffle_color)
    for x, xam in enumerate(grid):
        for y, yam in enumerate(grid[0]):
            grid_number = grid[x][y]
            Tile([x, y], grid_number)


def main():
    global mouse_pressed, flippable, grid
    running = True
    timer.tick(60)

    regen_tiles()

    while running:
        solved_tiles = []
        mouse_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True

        screen.fill((0, 0, 0))

        for tile in tiles:
            tile.update()
            if tile.solved:
                solved_tiles.append(tile)
            if tile.flipping:
                flipping_tiles.append(tile)

        if len(flipping_tiles) >= 2:
            flippable = False
            if flipping_tiles[0].flip_time == 1 and flipping_tiles[1].flip_time == 1:
                if flipping_tiles[0].number == flipping_tiles[1].number:
                    flipping_tiles[0].solved = True
                    flipping_tiles[1].solved = True
                flipping_tiles[0].flipping = False
                flipping_tiles[1].flipping = False
        else:
            flippable = True
        flipping_tiles.clear()

        if len(solved_tiles) == len(tiles):
            regen_tiles()

        pygame.display.flip()


if __name__ == '__main__':
    main()
