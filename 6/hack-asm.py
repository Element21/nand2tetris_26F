#!/usr/bin/env python3

import argparse, string

from hack_assembler import HackAssembler

parser = argparse.ArgumentParser(
    prog="Hack Assembler",
    description="Given a hack assembly file, assemble it into machine code for the hack CPU to execute",
)

parser.add_argument("input_filename")
parser.add_argument("output_filename")
parser.add_argument("-d", "--debug", action="store_true")  # If set, args.debug is True

args = parser.parse_args()

myAssembler = HackAssembler()