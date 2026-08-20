import tkinter as tk
from tkinter import scrolledtext

from src.brain.brain import Brain
from src.core.orchestrator import Orchestrator


class AURAApp:

    def __init__(self, root):
        self.root = root
        self.root.title("AURA AI")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        self.orchestrator = Orchestrator(Brain())

        # Header
        header = tk.Frame(root)
        header.pack(fill="x", padx=15, pady=(15, 5))

        title = tk.Label(
            header,
            text="🧠 AURA AI",
            font=("Arial", 22, "bold")
        )
        title.pack(side="left")

        status = tk.Label(
            header,
            text="● ONLINE",
            font=("Arial", 11, "bold")
        )
        status.pack(side="right")

        # Chat area
        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 12),
            state="disabled"
        )
        self.chat.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Input area
        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.entry = tk.Entry(
            input_frame,
            font=("Arial", 13)
        )
        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        self.entry.bind("<Return>", self.send_message)

        send_button = tk.Button(
            input_frame,
            text="SEND",
            font=("Arial", 11, "bold"),
            command=self.send_message
        )
        send_button.pack(
            side="right",
            padx=(10, 0),
            ipadx=15,
            ipady=5
        )

        self.add_message(
            "AURA",
            "Hello! I am AURA AI. How can I help you?"
        )

        self.entry.focus()

    def add_message(self, sender, message):
        self.chat.config(state="normal")
        self.chat.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def send_message(self, event=None):
        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(0, tk.END)

        self.add_message("YOU", text)

        try:
            response = self.orchestrator.handle(text)
        except Exception as exc:
            response = f"Error: {exc}"

        self.add_message("AURA", response)


def main():
    root = tk.Tk()
    AURAApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
