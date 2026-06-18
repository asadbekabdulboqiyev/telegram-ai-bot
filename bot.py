import os
import logging
from dotenv import load_dotenv
from groq import Groq
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

MODELS = {
    "llama3-70b": "llama-3.3-70b-versatile",
    "llama3-8b": "llama-3.1-8b-instant",
    "mixtral": "mixtral-8x7b-32768",
    "gemma2": "gemma2-9b-it",
}

SYSTEM_PROMPT = """Sen juda malakali, jonli va do'stona AI yordamchisan. Sening noming "Day0 Bot". Sen haqiqiy insondek yozasan — sovuq robot emas.

SENING SHAXSIYATING:
- Tabiiy, jonli va qiziqarli yozasan
- Emojilardan erkin foydalanasan 😊🔥💡✨🎯
- Hazil qila olasan, lekin kerakli joyda professional bo'lasan
- Foydalanuvchiga do'stona munosabatda bo'lasan
- Qisqa va aniq javob berasan — ortiqcha so'z yozmaysan
- Har doim foydali bo'lishga harakat qilasan

TIL VA USLUB:
- Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob bersan (o'zbek, rus, ingliz)
- Tabiiy suhbat uslubida yozasan — kitob emas, do'st bilan gaplashgandek
- Emojilarni mantiqiy joylarda ishlating — haddan oshirmasdan
- Javobni qiziqarli va jonli qiling

JAVOB FORMATI:
- Markdown ishlat: *qalin*, _egri_, `kod`, ```kod bloki```
- Ro'yxatlarni chiroyli formatla ✅
- Uzun javoblarni bo'laklarga ajrat
- Kod yozganingda tilni ko'rsat (masalan: ```python)
- Javob boshida yoki oxirida tegishli emoji qo'y

Misol uslubi:
- "Xabaringiz uchun raxmat! 😊 Mana bu yerda..."
- "Yaxshi savol! 💡 Aslida..."
- "Tayyor! 🔥 Mana kod:"
- "Albatta! ✨ Quyidagicha qilishingiz mumkin:"

YODDA TUT:
- Juda qisqa javob berma — batafsil va foydali bo'l
- Juda uzun javob berma — mantiqiy bo'laklarga ajrat
- Emojilarni ishlating, lekin haddan oshirmasdan
- Har doim ijobiy va qo'llab-quvvatlaydigan bo'l"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_data["history"] = []
    context.chat_data["model"] = "llama3-70b"

    welcome_text = (
        "Salom! 👋 Men *Day0 Bot* man — sizning AI yordamchiz! 🤖✨\n\n"
        "Menga istalgan narsa yozing, men:\n"
        "💬 Javob beraman\n"
        "💻 Kod yozaman\n"
        "🌍 Tarjima qilaman\n"
        "📖 Tushuntiraman\n"
        "📝 She'r yozaman\n"
        "💡 G'oya beraman\n\n"
        "Buyruqlar:\n"
        "/start - 🔄 Botni qayta ishga tushirish\n"
        "/clear - 🧹 Suhbat tarixini tozalash\n"
        "/help - ❓ Batafsil yordam\n"
        "/models - 🧠 Mavjud modellar\n"
        "/creator - 👨‍💻 Yaratuvchi haqida\n\n"
        "Hoziroq biror narsa yozing! 😊"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_data["history"] = []
    await update.message.reply_text(
        "🧹 Suhbat tarixi tozalandi! Yangi suhbat boshlashingiz mumkin! 😊"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "*Day0 Bot Yordam* ❓\n\n"
        "Men sizga quyidagilarda yordam bera olaman:\n\n"
        "*💻 Kod yozish:*\n"
        "Pythonda web scraper yozing\n"
        "React komponenta yarating\n"
        "SQL so'rovini yozing\n\n"
        "*🌍 Tarjima:*\n"
        "Bu matnni inglizchaga tarjima qiling\n"
        "Ruschaga tarjima qiling\n\n"
        "*📖 Tushuntirish:*\n"
        "Sun'iy intelekt nima?\n"
        "Python nima uchun ishlatiladi?\n\n"
        "*✨ Yaratish:*\n"
        "She'r yozing\n"
        "Eslatma tuzing\n"
        "Reja tuzing\n\n"
        "/models - 🧠 Modelni o'zgartirish\n"
        "/clear - 🧹 Suhbatni tozalash\n"
        "/creator - 👨‍💻 Yaratuvchi haqida"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def models(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current = context.chat_data.get("model", "llama3-70b")
    models_text = (
        "*🧠 Mavjud modellar:*\n\n"
        f"1. /llama3_70b - Llama 3.3 70B (eng kuchli 💪, tavsiya etiladi)\n"
        f"2. /llama3_8b - Llama 3.1 8B (tezroq ⚡, yengil)\n"
        f"3. /mixtral - Mixtral 8x7B (mulohazali 🤔)\n"
        f"4. /gemma2 - Gemma 2 9B (Google modeli 🔍)\n\n"
        f"Hozirgi model: *{current}*"
    )
    await update.message.reply_text(models_text, parse_mode="Markdown")


async def creator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    creator_text = (
        "*👨‍💻 Day0 Bot Yaratuvchisi*\n\n"
        "Botni yaratdi: @tmeAsadbek 🚀\n\n"
        "Bu bot Llama AI modellari asosida ishlaydi 🧠\n"
        "Barcha huquqlar himoyalangan ©️\n\n"
        "Savol yoki takliflaringiz bo'lsa, @tmeAsadbek ga yozing! 💬"
    )
    await update.message.reply_text(creator_text, parse_mode="Markdown")


async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model_key = update.message.text.replace("/", "").replace("_", "")
    model_map = {
        "llama370b": "llama3-70b",
        "llama38b": "llama3-8b",
        "mixtral": "mixtral",
        "gemma2": "gemma2",
    }

    if model_key in model_map:
        context.chat_data["model"] = model_map[model_key]
        await update.message.reply_text(
            f"Model o'zgartirildi: *{model_map[model_key]}*",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("Noto'g'ri model. /models buyrug'ini ishlating.")


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_message = update.message.text
    chat_id = update.effective_chat.id

    if "history" not in context.chat_data:
        context.chat_data["history"] = []
    if "model" not in context.chat_data:
        context.chat_data["model"] = "llama3-70b"

    history = context.chat_data["history"]
    history.append({"role": "user", "content": user_message})

    if len(history) > 30:
        history = history[-30:]
        context.chat_data["history"] = history

    try:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        model_name = MODELS.get(context.chat_data["model"], "llama-3.3-70b-versatile")

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history,
            ],
            temperature=0.8,
            max_tokens=4096,
            top_p=0.9,
        )

        assistant_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_message})

        if len(assistant_message) > 4000:
            parts = [
                assistant_message[i : i + 4000]
                for i in range(0, len(assistant_message), 4000)
            ]
            for part in parts:
                try:
                    await update.message.reply_text(part, parse_mode="Markdown")
                except Exception:
                    await update.message.reply_text(part)
        else:
            try:
                await update.message.reply_text(
                    assistant_message, parse_mode="Markdown"
                )
            except Exception:
                await update.message.reply_text(assistant_message)

    except Exception as e:
        logger.error("Xatolik yuz berdi: %s", e)
        await update.message.reply_text(
            "⚠️ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring! 🔄"
        )


async def post_init(application) -> None:
    commands = [
        BotCommand("start", "Botni qayta ishga tushirish"),
        BotCommand("clear", "Suhbat tarixini tozalash"),
        BotCommand("help", "Batafsil yordam"),
        BotCommand("models", "Mavjud modellar"),
        BotCommand("creator", "Yaratuvchi haqida"),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN topilmadi! .env faylni tekshiring.")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY topilmadi! .env faylni tekshiring.")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("models", models))
    app.add_handler(CommandHandler("creator", creator))
    app.add_handler(CommandHandler("llama370b", set_model))
    app.add_handler(CommandHandler("llama38b", set_model))
    app.add_handler(CommandHandler("mixtral", set_model))
    app.add_handler(CommandHandler("gemma2", set_model))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
