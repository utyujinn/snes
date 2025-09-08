build/Main.smc: Main.asm Main.link | build
	wla-65816 -o build/Main.obj Main.asm
	wlalink Main.link build/Main.smc

build:
	@mkdir -p build

.PHONY: clean

clean:
	rm -rf build

