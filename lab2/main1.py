def init_rc4(key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_crypt(data, key):
    S = init_rc4(key)
    i = 0
    j = 0
    output = bytearray()

    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        output.append(byte ^ k)

    return bytes(output)

def main():
    key = input("Введите ключ: ")
    plaintext = input("Введите строку для шифрования: ").encode()
    
    encrypted_data = rc4_crypt(plaintext, key.encode())
    print("Зашифрованная строка:", encrypted_data.hex())

    decrypted_data = rc4_crypt(encrypted_data, key.encode())
    print("Расшифрованная строка:", decrypted_data.decode())

if __name__ == "__main__":
    main()