import json
from pathlib import Path


class SecretStore:
    def __init__(self, path="data/qverse_secrets.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8") or "{}")

    def save_secret(self, name, value):
        data = self.load()
        data[name] = value
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"name": name, "configured": bool(value), "masked": self.mask(value)}

    def get_secret(self, name):
        return self.load().get(name)

    def list_secrets(self):
        data = self.load()
        return {name: {"configured": bool(value), "masked": self.mask(value)} for name, value in data.items()}

    def mask(self, value):
        if not value:
            return ""
        if len(value) <= 8:
            return "****"
        return value[:4] + "..." + value[-4:]


secret_store = SecretStore()
