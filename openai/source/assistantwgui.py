import openai
import tkinter as tk
from tkinter import scrolledtext

openai.api_key = 'YOUR_API_KEY'

def ask_openai(question):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=question,
      max_tokens=150
    )
    return response.choices[0].text.strip()

def get_response():
    user_input = user_text.get("1.0",'end-1c')
    response = ask_openai(user_input)
    assistant_text.config(state=tk.NORMAL)
    assistant_text.insert(tk.END, "You: " + user_input + "\n")
    assistant_text.insert(tk.END, "Assistant: " + response + "\n\n")
    assistant_text.config(state=tk.DISABLED)
    user_text.delete("1.0", tk.END)

app = tk.Tk()
app.title("AI Assistant")

user_text = tk.Text(app, height=5, width=50)
user_text.pack(pady=10)

assistant_text = scrolledtext.ScrolledText(app, height=15, width=50, state=tk.DISABLED)
assistant_text.pack(pady=10)

ask_button = tk.Button(app, text="Ask", command=get_response)
ask_button.pack(pady=5)

app.mainloop()
