.DEFAULT_GOAL := all

# === Rare Emerald branch build ===
# Keep the normal HGSS build system intact, but run the Rare Emerald source
# migration passes before tool/ROM generation.

include make/consts.mk
include make/common.mk
include make/warnings.mk
include make/config.mk
include make/calcrom.mk
include make/messages.mk
include make/game.mk
include make/graphics.mk
include make/fielddata.mk
include make/poketool.mk
include make/application.mk
include make/resource.mk
include make/sound.mk
include make/overlay.mk
include make/code.mk
include make/arm7.mk
include make/rom.mk

.PHONY: all tidy clean clean-tools tools patch_mwasmarm
.PHONY: main sub dsprot libsyscall sdk sdk9 sdk7
.PRECIOUS: $(ROM)

MAKEFLAGS += --no-print-directory

all:
	python tools/rare_emerald/prepatch_starter.py
	python tools/rare_emerald/apply_source_patches.py
	python tools/rare_emerald/apply_gameplay_v5.py
	python tools/rare_emerald/apply_gameplay_v6.py
	$(MAKE) tools
	$(MAKE) patch_mwasmarm
	$(MAKE) $(ROM)

tidy:
	@$(MAKE) -C lib/dsprot tidy
	@$(MAKE) -C lib/syscall tidy
	@$(MAKE) -C sub tidy
	@$(MAKE) -C arm7 tidy
	@$(MAKE) -C sdk tidy
	@$(MAKE) -C . tidy-main

clean:
	rm -rf $(BUILD_DIR)

clean-tools:
	$(MAKE) -C tools clean

tools:
	$(MAKE) -C tools

patch_mwasmarm:
	$(MWASM_PATCHER) -q $(MWASMARM)

main:
	$(MAKE) -C . main

sub:
	$(MAKE) -C sub

dsprot:
	$(MAKE) -C lib/dsprot

libsyscall:
	$(MAKE) -C lib/syscall

sdk:
	$(MAKE) -C sdk

sdk9:
	$(MAKE) -C sdk sdk9

sdk7:
	$(MAKE) -C sdk sdk7

arm7:
	$(MAKE) -C arm7

rom:
	$(MAKE) $(ROM)
