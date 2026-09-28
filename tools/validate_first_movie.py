#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

errors: list[str] = []
warnings: list[str] = []


def check_file(rel: str) -> Path:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing required file: {rel}")
    return path


first_movie = check_file("include/constants/first_movie.h")
trainers_h = check_file("include/constants/trainers.h")
trainers_json = check_file("files/poketool/trainer/trainers.json")
title_c = check_file("src/title_screen.c")
title_mk = check_file("files/demo/title/titledemo.mk")

if first_movie.exists():
    txt = first_movie.read_text(encoding="utf-8")
    m = re.search(r"#define\s+VAR_FIRST_MOVIE_CHAPTER\s+(0x[0-9A-Fa-f]+)", txt)
    if not m:
        errors.append("VAR_FIRST_MOVIE_CHAPTER is not defined")
    elif m.group(1).lower() == "0x40fc":
        errors.append("campaign state still collides with stock VAR_UNK_40FC")
    elif m.group(1).lower() != "0x40fd":
        warnings.append(f"campaign state moved to unexpected variable {m.group(1)}")

if trainers_h.exists() and trainers_json.exists():
    h = trainers_h.read_text(encoding="utf-8")
    data = json.loads(trainers_json.read_text(encoding="utf-8"))
    count = len(data.get("trainers", []))
    m = re.search(r"#define\s+LAST_TRAINER_INDEX\s+(\d+)", h)
    if not m:
        errors.append("LAST_TRAINER_INDEX not found")
    else:
        expected = int(m.group(1))
        if count != expected:
            errors.append(f"trainer table count {count} != LAST_TRAINER_INDEX {expected}")

if title_c.exists():
    txt = title_c.read_text(encoding="utf-8")
    for token in [
        "NARC_titledemo_titledemo_00000044_NCGR",
        "NARC_titledemo_titledemo_00000045_NSCR",
        "NARC_titledemo_titledemo_00000046_NCLR",
        "NARC_titledemo_titledemo_00000047_NCGR",
        "NARC_titledemo_titledemo_00000048_NSCR",
        "NARC_titledemo_titledemo_00000049_NCLR",
        "SPECIES_MEWTWO",
    ]:
        if token not in txt:
            errors.append(f"title integration token missing: {token}")

if title_mk.exists():
    txt = title_mk.read_text(encoding="utf-8")
    for n in range(44, 50):
        token = f"titledemo_{n:08d}"
        if token not in txt:
            errors.append(f"title build resource missing: {token}")

for rel in [".first_movie/title/top.png", ".first_movie/title/bottom.png"]:
    path = ROOT / rel
    if not path.exists():
        warnings.append(f"local title source not staged yet: {rel}")

print("=== First Movie preflight ===")
if warnings:
    print("\nWarnings:")
    for item in warnings:
        print(f"  - {item}")

if errors:
    print("\nFAILED:")
    for item in errors:
        print(f"  - {item}")
    sys.exit(1)

print("\nPASS: repository consistency checks completed.")
print("Next build command: make COMPARE=0")
