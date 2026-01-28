# boot_love_os.py
import os
import sys
import subprocess
import tempfile
from cryptography.fernet import Fernet

# --- 1. Key Authentication ---
key_file = "secret.key"
if not os.path.exists(key_file):
    print("🛑 ERROR: Authentication key (secret.key) not found.")
    print("Please place the key file in this directory to initialize the system.")
    sys.exit(1)

with open(key_file, "rb") as k:
    key = k.read()

cipher = Fernet(key)

# --- 2. System Menu ---
print("\n🪐 Love-OS Secure Bootloader v1.0")
print("-----------------------------------")
print("1. Dashboard (UI)         [Launch: Streamlit]")
print("2. Kernel v0.7 (Chat)     [Launch: Console]")
print("3. Relational Engine      [Launch: Math]")
print("4. Team Compressor        [Launch: Analytics]")
print("-----------------------------------")

choice = input("Select Module to Launch [1-4]: ")

# File Mapping
files = {
    "1": "love_os_dashboard.bin",
    "2": "love_os_v0_7_kernel.bin",
    "3": "love_os_relational_engine.bin",
    "4": "team_compressor.bin"
}

target_bin = files.get(choice)

# --- 3. Decryption & Execution ---
if target_bin and os.path.exists(target_bin):
    print(f"\n🔓 Decrypting... ({target_bin})")
    
    with open(target_bin, "rb") as f:
        encrypted_data = f.read()
    
    try:
        decrypted_code = cipher.decrypt(encrypted_data)
        
        # A. Dashboard (Streamlit requires a physical file)
        if choice == "1":
            print("🚀 Deploying Dashboard Interface...")
            # Create temp file (Manual management required for Streamlit)
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                tmp.write(decrypted_code)
                tmp_name = tmp.name
            
            try:
                subprocess.run(["streamlit", "run", tmp_name])
            except KeyboardInterrupt:
                pass
            finally:
                # Cleanup immediately (Evidence elimination)
                os.remove(tmp_name)
                print("\n🧹 Temporary files wiped. Security secure.")

        # B. Other Tools (Direct Memory Execution)
        else:
            print("🚀 System Link Established. Executing...")
            print("-----------------------------------")
            # Execute code directly in memory
            exec(decrypted_code)

    except Exception as e:
        print(f"💀 Execution Error: {e}")
        print("Invalid key or corrupted binary file.")

else:
    print("❌ File not found or invalid selection.")
