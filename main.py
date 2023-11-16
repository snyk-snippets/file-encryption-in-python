import aws_encryption_sdk

# Configuration
KEY_ARNs = [
    'arn:aws:kms:us-west-1:185803171344:key/xxx'
]

client = aws_encryption_sdk.EncryptionSDKClient()
kms_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(
    key_ids=KEY_ARNs)


def encrypt_file(file_path, encrypted_path):
    with open(file_path, 'rb') as pt_file, open(encrypted_path, 'wb') as ct_file:
        with client.stream(
            mode='e',
            source=pt_file,
            key_provider=kms_key_provider
        ) as encryptor:
            for chunk in encryptor:
                ct_file.write(chunk)


def decrypt_file(encrypted_path, decrypted_path):
    with open(encrypted_path, 'rb') as ct_file, open(decrypted_path, 'wb') as pt_file:
        with client.stream(
            mode='d',
            source=ct_file,
            key_provider=kms_key_provider
        ) as decryptor:
            for chunk in decryptor:
                pt_file.write(chunk)


# Use the functions
encrypt_file('test.txt', 'encrypted_file.txt')
decrypt_file('encrypted_file.txt', 'decrypted_file.txt')

print("Encryption and decryption successful!")
