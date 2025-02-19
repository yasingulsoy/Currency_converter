import requests

class CurrencyAPI:
    BASE_URL = "https://api.exchangerate-api.com/v4/latest/"

    @staticmethod #nesne oluşturmadan çağırmak için kullandık
    def get_exchange_rates(base_currency="USD"):
        """Belirtilen baz kura göre döviz oranlarını getirir."""
        url = f"{CurrencyAPI.BASE_URL}{base_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('rates', {})
        return {}

    @staticmethod
    def get_currency_info(currency_code):
        #Belirli bir döviz biriminin ayrıntılı bilgileris
        url = f"{CurrencyAPI.BASE_URL}{currency_code.upper()}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
