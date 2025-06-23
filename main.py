import logging
import re
import time
import threading
import schedule
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from scraper import scrape_product_info, is_valid_trendyol_url
from data_manager import add_product, remove_product, get_all_products, update_product_price
from config import TELEGRAM_BOT_TOKEN, CHECK_INTERVAL, ALLOWED_GROUP_IDS

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variable to store bot instance
_bot_instance = None

def is_allowed_chat(chat_id):
    """Check if the chat_id is in the allowed list."""
    return chat_id in ALLOWED_GROUP_IDS

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id
    
    # Check if the chat is allowed
    if not is_allowed_chat(chat_id):
        logger.info(f"Unauthorized start command from chat_id: {chat_id}")
        return
        
    update.message.reply_text(
        'Merhaba! Trendyol Fiyat Takip Botuna hoş geldiniz.\n\n'
        'Komutlar:\n'
        '/ekle [Trendyol linki] - Fiyat takibi için yeni bir ürün ekler\n'
        '/sil [Trendyol linki] - Takipten bir ürün çıkarır\n'
        '/listele - Takip edilen tüm ürünleri listeler\n\n'
        'Ayrıca, direkt olarak Trendyol.com veya ty.gl linki göndererek de ürün ekleyebilirsiniz.'
    )

def extract_url(text):
    """Extract URL from text."""
    url_pattern = r'https?://(?:www\.)?(trendyol\.com|ty\.gl|tyml\.gl|trendyol-milla\.com)[^\s]+'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

def add_product_handler(update: Update, context: CallbackContext):
    """Add a product to track."""
    chat_id = update.effective_chat.id
    
    # Check if the chat is allowed
    if not is_allowed_chat(chat_id):
        logger.info(f"Unauthorized add_product command from chat_id: {chat_id}")
        return
    
    # Extract URL from command or message text
    if context.args:
        url = extract_url(' '.join(context.args))
    else:
        update.message.reply_text('Lütfen geçerli bir Trendyol linki ekleyin.\n'
                                'Örnek: /ekle https://www.trendyol.com/...')
        return
    
    if not url or not is_valid_trendyol_url(url):
        update.message.reply_text('Geçerli bir Trendyol linki bulunamadı.')
        return
    
    # Send initial message
    message = update.message.reply_text('Ürün bilgileri alınıyor...')
    
    # Fetch product info
    product_name, price, error = scrape_product_info(url)
    
    if error == "Tükendi":
        # Handle sold out product
        success = add_product(chat_id, url, product_name, price)  # price is 0 for sold out products
        
        if success:
            message.edit_text(
                f'Ürün başarıyla eklendi!\n\n'
                f'Ürün: {product_name}\n'
                f'Durum: Tükendi\n\n'
                f'Ürün tekrar stokta olduğunda size bildirim göndereceğim.'
            )
        else:
            message.edit_text('Ürün eklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
        return
    elif error:
        message.edit_text(f'Hata: {error}')
        return
    
    if not price:
        message.edit_text('Ürün fiyatı alınamadı. Lütfen linki kontrol edin.')
        return
    
    # Add the product to tracking
    success = add_product(chat_id, url, product_name, price)
    
    if success:
        message.edit_text(
            f'Ürün başarıyla eklendi!\n\n'
            f'Ürün: {product_name}\n'
            f'Güncel Fiyat: {price:.2f} TL\n\n'
            f'Fiyat değiştiğinde size bildirim göndereceğim.'
        )
    else:
        message.edit_text('Ürün eklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')

def url_handler(update: Update, context: CallbackContext):
    """Handle messages containing Trendyol URLs."""
    chat_id = update.effective_chat.id
    
    # Check if the chat is allowed
    if not is_allowed_chat(chat_id):
        logger.info(f"Unauthorized URL message from chat_id: {chat_id}")
        return
    
    # Extract URL from message text
    url = extract_url(update.message.text)
    
    if not url or not is_valid_trendyol_url(url):
        return  # Ignore non-Trendyol URLs
    
    # Send initial message
    message = update.message.reply_text('Ürün bilgileri alınıyor...')
    
    # Fetch product info
    product_name, price, error = scrape_product_info(url)
    
    if error == "Tükendi":
        # Handle sold out product
        success = add_product(chat_id, url, product_name, price)  # price is 0 for sold out products
        
        if success:
            message.edit_text(
                f'Ürün başarıyla eklendi!\n\n'
                f'Ürün: {product_name}\n'
                f'Durum: Tükendi\n\n'
                f'Ürün tekrar stokta olduğunda size bildirim göndereceğim.'
            )
        else:
            message.edit_text('Ürün eklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
        return
    elif error:
        message.edit_text(f'Hata: {error}')
        return
    
    if not price:
        message.edit_text('Ürün fiyatı alınamadı. Lütfen linki kontrol edin.')
        return
    
    # Add the product to tracking
    success = add_product(chat_id, url, product_name, price)
    
    if success:
        message.edit_text(
            f'Ürün başarıyla eklendi!\n\n'
            f'Ürün: {product_name}\n'
            f'Güncel Fiyat: {price:.2f} TL\n\n'
            f'Fiyat değiştiğinde size bildirim göndereceğim.'
        )
    else:
        message.edit_text('Ürün eklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')

def remove_product_handler(update: Update, context: CallbackContext):
    """Remove a product from tracking."""
    chat_id = update.effective_chat.id
    
    # Check if the chat is allowed
    if not is_allowed_chat(chat_id):
        logger.info(f"Unauthorized remove_product command from chat_id: {chat_id}")
        return
    
    # Extract URL from command
    if context.args:
        url = extract_url(' '.join(context.args))
    else:
        update.message.reply_text('Lütfen silmek istediğiniz ürünün Trendyol linkini ekleyin.\n'
                                'Örnek: /sil https://www.trendyol.com/...')
        return
    
    if not url:
        update.message.reply_text('Geçerli bir Trendyol linki bulunamadı.')
        return
    
    # Remove the product from tracking
    success = remove_product(chat_id, url)
    
    if success:
        update.message.reply_text('Ürün takipten çıkarıldı.')
    else:
        update.message.reply_text('Ürün bulunamadı veya zaten takip edilmiyor.')

def list_products(update: Update, context: CallbackContext):
    """List all tracked products."""
    chat_id = update.effective_chat.id
    
    # Check if the chat is allowed
    if not is_allowed_chat(chat_id):
        logger.info(f"Unauthorized list_products command from chat_id: {chat_id}")
        return
    
    # Get all products for this chat
    products = get_all_products(chat_id)
    
    if not products:
        update.message.reply_text('Henüz takip edilen ürün bulunmamaktadır.')
        return
    
    # Prepare the message text
    message = 'Takip Edilen Ürünler:\n\n'
    
    for url, product_info in products.items():
        product_name = product_info.get('product_name', 'İsimsiz Ürün')
        current_price = product_info.get('current_price', 0)
        initial_price = product_info.get('initial_price', 0)
        
        # Check if product is sold out (price is 0)
        if current_price == 0:
            message += (
                f'🔹 <b>{product_name}</b>\n'
                f'   <b>Tükendi</b>\n'
                f'   <a href="{url}">Link</a>\n\n'
            )
            continue
        
        price_diff = current_price - initial_price
        if price_diff > 0:
            price_trend = f'📈 +{price_diff:.2f} TL'
        elif price_diff < 0:
            price_trend = f'📉 {price_diff:.2f} TL'
        else:
            price_trend = '➡️ Değişim yok'
        
        message += (
            f'🔹 <b>{product_name}</b>\n'
            f'   Güncel Fiyat: <b>{current_price:.2f} TL</b> {price_trend}\n'
            f'   <a href="{url}">Link</a>\n\n'
        )
    
    update.message.reply_text(message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

# Global variable to store bot instance
_bot_instance = None

def check_prices():
    """Check prices for all tracked products and notify if there's a change."""
    global _bot_instance
    
    if not _bot_instance:
        logger.error("Bot instance not available for price checking")
        return
        
    data = get_all_products()
    
    if not data:
        logger.info("No products to check")
        return
    
    for chat_id, products in data.items():
        for url, product_info in list(products.items()):
            product_name = product_info['product_name']
            current_price = product_info['current_price']
            
            logger.info(f"Checking price for {product_name} at {url}")
            
            # Fetch new product info
            new_product_name, new_price, error = scrape_product_info(url)
            
            # Handle sold out status
            if error == "Tükendi":
                # If the product was available before but is now sold out
                if current_price > 0:
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=f'⚠️ Ürün tükendi!\n\n'
                             f'Ürün: {product_name}\n'
                             f'Önceki Fiyat: {current_price:.2f} TL\n'
                             f'Durum: Tükendi\n\n'
                             f'<a href="{url}">Ürün Linki</a>',
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                    # Update the price to 0 to mark as sold out
                    update_product_price(chat_id, url, 0)
                continue
            elif error:
                logger.error(f"Error checking {url}: {error}")
                continue
            
            if not new_price:
                logger.error(f"Could not get price for {url}")
                continue
            
            # If the product was sold out before but is now available
            if current_price == 0 and new_price > 0:
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f'🎉 Ürün tekrar stokta!\n\n'
                         f'Ürün: {product_name}\n'
                         f'Güncel Fiyat: {new_price:.2f} TL\n\n'
                         f'<a href="{url}">Ürün Linki</a>',
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                update_product_price(chat_id, url, new_price)
                continue
            
            # If price has changed
            if new_price != current_price:
                price_diff = new_price - current_price
                percentage = (price_diff / current_price) * 100 if current_price > 0 else 0
                
                if price_diff > 0:
                    message = (
                        f'⚠️ Fiyat arttı!\n\n'
                        f'Ürün: {product_name}\n'
                        f'Önceki Fiyat: {current_price:.2f} TL\n'
                        f'Yeni Fiyat: {new_price:.2f} TL\n'
                        f'Fark: +{price_diff:.2f} TL ({percentage:.1f}%)\n\n'
                        f'<a href="{url}">Ürün Linki</a>'
                    )
                else:
                    message = (
                        f'🔥 Fiyat düştü!\n\n'
                        f'Ürün: {product_name}\n'
                        f'Önceki Fiyat: {current_price:.2f} TL\n'
                        f'Yeni Fiyat: {new_price:.2f} TL\n'
                        f'Fark: {price_diff:.2f} TL ({percentage:.1f}%)\n\n'
                        f'<a href="{url}">Ürün Linki</a>'
                    )
                
                context.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                
                # Update the price
                update_product_price(chat_id, url, new_price)
            
            try:
                _, new_price, error = scrape_product_info(url)
                
                if error:
                    logger.error(f"Error checking {url}: {error}")
                    continue
                
                if new_price is None:
                    logger.error(f"Could not get price for {url}")
                    continue
                
                # If the price has changed
                if abs(new_price - current_price) > 0.01:  # Allow for small decimal differences
                    # Update the price in the database
                    update_product_price(chat_id, url, new_price)
                    
                    # Prepare and send notification
                    price_diff = new_price - current_price
                    if price_diff > 0:
                        trend_emoji = "📈 Fiyat Yükseldi"
                        trend_color = "🔴"
                    else:
                        trend_emoji = "📉 Fiyat Düştü"
                        trend_color = "🟢"
                    
                    notification_text = (
                        f'{trend_color} <b>{trend_emoji}!</b>\n\n'
                        f'<b>{product_name}</b>\n'
                        f'Eski Fiyat: <b>{current_price:.2f} TL</b>\n'
                        f'Yeni Fiyat: <b>{new_price:.2f} TL</b>\n'
                        f'Fark: <b>{price_diff:+.2f} TL (%{(price_diff/current_price*100):+.1f})</b>\n\n'
                        f'<a href="{url}">Ürüne Git</a>'
                    )
                    
                    # Send notification
                    try:
                        _bot_instance.send_message(
                            chat_id=int(chat_id),
                            text=notification_text,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=True
                        )
                        logger.info(f"Price change notification sent to {chat_id}")
                    except Exception as send_error:
                        logger.error(f"Failed to send notification to {chat_id}: {send_error}")
                else:
                    logger.info(f"No price change for {product_name}")
            
            except Exception as e:
                logger.error(f"Error checking price for {url}: {e}")

def run_scheduler():
    """Run the scheduler in a separate thread."""
    while True:
        schedule.run_pending()
        time.sleep(1)

def error(update: Update, context: CallbackContext):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")
    # Notify user about the error if possible
    if update.effective_message:
        update.effective_message.reply_text('Bir hata oluştu. Lütfen daha sonra tekrar deneyin.')

def main():
    """Start the bot."""
    global _bot_instance
    
    if not TELEGRAM_BOT_TOKEN:
        logger.error("No token provided. Set TELEGRAM_BOT_TOKEN in .env file.")
        return
        
    if not ALLOWED_GROUP_IDS:
        logger.warning("ALLOWED_GROUP_IDS is not set in .env file. Bot will not respond to any group.")
        logger.warning("Set ALLOWED_GROUP_IDS with comma-separated group IDs in your .env file.")
    
    # Create the Updater and pass it the bot's token
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # Store bot instance globally for price checking
    _bot_instance = updater.bot
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ekle", add_product_handler))
    dispatcher.add_handler(CommandHandler("sil", remove_product_handler))
    dispatcher.add_handler(CommandHandler("listele", list_products))
    
    # Message handler for Trendyol links
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command & Filters.regex(r'https?://(www\.)?(trendyol\.com|ty\.gl|tyml\.gl|trendyol-milla\.com)'), 
        url_handler
    ))
    
    # Error handler
    dispatcher.add_error_handler(error)
    
    # Clear any existing scheduled jobs to prevent duplicates
    schedule.clear()
    
    # Schedule price checking based on the defined interval
    schedule.every(CHECK_INTERVAL).minutes.do(check_prices)
    
    # Start the scheduler in a new thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Start the Bot
    updater.start_polling()
    logger.info("Bot started!")
    
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()

