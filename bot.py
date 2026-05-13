import os
from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# ====== CONFIGURATION ======
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# ====== KEYBOARDS ======
def menu_principal():
    keyboard = [
        [InlineKeyboardButton("♻️ Recyclage industriel", callback_data="sec_recyclage")],
        [InlineKeyboardButton("💧 Traitement des eaux", callback_data="sec_eau")],
        [InlineKeyboardButton("🏗️ Matériaux & construction", callback_data="sec_materiaux")],
        [InlineKeyboardButton("⚡ Énergie & biomasse", callback_data="sec_energie")],
        [InlineKeyboardButton("🧪 Chimie fine", callback_data="sec_chimie")],
        [InlineKeyboardButton("🌾 Agrochimie", callback_data="sec_agro")],
        [InlineKeyboardButton("🧴 Cosmétique naturelle", callback_data="sec_cosmetique")],
    ]
    return InlineKeyboardMarkup(keyboard)

def menu_difficulte(secteur):
    keyboard = [
        [InlineKeyboardButton("🟢 سهل — أقل من 5M DZD", callback_data=f"diff_{secteur}_facile")],
        [InlineKeyboardButton("🟡 متوسط — 5 إلى 20M DZD", callback_data=f"diff_{secteur}_moyen")],
        [InlineKeyboardButton("🔴 طموح — أكثر من 20M DZD", callback_data=f"diff_{secteur}_ambitieux")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="retour_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def menu_focus(secteur, difficulte):
    keyboard = [
        [InlineKeyboardButton("🇩🇿 استبدال الاستيراد", callback_data=f"gen_{secteur}_{difficulte}_import")],
        [InlineKeyboardButton("🌍 تصدير — أفريقيا وأوروبا", callback_data=f"gen_{secteur}_{difficulte}_export")],
        [InlineKeyboardButton("🏭 سوق B2B محلي", callback_data=f"gen_{secteur}_{difficulte}_b2b")],
        [InlineKeyboardButton("💡 ابتكار تكنولوجي", callback_data=f"gen_{secteur}_{difficulte}_innovation")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"sec_{secteur}")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== SECTOR LABELS ======
SECTEURS = {
    "recyclage": "♻️ Recyclage industriel",
    "eau": "💧 Traitement des eaux industrielles",
    "materiaux": "🏗️ Matériaux de construction innovants",
    "energie": "⚡ Énergie & biomasse",
    "chimie": "🧪 Chimie fine et produits industriels",
    "agro": "🌾 Agrochimie et intrants agricoles",
    "cosmetique": "🧴 Cosmétique et chimie naturelle",
}

DIFFICULTES = {
    "facile": "سهل — رأس مال أقل من 5 ملايين DZD",
    "moyen": "متوسط — رأس مال 5 إلى 20 مليون DZD",
    "ambitieux": "طموح — رأس مال أكثر من 20 مليون DZD",
}

FOCUS = {
    "import": "استبدال الاستيراد",
    "export": "تصدير نحو أفريقيا وأوروبا",
    "b2b": "سوق B2B صناعي محلي",
    "innovation": "ابتكار تكنولوجي محلي",
}

# ====== GENERATE IDEAS VIA CLAUDE ======
def generer_idees(secteur, difficulte, focus):
    secteur_label = SECTEURS.get(secteur, secteur)
    diff_label = DIFFICULTES.get(difficulte, difficulte)
    focus_label = FOCUS.get(focus, focus)

    prompt = f"""أنت خبير في ريادة الأعمال الصناعية في الجزائر متخصص في génie chimique.

ولّد 5 أفكار startups صناعية واقعية في الجزائر في القطاع: "{secteur_label}".
مستوى الصعوبة: {diff_label}.
التوجه: {focus_label}.

لكل فكرة أعطني بالتنسيق التالي بالضبط:

🏭 **[اسم الفكرة]**
📌 المشكلة: [مشكلة حقيقية في الجزائر]
💡 الحل: [واش تعمل الـ startup]
👥 العملاء: [مين يدفع]
💰 الربح: [كيفاش تربح]
💵 رأس المال: [X إلى Y مليون DZD]
🇩🇿 الميزة في DZ: [ليش تمشي في الجزائر]
📊 الصعوبة: [سهل/متوسط/صعب] | الإمكانية: [منخفضة/متوسطة/عالية/عالية جداً]

---

قيود:
- واقعية 100% للسوق الجزائري 2024-2025
- مواد خام محلية أين أمكن
- تجنب القطاعات المحتكرة من الدولة
- اكتب بمزيج عربية وفرنسية طبيعي"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return response.text

# ====== HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *مرحبا بك في StartupDZ Bot!*\n\n"
        "أنا مساعدك الذكي لإيجاد أفكار startups صناعية واقعية في الجزائر 🇩🇿\n\n"
        "اختار القطاع اللي يهمك 👇",
        parse_mode="Markdown",
        reply_markup=menu_principal()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *كيفاش تستخدم البوت:*\n\n"
        "1️⃣ اختار القطاع الصناعي\n"
        "2️⃣ اختار مستوى الصعوبة\n"
        "3️⃣ اختار التوجه الاستراتيجي\n"
        "4️⃣ الـ AI يولّد أفكار مخصصة للجزائر\n\n"
        "اضغط /start للبداية 🚀",
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # رجوع للقائمة الرئيسية
    if data == "retour_menu":
        await query.edit_message_text(
            "🚀 *StartupDZ Bot*\n\nاختار القطاع اللي يهمك 👇",
            parse_mode="Markdown",
            reply_markup=menu_principal()
        )

    # اختيار القطاع
    elif data.startswith("sec_"):
        secteur = data.replace("sec_", "")
        secteur_label = SECTEURS.get(secteur, secteur)
        await query.edit_message_text(
            f"✅ القطاع: *{secteur_label}*\n\nاختار مستوى الصعوبة 👇",
            parse_mode="Markdown",
            reply_markup=menu_difficulte(secteur)
        )

    # اختيار الصعوبة
    elif data.startswith("diff_"):
        parts = data.split("_")
        secteur = parts[1]
        difficulte = parts[2]
        secteur_label = SECTEURS.get(secteur, secteur)
        diff_label = DIFFICULTES.get(difficulte, difficulte)
        await query.edit_message_text(
            f"✅ القطاع: *{secteur_label}*\n"
            f"✅ الصعوبة: *{diff_label}*\n\n"
            f"اختار التوجه الاستراتيجي 👇",
            parse_mode="Markdown",
            reply_markup=menu_focus(secteur, difficulte)
        )

    # توليد الأفكار
    elif data.startswith("gen_"):
        parts = data.split("_")
        secteur = parts[1]
        difficulte = parts[2]
        focus = parts[3]

        await query.edit_message_text(
            "⏳ *الـ AI يبحث ويحلل السوق الجزائري...*\n\nاستنى شوية 🔍",
            parse_mode="Markdown"
        )

        try:
            idees = generer_idees(secteur, difficulte, focus)
            secteur_label = SECTEURS.get(secteur, secteur)
            diff_label = DIFFICULTES.get(difficulte, difficulte)
            focus_label = FOCUS.get(focus, focus)

            header = (
                f"🎯 *نتائج البحث:*\n"
                f"📂 {secteur_label}\n"
                f"📊 {diff_label}\n"
                f"🎯 {focus_label}\n\n"
                f"{'─'*30}\n\n"
            )

            full_text = header + idees

            # Telegram max 4096 chars
            if len(full_text) > 4000:
                await query.edit_message_text(
                    full_text[:4000] + "\n\n_...يتبع_",
                    parse_mode="Markdown"
                )
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=full_text[4000:],
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(full_text, parse_mode="Markdown")

            # زر للبداية من جديد
            keyboard = [[InlineKeyboardButton("🔄 أفكار جديدة", callback_data="retour_menu")]]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="💬 تحب تعرف أكثر عن فكرة معينة؟ فقط اكتبلي اسمها ونفصّل ليك!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        except Exception as e:
            await query.edit_message_text(
                f"❌ صرالي خطأ: {str(e)}\n\nجرب مرة أخرى /start",
                parse_mode="Markdown"
            )

# معالجة الرسائل النصية — سؤال حر
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.reply_text("⏳ نفكر معك...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=f"""أنت خبير في ريادة الأعمال الصناعية في الجزائر متخصص في génie chimique.
أجب على هذا السؤال بشكل مختصر ومفيد للسوق الجزائري:

{user_text}

اكتب بمزيج عربية وفرنسية طبيعي. الجواب ما يتعداش 500 كلمة."""
        )
        await update.message.reply_text(response.text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {str(e)}")

# ====== MAIN ======
def main():
    request = HTTPXRequest(connect_timeout=30, read_timeout=30)
    app = Application.builder().token(TELEGRAM_TOKEN).request(request).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("✅ البوت شغّال!")
    app.run_polling()

if __name__ == "__main__":
    main()
