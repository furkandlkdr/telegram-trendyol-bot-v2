# [EN] Trendyol Price Tracking Bot

This bot tracks product prices on Trendyol and sends notifications via Telegram when prices change.

## Features

- Support for Trendyol.com and ty.gl (shortened) links
- Product addition (`/ekle` command or by directly sending a link)
- Product removal (`/sil` command)
- Listing tracked products (`/listele` command)
- Regular price checking
- Automatic notifications for price changes
- Code optimized for low-power devices like Raspberry Pi
- Multi-group support with permissions

## Installation

### Requirements

- Python 3.6 or newer
- pip (Python package manager)
- Telegram Bot Token (obtainable from BotFather)

### Steps

1. Clone or download this repository:

```bash
git clone https://github.com/furkandlkdr/telegram-trendyol-bot-v2.git
cd telegram-trendyol-bot-v2
```

2. Create and activate a virtual Python environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Edit the `.env` file to add your bot token and allowed group IDs:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
CHECK_INTERVAL=30 # Minutes
ALLOWED_GROUP_IDS=-1001234567890,-1009876543210 # Your group id's
```

5. Start the bot:

```bash
python main.py
```

## Usage

1. Add the bot to your Telegram group and add this group's ID to the `ALLOWED_GROUP_IDS` variable in the `.env` file.
   - To find the group ID: Add the bot to the group, send a message, and visit `https://api.telegram.org/bot{TOKEN}/getUpdates`.

2. Start the bot in Telegram by sending the `/start` command.

3. To add a product:
   - Use the `/ekle https://www.trendyol.com/...` command
   - Or send a Trendyol link directly

4. To list tracked products:
   - Send the `/listele` command

5. To remove a product from tracking:
   - Use the `/sil https://www.trendyol.com/...` command

## Automatic Startup (for Raspberry Pi)

To make the bot start automatically on system boot on a Raspberry Pi, create a systemd service file:

```bash
sudo nano /etc/systemd/system/trendyol-bot.service
```

Add the following to the file **(adjust paths according to your setup!)**:

```
[Unit]
Description=Trendyol Price Tracking Bot
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/telegram-trendyol-bot-v2
ExecStart=/home/pi/telegram-trendyol-bot-v2/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable trendyol-bot.service
sudo systemctl start trendyol-bot.service
```

To check the service status:

```bash
sudo systemctl status trendyol-bot.service
```

## File Structure

- `main.py`: Main bot file, manages Telegram bot functionality
- `scraper.py`: Scrapes price and product information from Trendyol
- `data_manager.py`: Manages product data in JSON format
- `config.py`: Contains bot settings
- `tracked_products.json`: Contains tracked product data (automatically created)
- `requirements.txt`: Lists required Python libraries

## Note

This bot is designed for personal use. Trendyol may block bot usage. In such cases, the bot may not work properly.

---

# [TR] Trendyol Fiyat Takip Botu

Bu bot, Trendyol'daki ürünlerin fiyatlarını takip eder ve fiyat değişikliklerinde Telegram üzerinden bildirim gönderir.

## Özellikler

- Trendyol.com ve ty.gl (kısaltılmış) linkleri desteklenir
- Ürün ekleme (`/ekle` komutu veya direkt link gönderme)
- Ürün silme (`/sil` komutu)
- Takip edilen ürünleri listeleme (`/listele` komutu)
- Düzenli aralıklarla fiyat kontrolü
- Fiyat değişikliklerinde otomatik bildirim
- Raspberry Pi gibi düşük güçlü cihazlar için optimize edilmiş kod

## Kurulum

### Gereksinimler

- Python 3.6 veya daha yeni bir sürüm
- pip (Python paket yöneticisi)
- Telegram Bot Token (BotFather üzerinden alınabilir)

### Adımlar

1. Bu repo'yu klonlayın veya indirin:

```bash
git clone https://github.com/furkandlkdr/trendyol-fiyat-takip-botu.git
cd trendyol-fiyat-takip-botu
```

2. Sanal bir Python ortamı oluşturun ve etkinleştirin:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate  # Windows
```

3. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

4. `.env` dosyasını düzenleyerek bot token'ınızı ve izin verilen grup ID'lerinizi ekleyin:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
CHECK_INTERVAL=30
ALLOWED_GROUP_IDS=-1001234567890,-1009876543210
```

5. Bot'u başlatın:

```bash
python main.py
```

## Kullanım

1. Bot'u Telegram grubunuza ekleyin ve `.env` dosyasında bu grubun ID'sini `ALLOWED_GROUP_IDS` değişkenine ekleyin.
   - Grup ID'sini bulmak için: Bot'u gruba ekleyin, bir mesaj gönderin ve `https://api.telegram.org/bot{TOKEN}/getUpdates` adresini ziyaret edin.

2. Telegram'da bot'u başlatın: `/start` komutunu gönderin.

3. Ürün eklemek için:
   - `/ekle https://www.trendyol.com/...` komutunu kullanın
   - veya doğrudan Trendyol linkini gönderin

3. Takip edilen ürünleri listelemek için:
   - `/listele` komutunu gönderin

4. Bir ürünü takipten çıkarmak için:
   - `/sil https://www.trendyol.com/...` komutunu kullanın

## Otomatik Başlatma (Raspberry Pi için)

Botun Raspberry Pi üzerinde sistem başlangıcında otomatik çalışması için systemd servis dosyası oluşturabilirsiniz:

```bash
sudo nano /etc/systemd/system/trendyol-bot.service
```

Dosyaya şunları ekleyin (yolları kendi kurulumunuza göre düzenleyin):

```
[Unit]
Description=Trendyol Fiyat Takip Botu
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/trendyol-fiyat-takip-botu
ExecStart=/home/pi/trendyol-fiyat-takip-botu/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Servisi etkinleştirin ve başlatın:

```bash
sudo systemctl enable trendyol-bot.service
sudo systemctl start trendyol-bot.service
```

Servisi kontrol etmek için:

```bash
sudo systemctl status trendyol-bot.service
```

## Dosya Yapısı

- `main.py`: Ana bot dosyası, Telegram bot işlevselliğini yönetir
- `scraper.py`: Trendyol sitesinden fiyat ve ürün bilgilerini çeker
- `data_manager.py`: Ürün verilerini JSON formatında yönetir
- `config.py`: Bot ayarlarını içerir
- `tracked_products.json`: Takip edilen ürünlerin verilerini içerir (otomatik oluşturulur)
- `requirements.txt`: Gerekli Python kütüphanelerini listeler

## Not

Bu bot kişisel kullanım için tasarlanmıştır. Trendyol, bot kullanımını engelleyebilir. Bu tür durumlarda bot düzgün çalışmayabilir.
