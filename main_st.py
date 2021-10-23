from permutations import get_permutations
import multiprocessing
import random
import pygame
import math
import time

WIDTH = 800
HEIGHT = 600
TOTAL_CITIES = 10
BORDER_PERCENT = 5  # percent of border in which cities will not appear

def feature():
    # This is just code for a new feature that I am testing
    pass

def swap(array, i, j):
    array[i], array[j] = array[j], array[i]


def calc_distance(points):
    total_distance_squared = 0
    for i in range(len(points) - 1):
        total_distance_squared += (
                (points[i + 1].x - points[i].x) ** 2 +
                (points[i + 1].y - points[i].y) ** 2
        )
    return total_distance_squared


def draw_path(screen, cities, color=(100, 100, 100), size=5):
    for i in range(len(cities) - 1):
        pygame.draw.line(
            screen, color,
            (cities[i].x, cities[i].y), (cities[i + 1].x, cities[i + 1].y),
            size
        )


def main():
    border_width = round(WIDTH * BORDER_PERCENT / 100)
    border_height = round(HEIGHT * BORDER_PERCENT / 100)

    cities = [
        pygame.math.Vector2(
            x=random.randint(border_width, WIDTH - border_width),
            y=random.randint(border_height, HEIGHT - border_height)
        ) for i in range(TOTAL_CITIES)
    ]

    record_distance = calc_distance(cities)
    record_order = cities.copy()
    permutations = get_permutations(TOTAL_CITIES)
    total_permutations = math.factorial(TOTAL_CITIES)
    current_permutation_number = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    TIME_STEP = 1
    frame = 0
    running = True
    display_message = True

    t1 = time.time()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_permutation_number < total_permutations:
            current_order = [cities[i] for i in next(permutations)]
        elif display_message:
            print(f'Best order with distance {record_distance} found in {round(time.time() - t1, 2)} seconds.')
            display_message = False

        current_permutation_number += 1
        draw_path(screen, current_order, (100, 100, 100), 1)

        distance = calc_distance(current_order)
        if distance < record_distance:
            record_distance = distance
            record_order = current_order.copy()

        draw_path(screen, record_order, (150, 50, 50), 7)
        pygame.draw.line(screen, (255, 0, 0), (0, 10), (WIDTH * current_permutation_number / total_permutations, 10),
                         10)

        # if frame == TIME_STEP:
        # 	pygame.display.update()
        # 	frame = 0
        # frame += 1
        pygame.display.update()


if __name__ == '__main__':
    main()
