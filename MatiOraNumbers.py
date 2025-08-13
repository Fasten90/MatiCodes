import tkinter as tk
import random

def time_to_minutes(timestr):
    h, m = map(int, timestr.split(":"))
    return h * 60 + m

def minutes_to_time(minutes):
    minutes = minutes % (24 * 60)
    h = minutes // 60
    m = minutes % 60
    return f"{h:02}:{m:02}"

class TimeCollisionGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=600, bg='black')
        self.canvas.pack()

        self.level = 1
        self.player_speed = 10
        self.init_game()

    def init_game(self):
        self.reset_game()  # Reset everything before starting new game
        
        self.finished = False
        self.spawned_count = 0
        self.max_spawns = random.randint(20, 40)

        self.falling_times = []
        self.wall_objects = []
        self.wall_times = []

        self.level_text = self.canvas.create_text(10, 10, anchor='nw', fill='white',
                                                  text=f"Szint: {self.level}", font=("Arial", 14, "bold"))

        self.player_time = 12  # 00:12
        self.player = self.canvas.create_text(
            200, 550, text=minutes_to_time(self.player_time),
            fill="white", font=("Arial", 24, "bold")
        )

        self.bind_controls()
        self.spawn_time()
        self.update()

    def reset_game(self):
        """Reset the game state, clearing all objects and variables."""
        self.canvas.delete("all")  # Delete everything on the canvas
        self.level = 1
        self.player_speed = 10
        self.spawned_count = 0
        self.falling_times = []
        self.wall_objects = []
        self.wall_times = []

    def bind_controls(self):
        self.root.bind("<Left>", lambda e: self.move_player(-self.player_speed, 0))
        self.root.bind("<Right>", lambda e: self.move_player(self.player_speed, 0))
        self.root.bind("<Up>", lambda e: self.move_player(0, -self.player_speed))
        self.root.bind("<Down>", lambda e: self.move_player(0, self.player_speed))

        self.canvas.bind("<Button-1>", self.touch_start)
        self.canvas.bind("<B1-Motion>", self.touch_move)

        self.last_touch = None

    def touch_start(self, event):
        self.last_touch = (event.x, event.y)

    def touch_move(self, event):
        if self.last_touch:
            dx = event.x - self.last_touch[0]
            dy = event.y - self.last_touch[1]
            self.move_player(dx, dy)
            self.last_touch = (event.x, event.y)

    def move_player(self, dx, dy):
        x, y = self.canvas.coords(self.player)
        new_x = max(20, min(380, x + dx))
        new_y = max(300, min(580, y + dy))
        self.canvas.coords(self.player, new_x, new_y)

    def spawn_time(self):
        if self.spawned_count < self.max_spawns:
            random_minutes = random.randint(5, 60)
            time_str = minutes_to_time(random_minutes)
            x = random.randint(50, 350)
            obj = self.canvas.create_text(x, -30, text=time_str, fill="cyan", font=("Arial", 20, "bold"))
            self.falling_times.append((obj, random_minutes))
            self.spawned_count += 1
            self.root.after(1000, self.spawn_time)
        elif not self.wall_objects:
            self.spawn_wall()

    def spawn_wall(self):
        self.wall_times = []
        self.wall_objects = []

        extra = random.randint(2, 4)
        max_time = self.player_time + (extra * 60)

        current = 0
        while current <= max_time:
            self.wall_times.append(current)
            current += 60

        for i, t in enumerate(self.wall_times):
            time_str = minutes_to_time(t)
            y = -60 - i * 40
            wall = self.canvas.create_text(200, y, text=f"🧱 {time_str} 🧱", fill="orange", font=("Arial", 18, "bold"))
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
        if not self.wall_objects or self.finished:
            return

        px, py = self.canvas.coords(self.player)
        for i, (wall, wall_minutes) in enumerate(self.wall_objects):
            wx, wy = self.canvas.coords(wall)
            if abs(px - wx) < 60 and abs(py - wy) < 30:
                if self.player_time >= wall_minutes:
                    # Fal áttörve
                    self.canvas.itemconfig(wall, fill="gray")
                else:
                    # Nem tudtunk áttörni → játék vége itt
                    self.canvas.itemconfig(wall, fill="red")
                    self.end_game(i)
                    return

        # Ha minden falon átjutottunk
        if self.wall_objects[-1][1] <= self.player_time:
            self.end_game(len(self.wall_objects) - 1)

    def end_game(self, last_reached_index):
        self.finished = True

        total = len(self.wall_objects)
        for i, (wall, _) in enumerate(self.wall_objects):
            if i <= last_reached_index and self.player_time >= self.wall_objects[i][1]:
                self.canvas.itemconfig(wall, fill="gray")
            elif i > last_reached_index:
                self.canvas.itemconfig(wall, fill="red")

        if last_reached_index == total - 1:
            msg = "🎉 Áttörted az összes falat!"
        elif last_reached_index == -1:
            msg = "😢 Egy falat sem tudtál áttörni."
        else:
            msg = f"🏁 Áttört falak: {last_reached_index + 1} / {total}"

        self.canvas.create_text(200, 250, text=msg, fill="yellow", font=("Arial", 18, "bold"))
        self.show_end_buttons()

    def show_end_buttons(self):
        self.btn_frame = tk.Frame(self.root, bg='black')
        self.btn_frame.place(relx=0.5, rely=0.6, anchor='n')

        tk.Button(self.btn_frame, text="Következő pálya", font=("Arial", 14),
                  command=self.start_new_level).pack(pady=5)
        tk.Button(self.btn_frame, text="Újrapróbálás", font=("Arial", 14),
                  command=self.restart).pack(pady=5)
        tk.Button(self.btn_frame, text="Kilépés", font=("Arial", 14),
                  command=self.root.quit).pack(pady=5)

    def start_new_level(self):
        self.level += 1
        self.btn_frame.destroy()
        self.init_game()

    def restart(self):
        self.btn_frame.destroy()
        self.init_game()

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Óraütközés Játék")
    game = TimeCollisionGame(root)
    root.mainloop()
