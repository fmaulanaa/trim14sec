# trim14sec — Pemotong Video MP4 Massal

Aplikasi Python berbasis Tkinter untuk memotong video MP4 dari awal sampai maksimal 14 detik. Pilih satu folder, lalu hasil disimpan di folder yang sama dengan awalan nama `A_`.

## Fitur

- Memilih folder video melalui dialog.
- Memproses ekstensi `.mp4` tanpa membedakan huruf besar/kecil.
- Memotong video mulai detik 0 hingga maksimal detik ke-14.
- Menjaga durasi asli video yang lebih pendek dari 14 detik.
- Menyimpan hasil sebagai `A_namafile.mp4`.
- Melanjutkan batch jika satu file gagal, lalu menampilkan ringkasan kegagalan.
- Menutup resource video setelah pemrosesan.

## Persyaratan dan instalasi

- Python 3
- Tkinter
- MoviePy dan dukungan FFmpeg yang diperlukan MoviePy

Pasang MoviePy:

```bash
python -m pip install moviepy
```

## Menjalankan

```bash
python 14detik.py
```

Tekan **Pilih Direktori**, pilih folder berisi video, lalu tunggu sampai ringkasan hasil ditampilkan. Waktu pemrosesan tergantung jumlah file, resolusi, codec, dan kemampuan komputer.

## Cara kerja

1. `choose_directory()` meminta pengguna memilih folder.
2. Daftar MP4 dikumpulkan sebelum pemrosesan dimulai.
3. File yang sudah memiliki awalan `A_` dilewati agar hasil lama tidak diproses sebagai input lagi.
4. `trim_video()` membuka video dengan `VideoFileClip`.
5. Durasi potongan dihitung sebagai nilai terkecil antara 14 detik dan durasi video sumber.
6. Program menggunakan `subclipped()` bila tersedia (MoviePy 2.x), atau `subclip()` untuk versi lama.
7. Video hasil ditulis dan kedua clip ditutup di blok `finally`.
8. Kegagalan per file dicatat sehingga file lain tetap dapat diproses.

## Pengujian yang disarankan

- Video lebih panjang dari 14 detik: hasil berdurasi 14 detik.
- Video lebih pendek dari 14 detik: hasil mempertahankan durasi sumber.
- Folder tanpa MP4: tampil pesan bahwa tidak ada file yang diproses.
- Video rusak di antara video valid: file lain tetap diproses dan kegagalan ditampilkan.
- Uji codec yang digunakan pada komputer target.

## Batasan

Pemrosesan video berlangsung sinkron sehingga antarmuka dapat tampak tidak responsif ketika encoding file besar. Hasil encoding mengikuti pengaturan bawaan MoviePy/FFmpeg. Pengujian dengan video nyata tetap diperlukan.

## Catatan audit

Penambahan komentar rinci berbahasa Indonesia disertai perbaikan kompatibilitas API MoviePy, penanganan video pendek, penutupan resource, pelaporan error per file, dan pengecualian file keluaran berawalan `A_`.
