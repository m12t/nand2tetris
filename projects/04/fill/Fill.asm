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
//    JMP paint(white)

// black:
//    set screen to all zeros
//    JMP paint(black)

// paint:
//    while index < keyboard:
//        value[index] = color
// ------------------------------------

// NOTES on HACK resigters:
// D: data register
// A: address register
// M: the selected RAM register

// I/O pointers: The symbols SCREEN and KBD are predefined to refer to RAM
// addresses 16384 (0x4000) and 24576 (0x6000), respectively, which are the base
// addresses of the screen and keyboard memory maps.


(LOOP)
    // reset the screen index (arr) to the beginning of the screen
    @SCREEN  // same as @16384 but better for readability and portability since SCREEN might not always be at 16384.
    D = A    // set the D register to the address of SCREEN, or 16384
    @index   // create a variable in ram called index
    M = D    // set the value of ram[index] to D, in this case, 16384

    // check the key value and paint accordingly
    @KBD     // same as @24576 but better for readability and portability since keyboard might not always be at 24576.
    D = M    // set the D register to the key code grabbed from the keyboard
    @BLACK
    D; JEQ   // if the key code == 0, paint black
    @WHITE
    D; JNE   // if the key code != 0, paint white


(BLACK)
    @color     // the "color" to paint
    M = -1     // -1 is all ones in 2's complement, so all black
    @PAINT
    0; JMP


(WHITE)
    @color
    M = 0      // 0 is all zeros in 2's complement, so all white
    @PAINT
    0; JMP


(PAINT)
    // the main loop to paint the screen
    @color
    D = M      // set the D register to the color specified earlier

    @index
    A = M      // set the D register to the color specified earlier
    M = D      // do the actual "paint" of the value by setting RAM[index] = color

    @index
    M = M + 1  // increment the index by 1 since a value was just painted
    D = M      // store this new index in the D register for use below

    @KBD
    D = A - D  // compare the KBD address, which is immediately following the last screen pixel, with the current index
    @LOOP
    D; JEQ     // if the index is at the keyboard, jump back to the main loop, else continue

    @PAINT
    0; JMP     // the screen isn't yet completely painted, do another iteration
