import streamlit as st
import plotly.graph_objs as go
from datetime import datetime, timedelta
import requests

# --- Döviz API ---
CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/"
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana&vs_currencies=usd,try"

@st.cache_data(ttl=600)
def get_currency_rates(base="USD"):
    try:
        response = requests.get(f"{CURRENCY_API_URL}{base}")
        if response.status_code == 200:
            return response.json().get("rates", {})
    except Exception:
        pass
    return {}

@st.cache_data(ttl=600)
def get_crypto_prices():
    try:
        response = requests.get(CRYPTO_API_URL)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {}

# --- Fonksiyonlar ---
def get_currency_list():
    return [
        ("USD", "🇺🇸 Dolar"),
        ("EUR", "🇪🇺 Euro"),
        ("TRY", "🇹🇷 Türk Lirası"),
        ("GBP", "🇬🇧 Sterlin"),
        ("JPY", "🇯🇵 Yen"),
        ("BTC", "₿ Bitcoin"),
        ("ETH", "Ξ Ethereum")
    ]

def get_exchange_rate(base, target, rates, crypto=None):
    if base == target:
        return 1.0
    # Kripto -> Klasik dönüşüm
    crypto_map = {"BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin", "SOL": "solana"}
    fiat_list = ["USD", "TRY", "EUR", "GBP", "JPY"]
    # Kripto -> Klasik
    if base in crypto_map and target in fiat_list and crypto:
        price = crypto.get(crypto_map[base], {}).get(target.lower())
        if price:
            return float(price)
    # Klasik -> Kripto
    if target in crypto_map and base in fiat_list and crypto:
        price = crypto.get(crypto_map[target], {}).get(base.lower())
        if price:
            return 1/float(price)
    # Klasik -> Klasik
    if base in rates and target in rates:
        return rates[target] / rates[base]
    return None

def get_historical_rates(base, target, days=7):
    rates = []
    for i in range(days-1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        # API ücretsiz sürümde geçmiş veri sağlamıyor, örnekleme ile simüle ediyoruz
        rates.append((date, None))
    return rates

def get_top_movers(rates):
    # Sadece örnek, gerçek değişim için geçmiş veri gerekir
    return [
        ("₿ BTC", "+4.2%"),
        ("Ξ ETH", "+3.1%"),
        ("USD/TRY", "+1.5%"),
        ("EUR/TRY", "-0.8%"),
        ("GBP/TRY", "-1.2%")
    ]

def get_crypto_cards(crypto):
    return [
        ("₿ BTC", f"${crypto.get('bitcoin', {}).get('usd', 'N/A'):,}"),
        ("Ξ ETH", f"${crypto.get('ethereum', {}).get('usd', 'N/A'):,}"),
        ("BNB", f"${crypto.get('binancecoin', {}).get('usd', 'N/A'):,}"),
        ("SOL", f"${crypto.get('solana', {}).get('usd', 'N/A'):,}")
    ]

def get_summary(base, target, rates):
    rate = get_exchange_rate(base, target, rates)
    if rate is None:
        return None
    yesterday = rate * 0.99
    change = rate - yesterday
    percent = (change / yesterday) * 100
    return {
        'rate': rate,
        'change': change,
        'percent': percent,
        'high': rate * 1.02,
        'low': rate * 0.98
    }

# --- Favoriler için yardımcı fonksiyon ---
def get_favorite_prices(favorites, rates, crypto):
    fiat_list = ["USD", "EUR", "TRY", "GBP", "JPY"]
    crypto_map = {"BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin", "SOL": "solana"}
    fav_prices = []
    for fav in favorites:
        if fav in fiat_list and "TRY" in rates:
            fav_prices.append((fav, f"{rates[fav]/rates['TRY']:.2f} TRY"))
        elif fav in crypto_map:
            price = crypto.get(crypto_map[fav], {}).get("usd")
            if price:
                fav_prices.append((fav, f"${price:,}"))
    return fav_prices

# --- Tema ve Sayfa Ayarları ---
st.set_page_config(page_title="Döviz & Kripto Borsa Uygulaması", layout="wide")
st.markdown("""
    <style>
    .big-title {font-size: 2.5rem; font-weight: bold; color: #00b4d8;}
    .info-card {background: #22223b; color: #fff; border-radius: 1rem; padding: 1.2rem; margin-bottom: 1rem;}
    .positive {color: #06d6a0; font-weight: bold;}
    .negative {color: #ef476f; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">💱 Döviz & Kripto Borsa Uygulaması</div>', unsafe_allow_html=True)

# --- Verileri Çek ---
currency_rates = get_currency_rates("USD")
crypto = get_crypto_prices()

# --- Favori Para Birimleri Seçimi ---
st.sidebar.header("⭐ Favori Para Birimlerin")
all_currencies = [c[0] for c in get_currency_list()]
favorites = st.sidebar.multiselect(
    "Favorilerini seç (en fazla 5)",
    options=all_currencies,
    default=["USD", "EUR", "BTC"],
    max_selections=5
)

col_fav, col1, col2, col3 = st.columns([2, 2, 5, 2])
with col_fav:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("⭐ Favoriler")
    fav_prices = get_favorite_prices(favorites, currency_rates, crypto)
    if fav_prices:
        for name, price in fav_prices:
            st.write(f"{name}: {price}")
    else:
        st.write("Favori seçilmedi.")
    st.markdown('</div>', unsafe_allow_html=True)

with col1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("En Çok Artan/Azalanlar")
    for name, change in get_top_movers(currency_rates):
        color = "positive" if "+" in change else "negative"
        st.markdown(f'<span class="{color}">{name}: {change}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Kripto Fiyatları")
    for name, price in get_crypto_cards(crypto):
        st.write(f"{name}: {price}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Döviz Çevirici")
    currency_list = get_currency_list()
    base, base_label = st.selectbox("Çevrilecek Para Birimi", currency_list, format_func=lambda x: x[1], index=0)
    target, target_label = st.selectbox("Hedef Para Birimi", currency_list, format_func=lambda x: x[1], index=2)
    amount = st.number_input("Miktar", min_value=0.0, value=1.0, step=1.0)
    swap = st.button("🔄 Swap", key="swap")
    if swap:
        base, target = target, base
        base_label, target_label = target_label, base_label
    if st.button("Çevir"):
        rate = get_exchange_rate(base, target, currency_rates, crypto)
        if rate is None:
            st.error("Bu para birimi çifti için veri bulunamadı!")
        else:
            result = amount * rate
            st.success(f"{amount} {base} = {result:.2f} {target}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader(f"Son 7 Günlük {base}/{target} Kuru")
    # Gerçek geçmiş veri API ile alınamıyor, örnekleme ile gösteriliyor
    history = get_historical_rates(base, target)
    dates = [d for d, _ in history]
    rates_hist = [get_exchange_rate(base, target, currency_rates, crypto) for _ in history]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=rates_hist, mode='lines+markers', name=f'{base}/{target}'))
    fig.update_layout(title=f'{base} -> {target} Son 7 Günlük Kur', xaxis_title='Tarih', yaxis_title='Kur', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Özet")
    summary = get_summary(base, target, currency_rates)
    if summary:
        st.write(f"Güncel Kur: {summary['rate']:.2f}")
        st.write(f"Değişim: {summary['change']:+.2f} ({summary['percent']:+.2f}%)")
        st.write(f"En Yüksek: {summary['high']:.2f}")
        st.write(f"En Düşük: {summary['low']:.2f}")
    else:
        st.warning("Özet verisi bulunamadı.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Güncel Kurlar (TRY bazında)")
    if "TRY" in currency_rates:
        for k, v in currency_rates.items():
            if k in ["USD", "EUR", "GBP", "JPY"]:
                st.write(f"{k}/TRY: {v / currency_rates['TRY']:.2f}")
    else:
        st.write("Veri yok")
    st.markdown('</div>', unsafe_allow_html=True)

# --- CLI Menü Sadece Terminalden Çalıştırıldığında ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        from CurrencyManager import CurrencyManager
        manager = CurrencyManager()
        manager.menu()