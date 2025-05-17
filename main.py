import network
import time
import json
import socket
import machine
import os
import gc
import urequests
from machine import UART,Pin
import time
from tnxinterpreter import interpreter

lcd1=Pin(32,Pin.OUT)
lcd2=Pin(33,Pin.OUT)
avrres=Pin(25,Pin.OUT)
lcd1.value(1)
lcd2.value(1)
uart = UART(1, baudrate=115200, tx=17, rx=16)
lcd=False
def get_device_info():
    wlan = network.WLAN(network.STA_IF)
    mac = ':'.join('{:02x}'.format(b) for b in wlan.config('mac'))
    ip = wlan.ifconfig()[0]
    cpu_freq = machine.freq() // 1000000
    free_heap = gc.mem_free()
    used_heap = gc.mem_alloc()
    uptime = time.ticks_ms() // 1000
    reset_cause = machine.reset_cause()

    info = f"""
ESP32 Device Info:
MAC Address: {mac}
IP Address: {ip}
CPU Frequency: {cpu_freq} MHz
Free Heap: {free_heap} bytes
Used Heap: {used_heap} bytes
Uptime: {uptime} seconds
Reset Cause: {reset_cause}
"""
    return info

def rm(path, conn):
    if path in os.listdir('.'):
        try:
            os.remove(path)
            conn.send(b"file removed")
        except OSError:
            try:
                os.rmdir(path)
                conn.send(b"folder removed")
            except Exception as e2:
                conn.send(("Error: " + str(e2)).encode('utf-8'))
    else:
        conn.send(b"file is unavailable")

def http(mt, url, conn, headers=None, dta=None):
    try:
        if mt == 1:
            r = urequests.get(url, headers=headers)
        elif mt == 2:
            r = urequests.post(url, headers=headers, data=json.dumps(dta))
        elif mt == 3:
            r = urequests.delete(url, headers=headers, data=json.dumps(dta))
        elif mt == 4:
            r = urequests.put(url, headers=headers, data=json.dumps(dta))
        else:
            conn.send(b"Unsupported HTTP method\n")
            return
        conn.send(r.text.encode('utf-8'))
        r.close()
    except Exception as e:
        conn.send(("HTTP Error: " + str(e)).encode('utf-8'))

def usendim(data, conn):
    parts = data.split(" ")
    try:
        mt = int(parts[parts.index("/m") + 1])
        url = parts[parts.index("/u") + 1]

        header = {"User-Agent": "MyMicroPythonAgent/1.0"}
        if "/h" in parts:
            h_index = parts.index("/h") + 1
            header = json.loads(parts[h_index])

        dta = {}
        if "/d" in parts:
            d_index = parts.index("/d") + 1
            dta = json.loads(parts[d_index])

        if not (url.startswith("http://") or url.startswith("https://")):
            conn.send(b"Error: Invalid URL")
        else:
            http(mt, url, conn, headers=header, dta=dta)

    except Exception as e:
        conn.send(("Command parsing error: " + str(e)).encode('utf-8'))

# --------------------- ANA PROGRAM BAŞLANGICI ---------------------

with open("config.json", "r") as config:
    cfg = json.load(config)
ssid = cfg["ntwn"]
password = cfg["ntky"]
print(f"WiFi Name: {ssid}")
print(f"WiFi Password: {password}")

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    print("Connecting to WiFi...")
    time.sleep(1)

print(f'Connected, IP address: {wifi.ifconfig()[0]}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 4545))
s.listen(1)
print("TCP server listening on port 4545")
conn, addr = s.accept()
print('Connection from', addr)

nf = get_device_info()
conn.send(nf.encode('utf-8'))

while True:
    try:
        data = conn.recv(1024)
        if data and not lcd:
            data = data.decode('utf-8').strip()
            print(f"Received: {data}")
            try:
                if data == "rst":
                    conn.send(b'ok')
                    conn.close()
                    lcd1.value(0)
                    lcd2.value(0)
                    avrres.value(0)
                    time.sleep(100)
                    avrres.value(1)
                    print("Resetting device...")
                    machine.reset()
                elif data == "ls":
                    files = os.listdir('.')
                    conn.send(str(files).encode('utf-8'))
                elif data.startswith("cd "):
                    os.chdir(data.split(' ')[1])
                elif data.startswith("mkdir "):
                    os.mkdir(data.split(' ')[1])
                elif data.startswith("mkfile "):
                    _, rest = data.split(' ', 1)
                    filename, content = rest.split('>>', 1)
                    if filename.strip() not in os.listdir('.'):
                        with open(filename.strip(), 'w') as f:
                            f.write(content)
                        conn.send(b'File created')
                    else:
                        conn.send(b'file already available')
                elif data.startswith("cat "):
                    filename = data.split(' ')[1]
                    if filename not in os.listdir('.'):
                        conn.send(b'file is not available')
                    else:
                        with open(filename, "r") as f:
                            conn.send(f.read().encode('utf-8'))
                elif data.startswith("rmfile "):
                    rm(data.split(' ')[1], conn)
                elif data.startswith("http "):
                    usendim(data, conn)
                elif data == "ser":
                    lcd=True
                    conn.send(b'ser mode open(notice:serial mode cominication on arduıno uno)')
                elif data.startswith("runtnx"):
                    interpreter(data.split(' ')[1],conn)
                else:
                    conn.send(b'Unknown command')
            except Exception as e:
                conn.send(("Command parsing error: " + str(e)).encode('utf-8'))

                
        elif data and lcd:
            uart.write(data + b'\n')  # Doğru kullanım burada
            start = time.ticks_ms()
            while True:
                if time.ticks_diff(time.ticks_ms(), start) >= 5000:
                    conn.send(b'avr not responding')
                    break
                if uart.any():
                    cevap = uart.read()
                    if cevap:
                        conn.send(cevap)
                        break
    except Exception as e:
        print("Error:", e)
        break

