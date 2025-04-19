import tkinter as tk
import random

# --- Segédfüggvények ---
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
        self.wall_objects = []
        self.wall_times = []

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
        elif not self.wall_objects:
            self.spawn_wall()

    def spawn_wall(self):
        self.wall_times = []
        self.wall_objects = []
        base_minutes = random.randint(60, 180)  # 1:00 - 3:00
        for i in range(3):
            t = base_minutes + i * 60
            self.wall_times.append(t)
            time_str = minutes_to_time(t)
            y = -60 - i * 50
            wall = self.canvas.create_text(200, y, text=f"🧱 {time_str} 🧱", fill="orange", font=("Arial", 20, "bold"))
            self.wall_objects.append((wall, t))

    def move_walls(self):
        for wall, _ in self.wall_objects:
            self.canvas.move(wall, 0, 3)

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
        if not self.wall_objects:
            return

        px, py = self.canvas.coords(self.player)
        for wall, t in self.wall_objects:
            wx, wy = self.canvas.coords(wall)
            if abs(wx - px) < 50 and abs(wy - py) < 30:
                if self.player_time >= t:
                    self.canvas.itemconfig(wall, fill="gray")  # áttörve
                else:
                    self.end_game()
                    break

    def end_game(self):
        if self.finished:
            return
        self.finished = True
        self.canvas.create_text(200, 250, text="🏁 VÉGE A PÁLYÁNAK 🏁", fill="yellow", font=("Arial", 24, "bold"))

        self.btn_frame = tk.Frame(self.root, bg='black')
        self.btn_frame.place(relx=0.5, rely=0.6, anchor='n')

        tk.Button(self.btn_frame, text="Next Level", font=("Arial", 14),
                  command=self.next_level).pack(pady=5)
        tk.Button(self.btn_frame, text="Restart", font=("Arial", 14),
                  command=self.restart).pack(pady=5)
        tk.Button(self.btn_frame, text="Quit", font=("Arial", 14),
                  command=self.root.quit).pack(pady=5)

    def next_level(self):
        self.btn_frame.destroy()
        self.level += 1
        self.player_time = 12
        self.canvas.itemconfig(self.player, text=minutes_to_time(self.player_time))
        self.canvas.itemconfig(self.level_text, text=f"Szint: {self.level}")
        for wall, _ in self.wall_objects:
            self.canvas.delete(wall)
        self.wall_objects.clear()
        self.wall_times.clear()
        self.spawned_count = 0
        self.finished = False
        self.falling_times.clear()
        self.spawn_time()

    def restart(self):
        self.btn_frame.destroy()
        for wall, _ in self.wall_objects:
            self.canvas.delete(wall)
        self.wall_objects.clear()
        self.wall_times.clear()
        self.spawned_count = 0
        self.finished = False
        self.player_time = 12
        self.canvas.itemconfig(self.player, text=minutes_to_time(self.player_time))
        self.canvas.itemconfig(self.level_text, text=f"Szint: {self.level}")
        for obj, _ in self.falling_times:
            self.canvas.delete(obj)
        self.falling_times.clear()
        self.spawn_time()

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

        self.move_walls()
        self.check_collision()
        self.check_wall_collision()
        self.root.after(50, self.update)

# --- Futtatás ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Óraütközés Játék")
    game = TimeCollisionGame(root)
    root.mainloop()
