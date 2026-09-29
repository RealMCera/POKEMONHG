# Supply a GNU ARM Embedded toolchain for objcopy, ar, etc.

# On MSYS2/UCRT64, default to the standard devkitPro install location when
# DEVKITARM is not already exported by the shell.
ifneq ($(filter MSYS MINGW32 MINGW64 UCRT64 CLANG64 CLANGARM64,$(MSYSTEM)),)
ifndef DEVKITARM
DEVKITPRO ?= C:/devkitPro
DEVKITARM := $(DEVKITPRO)/devkitARM
endif
endif

ifdef DEVKITARM
TOOLCHAIN := $(DEVKITARM)
endif

ifdef TOOLCHAIN
export PATH := $(TOOLCHAIN)/bin:$(PATH)
endif

PREFIX := arm-none-eabi-

OBJCOPY := $(PREFIX)objcopy
AR      := $(PREFIX)ar
