import tkinter as tk
from src.gui import VideoExtractorGUI

root = tk.Tk()
app = VideoExtractorGUI(root)
root.geometry("700x550")
root.mainloop()
