from common import parse_args_and_get_input

args, lines = parse_args_and_get_input()


class DirNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.direct_size = 0
        self.total_size = 0


example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

example_lines = example.splitlines()


def dfs_sizer(start) -> int:
    total_child_size = 0
    for child in start.children:
        total_child_size += dfs_sizer(child)
    start.total_size = start.direct_size + total_child_size
    print(f"{start.name}: {start.total_size}")

    return start.total_size


def print_node(start, indent):
    indent_text = " " * indent + start.name
    #print(f"{indent_text} direct s: {start.direct_size}")
    #print(f"{indent_text} size if small: {start.total_size if start.total_size <= 100000 else 0}")
    print(f"{indent_text} total size: {start.total_size / 1000}k")
    for child in start.children:
        print_node(child, indent + 4)


def dfs_lte_100k_summer(start):
    child_total = 0
    for child in start.children:
        child_total += dfs_lte_100k_summer(child)
    self_total = start.total_size

    if self_total <= 100000:
        return self_total + child_total
    return child_total


def build_tree(current_node, lines):
    node_stack = [current_node]

    for line in lines:
        if line.startswith("$ cd"):
            target = line[5:]
            if target == "..":
                node_stack.pop()
                current_node = node_stack[-1]
            else:
                if target != "/":
                    current_node = next(child for child in current_node.children if child.name == target)
                    node_stack.append(current_node)
            continue

        ord_val = ord(line[0])

        if line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            dir_name = line.split(" ")[1]
            current_node.children.append(DirNode(dir_name))
        elif ord_val >= 48 and ord_val <= 57:
            current_node.direct_size += int(line.split(" ")[0])
        else:
            raise Exception(line)


def sizes_to_list(start, sizes):
    for child in start.children:
        sizes_to_list(child, sizes)
    sizes.append(start.total_size)
    return sizes


def run(lines):
    root_node = DirNode("/")
    build_tree(root_node, lines)
    dfs_sizer(root_node)

    if args.part_one:
        print(f"sum via described part one method: {dfs_lte_100k_summer(root_node)}")
        print_node(root_node, 0)
    else:
        total_space = 70000000
        update_size = 30000000
        available_space = total_space - root_node.total_size
        print(f"available: {available_space/1000}k")
        to_free = update_size - available_space
        print(f"to free: {to_free / 1000}k")
        all_sizes = sizes_to_list(root_node, [])
        print(sorted(x for x in all_sizes))
        print(sorted(x for x in all_sizes if x >= to_free)[0])
        #print_node(root_node, 0)


#run(example_lines)
run(lines)
