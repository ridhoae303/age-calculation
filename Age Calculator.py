# Enchanted by ridhoae303
# I was just bored, so I tweaked this script to make it more interesting.

import tkinter as tk
from tkinter import ttk
from datetime import date
import calendar
import urllib.request


class Tanggal:
    def __init__(self, tahun, bulan, hari):
        self.date = date(tahun, bulan, hari)

    def hitung_umur(self, referensi=None):
        if referensi is None:
            referensi = date.today()
        if referensi < self.date:
            raise ValueError("Tanggal referensi gak boleh lebih awal dari tanggal lahir bjir")

        tahun = referensi.year - self.date.year
        bulan = referensi.month - self.date.month
        hari = referensi.day - self.date.day

        if hari < 0:
            bulan_sebelum = referensi.month - 1 if referensi.month > 1 else 12
            tahun_sebelum = referensi.year if referensi.month > 1 else referensi.year - 1
            _, jumlah_hari = calendar.monthrange(tahun_sebelum, bulan_sebelum)
            hari += jumlah_hari
            bulan -= 1

        if bulan < 0:
            tahun -= 1
            bulan += 12

        return tahun, bulan, hari


def perbarui_hari_max(*args):
    try:
        y = int(var_tahun_lahir.get())
        m = int(var_bulan_lahir.get())
        _, maks = calendar.monthrange(y, m)
        spin_hari_lahir.config(to=maks)
        sekarang = int(var_hari_lahir.get())
        if sekarang > maks:
            var_hari_lahir.set(maks)
    except (ValueError, tk.TclError):
        pass


def isi_tanggal_sekarang():
    if var_realtime.get():
        today = date.today()
        var_tahun_sekarang.set(str(today.year))
        var_bulan_sekarang.set(str(today.month))
        var_hari_sekarang.set(str(today.day))
    else:
        var_tahun_sekarang.set("")
        var_bulan_sekarang.set("")
        var_hari_sekarang.set("")


def toggle_manual():
    mode = "disabled" if var_realtime.get() else "normal"
    spin_tahun_sekarang.config(state=mode)
    spin_bulan_sekarang.config(state=mode)
    spin_hari_sekarang.config(state=mode)
    isi_tanggal_sekarang()


def kirim_ke_server(tahun, bulan, hari):
    url = "https://httpbin.org/post" # If you have an endpoint, replace it with your API endpoint
    data = f"umur={tahun}&bulan={bulan}&hari={hari}".encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def hitung_umur():
    try:
        yb = int(var_tahun_lahir.get())
        mb = int(var_bulan_lahir.get())
        db = int(var_hari_lahir.get())
        lahir = Tanggal(yb, mb, db)

        if var_realtime.get():
            referensi = None
        else:
            yn = int(var_tahun_sekarang.get())
            mn = int(var_bulan_sekarang.get())
            dn = int(var_hari_sekarang.get())
            referensi = date(yn, mn, dn)

        th, bl, hr = lahir.hitung_umur(referensi)
        var_hasil.set(f"Usia: {th} tahun, {bl} bulan, {hr} hari")

        if var_kirim_server.get():
            if kirim_ke_server(th, bl, hr):
                var_status_server.set("Status: Data terkirim ke server")
            else:
                var_status_server.set("Status: Gagal mengirim data")
        else:
            var_status_server.set("")

    except (ValueError, tk.TclError):
        var_hasil.set("Ini apaan anjay, tanggal gak valid lah!")
        var_status_server.set("")


def bersihkan():
    var_tahun_lahir.set("")
    var_bulan_lahir.set("")
    var_hari_lahir.set("")
    isi_tanggal_sekarang()
    var_hasil.set("")
    var_status_server.set("")


root = tk.Tk()
root.title("Kalkulator Umur")
root.geometry("420x480")
root.configure(bg="#e1e5ea")

gaya = ttk.Style()
gaya.theme_use("clam")
gaya.configure("TLabel", background="#e1e5ea", font=("Segoe UI", 9))
gaya.configure("TLabelframe", background="#e1e5ea", font=("Segoe UI", 10, "bold"))
gaya.configure("TLabelframe.Label", background="#e1e5ea")
gaya.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
gaya.configure("TCheckbutton", background="#e1e5ea")

var_tahun_lahir = tk.StringVar()
var_bulan_lahir = tk.StringVar()
var_hari_lahir = tk.StringVar()

var_realtime = tk.BooleanVar(value=True)
var_kirim_server = tk.BooleanVar(value=False)

var_tahun_sekarang = tk.StringVar()
var_bulan_sekarang = tk.StringVar()
var_hari_sekarang = tk.StringVar()

var_hasil = tk.StringVar()
var_status_server = tk.StringVar()

var_tahun_lahir.trace_add("write", perbarui_hari_max)
var_bulan_lahir.trace_add("write", perbarui_hari_max)

frame_lahir = ttk.LabelFrame(root, text="Tanggal Lahir", padding=(15, 10))
frame_lahir.pack(padx=15, pady=10, fill="x")

ttk.Label(frame_lahir, text="Tahun").grid(row=0, column=0, sticky="w")
spin_tahun_lahir = ttk.Spinbox(frame_lahir, from_=1900, to=2100, textvariable=var_tahun_lahir, width=7)
spin_tahun_lahir.grid(row=0, column=1, padx=5, pady=4)

ttk.Label(frame_lahir, text="Bulan").grid(row=0, column=2, sticky="w")
spin_bulan_lahir = ttk.Spinbox(frame_lahir, from_=1, to=12, textvariable=var_bulan_lahir, width=5)
spin_bulan_lahir.grid(row=0, column=3, padx=5, pady=4)

ttk.Label(frame_lahir, text="Hari").grid(row=0, column=4, sticky="w")
spin_hari_lahir = ttk.Spinbox(frame_lahir, from_=1, to=31, textvariable=var_hari_lahir, width=5)
spin_hari_lahir.grid(row=0, column=5, padx=5, pady=4)

frame_sekarang = ttk.LabelFrame(root, text="Tanggal Sekarang", padding=(15, 10))
frame_sekarang.pack(padx=15, pady=10, fill="x")

cek_realtime = ttk.Checkbutton(frame_sekarang, text="Gunakan tanggal hari ini",
                               variable=var_realtime, command=toggle_manual)
cek_realtime.grid(row=0, column=0, columnspan=6, sticky="w", padx=5, pady=5)

ttk.Label(frame_sekarang, text="Tahun").grid(row=1, column=0, sticky="w")
spin_tahun_sekarang = ttk.Spinbox(frame_sekarang, from_=1900, to=2100, textvariable=var_tahun_sekarang,
                                  width=7, state="disabled")
spin_tahun_sekarang.grid(row=1, column=1, padx=5, pady=4)

ttk.Label(frame_sekarang, text="Bulan").grid(row=1, column=2, sticky="w")
spin_bulan_sekarang = ttk.Spinbox(frame_sekarang, from_=1, to=12, textvariable=var_bulan_sekarang,
                                  width=5, state="disabled")
spin_bulan_sekarang.grid(row=1, column=3, padx=5, pady=4)

ttk.Label(frame_sekarang, text="Hari").grid(row=1, column=4, sticky="w")
spin_hari_sekarang = ttk.Spinbox(frame_sekarang, from_=1, to=31, textvariable=var_hari_sekarang,
                                 width=5, state="disabled")
spin_hari_sekarang.grid(row=1, column=5, padx=5, pady=4)

cek_kirim = ttk.Checkbutton(root, text="Kirim hasil ke server", variable=var_kirim_server)
cek_kirim.pack(pady=(5, 0))

frame_tombol = ttk.Frame(root)
frame_tombol.pack(pady=10)

ttk.Button(frame_tombol, text="Hitung Umur", command=hitung_umur).pack(side="left", padx=5)
ttk.Button(frame_tombol, text="Clear", command=bersihkan).pack(side="left", padx=5)

lbl_hasil = ttk.Label(root, textvariable=var_hasil, font=("Segoe UI", 12, "bold"),
                      background="#e1e5ea", anchor="center")
lbl_hasil.pack(pady=5, fill="x", padx=20)

lbl_status = ttk.Label(root, textvariable=var_status_server, font=("Segoe UI", 9),
                       background="#e1e5ea", anchor="center")
lbl_status.pack(pady=5, fill="x", padx=20)

isi_tanggal_sekarang()
perbarui_hari_max()
root.mainloop()
