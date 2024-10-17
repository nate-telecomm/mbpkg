#!/usr/bin/env python3

import tkinter as tk
import random
import threading
for n in range(10):
    def allofthisstuff():
        class MovingMessageBox:
            def __init__(self, root):
                self.root = root
                self.root.title("Moving Message Box")
            
                # Create a label for the message
                self.message_label = tk.Label(root, text="hi", font=("Helvetica", 16))
                self.message_label.pack()

                # Set the size of the window
                self.root.geometry("100x100")  # Fixed size
                self.root.overrideredirect(True)  # Remove window decorations (title bar, etc.)

                # Start the movement
                self.move_message()

            def move_message(self):
                # Get the width and height of the screen
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()

                # Generate random positions
                new_x = random.randint(0, screen_width - self.message_label.winfo_width())
                new_y = random.randint(0, screen_height - self.message_label.winfo_height())

                # Move the message
                self.root.geometry(f"+{new_x}+{new_y}")

                # Schedule the next movement after 1000 milliseconds (1 second)
                self.root.after(1, self.move_message)

        if __name__ == "__main__":
            root = tk.Tk()
            app = MovingMessageBox(root)
            root.mainloop()
    t = threading.Thread(target=allofthisstuff)
    t.start()
