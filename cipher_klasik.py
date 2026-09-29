# ==========================================================
# APLIKASI CIPHER KLASIK BERBASIS GUI (tkinter)
# Tab 1 : Caesar Cipher            (substitusi abjad-tunggal)
# Tab 2 : Vigenere Cipher          (substitusi abjad-majemuk)
# Tab 3 : Columnar Transposition   (transposisi)
# Jalankan: python gui_cipher.py
# ==========================================================
import tkinter as tk
from tkinter import ttk, messagebox


# ----------------------------------------------------------
# BAGIAN 1: LOGIKA CIPHER (sama seperti versi terminal)
# ----------------------------------------------------------
def bersihkan(teks):
    """Ambil hanya huruf, ubah ke kapital (spasi/angka dibuang)."""
    return "".join(h.upper() for h in teks if h.isalpha())


# ---------- Caesar ----------
def caesar_enkripsi(plainteks, k):
    hasil = ""
    for huruf in plainteks:
        if huruf.isalpha():
            p = ord(huruf.upper()) - ord("A")      # A=0 ... Z=25
            c = (p + k) % 26                       # c = (p + k) mod 26
            hasil += chr(c + ord("A"))
        else:
            hasil += huruf                         # spasi/angka dibiarkan
    return hasil


def caesar_dekripsi(cipherteks, k):
    hasil = ""
    for huruf in cipherteks:
        if huruf.isalpha():
            c = ord(huruf.upper()) - ord("A")
            p = (c - k) % 26                       # p = (c - k) mod 26
            hasil += chr(p + ord("A")).lower()
        else:
            hasil += huruf
    return hasil


def caesar_brute_force(cipherteks):
    baris = []
    for k in range(26):
        baris.append(f"k = {k:2d}  ->  {caesar_dekripsi(cipherteks, k)}")
    return "\n".join(baris)


# ---------- Vigenere ----------
def vigenere_enkripsi(plainteks, kunci):
    plainteks, kunci = bersihkan(plainteks), bersihkan(kunci)
    hasil = ""
    for i in range(len(plainteks)):
        p = ord(plainteks[i]) - ord("A")
        k = ord(kunci[i % len(kunci)]) - ord("A")  # kunci diulang
        hasil += chr((p + k) % 26 + ord("A"))
    return hasil


def vigenere_dekripsi(cipherteks, kunci):
    cipherteks, kunci = bersihkan(cipherteks), bersihkan(kunci)
    hasil = ""
    for i in range(len(cipherteks)):
        c = ord(cipherteks[i]) - ord("A")
        k = ord(kunci[i % len(kunci)]) - ord("A")
        hasil += chr((c - k) % 26 + ord("A"))
    return hasil.lower()


# ---------- Columnar Transposition ----------
def urutan_kolom(kunci):
    """Urutan baca kolom berdasarkan urutan alfabet huruf kunci."""
    return sorted(range(len(kunci)), key=lambda i: (kunci[i], i))


def columnar_enkripsi(plainteks, kunci):
    plainteks = bersihkan(plainteks)
    n = len(kunci)
    while len(plainteks) % n != 0:                 # tambah huruf dummy X
        plainteks += "X"
    baris = [plainteks[i:i + n] for i in range(0, len(plainteks), n)]
    hasil = ""
    for kol in urutan_kolom(kunci):
        for b in baris:
            hasil += b[kol]
    return hasil


def columnar_dekripsi(cipherteks, kunci):
    cipherteks = bersihkan(cipherteks)
    n = len(kunci)
    if len(cipherteks) % n != 0:
        raise ValueError(
            f"Panjang cipherteks ({len(cipherteks)}) harus kelipatan "
            f"jumlah kolom ({n}).")
    jml_baris = len(cipherteks) // n
    kolom, pos = {}, 0
    for kol in urutan_kolom(kunci):
        kolom[kol] = cipherteks[pos:pos + jml_baris]
        pos += jml_baris
    hasil = ""
    for r in range(jml_baris):
        for kol in range(n):
            hasil += kolom[kol][r]
    return hasil.lower()


# ---------- Validasi kunci ----------
def kunci_caesar(teks):
    try:
        return int(teks.strip())
    except ValueError:
        raise ValueError("Kunci Caesar harus berupa angka bulat (0-25).")


def kunci_vigenere(teks):
    k = bersihkan(teks)
    if not k:
        raise ValueError("Kunci Vigenere harus berisi huruf (misal: LAMPION).")
    return k


def kunci_columnar(teks):
    teks = teks.strip()
    if teks.isdigit():
        n = int(teks)
        if n < 2:
            raise ValueError("Jumlah kolom minimal 2.")
        return "A" * n                             # huruf sama -> urut kiri-kanan
    k = bersihkan(teks)
    if len(k) < 2:
        raise ValueError("Kunci berupa angka (misal 6) atau kata "
                         "minimal 2 huruf (misal TOMBAK).")
    return k


# ----------------------------------------------------------
# BAGIAN 2: TAMPILAN GUI
# ----------------------------------------------------------
WARNA_HEADER = "#1f2a44"
WARNA_AKSEN = "#3b82f6"
WARNA_BG = "#f3f4f6"


class CipherTab(ttk.Frame):
    """Satu tab cipher: input, kunci, tombol, dan output."""

    def __init__(self, master, judul, deskripsi, label_kunci, contoh_kunci,
                 fungsi_kunci, fungsi_enkripsi, fungsi_dekripsi,
                 fungsi_brute=None):
        super().__init__(master, padding=14)
        self.fungsi_kunci = fungsi_kunci
        self.fungsi_enkripsi = fungsi_enkripsi
        self.fungsi_dekripsi = fungsi_dekripsi
        self.fungsi_brute = fungsi_brute

        ttk.Label(self, text=judul, style="Judul.TLabel").pack(anchor="w")
        ttk.Label(self, text=deskripsi, style="Info.TLabel",
                  wraplength=680, justify="left").pack(anchor="w", pady=(2, 10))

        # Input teks
        ttk.Label(self, text="Teks masukan (plainteks / cipherteks):").pack(anchor="w")
        self.input_teks = tk.Text(self, height=5, font=("Consolas", 11),
                                  wrap="word", relief="solid", borderwidth=1)
        self.input_teks.pack(fill="x", pady=(2, 10))

        # Kunci
        baris_kunci = ttk.Frame(self)
        baris_kunci.pack(fill="x", pady=(0, 10))
        ttk.Label(baris_kunci, text=label_kunci).pack(side="left")
        self.input_kunci = ttk.Entry(baris_kunci, width=22, font=("Consolas", 11))
        self.input_kunci.pack(side="left", padx=8)
        ttk.Label(baris_kunci, text=f"contoh: {contoh_kunci}",
                  style="Info.TLabel").pack(side="left")

        # Tombol
        baris_tombol = ttk.Frame(self)
        baris_tombol.pack(fill="x", pady=(0, 10))
        ttk.Button(baris_tombol, text="🔒 Enkripsi", style="Aksen.TButton",
                   command=self.enkripsi).pack(side="left", padx=(0, 6))
        ttk.Button(baris_tombol, text="🔓 Dekripsi", style="Aksen.TButton",
                   command=self.dekripsi).pack(side="left", padx=6)
        if fungsi_brute:
            ttk.Button(baris_tombol, text="🔍 Brute Force",
                       command=self.brute).pack(side="left", padx=6)
        ttk.Button(baris_tombol, text="📋 Salin Hasil",
                   command=self.salin).pack(side="left", padx=6)
        ttk.Button(baris_tombol, text="🗑 Bersihkan",
                   command=self.bersihkan_semua).pack(side="left", padx=6)

        # Output
        ttk.Label(self, text="Hasil:").pack(anchor="w")
        self.output = tk.Text(self, height=12, font=("Consolas", 11),
                              wrap="word", relief="solid", borderwidth=1,
                              bg="#eef2ff", state="disabled")
        self.output.pack(fill="both", expand=True, pady=(2, 0))

    # --- helper ---
    def _ambil_input(self):
        teks = self.input_teks.get("1.0", "end").strip()
        if not teks:
            raise ValueError("Teks masukan tidak boleh kosong.")
        return teks

    def _tulis_output(self, hasil):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", hasil)
        self.output.config(state="disabled")

    def _jalankan(self, aksi):
        try:
            self._tulis_output(aksi())
        except ValueError as e:
            messagebox.showerror("Input tidak valid", str(e))

    # --- aksi tombol ---
    def enkripsi(self):
        self._jalankan(lambda: self.fungsi_enkripsi(
            self._ambil_input(), self.fungsi_kunci(self.input_kunci.get())))

    def dekripsi(self):
        self._jalankan(lambda: self.fungsi_dekripsi(
            self._ambil_input(), self.fungsi_kunci(self.input_kunci.get())))

    def brute(self):
        self._jalankan(lambda: self.fungsi_brute(self._ambil_input()))

    def salin(self):
        hasil = self.output.get("1.0", "end").strip()
        if hasil:
            self.clipboard_clear()
            self.clipboard_append(hasil)
            messagebox.showinfo("Tersalin", "Hasil sudah disalin ke clipboard.")

    def bersihkan_semua(self):
        self.input_teks.delete("1.0", "end")
        self.input_kunci.delete(0, "end")
        self._tulis_output("")


class Aplikasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Cipher Klasik - IF4020 Kriptografi")
        self.geometry("780x680")
        self.minsize(720, 620)
        self.configure(bg=WARNA_BG)
        self._atur_gaya()

        header = tk.Frame(self, bg=WARNA_HEADER)
        header.pack(fill="x")
        tk.Label(header, text="🔐 Aplikasi Cipher Klasik", bg=WARNA_HEADER,
                 fg="white", font=("Segoe UI", 18, "bold")
                 ).pack(anchor="w", padx=18, pady=(12, 0))
        tk.Label(header, text="Caesar  •  Vigenère  •  Columnar Transposition",
                 bg=WARNA_HEADER, fg="#cbd5e1", font=("Segoe UI", 10)
                 ).pack(anchor="w", padx=18, pady=(0, 12))

        tab = ttk.Notebook(self)
        tab.pack(fill="both", expand=True, padx=10, pady=10)

        tab.add(CipherTab(
            tab, "Caesar Cipher (Substitusi Abjad-Tunggal)",
            "Setiap huruf digeser sejauh k. Enkripsi: c = (p + k) mod 26, "
            "dekripsi: p = (c - k) mod 26. Brute Force mencoba semua kunci 0-25 "
            "untuk memecahkan cipherteks tanpa kunci.",
            "Kunci k (0-25):", "3",
            kunci_caesar, caesar_enkripsi, caesar_dekripsi, caesar_brute_force),
            text="  Caesar  ")

        tab.add(CipherTab(
            tab, "Vigenère Cipher (Substitusi Abjad-Majemuk)",
            "Kunci berupa kata yang diulang sepanjang pesan, sehingga tiap huruf "
            "memakai pergeseran berbeda. Spasi dibuang dan hasil berupa huruf kapital.",
            "Kata kunci:", "LAMPION",
            kunci_vigenere, vigenere_enkripsi, vigenere_dekripsi),
            text="  Vigenère  ")

        tab.add(CipherTab(
            tab, "Columnar Transposition Cipher (Transposisi)",
            "Pesan ditulis per baris sebanyak n kolom lalu dibaca per kolom. "
            "Kunci bisa angka (jumlah kolom, mis. 6) atau kata (mis. TOMBAK) "
            "yang menentukan urutan pembacaan kolom. Kekurangan huruf diisi 'X'.",
            "Kunci (angka/kata):", "6  atau  TOMBAK",
            kunci_columnar, columnar_enkripsi, columnar_dekripsi),
            text="  Columnar  ")

    def _atur_gaya(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame", background=WARNA_BG)
        s.configure("TLabel", background=WARNA_BG, font=("Segoe UI", 10))
        s.configure("Judul.TLabel", font=("Segoe UI", 14, "bold"),
                    foreground=WARNA_HEADER)
        s.configure("Info.TLabel", foreground="#6b7280")
        s.configure("TButton", font=("Segoe UI", 10), padding=6)
        s.configure("Aksen.TButton", background=WARNA_AKSEN,
                    foreground="white", font=("Segoe UI", 10, "bold"))
        s.map("Aksen.TButton", background=[("active", "#2563eb")])
        s.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(10, 6))


if __name__ == "__main__":
    Aplikasi().mainloop()