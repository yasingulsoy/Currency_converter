# manager.py - Kullanıcı ile etkileşimi yönetir

from CurrencyAPI import CurrencyAPI
from CurrencyConverter import CurrencyConverter
from Logger import Logger

class CurrencyManager:
    def __init__(self):
        self.rates = CurrencyAPI.get_exchange_rates()
        self.converter = CurrencyConverter(self.rates)

    def show_rates(self):
        """Güncel döviz kurlarını ekrana yazdırır."""
        print("\nGüncel Kurlar (TRY bazında):")  
        if "TRY" in self.rates:
            for currency, rate in self.rates.items():
                print(f"1 {currency} = {rate / self.rates['TRY']:.2f} TRY")  

    def convert_currency(self):
        #Kullanıcının döviz dönüşümü yapmasını sağla
        source_currency = input("Dönüştürülecek kuru giriniz (örn. USD): ").strip().upper()  
        target_currency = input("Hedef kuru giriniz (örn. TRY): ").strip().upper()  
        try:
            amount = float(input("Dönüştürülecek miktarı giriniz: "))  
            result = self.converter.convert(amount, source_currency, target_currency)
            if result is not None:
                print(f"{amount} {source_currency} = {result:.2f} {target_currency}")  
            else:
                print("Geçersiz kur kodu girdiniz!")  
        except ValueError:
            print("Geçersiz miktar. Lütfen sayı giriniz.")  

    def get_currency_info(self):
        #Belirtilen kurun detaylarını getir
        currency_code = input("Bilgilerini almak istediğiniz kuru giriniz (örn. USD): ").strip().upper()  
        data = CurrencyAPI.get_currency_info(currency_code)

        if data and "TRY" in data['rates']:
            rate_try = data['rates']['TRY']
            print(f"\n{currency_code} için güncel bilgiler:")  
            print(f"1 {currency_code} = {rate_try:.2f} TRY")  
        else:
            print("Geçersiz veya desteklenmeyen kur kodu.")  

    def show_history(self):
        Logger.show_history()

    def menu(self):
        while True:
            print("\n1. Kur dönüşümü yap")  
            print("2. Belirli kur bilgisini getir")  
            print("3. Güncel kurları göster")  
            print("4. Geçmiş işlemleri görüntüle")  
            print("5. Çıkış")  

            choice = input("Seçiminizi yapın: ")  
            if choice == "1":
                self.convert_currency()
            elif choice == "2":
                self.get_currency_info()
            elif choice == "3":
                self.show_rates()
            elif choice == "4":
                self.show_history()
            elif choice == "5":
                print("Çıkış yapılıyor...")  
                break
            else:
                print("Geçersiz seçim, lütfen tekrar deneyin.")  
