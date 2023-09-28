import telebot
import random
import string
import requests
from telebot import types


TOKEN = input("6086089724:AAELu6YRS_U0JuJMmWPyhtnBMWJ18iOnPRY")
bot = telebot.TeleBot("6086089724:AAELu6YRS_U0JuJMmWPyhtnBMWJ18iOnPRY")

print(*"SELAM SAHİP 🎉")


OWNER_ID = [5638708289]
sudo_users = [5638708289]


kullanici_anahtarlar = {}


giris_yapan_kullanicilar = []


olusturulan_anahtarlar = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_username = message.from_user.username

    
    reply_text = f"Merhaba {user_name}, (@{user_username})!\n\n@FallenSorguBot Sorgu Botuna Hoş Geldin.\n\nBot Şuan aktiftir Komutlar İçin /help"

    
    markup = types.InlineKeyboardMarkup()
    btn_add_to_group = types.InlineKeyboardButton("Beni Gruba Ekle", url='https://t.me/FallenSorguBot?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users')
    btn_kurucu_shp = types.InlineKeyboardButton("S A H I P", url='https://t.me/BenYakup')  
    
    markup.add(btn_add_to_group, btn_kurucu_shp)

    
    bot.send_message(message.chat.id, reply_text, reply_markup=markup)

@bot.message_handler(commands=['help', 'yardim'])
def yardim(message):
    user_name = message.from_user.first_name
    user_username = message.from_user.username

    
    reply_text = f"Merhaba {user_name} işte Komutlarım:\n\n/tc - TC Sorgular /join - grubumuza katıl\n\nBütün Sorgular Ücretli ve ücretsizdir\n\n uyelik Alımı İçin: @BenYakup\n\n"

    
    markup = types.InlineKeyboardMarkup()
    btn_add_to_group = types.InlineKeyboardButton("Beni Gruba Ekle", url='https://t.me/FallenSorguBot?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users')
    btn_kurucu_shp = types.InlineKeyboardButton("S A H I P", url='https://t.me/BenYakup')   
    
    markup.add(btn_add_to_group, btn_kurucu_shp)

    
    bot.send_message(message.chat.id, reply_text, reply_markup=markup)


@bot.message_handler(commands=['login'])
def login(message):
    chat_id = message.chat.id
    if chat_id in giris_yapan_kullanicilar:
        bot.send_message(chat_id, "Zaten giriş Yapmışsın aga.")
    else:
        bot.send_message(chat_id, "Lütfen Size Verilen Anahtarı Girin:")
        bot.register_next_step_handler(message, process_login)

def process_login(message):
    chat_id = message.chat.id
    anahtar = message.text.strip()
    if chat_id in giris_yapan_kullanicilar:
        bot.send_message(chat_id, "Zaten giriş Yapmışsın aga.")
    else:
        if chat_id in (sudo_users + OWNER_ID) and validate_key(anahtar):
            kullanici_anahtarlar[chat_id] = anahtar
            giris_yapan_kullanicilar.append(chat_id)
            bot.send_message(chat_id, "Giriş başarılı!\n\nKomutlar için /help")
        else:
            bot.send_message(chat_id, "Geçersiz Anahtar Yada Silinmiş. Yenisini Almak için: @BenYakup")

def validate_key(key):
    if len(key) == 12 and all(char.isalnum() for char in key):
        return True
    else:
        return False

@bot.message_handler(commands=['gen'])
def generate_key(message):
    chat_id = message.chat.id
    if chat_id in (sudo_users + OWNER_ID):
        anahtar = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        kullanici_anahtarlar[chat_id] = anahtar
        olusturulan_anahtarlar[chat_id] = anahtar  
        bot.send_message(chat_id, f"Anahtar Oluşturuldu! Key: {anahtar}")
    else:
        bot.send_message(chat_id, "Bu Komut Bot Yetkililerine Özel.")

@bot.message_handler(commands=['adminekle'])
def add_admin(message):
    chat_id = message.chat.id
    if chat_id in OWNER_ID:
        try:
            new_admin_id = int(message.text.split(' ')[1])
            if new_admin_id not in sudo_users:
                sudo_users.append(new_admin_id)
                bot.send_message(chat_id, f"{new_admin_id} kullanıcısı admin olarak eklenmiştir.")
            else:
                bot.send_message(chat_id, f"{new_admin_id} zaten bir admin.")
        except ValueError:
            bot.send_message(chat_id, "Kullanıcı bulunamadı. geçerli bir ID Girin.")
    else:
        bot.send_message(chat_id, "Bu Komutu kullanma izniniz yok.")

@bot.message_handler(commands=['adminsil'])
def remove_admin(message):
    chat_id = message.chat.id
    if chat_id in OWNER_ID:
        try:
            removed_admin_id = int(message.text.split(' ')[1])
            if removed_admin_id in sudo_users:
                sudo_users.remove(removed_admin_id)
                bot.send_message(chat_id, f"{removed_admin_id} kullanıcısı admin listesinden silinmiştir.")
            else:
                bot.send_message(chat_id, f"{removed_admin_id} ID li kullanıcı Zaten admin değil?")
        except ValueError:
            bot.send_message(chat_id, "Kullanıcı bulunmadı. geçerli bir ID Girin.")
    else:
        bot.send_message(chat_id, "bu komutu kullanmaya izniniz yok.")

@bot.message_handler(commands=['tc'])
def tc(message):
    chat_id = message.chat.id
    if chat_id in giris_yapan_kullanicilar:
        try:
            tc_number = message.text.split(' ')[1]
            API_URL_TC = f'http://sentinelcheck.site/api/tc/api.php?tc={tc_number}'  
            response = requests.get(API_URL_TC)
            if response.status_code == 200:
                data = response.json()
                if data:
                    bilgiler = data[0]
                    reply_text = f"╔═══════════════\n╟ @FallenSorguBot \n╚═══════════════\n\n╔═══════════════\n"
                    for key, value in bilgiler.items():
                        reply_text += f"╟ {key.upper()}: {value}\n"
                    reply_text += "╚═══════════════"
                    bot.send_message(chat_id, reply_text)
                else:
                    bot.send_message(chat_id, "TC kimlik numarası bulunamadı.")
            else:
                bot.send_message(chat_id, "API geçersiz yanıt verdi.")
        except Exception as e:
            bot.send_message(chat_id, "hata: " + str(e))
    else:
        bot.send_message(chat_id, "Bota giriş yapmamışsınız. Komutu kullanmak için giriş yapın /login")
        
@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if user_id in sudo_users OWNER_ID:
        bot.reply_to(message, 'Merhaba Yöneticim!💫 İşte komutlarınız:\n\n/wban - Kullanıcıyı Bottan Yasaklarım /adminekle - kullanici id /adminsil - kullanici id\n/unwban - Yasağı Kaldırırım\n/gen - Yeni Key Oluştururum')
    else:
        
        bot.reply_to(message, 'Bu Komutu Kullanmaya İznin Yok aga.🤬') 
        
@bot.message_handler(commands=['join'])
def send_join_buttons(message):
    # İki tane buton oluşturun
    keyboard = types.InlineKeyboardMarkup()
    group_button = types.InlineKeyboardButton("Support⛑️", url="t.me/MajesteTr")
    channel_button = types.InlineKeyboardButton("News Channel🆕", url="t.me/FallenPro")
    albyrk_button = types.InlineKeyboardButton("Sohbet Grubum", url="t.me/AlbayrakChat")
    keyboard.row(group_button, channel_button, albyrk_button)
    bot.send_message(message.chat.id, "Yeniliklerden haberdar olmak için katılın💌!", reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling()

