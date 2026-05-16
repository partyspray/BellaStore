import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from datetime import datetime

# استبدل هذا التوكن بالتوكن الخاص ببوتك من BotFather
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

# دالة لتوليد بيانات الكارت بناءً على النوع المختار
def generate_card_by_type(brand):
    # الفيزا تبدأ بـ 4، الماستركارد تبدأ بـ 5
    prefix = '4' if brand == 'Visa' else '5'
    
    # توليد باقي أرقام الكارت (15 رقم إضافي ليصبح المجموع 16)
    card_number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(15)])
    
    # توليد الشهر (01-12) والسنة (من السنة الحالية لـ 5 سنين قدام)
    month = f"{random.randint(1, 12):02d}"
    year = str(datetime.now().year + random.randint(1, 5))[2:]
    
    # توليد كود الـ CVV (3 أرقام)
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    return card_number, f"{month}/{year}", cvv

# التفاعل مع أمر /start أو /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "أهلاً بك في بوت توليد الفيزات العشوائية! 💳\n\n"
        "اضغط على الأمر التالي لتوليد كارت:\n"
        "/gen - لاختيار نوع الكارت وتوليده"
    )
    bot.reply_to(message, welcome_text)

# التفاعل مع أمر /gen لإظهار الأزرار
@bot.message_handler(commands=['gen'])
def choose_card_type(message):
    # إنشاء لوحة الأزرار
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 # عدد الأزرار في الصف الواحد
    
    # إضافة زر الفيزا وزر الماستركارد
    markup.add(
        InlineKeyboardButton("Visa 🟦", callback_data="gen_visa"),
        InlineKeyboardButton("Mastercard 🟧", callback_data="gen_master")
    )
    
    bot.send_message(message.chat.id, "من فضلك اختر نوع الكارت الذي تريد توليده:", reply_markup=markup)

# استقبال ضغطات الأزرار (Callback Queries)
@bot.callback_query_handler(func=lambda call: call.data in ['gen_visa', 'gen_master'])
def callback_query(call):
    # تحديد النوع بناءً على البيانات القادمة من الزر المفتوح
    if call.data == "gen_visa":
        brand = "Visa"
    else:
        brand = "Mastercard"
        
    # توليد الكارت
    card_num, expiry, cvv = generate_card_by_type(brand)
    
    response = (
        f"**💳 تم توليد كارت عشوائي بنجاح:**\n\n"
        f"**النوع:** {brand}\n"
        f"**الرقم:** `{card_num}`\n"
        f"**التاريخ:** `{expiry}`\n"
        f"**CVV:** `{cvv}`\n\n"
        f"⚠️ *ملاحظة: هذه البيانات عشوائية ووهمية تماماً وتستخدم للتجربة فقط.*"
    )
    
    # إرسال البيانات للمستخدم كرد على الضغطة (مع دعم نسخ الأرقام بلمسة واحدة)
    bot.send_message(call.message.chat.id, response, parse_mode='Markdown')
    
    # إخطار تليجرام أن الضغطة تمت بنجاح لإنهاء علامة التحميل على الزر
    bot.answer_callback_query(call.id)

# تشغيل البوت بشكل مستمر
print("البوت يعمل الآن...")
bot.infinity_polling()
