import tkinter as tk
import random

number_list = [6, 12, 24, 48]

class NumberTableApp:
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
            else:
                self.table[last_empty][col] = new_number
        else:
            # Ha az oszlop tele van, csak akkor adja hozzá, ha az alján lévő szám megegyezik
            if self.table[self.rows - 1][col] == new_number:
                self.history.append([row[:] for row in self.table])  # Lépés mentése
                self.table[self.rows - 1][col] *= 2
            else:
                return  # Ha nem egyezik, nem csinál semmit

        self.update_display()
        self.generate_new_number()

    def update_display(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].config(text=str(self.table[r][c]) if self.table[r][c] is not None else "")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberTableApp(root)
    root.mainloop()
