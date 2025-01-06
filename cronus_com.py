#instalar o pyusb
#pip install pyusb

import usb.core
import sys
import os
from pathlib import Path

VENDOR_ID = 0x2008
PRODUCT_ID = 0x10

data = bytearray(64)
b0 = bytearray(64)
e6 = bytearray(64)
f0 = bytearray(64)
f1 = bytearray(64)
fa = bytearray(64)
fb = bytearray(64)

b0[:4] = [176, 0, 0, 1]
f0[:4] = [240, 0, 0, 1] #versão do firmware
f1[:4] = [241, 0, 0, 1] #serial do cronus


output_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(output_dir, "data")
if not Path(output_dir).exists(): os.mkdir(output_dir)

# Finding a USB HID device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if not dev:
    print("Dispositivo não encontrado")
    sys.exit()

dev.set_configuration()

dev.write(1, bytes(f0))

data = [0]

while data:
    try:
        data = dev.read(0x81, 64)  # Lê 64 bytes do endpoint
        if data:
            ascii = [chr(num) for num in data]
            hex = [f"{byte:02X}" for byte in data]

            for i in range(0, len(hex), 16):
                print(" ".join(hex[i:i+16]) +" | "+" ".join(ascii[i:i+16]))

            print()

    except usb.core.USBError as e:
        if e.errno == 110 or e.errno == 10060:  # Erro de timeout (se você esperar dados)
            print("Timeout: Nenhum dado disponível")
            if f: f.close
            break
        else:
            raise  # Levanta o erro se não for um timeout

if f: f.close
