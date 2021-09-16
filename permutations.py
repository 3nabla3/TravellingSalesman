""" https://www.quora.com/How-would-you-explain-an-algorithm-that-generates-permutations-using-lexicographic-ordering """



def get_permutations(number):
	vals = list(range(number))
	running = True

	while running:
		yield vals
		largest_i = -1

		for i in range(len(vals) - 1):
			if vals[i] < vals[i+1]:
				largest_i = i

		# print(largest_i)

		if largest_i == -1:
			running = False
			continue

		largest_j = -1

		for j in range(len(vals)):
			if vals[largest_i] < vals[j]:
				largest_j = j

		# print(largest_j)

		vals[largest_i], vals[largest_j] = vals[largest_j], vals[largest_i]

		last_part_flipped = vals[largest_i + 1:][::-1]
		vals = vals[0:largest_i + 1] + last_part_flipped


if __name__ == '__main__':
	perms = get_permutations(4)
	perms = list(perms)
	perms[:len(perms) //2 ]
	for perm in perms:
		print(perm)