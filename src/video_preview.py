import cv2
from PIL import Image, ImageTk

class VideoPreview:
    def __init__(self, canvas, root, width=640, height=360):
        self.canvas = canvas
        self.root = root
        self.width = width
        self.height = height
        self.cap = None
        self.running = False
        self.paused = False

    def start(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.running = True
        self.paused = False
        self._update_frame()

    def _update_frame(self):
        if not self.running:
            if self.cap:
                self.cap.release()
            return
        if not self.paused:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(img)
                self.canvas.config(image=imgtk)
                self.canvas.image = imgtk
        self.root.after(30, self._update_frame)

    def pause(self):
        self.paused = not self.paused

    def stop(self):
        self.running = False
