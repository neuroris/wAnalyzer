from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding, strxor

class WookCipher:
    def __init__(self, key=None):
        self.file_name = 'D:/Programming/Data/data.bin'
        self.login_id = None
        self.login_password = None
        self.account_password = None
        self.certificate_password = None
        self.raw_key = key

    def set_key(self, key):
        key_len = len(key)
        set_key = None

        if 0 < key_len < 16:
            portion = 16 // key_len
            remainder = 16 % key_len
            set_key = key * portion + key[:remainder]
        elif key_len >= 16:
            set_key = key[:16]

        return set_key

    def encrypt_data(self, login_id, login_password, account_password, certificate_password, given_key=None, file_name=None):
        plain_data = ';'.join((login_id, login_password, account_password, certificate_password))
        if file_name is not None:
            self.file_name = file_name

        # key setting
        random = Random.new()
        raw_key = given_key
        if raw_key is None:
            raw_key = self.raw_key
        set_key = self.set_key(raw_key)
        iv = random.read(AES.block_size)
        encoded_key = set_key.encode()
        key = strxor.strxor(encoded_key, iv)

        # Encryption
        encoded_data = plain_data.encode()
        padded_data = Padding.pad(encoded_data, AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(padded_data)

        # File writing
        with open(self.file_name, 'wb') as file:
            file.write(iv)
            file.write(encrypted_data)

    def decrypt_data(self, given_key=None, file_name=None):
        # data parsing
        if file_name is not None:
            self.file_name = file_name
        with open(self.file_name, 'rb') as file:
            iv = file.read(AES.block_size)
            encrypted_data = file.read()

        # key setting
        raw_key = given_key
        if raw_key is None:
            raw_key = self.raw_key
        set_key = self.set_key(raw_key)
        encoded_key = set_key.encode()
        key = strxor.strxor(encoded_key, iv)

        # decrypt data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        unpadded_data = Padding.unpad(decrypted_data, AES.block_size)
        plain_data = unpadded_data.decode()
        parsed_data = plain_data.split(';')
        self.login_id = parsed_data[0]
        self.login_password = parsed_data[1]
        self.account_password = parsed_data[2]
        self.certificate_password = parsed_data[3]

        return parsed_data

class WookLog:
    def __init__(self):
        pass

    def custom_init(self, log):
        self.log = log

    def debug(self, message, *args):
        message += ' %s'*len(args)
        self.log.debug(message, *args)

    def info(self, message, *args):
        message += ' %s'*len(args)
        self.log.info(message, *args)

    def warning(self, message, *args):
        message += ' %s' * len(args)
        self.log.warning(message, *args)

    def error(self, message, *args):
        message += ' %s' * len(args)
        self.log.error(message, *args)

    def critical(self, message, *args):
        message += ' %s' * len(args)
        self.log.critical(message, *args)