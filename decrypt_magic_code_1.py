import csv


ENCRYPTED_MAGIC_CODE_1_FILE = 'encrypted_magic_code_1.txt'
DECRYPTED_MAGIC_CODE_1_FILE = 'decrypted_magic_code_1.csv'


def decrypt_magic_code_1(key: int):
    with open(ENCRYPTED_MAGIC_CODE_1_FILE, 'rt') as f:
        rows = [
            (
                line.strip(),
                f'{(i - key) % 0x10000:04x}',
            )
            for i, line in enumerate(f)
            if line.strip()
        ]
    
    with open(DECRYPTED_MAGIC_CODE_1_FILE, 'wt', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('encrypted_code_1', 'magic_code_1'))
        writer.writerows(rows)


if __name__ == '__main__':
    key = 114514  # Change me
    decrypt_magic_code_1(key)
