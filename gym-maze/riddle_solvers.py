from scapy.all import *
from scapy.layers.dns import DNS
from scapy.layers.inet import TCP
from amazoncaptcha import AmazonCaptcha
import numpy as np
from tempfile import TemporaryFile
from PIL import Image
import time



from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP
import base64
import jwt
import json
import pathlib
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from jwcrypto import jwk
from io import BytesIO

#old cipher
# def cipher_solver(str):
#     #print("Cipher ",str)
#     str += '=' * (-len(str) % 4)
#     decoded_str = base64.b64decode(str)
#     decoded_str_utf = decoded_str.decode("utf-8")

#     # print(decoded_str_utf)
#     key = decoded_str_utf.split(",")[1]
#     to_code = decoded_str_utf.split(",")[0]
#     to_code = to_code[1:]
#     binary_key = key.split(")")[0]
#     dec_key = int(binary_key, 2)
#     # print(to_code)
#     count = 0
#     temp = "0"
#     list_of = []
#     for i in to_code:
#         if count == 7:
#             list_of.append(temp)
#             count = 1
#             temp = "0" + i
#         else:
#             temp = temp + i
#             count += 1
#     list_of.append(temp)

#     # print(list_of)

#     result = "".join(list_of)
#     # print(result)

#     input_string = int(result, 2);

#     bytes = (input_string.bit_length() + 7) // 8
#     input_array = input_string.to_bytes(bytes, "big")
#     value = input_array.decode()
#     # print(ASCII_value)
#     shifted_string = ""


#     for char in value:
#         char_code = ord(char)
#         if 65 <= char_code <= 90:
#             shifted_code = ((char_code - 65)-dec_key)% 26 + 65
#         elif 97 <= char_code <= 122:
#             shifted_code = ((char_code - 97)-dec_key) % 26+97
#         shifted_char = chr(shifted_code)
#         shifted_string += shifted_char
#     #print(shifted_string)
#     return shifted_string
#     pass

# new cipher

def cipher_solver(str):
    str += '=' * (-len(str) % 4)
    decoded_str = base64.b64decode(str)
    decoded_str_utf = decoded_str.decode("utf-8")

    # print(decoded_str_utf)
    key = decoded_str_utf.split(",")[1]
    to_code = decoded_str_utf.split(",")[0]
    to_code = to_code[1:]
    binary_key = key[:-1]

    dec_key = int(binary_key, 2)
    result = ""


    for i in range(0, len(to_code), 7):
        res = '0'+to_code[i:i+7]
        result += res

    input_string = int(result, 2)

    bytes = (input_string.bit_length() + 7) // 8
    input_array = input_string.to_bytes(bytes, "big")
    value = input_array.decode()
    shifted_string = ""


    for char in value:
        char_code = ord(char)
        if 65 <= char_code <= 90:
            shifted_code = ((char_code - 65)-dec_key)% 26 + 65
        elif 97 <= char_code <= 122:
            shifted_code = ((char_code - 97)-dec_key) % 26+97
        shifted_char = chr(shifted_code)
        shifted_string += shifted_char
    return shifted_string

# old captcha
# def captcha_solver(str):
#     print("Captcha")
#     q=np.array(str)
#     img = Image.fromarray(q)
#     #print(img)
#     file = TemporaryFile()
#     img.save(file, "PNG")
#     #print(file)
#     captcha = AmazonCaptcha(file)
#     solution = captcha.solve()
#     #print(solution)
#     return solution
#     pass


#new captcha
def captcha_solver(str):
    q=np.array(str)
    img = Image.fromarray(q)
    img_in_bytes = io.BytesIO()
    img.save(img_in_bytes, "PNG")
    captcha = AmazonCaptcha(img_in_bytes)
    solution = captcha.solve()
    return solution

# OLD PCAP
# def pcap_solver(question):
#     #print("Pcaaaaaaaaap",question)
#     decoded_file = base64.b64decode(question)
#     src_ip = "188.68.45.12"
#     packet = rdpcap(BytesIO(decoded_file))
#     filtered_packets = [packet for packet in packet if IP in packet and packet[IP].src == src_ip and packet.haslayer(DNS)]
#     query_names = []

#     for packet in filtered_packets:
#       if packet.haslayer(DNSQR):
#         dns_query = packet[DNSQR].qname.decode("utf-8")
#         str = dns_query.split(".")[1]
#         pos = dns_query.split('.')[0]
#         str += '=' * (-len(str) % 4)
#         pos += '=' * (-len(pos) % 4)
#         decoded_p = base64.b64decode(pos)
#         decoded_pos_u = decoded_p.decode("utf-8")
#         decoded_str = base64.b64decode(str)
#         decoded_str_utf = decoded_str.decode("utf-8")
#         query_names.append((decoded_pos_u, decoded_str_utf))

#     sorted_names = sorted(query_names)
#     second_elements = []
#     for pair in sorted_names:
#         second_elements.append(pair[1])
#     result = "".join(second_elements)
#     return result
#     pass

#NEW PCAP
def pcap_solver(question):
    print("pcap")
    decoded_file = base64.b64decode(question)
    src_ip = "188.68.45.12"
    packet = rdpcap(BytesIO(decoded_file))
    filtered_packets = [packet for packet in packet if IP in packet and packet[IP].src == src_ip and packet.haslayer(DNS)]
    query_names = {}

    for packet in filtered_packets:
      if packet.haslayer(DNSQR):
        dns_query = packet[DNSQR].qname.decode("utf-8")
        str = dns_query.split(".")[1]
        pos = dns_query.split('.')[0]
        str += '=' * (-len(str) % 4)
        pos += '=' * (-len(pos) % 4)
        decoded_p = base64.b64decode(pos)
        decoded_pos_u = int(decoded_p.decode("utf-8"))
        decoded_str = base64.b64decode(str)
        decoded_str_utf = decoded_str.decode("utf-8")
        query_names[decoded_pos_u]= decoded_str_utf

    sorted_names = sorted(query_names)
    sorted_dict = {key: query_names[key] for key in sorted_names}
    res=""
    for i in sorted_dict:
        res+=sorted_dict[i]
    return res
    pass



#def p_cap_decoder(file_path):
    

#print(p_cap_decoder("C:/Users/User/Downloads/YoUgOtThEsEcReT.pcap"))

def server_solver(str):
    print("Server")
    jwk1={
    "kty": "RSA",
    "e": "AQAB",
    "kid": "bc28409d-54f5-47b2-bb31-af9faeffe247",
    "n": "qA4QF67qzsdX2-6KHkuXDV899L-Pbhtfy3AbY78LkohtNMbeULoGRUJgr3rHbSZ5EdjvOsESfjT_dFecf7Du6aeKMiRZrowQs2ViBrLyKo0-krpvmHBGnv0bJtLjEDKMs7IXgaSfSXZXBq0hdBlJRHyaK4lwT3HpwgeWw6ZhNVaO5N05DUPBMmZyid3X4sF330jlGx4KPOcllcoq17PgiTa34QB9BjazpgkNI9YH7IXcHPd7sA56A-OMxEcawDQXVUdOGrEX7SqvM3KYvDSspchxrRMekVnaMFVnS_60zuQJDArK4h78nUeVerhu2UzOsRMcpH8mD-vl9i5-9q363w"
}
    pay_load = str.split(".")[1]
    pay_load += '=' * (-len(pay_load) % 4)
    decoded_pay_load = base64.b64decode(pay_load)
    decoded_pay_load_utf = decoded_pay_load.decode("utf-8")

    headr = str.split(".")[0]
    headr += '=' * (-len(headr) % 4)
    decoded_header = base64.b64decode(headr)
    decoded_header_utf = decoded_header.decode("utf-8")
    # text
    #print(decoded_pay_load_utf)

    header_data = json.loads(decoded_header_utf)
    pay_load_data = json.loads(decoded_pay_load_utf)
    # object
    header_data['jwk']=jwk1
    pay_load_data['admin'] = 'true'


    
    private_key='''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAqA4QF67qzsdX2+6KHkuXDV899L+Pbhtfy3AbY78LkohtNMbe
ULoGRUJgr3rHbSZ5EdjvOsESfjT/dFecf7Du6aeKMiRZrowQs2ViBrLyKo0+krpv
mHBGnv0bJtLjEDKMs7IXgaSfSXZXBq0hdBlJRHyaK4lwT3HpwgeWw6ZhNVaO5N05
DUPBMmZyid3X4sF330jlGx4KPOcllcoq17PgiTa34QB9BjazpgkNI9YH7IXcHPd7
sA56A+OMxEcawDQXVUdOGrEX7SqvM3KYvDSspchxrRMekVnaMFVnS/60zuQJDArK
4h78nUeVerhu2UzOsRMcpH8mD+vl9i5+9q363wIDAQABAoIBAAxd4iitmjrdAX9x
bNMkGRM5vIHu7M7Owq+Vg6mrhkSVhIL7O9XkWPZhly+indu2FpFN9Cc2Zc/iwrlD
HATR6arirAraxCMezIXSQpkfZvtJovhCMiWDsZ0c7BGt0cBZ4yLzSpAjcKAdZ/PZ
hRozJPVrI+wE2tgFyz/LgvhjA6+pUFRi2WX6E7x4TjIQW71V0BGVyIxoyct+PApg
yJoHA2pGZUXytLaQPj2vwKEMWGv8erYvXPavIA+Qk0V3DmQNO1B+txexMnG0hi4z
4OKVPQGZV4VzKSJPislKl3EpF9qNotnPbAImxugo1mzXC6jH+0WuO0a+Tvp0AKLt
YbwPnfkCgYEA16Cqh6WnkTLu7CyGmepeLyDyMhNkKUgfxbnEROo1ax61BKDRIOib
C7ER9bHQMXhw7oyQuijAl7jJOt9j4R/A9Vu+IC/kZ2cEo6Bgtxqb0EAU6rAQzBIc
Rj2BI2ew9OLR77NatpjwgWKpMLyYAOj2GQqLJURnnuqH6WX5fUq7iFkCgYEAx4Us
AAi+I2NsiImM2CoARlw39SUCd/MjEoSUTDzqOAF43V/gUSk9nYDf43OFZWRLhfMG
OoGCG/fC/gb4ZDAOsTMylOFqSJ2EYkMDaA8T/xsWFC1TVloyF1CZp79Z67O0AU7t
a49UokIqJ5vmmKh1Mnx1OE040eodVaex6/w7NfcCgYBOlRMQ1GI5HGLOV3vGZA9n
BY6+iSqbkNljacwJgYFuRIab5S/R2nOG00VEUUUaglZF2Zx0+50UrhdICVmRFc1w
nbqwaEPJG1Ype61DjcLzJid5UCkO9hqvzoJdsNBgrrjrrmWE3j/oJ1iZlmGfE0d8
4MbNEhzhYX+eo7dE3hNyIQKBgDctMPnhcRPATyeDQpwVIXZT0nXNAl3Bs5VPbOOY
hP1wCsjN1u8bBJsmJMR2EhH0Jp6okrRjVGP/pMEzlEXAtI90pSxfGlFynkW+WpbQ
dKs8BmMWFdHvp6Ki+5tUY723OLST6zyvqqwkuBu0FZVqIN8RZClp0ajbobkqYx3r
50QJAoGAN30mH5NFNi7Hl8Mz0ZkiHR2qf+/N0Vb8tDuo8B2si99gP/Pfsy0Eh9ng
3jcxJ5/RrblQxLfvosSyA+bQX3+54p1LY00JA/SqKhu60vaab/6TE7ybJnaTYfLP
A5PMZy8G8sXL6YjVVZTIrnh4mPjQN4C5DiYzR33W4iGPP6IHTAQ=
-----END RSA PRIVATE KEY-----'''
    ans=jwt.encode(payload=pay_load_data,key=private_key,algorithm='RS256',headers={"jwk": jwk1,"kid": "bc28409d-54f5-47b2-bb31-af9faeffe247"})
    #print(ans)
    return ans
    pass



