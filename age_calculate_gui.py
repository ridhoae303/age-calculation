import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta

# Class Tanggal untuk menghitung umur
class Tanggal:
    def __init__(self, tahun, bulan, hari):
        self.tanggal = date(tahun, bulan, hari)

    def hitung_umur(self, tanggal_sekarang=None):
        if tanggal_sekarang is None:
            tanggal_sekarang = date.today()

        tahun_awal, bulan_awal, hari_awal = self.tanggal.year, self.tanggal.month, self.tanggal.day
        tahun_akhir, bulan_akhir, hari_akhir = tanggal_sekarang.year, tanggal_sekarang.month, tanggal_sekarang.day

        selisih_tahun = tahun_akhir - tahun_awal
        selisih_bulan = bulan_akhir - bulan_awal
        if selisih_bulan < 0:
            selisih_tahun -= 1
            selisih_bulan += 12

        selisih_hari = hari_akhir - hari_awal
        if selisih_hari < 0:
            bulan_sebelumnya = tanggal_sekarang - timedelta(days=tanggal_sekarang.day)
            jumlah_hari_bulan_lalu = bulan_sebelumnya.day
            selisih_hari += jumlah_hari_bulan_lalu
            selisih_bulan -= 1
            if selisih_bulan < 0:
                selisih_tahun -= 1
                selisih_bulan += 12

        return selisih_tahun, selisih_bulan, selisih_hari


# Fungsi untuk menangani perhitungan umur
def hitung_umur():
    try:
        # Tanggal lahir
        tahun_lahir = int(entry_tahun_lahir.get())
        bulan_lahir = int(entry_bulan_lahir.get())
        hari_lahir = int(entry_hari_lahir.get())
        tanggal_lahir = Tanggal(tahun_lahir, bulan_lahir, hari_lahir)

        # Tanggal sekarang
        if use_real_time_var.get():
            tanggal_sekarang = None
        else:
            tahun_sekarang = int(entry_tahun_sekarang.get())
            bulan_sekarang = int(entry_bulan_sekarang.get())
            hari_sekarang = int(entry_hari_sekarang.get())
            tanggal_sekarang = date(tahun_sekarang, bulan_sekarang, hari_sekarang)

        # Hitung umur
        umur = tanggal_lahir.hitung_umur(tanggal_sekarang)
        label_hasil.config(
            text=f"Usia: {umur[0]} tahun, {umur[1]} bulan, {umur[2]} hari"
        )
    except Exception as e:
        label_hasil.config(text=f"Error: {str(e)}")


# Membuat antarmuka utama
root = tk.Tk()
root.title("Kalkulator Umur")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

# Frame untuk tanggal lahir
frame_lahir = ttk.LabelFrame(root, text="Tanggal Lahir", padding=(10, 10))
frame_lahir.pack(padx=10, pady=10, fill="x")

entry_tahun_lahir = ttk.Entry(frame_lahir, width=10)
entry_tahun_lahir.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_lahir, text="Tahun").grid(row=0, column=0)

entry_bulan_lahir = ttk.Entry(frame_lahir, width=5)
entry_bulan_lahir.grid(row=0, column=3, padx=5, pady=5)
ttk.Label(frame_lahir, text="Bulan").grid(row=0, column=2)

entry_hari_lahir = ttk.Entry(frame_lahir, width=5)
entry_hari_lahir.grid(row=0, column=5, padx=5, pady=5)
ttk.Label(frame_lahir, text="Hari").grid(row=0, column=4)

# Frame untuk tanggal sekarang
frame_sekarang = ttk.LabelFrame(root, text="Tanggal Sekarang", padding=(10, 10))
frame_sekarang.pack(padx=10, pady=10, fill="x")

use_real_time_var = tk.BooleanVar(value=True)
checkbox_realtime = ttk.Checkbutton(
    frame_sekarang,
    text="Gunakan tanggal hari ini",
    variable=use_real_time_var,
    command=lambda: toggle_manual_entry(),
)
checkbox_realtime.grid(row=0, column=0, columnspan=6, sticky="w", padx=5, pady=5)

entry_tahun_sekarang = ttk.Entry(frame_sekarang, width=10, state="disabled")
entry_tahun_sekarang.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_sekarang, text="Tahun").grid(row=1, column=0)

entry_bulan_sekarang = ttk.Entry(frame_sekarang, width=5, state="disabled")
entry_bulan_sekarang.grid(row=1, column=3, padx=5, pady=5)
ttk.Label(frame_sekarang, text="Bulan").grid(row=1, column=2)

entry_hari_sekarang = ttk.Entry(frame_sekarang, width=5, state="disabled")
entry_hari_sekarang.grid(row=1, column=5, padx=5, pady=5)
ttk.Label(frame_sekarang, text="Hari").grid(row=1, column=4)


def toggle_manual_entry():
    state = "disabled" if use_real_time_var.get() else "normal"
    entry_tahun_sekarang.config(state=state)
    entry_bulan_sekarang.config(state=state)
    entry_hari_sekarang.config(state=state)


# Tombol Hitung
btn_hitung = ttk.Button(root, text="Hitung Umur", command=hitung_umur)
btn_hitung.pack(pady=10)

# Label Hasil
label_hasil = ttk.Label(root, text="", font=("Arial", 12), background="#f0f0f0")
label_hasil.pack(pady=10)

# Menjalankan aplikasi
root.mainloop()