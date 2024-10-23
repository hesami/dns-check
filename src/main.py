import subprocess
import time
import statistics
import os
import signal
import requests
from geopy.distance import geodesic
from tqdm import tqdm
import textwrap
import colorama
from colorama import Fore, Style
from tabulate import tabulate
import platform

colorama.init(autoreset=True)

# Default DNS list
default_dns_list = [
    {"ip": "217.218.155.155", "city": "Tehran", "asn": "AS12880"},  # Tehran, TIC
    {"ip": "2.188.21.130", "city": "Tehran", "asn": "AS49666"},  # Tehran, Shatel
    {"ip": "2.185.239.133", "city": "Marīvān", "asn": "AS58224"},  # Marīvān, MobinNet
    {"ip": "194.225.62.80", "city": "Tehran", "asn": "AS43965"},  # Tehran, Afranet
    {"ip": "217.218.127.127", "city": "Tehran", "asn": "AS12880"},  # Tehran, TIC
    {"ip": "2.189.44.44", "city": "Tehran", "asn": "AS49666"},  # Tehran, Shatel
    {"ip": "178.22.122.100", "city": "Tehran", "asn": "AS43754"},  # Tehran, TIC Secondary
    {"ip": "194.36.174.1", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "2.185.239.137", "city": "Marīvān", "asn": "AS58224"},  # Marīvān, MobinNet
    {"ip": "2.185.239.136", "city": "Marīvān", "asn": "AS58224"},  # Marīvān, MobinNet
    {"ip": "194.225.152.10", "city": "Tehran", "asn": "AS6736"},  # Tehran, TIC Secondary
    {"ip": "5.145.112.39", "city": "Tehran", "asn": "AS60256"},  # Tehran, Respina
    {"ip": "5.145.112.38", "city": "Shiraz", "asn": "AS60256"},  # Shiraz, Respina
    {"ip": "5.200.200.200", "city": "Gorgan", "asn": "AS58224"},  # Gorgan, MobinNet
    {"ip": "194.36.174.150", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "89.165.10.98", "city": "Tehran", "asn": "AS39501"},  # Tehran, Afranet
    {"ip": "81.12.27.54", "city": "Mashhad", "asn": "AS58224"},  # Mashhad, MobinNet
    {"ip": "217.219.218.51", "city": "Isfahan", "asn": "AS58256"},  # Isfahan, ITC
    {"ip": "5.160.139.13", "city": "Shiraz", "asn": "AS50810"},  # Shiraz, ParsOnline
    {"ip": "91.99.101.2", "city": "Tehran", "asn": "AS44244"},  # Tehran, IR Telecom
    {"ip": "185.88.177.101", "city": "Tabriz", "asn": "AS56402"},  # Tabriz, Farabord
    {"ip": "46.209.1.50", "city": "Ahvaz", "asn": "AS58120"},  # Ahvaz, Dadeh Pardazesh
    {"ip": "79.127.127.136", "city": "Tehran", "asn": "AS25124"},  # Tehran, Respina
    {"ip": "217.11.16.59", "city": "Mashhad", "asn": "AS58224"},  # Mashhad, Parsian
    {"ip": "5.144.130.1", "city": "Tabriz", "asn": "AS34636"},  # Tabriz, Aria Shatel
    {"ip": "31.7.57.32", "city": "Tehran", "asn": "AS59441"},  # Tehran, ParsOnline DNS 1
    {"ip": "31.7.57.36", "city": "Tehran", "asn": "AS59441"},  # Tehran, ParsOnline DNS 2
    {"ip": "185.73.240.77", "city": "Isfahan", "asn": "AS58256"},  # Isfahan, TCI
    {"ip": "79.175.133.42", "city": "Karaj", "asn": "AS49100"},  # Karaj, ISP
    {"ip": "5.56.132.66", "city": "Yazd", "asn": "AS48276"},  # Yazd, Sabsever
    {"ip": "185.105.184.5", "city": "Rasht", "asn": "AS50810"},  # Rasht, Pardis Telecom
    {"ip": "81.91.128.142", "city": "Shiraz", "asn": "AS43754"},  # Shiraz, Farahan ISP
    {"ip": "5.160.203.133", "city": "Mashhad", "asn": "AS12880"},  # Mashhad, MobinNet
    {"ip": "78.38.64.20", "city": "Tehran", "asn": "AS25184"},  # Tehran, Shatel
    {"ip": "178.252.147.201", "city": "Isfahan", "asn": "AS58256"},  # Isfahan, TIC
    {"ip": "31.193.48.82", "city": "Tehran", "asn": "AS56968"},  # Tehran, ParsOnline Backup
    {"ip": "37.32.28.14", "city": "Mashhad", "asn": "AS59796"},  # Mashhad, Data Niru
    {"ip": "5.160.131.181", "city": "Shiraz", "asn": "AS50810"},  # Shiraz, Pishgaman
    {"ip": "82.99.219.144", "city": "Tehran", "asn": "AS58224"},  # Tehran, MobinNet
    {"ip": "5.144.129.17", "city": "Tabriz", "asn": "AS34636"},  # Tabriz, Aria
    {"ip": "213.207.193.130", "city": "Tehran", "asn": "AS41881"},  # Tehran, Fanavaran
    {"ip": "185.51.200.50", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "185.51.200.10", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "91.99.101.12", "city": "Tehran", "asn": "AS12880"},  # Tehran, TIC
    {"ip": "213.176.123.5", "city": "Tehran", "asn": "AS44244"},  # Tehran, IR Telecom
    {"ip": "185.143.233.233", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "185.143.234.234", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "188.114.98.98", "city": "Tehran", "asn": "AS13335"},  # Tehran, Cloudflare
    {"ip": "188.114.97.97", "city": "Tehran", "asn": "AS13335"},  # Tehran, Cloudflare
    {"ip": "178.22.122.101", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet Secondary
    {"ip": "185.51.200.3", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "171.25.193.172", "city": "Tehran", "asn": "AS3215"},  # Tehran, TOR Exit Node
    {"ip": "217.218.77.78", "city": "Tehran", "asn": "AS12880"},  # Tehran, TIC
    {"ip": "217.151.159.42", "city": "Tehran", "asn": "AS43754"},  # Tehran, MobinNet
    {"ip": "81.91.161.178", "city": "Yazd", "asn": "AS43754"}  # Yazd, Respina
]
def get_user_dns_list():
    """Get custom DNS list from user input"""
    custom_list = []
    print(f"\n{Fore.CYAN}Enter the DNS IP addresses you wish to test (type 'done' to finish):{Style.RESET_ALL}")
    while True:
        ip = input("DNS IP: ")
        if ip.lower() == 'done':
            break
        if ip:
            custom_list.append({"ip": ip, "city": "Unknown", "asn": "Unknown"})
    return custom_list

def load_dns_from_file(file_path):
    """Load DNS list from file"""
    dns_list = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                ip = line.strip()
                if ip:
                    dns_list.append({"ip": ip, "city": "Unknown", "asn": "Unknown"})
        return dns_list
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_path}' not found.{Style.RESET_ALL}")
        return None

def ping_dns(ip, duration=5):
    """Ping DNS server and collect response times"""
    response_times = []
    packet_loss_count = 0
    
    for _ in range(duration):
        try:
            ping_option = "-n" if platform.system() == "Windows" else "-c"
            pings = 1
            result = subprocess.run(["ping", ping_option, str(pings), ip], capture_output=True, text=True, timeout=3)
            if "time=" in result.stdout:
                time_str = result.stdout.split("time=")[1].split("ms")[0].strip()
                try:
                    response_time = float(time_str)
                    response_times.append(response_time)
                except ValueError:
                    packet_loss_count += 1
            else:
                packet_loss_count += 1
        except subprocess.TimeoutExpired:
            packet_loss_count += 1
        except Exception:
            packet_loss_count += 1
        time.sleep(1)
    
    if packet_loss_count == duration:
        return None, packet_loss_count
    
    return response_times, packet_loss_count

def get_dns_info(ip):
    """Fetch DNS server information using ip-api.com"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"{Fore.RED}Error fetching data for {ip}: {e}{Style.RESET_ALL}")
        return None

def calculate_distance(server_location, user_location):
    """Calculate approximate distance from user to DNS server"""
    return geodesic(server_location, user_location).km

def test_dns_servers(dns_list, user_location, duration=5, check_stddev=False, check_max_time=False):
    dns_results = []
    successful_tests = 0
    failed_tests = 0
    
    print(f"\n{Fore.YELLOW}Starting DNS tests...{Style.RESET_ALL}\n")
    
    # Use tqdm to show progress bar
    progress_bar = tqdm(total=len(dns_list), ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} DNSs tested", colour='blue')
    
    for dns in dns_list:
        try:
            dns_info = get_dns_info(dns['ip'])
            if dns_info and dns_info.get('status') == 'success':
                dns.update(dns_info)
                server_location = (dns_info['lat'], dns_info['lon'])
                dns['distance_km'] = calculate_distance(server_location, user_location)
            else:
                failed_tests += 1
                progress_bar.set_postfix(successful=successful_tests, failed=failed_tests)
                progress_bar.update(1)
                continue
            
            response_times, packet_loss_count = ping_dns(dns['ip'], duration)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Testing interrupted by user.{Style.RESET_ALL}")
            break
        
        if response_times is None:
            failed_tests += 1
            progress_bar.set_postfix(successful=successful_tests, failed=failed_tests)
            progress_bar.update(1)
            continue

        if response_times:
            avg_time = statistics.mean(response_times)
            stddev_time = statistics.stdev(response_times) if len(response_times) > 1 else 0
            max_time = max(response_times)
            reliability = (1 - (packet_loss_count / duration)) * 100
        else:
            avg_time = 0
            stddev_time = 0
            max_time = 0
            reliability = 0
        
        dns_results.append({
            "ip": dns["ip"],
            "city": dns.get("city", "Unknown"),
            "country": dns.get("country", "Unknown"),
            "regionName": dns.get("regionName", "Unknown"),
            "asn": dns.get("asn", "Unknown"),
            "isp": dns.get("isp", "Unknown"),
            "avg_time": avg_time,
            "stddev_time": stddev_time,
            "max_time": max_time,
            "reliability": reliability,
            "packet_loss": packet_loss_count,
            "distance_km": dns.get("distance_km", "Unknown")
        })

        successful_tests += 1
        progress_bar.set_postfix(successful=successful_tests, failed=failed_tests)
        progress_bar.update(1)
    
    progress_bar.close()

    if not dns_results:
        print(f"{Fore.RED}No valid DNS results found. Please check the input DNS servers.{Style.RESET_ALL}")
        return []

    sort_key = ['avg_time']
    if check_stddev:
        sort_key.append('stddev_time')
    if check_max_time:
        sort_key.append('max_time')
    
    dns_results.sort(key=lambda x: tuple(x[key] for key in sort_key))
    
    return dns_results

def print_results(results):
    """Display DNS test results as a table"""
    headers = ["IP", "City", "Country", "Region", "ASN", "ISP", "Avg Time (ms)", "StdDev (ms)", "Max Time (ms)", "Reliability (%)", "Distance (km)", "Packet Loss"]
    table = [[
        result['ip'], 
        textwrap.shorten(result['city'], width=15, placeholder="..."),
        textwrap.shorten(result['country'], width=10, placeholder="..."),
        textwrap.shorten(result['regionName'], width=10, placeholder="..."),
        textwrap.shorten(result['asn'], width=10, placeholder="..."),
        textwrap.shorten(result['isp'], width=15, placeholder="..."),
        f"{result['avg_time']:.2f}",
        f"{result['stddev_time']:.2f}",
        f"{result['max_time']:.2f}",
        f"{result['reliability']:.2f}",
        f"{result['distance_km']:.2f}" if isinstance(result['distance_km'], float) else "Unknown",
        result['packet_loss']
    ] for result in results]
    
    print(f"\n{Fore.YELLOW}===================== DNS Test Results ====================={Style.RESET_ALL}")
    print(tabulate(table, headers, tablefmt="grid"))
    print(f"{Fore.YELLOW}============================================================{Style.RESET_ALL}\n")

def main():
    dns_list = []
    user_location = (36.6753, 48.4809)  # Default location (Zanjan, Iran) for distance calculation
    
    try:
        print(f"\n{Fore.CYAN}Select the DNS list option:{Style.RESET_ALL}")
        list_choice = input("1. Iran DNS List\n2. Enter custom DNS\n3. Load DNS list from file\nChoice: ")

        if list_choice == '1':
            dns_list = default_dns_list
        elif list_choice == '2':
            dns_list = get_user_dns_list()
        elif list_choice == '3':
            file_path = input("Enter the file path: ")
            dns_list = load_dns_from_file(file_path)
            if not dns_list:
                print(f"{Fore.RED}No DNS servers loaded. Exiting...{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}Invalid choice. Exiting...{Style.RESET_ALL}")
            return
        
        if not dns_list:
            print(f"{Fore.RED}No DNS servers to test. Exiting...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}Performing DNS tests...{Style.RESET_ALL}")
        results = test_dns_servers(dns_list, user_location)
        
        if results:
            print_results(results)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Process interrupted by user. Exiting...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
