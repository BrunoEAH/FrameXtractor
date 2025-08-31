import cv2
import os

def extract_frames(video_path, output_folder, nth_frame=1, cancel_flag=None, progress_callback=None):
    """
    Extracts every nth frame from a video.
    cancel_flag: a mutable object like {'cancel': False} to allow stopping extraction
    progress_callback: a function to update GUI progress
    """
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    saved_count = 0

    while True:
        if cancel_flag and cancel_flag.get('cancel'):
            break
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % nth_frame == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        frame_count += 1
        if progress_callback:
            progress_callback(frame_count, total_frames)

    cap.release()
    return saved_count
