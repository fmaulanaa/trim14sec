"""Aplikasi GUI untuk memotong video MP4 massal menjadi maksimal 14 detik."""
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from moviepy.video.io.VideoFileClip import VideoFileClip

DURASI_MAKSIMAL_DETIK = 14
AWALAN_FILE_KELUARAN = "A_"


def trim_video(input_file, output_file):
    """Potong satu video dari awal sampai maksimal 14 detik.

    Resource video ditutup pada blok finally, termasuk ketika proses encoding
    gagal. Exception diteruskan ke pemanggil agar kegagalan satu file dapat
    dicatat tanpa menghentikan pemrosesan file lainnya.
    """
    video_clip = None
    trimmed_clip = None
    try:
        # VideoFileClip membuka file dan resource pembaca audio/video.
        video_clip = VideoFileClip(input_file)

        # Video yang lebih pendek dari 14 detik tidak boleh dipotong melewati
        # akhir durasi aslinya.
        end_time = min(DURASI_MAKSIMAL_DETIK, video_clip.duration)

        # MoviePy 2.x menggunakan subclipped(); MoviePy 1.x menggunakan
        # subclip(). Pilih API yang tersedia agar kompatibel lintas versi.
        if hasattr(video_clip, "subclipped"):
            trimmed_clip = video_clip.subclipped(0, end_time)
        else:
            trimmed_clip = video_clip.subclip(0, end_time)

        # Tulis video hasil ke path yang diberikan oleh fungsi pemanggil.
        trimmed_clip.write_videofile(output_file)
    finally:
        # Tutup hasil terlebih dahulu lalu sumber; cek None bila pembukaan
        # atau proses pemotongan gagal sebelum clip berhasil dibuat.
        if trimmed_clip is not None:
            trimmed_clip.close()
        if video_clip is not None:
            video_clip.close()


def choose_directory():
    """Pilih folder dan proses file MP4 di dalamnya satu per satu."""
    directory_path = filedialog.askdirectory(
        title="Pilih direktori dengan video"
    )
    if not directory_path:
        # Dialog dibatalkan; tidak ada pekerjaan yang perlu dilakukan.
        return

    # Ambil snapshot daftar file sebelum membuat output. File keluaran yang
    # sudah ada tidak diproses ulang sebagai input.
    video_files = [
        name for name in os.listdir(directory_path)
        if name.lower().endswith(".mp4")
        and not name.startswith(AWALAN_FILE_KELUARAN)
    ]

    if not video_files:
        message_label.config(text="Tidak ditemukan file MP4 untuk diproses.")
        return

    berhasil = 0
    gagal = []

    # Error ditangani per file agar satu video rusak tidak menghentikan batch.
    for index, file_name in enumerate(video_files, start=1):
        input_file = os.path.join(directory_path, file_name)
        output_file = os.path.join(
            directory_path, f"{AWALAN_FILE_KELUARAN}{file_name}"
        )
        message_label.config(
            text=f"Memproses {index}/{len(video_files)}: {file_name}"
        )
        root.update_idletasks()

        try:
            trim_video(input_file, output_file)
            berhasil += 1
        except Exception as error:
            # Tampilkan nama file dan penyebab yang dilaporkan oleh MoviePy.
            gagal.append(f"{file_name}: {error}")

    ringkasan = f"Selesai. Berhasil: {berhasil}. Gagal: {len(gagal)}."
    message_label.config(text=ringkasan)

    if gagal:
        rincian = "\n".join(f"- {item}" for item in gagal[:10])
        if len(gagal) > 10:
            rincian += f"\n- ... dan {len(gagal) - 10} file lainnya."
        messagebox.showwarning(
            "Pemrosesan selesai dengan kesalahan",
            f"{ringkasan}\n\nRincian kegagalan:\n{rincian}",
            parent=root
        )
    else:
        messagebox.showinfo("Selesai", ringkasan, parent=root)


# Buat antarmuka di bagian akhir agar logika pemrosesan video mudah dibaca.
root = tk.Tk()
root.title("Aplikasi Trim Video Massal")
choose_directory_button = tk.Button(
    root, text="Pilih Direktori", command=choose_directory
)
choose_directory_button.pack(pady=20)
message_label = tk.Label(root, text="", font=("Helvetica", 12))
message_label.pack(padx=12, pady=8)

if __name__ == "__main__":
    root.mainloop()
