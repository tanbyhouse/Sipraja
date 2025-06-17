from connectdb import get_connection
from admin import daftar_pesanan,daftar_alat_berat,lihat_histori, tambah_alat, hapus_alat, ubah_alat
def register():
    conn = get_connection()
    cur = conn.cursor()

    print("\n=== Registrasi ===")
    username = input("Masukkan Username: ")
    password = input("Masukkan Password: ")
    nama = input("Masukkan Nama Lengkap: ")
    no_telepon = input("Masukkan Nomor Telepon: ")
    alamat = input("Masukkan Alamat: ")

    cur.execute("SELECT * FROM customer WHERE username = %s", (username,))
    if cur.fetchone():
        print("Username sudah digunakan.")
    else:
        cur.execute("INSERT INTO customer (username, password, nama_customer, no_telepon_customer, alamat) VALUES (%s, %s,%s, %s,%s)", (username, password, nama, no_telepon, alamat))
        conn.commit()
        print("Registrasi berhasil!")

    conn.close()

def login():
    conn = get_connection()
    cur = conn.cursor()

    print("\n=== Login ===")
    username = input("Username: ")
    password = input("Password: ")

    cur.execute("SELECT password FROM admin WHERE username = %s", (username,))
    admin_result = cur.fetchone()
    conn.close()

    if admin_result:
        stored_pw = admin_result[0]
        if password == stored_pw:
            conn.close()
            return (username, 'admin')
        else:
            print("Password salah.")
            conn.close()
            return None
        
    cur.execute("SELECT password FROM customer WHERE username = %s", (username,))
    cust_result = cur.fetchone()
    
    if cust_result:
        stored_pw = cust_result[0]
        if password == stored_pw:
            conn.close()
            return (username, 'customer')
        else:
            print("Password salah.")
            conn.close()
            return None

    print("Username tidak ditemukan.")
    conn.close()
    return None

def autentikasi(username, role):
    if role == 'admin':
        admin_menu(username)
    else:
        customer_menu(username)

def admin_menu(username):
    while True:
        print(f"\n[ADMIN] \nSelamat datang, {username}!")
        print("1.Akses Daftar Pesanan")
        print("2.Akses Daftar Alat Berat")
        print("3.Lihat Histori Pesanan")
        print("4.Keluar")
        pilihan = input("\n\nPilih menu: ")
    
        if pilihan == "1":
            daftar_pesanan()
        elif pilihan == "2":
            daftar_alat_berat()  
            print("\n1.Tambah Alat Berat")
            print("2.Hapus Alat Berat")
            print("3.Edit Alat Berat")
            print("4.Kembali ke menu utama")
            pilihan_alat = input("\nPilih menu: ")
            if pilihan_alat == "1":
                tambah_alat()
            elif pilihan_alat == "2":
                hapus_alat()
            elif pilihan_alat == "3":
                ubah_alat()
            elif pilihan_alat == "4":
                continue
        elif pilihan == "3":
            lihat_histori() 
        elif pilihan == "4":
            print("Keluar dari admin menu...")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")
    
    
def customer_menu(username):
    print(f"\n[CUSTOMER] Selamat datang, {username}!")
    input("Tekan enter untuk kembali...")

if __name__ == "__main__":
    while True:
        print("\n=== SIPRAJA: APLIKASI PENYEWAAN ALAT BERAT ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            user_login = login()
            if user_login:
                username, role = user_login
                autentikasi(username, role)
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("Keluar dari aplikasi.")
            break
        else:
            print("Pilihan tidak valid.")
