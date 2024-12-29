import subprocess
import time

def run_scripts():
    while True:
        # Menjalankan script 1
        print("Menjalankan script1.py...")
        subprocess.run(["python", "proxy.py"])
        
        # Menjalankan script 2
        print("Menjalankan script2.py...")
        subprocess.run(["python", "upload.py"])
        
        # Tunggu selama 5 menit
        print("Menunggu selama 5 menit sebelum menjalankan ulang...")
        time.sleep(5 * 60)  # 5 menit dalam detik

if __name__ == "__main__":
    run_scripts()