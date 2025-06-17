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
        SELECT c.nama_customer, c.no_telepon_customer, c.alamat, p.tanggal_pemesanan, p.tanggal_mulai_sewa, p.tanggal_selesai_sewa,
        p.total_harga, sp.status_penyewaan, a.nama_alat_berat
        FROM penyewaan p
        JOIN customer c ON p.id_customer = c.id_customer
        JOIN status_penyewaan sp ON p.id_status_penyewaan = sp.id_status_penyewaan
        JOIN detail_penyewaan dp ON p.id_penyewaan = dp.id_penyewaan
        JOIN alat_berat a ON dp.id_alat_berat = a.id_alat_berat
        WHERE sp.status_penyewaan = 'Menunggu'
        ORDER BY p.tanggal_pemesanan DESC
    """
    cur.execute(query)
    results = cur.fetchall()
    
    if results:
        tampilkan_pesanan(results)
    else:
        print("Tidak ada pesanan yang masuk.")
    input("Tekan Enter untuk kembali ke menu...")
    conn.close()
    

def tampilkan_pesanan(results):
    headers = [
        "Nama", "No Telepon", "Alamat",
        "Tgl Pemesanan", "Tgl Sewa", "Tgl Selesai Sewa", "Total",
        "Status", "Alat Berat"
    ]
    
    formatted_results = []
    for row in results:
        formatted_row = list(row)
        formatted_row[2] = bungkus_teks(formatted_row[2], 15)
        formatted_row[6] = f"Rp {int(formatted_row[6]):,}".replace(",", ".") 
        formatted_results.append(formatted_row)

    print(tabulate(formatted_results, headers=headers, tablefmt="fancy_grid", stralign="center",numalign="center"))

def daftar_alat_berat():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n=== Daftar Alat Berat ===")
    query = """
        SELECT a.nama_alat_berat, a.harga_sewa_per_hari, a.jumlah, 
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
    input("Tekan Enter untuk kembali ke menu...")
    conn.close()
    
def tampilkan_alat(results):
    headers = [
        "Nama", "Harga Sewa/hari", "Jumlah",
        "Operator", "Status"
    ]
    
    formatted_results = []
    for row in results:
        formatted_row = list(row)
        formatted_row[1] = f"Rp {int(float(formatted_row[1])):,}".replace(",", ".")
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