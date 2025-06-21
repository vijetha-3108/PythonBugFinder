import tkinter as tk
from tkcode import CodeEditor
import traceback
import re
import io
import sys
import threading
import time

# --- Expanded Error Explanations ---
ERROR_EXPLANATIONS = {
    "SyntaxError": "🧠 This usually happens due to missing colons, wrong indentation, or incorrect syntax.",
    "IndentationError": "🔧 Check your indentation. Python is sensitive to spaces and tabs!",
    "NameError": "🔍 You're using a variable or function that hasn't been defined yet.",
    "TypeError": "🛠 You're using a function or operator on the wrong data type.",
    "ZeroDivisionError": "⚠ You tried to divide by zero – which is undefined.",
    "IndexError": "📦 You're trying to access an index that doesn't exist in a list or string.",
    "ValueError": "❗ You're passing a value to a function that is of the correct type but inappropriate.",
    "AttributeError": "🔑 You're trying to access an attribute or method that doesn't exist for that object.",
    "KeyError": "🗝 You're trying to access a dictionary key that doesn't exist.",
    "ImportError": "📦 Python can't find the module you're trying to import.",
    "ModuleNotFoundError": "📦 Python can't find the module you're trying to import.",
    "FileNotFoundError": "📁 The file you're trying to access does not exist.",
    "OSError": "💾 An operating system error occurred (file, directory, permissions, etc).",
    "RuntimeError": "🏃‍♂️ An error that doesn't fall into other categories. Check your logic.",
    "RecursionError": "🔁 Your function called itself too many times (infinite recursion?).",
    "MemoryError": "💾 Your code tried to use more memory than is available.",
    "OverflowError": "🔢 A number is too large to be represented.",
    "StopIteration": "🛑 An iterator has no more items.",
    "AssertionError": "❗ An assert statement failed.",
    "PermissionError": "🚫 You don't have permission to perform this action.",
    "EOFError": "📚 End Of File reached unexpectedly (e.g., input() got no data).",
    "FloatingPointError": "⚠ A floating point calculation failed.",
    "NotImplementedError": "🚧 This feature isn't implemented yet.",
    "SystemExit": "🚪 The code tried to exit Python.",
}

# --- Constants ---
TITLE_FONT = ("Segoe UI Semibold", 21)
LABEL_FONT = ("Segoe UI", 14, "bold")
BUTTON_FONT = ("Segoe UI", 13)
CODE_FONT = ("Consolas", 12)
OUTPUT_FONT = ("Consolas", 12)
ACCENT_COLOR = "#10b981"
BUTTON_HOVER_COLOR = "#059669"
DARK_TEXT_COLOR = "#f1f5f9"
PLACEHOLDER_COLOR = "#94a3b8"
BG_COLOR = "#0f172a"
FRAME_COLOR = "#1e293b"
TEXT_BG_COLOR = "#111827"
ERROR_TEXT_COLOR = "#ef4444"
SUCCESS_TEXT_COLOR = "#22c55e"

code_placeholder = "# Write your Python code here...\n# Example:\n# print('Hello World')"

# --- Functions ---
def analyze_code_async():
    spinner_label.config(text="⏳ Analyzing...", fg="#facc15")
    run_button.config(state="disabled")
    window.update_idletasks()
    time.sleep(0.2)
    analyze_code()
    spinner_label.config(text="")
    run_button.config(state="normal")

def analyze_code():
    code = code_input.get("1.0", tk.END)
    output_display.config(state=tk.NORMAL)
    output_display.delete("1.0", tk.END)

    if not code.strip() or code.strip() == code_placeholder.strip():
        output_display.insert(tk.END, "⚠ Please enter valid Python code to analyze.\n")
        output_display.tag_add("error", "1.0", "end")
        output_display.config(state=tk.DISABLED)
        return

    try:
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        local_vars = {}
        exec(code, {}, local_vars)
        sys.stdout = old_stdout
        output_text = redirected_output.getvalue()

        final_output = "✅ Code executed successfully!\n"
        if output_text.strip():
            final_output += f"\n📤 Output:\n{output_text}"

        output_display.insert(tk.END, final_output)
        output_display.tag_add("success", "1.0", "end")

    except Exception as e:
        sys.stdout = old_stdout
        error_type = type(e).__name__
        error_msg = str(e)
        tb = traceback.format_exc()

        line_info = re.search(r'File "<string>", line (\d+)', tb)
        line_number = line_info.group(1) if line_info else "?"

        explanation = ERROR_EXPLANATIONS.get(error_type, "😕 This error type is currently not explained.")

        output = f"❌ Error: {error_type} on line {line_number}\n"
        output += f"📌 Message: {error_msg}\n"
        output += f"💡 Explanation: {explanation}\n"

        output_display.insert(tk.END, output)
        output_display.tag_add("error", "1.0", "end")

    output_display.config(state=tk.DISABLED)

def on_code_focus_in(event):
    if code_input.get("1.0", tk.END).strip() == code_placeholder:
        code_input.delete("1.0", tk.END)
        code_input.config(fg=DARK_TEXT_COLOR)

def on_code_focus_out(event):
    if not code_input.get("1.0", tk.END).strip():
        code_input.insert("1.0", code_placeholder)
        code_input.config(fg=PLACEHOLDER_COLOR)

def update_line_numbers(event=None):
    code_lines = code_input.get("1.0", tk.END).split("\n")
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete("1.0", tk.END)
    for i in range(1, len(code_lines)):
        line_numbers.insert(tk.END, f"{i}\n")
    line_numbers.config(state=tk.DISABLED)

def sync_scroll(*args):
    code_input.yview(*args)
    line_numbers.yview(*args)

def on_enter(e): run_button['background'] = BUTTON_HOVER_COLOR
def on_leave(e): run_button['background'] = ACCENT_COLOR

def clear_output():
    output_display.config(state=tk.NORMAL)
    output_display.delete("1.0", tk.END)
    output_display.config(state=tk.DISABLED)

def run_code_shortcut(event=None):
    threading.Thread(target=analyze_code_async).start()
    return "break"

def clear_output_shortcut(event=None):
    clear_output()
    return "break"

# --- Main Window ---
window = tk.Tk()
window.title("🐞 BugFinder – Python Code Debugger & Explainer")
window.geometry("1000x750")
window.minsize(900, 600)
window.configure(bg=BG_COLOR)
window.resizable(True, True)

main_frame = tk.Frame(window, bg=BG_COLOR, padx=30, pady=25)
main_frame.pack(fill=tk.BOTH, expand=True)

# Configure grid for flexible layout
main_frame.grid_rowconfigure(1, weight=2)
main_frame.grid_rowconfigure(4, weight=3)
main_frame.grid_columnconfigure(0, weight=1)

title_label = tk.Label(main_frame, text="🐍 Paste Your Python Code Below", font=TITLE_FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

# --- Code Input Frame ---
code_outer_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=3, relief="ridge")
code_outer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 15))

line_numbers = tk.Text(code_outer_frame, width=4, padx=6, font=CODE_FONT, bg="#0f172a", fg="#64748b",
                       state=tk.DISABLED, relief=tk.FLAT, wrap=tk.NONE)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

# --- Syntax Highlighting Code Editor ---
code_input = CodeEditor(
    code_outer_frame,
    width=90,
    height=20,
    language="python",
    highlighter="dracula",
    autofocus=True,
    blockcursor=True,
    insertborderwidth=3,
    padx=10,
    pady=10,
)
code_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
code_input.content = code_placeholder
code_input.bind("<<TextModified>>", update_line_numbers)

# --- Analyze Button + Spinner + Clear Output ---
button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 15))

run_button = tk.Button(button_frame, text="🔍 Analyze Code",
                       command=lambda: threading.Thread(target=analyze_code_async).start(),
                       font=BUTTON_FONT, bg=ACCENT_COLOR, fg="white",
                       activebackground=BUTTON_HOVER_COLOR, activeforeground="white",
                       cursor="hand2", relief=tk.FLAT, padx=16, pady=10, bd=0)
run_button.pack(side=tk.LEFT)
run_button.bind("<Enter>", on_enter)
run_button.bind("<Leave>", on_leave)

clear_btn = tk.Button(button_frame, text="🗑️ Clear Output",
                      command=clear_output, font=BUTTON_FONT,
                      bg="#7c3aed", fg="white", activebackground="#6d28d9",
                      activeforeground="white", cursor="hand2", relief=tk.FLAT, padx=14, pady=10, bd=0)
clear_btn.pack(side=tk.LEFT, padx=(15, 0))

spinner_label = tk.Label(button_frame, text="", font=("Segoe UI", 11, "italic"), bg=BG_COLOR, fg="#facc15")
spinner_label.pack(side=tk.LEFT, padx=(15, 0))

# --- Output Box ---
output_label = tk.Label(main_frame, text="🧾 Output & Explanation", font=LABEL_FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
output_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 8))

output_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=3, relief="ridge")
output_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 20))

output_display = tk.Text(output_frame, width=90, height=20, font=OUTPUT_FONT,
                        bg=TEXT_BG_COLOR, fg=ERROR_TEXT_COLOR,
                        relief=tk.FLAT, state=tk.DISABLED, wrap=tk.WORD,
                        bd=0, insertbackground=ACCENT_COLOR, spacing3=4)
output_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
output_display.tag_configure("error", foreground=ERROR_TEXT_COLOR)
output_display.tag_configure("success", foreground=SUCCESS_TEXT_COLOR)

output_display.config(state=tk.NORMAL)
output_display.insert(tk.END, "🔸 Enter Python code above and click 'Analyze Code' to detect errors and explanations.\n")
output_display.config(state=tk.DISABLED)

# --- Keyboard Shortcuts ---
window.bind("<Control-Return>", run_code_shortcut)
window.bind("<Control-l>", clear_output_shortcut)

# --- Initial Setup ---
update_line_numbers()

window.mainloop()
