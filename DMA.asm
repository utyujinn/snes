 .macro LoadPalette
 pha
 php

 rep	#$20		; 16bit A
 lda	#\3
 sta	$4305		; # of bytes to be copied
 lda	#\1		; offset of data into 4302, 4303
 sta	$4302
 sep	#$20		; 8bit A

 lda	#:\1		; bank address of data in memory(ROM)
 sta	$4304
 lda	#\2
 sta	$2121		; address of CGRAM to start copying graphics to

 stz	$4300		; 0= 1 byte increment (not a word!)
 lda	#$22
 sta	$4301		; destination 21xx   this is 2122 (CGRAM Gate)

 lda	#$01		; turn on bit 1 (corresponds to channel 0) of DMA channel reg.
 sta	$420b		;   to enable transfer

 plp
 pla
 .endm
;macro for loading graphics data into the VRAM
 ;only use if SIZE is less than 256 bytes
 ;syntax LoadVRAM LABEL  VRAM_ADDRESS  SIZE
 .macro LoadVRAM

 pha			; save the current accumulator, Y index and status registers for the time the function is executed.
 phy
 php
 
 rep	#$20		; set the accumulator (A) register into 16 bit mode
 sep	#$10		; set the index (X and Y) register into 8 bit mode

 ldy	#$80		;  we will try to write 128 ($80) bytes in one row ...
 sty	$2115		; ... and we will let the PPU let this know.

 lda	#\2		; the controller will get the hardware register ($2118) as location to where to write the data.
 sta	$2116		; but we still need to specify WHERE in VRAM we want to write the data - what we are doing right now.

 lda	#\3		; number of bytes to be sent from the controller.
 sta	$4305

 sep	#$20		; set the accumulator (A) register into 8 bit mode

 lda.w	#\1		; from where the data is supposed to be loaded from		
 sta	$4302
 
 ldy	#:\1		; from which bank the data is supposed to be loaded from
 sty	$4304

 ldy	#$01		; set the mode on how the channel is supposed to do it's work. 1= word increment
 sty	$4300

 ldy	#$18		; remember that I wrote "the controller will get the hardware register"? This is it. 2118 is the VRAM gate.
 sty	$4301
 
 ldy	#$01		; turn on bit 1 (channel 0) of DMA - that is, start rollin'
 sty	$420b
  
 plp			; Restore the state of all registers before leaving the function.
 ply
 pla
 .endm
