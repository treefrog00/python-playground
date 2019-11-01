import argparse


def main():
    parser = argparse.ArgumentParser(description="blah.")
    parser.add_argument("file_path", help="path to input file")

    args = parser.parse_args()


if __name__ == "__main__":
    main()
