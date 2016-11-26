# coding:utf-8

import os

from handlers import Passport, VerifyCode,Profile
from handlers.BaseHandler import StaticFileHandler

handlers = [
    (r"/api/imagecode", VerifyCode.ImageCodeHandler),#验证码
    (r"/api/smscode", VerifyCode.SMSCodeHandler),#短信
    (r'^/api/register$', Passport.RegisterHandler),#注册
    (r'^/api/login$', Passport.LoginHandler),#登陆
    (r'^/api/logout$', Passport.LogoutHandler),#注销
    (r"^/api/profile/avatar",Profile.AvatarHandler),
    (r"^/api/profile/name",Profile.UpNameHandler),
    (r"^/api/profile/auth",Profile.SetAuthHandler),




    (r'^/api/check_login$', Passport.CheckLoginHandler),#检查用户状态

    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]