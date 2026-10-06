# Supply a GNU ARM Embedded toolchain for objcopy, ar, etc.

# On native MSYS2/UCRT64, use the standard devkitPro path directly instead of
# relying on PATH propagation through recursive make invocations.
ifneq ($(filter MSYS MINGW32 MINGW64 UCRT64 CLANG64 CLANGARM64,$(MSYSTEM)),)
# Ignore devkitPro's Unix-style /opt/devkitpro environment value under native
# Windows MSYS2. This project uses the standard Windows install at C:\devkitPro.
DEVKITPRO := /c/devkitPro
DEVKITARM := $(DEVKITPRO)/devkitARM
TOOLCHAIN := $(DEVKITARM)
PREFIX := $(TOOLCHAIN)/bin/arm-none-eabi-
else
ifdef DEVKITARM
TOOLCHAIN := $(DEVKITARM)
endif
ifdef TOOLCHAIN
export PATH := $(TOOLCHAIN)/bin:$(PATH)
endif
PREFIX := arm-none-eabi-
endif

OBJCOPY := $(PREFIX)objcopy
AR      := $(PREFIX)ar
