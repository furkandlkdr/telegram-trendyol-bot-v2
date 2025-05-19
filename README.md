# Trendyol Fiyat Takip Botu

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
git clone https://github.com/username/trendyol-fiyat-takip-botu.git
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
