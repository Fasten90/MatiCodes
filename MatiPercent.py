import tkinter as tk
import time

def fut():
    # példa: (kezdő, vég, szín)
    szakaszok = [
        (0, 10, "red"),
        (10, 50, "orange"),
        (50, 90, "yellow"),
        (90, 100, "green"),
    ]

    for start, end, color in szakaszok:
        for i in range(start, end):
            fill_height = rh * (i / 100)
            canvas.coords(rect, x1, y2 - fill_height, x2, y2)
            canvas.itemconfig(rect, fill=color)
            canvas.itemconfig(text_item, text=str(i) + " %")
            root.update()
            time.sleep(1)

    for _ in range(100):
        root.update()
        time.sleep(1)

def kilep(event):
    root.destroy()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", kilep)
root.protocol("WM_DELETE_WINDOW", lambda: None)

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True)

# Képernyőméret
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

# Téglalap méretei
rw = w // 3
rh = h // 3

x1 = w//2 - rw//2
y1 = h//2 - rh//2
x2 = w//2 + rw//2
y2 = h//2 + rh//2

rect = canvas.create_rectangle(x1, y2, x2, y2, fill="white")
text_item = canvas.create_text(w//2, h//2, text="", fill="black", font=("Arial", 40))

fut()

root.mainloop()

