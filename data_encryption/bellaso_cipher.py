class BellasoCipher:
    def __init__(self, key: str) -> None:
        self.key = key

    def _encrypt(self, plain_text: str, key: str) -> str:
        encrypted_text: list[str] = []
        key_length: int = len(key)
        for i, char in enumerate(plain_text):
            if char.isalpha():
                base: int = ord("A") if char.isupper() else ord("a")
                key_char: str = key[i % key_length].upper()
                key_shift: int = ord(key_char) - ord("A")
                encrypted_char: str = chr((ord(char) - base + key_shift) % 26 + base)
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)
        return "".join(encrypted_text)

    def encrypt(self, plain_text: str) -> str:
        return self._encrypt(plain_text, self.key)

    def decrypt(self, cipher_text: str) -> str:
        reversed_key: str = "".join(
            chr(
                (ord(k.upper()) - ord("A")) * -1 + ord("A")
            ) for k in self.key
        )
        return self._encrypt(cipher_text, reversed_key)


def main() -> None:
    key: str = "KEYWORD"
    cipher: BellasoCipher = BellasoCipher(key=key)
    plaintext: str = "Hello, World!"
    encrypted: str = cipher.encrypt(plaintext)
    decrypted: str = cipher.decrypt(encrypted)

    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")


if __name__ == "__main__":
    main()
