import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# --- Koneksi Database ---
try:
    import mysql.connector
except ImportError:
    import sys
    from tkinter import messagebox
    messagebox.showerror(
        "Missing dependency",
        "Module 'mysql.connector' not found.\nInstall it with: pip install mysql-connector-python"
    )
    sys.exit(1)

db = mysql.connector.connect(
    host="db.darsinurse.hint-lab.id",  # atau host="103.106.72.178"
    user="darsinurse",
    password="darsinurse123",
    database="darsinurse",
    port=3306                         # port ditulis di parameter port, bukan di host
)
cursor = db.cursor()

# --- Fungsi Simpan Data ---
def save_data():
    emr = entry_emr.get()
    room = entry_room.get()
    device = entry_device.get()
    
    if not emr or not room or not device:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")
        return
    
    try:
        query = "INSERT INTO room_device (emr_no, room_id, device_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (emr, room, device))
        db.commit()
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        entry_emr.delete(0, tk.END)
        entry_room.delete(0, tk.END)
        entry_device.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Gagal menyimpan data: {err}")

# --- GUI ---
root = tk.Tk()
root.title("Form Assign Device ke Pasien")

tk.Label(root, text="EMR No:").grid(row=0, column=0, padx=10, pady=5)
entry_emr = tk.Entry(root)
entry_emr.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Room ID:").grid(row=1, column=0, padx=10, pady=5)
entry_room = tk.Entry(root)
entry_room.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Device ID:").grid(row=2, column=0, padx=10, pady=5)
entry_device = tk.Entry(root)
entry_device.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Simpan", command=save_data).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
