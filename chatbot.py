from datetime import datetime
from colorama import init, Fore, Back, Style
import random
import re
import os

init(autoreset=True)

# ─────────────────────────────────────────
#  COLOR SHORTCUTS
# ─────────────────────────────────────────
BOT_COLOR   = Fore.CYAN + Style.BRIGHT
USER_COLOR  = Fore.GREEN + Style.BRIGHT
HEAD_COLOR  = Fore.MAGENTA + Style.BRIGHT
INFO_COLOR  = Fore.YELLOW
ERR_COLOR   = Fore.RED
RESET       = Style.RESET_ALL
DIM         = Style.DIM

# ─────────────────────────────────────────
#  DATA POOLS
# ─────────────────────────────────────────
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? He used up all his cache!",
    "How many programmers to change a lightbulb? None — it's a hardware problem.",
    "Why do Java devs wear glasses? Because they don't C#!",
    "What do you call a programmer from Finland? Nerdic.",
    "Why was the computer cold? It left its Windows open.",
    "A SQL query walks into a bar and asks two tables: 'Can I join you?'",
]

QUOTES = [
    "Success comes from consistent effort. Keep learning!",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Code is like humor. When you have to explain it, it's bad.",
    "Every expert was once a beginner. Keep going!",
    "Don't watch the clock; do what it does. Keep going.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
]

FACTS = [
    "The first computer bug was an actual moth found in a Harvard relay in 1947.",
    "Python is named after Monty Python, not the snake.",
    "The first computer programmer was Ada Lovelace, in the 1840s.",
    "There are over 700 programming languages in existence.",
    "About 70% of all websites use JavaScript.",
    "The term 'Wi-Fi' doesn't actually stand for anything — it's just a brand name.",
    "Humans blink only 7 times/min while using screens (normally 15-20).",
]

RIDDLES = [
    {"q": "I speak without a mouth and hear without ears. I come alive with wind. What am I?", "a": "An echo!"},
    {"q": "The more you take, the more you leave behind. What am I?",                          "a": "Footsteps!"},
    {"q": "I have cities, but no houses. Mountains, but no trees. What am I?",                 "a": "A map!"},
    {"q": "What has hands but can't clap?",                                                     "a": "A clock!"},
    {"q": "What gets wetter the more it dries?",                                                "a": "A towel!"},
]

# ─────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def divider(char="─", color=Fore.MAGENTA):
    print(color + char * 47 + RESET)

def bot_say(msg):
    ts = datetime.now().strftime("%H:%M")
    print(f"\n  {BOT_COLOR}🤖 SmartBot {DIM}[{ts}]{RESET}")
    for line in msg.split("\n"):
        print(f"  {Fore.WHITE}  {line}{RESET}")

def user_label(name):
    ts = datetime.now().strftime("%H:%M")
    return f"\n  {USER_COLOR}👤 {name} {DIM}[{ts}]{RESET}\n  > "

def show_banner(name=""):
    clear()
    divider("═", Fore.MAGENTA)
    print(HEAD_COLOR + "        🤖  S M A R T B O T  🤖        " + RESET)
    if name:
        print(f"  {DIM}  Chatting as: {Fore.GREEN}{name}{RESET}")
    divider("═", Fore.MAGENTA)

def show_help():
    divider()
    categories = {
        "💬 Greetings"   : ["hi / hello / hey"],
        "🕐 Time & Date" : ["time", "date", "day"],
        "😂 Fun"         : ["joke", "fact", "riddle", "motivate"],
        "🎲 Games"       : ["flip a coin", "roll a dice", "random number"],
        "🧮 Math"        : ["calculate 10 * 5 + 2"],
        "🌡  Convert"     : ["convert 37c", "convert 98f"],
        "🔤 Text Tools"  : ["reverse hello", "uppercase hi", "lowercase HI",
                            "count words <sentence>", "repeat 3 hello"],
        "👤 Personal"    : ["my name", "how many messages"],
        "❌ Quit"        : ["bye / goodbye / exit"],
    }
    for cat, cmds in categories.items():
        print(f"  {INFO_COLOR}{cat}{RESET}")
        for c in cmds:
            print(f"    {DIM}• {c}{RESET}")
    divider()

# ─────────────────────────────────────────
#  CHATBOT LOGIC
# ─────────────────────────────────────────
def smartbot():
    show_banner()
    print(f"\n  {BOT_COLOR}🤖{RESET} Hello! What's your name?")
    name = input(f"  {Fore.WHITE}> {RESET}").strip()
    while not name:
        print(f"  {ERR_COLOR}Please enter your name.{RESET}")
        name = input(f"  {Fore.WHITE}> {RESET}").strip()

    show_banner(name)
    bot_say(f"Welcome, {name}! 👋 I'm SmartBot.\n  Type 'help' to see all commands.")

    message_count = 0
    riddle_mode   = False
    current_riddle = None

    while True:
        try:
            raw = input(user_label(name)).strip()
        except (EOFError, KeyboardInterrupt):
            bot_say(f"Goodbye, {name}! Have a great day! 👋")
            divider()
            break

        if not raw:
            continue

        message_count += 1
        u = raw.lower()

        # ── Exit ──────────────────────────────────────────
        if u in ["bye", "goodbye", "exit", "quit"]:
            bot_say(f"Goodbye, {name}! Have an amazing day! 👋")
            divider()
            break

        # ── Riddle answer reveal ───────────────────────────
        if riddle_mode:
            bot_say(f"The answer was: {Fore.YELLOW}{current_riddle['a']}{RESET}\n  Did you get it right? 😄")
            riddle_mode    = False
            current_riddle = None
            continue

        # ── Greetings ─────────────────────────────────────
        if u in ["hi", "hello", "hey", "howdy", "hiya"]:
            bot_say(f"Hey {name}! 👋 How can I help you today?")

        elif "how are you" in u:
            bot_say("Running at 100% efficiency! Thanks for asking 😊")

        elif "your name" in u or "who are you" in u:
            bot_say("I'm SmartBot — your friendly AI assistant! 🤖")

        # ── Time & Date ────────────────────────────────────
        elif "time" in u:
            bot_say(f"⏰ Current time: {Fore.YELLOW}{datetime.now().strftime('%H:%M:%S')}{RESET}")

        elif "date" in u:
            bot_say(f"📅 Today's date: {Fore.YELLOW}{datetime.now().strftime('%d %B %Y')}{RESET}")

        elif "day" in u:
            bot_say(f"📆 Today is: {Fore.YELLOW}{datetime.now().strftime('%A')}{RESET}")

        # ── Fun ────────────────────────────────────────────
        elif "joke" in u:
            bot_say(f"😂 {Fore.YELLOW}{random.choice(JOKES)}{RESET}")

        elif any(w in u for w in ["motivat", "inspir", "quote"]):
            bot_say(f'⚡ "{Fore.YELLOW}{random.choice(QUOTES)}{RESET}"')

        elif "fact" in u:
            bot_say(f"📖 Did you know?\n  {Fore.YELLOW}{random.choice(FACTS)}{RESET}")

        elif "riddle" in u:
            current_riddle = random.choice(RIDDLES)
            riddle_mode    = True
            bot_say(f"🧩 {Fore.YELLOW}{current_riddle['q']}{RESET}\n  (Type anything to reveal the answer!)")

        # ── Games ──────────────────────────────────────────
        elif "flip" in u or "coin" in u:
            result = random.choice(["🪙 Heads!", "🪙 Tails!"])
            bot_say(f"{Fore.YELLOW}{result}{RESET}")

        elif "roll" in u or "dice" in u:
            bot_say(f"🎲 You rolled: {Fore.YELLOW}{random.randint(1, 6)}{RESET}")

        elif "random number" in u:
            bot_say(f"🔢 Your random number: {Fore.YELLOW}{random.randint(1, 100)}{RESET}")

        # ── Calculator ─────────────────────────────────────
        elif u.startswith("calculate"):
            expression = raw[9:].strip()
            allowed = set("0123456789+-*/()%. ")
            if all(c in allowed for c in expression):
                try:
                    result = eval(expression)
                    bot_say(f"🧮 {Fore.WHITE}{expression}{RESET} = {Fore.YELLOW}{round(result, 6)}{RESET}")
                except Exception:
                    bot_say(f"{ERR_COLOR}Invalid expression. Try: calculate 10 * 5 + 2{RESET}")
            else:
                bot_say(f"{ERR_COLOR}Invalid characters detected.{RESET}")

        # ── Temperature Converter ──────────────────────────
        elif u.startswith("convert"):
            c_m = re.search(r"([\d.]+)\s*[°]?c", u)
            f_m = re.search(r"([\d.]+)\s*[°]?f", u)
            if c_m:
                c = float(c_m.group(1))
                bot_say(f"🌡  {Fore.WHITE}{c}°C{RESET} = {Fore.YELLOW}{c*9/5+32:.1f}°F{RESET}")
            elif f_m:
                f = float(f_m.group(1))
                bot_say(f"🌡  {Fore.WHITE}{f}°F{RESET} = {Fore.YELLOW}{(f-32)*5/9:.1f}°C{RESET}")
            else:
                bot_say("Try: convert 37c   or   convert 98f")

        # ── Text Tools ─────────────────────────────────────
        elif u.startswith("reverse"):
            word = raw[7:].strip()
            bot_say(f"🔤 {Fore.YELLOW}{word[::-1]}{RESET}") if word else bot_say("Try: reverse hello")

        elif u.startswith("uppercase"):
            bot_say(f"🔡 {Fore.YELLOW}{raw[9:].strip().upper()}{RESET}")

        elif u.startswith("lowercase"):
            bot_say(f"🔡 {Fore.YELLOW}{raw[9:].strip().lower()}{RESET}")

        elif u.startswith("count words"):
            sentence = raw[11:].strip()
            words    = sentence.split()
            bot_say(f"📊 That sentence has {Fore.YELLOW}{len(words)} word(s){RESET}.")

        elif u.startswith("repeat"):
            m = re.match(r"repeat\s+(\d+)\s+(.+)", u)
            if m:
                n    = min(int(m.group(1)), 10)
                word = m.group(2)
                bot_say(f"🔄 {Fore.YELLOW}{', '.join([word]*n)}{RESET}")
            else:
                bot_say("Try: repeat 3 hello")

        # ── Personal ───────────────────────────────────────
        elif "my name" in u:
            bot_say(f"Your name is {Fore.YELLOW}{name}{RESET}! 😊")

        elif "how many message" in u or "message count" in u:
            bot_say(f"📨 You've sent {Fore.YELLOW}{message_count}{RESET} message(s) this session.")

        # ── Extras ─────────────────────────────────────────
        elif "good morning" in u:
            bot_say("☀️  Good morning! Hope your day is as bright as your code!")

        elif "good night" in u:
            bot_say("🌙 Good night! Bugs can wait till tomorrow.")

        elif "thank" in u:
            bot_say(f"You're welcome, {name}! 😊")

        elif "love you" in u:
            bot_say("Aww! 🤖❤️  I love helping you!")

        elif "weather" in u:
            bot_say("🌤  Can't fetch live weather yet — but it's always sunny in the world of code! ☀️")

        elif "help" in u:
            show_help()

        # ── Fallback ───────────────────────────────────────
        else:
            bot_say(f"🤔 I didn't catch that. Type {Fore.YELLOW}'help'{RESET} to see all commands!")

        print()

# ─────────────────────────────────────────
if __name__ == "__main__":
    smartbot()