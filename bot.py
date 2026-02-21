import telebot
import instaloader
import os

# ===== ENV VARIABLES =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

bot = telebot.TeleBot(BOT_TOKEN)

L = instaloader.Instaloader(dirname_pattern="downloads/{target}")

# ===== LOGIN =====
try:
    if IG_USERNAME and IG_PASSWORD:
        L.login(IG_USERNAME, IG_PASSWORD)
        print("Instagram Login Success ✅")
    else:
        print("No IG login (limited features)")
except Exception as e:
    print(f"Login Failed ❌ {e}")

# Folder
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send username or Instagram link")

# ===== HANDLER =====
@bot.message_handler(func=lambda msg: True)
def handle(message):
    text = message.text.strip()

    try:
        # Profile
        if "instagram.com" not in text:
            bot.reply_to(message, "Downloading profile...")
            L.download_profile(text, profile_pic_only=False)
            bot.reply_to(message, "Done ✅")

        # Post/Reel
        elif "/p/" in text or "/reel/" in text:
            shortcode = text.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target="downloads")
            bot.reply_to(message, "Downloaded ✅")

        # Story
        elif "/stories/" in text:
            username = text.split("/")[4]
            profile = instaloader.Profile.from_username(L.context, username)

            for story in L.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    L.download_storyitem(item, target="downloads")

            bot.reply_to(message, "Story Done ✅")

        else:
            bot.reply_to(message, "Invalid input ❌")

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

print("Bot Running 🚀")
bot.polling()
