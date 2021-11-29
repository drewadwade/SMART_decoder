

# SMART_decoder.py takes image file QR codes and decodes the SMART Health Card data in them

import base64
import cv2
import re
import sys
import zlib

from pyzbar.pyzbar import decode

# Define the usage message for display on failed attempts and exit the program
def usage():
    print("")
    print("usage: python3 SMART_decoder.py <inputfile>")
    print("SMART decoder takes image file QR codes and decodes the SMART Health Card data in them")
    print("")
    print("positional arguments:")
    print("  inputfile                provide the filename of the QR code image file")
    print("")
    exit()

def decodeSHC(data):
  missing_padding = len(data) % 4
  if missing_padding:
      data += str(b'='* (4 - missing_padding))
  return base64.urlsafe_b64decode(data)


# Check for valid input file
try:
    inputfile=sys.argv[1]
    SHC_data = ((decode(cv2.imread(inputfile)))[0][0]).decode('utf-8')
except:
    print("Error: Input file could not be accessed.")
    usage()

print("The SMART Health Card data encoded in the QR code is:")
print(SHC_data)
print("")

# Increment all of the SHC 2-digit numbers by 45 to get the ASCII data for the JWS
pairs = re.findall('..', SHC_data[5:])
jws = ""
for pair in pairs:
  jws += chr(int(pair)+ 45)

# URL-safe base64 decode the ASCII data and split the JWS into header and data components
jws_parts = list(map(decodeSHC, jws.split(".")))

# Decompress the Proof of Vaccination data portion
proof_data = zlib.decompress(jws_parts[1], wbits=-15)

print("The JSON Web Secret encoded in the SHC data is:")  
print(jws)
print ("")

print("The JSON Web Secret header is:")  
print(jws_parts[0].decode('utf-8'))
print ("")

print("The Proof of Vaccination data contained in the JSON Web Secret is:")
print(proof_data.decode('utf-8'))
print ("")

print("The JSON Web Secret signature is:")  
print(jws_parts[2].decode('latin1'))
print ("")




#eyJ6aXAiOiJERUYiLCJhbGciOiJFUzI1NiIsImtpZCI6ImhvRE5VTDVZUzBGN1M4MmtGa25meDJwZkFQTE9sVWNtZkJoMlV0UlBVcG8ifQ.7VPbbtNAEP0VtLw6viUktd9K0wcQtEgEpArlYbMeJwt7sfZiEaL8OzN2Slv1wjMSL5Z298yZc-aMD0x6z2q2C6HzdZZ1vUg9uF4KSPfxhzWp4FkAHzLERXAsYWbTsrqYTxfF_E1RTdNZlbBesPrAwr4DVn_7Q-Y1d2EHXIUd0rjGvx4PEzog0_M4qXU08hcP0poXgcL2sikqtk6YcNCACZKrz3HzHUQgSe1Ouq_gPPHUbJbmaYF8dPs2mkYBYRx4G52A1SCfnR6Skx0mrFLINirBBm6PHpE5KvXFKQTc1tc5Am4PTxB_QjtYTyPkGkYSrqVCPra8vsT7rezB0ATfn19dsvURXW0kOl7yQARFdZZPinxSztjxmDwpoXhZwruHc-1OigZgCw4MVd03dEyYhsAJ4UFEJ8Po3u99AH1vcR5Fk2EQ2ELYZmh8_qFIS3ZcI2HPhZAGLoaXAyGk2T5mRdKdWqTWbTPKK_OyyUT_846zzBcjoRWobBBPg1pJPb6WxSSfTvI5VigbrqLe4P7WbJrn-aycV2c0AHCtdZrusT0XwTqS1EjfKU653KySVxfc8IbjyDEOH3iIftgK3SkIQHusuYktFkcHQ7kc9rCV4-mvpvRgqucqku6P10ts9Vy-5f98H-Q7o5_hn8x3TZ_f.u8wfmG572bt4EQBZI__JAqtIMeQbi-VMnPaRZFgbdKGfBfLgBuqV_LnOKg25XwjMXYZ9OX55T66gE4dJ1VsmMA