class CeasarCipher:
    def __init__(self, shift: int) -> None:
        self.shift = shift % 26  # Ensure the shift is within 0-25

    def _encrypt(self, plain_text: str, key: int):
        encrypted_text: list[str] = []
        for char in plain_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - base + key) % 26 + base)
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)
        return "".join(encrypted_text)
    
    def _decrypt(self, plain_text: str, key: int):
        reversed_key: int = -key
        return self._encrypt(plain_text, reversed_key)

    def encrypt(self, plain_text: str) -> str:
        return self._encrypt(plain_text, self.shift)

    def decrypt(self, ciphertext: str) -> str:
        return self._decrypt(ciphertext, self.shift)


def main() -> None:
    cipher: CeasarCipher = CeasarCipher(shift=3)
    plaintext: str = "Hello, World!"
    encrypted: str = cipher.encrypt(plaintext)
    decrypted: str = cipher.decrypt(encrypted)

    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")


if __name__ == "__main__":
    main()
