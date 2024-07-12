from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

# 预设密钥和初始化向量
KEY = b'\xc2\xac6\x87\x8f\xf1\x1e\xf4\x01\x8d\xa3,:#\x1b\xe4\x05u7\xf3\xb1\x05I\x9a\xbf\xa0\xc9\x85\xfb(*\xdd'  # 32字节密钥


def encrypt(IV,data: str) -> str:
    """ 使用AES CBC模式加密数据 """
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt(IV,encrypted_data: bytes) -> str:
    """ 使用AES CBC模式解密数据 """
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(padded_data) + unpadder.finalize()
    return decrypted_data.decode('utf-8')

