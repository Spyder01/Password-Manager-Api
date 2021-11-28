import rsa

publicKey, privateKey = rsa.newkeys(512)


def encrypt (password):
    return rsa.encrypt(password.encode(), publicKey)

def decrypt (password):
    return rsa.decrypt(password, privateKey).decode()

 