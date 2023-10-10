# Реализация TEA (Tiny Encryption Algorithm)

def string_to_bytes(s):
    return bytes(s, encoding='utf-8')

def bytes_to_string(b):
    return b.decode('utf-8')

def pad_message(message):
    # Дополним сообщение до кратного 8 байтам (64 битам)
    pad_length = 8 - (len(message) % 8)
    padding = bytes([pad_length] * pad_length)
    return message + padding

def unpad_message(padded_message):
    # Удалим дополнение
    pad_length = padded_message[-1]
    return padded_message[:-pad_length]

def tea_encrypt(plain_text, key):
    v0, v1 = int.from_bytes(plain_text[:4], byteorder='big'), int.from_bytes(plain_text[4:], byteorder='big')
    k0, k1, k2, k3 = int.from_bytes(key[:4], byteorder='big'), int.from_bytes(key[4:8], byteorder='big'), int.from_bytes(key[8:12], byteorder='big'), int.from_bytes(key[12:], byteorder='big')
    delta = 0x9e3779b9
    sum = 0

    for _ in range(32):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF

    return v0.to_bytes(4, byteorder='big') + v1.to_bytes(4, byteorder='big')

def tea_decrypt(cipher_text, key):
    v0, v1 = int.from_bytes(cipher_text[:4], byteorder='big'), int.from_bytes(cipher_text[4:], byteorder='big')
    k0, k1, k2, k3 = int.from_bytes(key[:4], byteorder='big'), int.from_bytes(key[4:8], byteorder='big'), int.from_bytes(key[8:12], byteorder='big'), int.from_bytes(key[12:], byteorder='big')
    delta = 0x9e3779b9
    sum = (delta * 32) & 0xFFFFFFFF

    for _ in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        sum = (sum - delta) & 0xFFFFFFFF

    return v0.to_bytes(4, byteorder='big') + v1.to_bytes(4, byteorder='big')

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        plain_text = f.read()
        padded_message = pad_message(plain_text)
        cipher_text = b''

        for i in range(0, len(padded_message), 8):
            block = padded_message[i:i + 8]
            encrypted_block = tea_encrypt(block, key)
            cipher_text += encrypted_block

    with open(output_file, 'wb') as f:
        f.write(cipher_text)

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        cipher_text = f.read()
        plain_text = b''

        for i in range(0, len(cipher_text), 8):
            block = cipher_text[i:i + 8]
            decrypted_block = tea_decrypt(block, key)
            plain_text += decrypted_block

        unpadded_message = unpad_message(plain_text)

    with open(output_file, 'wb') as f:
        f.write(unpadded_message)


def main():
    key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'  # 128-битный ключ
    input_file = 'test.txt'
    encrypted_file = 'encrypted_file.txt'
    decrypted_file = 'decrypted_file.txt'

    # Шифрование файла
    encrypt_file(input_file, encrypted_file, key)

    # Расшифрование файла
    decrypt_file(encrypted_file, decrypted_file, key)


if __name__ == "__main__":
    main()