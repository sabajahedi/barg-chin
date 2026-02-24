import os
import sys
import httpx

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MEMBERS = "@DrMAminiSh @Telahe72 @kazemi967 @Greeenbear @JahediSaba"

NIGHT_MESSAGE = (
    "عزیزان! برین حیاطتون رو جارو کنین و برگاتون رو جمع کنین! 🍂🍁\n\n"
    + MEMBERS
)

DAY_MESSAGE = (
    "عزیزان! حیاط رو جارو کردین یا برگاتون پخش و پلاست؟ 🍂🍁\n\n"
    + MEMBERS
)

# First CLI argument: "night" or "day"
period = sys.argv[1] if len(sys.argv) > 1 else "night"
message = DAY_MESSAGE if period == "day" else NIGHT_MESSAGE

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
resp = httpx.post(url, json={"chat_id": CHAT_ID, "text": message})
resp.raise_for_status()
print(f"{period.capitalize()} reminder sent successfully")
