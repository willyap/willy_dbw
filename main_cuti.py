import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *

root = Tk()
root.title('FORM PENGAJUAN CUTI')
root.geometry("1300x500")

#fungsi untuk action klik data
def getValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    row_id = listbox.selection()[0]
    select = listbox.set(row_id)
    e1.insert(0, select['nama'])
    e2.insert(0, select['nik'])
    e3.insert(0, select['tanggal_cuti'])
    e4.insert(0, select['jumlah_hari'])
    e5.insert(0, select['keterangan'])

#setting konfigurasi database pada setiap fungsi add(), approve(), reject(), delete() dan show()
#fungsi menambahkan cuti
def add():
    nama = e1.get()  
    nik = e2.get()
    tanggal_cuti = e3.get()
    jumlah_hari = e4.get()
    keterangan = e5.get()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db_cuti")
    mycursor = db.cursor()

    try:
        sql = "INSERT INTO karyawan (nama, nik, tanggal_cuti, jumlah_hari, keterangan) VALUES (%s, %s, %s, %s, %s)"
        val = (nama, nik, tanggal_cuti, jumlah_hari, keterangan)
        mycursor.execute(sql, val)
        db.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("sukses","Permohonan cuti sudah berhasil dimasukkan \n\nMohon jalankan ulang program")
        root.destroy()
    except Exception as e:
        print (e)
        db.rollback()
        db.close()

#fungsi menyetujui pengajuan cuti
def approve():
    nik = e2.get()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db_cuti")
    mycursor = db.cursor()
    try:
        sql = "UPDATE karyawan SET status = %s WHERE nik = %s"
        val = ("disetujui", nik)
        mycursor.execute(sql, val)
        db.commit()
        messagebox.showinfo("Sukses","Permohonan cuti sudah disetujui \n\nMohon jalankan ulang program")
        root.destroy()
    except Exception as e:
        print (e)
        db.rollback()
        db.close()

#fungsi menolak pengajuan cuti
def reject():
    nik = e2.get()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db_cuti")
    mycursor = db.cursor()
    try:
        sql = "UPDATE karyawan SET status = %s WHERE nik = %s"
        val = ("ditolak", nik)
        mycursor.execute(sql, val)
        db.commit()
        messagebox.showinfo("Menolak","Menolak permohonan cuti \n\nMohon jalankan ulang program")
        root.destroy()
    except Exception as e:
        print (e)
        db.rollback()
        db.close()

#fungsi menghapus data permohonan cuti
def delete():
    nik = e2.get()
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db_cuti")
    mycursor = db.cursor()
    messagebox.askquestion("konfirmasi hapus", "Apakah Anda yakin?")
    try:
        sql = "DELETE FROM karyawan WHERE nik = %s"
        val = (nik,)
        mycursor.execute(sql, val)
        db.commit()
        messagebox.showwarning("terhapus","data berhasil dihapus \n\nMohon jalankan ulang program")
        root.destroy()
    except Exception as e:
        print (e)
        db.rollback()
        db.close()

#fungsi menampilkan data pemohon cuti
def show():
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db_cuti")
    mycursor = db.cursor()
    mycursor.execute("SELECT nama, nik, tanggal_cuti, jumlah_hari, keterangan, status FROM karyawan")
    tampil = mycursor.fetchall()
    print(tampil)

    for i, (id, nama, nik, tanggal_cuti, jumlah_hari, keterangan) in enumerate (tampil, start=1):
        listbox.insert("", "end", values=(id, nama, nik, tanggal_cuti, jumlah_hari, keterangan))
        db.close()

#deklarasi variabel untuk input data
global e1
global e2
global e3
global e4
global e5


#INFORMASI TENTANG APLIKASI
tk.Label(root, text="Form Cuti Pegawai", fg="black", font=(None,30)).place(x=530, y=5)
tk.Label(root, text="silahkan isi form untuk mengajukan cuti anda", fg="black", font=(None,15)).place(x=500, y=70)

#Membuat form pengajuan cuti
Label(root, text="Nama Pegawai").place(x=10, y=10)
Label(root, text="Silahkan masukkan nama anda", font=(None,8)).place(x=270, y=10)
Label(root, text="NIK").place(x=10, y=40)
Label(root, text="Silahkan masukkan NIK anda (6 digit)", font=(None,8)).place(x=270, y=40)
Label(root, text="Tanggal Cuti").place(x=10, y=70)
Label(root, text="Silahkan masukkan tanggal mulai cuti", font=(None,8)).place(x=270, y=70)
Label(root, text="(thn - bln - tgl)                         contoh: 2021-04-21", font=(None,8)).place(x=10, y=90)
Label(root, text="Jumlah Hari").place(x=10, y=120)
Label(root, text="Silahkan masukkan jumlah hari cuti", font=(None,8)).place(x=270, y=120)
Label(root, text="Keterangan").place(x=10, y=150)
Label(root, text="Silahkan isi alasan anda mengambil cuti", font=(None,8)).place(x=270, y=150)

#kolom pengisian data
e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)

e3 = Entry(root)
e3.place(x=140, y=70)

e4 = Entry(root)
e4.place(x=140, y=120)

e5 = Entry(root)
e5.place(x=140, y=150)

#catatan kaki dan tombol untuk submit fungsi tambah, approve, tolak, dan hapus data
Label(root, text="*diisi oleh pegawai").place(x=270,y=190)
Button(root, text="tambah cuti", command = add, height=3, width=13, bg = '#03c2fc').place(x=160,y=190)
Label(root, text="*diisi oleh atasan").place(x=790,y=190)
Label(root, text="klik 2x pada data yang ingin dipilih, lalu tekan tombol dibawah").place(x=880,y=170)
Button(root, text="Approve", command = approve, height=3, width=13, bg = '#17fa0f').place(x=890,y=190)
Button(root, text="Tolak", command = reject, height=3, width=13, bg = "yellow").place(x=1000,y=190)
Button(root, text="Hapus", command = delete, height=3, width=13, bg = 'red').place(x=1110,y=190)

#deklarasi tabel untuk menampilkan data pemohon cuti
cols = ('nama', 'nik', 'tanggal_cuti', 'jumlah_hari', 'keterangan','status')
listbox = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    listbox.heading(col, text=col)
    listbox.grid(row=1, column=0, columnspan=2)
    listbox.place(x=10, y=260)
show()
listbox.bind('<Double-Button-1>', getValue)


root.mainloop()
