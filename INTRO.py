import tkinter as tk
from PIL import Image, ImageTk

def play_gif():
    """Plays a GIF animation at startup and closes automatically."""
    root = tk.Tk()
    root.title("Welcome Animation")
    
    # Load the GIF
    gif_path = "jarvis-tony-stark.gif"  # Ensure this file exists
    gif = Image.open(gif_path)
    frames = []

    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))  # Move to next frame
    except EOFError:
        pass  # End of GIF frames

    label = tk.Label(root)
    label.pack()

    def update(ind=0):
        """Update function for animation"""
        if ind < len(frames):
            label.configure(image=frames[ind])
            root.after(50, update, ind + 1)  # Adjust speed (50ms per frame)
        else:
            root.quit()  # Close window after the animation finishes

    root.after(0, update)  # Start animation
    root.mainloop()  # Run Tkinter event loop

if __name__ == "__main__":
    play_gif()

