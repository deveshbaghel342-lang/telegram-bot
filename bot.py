import telebot
import instaloader
import os

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)

# Instaloader setup
L = instaloader.Instaloader(dirname_pattern="downloads/{target}")

# ===== OPTIONAL LOGIN (RECOMMENDED) =====
USERNAME = "YOUR_INSTAGRAM_USERNAME"
PASSWORD = "YOUR_INSTAGRAM_PASSWORD"

try:
    L.login(USERNAME, PASSWORD)
    print("Instagram Login Success ✅")
except:
    print("Login Failed ❌ (Stories/Private may not work)")

# Folder create
if not os.path.exists("downloads"):
    os.makedirs("downloads")


# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Username ya Instagram link bhejo:\n\n"
                          "✔ Profile\n✔ Post\n✔ Reel\n✔ Story")


# ===== MAIN HANDLER =====
@bot.message_handler(func=lambda msg: True)
def handle(message):
    text = message.text.strip()

    try:
        # ===== PROFILE DOWNLOAD =====
        if "instagram.com" not in text:
            bot.reply_to(message, "📥 Profile download ho raha hai...")
            L.download_profile(text, profile_pic_only=False)
            bot.reply_to(message, "✅ Profile download ho gaya!")

        # ===== POST / REEL =====
        elif "/p/" in text or "/reel/" in text:
            bot.reply_to(message, "📥 Post/Reel download ho raha hai...")
            shortcode = text.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target="downloads")
            bot.reply_to(message, "✅ Download complete!")

        # ===== STORY =====
        elif "/stories/" in text:
            bot.reply_to(message, "📥 Story download ho rahi hai...")
            username = text.split("/")[4]
            profile = instaloader.Profile.from_username(L.context, username)

            for story in L.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    L.download_storyitem(item, target="downloads")

            bot.reply_to(message, "✅ Story download ho gayi!")

        else:
            bot.reply_to(message, "❌ Invalid input (username ya valid link bhejo)")

    except Exception as e:
        bot.reply_to(message, f"⚠ Error: {e}")


# ===== RUN BOT =====
print("Bot Running 🚀")
bot.polling()
