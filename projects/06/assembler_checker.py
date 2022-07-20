"""
a little script to verify that the output of the assembler is correct.

this is accomplished by using the `Source of Truth` assembler provided
by Noam Nisan and Shimon Schocken at tools/Assembler.sh
"""

import argparse


def main(args: dict):
    differences = 0
    file1 = args.file1
    file2 = args.file2

    program1 = []
    program2 = []

    with open(file1, 'r') as f:
        program1 = list(f)

    with open(file2, 'r') as f:
        program2 = list(f)

    program1_len = len(program1)
    program2_len = len(program2)
    shortest = min(program1_len, program2_len)

    if program1_len != program2_len:
        print("------------------------------------")
        print("ERROR! Program lengths do not match:")
        print("program1 length:", program1_len)
        print("program2 length:", program2_len)
        print("------------------------------------")

    for i in range(shortest):
        if program1[i] != program2[i]:
            differences += 1
            print("------------------------------------")
            print(f"comparison failure on line {i}")
            print("program1 output:", program1[i])
            print("program2 output:", program2[i])
    print("------------------------------------")

    longest = max(program1_len, program2_len)
    print(f"the files were a {100*(1-(differences/longest)):.2f}% match")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # required args:
    parser.add_argument('--file1', type=str, required=True,
                        help='the path to the first file you wish to compare')
    parser.add_argument('--file2', type=str, required=True,
                        help='the path to the second file you wish to compare')
    args = parser.parse_args()
    main(args)
