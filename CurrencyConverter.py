from Logger import Logger

class CurrencyConverter:
    #Girilen miktarı belirtilen döviz kuruna çevir

    def __init__(self, rates):
        self.rates = rates

    def convert(self, amount, source_currency, target_currency):
        source_currency = source_currency.upper()
        target_currency = target_currency.upper()

        if source_currency in self.rates and target_currency in self.rates:
            converted_amount = amount * (self.rates[target_currency] / self.rates[source_currency])
            Logger.log_conversion(amount, source_currency, target_currency, converted_amount)
            return converted_amount
        return None
