import os
import subprocess

# Path repositori lokal
repo_dir = "C:/Users/Administrator/Desktop/ujicoba"

# Daftar file yang ingin diupload
files_to_upload = [
    "C:/Users/Administrator/Desktop/ujicoba/vaild_proxies.txt"
]

# Navigasi ke folder repositori
os.chdir(repo_dir)

# Salin file ke folder repositori
for file_path in files_to_upload:
    os.system(f'copy "{file_path}" "{repo_dir}"')

# Jalankan perintah Git
commands = [
    "git add .",
    "git commit -m 'proxy'",
    "git push origin main"
]

for command in commands:
    subprocess.run(command, shell=True)
