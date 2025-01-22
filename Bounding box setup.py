import tkinter as tk
from pynput import keyboard

class ScreenSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.selection_window = None

        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+s': self.start_selection
        })
        self.hotkey_listener.start()

    def start_selection(self):
        self.selection_window = tk.Toplevel()
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)  # Semi-transparent overlay
        self.selection_window.attributes('-topmost', True)
        self.selection_window.config(cursor="cross")
        self.canvas = tk.Canvas(self.selection_window, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        thelist = [self.start_x, self.start_y, event.x, event.y]
        print(thelist)
        self.selection_window.destroy()

    def run(self):
        print("Press Ctrl+Shift+S to start the selection tool.")
        self.root.mainloop()

if __name__ == "__main__":
    selector = ScreenSelector()
    selector.run()




