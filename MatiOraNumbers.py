import tkinter as tk
import random
from datetime import timedelta, datetime

# --- Konverziós segédfüggvények ---
def time_to_minutes(timestr):
    h, m = map(int, timestr.split(":"))
    return h * 60 + m

def minutes_to_time(minutes):
    minutes = minutes % (24 * 60)  # max 24h
    h = minutes // 60
    m = minutes % 60
    return f"{h:02}:{m:02}"

# --- Játék osztály ---
class TimeCollisionGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=600, bg='black')
        self.canvas.pack()

        self.player_time = 12  # 00:12 perc
        self.player = self.canvas.create_text(
            200, 550, text=minutes_to_time(self.player_time),
            fill="white", font=("Arial", 24, "bold")
        )

        self.falling_times = []
        self.spawn_time()
        self.update()

    def spawn_time(self):
        random_minutes = random.randint(1, 180)  # 0:01 - 3:00 között
        time_str = minutes_to_time(random_minutes)
        x = random.randint(50, 350)
        obj = self.canvas.create_text(x, -30, text=time_str, fill="cyan", font=("Arial", 20, "bold"))
        self.falling_times.append((obj, random_minutes))
        self.root.after(2000, self.spawn_time)

    def check_collision(self):
        px1, py1 = self.canvas.coords(self.player)
        for obj, t_minutes in self.falling_times:
            ox, oy = self.canvas.coords(obj)
            if abs(ox - px1) < 50 and abs(oy - py1) < 30:
                # Ütközés!
                self.player_time += t_minutes
                self.canvas.itemconfig(self.player, text=minutes_to_time(self.player_time))
                self.canvas.delete(obj)
                self.falling_times.remove((obj, t_minutes))

    def update(self):
        to_remove = []
        for obj, t_minutes in self.falling_times:
            self.canvas.move(obj, 0, 5)
            _, y = self.canvas.coords(obj)
            if y > 600:
                self.canvas.delete(obj)
                to_remove.append((obj, t_minutes))

        for item in to_remove:
            self.falling_times.remove(item)

        self.check_collision()
        self.root.after(50, self.update)

# --- Futtatás ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Óraütközés Játék")
    game = TimeCollisionGame(root)
    root.mainloop()

