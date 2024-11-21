from faplus import settings

DEBUG = getattr(settings, "DEBUG", True)
FAP_LOGIN_URL = getattr(settings, "FAP_LOGIN_URL", None)

apis = {
    
}

if not FAP_LOGIN_URL:
    from .views.user import login_view
    apis["/user"] = [
        ("07", "/login", login_view, "登录")
    ]


if DEBUG:
    from .views.encrypt_decrypt import rsa_encrypt_view, rsa_decrypt_view, \
        aes_decrypt_view, aes_encrypt_view, md5_encrypt_view \
        ,aes2_decrypt_view,aes2_encrypt_view
    
    from .views.user import create_user_view, test_view
    
    apis["/debug/user"] = [
        ("07", "/create", create_user_view, "创建用户",  ["DEBUG"]),
        ("08", "/test", test_view, "测试",  ["DEBUG"]),
    ]
    
    apis["/debug/rsa"] = [
        ("00", "/encrypt", rsa_encrypt_view, "RSA加密",  ["DEBUG"]),
        ("01", "/decrypt", rsa_decrypt_view, "RSA解密",  ["DEBUG"]),
    ]
    
    apis["/debug/aes"] = [
        ("02", "/encrypt", aes_encrypt_view, "AES加密",  ["DEBUG"]),
        ("03", "/decrypt", aes_decrypt_view, "AES解密",  ["DEBUG"]),
    ]
    
    apis["/debug/md5"] = [
        ("04", "/encrypt", md5_encrypt_view, "MD5加密",  ["DEBUG"]),
    ]
    
    apis["/debug/aes2"] = [
        ("05", "/encrypt", aes2_encrypt_view, "AES2加密",  ["DEBUG"]),
        ("06", "/decrypt", aes2_decrypt_view, "AES2解密",  ["DEBUG"]),
    ]