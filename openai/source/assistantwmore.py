import openai
import pyttsx3

openai.api_key = 'YOUR_API_KEY'

engine = pyttsx3.init()

def ask_openai(question):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=question,
      max_tokens=150
    )
    return response.choices[0].text.strip()

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("Welcome to your AI Assistant. Ask me anything!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        response = ask_openai(user_input)
        print("Assistant:", response)
        speak(response)
