#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "project_brain"
OUT.mkdir(parents=True, exist_ok=True)

now = datetime.now(timezone.utc).isoformat()

files = {
    "QVERSE_PROJECT_BIBLE.md": f"""# Q-Verse Project Bible

Created: {now}

## Core Vision

Q-Verse is not only a game, token, ecosystem, or agent.

Q-Verse is a living digital universe built around memory, learning, creativity, and evolving intelligence.

## Main Principle

We are not building a classic game engine.

We are building a Game Brain.

The Game Brain must learn from every player, every day, and generate new situations, new thoughts, new stories, and new worlds.

## Active Projects

1. Q-Verse Ecosystem
2. Q-Verse Game Brain
3. USDTg / Ecosystem Finance Layer
4. Nyrvexa
5. Kindrail

## Founder

Irfan Gedik
""",

    "QVERSE_GAME_BRAIN.md": f"""# Q-Verse Game Brain

Created: {now}

## Definition

Q-Verse Game Brain is the living intelligence layer of the game universe.

It should not depend on a ready-made game engine as its core logic.

## Core Capabilities

- Learn from each player
- Remember player actions
- Generate new situations
- Generate new thoughts
- Generate new world fragments
- Evolve NPC behavior
- Evolve storylines
- Protect world consistency
- Create new quests dynamically

## Main Loop

Player Action -> Observation -> Memory Update -> Meaning Extraction -> World State Update -> New Situation Generation -> Player Response -> Learning
""",

    "QVERSE_ROADMAP.md": f"""# Q-Verse Roadmap

Created: {now}

## Phase 1 — Project Brain

- Create permanent project documents
- Define project memory structure
- Define decision ledger
- Define task ledger
- Define Game Brain architecture

## Phase 2 — Game Brain Prototype

- Build QVerseGameBrain class
- Add player observation
- Add memory save/load
- Add worldte model
- Add simple situation generator
""",

    "QVERSE_DECISIONS.md": f"""# Q-Verse Decision Ledger

Created: {now}

## Decisions

### 001 — Agent development is no longer the main project

Q-Verse Agent may remain as a support tool, but the main direction is Q-Verse Project Brain and Q-Verse Game Brain.

### 002 — No ready-made game engine as the core brain

The core must be a new learning Game Brain.

### 003 — Project Brain first

Before building the game, the project needs a permanent memory and planning structure.
""",

    "QVERSE_TASKS.md": f"""# Q-Verse Task Ledger

Created: {now}

## Immediate Tasks

- [ ] Review Project Bible
- [ ] Expand Game Brain architecture
- [ ] Create first Python prototype for QVerseGameBrain
- [ ] Define player memory schema
- [ ] Define world state schema
- [ ] Define NPC mind schema
- [ ] Define first playable text-based simulation
"""
}

for name, content in files.items():
    path = OUT / name
    path.write_text(content, encoding="utf-8")
    print(f"[OK] ")

print("Q-Verse Project Brain documents created.")
