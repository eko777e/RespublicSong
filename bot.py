import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import Message

# ===== TELEGRAM API =====
API_ID = 24168862
API_HASH = "916a9424dd1e58ab7955001ccc0172b3"
BOT_TOKEN = "8490134432:AAEZl64j3bdudQZBfBzP64dPDMGiD3lkU4g"

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== START =====
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "🎧 Salam!\n\n"
        "Musiqi yükləmək üçün:\n"
        "/song musiqi adı\n\n"
        "Misal:\n"
        "/song Tural Sedali Darixmisam"
    )

# ===== SONG SEARCH =====
@app.on_message(filters.command("song"))
async def song_download(client, message: Message):

    if len(message.command) < 2:
        return await message.reply("❌ Musiqi adı yaz.\n\nMisal:\n/song Rihanna Diamonds")

    query = " ".join(message.command[1:])

    msg = await message.reply("🔎 Musiqi axtarılır...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "cookiefile": "cookies.txt",   # 🍪 COOKIES əlavə edildi
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(f"ytsearch1:{query}", download=True)

            video = info["entries"][0]

        filename = f"{video['title']}.mp3"

        await message.reply_audio(
            audio=filename,
            title=video.get("title"),
            performer=video.get("uploader")
        )

        os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Xəta:\n{e}")

# ===== RUN =====
app.run()
