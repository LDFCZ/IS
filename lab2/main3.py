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


def tea_hash(data, key):
    # Инициализация хеша
    hash_value = 0

    # Проход по данным блоками
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        
        # Добавление блока данных к хешу с использованием TEA-шифра
        block_hash = int.from_bytes(block, byteorder='big')
        hash_value ^= block_hash
        hash_value ^= int.from_bytes(tea_encrypt(block, key), byteorder='big')

    return hash_value

def main():

    key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'  # 128-битный ключ
    data = input("Введите строку для шифрования: ").encode()

    hash_result = tea_hash(data, key)
    print(f'Hash result: {hash_result}')


if __name__ == "__main__":
    main()