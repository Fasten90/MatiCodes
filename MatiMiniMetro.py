import tkinter as tk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rajzoló alkalmazás")
        
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        
        self.last_x = None
        self.last_y = None
        
        self.clear_button = tk.Button(root, text="Törlés", command=self.clear_canvas)
        self.clear_button.pack()
    
    def draw(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=2, capstyle=tk.ROUND, smooth=tk.TRUE)
        self.last_x = event.x
        self.last_y = event.y
    
    def reset(self, event):
        self.last_x = None
        self.last_y = None
    
    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

