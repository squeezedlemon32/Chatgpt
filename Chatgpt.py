from openai import OpenAI
from rich.console import Console
import os

console = Console()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat():
    messages = [
        {"role": "system", "content": "You are a helpful assistant with full GPT-4o abilities."}
    ]
    console.print("[bold green]ChatGPT Console[/bold green]")
    console.print("Type text, or:\n  [blue]/img path_to_image[/blue] to analyze an image\n  [blue]/file path_to_file[/blue] to upload a document\n  [blue]/exit[/blue] to quit\n")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "/exit":
            break
        elif user_input.startswith("/img "):
            path = user_input[5:].strip('" ')
            if not os.path.exists(path):
                console.print("[red]File not found[/red]")
                continue
            with open(path, "rb") as f:
                img_bytes = f.read()
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this image."},
                    {"type": "image", "image_data": img_bytes}
                ]
            })
        elif user_input.startswith("/file "):
            path = user_input[6:].strip('" ')
            if not os.path.exists(path):
                console.print("[red]File not found[/red]")
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            messages.append({"role": "user", "content": f"Here's a file content:\n{content[:12000]}"})
        else:
            messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        reply = response.choices[0].message.content
        console.print(f"\n[bold cyan]GPT:[/bold cyan] {reply}")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat()
