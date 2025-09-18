# IDS Lite (Python)

A lightweight Intrusion Detection System (IDS) prototype written in Python.  
It monitors incoming UDP traffic, detects packet bursts (possible DoS/DDoS behavior), and blocks abusive IPs temporarily.  

---

## 🔒 Cybersecurity Relevance
- Demonstrates core **network monitoring** and **traffic analysis** concepts.  
- Implements a basic form of **rate-limiting** to mitigate flood attacks.  
- Introduces ideas used in **IDS/IPS systems** like Snort and Suricata.  

---

## ⚙️ Features
- Monitors UDP packets on `127.0.0.1:9999`.  
- Logs all events to `events.log` using Python’s `logging` module.  
- Detects **bursts**: more than `N` packets in `T` seconds.  
- Automatically **blacklists** offenders for a configurable duration.  
- Drops packets from blacklisted IPs.  

---

## 🛠️ Tech Stack
- **Python 3**  
- **socket** (low-level networking)  
- **logging** (event tracking)  

---

## 🚀 How It Works
1. The script listens on `127.0.0.1:9999` for UDP packets.  
2. Tracks how many packets each IP sends in a sliding time window (`T` seconds).  
3. If the count exceeds threshold `N`, the IP is flagged as **suspicious** and blacklisted for `BAN_TIME` seconds.  
4. All events (packets, detections, drops) are logged into `events.log`.  

---

## 🔧 Usage
Clone the repo and run:

```bash
python ids_lite.py
```

Send test packets from another terminal:

```bash
# Normal traffic
echo "Hello" | nc -u 127.0.0.1 9999

# Flood traffic (triggers detection)
for i in {1..20}; do echo "Attack" | nc -u 127.0.0.1 9999; done
```

Check logs:

```bash
cat events.log
```
