
import random
import tkinter as tk
from tkinter import ttk, messagebox

# ---- Original data ----
SCRAMBLE_OPTIONS = ["R","R'","R2","U","U'","U2","F","F'","F2","L","L'","L2","D","D'","D2","B","B'","B2"]

LEFT_SCRAMBLE = ["L","L'","L2","U","U'","U2"]
RIGHT_SCRAMBLE = ["R","R'","R2","U","U'","U2"]

def generate_scramble(scramble_list, count=15):
    """
    Generates a scramble ensuring no two consecutive moves start with the same face letter.
    """
    final_scramble = []
    previous_face = ""  # track just the face letter, e.g. 'R', 'U'
    for _ in range(count):
        while True:
            current = random.choice(scramble_list)
            current_face = current[0]
            if current_face == previous_face:
                continue
            final_scramble.append(current)
            previous_face = current_face
            break
    return ", ".join(final_scramble)

class ScrambleUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cube Scrambler")
        self.geometry("520x320")
        self.resizable(False, False)

        # State
        self.scramble_type = tk.StringVar(value="Both")
        self.scramble_len = tk.IntVar(value=15)
        self.last_list = SCRAMBLE_OPTIONS  # default
        self.last_len = 15

        # --- Layout ---
        self._build_controls()
        self._build_output()

        # Keyboard shortcut for Next
        self.bind("<Return>", lambda e: self.on_next())

    def _build_controls(self):
        frm = ttk.LabelFrame(self, text="Options")
        frm.pack(fill="x", padx=12, pady=10)

        # Scramble Type
        ttk.Label(frm, text="Scramble:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        type_box = ttk.Combobox(
            frm,
            textvariable=self.scramble_type,
            values=("Left", "Right", "Both"),
            state="readonly",
            width=12
        )
        type_box.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        # Length
        ttk.Label(frm, text="Length:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        len_box = ttk.Combobox(
            frm,
            textvariable=self.scramble_len,
            values=(5, 10, 15),
            state="readonly",
            width=6
        )
        len_box.grid(row=0, column=3, padx=8, pady=8, sticky="w")

        # Buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=0, column=4, padx=8, pady=8, sticky="e")
        ttk.Button(btn_frame, text="Generate", command=self.on_generate).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Next", command=self.on_next).grid(row=0, column=1, padx=6)

    def _build_output(self):
        out_frame = ttk.LabelFrame(self, text="Scramble")
        out_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        
        self.output = tk.Text(out_frame, height=4, wrap="word", font=("Helvetica", 20))
        self.output.pack(fill="both", expand=True, padx=8, pady=8)
        self.output.configure(state="disabled")

        # Styling tags
        self.output.tag_configure("prime", foreground="blue")
        self.output.tag_configure("normal", foreground="black")


        controls = ttk.Frame(out_frame)
        controls.pack(fill="x", padx=8, pady=4)
        ttk.Button(controls, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side="left")
        ttk.Button(controls, text="Clear", command=self.clear_output).pack(side="left", padx=6)

    def _resolve_list(self):
        s_type = self.scramble_type.get().lower()
        if s_type == "left":
            return LEFT_SCRAMBLE
        elif s_type == "right":
            return RIGHT_SCRAMBLE
        return SCRAMBLE_OPTIONS

    
    def on_generate(self):
        try:
            lst = self._resolve_list()
            n = int(self.scramble_len.get())
            scramble = generate_scramble(lst, n)

            self.last_list = lst
            self.last_len = n

            self.output.configure(state="normal")
            self.output.delete("1.0", "end")
            for move in scramble.split(", "):
                tag = "prime" if "'" in move else "normal"
                self.output.insert("end", move + " ", tag)
            self.output.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate scramble:\n{e}")


    
    def on_next(self):
        # Use last chosen list/length again
        try:
            scramble = generate_scramble(self.last_list, self.last_len)

            self.output.configure(state="normal")
            self.output.delete("1.0", "end")

            # Insert each move with a tag: prime -> blue, normal -> black
            for move in scramble.split(", "):
                tag = "prime" if "'" in move else "normal"
                self.output.insert("end", move + " ", tag)

            self.output.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate next scramble:\n{e}")


    def copy_to_clipboard(self):
        try:
            text = self.output.get("1.0", "end").strip()
            if text:
                self.clipboard_clear()
                self.clipboard_append(text)
                messagebox.showinfo("Copied", "Scramble copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"Clipboard operation failed:\n{e}")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

if __name__ == "__main__":
    app = ScrambleUI()
    app.mainloop()
