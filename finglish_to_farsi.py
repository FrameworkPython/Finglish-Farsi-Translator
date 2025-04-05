import re
import argparse

char_map = {
    'a': 'ا', 'A': 'آ', 'e': 'ع', 'E': 'اِ', 'i': 'ی', 'o': 'ُ', 
    'b': 'ب', 'c': 'ث', 'd': 'د', 'f': 'ف', 'g': 'گ', 'h': 'ه', 
    'j': 'ج', 'k': 'ک', 'l': 'ل', 'm': 'م', 'n': 'ن', 'p': 'پ', 
    'q': 'ق', 'r': 'ر', 's': 'س', 'S': 'ث', 't': 'ت', 'T': 'ط', 
    'u': 'و', 'v': 'و', 'w': 'و', 'x': 'خ', 'y': 'ی', 'z': 'ز', 
    'Z': 'ذ', 'Z': 'ظ', 'Z': 'ض', 'sh': 'ش', 'ch': 'چ', 'zh': 'ژ', 
    'kh': 'خ', 'gh': 'ق'
}

def is_emoji(s):
    return bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]', s))

def Finglish_be_Farsi(matn):
    sorted_keys = sorted(char_map.keys(), key=len, reverse=True)
    for key in sorted_keys:
        matn = re.sub(re.escape(key), char_map[key], matn)
    return matn

def Farsi_be_Finglish(matn):
    temp_char_map = {v: k for k, v in char_map.items()}
    for persian_char, finglish_char in temp_char_map.items():
        matn = re.sub(re.escape(persian_char), finglish_char, matn)
    return matn

def Tashkhis_va_Tarjome(matn):
    if re.search(r'[a-zA-Z]', matn): 
        return Finglish_be_Farsi(matn)
    result = []
    for segment in re.split(r'(\s+)', matn):
        if re.search(r'[آ-ی]', segment) and not is_emoji(segment):
            result.append(Farsi_be_Finglish(segment))
        else:
            result.append(segment)
    return ''.join(result)

def translate_terminal():
    while True:
        input_text = input("Enter text (type 'exit' to quit): ").strip()
        if input_text.lower() == 'exit':
            break
        result_text = Tashkhis_va_Tarjome(input_text)
        print("Translated text:", result_text)

def translate_gui():
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox

    def translate():
        input_text = input_box.get("1.0", tk.END).strip()
        if input_text:
            result_text = Tashkhis_va_Tarjome(input_text)
            output_box.config(state=tk.NORMAL)
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, result_text)
            output_box.config(state=tk.DISABLED)

    def paste_text():
        try:
            clipboard_text = app.clipboard_get()
            input_box.insert(tk.END, clipboard_text)
        except tk.TclError:
            messagebox.showerror("Error", "No text in clipboard")

    def copy_text():
        output_text = output_box.get("1.0", tk.END).strip()
        if output_text:
            app.clipboard_clear()
            app.clipboard_append(output_text)
            messagebox.showinfo("Success", "Text copied to clipboard")

    def delete_text():
        input_box.delete("1.0", tk.END)
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.config(state=tk.DISABLED)

    app = tk.Tk()
    app.title("Finglish/Farsi Translator")

    main_frame = ttk.Frame(app, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    input_label = ttk.Label(main_frame, text="Enter text:")
    input_label.grid(row=0, column=0, sticky=tk.W)

    input_box = tk.Text(main_frame, height=10, width=50)
    input_box.grid(row=1, column=0, columnspan=3, pady=5)

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, columnspan=3, pady=5)

    paste_button = ttk.Button(button_frame, text="Paste", command=paste_text)
    paste_button.grid(row=0, column=0, padx=(0, 5))

    translate_button = ttk.Button(button_frame, text="Translate", command=translate)
    translate_button.grid(row=0, column=1, padx=(5, 5))

    delete_button = ttk.Button(button_frame, text="Delete", command=delete_text)
    delete_button.grid(row=0, column=2, padx=(5, 0))

    output_label = ttk.Label(main_frame, text="Translated text:")
    output_label.grid(row=3, column=0, sticky=tk.W)

    output_box = tk.Text(main_frame, height=10, width=50, state=tk.DISABLED)
    output_box.grid(row=4, column=0, columnspan=3, pady=5)

    copy_button = ttk.Button(main_frame, text="Copy", command=copy_text)
    copy_button.grid(row=5, column=0, columnspan=3)

    app.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finglish-Farsi Translator")
    parser.add_argument('--mode', choices=['gui', 'terminal'], default='gui', help="Choose the mode of operation: gui or terminal")
    args = parser.parse_args()

    if args.mode == 'gui':
        translate_gui()
    else:
        translate_terminal()
