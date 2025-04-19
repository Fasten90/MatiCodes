import tkinter as tk
import random
from datetime import timedelta, datetime

# --- Konverziós segédfüggvények ---
def time_to_minutes(timestr):
    h, m = map(int, timestr.split(":"))
    return h * 60 + m

def minutes_to_time(minutes):
    minutes = minutes % (24 * 60)
    h = minutes // 60
    m = minutes % 60
    return f"{h:02}:{m:02}"

# --- Játék osztály ---
class TimeCollisionGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=600, bg='black')
        self.canvas.pack()

        self.level = 1
        self.spawned_count = 0
        self.max_spawns = random.randint(20, 40)
        self.finished = False

        self.level_text = self.canvas.create_text(10, 10, anchor='nw', fill='white',
                                                  text=f"Szint: {self.level}", font=("Arial", 14, "bold"))

        self.player_time = 12  # 00:12 perc
        self.player = self.canvas.create_text(
            200, 550, text=minutes_to_time(self.player_time),
            fill="white", font=("Arial", 24, "bold")
        )
        self.player_speed = 10

        self.falling_times = []
        self.wall = None
        self.wall_time = None

        self.bind_keys()
        self.spawn_time()
        self.update()

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.move_player(-self.player_speed, 0))
        self.root.bind("<Right>", lambda e: self.move_player(self.player_speed, 0))
        self.root.bind("<Up>", lambda e: self.move_player(0, -self.player_speed))
        self.root.bind("<Down>", lambda e: self.move_player(0, self.player_speed))

    def move_player(self, dx, dy):
        x, y = self.canvas.coords(self.player)
        new_x = max(20, min(380, x + dx))
        new_y = max(300, min(580, y + dy))  # Alsó fél pálya
        self.canvas.coords(self.player, new_x, new_y)

    def spawn_time(self):
        if self.spawned_count < self.max_spawns:
            random_minutes = random.randint(1, 180)
            time_str = minutes_to_time(random_minutes)
            x = random.randint(50, 350)
            obj = self.canvas.create_text(x, -30, text=time_str, fill="cyan", font=("Arial", 20, "bold"))
            self.falling_times.append((obj, random_minutes))
            self.spawned_count += 1
            self.root.after(1200, self.spawn_time)
        elif not self.wall:
            self.spawn_wall()

    def spawn_wall(self):
        # Pálya végi "fal"
        self.wall_time = random.randint(60, 240)  # 1:00 - 4:00
        time_str = minutes_to_time(self.wall_time)
        self.wall = self.canvas.create_text(200, -30, text=f"⛔ {time_str} ⛔",
                                            fill="red", font=("Arial", 22, "bold"))
    
    def check_collision(self):
        px, py = self.canvas.coords(self.player)
        for obj, t_minutes in list(self.falling_times):
            ox, oy = self.canvas.coords(obj)
            if abs(ox - px) < 50 and abs(oy - py) < 30:
                self.player_time += t_minutes
                self.canvas.itemconfig(self.player, text=minutes_to_time(self.player_time))
                self.canvas.delete(obj)
                self.falling_times.remove((obj, t_minutes))

    def check_wall_collision(self):
        if not self.wall:
            return
        px, py = self.canvas.coords(self.player)
        wx, wy = self.canvas.coords(self.wall)
        if abs(wx - px) < 50 and abs(wy - py) < 30:
            if self.player_time > self.wall_time:
                # Áttörjük!
                self.canvas.delete(self.wall)
                self.wall = None
                self.level += 1
                self.spawned_count = 0
                self.max_spawns = random.randint(20, 40)
                self.canvas.itemconfig(self.level_text, text=f"Szint: {self.level}")
                self.root.after(1000, self.spawn_time)
            else:
                # Játék vége
                self.canvas.create_text(200, 300, text="VÉGE A JÁTÉKNAK 😢", fill="yellow",
                                        font=("Arial", 26, "bold"))
                self.finished = True

    def update(self):
        if self.finished:
            return

        to_remove = []
        for obj, t_minutes in self.falling_times:
            self.canvas.move(obj, 0, 5)
            _, y = self.canvas.coords(obj)
            if y > 620:
                self.canvas.delete(obj)
                to_remove.append((obj, t_minutes))

        for item in to_remove:
            if item in self.falling_times:
                self.falling_times.remove(item)

        if self.wall:
            self.canvas.move(self.wall, 0, 4)

        self.check_collision()
        self.check_wall_collision()
        self.root.after(50, self.update)

# --- Futtatás ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Óraütközés Játék")
    game = TimeCollisionGame(root)
    root.mainloop()
