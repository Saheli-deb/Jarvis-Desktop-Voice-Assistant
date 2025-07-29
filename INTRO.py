import tkinter as tk
from PIL import Image, ImageTk
import os

def play_gif():
    """Plays a GIF animation at startup in full screen and closes automatically."""
    root = tk.Tk()
    root.title("Welcome Animation")
    
    # Make window full screen
    root.attributes('-fullscreen', True)
    root.configure(bg='black')
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Load the GIF
    gif_path = "jarvis-tony-stark.gif"  # Ensure this file exists
    gif = Image.open(gif_path)
    frames = []

    try:
        while True:
            # Resize frame to fit screen while maintaining aspect ratio
            frame = gif.copy()
            frame.thumbnail((screen_width, screen_height), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(len(frames))  # Move to next frame
    except EOFError:
        pass  # End of GIF frames

    # Center the label
    label = tk.Label(root, bg='black')
    label.place(relx=0.5, rely=0.5, anchor='center')

    def update(ind=0):
        """Update function for animation"""
        if ind < len(frames):
            label.configure(image=frames[ind])
            root.after(50, update, ind + 1)  # Adjust speed (50ms per frame)
        else:
            root.quit()  # Close window after the animation finishes

    root.after(0, update)  # Start animation
    root.mainloop()  # Run Tkinter event loop

def play_gif_with_menu():
    """Plays GIF and then shows startup menu"""
    # Play the GIF first
    play_gif()
    
    # Then show the startup menu
    from startup_menu import display_startup_menu
    display_startup_menu()

if __name__ == "__main__":
    play_gif_with_menu()

