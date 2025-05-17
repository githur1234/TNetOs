#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd1(0x26, 16, 2);
LiquidCrystal_I2C lcd2(0x25, 16, 2);
struct CustomChar {
  String name;
  byte data[8];
};

CustomChar customChars[8]; // En fazla 8 adet
int customCharCount = 0;

int findCustomCharIndex(String name) {
  for (int i = 0; i < customCharCount; i++) {
    if (customChars[i].name == name) return i;
  }
  return -1;
}

void addOrUpdateCustomChar(String name, byte data[8], LiquidCrystal_I2C* lcd) {
  int idx = findCustomCharIndex(name);
  if (idx == -1) {
    if (customCharCount >= 8) {
      Serial.println("Maksimum 8 özel karakter olabilir.");
      return;
    }
    idx = customCharCount++;
  }
  customChars[idx].name = name;
  memcpy(customChars[idx].data, data, 8);
  lcd->createChar(idx, data);
  Serial.println("Özel karakter tanımlandı: " + name + " (index " + String(idx) + ")");
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  lcd1.init();
  lcd1.backlight();

  lcd2.init();
  lcd2.backlight();

  Serial.println("Hazırım.");
}

void loop() {
  if (Serial.available()) {
    String komut = Serial.readStringUntil('\n');
    komut.trim();

    islemYap(komut);
  }
}

void islemYap(String komut) {
  int space1 = komut.indexOf(' ');
  if (space1 == -1) return;

  String hedef = komut.substring(0, space1);
  String geriKalan = komut.substring(space1 + 1);

  int space2 = geriKalan.indexOf(' ');
  String islemtipi;
  String parametre;
  if (space2 == -1) {
    islemtipi = geriKalan;
    parametre = "";
  } else {
    islemtipi = geriKalan.substring(0, space2);
    parametre = geriKalan.substring(space2 + 1);
  }

  LiquidCrystal_I2C *lcd = nullptr;
  if (hedef == "lcd1") lcd = &lcd1;
  else if (hedef == "lcd2") lcd = &lcd2;
  else return;

  if (islemtipi == "init") {
    lcd->init();
    lcd->backlight();
    Serial.println(hedef + " init yapıldı.");
  }
  else if (islemtipi == "clear") {
    lcd->clear();
    Serial.println(hedef + " temizlendi.");
  }
  else if (islemtipi == "print") {
    lcd->print(parametre);
    Serial.println(hedef + " yazıldı: " + parametre);
  }
  else if (islemtipi == "backlight") {
    if (parametre == "on") lcd->backlight();
    else if (parametre == "off") lcd->noBacklight();
    Serial.println(hedef + " backlight " + parametre);
  }
  else if (islemtipi == "setcursor") {
    int space3 = parametre.indexOf(' ');
    if (space3 == -1) {
      Serial.println("Hatalı setcursor parametresi");
      return;
    }
    int col = parametre.substring(0, space3).toInt();
    int row = parametre.substring(space3 + 1).toInt();
    lcd->setCursor(col, row);
    Serial.println(hedef + " setCursor: " + String(col) + ", " + String(row));
  }
  else if (islemtipi == "write") {
  if (parametre.length() == 1) {
    lcd->write(parametre[0]);
    Serial.println(hedef + " write: " + parametre);
  } else {
    // İsimle özel karakter yazma
    int idx = findCustomCharIndex(parametre);
    if (idx != -1) {
      lcd->write(idx);
      Serial.println(hedef + " write özel karakter: " + parametre);
    } else {
      Serial.println("write: Karakter bulunamadı: " + parametre);
    }
  }
}
else if (islemtipi == "customchar") {
  // format: "isim hex0,hex1,hex2,...,hex7"
  int space3 = parametre.indexOf(' ');
  if (space3 == -1) {
    Serial.println("Hatalı customchar parametresi");
    return;
  }
  String name = parametre.substring(0, space3);
  String dataStr = parametre.substring(space3 + 1);
  byte charData[8];

  int start = 0;
  for (int i = 0; i < 8; i++) {
    int commaPos = dataStr.indexOf(',', start);
    String val;
    if (commaPos == -1 && i == 7) {
      val = dataStr.substring(start);
    } else if (commaPos != -1) {
      val = dataStr.substring(start, commaPos);
      start = commaPos + 1;
    } else {
      Serial.println("customchar veri eksik");
      return;
    }
    val.trim();
    if (val.startsWith("0x") || val.startsWith("0X")) {
      charData[i] = (byte) strtol(val.c_str(), NULL, 16);
    } else {
      charData[i] = (byte) val.toInt();
    }
  }
  addOrUpdateCustomChar(name, charData, lcd);
}

  else {
    Serial.println("Bilinmeyen komut: " + islemtipi);
  }
}
