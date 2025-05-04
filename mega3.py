import os
import sys
import time
import random
import threading
import requests
import subprocess
import socket
import concurrent.futures
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'

class Symbols:
    INFO = f"{Colors.BRIGHT_BLUE}[i]{Colors.RESET}"
    SUCCESS = f"{Colors.BRIGHT_GREEN}[+]{Colors.RESET}"
    WARNING = f"{Colors.BRIGHT_YELLOW}[!]{Colors.RESET}"
    ERROR = f"{Colors.BRIGHT_RED}[X]{Colors.RESET}"
    RUN = f"{Colors.BRIGHT_MAGENTA}[*]{Colors.RESET}"
    INPUT = f"{Colors.BRIGHT_CYAN}[?]{Colors.RESET}"

def print_slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.BRIGHT_MAGENTA}╔══════════════════════════════════════════════════════════╗
║  {Colors.BRIGHT_RED}    _____                      _  _    ___  _  _        {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_RED}   | ____|_ __ _ __ ___  _ __| || |  / _ \| || |        {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_RED}   |  _| | '__| '__/ _ \| '__| || |_| | | | || |_       {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_RED}   | |___| |  | | | (_) | |  |__   _| |_| |__   _|      {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_RED}   |_____|_|  |_|  \___/|_|     |_|  \___/   |_|        {Colors.BRIGHT_MAGENTA}║
║                                                          ║
║           Advanced Security Testing Framework            ║
║                                                          ║
║     Creator: Mr Error 404        Version: 3.0 MEGA       ║
║     TikTok: @sir_error404       Status: Premium          ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def print_tool_header(text):
    print(f"\n{Colors.BRIGHT_MAGENTA}{'═' * 60}")
    print(f"{Colors.BRIGHT_WHITE}{text.center(60)}")
    print(f"{Colors.BRIGHT_MAGENTA}{'═' * 60}{Colors.RESET}\n")

def show_progress(current, total):
    bar_width = 40
    progress = int(bar_width * current / total)
    bar = f"[{'=' * progress}{' ' * (bar_width - progress)}]"
    percent = current / total * 100
    print(f"\r{Colors.BRIGHT_BLUE}Progress: {bar} {percent:.1f}%{Colors.RESET}", end='')
    if current == total:
        print()

def animate_loading(text, duration=2):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.BRIGHT_CYAN}{chars[i % len(chars)]} {text}...{Colors.RESET}", end='')
        time.sleep(0.1)
        i += 1
    print()

class SecurityFramework:
    def __init__(self):
        self.tools = {
            '01': ('Website Information', self.website_info),
            '02': ('SQLi-Scanner', self.sqli_scanner),
            '03': ('Admin Panel Finder', self.admin_finder),
            '04': ('Port Scanner', self.port_scanner),
            '05': ('Directory Scanner', self.directory_scanner),
            '06': ('Subdomain Scanner', self.subdomain_scanner),
            '07': ('WordPress Scanner', self.wordpress_scanner),
            '08': ('XSS-Scanner', self.xss_scanner),
            '09': ('FTP/SSH Scanner', self.ftp_ssh_scanner),
            '10': ('Email Scraper', self.email_scraper),
            '11': ('DNS Tools', self.dns_tools),
            '12': ('CMS Detector', self.cms_detector),
            '13': ('Reverse IP Lookup', self.reverse_ip),
            '14': ('About Framework', self.show_about)
        }
        self.create_directories()

    def create_directories(self):
        dirs = [
            'results/website_info', 'results/sqli',
            'results/admin_panels', 'results/ports',
            'results/directories', 'results/subdomains',
            'results/wordpress', 'results/xss',
            'results/ftp_ssh', 'results/emails',
            'results/dns', 'results/cms',
            'results/reverse_ip'
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

    def show_menu(self):
        while True:
            try:
                clear_screen()
                print_banner()
                print(f"{Colors.BRIGHT_MAGENTA}╔══════════════════════════════════════════════════════════╗")
                print(f"║{Colors.BRIGHT_WHITE}                   AVAILABLE TOOLS                        {Colors.BRIGHT_MAGENTA}║")
                print(f"╠══════════════════════════════════════════════════════════╣")

                tools_list = list(self.tools.items())
                half = len(tools_list) // 2

                for i in range(half):
                    left_tool = tools_list[i]
                    right_tool = tools_list[i + half]
                    left = f"{Colors.BRIGHT_CYAN}{left_tool[0]}{Colors.BRIGHT_WHITE} {left_tool[1][0]}"
                    right = f"{Colors.BRIGHT_CYAN}{right_tool[0]}{Colors.BRIGHT_WHITE} {right_tool[1][0]}"
                    print(f"║ {left:<35}    ║ {right:<35} {Colors.BRIGHT_MAGENTA}║")

                print(f"╠══════════════════════════════════════════════════════════╣")
                print(f"║{Colors.BRIGHT_RED} 99{Colors.BRIGHT_WHITE} Exit Framework                                        {Colors.BRIGHT_MAGENTA}║")
                print(f"╚══════════════════════════════════════════════════════════╝{Colors.RESET}")

                choice = input(f"\n{Colors.BRIGHT_GREEN}┌──({Colors.BRIGHT_RED}Mr㉿Error404{Colors.BRIGHT_GREEN})-[{Colors.BRIGHT_WHITE}~/framework{Colors.BRIGHT_GREEN}]\n└─$ {Colors.RESET}")

                if choice == '99':
                    print_slow(f"\n{Symbols.INFO} Thanks for using Error404 Framework! Goodbye...")
                    break

                if choice in self.tools:
                    animate_loading(f"Loading {self.tools[choice][0]}")
                    self.tools[choice][1]()
                    input(f"\n{Symbols.INPUT} Press Enter to continue...")
                else:
                    print(f"\n{Symbols.ERROR} Invalid option selected!")
                    time.sleep(1)

            except KeyboardInterrupt:
                continue
            except Exception as e:
                print(f"\n{Symbols.ERROR} An error occurred: {str(e)}")
                time.sleep(2)
                continue

    def save_results(self, tool_name, target, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/{tool_name}/{target}_{timestamp}.txt"

        with open(filename, "w") as f:
            f.write(f"Error404 Security Framework - {tool_name}\n")
            f.write(f"Target: {target}\n")
            f.write(f"Scan Time: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            f.write(results)

        print(f"\n{Symbols.SUCCESS} Results saved to {filename}")

    def website_info(self):
        clear_screen()
        print_tool_header("Website Information Gathering")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        try:
            print(f"\n{Symbols.RUN} Gathering information...")
            response = requests.get(url, timeout=15, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')

            info = {
                'Server': response.headers.get('Server', 'Not Found'),
                'Technologies': response.headers.get('X-Powered-By', 'Not Found'),
                'IP Address': socket.gethostbyname(urlparse(url).netloc),
                'Response Code': response.status_code,
                'Title': soup.title.string if soup.title else 'Not Found',
                'Meta Tags': len(soup.find_all('meta')),
                'Links': len(soup.find_all('a')),
                'Images': len(soup.find_all('img')),
                'Scripts': len(soup.find_all('script')),
                'Forms': len(soup.find_all('form'))
            }

            results = ""
            for key, value in info.items():
                results += f"{key}: {value}\n"
                print(f"{Symbols.SUCCESS} {key}: {value}")

            self.save_results('website_info', urlparse(url).netloc, results)

        except Exception as e:
            print(f"{Symbols.ERROR} Error: {str(e)}")

    def sqli_scanner(self):
        clear_screen()
        print_tool_header("SQL Injection Scanner")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        payloads = [
            "'", "\"", "1'", "1\"",
            "' OR '1'='1", "\" OR \"1\"=\"1",
            "' OR '1'='1'--", "\" OR \"1\"=\"1\"--",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "1' ORDER BY 1--",
            "1' ORDER BY 2--",
            "1' GROUP BY 1,2,3--",
            "' OR 'x'='x",
            "' AND id IS NULL; --",
            "' UNION ALL SELECT NULL--",
            "' UNION ALL SELECT NULL,NULL--",
            "' UNION ALL SELECT NULL,NULL,NULL--"
        ]

        print(f"\n{Symbols.RUN} Starting SQL injection scan...")
        results = ""
        vulnerable = False

        for payload in payloads:
            try:
                print(f"\n{Symbols.RUN} Testing payload: {payload}")
                test_url = url + payload
                response = requests.get(test_url, timeout=10, verify=False)

                error_signs = [
                    'sql syntax',
                    'mysql error',
                    'mysql_fetch',
                    'mysql_num_rows',
                    'mysql_result',
                    'postgresql error',
                    'sqlite error',
                    'ora-00933',
                    'oracle error',
                    'microsoft sql server',
                    'msql',
                    'microsoft ole db'
                ]

                for sign in error_signs:
                    if sign in response.text.lower():
                        vulnerable = True
                        vuln_info = f"Vulnerability found with payload: {payload}\n"
                        results += vuln_info
                        print(f"{Symbols.SUCCESS} {vuln_info}")
                        break

            except Exception as e:
                print(f"{Symbols.WARNING} Error testing payload: {str(e)}")
                continue

        if not vulnerable:
            print(f"\n{Symbols.INFO} No SQL injection vulnerabilities found")
            results = "No vulnerabilities detected\n"

        self.save_results('sqli', urlparse(url).netloc, results)

    def admin_finder(self):
        clear_screen()
        print_tool_header("Admin Panel Finder")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        paths = [
            'admin/', 'administrator/', 'admin1/', 'admin2/', 'admin3/',
            'admin4/', 'admin5/', 'admin.php/', 'admin.html/', 'admin.asp/',
            'wp-admin/', 'wp-login.php/', 'admin/cp.php/', 'cp.php/',
            'admincp/', 'admincp.php/', 'admin/controlpanel.php/',
            'adminpanel/', 'webadmin/', 'admins/', 'logins/', 'admin.jsp/',
            'admin/admin.jsp/', 'admin/home.jsp/', 'manager/',
            'administration/', 'joomla/administrator/', 'cms/administrator/'
        ]

        print(f"\n{Symbols.RUN} Starting admin panel scan...")
        results = ""
        found = False

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(requests.get, url.rstrip('/') + '/' + path, timeout=5, verify=False): path for path in paths}

            for future in concurrent.futures.as_completed(future_to_url):
                path = future_to_url[future]
                try:
                    response = future.result()
                    if response.status_code in [200, 201, 202, 203, 301, 302, 307, 403]:
                        found = True
                        panel_info = f"Admin panel found: {url}/{path} (Status: {response.status_code})\n"
                        results += panel_info
                        print(f"{Symbols.SUCCESS} {panel_info}")
                except:
                    continue

        if not found:
            print(f"\n{Symbols.INFO} No admin panels found")
            results = "No admin panels detected\n"

        self.save_results('admin_panels', urlparse(url).netloc, results)

    def port_scanner(self):
        clear_screen()
        print_tool_header("Port Scanner")

        target = input(f"{Symbols.INPUT} Enter target IP/Domain: ")
        try:
            target_ip = socket.gethostbyname(target)
        except:
            print(f"{Symbols.ERROR} Invalid target")
            return

        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
                993, 995, 1723, 3306, 3389, 5900, 8080]

        print(f"\n{Symbols.RUN} Starting port scan on {target_ip}...")
        results = f"Port scan results for {target_ip}\n\n"
        open_ports = []

        def scan_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            sock.close()
            return port, result == 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_port = {executor.submit(scan_port, port): port for port in ports}

            for future in concurrent.futures.as_completed(future_to_port):
                port, is_open = future.result()
                if is_open:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    open_ports.append((port, service))
                    port_info = f"Port {port} ({service}) is open\n"
                    results += port_info
                    print(f"{Symbols.SUCCESS} {port_info}")

        if not open_ports:
            print(f"\n{Symbols.INFO} No open ports found")
            results += "No open ports detected\n"

        self.save_results('ports', target_ip, results)

    def directory_scanner(self):
        clear_screen()
        print_tool_header("Directory Scanner")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        dirs = [
            'admin', 'administrator', 'backup', 'backups', 'css', 'images',
            'img', 'js', 'javascript', 'logs', 'old', 'temp', 'test', 'tmp',
            'upload', 'uploads', 'video', 'videos', 'webmail', 'wordpress'
        ]

        print(f"\n{Symbols.RUN} Starting directory scan...")
        results = ""
        found = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_dir = {executor.submit(requests.get, url.rstrip('/') + '/' + d, timeout=5, verify=False): d for d in dirs}

            for future in concurrent.futures.as_completed(future_to_dir):
                directory = future_to_dir[future]
                try:
                    response = future.result()
                    if response.status_code in [200, 201, 202, 203, 301, 302, 307, 403]:
                        dir_info = f"Directory found: /{directory} (Status: {response.status_code})\n"
                        results += dir_info
                        print(f"{Symbols.SUCCESS} {dir_info}")
                        found.append(directory)
                except:
                    continue

        if not found:
            print(f"\n{Symbols.INFO} No directories found")
            results = "No directories detected\n"

        self.save_results('directories', urlparse(url).netloc, results)

    def subdomain_scanner(self):
        clear_screen()
        print_tool_header("Subdomain Scanner")

        domain = input(f"{Symbols.INPUT} Enter domain (e.g. example.com): ")

        subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop',
            'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover',
            'autoconfig', 'news', 'cp', 'wordpress', 'blog', 'shop', 'dev',
            'portal', 'ssl', 'secure', 'customer', 'beta', 'api'
        ]

        print(f"\n{Symbols.RUN} Starting subdomain scan...")
        results = ""
        found = []

        def check_subdomain(subdomain):
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url, timeout=5, verify=False)
                ip = socket.gethostbyname(f"{subdomain}.{domain}")
                return subdomain, ip
            except:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_subdomain = {executor.submit(check_subdomain, s): s for s in subdomains}

            for future in concurrent.futures.as_completed(future_to_subdomain):
                result = future.result()
                if result:
                    subdomain, ip = result
                    sub_info = f"Subdomain found: {subdomain}.{domain} ({ip})\n"
                    results += sub_info
                    print(f"{Symbols.SUCCESS} {sub_info}")
                    found.append(subdomain)

        if not found:
            print(f"\n{Symbols.INFO} No subdomains found")
            results = "No subdomains detected\n"

        self.save_results('subdomains', domain, results)

    def wordpress_scanner(self):
        clear_screen()
        print_tool_header("WordPress Scanner")

        url = input(f"{Symbols.INPUT} Enter WordPress site URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        print(f"\n{Symbols.RUN} Starting WordPress scan...")
        results = ""

        try:
            response = requests.get(url, timeout=10, verify=False)
            if 'wp-content' not in response.text:
                print(f"{Symbols.ERROR} This doesn't appear to be a WordPress site")
                return

            results += "WordPress installation detected\n\n"

            # Version check
            if 'meta name="generator" content="WordPress' in response.text:
                version = re.search('content="WordPress (.*?)"', response.text)
                if version:
                    ver_info = f"WordPress version: {version.group(1)}\n"
                    results += ver_info
                    print(f"{Symbols.SUCCESS} {ver_info}")

            # Theme detection
            theme = re.search('/wp-content/themes/(.*?)/', response.text)
            if theme:
                theme_info = f"Active theme: {theme.group(1)}\n"
                results += theme_info
                print(f"{Symbols.SUCCESS} {theme_info}")

            # Plugin detection
            plugins = re.findall('/wp-content/plugins/(.*?)/', response.text)
            if plugins:
                results += "\nDetected plugins:\n"
                for plugin in set(plugins):
                    plugin_info = f"- {plugin}\n"
                    results += plugin_info
                    print(f"{Symbols.SUCCESS} Found plugin: {plugin}")

            # Common vulnerabilities check
            vuln_paths = [
                '/wp-content/debug.log',
                '/wp-config.php~',
                '/wp-config.php.save',
                '/wp-admin/install.php',
                '/.wp-config.php.swp',
                '/wp-config-sample.php'
            ]

            results += "\nVulnerability scan results:\n"
            for path in vuln_paths:
                try:
                    test_url = url.rstrip('/') + path
                    response = requests.get(test_url, timeout=5, verify=False)
                    if response.status_code == 200:
                        vuln_info = f"Potential vulnerability: {path}\n"
                        results += vuln_info
                        print(f"{Symbols.WARNING} {vuln_info}")
                except:
                    continue

        except Exception as e:
            print(f"{Symbols.ERROR} Error: {str(e)}")
            results = f"Scan error: {str(e)}\n"

        self.save_results('wordpress', urlparse(url).netloc, results)

    def xss_scanner(self):
        clear_screen()
        print_tool_header("XSS Vulnerability Scanner")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            '"><script>alert("XSS")</script>',
            '"><img src=x onerror=alert("XSS")>',
            '"><svg onload=alert("XSS")>',
            '\';alert("XSS");//',
            '<scr<script>ipt>alert("XSS")</scr</script>ipt>',
            '<script>eval(String.fromCharCode(88,83,83))</script>'
        ]

        print(f"\n{Symbols.RUN} Starting XSS vulnerability scan...")
        results = ""
        found = False

        for payload in payloads:
            try:
                print(f"\n{Symbols.RUN} Testing payload: {payload}")
                encoded_payload = requests.utils.quote(payload)
                test_url = url + encoded_payload
                response = requests.get(test_url, timeout=10, verify=False)

                if payload in response.text:
                    found = True
                    vuln_info = f"XSS vulnerability found with payload: {payload}\n"
                    results += vuln_info
                    print(f"{Symbols.SUCCESS} {vuln_info}")

            except Exception as e:
                print(f"{Symbols.WARNING} Error testing payload: {str(e)}")
                continue

        if not found:
            print(f"\n{Symbols.INFO} No XSS vulnerabilities found")
            results = "No vulnerabilities detected\n"

        self.save_results('xss', urlparse(url).netloc, results)

    def ftp_ssh_scanner(self):
        clear_screen()
        print_tool_header("FTP/SSH Scanner")

        target = input(f"{Symbols.INPUT} Enter target IP/Domain: ")
        try:
            target_ip = socket.gethostbyname(target)
        except:
            print(f"{Symbols.ERROR} Invalid target")
            return

        print(f"\n{Symbols.RUN} Scanning for FTP (21) and SSH (22)...")
        results = ""

        def check_port(port):
            service = "FTP" if port == 21 else "SSH"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target_ip, port))

                if result == 0:
                    try:
                        banner = sock.recv(1024).decode().strip()
                        service_info = f"{service} service found on port {port}\nBanner: {banner}\n"
                        results = service_info
                        print(f"{Symbols.SUCCESS} {service_info}")
                    except:
                        service_info = f"{service} port {port} is open\n"
                        results = service_info
                        print(f"{Symbols.SUCCESS} {service_info}")

                sock.close()
                return results
            except:
                return ""

        ftp_result = check_port(21)
        ssh_result = check_port(22)

        final_results = ftp_result + ssh_result

        if not final_results:
            print(f"\n{Symbols.INFO} No FTP/SSH services found")
            final_results = "No services detected\n"

        self.save_results('ftp_ssh', target_ip, final_results)

    def email_scraper(self):
        clear_screen()
        print_tool_header("Email Scraper")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        print(f"\n{Symbols.RUN} Scraping emails...")
        results = ""

        try:
            response = requests.get(url, timeout=10, verify=False)
            emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', response.text))

            if emails:
                results = f"Found {len(emails)} unique email(s):\n\n"
                for email in emails:
                    results += f"{email}\n"
                    print(f"{Symbols.SUCCESS} Found: {email}")
            else:
                print(f"\n{Symbols.INFO} No emails found")
                results = "No emails detected\n"

        except Exception as e:
            print(f"{Symbols.ERROR} Error: {str(e)}")
            results = f"Scraping error: {str(e)}\n"

        self.save_results('emails', urlparse(url).netloc, results)

    def dns_tools(self):
        clear_screen()
        print_tool_header("DNS Analysis Tools")

        domain = input(f"{Symbols.INPUT} Enter domain: ")
        print(f"\n{Symbols.RUN} Gathering DNS information...")
        results = ""

        try:
            # A Record
            ip = socket.gethostbyname(domain)
            results += f"A Record (IPv4): {ip}\n"
            print(f"{Symbols.SUCCESS} A Record: {ip}")

            # Reverse DNS
            try:
                reverse_dns = socket.gethostbyaddr(ip)[0]
                results += f"Reverse DNS: {reverse_dns}\n"
                print(f"{Symbols.SUCCESS} Reverse DNS: {reverse_dns}")
            except:
                results += "Reverse DNS: Not found\n"

            # Mail servers
            try:
                answers = socket.getaddrinfo(f"mail.{domain}", None)
                if answers:
                    results += "\nMail servers:\n"
                    for answer in answers:
                        results += f"- {answer[4][0]}\n"
                        print(f"{Symbols.SUCCESS} Mail server: {answer[4][0]}")
            except:
                results += "Mail servers: Not found\n"

        except Exception as e:
                        print(f"{Symbols.ERROR} Error:{str(e)}")
        results = F"DNS analysis error: {str(e)}\n"

        self.save_results('dns', domain, results)

    def cms_detector(self):
        clear_screen()
        print_tool_header("CMS Detector")

        url = input(f"{Symbols.INPUT} Enter target URL: ")
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        print(f"\n{Symbols.RUN} Detecting CMS...")
        results = ""

        cms_signatures = {
            'WordPress': [
                '/wp-content/',
                '/wp-includes/',
                'wp-login.php',
                'WordPress'
            ],
            'Joomla': [
                '/administrator/',
                '/components/',
                '/modules/',
                'Joomla!'
            ],
            'Drupal': [
                '/sites/default/',
                '/sites/all/',
                'Drupal.settings'
            ],
            'Magento': [
                '/skin/frontend/',
                '/magento/admin/',
                'Mage.Cookies'
            ],
            'PrestaShop': [
                '/prestashop/',
                '/modules/prestashop/',
                'PrestaShop'
            ]
        }

        try:
            response = requests.get(url, timeout=10, verify=False)
            found_cms = None

            for cms, signatures in cms_signatures.items():
                for signature in signatures:
                    if signature.lower() in response.text.lower():
                        found_cms = cms
                        break
                if found_cms:
                    break

            if found_cms:
                cms_info = f"Detected CMS: {found_cms}\n"
                results += cms_info
                print(f"{Symbols.SUCCESS} {cms_info}")

                # Additional CMS-specific checks
                if found_cms == 'WordPress':
                    # Check WordPress version
                    version = re.search('content="WordPress (.*?)"', response.text)
                    if version:
                        version_info = f"WordPress version: {version.group(1)}\n"
                        results += version_info
                        print(f"{Symbols.SUCCESS} {version_info}")

                elif found_cms == 'Joomla':
                    # Check Joomla version from manifest
                    try:
                        manifest = requests.get(url + '/administrator/manifests/files/joomla.xml', timeout=5, verify=False)
                        version = re.search('<version>(.*?)</version>', manifest.text)
                        if version:
                            version_info = f"Joomla version: {version.group(1)}\n"
                            results += version_info
                            print(f"{Symbols.SUCCESS} {version_info}")
                    except:
                        pass
            else:
                print(f"\n{Symbols.INFO} Could not determine CMS")
                results = "No CMS detected\n"

        except Exception as e:
            print(f"{Symbols.ERROR} Error: {str(e)}")
            results = f"Detection error: {str(e)}\n"

        self.save_results('cms', urlparse(url).netloc, results)

    def reverse_ip(self):
        clear_screen()
        print_tool_header("Reverse IP Lookup")

        ip = input(f"{Symbols.INPUT} Enter IP address: ")

        try:
            socket.inet_aton(ip)
        except:
            print(f"{Symbols.ERROR} Invalid IP address")
            return

        print(f"\n{Symbols.RUN} Performing reverse IP lookup...")
        results = ""

        try:
            # Basic reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                host_info = f"Hostname: {hostname}\n"
                results += host_info
                print(f"{Symbols.SUCCESS} {host_info}")
            except:
                results += "No hostname found\n"
                print(f"{Symbols.INFO} No hostname found")

            # Additional IP information
            try:
                response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'error' not in data:
                        ip_info = f"""
Location Information:
-------------------
Country: {data.get('country_name', 'Unknown')}
Region: {data.get('region', 'Unknown')}
City: {data.get('city', 'Unknown')}
ISP: {data.get('org', 'Unknown')}
ASN: {data.get('asn', 'Unknown')}
Timezone: {data.get('timezone', 'Unknown')}
"""
                        results += ip_info
                        print(ip_info)
            except:
                pass

        except Exception as e:
            print(f"{Symbols.ERROR} Error: {str(e)}")
            results = f"Lookup error: {str(e)}\n"

        self.save_results('reverse_ip', ip, results)

    def show_about(self):
        clear_screen()
        about = f"""
{Colors.BRIGHT_MAGENTA}╔══════════════════════════════════════════════════════════╗
║              Advanced Security Testing Framework             ║
╠══════════════════════════════════════════════════════════╣
║  {Colors.BRIGHT_WHITE}Developer:{Colors.BRIGHT_GREEN}    Mr Error 404                               {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_WHITE}Version:{Colors.BRIGHT_GREEN}      3.0 MEGA                                   {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_WHITE}TikTok:{Colors.BRIGHT_GREEN}       @sir_error404                             {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_WHITE}Status:{Colors.BRIGHT_GREEN}       Premium Framework                          {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_WHITE}Tools:{Colors.BRIGHT_GREEN}        13 Advanced Security Tools                 {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_WHITE}Updates:{Colors.BRIGHT_GREEN}      Regular Updates & New Features             {Colors.BRIGHT_MAGENTA}║
║  {Colors.BRIGHT_WHITE}Purpose:{Colors.BRIGHT_GREEN}      Security Testing & Vulnerability Analysis  {Colors.BRIGHT_MAGENTA}║
╚══════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        print(about)

if __name__ == "__main__":
    try:
        clear_screen()
        animate_loading("Starting Error404 Security Framework")
        framework = SecurityFramework()
        framework.show_menu()
    except KeyboardInterrupt:
        print(f"\n{Symbols.WARNING} Program terminated by user")
        sys.exit()
    except Exception as e:
        print(f"\n{Symbols.ERROR} Fatal error: {str(e)}")
        sys.exit(1)