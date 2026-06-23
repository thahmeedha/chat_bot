import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import requests

# ----------------- API CONFIG -----------------
API_KEY = "YOUR_API_KEY_HERE"  # ⚠️ Don't expose real key publicly
MODEL = "deepseek/deepseek-chat"


# ----------------- AI FUNCTION -----------------
def get_reply(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⏳ Network timeout. Try again."

    except Exception as e:
        return f"⚠ Error: {str(e)}"


# ----------------- PAGE SWITCH -----------------
def sp(page):
    page.tkraise()


# ----------------- MAIN WINDOW -----------------
main = tk.Tk()
main.geometry("1920x1080")
main.configure(bg="gray")

container = tk.Frame(main)
container.place(x=0, y=0, width=1920, height=1080)

welcome_page = tk.Frame(container, bg="lightblue")
chatbot_page = tk.Frame(container, bg="lightgreen")

for page in (welcome_page, chatbot_page):
    page.place(x=0, y=0, width=1920, height=1080)

# ----------------- WELCOME PAGE -----------------
title = tk.Label(welcome_page, text="Welcome to chatbot",
                 bg="lightblue", fg="white", font=("Arial", 25))
title.place(x=650, y=100)

# Username
tk.Label(welcome_page, text="User Name:",
         bg="lightblue", fg="white", font=("Arial", 20)).place(x=450, y=200)

user_name = tk.Entry(welcome_page, font=("Arial", 20))
user_name.place(x=650, y=200)

# Phone
tk.Label(welcome_page, text="User Phone:",
         bg="lightblue", fg="white", font=("Arial", 20)).place(x=450, y=270)

user_phone = tk.Entry(welcome_page, font=("Arial", 20))
user_phone.place(x=650, y=270)

# Email
tk.Label(welcome_page, text="User Email:",
         bg="lightblue", fg="white", font=("Arial", 20)).place(x=450, y=340)

user_email = tk.Entry(welcome_page, font=("Arial", 20))
user_email.place(x=650, y=340)

# State dropdown
tk.Label(welcome_page, text="User State:",
         bg="lightblue", fg="white", font=("Arial", 20)).place(x=450, y=410)

states_list = ["Tamilnadu", "Kerala", "Andhra", "Karnataka"]
state_box = ttk.Combobox(welcome_page, values=states_list, font=("Arial", 20))
state_box.place(x=650, y=410)

# Submit Button
tk.Button(welcome_page, text="Submit",
          font=("Arial", 20),
          bg="gray", fg="white",
          command=lambda: sp(chatbot_page)).place(x=650, y=480)

# ----------------- CHATBOT PAGE -----------------
title = tk.Label(chatbot_page,
                 text="CHATBOT READY TO ASSIST YOU 😊",
                 bg="lightgreen", fg="white", font=("Arial", 25))
title.place(x=240, y=30)

# Back button
tk.Button(chatbot_page, text="Back",
          font=("Arial", 20),
          bg="gray", fg="white",
          command=lambda: sp(welcome_page)).place(x=1150, y=20)

# Chat display
chat_display = scrolledtext.ScrolledText(
    chatbot_page, wrap='word', font=('Arial', 12),
    state=tk.DISABLED, width=95, height=25
)
chat_display.place(x=100, y=90)

# Input field
user_input = tk.Entry(chatbot_page, font=('Arial', 14), width=80)
user_input.place(x=100, y=550)


# ----------------- SEND FUNCTION -----------------
def send_message():
    msg = user_input.get().strip()
    if msg == "":
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {msg}\n")
    chat_display.config(state=tk.DISABLED)

    user_input.delete(0, tk.END)

    reply = get_reply(msg)

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Bot: {reply}\n\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)


# Send button
tk.Button(chatbot_page, text="Send",
          font=("Arial", 20),
          bg="blue", fg="white",
          command=send_message).place(x=1050, y=530)

# Enter key
chatbot_page.bind("<Return>", lambda e: send_message())

# ----------------- START -----------------
welcome_page.tkraise()
main.mainloop()