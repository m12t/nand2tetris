"""
A simple non-symbolic assembler for the Hack assembly language
"""
# import argparse to handle the .asm file


comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001111",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

dest = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

jump = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def main():
    # if A instruction: assert instruction[15] == 0, and the rest of the value is the computed zero-padded 15 bit binary value given by @value
    # else (C instruction): instruction[15..13] = 1, then pass through a parser and extract the 3 components (dest, comp, jmp)
    out = []  # empty list for storing the "binary" translation
    # if True:
    #     for line in ["@1", "@14554", "MD=D+1;JLT"]:
    with open("max/Max.asm", "r") as f:
        for line in f.readlines():
            line = clean_line(line)
            if len(line) == 0:
                continue
            if line[0] == '@':  # it's an A instruction
                binary = parse_a(line)
            else:
                binary = parse_c(line)
            out.append(binary)
    print(out)
    # write out to a new file


def clean_line(line: str) -> str:
    try:
        line = line.split('//')[0]  # remove trailing comments
    except IndexError:
        pass
    line = line.replace(" ", "")  # strip whitespace so the lookups work
    line = line.replace("\n", "")  # strip whitespace so the lookups work
    return line


def decimal_to_binary(num: str) -> str:
    # generate a 15 bit binary number from a decimal
    # can this be negative...?
    if num[0] == 'R':
        num = num[1:]
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
    print(out)
    return out


def parse_a(line: str) -> str:
    out = decimal_to_binary(line[1:])  # everything after the @ character
    return "0" + out  # prepend the output with a 0 which signifies this is an A instruction


def parse_c(line: str) -> str:
    # should this be case sensitive? use .upper()???
    # the format for C instructions is: `dest = comp; jump` ... split the line on `=` and then `;`
    line = line.split('=')
    d = line[0]
    line = line[1].split(';')
    c = line[0]
    try:
        # handle trailing whitespace and comments eg M=D  // foo comment bar
        j = line[1]
    except IndexError:
        j = ""

    d = dest[d]
    c = comp[c]
    j = jump[j]

    return "111" + c + d + j


if __name__ == "__main__":
    # load the file
    main()
