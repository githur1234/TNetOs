# TNetOs
TNetOs esp32 mcropython tabanlı beta işletim sistemi 

# Kullanım
## micropython kurulum
  micropython esp32 için kurun [buradan](https://micropython.org/download/ESP32_GENERIC/) kurulum sayfasına gidebilirsiniz
## python kurulum
  Pythonu resmi sitesinden python 3.13.3 ü kurmanızı öneriririz
## Thonny ıde kurun
  Thonny ıdeyi [buradan](https://thonny.org/) indirebilirsiniz
## TNetOs kurulum
  git ile veya zip ile indirerek depoyu kurun
  zip ile indirdiyseniz zipi ayıklayın
  con.py dosyasını çıkarın(bu esp32 ye tcp ile bağlanarak komut çalıştırmanızı sağlar)
  kalan dosyalardan avr.ino yu da arduıno ıde ile arduınoya kurun (zorunlu değil ama gpıo pinlerini esp32 arduıno üzerinden yönetir kodu optimize edebilirsiniz)
  Thnonny ıdeyi açın ve Tool>Options>ınterpreter>Micropython (esp32) seçin
  repl ekranı gelmesi gerekir test için bu kodu yapıştırın:
  '''python
   from machine import Pin
   import time
   led=Pin(2,Pin.OUT)
   while True:
    led.value(0)
    time.sleep(1)
    led.value(1)
    time.sleep(1)
  bu kod esp32 içindeki dahili mavi ledi yanıp söndürür
  eğer çalıştıysa diğer dosyaları  esp32 nin içine atın 
  config.json daki ntky yi kendi ağ şifrenle
  ntwn yi kendi ağ adınla değiştir
  sonra  ctr+s ile dosyları kayıt edin 
## çalıştırma
 repl terminalinde bu komudu çalıştırın:'import machine;machine.reset()'
 bu esp32 ye soft reset atar attıktan sonra terminal ekranında kendi ağ adın ve şifren yazar 
 wifiya bağlanana kadar 'connecting to wifi...' shell ekranında gözükür
 bağlandığı zaman 'IP Adress:192.168.x.xx' yazar
 başta verilen conn.py ı çalıştırın 'esp32 ıp>>' yazan yere esp32 nin ıpsini yazın 
 eğer bağlandıysa esp32 nin genel bir ınfosunu size yazdırır
 ve bu kadar artık esp32 nin içindeki araçları kullanabilirsiniz(Not:araçlar burada belirtilmemiştir)
