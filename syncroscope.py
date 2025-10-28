import tkinter as tk
import math

class Syncroscope:
    def __init__(self, root, turbine):
        self.root = root

        self.turbine = turbine
        
        # Canvas for the synchronoscope
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack(anchor="e")

        # indicators
        self.ind1 = self.canvas.create_oval(30,30,60,60,fill="gray")
        self.ind2 = self.canvas.create_oval(235,30,265,60,fill="gray")
        
        # Draw the circular dial
        self.canvas.create_oval(50, 50, 250, 250, fill="lightgray")
        self.canvas.create_oval(50, 50, 250, 250, outline="black", width=2)
        self.canvas.create_text(150, 20, text="Syncroscope", font=("Arial", 14))
        
        # Draw markers on the dial
        for angle in range(0, 360, 30):
            x1 = 150 + 90 * math.cos(math.radians(angle))
            y1 = 150 - 90 * math.sin(math.radians(angle))
            x2 = 150 + 100 * math.cos(math.radians(angle))
            y2 = 150 - 100 * math.sin(math.radians(angle))
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
            
        # Draws the green sync lines
        x1 = 150 + 90 * math.cos(math.radians(86))
        y1 = 150 - 90 * math.sin(math.radians(86))
        x2 = 150 + 100 * math.cos(math.radians(86))
        y2 = 150 - 100 * math.sin(math.radians(86))
        self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3)
        x1 = 150 + 90 * math.cos(math.radians(94))
        y1 = 150 - 90 * math.sin(math.radians(94))
        x2 = 150 + 100 * math.cos(math.radians(94))
        y2 = 150 - 100 * math.sin(math.radians(94))
        self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3)
        
        # Create the needle
        self.needle = self.canvas.create_line(150, 150, 150, 60, fill="red", width=3)
        
        # Start the animation
        self.angle = 0
        self.animate()

    def animate(self):
        # Simulate the needle rotation
        self.temp = 60 - self.turbine.hertz
        self.angle += self.temp  # Adjust speed by changing this value
        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        
        if 86 < self.angle < 94:
            self.canvas.delete(self.ind1)
            self.ind1 = self.canvas.create_oval(30,30,60,60,fill="yellow")
        else:
            self.canvas.delete(self.ind1)
            self.ind1 = self.canvas.create_oval(30,30,60,60,fill="gray")
        if 2990 < self.turbine.rpm < 3010:
            self.canvas.delete(self.ind2)
            self.ind2 = self.canvas.create_oval(235,30,265,60,fill="yellow")
        else:
            self.canvas.delete(self.ind2)
            self.ind2 = self.canvas.create_oval(235,30,265,60,fill="gray")

        # Calculate needle position
        x = 150 + 90 * math.cos(math.radians(self.angle))
        y = 150 - 90 * math.sin(math.radians(self.angle))
        
        # Update needle position
        self.canvas.coords(self.needle, 150, 150, x, y)
        
        # Repeat animation
        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    import turbine
    t = turbine.Turbine(root)
    root.mainloop()