import tkinter as tk
import random

#number_list = [6, 12, 24, 48]
number_list = [2, 4, 8, 16, 32, 64]

colour_list = [
    [1, "#FFC0CB"],   # rózsaszín
    [2, "#FFA500"],   # narancssárga
    [4, "#800080"],   # lila
    [8, "#8B4513"],   # barna
    [16, "#808080"],  # szürke
    [32, "#FF0000"],  # piros
    [64, "#00008B"],  # sötétkék
    [128, "#FFFF00"], # sárga
    [256, "#ADD8E6"], # világoskék
    [512, "#800000"], # bordó
    [1024, "#90EE90"],# világoszöld
    [2048, "#006400"],# sötétzöld
    [4096, "#B22222"],# vörös
    [8192, "#D8BFD8"],# világoslila
]

# Gyors kereséshez dictionary
colour_map = {value: code for value, code in colour_list}


class NumberTableApp:
    # Ezt a sort figyelni kell, a telegramban formázás lesz, a dupla aláhúzás
    def __init__(self, root):
        self.root = root
        self.root.title("Szám táblázat")

        self.rows = 5
        self.cols = 4
        self.table = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.history = []

        self.buttons = []
        for col in range(self.cols):
            btn = tk.Button(root, text=f"Oszlop {col+1}", command=lambda c=col: self.add_number_to_column(c))
            btn.grid(row=0, column=col)
            self.buttons.append(btn)

        self.cells = [[tk.Label(root, text="", width=10, height=2, relief="ridge", borderwidth=2) 
                       for _ in range(self.cols)] for _ in range(self.rows)]

        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].grid(row=r+1, column=c)

        self.number_var = tk.StringVar(value=str(random.choice(number_list)))
        tk.Label(root, text="Következő szám:").grid(row=self.rows+1, column=0, columnspan=2)
        self.number_entry = tk.Entry(root, textvariable=self.number_var, font=("Arial", 14))
        self.number_entry.grid(row=self.rows+1, column=2, columnspan=2)

        self.undo_button = tk.Button(root, text="Visszavonás", command=self.undo_last_move)
        self.undo_button.grid(row=self.rows+2, column=0, columnspan=2)

        self.clear_button = tk.Button(root, text="Törlés", command=self.clear_table)
        self.clear_button.grid(row=self.rows+2, column=2, columnspan=2)

    def add_number_to_column(self, col):
        new_number = int(self.number_var.get())
        last_empty = None

        for row in range(self.rows):  # Fentről lefelé keres
            if self.table[row][col] is None:
                last_empty = row
                break

        if last_empty is not None:
            self.history.append([row[:] for row in self.table])  # Lépés mentése
            if last_empty > 0 and self.table[last_empty - 1][col] == new_number:
                self.table[last_empty - 1][col] *= 2
                self.merge_upwards(last_empty - 1, col)
            else:
                self.table[last_empty][col] = new_number
        else:
            # Ha az oszlop tele van, csak akkor adja hozzá, ha az alján lévő szám megegyezik
            if self.table[self.rows - 1][col] == new_number:
                self.history.append([row[:] for row in self.table])  # Lépés mentése
                self.table[self.rows - 1][col] *= 2
                self.merge_upwards(self.rows - 1, col)
            else:
                return  # Ha nem egyezik, nem csinál semmit

        self.update_display()
        self.generate_new_number()

    def merge_upwards(self, row, col):
        while row > 0 and self.table[row][col] == self.table[row - 1][col]:
            self.table[row - 1][col] *= 2
            self.table[row][col] = None
            row -= 1

    def update_display(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell_number = self.table[r][c]
                self.cells[r][c].config(text=str(cell_number) if cell_number is not None else "")
                if cell_number and isinstance(cell_number, int):
                    if cell_number in colour_map:
                        self.cells[r][c].config(fg=colour_map[cell_number])

    def generate_new_number(self):
        self.number_var.set(str(random.choice(number_list)))

    def undo_last_move(self):
        if self.history:
            self.table = self.history.pop()
            self.update_display()
            self.generate_new_number()

    def clear_table(self):
        self.history.append([row[:] for row in self.table])  # Lépés mentése
        self.table = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.update_display()
        self.generate_new_number()

# Ezt a sort figyelni kell, a telegramban formázás lesz, a dupla aláhúzás
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberTableApp(root)
    root.mainloop()
