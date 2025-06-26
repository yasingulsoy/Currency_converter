# Döviz & Kripto Borsa Uygulaması

Bu proje, **Streamlit** ile geliştirilmiş, gerçek zamanlı döviz ve kripto para verilerini kullanan modern bir döviz çevirici ve borsa uygulamasıdır. Tüm kurlar ve kripto fiyatları canlı olarak API üzerinden çekilmektedir.

## Özellikler
- Gerçek zamanlı döviz kurları (ExchangeRate API)
- Gerçek zamanlı kripto fiyatları (CoinGecko API)
- Anlık döviz çevirici
- Son 7 günlük kur grafiği (örnekleme ile)
- Modern ve şık arayüz (Streamlit)
- En çok artan/azalanlar ve kripto fiyatları kutuları
- Özet kutusu (güncel kur, değişim, en yüksek/düşük)
- Kolay kurulum ve kullanım

## Kurulum
1. Gerekli kütüphaneleri yükleyin:
   ```sh
   pip install streamlit plotly requests
   ```
2. Uygulamayı başlatın:
   ```sh
   streamlit run main.py
   ```

## Kullanım
- Para birimlerini seçin, miktarı girin ve "Çevir" butonuna tıklayın.
- Kripto fiyatları ve en çok artan/azalanlar sol kutuda, güncel kurlar sağ kutuda gösterilir.
- Orta alanda döviz çevirici, grafik ve özet kutusu bulunur.

## API Bilgisi
- Döviz kurları: [ExchangeRate API](https://www.exchangerate-api.com/)
- Kripto fiyatları: [CoinGecko API](https://www.coingecko.com/en/api)
- Ücretsiz API anahtarı gerektirmez, ancak yoğun kullanımda limit olabilir.

## Ekran Görüntüsü
> Buraya uygulamanın ekran görüntüsünü ekleyebilirsiniz.

## Katkı
Katkıda bulunmak için pull request gönderebilirsiniz.

## Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakınız.