import argparse

import lib_pyasm


# setup command-line arguments
parser = argparse.ArgumentParser(
    prog="pyasm",
    description="A small compiler for 'pyasm' files written in Python, that emits x86_64-linux code.")
parser.add_argument(
    "source",
    help="path of source file to be compiled")
parser.add_argument(
    "-o", "--output",
    help="path of file to write generated assembly")
args = parser.parse_args()

# globals
statements: list = []
strings: list = []
user_functions: list = []

lib_functions: dict = {
    "print": lib_pyasm.printRAX,
    "exit": lib_pyasm.sys_exit_0
}


def parse_statements():
    global statements, strings

    # read entire source file into string
    with open(args.source, "r") as f:
        source = f.read()
        f.close()

    # each statement is one line
    statements = source.split('\n')
    statements = [s for s in statements if s]

    # split arguments by spaces
    # TODO: change this to allow spaces in strings, using "".
    for i in range(len(statements)):
        statements[i] = statements[i].split(' ')

    for i in range(len(statements)):
        instruction: str = statements[i][0]
        if instruction == "print":
            strings.append(statements[i][1])


def generate_asm():
    # data section
    asm = "section .data\n"
    for i in range(len(strings)):
        asm += f"    text{i} db \"{strings[i]}\", 10, 0\n"
    asm += "\n"

    # text section
    asm += "section .text\n"
    asm += "    global _start\n"

    # paste definitions of our lib functions
    asm += lib_functions["print"]
    asm += lib_functions["exit"]
    asm += "\n"

    # entry point
    asm += "_start:\n"

    # scan for statements
    for i in range(len(statements)):
        if statements[i][0] == "print":
            asm += (
                f"    mov rax, text{strings.index(statements[i][1])}\n" +
                "    call _printRAX\n\n"
            )

    # at the end, perform sys_exit syscall
    asm += "    call _sys_exit\n"
    return asm


def main():
    parse_statements()
    listing = generate_asm()
    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(listing)
            f.close()
    else:
        print(listing)


if __name__ == '__main__':
    main()
