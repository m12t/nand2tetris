// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// program flow:
// * the program will run exactly `R1` times and
//   add R0 to itself to perform the multiplication
// * NOTE: no optimizations are implemented here, such
//   as checking for zeros in either operand, or looping
//   over the smaller operand so less operations are performed, etc.

// ------------ pseudocode ------------
// loop:
//    if r1 == 0:
//        exit
//    r1 -= 1
//    r2 = r2 + r0
//    JMP loop
// ------------------------------------

// NOTES on HACK resigters:
// D: data register
// A: address register
// M: the selected RAM register


// initialize R2 to 0
@R2
M = 0

(LOOP)
    // if R1 == 0: exit
    @R1
    D = M  // set the data register to the value of R1
    M = M - 1
    @END
    D; JEQ  // by using D, if R1 == 0: exit

    @R0
    D = M  // we add R0 to itself exactly R1 times, so set the data register to the value of R0
    
    @R2
    M = M + D  // add the value of R0 to R2

    @LOOP
    0; JMP


(END)
    @END
    0; JMP  // infinite loop
