Main.smc: Main.asm Main.link
	wla-65816 -o Main.obj Main.asm
	wlalink Main.link Main.smc
