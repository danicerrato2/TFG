import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

STATS_FILE = 'documents/spanish_abstracts_stats.txt'

stats_file = open(STATS_FILE, 'r', encoding='utf-8')
binwidth = 10
bandwidth_original = 0.25
bandwidth_chatGPT = 0.25
min_range = 0
max_range = 1

def merge_stats(stats: dict, merged_stats: dict):
	for key in stats.keys():
		if isinstance(stats[key], dict):
			merged_stats = merge_stats(stats[key], merged_stats)
		else:
			if key not in merged_stats.keys():
				merged_stats[key] = []
			if isinstance(stats[key], list):
				merged_stats[key].extend(stats[key])
			else:
				merged_stats[key].append(stats[key])
	
	return merged_stats

def print_plot(stat: str, original_stats: list, chatGPT_stats: list):
	global binwidth, bandwidth_original, bandwidth_chatGPT, min_range, max_range

	num_points = max(len(original_stats), len(chatGPT_stats))
	original = np.array(original_stats)
	chatGPT = np.array(chatGPT_stats)
	x = np.arange(min_range, max_range, binwidth)

	plt.figure()
	plt.hist(original, bins=x)
	plt.title("original")

	kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth_original).fit(original[:, None])
	log_dens_original = kde.score_samples(x[:, None])
	original_y = binwidth * num_points * np.exp(log_dens_original)

	plt.plot(x, original_y)

	plt.figure()
	plt.hist(chatGPT, bins=x)
	plt.title("chatGPT")

	kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth_chatGPT).fit(chatGPT[:, None])
	log_dens_chatGPT = kde.score_samples(x[:, None])
	chatGPT_y = binwidth * num_points * np.exp(log_dens_chatGPT)

	plt.plot(x, chatGPT_y)

	plt.figure()
	plt.plot(x, original_y, label=f"original (bandw={bandwidth_original})")
	plt.plot(x, chatGPT_y, label=f"chatGPT (bandw={bandwidth_chatGPT})")
	plt.legend()
	plt.title(f"{stat} ({num_points} valores) binw={binwidth}")
	plt.xlabel(stat)
	plt.ylabel("Cantidad")

	plt.show()

def show_keys(list_keys: list):
	for i, key in enumerate(list_keys):
		print(f"{i}: {key}")
	print("Elige un numero:")

def print_configuration():
    print(f"Range: {min_range} - {max_range}")
    print(f"Binwidth: {binwidth}")
    print(f"Bandwidth: {bandwidth_original} (original) - {bandwidth_chatGPT} (chatGPT)")

if __name__ == '__main__':
	original_stats = {}
	chatGPT_stats = {}

	stats_rows = stats_file.readlines()
	for stats_row in stats_rows:
		stats = json.loads(stats_row[:-2])

		original_stats = merge_stats(stats["Resumen"], original_stats)
		chatGPT_stats = merge_stats(stats["Resumen_ChatGPT"], chatGPT_stats)

	keys = list(set(original_stats.keys()).union(chatGPT_stats.keys()))
	keys.sort(reverse=True)
 
	show_keys(keys)
	key_number = input()
	key = keys[int(key_number)]
	while True:
		command = input("Siguiente comando: ").split()
		if len(command) == 0:
			continue
		if command[0] == 'key':
			show_keys(keys)
			key_number = input()
			key = keys[int(key_number)]
		elif command[0] == "exit":
			exit()
		elif command[0] == 'bin':
			binwidth = float(command[1])
		elif command[0] == 'band':
			bandwidth_original = float(command[1])
			bandwidth_chatGPT = float(command[2])
		elif command[0] == 'range':
			min_range = float(command[1])
			max_range = float(command[2])
		elif command[0] == 'show':
			print_plot(key, original_stats[key], chatGPT_stats[key])
		elif command[0] == 'data':
			print("\n" + str(original_stats[key]) + "\n\n" + str(chatGPT_stats[key]) + "\n")
		elif command[0] == 'config':
			print_configuration()
