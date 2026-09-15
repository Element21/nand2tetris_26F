// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// D register - Load to do operations? General purpose?
// M register - Value of current selected memory address
// A register - Address of current selected thing
// Used as the address when reading from or writing to data memory
// Used as the target address (program position) of a jump
// Used to load a specific integer into another register

(MAIN)
@KBD // Lookup keyboard register address
D = M // M is value of memory at the keyboard register, put it into D to do operations

@keyPressed
D;JGT // Jump to keyPressed if value of D (current kdb value) is greater than zero

// Else, jump to noKeyPressed
@noKeyPressed
0;JMP


(keyPressed)
@i
M = 0 // i=0

(keyPressedLoop)
@i // Reselect i if coming from a jump
D = M // D = i
@8192 // Loop through all 8k 16bit pages
D = D-A // D=i-8192

// Check if loop complete
@MAIN
D;JEQ // If (i-8192)==0 goto MAIN again

// Walk through screen memory and set to 1 (filled)
@i
D = M // D = current iteration (i)

@SCREEN // Select start of screen memory (16 bits)

D = A+D // Increment screen address by value of i (shift to next 16 bits each loop) (ONLY SHIFT 1 BIT OVER EACH TIME BUT IT STILL WORKS)
A = D // Select the newly incremented address
M = -1 // Set all 16 bits of new address to 1 (black) (2s complement)

@i
M = M+1 // Increment loop counter (next 16 bit register)

@keyPressedLoop // again
0;JMP



(noKeyPressed)
@i
M = 0 // i=0

(noKeyPressedLoop)
@i // Reselect i if coming from a jump
D = M // D = i
@8192 // Loop through all 8k 16bit pages
D = D-A // D=i-8192

// Check if loop complete
@MAIN
D;JEQ // If (i-8192)==0 goto MAIN again

// Walk through screen memory and set to 0 (cleared)
@i
D = M // D = current iteration (i)

@SCREEN // Select start of screen memory (16 bits)
D = A+D // Increment screen address by value of i (shift to next 16 bits each loop)
A = D // Select the newly incremented address
M = 0 // Set all 16 bits to 0

@i
M = M+1 // Increment loop counter (next 16 bit register)

@noKeyPressedLoop // again
0;JMP