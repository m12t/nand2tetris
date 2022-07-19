"""
A simple non-symbolic assembler for the Hack assembly language
"""
# import argparse to handle the .asm file


def main():
    # if A instruction: assert instruction[15] == 0, and the rest of the value is the computed zero-padded 15 bit binary value given by @value
    # else (C instruction): instruction[15..13] = 1, then pass through a parser and extract the 3 components (dest, comp, jmp)
    out = []  # empty list for storing the "binary" translation
    with open("add/Add.asm", "r") as f:
        for line in f.readlines():
            if line[0] == '@':  # it's an A instruction
                binary = parse_a(line)
            else:
                binary = parse_c(line)
            out.append(binary)
    decimal_to_binary(11237)


def decimal_to_binary(num: str) -> str:
    # generate a 15 bit binary number from a decimal
    # can this be negative...?
    num = int(num)
    # print(num)
    out = ["0"] * 15
    place = 14

    while num >= 0 and place >= 0:
        if num >= 2**place:
            out[14-place] = '1'
            num -= 2**place
        place -= 1
    out = "".join(out)
    # print(out)
    return out


def parse_a(line: str) -> str:
    pass


def parse_c(line: str) -> str:
    pass


if __name__ == "__main__":
    # load the file
    main()
