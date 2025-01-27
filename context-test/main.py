def print_guppy():
	"""
	Prints an ASCII art representation of a guppy fish
	"""
	guppy = [
		"    ,\\      ,",
		"    |\\____/|",
		"   /  o  o  \\",
		"  /     >    \\",
		" /  \\_____/   \\",
		"/__|       |__/\\",
		"   |       |",
		"   \\_______/"
	]

	for line in guppy:
		print(line)

if __name__ == "__main__":
	print_guppy()