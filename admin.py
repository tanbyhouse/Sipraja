from tabulate import tabulate
from connectdb import get_connection
import textwrap

def bungkus_teks(teks, lebar):
    return "\n".join(textwrap.wrap(teks, width=lebar))

def daftar_pesanan():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Daftar Pesanan Masuk ===")
    query = """
        SELECT p.id_penyewaan, c.nama_customer, c.no_telepon_customer, c.alamat, p.tanggal_pemesanan, p.tanggal_mulai_sewa, p.tanggal_selesai_sewa,
        p.total_harga, sp.status_penyewaan, a.nama_alat_berat
        FROM penyewaan p
        JOIN customer c ON p.id_customer = c.id_customer
        JOIN status_penyewaan sp ON p.id_status_penyewaan = sp.id_status_penyewaan
        JOIN detail_penyewaan dp ON p.id_penyewaan = dp.id_penyewaan
        JOIN alat_berat a ON dp.id_alat_berat = a.id_alat_berat
        ORDER BY p.tanggal_pemesanan DESC
    """
    cur.execute(query)
    results = cur.fetchall()
    
    if results:
        tampilkan_pesanan(results)
        id_pilih = input("\nMasukkan ID penyewaan yang ingin diproses (atau tekan Enter untuk kembali): ")
        if id_pilih:
            print("1.Menunggu\n2.Diterima\n3.Ditolak\n4.Selesai")
            pilihan = input("Pilih status baru (1-4): ")
            status_mapping = {
                "1": "Menunggu",
                "2": "Diterima",
                "3": "Ditolak",
                "4": "Selesai"
            }
            if pilihan in status_mapping:
                new_status = status_mapping[pilihan]
                
                cur.execute("""
                    UPDATE penyewaan
                    SET id_status_penyewaan = (SELECT id_status_penyewaan
                        FROM status_penyewaan
                        WHERE status_penyewaan = %s
                    )
                    WHERE id_penyewaan = %s
                """, (new_status, id_pilih))

                conn.commit()
                print(f"Status penyewaan dengan ID {id_pilih} berhasil diubah menjadi '{new_status}'.")
            else:
                print("Pilihan status tidak valid.")
        else:
            print("Tidak ada ID penyewaan yang dipilih.")
    else:
        print("Tidak ada pesanan yang masuk.")
    
    conn.close()
    

def tampilkan_pesanan(results):
    headers = [
        "ID","Nama", "No Telepon", "Alamat",
        "Tgl Pemesanan", "Tgl Sewa", "Tgl Selesai Sewa", "Total",
        "Status", "Alat Berat"
    ]
    
    formatted_results = []
    for row in results:
        formatted_row = list(row)
        formatted_row[9] = bungkus_teks(formatted_row[9], 15)
        formatted_row[3] = bungkus_teks(formatted_row[3], 15)
        formatted_row[7] = f"Rp {int(formatted_row[7]):,}".replace(",", ".") 
        formatted_results.append(formatted_row)

    print(tabulate(formatted_results, headers=headers, tablefmt="fancy_grid", stralign="center",numalign="center"))

def daftar_alat_berat():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Daftar Alat Berat ===")
    query = """
        SELECT a.id_alat_berat, a.nama_alat_berat, a.harga_sewa_per_hari, a.jumlah, 
        o.nama_operator,sk.status_ketersediaan
        FROM alat_berat a
        JOIN operator o ON a.id_operator = o.id_operator
        JOIN status_ketersediaan sk ON a.id_status_ketersediaan = sk.id_status_ketersediaan
        """
    cur.execute(query)
    results = cur.fetchall()
    
    if results:
        tampilkan_alat(results)
    else:
        print("Tidak ada pesanan yang masuk.")
    conn.close()
    
def tampilkan_alat(results):
    headers = [
        "ID","Nama", "Harga Sewa/hari", "Jumlah",
        "Operator", "Status"
    ]
    
    formatted_results = []
    for row in results:
        formatted_row = list(row)
        formatted_row[2] = f"Rp {int(float(formatted_row[2])):,}".replace(",", ".")
        formatted_results.append(formatted_row)

    print(tabulate(formatted_results, headers=headers, tablefmt="fancy_grid", stralign="center",numalign="center"))

def lihat_histori():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Histori Pesanan ===")
    query = """
        SELECT t.tanggal_pembayaran, c.nama_customer, t.jumlah_pembayaran, pg.tanggal_pengembalian,
            a.nama_alat_berat, sp.status_penyewaan, sb.status
        FROM transaksi t
        JOIN penyewaan p ON t.id_penyewaan = p.id_penyewaan
        JOIN pengembalian_alat pg ON p.id_penyewaan = pg.id_penyewaan
        JOIN status_pembayaran sb ON t.id_status_pembayaran = sb.id_status_pembayaran
        JOIN customer c ON t.id_customer = c.id_customer
        JOIN status_penyewaan sp ON p.id_status_penyewaan = sp.id_status_penyewaan
        JOIN detail_penyewaan dp ON p.id_penyewaan = dp.id_penyewaan
        JOIN alat_berat a ON dp.id_alat_berat = a.id_alat_berat
        GROUP BY 
            t.tanggal_pembayaran, c.nama_customer, t.jumlah_pembayaran,
            pg.tanggal_pengembalian, a.nama_alat_berat, sp.status_penyewaan, sb.status
        ORDER BY t.tanggal_pembayaran DESC
    """
    cur.execute(query)
    results = cur.fetchall()
    
    if results:
        tampilkan_histori(results)
    else:
        print("Tidak ada histori pesanan.")
    input("Tekan Enter untuk kembali ke menu...")
    conn.close()
    
def tampilkan_histori(results):
    headers = [
        "Tgl Pembayaran", "Nama", "Total",
        "Tgl Pengembalian", "Alat", "Status Sewa", "Status Pembayaran"
    ]
    
    formatted_results = []
    for row in results:
        formatted_row = list(row)
        formatted_row[2] = f"Rp {int(float(formatted_row[2])):,}".replace(",", ".")
        formatted_results.append(formatted_row)

    print(tabulate(formatted_results, headers=headers, tablefmt="fancy_grid", stralign="center",numalign="center"))
    
def tambah_alat():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Tambah Alat Berat ===")
    nama_alat = input("Nama Alat Berat: ")
    harga_sewa = float(input("Harga Sewa per Hari (Rp): "))
    jumlah = int(input("Jumlah Alat: "))
    deskripsi = input("Deskripsi Alat Berat: ")
    id_operator = input("ID Operator: ")
    id_status_ketersediaan = input("ID Status Ketersediaan: ")
    id_jenis_alat = input("ID Jenis Alat: ")

    query = """
        INSERT INTO alat_berat (
            nama_alat_berat, harga_sewa_per_hari, jumlah,
            deskripsi_alat_berat, id_operator, id_status_ketersediaan, id_jenis_alat
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    cur.execute(query, (
        nama_alat, harga_sewa, jumlah, deskripsi,
        id_operator, id_status_ketersediaan, id_jenis_alat
    ))
    conn.commit()
    
    print("Alat berat berhasil ditambahkan.")
    conn.close()
    
def hapus_alat():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Hapus Alat Berat ===")
    id_alat = input("Masukkan ID Alat Berat yang ingin dihapus: ")
    cur.execute("SELECT * FROM alat_berat WHERE id_alat_berat = %s", (id_alat,))
    alat = cur.fetchone()

    if not alat:
            print("ID alat tidak ditemukan.")
            return
        
    query = "DELETE FROM alat_berat WHERE id_alat_berat = %s"
    
    cur.execute(query, (id_alat,))
    conn.commit()
    print("Alat berat berhasil dihapus.")
    conn.close()
    
def ubah_alat():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Ubah Alat Berat ===")
    id_alat = input("Masukkan ID Alat Berat yang ingin diubah: ")
    cur.execute("SELECT * FROM alat_berat WHERE id_alat_berat = %s", (id_alat,))
    alat = cur.fetchone()

    if not alat:
        print("ID alat tidak ditemukan.")
        return

    print("\nMasukkan data baru (kosongkan jika tidak ingin mengubah):")
    nama_baru = input("Nama baru: ") or alat[1]
    harga_baru = input("Harga sewa baru: ") or alat[2]
    jumlah_baru = input("Jumlah baru: ") or alat[3]
    deskripsi_baru = input("Deskripsi baru: ") or alat[4]
    operator_baru = input("ID Operator baru: ") or alat[5]
    status_baru = input("ID Status Ketersediaan baru: ") or alat[6]
    jenis_baru = input("ID Jenis Alat baru: ") or alat[7]
    
    cur.execute("""
        UPDATE alat_berat SET 
            nama_alat_berat = %s,
            harga_sewa_per_hari = %s,
            jumlah = %s,
            deskripsi_alat_berat = %s,
            id_operator = %s,
            id_status_ketersediaan = %s,
            id_jenis_alat = %s
        WHERE id_alat_berat = %s
    """, (nama_baru, harga_baru, jumlah_baru, deskripsi_baru, operator_baru, status_baru, jenis_baru, id_alat))

    conn.commit()
    print("Alat berhasil diperbarui.")
    conn.close()
    
    