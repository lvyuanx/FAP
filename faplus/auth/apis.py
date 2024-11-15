from faplus import settings

apis = {
    
}


if settings.DEBUG:
    from .views.encrypt_decrypt import rsa_encrypt_view, rsa_decrypt_view, aes_decrypt_view, aes_encrypt_view, md5_encrypt_view
    
    apis["/rsa"] = [
        ("00", "/encrypt", rsa_encrypt_view, "RSA加密",  ["DEBUG"]),
        ("01", "/decrypt", rsa_decrypt_view, "RSA解密",  ["DEBUG"]),
    ]
    
    apis["/aes"] = [
        ("02", "/encrypt", aes_encrypt_view, "AES加密",  ["DEBUG"]),
        ("03", "/decrypt", aes_decrypt_view, "AES解密",  ["DEBUG"]),
    ]
    
    apis["/md5"] = [
        ("04", "/encrypt", md5_encrypt_view, "MD5加密",  ["DEBUG"]),
    ]