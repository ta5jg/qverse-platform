#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = {
    "api/managers/marketplace_manager.py": """from api.services.marketplace_service import marketplace_service\n\nclass MarketplaceManager:\n    def list_items(self):\n        return marketplace_service.list_items()\n\n    def get_dashboard(self):\n        items = self.list_items()\n        return {\"items\": items, \"total\": len(items)}\n\n    def get_metrics(self):\n        return marketplace_service.metrics()\n\nmarketplace_manager = MarketplaceManager()\n""",

    "api/services/marketplace_service.py": """from api.repositories.marketplace_repository import marketplace_repository\n\nclass MarketplaceService:\n    def list_items(self):\n        return marketplace_repository.list_all()\n\n    def metrics(self):\n        return {\"service\": \"marketplace_service\", \"total_items\": marketplace_repository.count()}\n\nmarketplace_service = MarketplaceService()\n""",

    "api/repositories/marketplace_repository.py": """class MarketplaceRepository:\n    def __init__(self):\n        self._items = []\n\n    def list_all(self):\n        return self._items\n\n    def count(self):\n        return len(self._items)\n\nmarketplace_repository = MarketplaceRepository()\n""",
}


def write_file(path: str, content: str, force: bool = False):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)

    if force or not target.exists() or target.stat().st_size == 0:
        target.write_text(content, encoding="utf-8")
        print(f"[WRITE] {path}")
    else:
        print(f"[SKIP] {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    print("Q-Verse Marketplace Bootstrap Started")

    for path, content in FILES.items():
        write_file(path, content, args.force)

    print("Q-Verse Marketplace Bootstrap Complete")