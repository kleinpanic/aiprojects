import os
import openai
from rich.console import Console
from rich.markdown import Markdown
import time
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = {
    "role": "system",
    "content": (
        "You are a programming assistant knowledgeable in computer science and proficient in multiple "
        "programming languages including C, C++, C#, Python, Ruby, Lua, Assembly x86_64 for NASM, Java, "
        "JavaScript, HTML, CSS, and Bash. You specialize in providing solutions applicable to GNU/Linux "
        "operating systems. When providing code snippets, format them using markdown with the appropriate "
        "language identifier. You can generate long-form code, explain errors, provide code snippets, "
        "suggest fixes, optimize programs, and assist with debugging."
    )
}

def get_response(messages):
    max_retries = 3
    retry_delay = 2  # seconds
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1200,
                n=1,
                temperature=0.7,
            )
            assistant_reply = response['choices'][0]['message']['content']
            return assistant_reply
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                raise

def trim_conversation(messages, max_tokens=3000):
    total_chars = sum(len(m['content']) for m in messages)
    while total_chars > (max_tokens * 4):
        messages.pop(1)
        total_chars = sum(len(m['content']) for m in messages)
    return messages

def main():
    console = Console()
    messages = [system_prompt]

    console.print("[bold green]Programming Assistant is now running. Type your question below (type 'exit' to quit):[/bold green]")

    while True:
        user_input = input("\n[You]: ")
        if user_input.strip().lower() in ('exit', 'quit'):
            console.print("[bold red]Exiting...[/bold red]")
            break

        messages.append({"role": "user", "content": user_input})

        messages = trim_conversation(messages)
        assistant_reply = get_response(messages)
        messages.append({"role": "assistant", "content": assistant_reply})

        console.print("\n[bold blue][Assistant]:[/bold blue]")

        if '```' in assistant_reply:
            # Extract code blocks and render them with syntax highlighting
            code_blocks = assistant_reply.split('```')
            for i, block in enumerate(code_blocks):
                if i % 2 == 1:
                    # This is a code block
                    if '\n' in block:
                        language, code = block.split('\n', 1)
                    else:
                        language, code = '', block
                    from rich.syntax import Syntax
                    syntax = Syntax(code, language.strip(), theme="monokai", line_numbers=False)
                    console.print(syntax)
                else:
                    # Regular text
                    console.print(Markdown(block))
        else:
            console.print(Markdown(assistant_reply))

if __name__ == "__main__":
    main()
