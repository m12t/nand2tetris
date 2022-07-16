// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// program flow:
// * Check the keyboard memory map for value != 0
// * paint the screen if keyboard detected, otherwise scrub paint

// ------------ pseudocode ------------

// loop:
//    if keyboard == 0:
//        JMP white
//    if keyboard != 0:
//        JMP black
//    JMP loop

// white:
//    set screen to all ones

// black:
//    set screen to all zeros
// ------------------------------------

// NOTES on HACK resigters:
// D: data register
// A: address register
// M: the selected RAM register

// I/O pointers: The symbols SCREEN and KBD are predefined to refer to RAM
// addresses 16384 (0x4000) and 24576 (0x6000), respectively, which are the base
// addresses of the screen and keyboard memory maps.

// set the ending index
@8192
D = A
@end
M = D

(LOOP)
    // reset the screen index (arr) to the beginning of the screen
    @offset
    M = 0

    // check the key value and paint accordingly
    @KBD
    D = M    // set the data register to the key code
    @PAINTBLACK
    D; JEQ   // if the key code == 0, paint black
    @PAINTWHITE
    D; JNE   // if the key code != 0, paint white


// (BLACK)
//     @color     // the "color" to paint
//     M = -1  // -1 is all ones in 2's complement, so all black
//     @PAINT
//     0; JMP


// (WHITE)
//     @color
//     M = 0
//     @PAINT
//     0; JMP

(PAINTWHITE)

    @offset
    D = M
    @end
    D = D - M  // end - current_offset
    @LOOP
    D; JEQ

    @SCREEN    // this holds the beginning screen index, 16384
    D = A      // the D register now holds the beginning screen index
    @offset
    A = D + M  // set the current index to Screen + offset
    M = 0

    @offset
    M = M + 1  // increment the offset by 1

    // the screen isn't yet painted, do another iteration
    @PAINTWHITE
    0; JMP


(PAINTBLACK)

    @offset
    D = M
    @end
    D = D - M  // end - current_offset
    @LOOP
    D; JEQ

    @SCREEN    // this holds the beginning screen index, 16384
    D = A      // the D register now holds the beginning screen index
    @offset
    A = D + M  // set the current index to Screen + offset
    M = -1

    @offset
    M = M + 1  // increment the offset by 1

    // the screen isn't yet painted, do another iteration
    @PAINTBLACK
    0; JMP
