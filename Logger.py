import datetime
import os

class Logger:
    LOG_FILE = "data/history.txt"

    @staticmethod
    def log_conversion(amount, source_currency, target_currency, result):
        """Bir döviz dönüşüm işlemini kaydeder."""
        os.makedirs("data", exist_ok=True)
        with open(Logger.LOG_FILE, "a") as file:
            file.write(f"[{datetime.datetime.now()}] {amount} {source_currency} -> {result:.2f} {target_currency}\n")

    @staticmethod
    def log_message(message):
        os.makedirs("data", exist_ok=True)
        with open(Logger.LOG_FILE, "a") as file:
            file.write(f"[{datetime.datetime.now()}] {message}\n")

    @staticmethod
    def show_history():
        if os.path.exists(Logger.LOG_FILE):
            with open(Logger.LOG_FILE, "r") as file:
                print("\n=== Döviz Dönüşüm Geçmişi ===")  # Türkçe çıktı
                print(file.read())
        else:
            print("\nHenüz döviz dönüşüm geçmişi bulunmamaktadır.")  # Türkçe çıktı
