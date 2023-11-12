import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

# Fungsi untuk memotong video menjadi durasi 14 detik
def trim_video(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    trimmed_clip = video_clip.subclip(0, 14)  # Memotong video menjadi 14 detik dari awal
    trimmed_clip.write_videofile(output_file)
    video_clip.reader.close()
    video_clip.audio.reader.close_proc()

# Fungsi untuk memilih direktori dengan file video
def choose_directory():
    directory_path = filedialog.askdirectory(title="Pilih direktori dengan video")
    if directory_path:
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".mp4"):
                input_file = os.path.join(directory_path, file_name)
                output_file = os.path.join(directory_path, f"A_{file_name}")
                trim_video(input_file, output_file)
        message_label.config(text="Trim video selesai.")

# Membuat GUI
root = tk.Tk()
root.title("Aplikasi Trim Video Massal")

choose_directory_button = tk.Button(root, text="Pilih Direktori", command=choose_directory)
choose_directory_button.pack(pady=20)

message_label = tk.Label(root, text="", font=("Helvetica", 12))
message_label.pack()

root.mainloop()
