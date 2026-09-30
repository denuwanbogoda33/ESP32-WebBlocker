# ESP32-WebBlocker

> 🛑 A lightweight DNS-based website blocker powered by an ESP32 and MicroPython.

**ESP32-WebBlocker** turns an ESP32 into a small, local DNS filtering device. It listens for DNS requests from devices on your network, checks requested domains against a configurable blocklist, and either blocks the request or forwards it to an upstream DNS server.

The concept is simple:

```text
ESP32 → DNS Request → Check Blocklist → Block or Forward
```

No dedicated Raspberry Pi, computer, or expensive network appliance is required.

---

## ✨ Features

* 🛑 Block selected domains using DNS
* ⚡ Runs directly on an ESP32
* 🐍 Written entirely in MicroPython
* 🌐 Forwards allowed DNS requests to Cloudflare DNS
* 📡 Works with devices connected to the same network
* 💾 Lightweight and suitable for low-resource hardware
* 🔧 Simple domain blocklist configuration
* 🖥️ Displays blocked requests in the MicroPython terminal
* 🧩 No external Python packages required

---

## 🧠 How It Works

ESP32-WebBlocker operates as a small DNS server running directly on your ESP32.

Normally, a device asks a DNS server:

```text
"What IP address belongs to youtube.com?"
```

With ESP32-WebBlocker, the request can instead go through your ESP32:

```text
Device
   │
   │ DNS request
   ▼
ESP32-WebBlocker
   │
   ├── 🚫 Blocked domain?
   │       │
   │       └── Yes → Return 0.0.0.0
   │
   └── No → Forward to 1.1.1.1
                │
                ▼
          Cloudflare DNS
```

### 🚫 Blocked Request

```text
youtube.com
      ↓
ESP32-WebBlocker
      ↓
🚫 BLOCKED
      ↓
0.0.0.0
```

### ✅ Allowed Request

```text
example.com
      ↓
ESP32-WebBlocker
      ↓
1.1.1.1
      ↓
Real DNS response
      ↓
Device
```

In other words, the ESP32 acts as a tiny DNS filtering proxy.

---

## 🛠️ Hardware

### Required

* ESP32 development board
* USB cable
* Computer running MicroPython / Thonny
* Wi-Fi network

That's it.

The ESP32 does not need additional sensors, displays, relays, or other hardware.

---

# 📦 Installation

## 1. Install MicroPython

Flash MicroPython onto your ESP32 if you haven't already.

You can use tools such as:

* [Thonny](https://thonny.org/)
* `esptool`
* Any other MicroPython-compatible workflow

---

## 2. Create `main.py`

Create a file named:

```text
main.py
```

Copy the ESP32-WebBlocker code into it.

---

## 3. Configure Wi-Fi

Find these lines:

```python
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

Replace them with your Wi-Fi credentials.

For example:

```python
WIFI_SSID = "MyWiFi"
WIFI_PASSWORD = "MyPassword"
```

> ⚠️ Keep your Wi-Fi password private. Do not commit your real credentials to GitHub.

---

## 4. Upload to the ESP32

Upload `main.py` to the ESP32 filesystem using Thonny or another MicroPython tool.

Then restart the ESP32.

You should see something similar to:

```text
Connecting to Wi-Fi...
Connected! ESP32 IP Address: 192.168.1.50

👉 Set this IP address as the primary DNS server
   in your router or device settings.
```

Take note of the ESP32's IP address.

---

# 🌐 Configure DNS

For ESP32-WebBlocker to filter DNS requests, devices need to use the ESP32 as their DNS server.

For example, if the ESP32 receives:

```text
192.168.1.50
```

set the device's DNS server to:

```text
192.168.1.50
```

You can configure this on:

* 📱 Android / iOS
* 💻 Windows
* 🐧 Linux
* 🍎 macOS
* 📡 Your router

### Router Configuration

If your router supports custom DNS configuration, you can configure the ESP32 as the DNS server for the network.

This allows devices using that router to automatically send their DNS queries through ESP32-WebBlocker.

> ⚠️ Router behavior varies by manufacturer. Some routers do not allow custom LAN DNS servers.

---

# 🚫 Configuring Blocked Domains

The blocklist is controlled by:

```python
BLOCKED_DOMAINS = [
    b"youtube.com",
    b"://youtube.com",
    b"youtube.lk",
    b"www.youtube.lk"
]
```

You can add additional domains to the list.

For example:

```python
BLOCKED_DOMAINS = [
    b"youtube.com",
    b"youtube.lk",
    b"example.com",
    b"example.org"
]
```

The ESP32 checks incoming DNS queries against this list.

---

# 🖥️ Monitoring

ESP32-WebBlocker prints blocked requests to the MicroPython terminal.

Example:

```text
🛑 BLOCKED: youtube.com
🛑 BLOCKED: www.youtube.lk
```

This allows you to see when the ESP32 is actively filtering DNS requests.

---

# 🔐 DNS Architecture

ESP32-WebBlocker uses two different paths depending on the requested domain.

### 🚫 Blocked Domains

```text
Client
  │
  │ DNS query
  ▼
ESP32-WebBlocker
  │
  └── Blocklist match
          │
          ▼
      0.0.0.0
```

### ✅ Allowed Domains

```text
Client
  │
  │ DNS query
  ▼
ESP32-WebBlocker
  │
  ▼
1.1.1.1
  │
  ▼
DNS response
  │
  ▼
Client
```

This gives the ESP32 a simple decision-making layer between the client and the upstream DNS server.

---

# ⚙️ Configuration

At the top of `main.py`, you can configure the main settings:

```python
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

UPSTREAM_DNS = "1.1.1.1"

BLOCKED_DOMAINS = [
    b"youtube.com",
    b"youtube.lk",
    b"www.youtube.lk"
]
```

### Upstream DNS

The default upstream resolver is:

```text
1.1.1.1
```

This is Cloudflare's public DNS resolver.

You can change it to another DNS server if required.

---

# 🧪 Example

Suppose your blocklist contains:

```python
BLOCKED_DOMAINS = [
    b"youtube.com"
]
```

A device requests:

```text
youtube.com
```

The ESP32 detects the domain and returns:

```text
0.0.0.0
```

The device therefore does not receive the normal DNS address for that domain.

Meanwhile, an allowed domain such as:

```text
github.com
```

is forwarded to:

```text
1.1.1.1
```

The DNS response is then returned to the requesting device.

---

# ⚠️ Important Limitations

ESP32-WebBlocker is intentionally simple.

It is a **DNS-based blocker**, not a full firewall or packet-filtering system.

## 🔒 HTTPS

Modern websites use HTTPS, so ESP32-WebBlocker does not inspect the actual encrypted webpage traffic.

Instead, it blocks the DNS resolution of selected domains.

---

## 🌐 Applications Can Use Other DNS Systems

Some applications and devices may use:

* DNS-over-HTTPS (DoH)
* DNS-over-TLS (DoT)
* Hardcoded DNS servers
* Other network mechanisms

These can potentially bypass a basic DNS-based filter.

---

## ▶️ YouTube Is More Complicated

YouTube is not a single domain.

Modern YouTube services can use multiple domains and infrastructure, while the YouTube mobile application may communicate with additional endpoints.

Therefore:

```text
youtube.com
```

being blocked does **not necessarily mean that every YouTube-related request will be blocked**.

---

## 🧱 Not a Complete Network Firewall

ESP32-WebBlocker should be considered a lightweight DNS filtering experiment rather than a replacement for dedicated network-filtering solutions such as:

* Pi-hole
* AdGuard Home
* Enterprise firewalls
* Dedicated router filtering
* Parental-control gateways

---

# 📁 Project Structure

```text
ESP32-WebBlocker/
│
├── main.py
├── README.md
└── LICENSE
```

Simple by design.

---

# 🚀 Future Ideas

ESP32-WebBlocker could eventually evolve into a much more capable network-filtering platform.

Potential improvements include:

* 📋 Larger blocklists
* 🌐 Web-based configuration panel
* 📊 DNS request statistics
* 🟢 Allowlist support
* 🔴 Blocklist management through a browser
* 💾 Persistent configuration
* ⏱️ Scheduled blocking
* 👨‍👩‍👧 Device-specific rules
* 📱 Mobile-friendly dashboard
* 🧠 Category-based filtering
* 🔄 Automatic blocklist updates
* 📈 Network activity graphs
* 🔒 DNS-over-TLS forwarding
* 📡 ESP32 access-point mode
* 🏠 Local hostname management

---

# 🤝 Contributing

Contributions, improvements, bug fixes, and ideas are welcome!

If you find a bug or have an idea for a feature, feel free to:

1. Open an issue
2. Describe the problem or idea
3. Submit a pull request if you have a fix or improvement

---

# ⚖️ Disclaimer

ESP32-WebBlocker is provided for educational and experimental purposes.

Use it only on networks and devices that you own or are authorized to administer.

The project is designed to demonstrate DNS filtering, networking, and embedded systems concepts on resource-constrained hardware.

---

# 📜 License

This project is open source under MIT LICENSE.

See the repository's `LICENSE` file for licensing details.

---

# ⭐ ESP32-WebBlocker

A tiny ESP32.

A little MicroPython.

A DNS server.

And suddenly your microcontroller is doing network administration. 💀

**Built with ❤️, MicroPython, and an ESP32.**
