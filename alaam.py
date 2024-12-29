import time
import subprocess

# Path ke script Python utama
script_paths = ["C:/Users/Administrator/Desktop/ujicoba/proxy.py", "C:/Users/Administrator/Desktop/upload.py"]

# Fungsi untuk menjalankan script
def run_script(script_path):
    try:
        print(f"Menjalankan {script_path}...")
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Script {script_path} gagal dijalankan: {e}")

# Loop untuk menjalankan kedua script secara berurutan dengan interval 5 menit
while True:
    for script_path in script_paths:
        run_script(script_path)  # Menunggu script selesai sebelum lanjut
        print(f"Script {script_path} selesai. Menunggu 5 menit sebelum melanjutkan...")
        time.sleep(300)  # Tunggu selama 300 detik (5 menit)
