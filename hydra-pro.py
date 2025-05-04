import os
import time
import requests
from colorama import init, Fore, Style, Back
import sys
import random
from concurrent.futures import ThreadPoolExecutor
import itertools
import socket
from datetime import datetime
import json
import shutil
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

class Colors:
    """Color management for console output"""
    PRIMARY = Fore.CYAN
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.WHITE
    TITLE = Fore.MAGENTA

    @staticmethod
    def rainbow(text):
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        colored_chars = []
        for i, char in enumerate(text):
            if char != ' ':
                colored_chars.append(f"{Style.BRIGHT}{colors[i % len(colors)]}{char}")
            else:
                colored_chars.append(char)
        return ''.join(colored_chars) + Style.RESET_ALL

class Effects:
    """Visual effects for the console"""
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def matrix_rain(duration=2):
        width = shutil.get_terminal_size().columns
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()"
        end_time = time.time() + duration

        while time.time() < end_time:
            line = ""
            for _ in range(width):
                char = random.choice(chars)
                color = random.choice([Fore.GREEN, Fore.CYAN])
                line += f"{Style.BRIGHT}{color}{char}"
            print(line)
            time.sleep(0.05)
        print(Style.RESET_ALL)

    @staticmethod
    def loading_spinner(text, duration=2):
        spinners = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.PRIMARY}{text} {spinners[i]}{Style.RESET_ALL}", end='')
            time.sleep(0.1)
            i = (i + 1) % len(spinners)
        print()

class WordlistManager:
    """Manages username and password lists"""
    def __init__(self):
        self.usernames = []
        self.passwords = []
        self.github_urls = {
            'usernames': [
                'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/xato-net-10-million-usernames.txt',
                'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt'
            ],
            'passwords': [
                'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords.txt',
                'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt'
            ]
        }
        self.local_files = {
            'usernames': 'hydra_usernames.txt',
            'passwords': 'hydra_passwords.txt'
        }

    def download_from_github(self):
        """Download wordlists from GitHub"""
        print(f"\n{Colors.INFO}Downloading wordlists from GitHub...")

        for list_type, urls in self.github_urls.items():
            words = set()
            for url in urls:
                try:
                    print(f"\n{Colors.PRIMARY}Downloading {list_type} from: {url}")
                    response = requests.get(url, stream=True)
                    total_size = int(response.headers.get('content-length', 0))

                    with tqdm(total=total_size, unit='B', unit_scale=True,
                            desc=f"{Colors.PRIMARY}Progress",
                            bar_format="{l_bar}{bar:30}{r_bar}") as pbar:
                        content = ""
                        for data in response.iter_content(chunk_size=1024):
                            content += data.decode('utf-8', errors='ignore')
                            pbar.update(len(data))

                        new_words = set(line.strip() for line in content.splitlines() if line.strip())
                        words.update(new_words)
                        print(f"{Colors.SUCCESS}Added {len(new_words):,} {list_type}")

                except Exception as e:
                    print(f"{Colors.ERROR}Error downloading from {url}: {str(e)}")
                    continue

           
            filename = self.local_files[list_type]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(words)))
            print(f"{Colors.SUCCESS}Saved {len(words):,} {list_type} to {filename}")

            if list_type == 'usernames':
                self.usernames = list(words)
            else:
                self.passwords = list(words)

    def load_local_lists(self):
        """Load wordlists from local files"""
        try:
            for list_type, filename in self.local_files.items():
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        words = [line.strip() for line in f if line.strip()]
                        if list_type == 'usernames':
                            self.usernames = words
                        else:
                            self.passwords = words
                    print(f"{Colors.SUCCESS}Loaded {len(words):,} {list_type} from {filename}")
                else:
                    print(f"{Colors.WARNING}{filename} not found, downloading...")
                    self.download_from_github()
                    return
        except Exception as e:
            print(f"{Colors.ERROR}Error loading wordlists: {str(e)}")
            self.download_from_github()

    def generate_random_username(self):
        """Generate a random username"""
        if not self.usernames:
            return "admin"

        base = random.choice(self.usernames)
        modifications = [
            lambda x: x,
            lambda x: x + str(random.randint(1, 999)),
            lambda x: x.capitalize(),
            lambda x: x + random.choice(['_admin', '_user', '_test']),
            lambda x: 'admin_' + x,
            lambda x: x + random.choice(['123', '321', '789'])
        ]
        return random.choice(modifications)(base)

class Banner:
    """Manages the program banner"""
    def __init__(self):
        self.ascii_art = """
██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗
███████║ ╚████╔╝ ██║  ██║██████╔╝███████║
██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║
██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
        """

    def render(self, target_info="No Target", status="OFFLINE"):
        """Render the banner with current information"""
        banner = Colors.rainbow(self.ascii_art)

        info_box = f"""
{Colors.PRIMARY}╔═══════════════════════════════════════════╗
║ {Colors.INFO}Target: {Colors.PRIMARY}{target_info:<35} ║
║ {Colors.INFO}Status: {Colors.SUCCESS if status == "ONLINE" else Colors.ERROR}{status:<35} ║
║ {Colors.INFO}Developer: {Colors.PRIMARY}Mr Error404{' ' * 24} ║
║ {Colors.INFO}TikTok: {Colors.PRIMARY}@sir_error404{' ' * 23} ║
╚═══════════════════════════════════════════╝{Style.RESET_ALL}
        """

        return f"{banner}\n{info_box}"
class HydraAdvanced:
    """Main program class"""
    def __init__(self):
        self.target = None
        self.selected_protocols = []
        self.attack_running = False
        self.attempts = 0
        self.successful = 0
        self.threads = 50
        self.found_credentials = []

        self.banner = Banner()
        self.wordlist_manager = WordlistManager()

        self.protocols = {
            1: "FTP",
            2: "TELNET",
            3: "HTTP",
            4: "HTTPS",
            5: "SMTP",
            6: "MySQL",
            7: "PostgreSQL",
            8: "SMB",
            9: "SSH",
            10: "RDP"
        }

    def check_internet(self):
        """Check internet connectivity"""
        try:
            requests.get("http://www.google.com", timeout=3)
            return "ONLINE"
        except:
            return "OFFLINE"

    def show_banner(self):
        """Display the program banner"""
        Effects.clear_screen()
        status = self.check_internet()
        print(self.banner.render(self.target or "No Target", status))

    def create_menu_box(self, title, options):
        """Create a formatted menu box"""
        menu = f"\n{Colors.PRIMARY}╔══════════════════════════════════╗\n"
        menu += f"║ {Colors.rainbow(title.center(30))} ║\n"
        menu += f"╠══════════════════════════════════╣\n"

        for key, value in options.items():
            menu += f"║ {Colors.PRIMARY}[{Colors.INFO}{key}{Colors.PRIMARY}] {Colors.INFO}{value}{' ' * (27 - len(value))} ║\n"

        menu += f"╚══════════════════════════════════╝{Style.RESET_ALL}"
        return menu

    def set_target(self):
        """Set the target for the attack"""
        self.show_banner()
        print(f"\n{Colors.INFO}Enter target IP or hostname:")
        target = input(f"{Colors.PRIMARY}┌──({Colors.INFO}HYDRA{Colors.PRIMARY})-[{Colors.INFO}target{Colors.PRIMARY}]\n└─$ {Colors.INFO}")

        if target.strip():
            self.target = target
            Effects.loading_spinner("Scanning target", 2)
            self.scan_ports()
        else:
            print(f"{Colors.ERROR}Invalid target provided")
        time.sleep(2)

    def scan_ports(self):
        """Scan target ports"""
        common_ports = [21, 22, 23, 25, 80, 443, 445, 3306, 3389, 5432]
        open_ports = []

        print(f"\n{Colors.INFO}Scanning ports...")
        with tqdm(total=len(common_ports), desc=f"{Colors.PRIMARY}Progress",
                 bar_format="{l_bar}{bar:30}{r_bar}") as pbar:
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((self.target, port))
                    if result == 0:
                        service = socket.getservbyport(port)
                        open_ports.append(f"{port}/{service}")
                        print(f"{Colors.SUCCESS}[+] Port {port}/{service} is open")
                    sock.close()
                except:
                    pass
                pbar.update(1)

        if open_ports:
            print(f"\n{Colors.SUCCESS}Found open ports: {', '.join(open_ports)}")
        else:
            print(f"\n{Colors.WARNING}No open ports found")

    def select_protocols(self):
        """Select protocols for the attack"""
        self.show_banner()
        options = {str(k): v for k, v in self.protocols.items()}
        print(self.create_menu_box("AVAILABLE PROTOCOLS", options))

        print(f"\n{Colors.INFO}Enter protocol numbers (comma-separated) or 'all':")
        choice = input(f"{Colors.PRIMARY}┌──({Colors.INFO}HYDRA{Colors.PRIMARY})-[{Colors.INFO}protocols{Colors.PRIMARY}]\n└─$ {Colors.INFO}")

        self.selected_protocols = []
        if choice.lower() == 'all':
            self.selected_protocols = list(self.protocols.values())
        else:
            try:
                for num in choice.split(','):
                    num = int(num.strip())
                    if num in self.protocols:
                        self.selected_protocols.append(self.protocols[num])
                        print(f"{Colors.SUCCESS}[✓] Added: {self.protocols[num]}")
                    else:
                        print(f"{Colors.ERROR}[!] Invalid protocol: {num}")
            except ValueError:
                print(f"{Colors.ERROR}Invalid input")

        if self.selected_protocols:
            print(f"\n{Colors.SUCCESS}Selected protocols: {', '.join(self.selected_protocols)}")
        else:
            print(f"\n{Colors.ERROR}No protocols selected")
        time.sleep(2)

    def try_credentials(self, protocol, username, password):
        """Test credentials against target"""
        if not self.attack_running:
            return False

        try:
            self.attempts += 1
            progress = f"\r{Colors.PRIMARY}[{self.attempts}] Trying {protocol}: {username}:{password}"
            print(f"{progress:<80}", end='', flush=True)

            
            success = False  

            if success:
                self.successful += 1
                self.found_credentials.append({
                    'protocol': protocol,
                    'username': username,
                    'password': password,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

                print(f"\n{Colors.SUCCESS}{'=' * 50}")
                print(f"{Colors.SUCCESS}[!] CREDENTIALS FOUND!")
                print(f"{Colors.SUCCESS}Protocol: {Colors.INFO}{protocol}")
                print(f"{Colors.SUCCESS}Username: {Colors.INFO}{username}")
                print(f"{Colors.SUCCESS}Password: {Colors.INFO}{password}")
                print(f"{Colors.SUCCESS}{'=' * 50}\n")

                self.save_credentials(protocol, username, password)

            return success

        except Exception as e:
            print(f"\n{Colors.ERROR}Error: {str(e)}")
            return False

    def save_credentials(self, protocol, username, password):
        """Save found credentials to file"""
        try:
            with open('hydra_found.txt', 'a') as f:
                f.write(f"{datetime.now()} - {protocol} - {username}:{password}\n")
        except:
            pass

    def start_attack(self):
        """Start the brute force attack"""
        if not self.target or not self.selected_protocols:
            print(f"{Colors.ERROR}Please set target and protocols first")
            time.sleep(2)
            return

        # Load or download wordlists
        self.wordlist_manager.load_local_lists()

        self.attack_running = True
        self.attempts = 0
        self.successful = 0

        Effects.matrix_rain(2)
        print(f"\n{Colors.INFO}Starting attack on {Colors.PRIMARY}{self.target}")
        print(f"{Colors.INFO}Selected protocols: {Colors.PRIMARY}{', '.join(self.selected_protocols)}")
        print(f"{Colors.WARNING}Press Ctrl+C to stop the attack\n")

        try:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                while self.attack_running:
                    username = self.wordlist_manager.generate_random_username()
                    password = random.choice(self.wordlist_manager.passwords)

                    for protocol in self.selected_protocols:
                        executor.submit(self.try_credentials, protocol, username, password)

        except KeyboardInterrupt:
            self.attack_running = False
            print(f"\n{Colors.WARNING}Attack stopped by user")

        print(f"\n{Colors.SUCCESS}Attack Summary:")
        print(f"{Colors.SUCCESS}Total attempts: {self.attempts}")
        print(f"{Colors.SUCCESS}Successful attempts: {self.successful}")

    def main_menu(self):
        """Main program loop"""
        while True:
            self.show_banner()
            options = {
                "1": "Set Target",
                "2": "Select Protocols",
                "3": "Start Attack",
                "4": "Update Wordlists",
                "5": "Exit"
            }
            print(self.create_menu_box("MAIN MENU", options))

            choice = input(f"\n{Colors.PRIMARY}┌──({Colors.INFO}HYDRA{Colors.PRIMARY})-[{Colors.INFO}menu{Colors.PRIMARY}]\n└─$ {Colors.INFO}")

            if choice == '1':
                self.set_target()
            elif choice == '2':
                self.select_protocols()
            elif choice == '3':
                self.start_attack()
            elif choice == '4':
                self.wordlist_manager.download_from_github()
            elif choice == '5':
                print(f"\n{Colors.INFO}Thanks for using HYDRA. Goodbye!")
                Effects.matrix_rain(1)
                sys.exit(0)

def main():
    try:
        Effects.matrix_rain(1)
        hydra = HydraAdvanced()
        Effects.loading_spinner("Initializing HYDRA", 2)
        hydra.main_menu()
    except Exception as e:
        print(f"\n{Colors.ERROR}Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()