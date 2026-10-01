#!/usr/bin/env python3

import argparse

from symbol_table import SymbolTable
from parser import Parser
from command import Command
from binary_encoder import BinaryEncoder

arg_parser = argparse.ArgumentParser(
    prog="Hack Assembler",
    description="Given a hack assembly file, assemble it into machine code for the hack CPU to execute",
)

arg_parser.add_argument("input_filename")
arg_parser.add_argument("output_filename")
arg_parser.add_argument(
    "-d", "--debug", action="store_true"
)  # If set, args.debug is True

args = arg_parser.parse_args()

# First Pass Go through the entire assembly program, line by line, and build the
# symbol table without generating any code. As you march through the program lines,
# keep a running number recording the ROM address into which the current command
# will be eventually loaded. This number starts at 0 and is incremented by 1 whenever
# a C-instruction or an A-instruction is encountered, but does not change when a label
# pseudocommand or a comment is encountered. Each time a pseudocommand (Xxx)
# is encountered, add a new entry to the symbol table, associating Xxx with the ROM
# address that will eventually store the next command in the program. This pass results
# in entering all the program’s labels along with their ROM addresses into the symbol
# table. The program’s variables are handled in the second pass.

# # Pass 1: Assign addresses to labels
asm_symbol_table = SymbolTable()
asm_parser = Parser(args.input_filename)

current_rom_address = 0

while asm_parser.has_more_commands():
    asm_parser.advance()  # Must advace BEFORE reading a command

    # Check if current line is an L_COMMAND, if so, it must be a label
    if asm_parser.get_command_type() == Command.L_COMMAND:
        "L command: Labels don't take up space in output machine code, dont inc ROM counter"

        extracted_label_name = asm_parser.symbol()

        asm_symbol_table.addEntry(extracted_label_name, current_rom_address)

        if args.debug:
            print(
                f"L COMMAND: {asm_parser.get_current_command()}\tLABEL NAME: {extracted_label_name}"
            )
    else:
        "A or C command"
        current_rom_address += 1  # Takes up one line in output machine code


# Second Pass Now go again through the entire program, and parse each line. Each
# time a symbolic A-instruction is encountered, namely, @Xxx where Xxx is a symbol
# and not a number, look up Xxx in the symbol table. If the symbol is found in the
# table, replace it with its numeric meaning and complete the command’s translation.
# If the symbol is not found in the table, then it must represent a new variable. To
# handle it, add the pair (Xxx, n) to the symbol table, where n is the next available
# RAM address, and complete the command’s translation. The allocated RAM
# addresses are consecutive numbers, starting at address 16 ( just after the addresses
# allocated to the predefined symbols)

# # Pass 2: Extract variables and encode final instruction
asm_parser.reset_command_idx()  # Go back to first command

current_ram_address = 16  # Free memory starts at address 16
output_file_commands: list[bytes] = []

while asm_parser.has_more_commands():
    asm_parser.advance()  # Must advace BEFORE reading a command

    # Check if current line is an L_COMMAND, if so, it must be a label
    command_type = asm_parser.get_command_type()
    if command_type == Command.A_COMMAND:
        "A command: extract symbol name and add to symbol table if it isn't already there"

        extracted_var_name = asm_parser.symbol()

        if extracted_var_name.isdigit():
            address_to_encode = int(extracted_var_name)
        elif asm_symbol_table.contains(extracted_var_name):
            address_to_encode = asm_symbol_table.get_address(extracted_var_name)
        else:
            address_to_encode = current_ram_address
            asm_symbol_table.addEntry(extracted_var_name, current_ram_address)
            current_ram_address += (
                1  # Select next free ram address for the next variable
            )

        output_file_commands.append(f"{address_to_encode:016b}".encode())

        if args.debug:
            print(
                f"A COMMAND: {asm_parser.get_current_command()}\tLABEL NAME: {extracted_var_name}"
            )
    elif command_type == Command.C_COMMAND:
        # Parse out parts of instruction
        dest = asm_parser.dest()
        comp = asm_parser.comp()
        jump = asm_parser.jump()

        if "M" in comp:
            "We need to load from memory instead of from A"
            a_bit = b"1"
        else:
            "Data comes from A register, not from memory"
            a_bit = b"0"

        # Lookup binary for all parts of the C-command.
        encoder = BinaryEncoder()
        dest_bits = encoder.lookup_dest(dest)
        comp_bits = encoder.lookup_comp(comp)
        jump_bits = encoder.lookup_jump(jump)

        # 111 = c command
        output_file_commands.append(b"111" + a_bit + comp_bits + dest_bits + jump_bits)

with open(args.output_filename, "wb") as output_file:
    output_file.write(b"\n".join(output_file_commands))
