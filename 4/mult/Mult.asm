// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

@R2
M = 0 // Clear R2

@sum
M = 0 // Clear sum

@R0
D = M // Load value into D

@R1
D = D-M // > 0, R0 bigger, else R1 bigger

@SETUP_R0_BIGGER
D;JGT // > 0, R0 bigger

@SETUP_R1_BIGGER
0;JMP // else, R1 bigger

(SETUP_R0_BIGGER)
// // R0 bigger, loop R1 times
@R1
D = M
@addTimes
M = D // loop counter = R1 value
@R0_BIGGER
0;JMP

(SETUP_R1_BIGGER)
// // R1 bigger, loop R0 times
@R0
D = M
@addTimes
M = D // loop counter = R0 value
@R1_BIGGER
0;JMP


(R0_BIGGER)
// Check if loop complete
@addTimes
D = M
// Check if addTimes is 0 (add R1 times)
@LOAD_RESULT_FROM_SUM
D;JEQ // Jump to end if loop is finished (multiplication complete)

// Decrement addTimes
@addTimes
M = M - 1

// Add R0 to sum
@R0
D = M // Get R0
@sum
M = D+M // Add R0 to sum

@R0_BIGGER
0;JMP


(R1_BIGGER)
// Check if loop complete
@addTimes
D = M
// Check if addTimes is 0 (add R0 times)
@LOAD_RESULT_FROM_SUM
D;JEQ // Jump to end if loop is finished (multiplication complete)

// Decrement addTimes
@addTimes
M = M - 1

// Add R1 to sum
@R1
D = M // Get R1
@sum
M = D+M // Add R1 to sum

@R1_BIGGER
0;JMP


(LOAD_RESULT_FROM_SUM)
@sum
D = M
@R2
M = D

@END
0;JMP


(END)
@END
0;JMP