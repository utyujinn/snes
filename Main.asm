; SNES Initialization Tutorial code(https://en.wikibooks.org/wiki/Super_NES_Programming/Initialization_Tutorial)
.include "Header.inc"
.include "Snes_Init.asm"
.include "DMA.asm"

; Needed to satisfy interrupt definition in "Header.inc".
VBlank:
    RTI

.bank 0
.section "MainCode"

Start:
    Snes_Init

    ; --- Turn screen off before VRAM/CGRAM access ---
    lda #%10000000  ; Force VBlank by turning off the screen.
    sta $2100

    ; --- Load our data into SNES memory ---
    LoadPalette Palette $00 PaletteEnd-Palette
    LoadVRAM MyTile, $0000, TileEnd-MyTile
    LoadVRAM MyMap, $4000, MapEnd-MyMap

    ; --- Configure PPU for BG1 Display ---
    sep #$20        ; Set A register to 8-bit.
    lda #%00000001  ; Set BG Mode 1 (allows for 16-color backgrounds).
    sta $2105
    lda #%00000001  ; Enable BG1 on the main screen.
    sta $212C
    ; Set VRAM location for the BG1 Tilemap.
    ; Destination is $1000. Address is in 2KB blocks ($1000 / $800 = 2).
    lda #$40
    sta $2107       ; BG1SC: BG1 Screen Base & Size.
    ; Set VRAM location for BG Tile Data.
    ; We put our tiles at $0000. Address is in 8KB blocks.
    lda #$00
    sta $210B       ; BG12NBA: BG1/2 Name Base Address.

    ; --- Turn screen on ---
    lda #%00001111  ; End force VBlank, setting brightness to 15 (100%).
    sta $2100

Forever:
    jmp Forever
.ends

; ===============================================================
; DATA - Graphics and color data goes here
; ===============================================================
.section "GraphicsData" SEMIFREE

Palette:
;.db $00, $00, $1F, $00, $00, $7C, $FF, $7F
;.end

;Palette:
    ; SNES colors are 15-bit: 0BBBBBGGGGGRRRRR
    .DB %00000000, %00000000,%00011111,%00000000,%11100000,%00000011,%00000000,%01111100
    .DB %00000000, %00000000,%00011111,%00000000,%11100000,%00000011,%00000000,%01111100
    .DB %00000000, %00000000,%00011111,%00000000,%11100000,%00000011,%00000000,%01111100
    .DB %00000000, %00000000,%00011111,%00000000,%11100000,%00000011,%00000000,%01111100
    ;.word $0000  ; Color 0: Transparent Black
    ;.word $001F  ; Color 1: Red   (%0000000000011111)
    ;.word $7C00  ; Color 2: Blue  (%0111110000000000)
    ;.word $7FFF  ; Color 3: White (%0111111111111111)
PaletteEnd:

MyTile:
    ; 8x8 pixel tile, 4 bits per pixel (16 colors)
    ; This creates a checkerboard of color 1 (Red) and color 2 (Blue).
    ; A 4bpp tile is 32 bytes total.
    ; Plane 0 (bit 0 of color index)
    .byte %10101010, %01010101, %10101010, %01010101, %10101010, %01010101, %10101010, %01010101
    ; Plane 1 (bit 1 of color index)
    .byte %01010101, %10101010, %01010101, %10101010, %01010101, %10101010, %01010101, %10101010
    ; Plane 2 (bit 2 of color index)
    .byte $00,$00,$00,$00,$00,$00,$00,$00
    ; Plane 3 (bit 3 of color index)
    .byte $00,$00,$00,$00,$00,$00,$00,$00
    .byte $00 $FF $7E $81 $7E $81 $7E $81 $7E $81 $7E $81 $7E $81 $00 $FF
    .byte $00 $FF $7E $81 $7E $81 $7E $81 $7E $81 $7E $81 $7E $81 $00 $FF
TileEnd:

MyMap:
    ; A 32x32 tilemap. Each entry is a word.
    ; Format: VHOo PPPP TTTT TTTT
    ; V=VFlip, H=HFlip, O=Priority, P=Palette, T=Tile Index
    ; We fill the screen with Tile #1, using Palette 0.
    .rept 32*16
    .word $0000 ; Use Tile #1, Palette 0, Prio 0, No flip
    .endr
    .rept 32*16
    .word $0001 ; Use Tile #1, Palette 0, Prio 0, No flip
    .endr
MapEnd:

.ends
