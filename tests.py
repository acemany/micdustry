from base64 import b64encode, b64decode

str1=b"bHtY7u"

def benc(string:str):
    try:
        return b64encode(string.encode("utf-8"))
    except:
        return "bruh"
def bdec(b64:bytes):
    try:
        return b64decode(b64)
    except:
        return "bruh"

print(f"\n{bdec(str1)}\n")
