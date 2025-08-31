import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from src.extract import extract_frames
from src.video_preview import VideoPreview
import threading

class VideoExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Extractor")
        self.video_path = None
        self.output_dir = None
        self.cancel_flag = {'cancel': False}
        self.preview = None

        self.setup_ui()

    def setup_ui(self):
        
        # Canvas for preview
        self.canvas = tk.Label(self.root, bg="black")
        self.canvas.pack(pady=10)
        self.preview = VideoPreview(self.canvas, self.root)


        # Frame for controls
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)


        # Buttons always available
        tk.Button(self.controls_frame, text="Select Video", command=self.select_video).grid(row=0, column=0, padx=5)
        tk.Button(self.controls_frame, text="Select Output Folder", command=self.select_output).grid(row=0, column=1, padx=5)
        
        # Frame interval input      
        tk.Label(self.root, text="Extract every Nth frame:").pack(pady=5)
        self.nth_entry = tk.Entry(self.root, width=5)
        self.nth_entry.insert(0, "1")  # default: every frame
        self.nth_entry.pack()


        # Buttons that appear only after selecting video
        self.play_btn = tk.Button(self.controls_frame, text="▶ Play/Pause", command=self.preview.pause)
        self.stop_btn = tk.Button(self.controls_frame, text="⏹ Stop", command=self.preview.stop)

        # Extraction buttons
        tk.Button(self.controls_frame, text="Extract Frames", command=self.start_extraction, bg="green", fg="white").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.controls_frame, text="Cancel Extraction", command=self.cancel_extraction, bg="red", fg="white").grid(row=2, column=1, padx=5, pady=5)


        # Success button (hidden until finished)
        self.success_btn = tk.Button(self.root, text="Done!", command=self.reset_ui, bg="blue", fg="white")


        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")])
        if self.video_path:
            self.preview.start(self.video_path)
            self.play_btn.grid(row=1, column=0, padx=5, pady=5)
            self.stop_btn.grid(row=1, column=1, padx=5, pady=5)
    
    def select_output(self):
        self.output_dir = filedialog.askdirectory()

    def start_extraction(self):
        if not self.video_path or not self.output_dir:
            messagebox.showerror("Error", "Please select video and output folder")
            return

        try:
            nth_frame=int(self.nth_entry.get())
            if nth_frame < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error!", "Please enter a valid positive number for Nth frame")
            return

        self.cancel_flag['cancel'] = False
        threading.Thread(target=self._extract_thread, args=(nth_frame,)).start()


    def _extract_thread(self, nth_frame):

        extract_frames(self.video_path, self.output_dir, nth_frame=nth_frame,
                    cancel_flag=self.cancel_flag,
                    progress_callback=self.update_progress)
        if not self.cancel_flag['cancel']:
            self.success_btn.pack(pady=10)


    def update_progress(self, frame_count, total_frames):
        progress = int(frame_count / total_frames * 100)
        self.progress_var.set(progress)
        self.root.update_idletasks()

    def cancel_extraction(self):
        self.cancel_flag['cancel'] = True


    def reset_ui(self):
        """Reset UI after success to allow new video selection"""
        self.video_path = None
        self.output_dir = None
        self.progress_var.set(0)
        self.canvas.config(image='', text="Video preview will appear here", bg="black")
        self.play_btn.grid_forget()
        self.stop_btn.grid_forget()
        self.success_btn.pack_forget()
