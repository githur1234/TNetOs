# 🛰️ TNetOs

**TNetOs**, ESP32 için geliştirilen, MicroPython tabanlı bir beta işletim sistemidir.

## ⚙️ Kurulum Adımları

### 🔹 MicroPython Kurulumu
ESP32 için MicroPython firmware’ini [buradan](https://micropython.org/download/ESP32_GENERIC/) indirip yükleyin.

### 🔹 Python Kurulumu
Python'un [resmi web sitesinden](https://www.python.org/downloads/) **Python 3.13.3** sürümünü indirip kurmanızı öneririz.

### 🔹 Thonny IDE Kurulumu
[Thonny IDE](https://thonny.org/)’yi indirerek kurun.

## 🛠️ TNetOs Yükleme

1. Depoyu `git clone` ile ya da `.zip` olarak indirip çıkarın.
2. `con.py` dosyasını dışarıya alın. (Bu dosya, ESP32'ye TCP üzerinden bağlanıp komut çalıştırmanızı sağlar.)
3. `avr.ino` dosyasını isterseniz Arduino IDE üzerinden bir Arduino karta yükleyin (isteğe bağlı). Bu sayede GPIO pinlerini Arduino üzerinden yönetebilirsiniz.
4. Thonny IDE’yi açın:
    - **Tools > Options > Interpreter**
    - **MicroPython (ESP32)** seçeneğini seçin.
5. REPL ekranı geldikten sonra aşağıdaki kodu yapıştırarak LED testini gerçekleştirin:

    ```python
    from machine import Pin
    import time

    led = Pin(2, Pin.OUT)

    while True:
        led.value(0)
        time.sleep(1)
        led.value(1)
        time.sleep(1)
    ```

6. Kod çalışıyorsa, diğer dosyaları ESP32’ye yükleyin.
7. `config.json` dosyasını açın ve aşağıdaki alanları kendi Wi-Fi bilgilerinize göre güncelleyin:

    ```json
    {
      "ntky": "WIFI_ŞİFREN",
      "ntwn": "WIFI_ADIN"
    }
    ```

8. Tüm dosyaları kaydedin (`Ctrl + S`).

## ▶️ TNetOs'u Çalıştırma

1. REPL terminaline şu komutu yazın:

    ```python
    import machine
    machine.reset()
    ```

2. Terminal ekranında şu satırları görmelisiniz:

    ```
    connecting to wifi...
    IP Address: 192.168.x.xx
    ```

3. `con.py` dosyasını çalıştırın ve gelen satıra ESP32'nin IP adresini yazın:

    ```
    esp32 ip >> 192.168.x.xx
    ```

ESP32’ye bağlandığınızda sistem size bazı genel bilgiler verir. Artık içindeki araçları kullanabilirsiniz.

> **Not:** Araçlar burada belirtilmemiştir.
