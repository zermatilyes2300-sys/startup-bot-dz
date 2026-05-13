# StartupDZ Bot 🚀

بوت Telegram يولّد أفكار startups صناعية للجزائر بالذكاء الاصطناعي.

## طريقة الرفع على Railway

### الخطوة 1 — ارفع الملفات على GitHub
1. روح لـ github.com وادخل لحسابك
2. اضغط **New repository**
3. اسمه: `startup-bot-dz`
4. اختار **Public** واضغط **Create repository**
5. اضغط **uploading an existing file**
6. ارفع الملفات الثلاثة: `bot.py` + `requirements.txt` + `Procfile`
7. اضغط **Commit changes**

### الخطوة 2 — شغّل على Railway
1. روح لـ railway.app وادخل بـ GitHub
2. اضغط **New Project**
3. اختار **Deploy from GitHub repo**
4. اختار `startup-bot-dz`
5. اضغط **Deploy Now**

### الخطوة 3 — أضف المتغيرات
في Railway اضغط على المشروع ثم **Variables** وأضف:

| Variable | Value |
|----------|-------|
| `TELEGRAM_TOKEN` | token ديالك من BotFather |
| `ANTHROPIC_API_KEY` | مفتاح Anthropic |

### الخطوة 4 — احصل على Anthropic API Key
1. روح لـ console.anthropic.com
2. سجّل حساب مجاني
3. روح لـ **API Keys** واضغط **Create Key**
4. كوبي الـ key وحطه في Railway

## كيفاش تستخدم البوت
- `/start` — القائمة الرئيسية
- `/help` — المساعدة
- أو اكتب أي سؤال مباشرة!
