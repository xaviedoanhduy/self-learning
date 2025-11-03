from bellaso_cipher import BellasoCipher
from ceasar_cipher import CeasarCipher

def test_bellaso_cipher() -> None:
    key: str = "KEYWORD"
    cipher: BellasoCipher = BellasoCipher(key=key)
    plaintext: str = "Hello, World!"
    encrypted: str = cipher.encrypt(plaintext)
    decrypted: str = cipher.decrypt(encrypted)

    assert encrypted == "Rijhc, Gsphr!"
    assert decrypted == plaintext

def test_ceasar_cipher() -> None:
    cipher: CeasarCipher = CeasarCipher(shift=3)
    plaintext: str = "Hello, World!"
    encrypted: str = cipher.encrypt(plaintext)
    decrypted: str = cipher.decrypt(encrypted)

    assert encrypted == "Khoor, Zruog!"
    assert decrypted == plaintext

if __name__ == "__main__":
    test_bellaso_cipher()
    test_ceasar_cipher()
    print("All tests passed.")
