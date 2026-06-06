#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    print("Q-Verse V12 runtime bootstrap is delegated to scripts/qverse_forge.py")
    print(f"Project root: {ROOT}")


if __name__ == "__main__":
    main()
