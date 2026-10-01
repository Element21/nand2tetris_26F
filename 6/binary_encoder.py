class BinaryEncoder:
    def __init__(self) -> None:
        "Translates Hack assembly language mnemonics into binary codes"
        self.dest_lookup = {
            "null": b"000",
            "M": b"001",
            "D": b"010",
            "MD": b"011",
            "A": b"100",
            "AM": b"101",
            "AD": b"110",
            "AMD": b"111",
        }

        self.comp_lookup = {
            # a=0
            "0": b"101010",
            "1": b"111111",
            "-1": b"111010",
            "D": b"001100",
            "A": b"110000",
            "!D": b"001101",
            "!A": b"110001",
            "-D": b"001111",
            "-A": b"110011",
            "D+1": b"011111",
            "A+1": b"110111",
            "D-1": b"001110",
            "A-1": b"110010",
            "D+A": b"000010",
            "D-A": b"010011",
            "A-D": b"000111",
            "D&A": b"000000",
            "D|A": b"010101",
            # a=1
            "M": b"110000",
            "!M": b"110001",
            "-M": b"110011",
            "M+1": b"110111",
            "M-1": b"110010",
            "D+M": b"000010",
            "D-M": b"010011",
            "M-D": b"000111",
            "D&M": b"000000",
            "D|M": b"010101",
        }

        self.jump_lookup = {
            "null": b"000",
            "JGT": b"001",
            "JEQ": b"010",
            "JGE": b"011",
            "JLT": b"100",
            "JNE": b"101",
            "JLE": b"110",
            "JMP": b"111",
        }

    def lookup_dest(self, mnemonic: str) -> bytes:
        "Returns the binary code of the dest mnemonic"
        try:
            return self.dest_lookup[mnemonic]
        except KeyError:
            raise ValueError(f"Invalid dest mnemonic: '{mnemonic}'")

    def lookup_comp(self, mnemonic: str) -> bytes:
        "Returns the binary code of the comp mnemonic"
        try:
            return self.comp_lookup[mnemonic]
        except KeyError:
            raise ValueError(f"Invalid comp mnemonic: '{mnemonic}'")

    def lookup_jump(self, mnemonic: str) -> bytes:
        "Returns the binary code of the jump mnemonic"
        try:
            return self.jump_lookup[mnemonic]
        except KeyError:
            raise ValueError(f"Invalid jump mnemonic: '{mnemonic}'")
