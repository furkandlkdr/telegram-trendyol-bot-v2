# [EN] Trendyol Price Tracking Bot

An advanced Telegram bot that tracks product prices on Trendyol and sends smart notifications when prices change. Designed for efficiency and reliability with enhanced user experience.

## ✨ Features

- 🔗 **Universal Link Support**: Works with both Trendyol.com and ty.gl (shortened) links
- ➕ **Easy Product Addition**: Use `/ekle` command or simply send a Trendyol link
- ➖ **Product Management**: Remove products with `/sil` command
- 📋 **Smart Listing**: View all tracked products with price trends using `/listele`
- 🔄 **Automated Price Monitoring**: Configurable interval-based price checking
- 🎯 **Smart Notifications**: 
  - 📈 "Price Increased" notifications with red indicator
  - 📉 "Price Decreased" notifications with green indicator
  - Detailed price difference and percentage change
- 🏠 **Multi-Group Support**: Restrict bot access to specific Telegram groups
- ⚡ **Optimized Performance**: Lightweight code perfect for Raspberry Pi and low-power devices
- 🛡️ **Enhanced Error Handling**: Robust error management and logging
- 🎨 **Rich Formatting**: HTML-formatted messages with clickable links

## 📋 Requirements

- **Python 3.6+** (Recommended: Python 3.8 or newer)
- **pip** (Python package manager)
- **Telegram Bot Token** (obtainable from [@BotFather](https://t.me/botfather))
- **Telegram Group ID(s)** for access control

## 🚀 Installation

### Quick Setup

1. **Clone the repository:**
```bash
git clone https://github.com/furkandlkdr/telegram-trendyol-bot.git
cd telegram-trendyol-bot
```

2. **Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your settings:

```env
# Telegram Bot Token from @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Price check interval in minutes (default: 30)
CHECK_INTERVAL=30

# Comma-separated list of allowed Telegram group IDs
ALLOWED_GROUP_IDS=-1001234567890,-1009876543210
```

5. **Start the bot:**
```bash
python main.py
```

## 🔧 Getting Group ID

To find your Telegram group ID:

1. Add the bot to your group
2. Send any message in the group
3. Visit: `https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates`
4. Look for `"chat":{"id": -1001234567890}` in the JSON response
5. Copy the negative number (including the minus sign)

## 📖 Usage Guide

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and show help | `/start` |
| `/ekle [URL]` | Add product to tracking | `/ekle https://www.trendyol.com/...` |
| `/sil [URL]` | Remove product from tracking | `/sil https://www.trendyol.com/...` |
| `/listele` | List all tracked products | `/listele` |

### Adding Products

**Method 1: Command**
```
/ekle https://www.trendyol.com/product-link
```

**Method 2: Direct Link**
Simply paste any Trendyol link in the group:
```
https://www.trendyol.com/your-product-link
https://ty.gl/shortened-link
```

### Product List Features

The `/listele` command shows:
- 📈 **Price increased** from initial price
- 📉 **Price decreased** from initial price  
- ➡️ **No change** in price
- Direct links to products
- Current vs initial price comparison

## 🔄 How It Works

1. **Product Addition**: Bot scrapes product name and current price
2. **Data Storage**: Information saved in `tracked_products.json`
3. **Scheduled Checks**: Bot checks prices every X minutes (configurable)
4. **Smart Notifications**: Only sends alerts when prices actually change
5. **Price Updates**: Database automatically updates with new prices

## 🐧 Automatic Startup (Linux/Raspberry Pi)

Create a systemd service for automatic startup:

```bash
sudo nano /etc/systemd/system/trendyol-bot.service
```

**Service configuration** (adjust paths for your setup):

```ini
[Unit]
Description=Trendyol Price Tracking Bot
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/telegram-trendyol-bot
ExecStart=/home/pi/telegram-trendyol-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable trendyol-bot.service
sudo systemctl start trendyol-bot.service
```

**Check status:**
```bash
sudo systemctl status trendyol-bot.service
```

## 📁 Project Structure

```
telegram-trendyol-bot/
├── main.py              # 🤖 Main bot logic and Telegram handlers
├── scraper.py           # 🕷️ Trendyol web scraping functionality
├── data_manager.py      # 💾 JSON data management (CRUD operations)
├── config.py           # ⚙️ Configuration and environment variables
├── requirements.txt    # 📦 Python dependencies
├── .env.example       # 📋 Environment variables template
├── .env              # 🔐 Your actual environment variables (create this)
├── tracked_products.json # 🗃️ Product database (auto-generated with bot)
└── README.md         # 📖 This documentation
```

### 🔧 Core Components

| File | Purpose | Key Functions |
|------|---------|---------------|
| `main.py` | Bot orchestration | Command handlers, price checking, notifications |
| `scraper.py` | Web scraping | Product info extraction, price parsing |
| `data_manager.py` | Data persistence | Add/remove products, price updates |
| `config.py` | Configuration | Environment variables, settings |

## 🔍 Technical Details

### Dependencies
- **python-telegram-bot 13.15**: Telegram Bot API wrapper
- **requests 2.31.0**: HTTP requests for web scraping
- **beautifulsoup4 4.12.2**: HTML parsing
- **lxml 4.9.3**: Fast XML/HTML parser
- **schedule 1.2.0**: Job scheduling
- **python-dotenv 1.0.0**: Environment variable management

### Key Features Implementation
- **Smart Price Detection**: Multiple selector fallbacks for robust price extraction
- **URL Validation**: Supports both full and shortened Trendyol links
- **Error Recovery**: Comprehensive error handling with logging
- **Memory Efficient**: Minimal resource usage, ideal for 24/7 operation
- **Thread Safety**: Proper threading for scheduler and bot operations

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if `TELEGRAM_BOT_TOKEN` is correct
- Verify group ID is in `ALLOWED_GROUP_IDS`
- Ensure bot has proper permissions in the group

**Price not detected:**
- Trendyol may have changed their HTML structure
- Check logs for scraping errors
- Try with different products

**Duplicate notifications:**
- Fixed with improved scheduler management
- Restart the bot if still occurring

**Memory issues on Raspberry Pi:**
- Reduce `CHECK_INTERVAL` to check less frequently
- Consider using swap if needed

### Logs and Debugging

Bot logs important events. Check console output for:
- Product addition/removal confirmations
- Price check results
- Error details
- Notification sending status

## ⚠️ Important Notes

- **Personal Use**: This bot is designed for personal/small group use
- **Rate Limiting**: Trendyol may implement anti-bot measures
- **Legal Compliance**: Ensure compliance with Trendyol's terms of service
- **Reliability**: While robust, web scraping can break if sites change structure
- **Privacy**: All data is stored locally in JSON format

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Documentation improvements
- Performance optimizations

## 🔗 Links

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/botfather) - Create your bot token
- [Trendyol](https://www.trendyol.com) - Supported e-commerce platform

---

# [TR] Trendyol Fiyat Takip Botu

Trendyol'daki ürün fiyatlarını takip eden ve fiyat değişikliklerinde akıllı bildirimler gönderen gelişmiş Telegram botu. Verimlilik ve güvenilirlik odaklı, geliştirilmiş kullanıcı deneyimi ile tasarlanmıştır.

## ✨ Özellikler

- 🔗 **Link Desteği**: Hem Trendyol.com hem de ty.gl (kısaltılmış) linklerle çalışır
- ➕ **Kolay Ürün Ekleme**: `/ekle` komutu kullanın veya direkt Trendyol linki gönderin-paylaşın
- ➖ **Ürün Yönetimi**: `/sil` komutu ile ürünleri kaldırın
- 📋 **Akıllı Listeleme**: `/listele` ile fiyat trendleriyle birlikte tüm takip edilen ürünleri görün
- 🔄 **Otomatik Fiyat İzleme**: Yapılandırılabilir aralıklarla fiyat kontrolü
- 🎯 **Akıllı Bildirimler**: 
  - 📈 Kırmızı gösterge ile "Fiyat Yükseldi" bildirimleri
  - 📉 Yeşil gösterge ile "Fiyat Düştü" bildirimleri
  - Detaylı fiyat farkı ve yüzde değişim bilgisi
- 🏠 **Çoklu Grup Desteği**: Bot erişimini belirli Telegram gruplarıyla sınırlayın
- ⚡ **Optimize Edilmiş Performans**: Raspberry Pi ve düşük güçlü cihazlar için mükemmel hafif kod
- 🛡️ **Gelişmiş Hata Yönetimi**: Sağlam hata yönetimi ve loglama
- 🎨 **Zengin Formatlama**: Tıklanabilir linklerle HTML formatlı mesajlar

## 📋 Gereksinimler

- **Python 3.6+** (Önerilen: Python 3.8 veya daha yeni)
- **pip** (Python paket yöneticisi)
- **Telegram Bot Token** ([@BotFather](https://t.me/botfather) üzerinden alınabilir)
- **Telegram Grup ID(leri)** erişim kontrolü için

## 🚀 Kurulum

### Hızlı Kurulum

1. **Repoyu klonlayın:**
```bash
git clone https://github.com/furkandlkdr/telegram-trendyol-bot.git
cd telegram-trendyol-bot
```

2. **Sanal ortam oluşturun ve etkinleştirin:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Çevre değişkenlerini yapılandırın:**
   - `.env.example` dosyasını `.env` olarak kopyalayın
   - `.env` dosyasını ayarlarınızla düzenleyin:

```env
# @BotFather'dan alınan Telegram Bot Token
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Dakika cinsinden fiyat kontrol aralığı (varsayılan: 30)
CHECK_INTERVAL=30

# İzin verilen Telegram grup ID'lerinin virgülle ayrılmış listesi
ALLOWED_GROUP_IDS=-1001234567890,-1009876543210
```

5. **Botu başlatın:**
```bash
python main.py
```

## 🔧 Grup ID'si Alma

Telegram grup ID'nizi bulmak için:

1. Botu grubunuza ekleyin
2. Grupta herhangi bir mesaj gönderin
3. Şu adresi ziyaret edin: `https://api.telegram.org/bot{BOT_TOKEN_INIIZ}/getUpdates`
4. JSON yanıtında `"chat":{"id": -1001234567890}` bölümünü arayın
5. Negatif sayıyı (eksi işaretiyle birlikte) kopyalayın

## 📖 Kullanım Kılavuzu

### Temel Komutlar

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `/start` | Botu başlat ve yardımı göster | `/start` |
| `/ekle [URL]` | Ürünü takibe ekle | `/ekle https://www.trendyol.com/...` |
| `/sil [URL]` | Ürünü takipten çıkar | `/sil https://www.trendyol.com/...` |
| `/listele` | Tüm takip edilen ürünleri listele | `/listele` |

### Ürün Ekleme

**Yöntem 1: Komut**
```
/ekle https://www.trendyol.com/urun-linki
```

**Yöntem 2: Direkt Link**
Herhangi bir Trendyol linkini gruba yapıştırın:
```
https://www.trendyol.com/urun-linkiniz
https://ty.gl/kisaltilmis-link
```

### Ürün Listesi Özellikleri

`/listele` komutu şunları gösterir:
- 📈 **Başlangıç fiyatından artış**
- 📉 **Başlangıç fiyatından düşüş**  
- ➡️ **Fiyatta değişiklik yok**
- Ürünlere direkt linkler
- Güncel ve başlangıç fiyat karşılaştırması

## 🔄 Nasıl Çalışır

1. **Ürün Ekleme**: Bot ürün adını ve güncel fiyatı çeker
2. **Veri Saklama**: Bilgiler `tracked_products.json` dosyasında saklanır
3. **Zamanlanmış Kontroller**: Bot her X dakikada bir fiyatları kontrol eder (yapılandırılabilir)
4. **Akıllı Bildirimler**: Sadece fiyatlar gerçekten değiştiğinde uyarı gönderir
5. **Fiyat Güncellemeleri**: Veritabanı otomatik olarak yeni fiyatlarla güncellenir

## 🐧 Otomatik Başlatma (Linux/Raspberry Pi)

Otomatik başlatma için systemd servisi oluşturun:

```bash
sudo nano /etc/systemd/system/trendyol-bot.service
```

**Servis yapılandırması** (yolları kendi kurulumunuza göre ayarlayın):

```ini
[Unit]
Description=Trendyol Fiyat Takip Botu
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/telegram-trendyol-bot
ExecStart=/home/pi/telegram-trendyol-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Etkinleştirin ve başlatın:**
```bash
sudo systemctl enable trendyol-bot.service
sudo systemctl start trendyol-bot.service
```

**Durumu kontrol edin:**
```bash
sudo systemctl status trendyol-bot.service
```

## 📁 Proje Yapısı

```
telegram-trendyol-bot/
├── main.py              # 🤖 Ana bot mantığı ve Telegram işleyicileri
├── scraper.py           # 🕷️ Trendyol web kazıma işlevselliği
├── data_manager.py      # 💾 JSON veri yönetimi (CRUD işlemleri)
├── config.py           # ⚙️ Yapılandırma ve çevre değişkenleri
├── requirements.txt    # 📦 Python bağımlılıkları
├── .env.example       # 📋 Çevre değişkenleri şablonu
├── .env              # 🔐 Gerçek çevre değişkenleriniz (bunu oluşturun)
├── tracked_products.json # 🗃️ Ürün veritabanı (bot tarafından otomatik oluşturulur)
└── README.md         # 📖 Bu dokümantasyon
```

### 🔧 Temel Bileşenler

| Dosya | Amaç | Ana Fonksiyonlar |
|-------|------|------------------|
| `main.py` | Bot orkestras | Komut işleyicileri, fiyat kontrolü, bildirimler |
| `scraper.py` | Web kazıma | Ürün bilgisi çıkarma, fiyat ayrıştırma |
| `data_manager.py` | Veri kalıcılığı | Ürün ekleme/çıkarma, fiyat güncellemeleri |
| `config.py` | Yapılandırma | Çevre değişkenleri, ayarlar |

## 🔍 Teknik Detaylar

### Bağımlılıklar
- **python-telegram-bot 13.15**: Telegram Bot API sarmalayıcısı
- **requests 2.31.0**: Web kazıma için HTTP istekleri
- **beautifulsoup4 4.12.2**: HTML ayrıştırma
- **lxml 4.9.3**: Hızlı XML/HTML ayrıştırıcısı
- **schedule 1.2.0**: İş zamanlama
- **python-dotenv 1.0.0**: Çevre değişkeni yönetimi

### Ana Özellikler Uygulaması
- **Akıllı Fiyat Tespiti**: Sağlam fiyat çıkarma için çoklu seçici yedekleri
- **URL Doğrulama**: Hem tam hem de kısaltılmış Trendyol linklerini destekler
- **Hata Kurtarma**: Loglama ile kapsamlı hata yönetimi
- **Bellek Verimli**: Minimal kaynak kullanımı, 7/24 işletim için ideal
- **Thread Güvenliği**: Zamanlayıcı ve bot işlemleri için uygun threading

## 🐛 Sorun Giderme

### Yaygın Sorunlar

**Bot yanıt vermiyor:**
- `TELEGRAM_BOT_TOKEN`'ın doğru olduğunu kontrol edin
- Grup ID'sinin `ALLOWED_GROUP_IDS`'te olduğunu doğrulayın
- Botun grupta uygun izinlere sahip olduğundan emin olun

**Fiyat tespit edilmiyor:**
- Trendyol HTML yapısını değiştirmiş olabilir
- Kazıma hatalarını kontrol etmek için logları inceleyin
- Farklı ürünlerle deneyin

**Çift bildirim:**
- Geliştirilmiş zamanlayıcı yönetimiyle düzeltildi
- Hala oluşuyorsa botu yeniden başlatın

**Raspberry Pi'de bellek sorunları:**
- Daha az sıklıkta kontrol için `CHECK_INTERVAL`'ı artırın
- Gerekirse swap kullanmayı düşünün

### Loglar ve Hata Ayıklama

Bot önemli olayları loglar. Konsol çıktısında şunları kontrol edin:
- Ürün ekleme/çıkarma onayları
- Fiyat kontrol sonuçları
- Hata detayları
- Bildirim gönderme durumu

## ⚠️ Önemli Notlar

- **Kişisel Kullanım**: Bu bot kişisel/küçük grup kullanımı için tasarlanmıştır
- **Hız Sınırlaması**: Trendyol anti-bot önlemleri uygulayabilir
- **Yasal Uyumluluk**: Trendyol'un kullanım şartlarına uygunluğu sağlayın
- **Güvenilirlik**: Sağlam olmasına rağmen, siteler yapı değiştirirse web kazıma bozulabilir
- **Gizlilik**: Tüm veriler yerel olarak JSON formatında saklanır

## 🛡️ Hata İzleme ve Bildirimler

### Otomatik Hata Bildirimleri

Bot artık hataları otomatik olarak admin'e bildirir:

- 🚨 **Kritik Hatalar**: Bot çöktüğünde anında bildirim
- ⚠️ **Scraping Hataları**: Çok sayıda scraping hatası durumunda uyarı
- 📊 **Watchdog Raporları**: Bot durumu hakkında düzenli bilgiler

### Admin Chat ID Ayarlama

`.env` dosyanıza admin chat ID'nizi ekleyin:

```env
ADMIN_CHAT_ID=123456789
```

**Chat ID'nizi bulmak için:**
1. Bot'unuza `/start` mesajı gönderin
2. `https://api.telegram.org/bot{BOT_TOKEN}/getUpdates` adresini ziyaret edin
3. `"from":{"id": 123456789}` değerini kopyalayın

### Watchdog Sistemi

Watchdog scripti botunuzu sürekli izler:

- ✅ **Process İzleme**: Bot çalışıp çalışmadığını kontrol eder
- 🔄 **Otomatik Restart**: Bot durduğunda otomatik yeniden başlatır  
- 📱 **Telegram Bildirimleri**: Tüm olaylar için bildirim gönderir
- 📝 **Detaylı Loglama**: Tüm aktiviteler loglanır

## 🥧 Raspberry Pi Özel Kurulum

### Otomatik Kurulum

```bash
# Projeyi klonlayın
git clone https://github.com/furkandlkdr/telegram-trendyol-bot.git
cd telegram-trendyol-bot

# Kurulum scriptini çalıştırın
chmod +x install_raspberry.sh
./install_raspberry.sh
```

### Manuel Kurulum

**1. Sistem hazırlığı:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl
```

**2. Proje kurulumu:**
```bash
git clone https://github.com/furkandlkdr/telegram-trendyol-bot.git
cd telegram-trendyol-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Çevre değişkenleri:**
```bash
cp .env.example .env
nano .env  # Ayarlarınızı girin
```

**4. Systemd servisleri:**
```bash
sudo cp systemd/trendyol-bot.service /etc/systemd/system/
sudo cp systemd/trendyol-watchdog.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable trendyol-bot.service
sudo systemctl enable trendyol-watchdog.service
```

**5. Servisleri başlatın:**
```bash
sudo systemctl start trendyol-bot.service
sudo systemctl start trendyol-watchdog.service
```

### Raspberry Pi İzleme Komutları

**Servis durumu:**
```bash
sudo systemctl status trendyol-bot.service
sudo systemctl status trendyol-watchdog.service
```

**Canlı loglar:**
```bash
sudo journalctl -u trendyol-bot.service -f
sudo journalctl -u trendyol-watchdog.service -f
```

**Servis yönetimi:**
```bash
sudo systemctl restart trendyol-bot.service
sudo systemctl stop trendyol-bot.service
sudo systemctl start trendyol-bot.service
```

**Sistem kaynaklarını izleme:**
```bash
htop                    # CPU ve RAM kullanımı
df -h                   # Disk kullanımı
free -h                 # Bellek durumu
journalctl --disk-usage # Log disk kullanımı
```

### Performans Optimizasyonları

**Bellek optimizasyonu:**
```bash
# Swap dosyası oluştur (isteğe bağlı)
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# /etc/fstab'a ekle
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

**Log döngüsü:**
```bash
# Log boyutunu sınırla
sudo nano /etc/systemd/journald.conf
# Şu satırları uncomment edin:
# SystemMaxUse=50M
# MaxRetentionSec=1week

sudo systemctl restart systemd-journald
```

### Sorun Giderme

**Bot başlamıyor:**
```bash
# Detaylı log kontrol
sudo journalctl -u trendyol-bot.service --no-pager

# Manuel test
cd /home/pi/telegram-trendyol-bot
source venv/bin/activate
python main.py
```

**Watchdog çalışmıyor:**
```bash
# Process kontrolü
ps aux | grep python
ps aux | grep watchdog

# Manuel watchdog testi
cd /home/pi/telegram-trendyol-bot
source venv/bin/activate
python watchdog.py
```

**Bellek sorunu:**
```bash
# Bellek kullanımını kontrol et
free -h
sudo systemctl status

# Gereksiz servisleri durdur
sudo systemctl disable bluetooth.service
sudo systemctl disable hciuart.service
```

## 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Lütfen şunlar için pull request gönderin veya issue açın:
- Hata düzeltmeleri
- Yeni özellikler
- Dokümantasyon iyileştirmeleri
- Performans optimizasyonları

## 📄 Lisans

Bu proje açık kaynaklıdır ve MIT Lisansı altında mevcuttur.

## 🔗 Linkler

- [Telegram Bot API Dokümantasyonu](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/botfather) - Bot token'ınızı oluşturun
- [Trendyol](https://www.trendyol.com) - Desteklenen e-ticaret platformu
