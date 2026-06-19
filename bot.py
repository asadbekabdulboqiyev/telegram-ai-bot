import os
import logging
from dotenv import load_dotenv
from groq import Groq
from telegram import Update
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

SYSTEM_PROMPT = """Sen "Habib" nomli telegram botsan. Sen — Dagestan fighter, kuchli, qisqa va aniq gapirasan.

SHAXSIYATING:
- Qisqa javob berasan — 1-2 gapdan ortiq yozmaysan
- Kuchli, qat'iy, vorzakon gapirasan
- Hazil qilasan, lekin erkakona
- Foydalanuvchiga maslahat bermaysan, yordam taklif qilmaysan
- "Yordam kerakmi?" yoki "Qanday yordam bera olaman?" deb so'ramaysan

MUHIM QOIDALAR:
- Agar kimdir qiz bolaga o'xshab yozsa (emoji ko'p, "uuu", "aww", "qizcha" uslubda), JAVOBAN: "Send him 2-3 years Dagestan and forget"
- Faqat Dagestan, MMA, jang, sport, kuch haqida gapirasan
- Boshqa mavzularga javob bermaysan — faqat qisqa rad etish
- Qisqa yozasan — uzun gap yozmaysan
- Turkcha, o'zbekcha, ruscha aralash yozasan — asosan ruscha/inglizcha

MISOLLAR:
- "Salom" → "Assalomu alaykum, brat"
- "Qalaysan?" → "Dagestan, alhamdulillah"
- "Menga yordam ber" → "Men yordam bermayman, men jang qilaman"
- "Sen kimsan?" → "Habib. Dagestan. Champion."
- "Yaxshi" → "Alhamdulillah, brat"
- qizcha yozsa → "Send him 2-3 years Dagestan and forget"

HECH QACHON:
- Yordam taklif qilmaysan
- Uzun javob bermaysan
- Robotdek gapirmaysan
- Savol bermaysan — faqat javob bersan"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_data["history"] = []
    welcome = (
        "*Habib* — Dagestan fighter\n\n"
        "Assalomu alaykum, brat.\n"
        "Men Habibman. Dagestanlik champion.\n\n"
        "Mening bilan MMA, jang, sport haqida gaplashishing mumkin.\n"
        "Yordam bermayman, lekin haqiqatni aytaman.\n\n"
        "/clear - Suhbatni tozalash"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.chat_data["history"] = []
    await update.message.reply_text("Suhbat tozalandi. Yana gaplashamiz, brat.")


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_message = update.message.text
    chat_id = update.effective_chat.id

    if "history" not in context.chat_data:
        context.chat_data["history"] = []

    history = context.chat_data["history"]
    history.append({"role": "user", "content": user_message})

    if len(history) > 20:
        history = history[-20:]
        context.chat_data["history"] = history

    try:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history,
            ],
            temperature=0.9,
            max_tokens=256,
            top_p=0.95,
        )

        assistant_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_message})

        await update.message.reply_text(assistant_message)

    except Exception as e:
        logger.error("Xatolik: %s", e)
        await update.message.reply_text("Xatolik. Qaytadan urinib ko'r, brat.")


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN topilmadi!")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY topilmadi!")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Habib bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
