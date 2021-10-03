from permutations import get_permutations
import multiprocessing
import random
import pygame
import time

WIDTH = 800
HEIGHT = 600
TOTAL_CITIES = 11
BORDER_PERCENT = 5  # percent of border in which cities will not appear


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


def find_shortest_path(shared_val, key, cities, thread_num, num_threads):
	permutations = get_permutations(TOTAL_CITIES)
	best_distance = calc_distance(cities)
	running = True

	for i in range(thread_num):
		next(permutations)

	while running:
		cities_in_permutation = None
		try:
			cities_in_permutation = [cities[i] for i in next(permutations)]
			for i in range(num_threads - 1):
				next(permutations)
		except StopIteration:
			running = False
			print(key, "stopped")
		distance = calc_distance(cities_in_permutation)
		if distance < best_distance:
			best_distance = distance
			shared_val[key] = cities_in_permutation.copy()
			tab = '\t' + ('\t' if len(key) == 2 else '')
			print(key, tab + "found best distance of", round(distance), "px")

	print(key, "finished")


def main():
	cities = []
	border_width = round(WIDTH * BORDER_PERCENT / 100)
	border_height = round(HEIGHT * BORDER_PERCENT / 100)
	for i in range(TOTAL_CITIES):
		# 	print("Done")
		v = pygame.math.Vector2(
			x=random.randint(border_width, WIDTH - border_width),
			y=random.randint(border_height, HEIGHT - border_height)
		)
		cities.append(v)

	processes = []
	num_threads = 12

	manager = multiprocessing.Manager()
	shared_dict = manager.dict()

	for i in range(num_threads):
		key = 'p' + str(i)
		process = multiprocessing.Process(target=find_shortest_path, args=(shared_dict, key, cities, i, num_threads))
		process.start()
		processes.append(process)

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	running = True
	display_message = True
	time.sleep(0.5)

	while running:
		screen.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("stopped")
				running = False

		best_distance = 1e100
		best_perm = []
		for i in range(num_threads):
			key = 'p' + str(i)
			distance = calc_distance(shared_dict[key])
			if distance < best_distance:
				best_distance = distance
				best_perm = shared_dict[key].copy()

		draw_path(screen, best_perm, (150, 50, 50), 7)

		all_dead = True
		for process in processes:
			if process.is_alive():
				all_dead = False
				break
		if all_dead and display_message:
			print("done")
			display_message = False

		for city in cities:
			pygame.draw.circle(screen, (0, 0, 255), (city.x, city.y), 10)

		pygame.display.update()

	for process in processes:
		process.kill()


if __name__ == '__main__':
	main()
