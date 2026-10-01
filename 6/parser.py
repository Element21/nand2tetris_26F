from command import Command


class Parser:
    def __init__(self, input_filename: str) -> None:
        "Opens the input file/stream and gets ready to parse it."
        self.input_filename: str = input_filename
        self.commands: list[str] = []
        self.current_command_idx: int = -1  # Call advance to begin reading

        # # Open if file exists
        with open(self.input_filename, "r") as f:
            try:
                _input_asm: list[str] = f.read().splitlines()
            except FileNotFoundError:
                raise FileNotFoundError(f'Cannot find the file "{self.input_filename}"')

        # # Clean input file
        for _dirty_line in _input_asm:  # pyright: ignore[reportPossiblyUnboundVariable]
            # Trim whitespace on edges, remove spaces
            _clean_line = _dirty_line.strip().replace(" ", "")
            _no_comments = _clean_line.split("//")[0]  # Keep only chars before "//"

            if len(_no_comments) > 0:
                "Add only non-empty lines"
                self.commands.append(_no_comments)

    def has_more_commands(self) -> bool:
        "Are there more commands in the input?"
        if (self.current_command_idx + 1) < len(self.commands):
            "Check if next index is within bounds of the cleaned `commands` list"
            return True
        else:
            return False

    def advance(self) -> None:
        "Reads the next command from the input and makes it the current command. Should be called only if hasMoreCommands() is true. Initially there is no current command"
        self.current_command_idx += 1

    def reset_command_idx(self) -> None:
        self.current_command_idx = -1

    def get_current_command(self) -> str:
        "Get the command at a Parser's current index"

        if self.current_command_idx < 0:
            raise AssertionError(
                "This Parser is uninitialized! Advance to read first command!"
            )

        return self.commands[self.current_command_idx]

    def get_command_type(self) -> Command:
        """
        Returns the type of the current command:
                A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
                C_COMMAND for dest=comp;jump
                L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.
        """
        if self.get_current_command().startswith("@"):
            "Identify commands selecting addresses"
            return Command.A_COMMAND
        elif self.get_current_command().startswith("("):
            "Indentify commands defining labels"
            return Command.L_COMMAND
        else:
            return Command.C_COMMAND

    def symbol(self) -> str:
        """
        Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
        Should be called only when commandType() is A_COMMAND or L_COMMAND
        """

        if self.get_command_type() == Command.A_COMMAND:
            "Get everything after @"
            return self.get_current_command().split("@")[1]
        elif self.get_command_type() == Command.L_COMMAND:
            return self.get_current_command().replace("(", "").replace(")", "")

        return ""

    def dest(self) -> str:
        """
        Returns the dest mnemonic in the current C-command.
        Should be called only when commandType() is C_COMMAND.
        """

        # Take everything before =, or use the null destination
        if "=" in self.get_current_command():
            return self.get_current_command().split("=", 1)[0]
        else:
            return "null"

    def comp(self) -> str:
        """
        Returns the comp mnemonic in the current C-command.
        Should be called only when commandType() is C_COMMAND.

        dest=comp;jump
            1. dest=comp
            or
            2. comp;jump
            or
            3. MD=D+1;JEQ
        """

        _command = self.get_current_command()

        if "=" in _command:
            """
            Get right side of equals sign (source)
            M=D+1 -> D+1
            """
            _command = _command.split("=")[1]

        if ";" in _command:
            "If there is a jump part, remove it. Leaving only comp"
            _command = _command.split(";")[0]

        return _command

    def jump(self) -> str:
        """
        dest=comp;jump
        comp;jump

        Returns the jump mnemonic in the current C-command.
        Should be called only when commandType() is C_COMMAND.
        """
        if ";" in self.get_current_command():
            "take right side of ;, or use the null jump instruction"
            return self.get_current_command().split(";")[1]
        else:
            return "null"
