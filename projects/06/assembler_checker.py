"""
a little script to verify that the output of the assembler is correct.

this is accomplished by using the `Source of Truth` assembler provided
by Noam Nisan and Shimon Schocken at tools/Assembler.sh

"""
import argparse


# TODO: add a % match as well as lines that differ

def main(args: dict):
    file1 = args.file1
    file2 = args.file2
    print("file1:", file1)
    print("file2:", file2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # required args:
    parser.add_argument('--file1', type=str, required=True,
                        help='the path to the first file you wish to compare')
    parser.add_argument('--file2', type=str, required=True,
                        help='the path to the second file you wish to compare')
    args = parser.parse_args()
    main(args)
