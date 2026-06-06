class TelegramRuntime:
    def handle_message(self, message):
        return {"integration": "telegram", "message": message, "status": "received"}

telegram_runtime = TelegramRuntime()\n