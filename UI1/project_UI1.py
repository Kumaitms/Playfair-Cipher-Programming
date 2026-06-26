import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

# Playfair cipher logic
def prepare_text(text):
    text = text.upper().replace("J", "I")
    prepared = ""
    i = 0
    while i < len(text):
        char1 = text[i]
        if char1 not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            i += 1
            continue
        if i + 1 < len(text):
            char2 = text[i + 1]
            if char2 == char1:
                char2 = 'X'
                i += 1
            else:
                i += 2
        else:
            char2 = 'X'
            i += 1
        prepared += char1 + char2
    return prepared

def generate_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")
    seen = set()
    matrix = []
    for char in keyword:
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and char not in seen:
            seen.add(char)
            matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None, None

def playfair_encrypt(plaintext, matrix):
    plaintext = prepare_text(plaintext)
    cipher = ""
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            cipher += matrix[row1][(col1 + 1) % 5]
            cipher += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher += matrix[(row1 + 1) % 5][col1]
            cipher += matrix[(row2 + 1) % 5][col2]
        else:
            cipher += matrix[row1][col2]
            cipher += matrix[row2][col1]
    return cipher
def playfair_decrypt(ciphertext, matrix):
    plaintext = ""

    # تأكد أن النص طوله زوجي
    if len(ciphertext) % 2 != 0:
        ciphertext += 'X'  # نضيف X إذا كان فردي

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if None in (row1, col1, row2, col2):
            continue

        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    return plaintext


# Encrypt / Decrypt Button Actions
def encrypt_mode():
    mode_var.set("encrypt")
    encrypt_button.configure(fg_color="#00ffff")
    decrypt_button.configure(fg_color="#112233")

def decrypt_mode():
    mode_var.set("decrypt")
    decrypt_button.configure(fg_color="#00ffff")
    encrypt_button.configure(fg_color="#112233")

def proceed_action():
    keyword = keyword_entry.get()
    text = input_entry.get()
    if not keyword or not text:
        messagebox.showerror("Error", "Please fill in both fields!")
        return
    matrix = generate_key_matrix(keyword)
    if mode_var.get() == "encrypt":
        result = playfair_encrypt(text, matrix)
    else:
        result = playfair_decrypt(text, matrix)
    output_box.delete("0.0", "end")
    output_box.insert("0.0", result.replace("X", ""))

# Window Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Playfair Cipher - Secure Tool")
root.geometry("900x600")
root.minsize(700, 500)

# Background Setup



bg_path = r"C:/Users/khale/OneDrive - King Faisal University/KFU/TY2/CS/Project/assets/background.png"     # Path here------------------------------




bg_image = Image.open(bg_path)
bg_ctk_image = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(900, 600))
bg_label = ctk.CTkLabel(root, image=bg_ctk_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def resize_background(event):
    # Resize the image to cover the window while maintaining aspect ratio
    new_width = event.width
    new_height = event.height
    bg_resized = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_ctk_image.configure(light_image=bg_resized, dark_image=bg_resized, size=(new_width, new_height))

root.bind("<Configure>", resize_background)

# Widgets (with fixed transparency)
title = ctk.CTkLabel(root, text="PLAYFAIR CIPHER", font=("Arial Black", 30), text_color="white", fg_color="transparent", bg_color="transparent")
title.place(relx=0.05, rely=0.05)

input_label = ctk.CTkLabel(root, text="Enter the text:", font=("Segoe UI", 16), fg_color="transparent", bg_color="transparent")
input_label.place(relx=0.05, rely=0.18)

input_entry = ctk.CTkEntry(root, width=300, height=40, border_width=2, corner_radius=8)
input_entry.place(relx=0.05, rely=0.23)

keyword_label = ctk.CTkLabel(root, text="Keyword:", font=("Segoe UI", 16), fg_color="transparent", bg_color="transparent")
keyword_label.place(relx=0.05, rely=0.35)

keyword_entry = ctk.CTkEntry(root, width=300, height=40, border_width=2, corner_radius=8)
keyword_entry.place(relx=0.05, rely=0.4)

mode_var = ctk.StringVar(value="encrypt")

encrypt_button = ctk.CTkButton(root, text="Encrypt", width=120, height=35, command=encrypt_mode, corner_radius=10, fg_color="#00ffff", text_color="black")
encrypt_button.place(relx=0.05, rely=0.53)

decrypt_button = ctk.CTkButton(root, text="Decrypt", width=120, height=35, command=decrypt_mode, corner_radius=10, fg_color="#112233", text_color="white")
decrypt_button.place(relx=0.25, rely=0.53)

proceed_button = ctk.CTkButton(root, text="Proceed", command=proceed_action, width=260, height=45, font=("Segoe UI", 18), corner_radius=20, fg_color="#00c4cc", text_color="black")
proceed_button.place(relx=0.05, rely=0.62)

output_label = ctk.CTkLabel(root, text="The output", font=("Segoe UI", 16), fg_color="transparent", bg_color="transparent")
output_label.place(relx=0.65, rely=0.1)

output_box = ctk.CTkTextbox(root, width=250, height=250, corner_radius=15, fg_color="#0A0A0A")
output_box.place(relx=0.65, rely=0.2)

# Run Main Loop
root.mainloop()
