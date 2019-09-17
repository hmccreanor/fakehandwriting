import math
import numpy as np
import pygame
import sys

pygame.init()

window_dims = (500, 600)
canvas_dims = (500, 500)
cell_size = (50, 50)

screen = pygame.display.set_mode(window_dims)

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet = "abcdef"
current_letter = 0

n_repetitions = 3
n = 0

handwriting = {}
current_glyph = np.zeros((int(canvas_dims[1] / cell_size[1]), int(canvas_dims[0] / cell_size[0])))
clicking = False

font = pygame.font.Font(None, 50)

gathering_data = True

while gathering_data:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
        elif event.type == pygame.MOUSEMOTION:
            if clicking:
                pos = pygame.mouse.get_pos()
                x = math.floor(pos[0] / cell_size[0])
                y = math.floor(pos[1] / cell_size[1])
                if pos[1] < canvas_dims[1]:
                    current_glyph[y][x] = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            clicking = False

        elif event.type == pygame.KEYDOWN:
            if n == 0:
                handwriting[alphabet[current_letter]] = current_glyph
            else:
                handwriting[alphabet[current_letter]] += current_glyph

            current_glyph = np.zeros((int(canvas_dims[1] / cell_size[1]), int(canvas_dims[0] / cell_size[0])))

            n += 1
    screen.fill((255, 255, 255))

    for y in range(current_glyph.shape[0]):
        pygame.draw.line(screen, (0, 0, 0), (0, y * cell_size[1]), (canvas_dims[0], y * cell_size[1]))

    for x in range(current_glyph.shape[1]):
        pygame.draw.line(screen, (0, 0, 0), (x * cell_size[0], 0), (x * cell_size[0], canvas_dims[1]))

    for y in range(current_glyph.shape[0]):
        for x in range(current_glyph.shape[1]):
            if current_glyph[y][x] == 1:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * cell_size[0], y * cell_size[1], cell_size[0], cell_size[1]))

    letter_prompt = font.render("Please type the letter " + alphabet[current_letter], True, (0, 0, 0))
    screen.blit(letter_prompt, (0, 500))

    if n == n_repetitions:
        handwriting[alphabet[current_letter]] /= n_repetitions
        print(handwriting[alphabet[current_letter]])
        current_letter += 1
        n = 0
    
    if current_letter == len(alphabet):
        gathering_data = False
    pygame.display.flip()

typing = True
typed_so_far = ""

chars = [[]]
current_line = 0

while typing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = chr(event.key)
            if key in alphabet:
                char = pygame.Surface(cell_size)
                char.fill((255, 255, 255))

                char_glyph_probabilities = handwriting[key]
                char_glyph = np.zeros(char_glyph_probabilities.shape)
                for y in range(char_glyph.shape[0]):
                    for x in range(char_glyph.shape[1]):
                        prob = char_glyph_probabilities[y][x]
                        state = np.random.choice(2, 1, p = (1 - prob, prob))
                        char_glyph[y][x] = state
                        if state == 1:
                            pygame.draw.rect(char, (0, 0, 0), pygame.Rect(x, y, 1, 1))
                print(char_glyph)

                char = pygame.transform.scale(char, (100, 100))
                if cell_size[0] * (len(chars[current_line]) + 1) > window_dims[0]:
                    print("newline")
                    chars.append([])
                    current_line += 1

                chars[current_line].append(char)
            
            if key == " ":
                chars.append(" ")

    screen.fill((255, 255, 255))

    for i in range(len(chars)):
        for j, char in enumerate(chars[i]):
            if char != " ":
                screen.blit(char, (j * cell_size[0], i * cell_size[1]))

    pygame.display.flip()
