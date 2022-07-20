"""
A simple non-symbolic assembler for the Hack assembly language
"""
# import argparse to handle the .asm file
import re


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

symbol_table = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16348",
    "KEYBOARD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
}

ram_index = 16  # new variables start at index 16


def main():
    with open("pong/Pong.asm", "r") as f:
        stripped_assembly = first_pass(f)
        # print(stripped_assembly)
        machine_code = second_pass(stripped_assembly)
    write_output(machine_code)


def write_output(machine_code):
    print(machine_code)
    with open("./pong.hack", 'w') as f:
        f.truncate(0)  # clear the file
        f.write(machine_code)
    

def first_pass(f):
    # first pass will:
    # 1. remove all whitespace so that row addresses can be handled
    # 2. look for symbol definitions (left parentheses) and append
    #    the addresses to the symbol table
    # symbol_table[xxx] = address following the format: (xxx)
    assembly = []
    line_count = 0
    for line in f.readlines():
        line = clean_line(line)
        # print('line', line)
        if line == "" or line == '\n' or line == '\t':
            continue
        if line[0] == '(':
            i = 1
            name = ""
            while line[i] != ')':
                name += line[i]
                i += 1
            symbol_table[name] = line_count
            # print('-=>', symbol_table[name])
        else:
            line_count += 1
            assembly.append(line + '\n')
    return "".join(assembly)


def second_pass(program):
    out = []
    for line in program.split('\n'):
        if line == "":
            continue
        # print('whole line',line)
        # line = clean_line(line)  # shouldn't be needed at this stage
        # print('line[0]', line[0])
        if line[0] == '@':  # it's an A instruction
            binary = parse_a(line)
        else:
            binary = parse_c(line)
        out.append(binary+'\n')
    return "".join(out)


def clean_line(line: str) -> str:
    try:
        line = line.split('//')[0]  # remove trailing comments
    except IndexError:
        pass
    line = line.replace(' ', "")  # strip whitespace so the lookups work
    line = line.replace('\n', "")  # strip whitespace so the lookups work
    return line


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
    global ram_index  # pull the ram_index into scope
    address = line[1:]
    if re.search('[A-Z.0-9]', address):
        if address in symbol_table:
            # print('addy', address)
            address = symbol_table[address]
            # print('letters found', address)
        else:
            symbol_table[address] = ram_index
            address = ram_index
            ram_index += 1
    out = decimal_to_binary(address)  # everything after the @ character
    return "0" + out  # prepend the output with a 0 which signifies this is an A instruction


def parse_c(line: str) -> str:
    # the format for C instructions is: `dest = comp; jump` ... split the line on `=` and then `;`
    # however, D;JGT is valid, and no equals is present
    # dest can be null ("") and jump can be null ("")
    # print('parse_c', line)
    d, c, j = "", "", ""
    if re.search("=", line):
        line = line.split('=')
        # print('equals found line', line)
        d = line[0]
        line = line[1]
    if re.search(";", line):
        # print('semi found')
        line = line.split(';')
        c = line[0]
        j = line[1]
    else:
        c = line
    # print('d', d)
    # print('c', c)
    # print('j', j)
    d = dest[d]
    c = comp[c]
    j = jump[j]
    # print('... bin:', "111" + c + d + j)
    return "111" + c + d + j


if __name__ == "__main__":
    # load the file
    main()
