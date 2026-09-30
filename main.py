import network
import socket
import gc

# 1. Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
UPSTREAM_DNS = "1.1.1.1" # Cloudflare DNS to resolve safe sites

# The domains you want to block
BLOCKED_DOMAINS = [
    b"youtube.com",
    b"://youtube.com",
    b"youtube.lk",
    b"www.youtube.lk"
]

# 2. Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    pass

# Force a static IP if you want, or just read the assigned one
ip_address = wlan.ifconfig()[0]
print("Connected! ESP32 IP Address:", ip_address)
print("👉 Set this IP address as the primary DNS server in your router or device settings.")

# 3. Start UDP DNS Server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 53)) # DNS standard port

def extract_domain(data):
    """Extracts the domain name from the raw DNS query packet."""
    try:
        domain = b""
        idx = 12 # DNS Question section starts here
        length = data[idx]
        while length != 0:
            domain += data[idx+1:idx+1+length] + b"."
            idx += 1 + length
            length = data[idx]
        return domain[:-1] # Remove trailing dot
    except:
        return b""

while True:
    try:
        gc.collect() # Prevent memory leaks
        data, addr = s.recvfrom(512)
        
        if len(data) < 12:
            continue
            
        domain = extract_domain(data)
        
        # Check if the domain matches our block list
        is_blocked = False
        for blocked in BLOCKED_DOMAINS:
            if blocked in domain:
                is_blocked = True
                break
                
        if is_blocked:
            print(f"🛑 BLOCKED: {domain.decode('utf-8')}")
            
            # Construct a DNS spoof reply pointing to 0.0.0.0
            packet = data[:2] + b"\x81\x83" + data[4:6] + data[4:6] + b"\x00\x00\x00\x00"
            packet += data[12:] # Append original question
            packet += b"\xc0\x0c" # Pointer to domain name
            packet += b"\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04\x00\x00\x00\x00" # TTL 60s, IP 0.0.0.0
            s.sendto(packet, addr)
            
        else:
            # Forward the query to the real upstream DNS server
            forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            forward_sock.settimeout(2)
            try:
                forward_sock.sendto(data, (UPSTREAM_DNS, 53))
                reply, _ = forward_sock.recvfrom(512)
                s.sendto(reply, addr)
            except:
                pass
            finally:
                forward_sock.close()
                
    except Exception as e:
        # Prevent the script from crashing on bad network packets
        pass

