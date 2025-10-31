from openai import OpenAI
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
import os, base64

console = Console()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def display_output(text):
    # Detect code blocks and format nicely
    if "```" in text:
        parts = text.split("```")
        for i, part in enumerate(parts):
            if i % 2 == 1:
                lang, *code = part.split("\n", 1)
                lang = lang.strip() or "text"
                code = code[0] if code else ""
                syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title=lang.upper(), border_style="cyan"))
            else:
                if part.strip():
                    console.print(part.strip())
    else:
        console.print(text)

def chat():
    messages = [
        {"role": "system", "content": "You are ChatGPT, a highly capable AI assistant using GPT-4o. Help with code, text, images, and reasoning tasks."}
    ]

    console.print("[bold green]ChatGPT Pro Terminal[/bold green]")
    console.print("Commands:\n"
                  "[blue]/img path[/blue] - analyze an image\n"
                  "[blue]/file path[/blue] - read and discuss a text file\n"
                  "[blue]/exit[/blue] - quit\n")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "/exit":
            break

        if user_input.startswith("/img "):
            path = user_input[5:].strip('" ')
            if not os.path.exists(path):
                console.print("[red]File not found[/red]")
                continue
            with open(path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this image carefully."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_data}"}
                ]
            })
        elif user_input.startswith("/file "):
            path = user_input[6:].strip('" ')
            if not os.path.exists(path):
                console.print("[red]File not found[/red]")
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            messages.append({"role": "user", "content": f"Here's a file content:\n{content[:15000]}"})
        else:
            messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            console.print(f"\n[bold cyan]GPT ({response.model}):[/bold cyan]")
            display_output(reply)
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    chat()
