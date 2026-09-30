from typing import TextIO


class HackAssembler():
    def __init__(self, input_filename: TextIO, debug: bool):
        self.input_filename = input_filename
        self.debug = debug


    def openInput(self):
        with open(self.input_filename, "r") as f:
            try:
                self.input_asm: list[str] = f.read().splitlines()
            except FileNotFoundError as e:
                print(f'Cannot find the file "{args.input_filename}"')


    def clean_input_asm(self):
        cleaned_input_asm = []
        for line_asm_contents in self.input_asm:
            # # Remove spaces
            # I write my assignments as "D = M" so we need to strip those spaces, also weird tabs or maybe other stuff from formatted comments?
            line_asm_contents = line_asm_contents.format_map({" ": "", "\t": ""})

            # # Is the line empty before or after removing spaces, tabs, other whitespace chars? Dont want it
            if len(line_asm_contents) == 0:
                continue  # Skip to next line without adding it to cleaned

            # # Try and remove comments next
            forward_slash_idx = line_asm_contents.find("/")

            # Check if a comment doesn't exist
            if forward_slash_idx == -1:
                cleaned_input_asm.append(line_asm_contents)
                continue  # Skip all other cleaning, but add to cleaned

            if forward_slash_idx == 0:
                "If slash is at the beginning, ditch the entire line"
                continue
            else:
                "Else, Keep only the code part"
                cleaned_line_asm_contents = line_asm_contents[: forward_slash_idx - 1]  # - 1 because end char should not be included
                cleaned_input_asm.append(cleaned_line_asm_contents)

        print(f"\n\nCLEANED:\n{cleaned_input_asm}")
