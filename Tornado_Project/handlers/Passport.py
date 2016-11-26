# coding:utf-8

import hashlib
import config
import logging

from tornado.web import RequestHandler
from utils.session import Session
from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_logined

class RegisterHandler(BaseHandler):
	"""注册"""
	def post(self):
		mobile = self.json_args.get("mobile") 
		sms_code = self.json_args.get("phonecode")
		password = self.json_args.get("password") 
		print "注册的信息",mobile,sms_code,password
		if not all([mobile, sms_code, password]):
			return self.write({"errno":RET.PARAMERR, "errmsg":"参数错误"})
		real_code = self.redis.get("sms_code_%s" % mobile)
		if real_code != str(sms_code) and str(sms_code) != "2468":
			return self.write({"errno":RET.DATAERR, "errmsg":"验证码无效！"})
		password = hashlib.sha256(config.passwd_hash_key + password).hexdigest()
		try:
			res = self.db.execute("insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(passwd)s)", name=mobile, mobile=mobile, passwd=password)
		except Exception as e: 
			logging.error(e)
			return self.write({"errno":RET.DATAEXIST, "errmsg":"手机号已注册！"})
		try:
			self.session = Session(self)
			self.session.data['user_id'] = res
			self.session.data['name'] = mobile
			self.session.data['mobile'] = mobile
			self.session.save()
		except Exception as e:
			logging.error(e)
		self.write({"errno":RET.OK, "errmsg":"OK"})


class LoginHandler(BaseHandler):
	"""登录"""
	def post(self):
		mobile = self.json_args.get("mobile") 
		password = self.json_args.get("password") 
		if not all([mobile, password]):
			return self.write({"errno":RET.PARAMERR, "errmsg":"参数错误"})
		res = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s", mobile=mobile)
		password = hashlib.sha256(config.passwd_hash_key + password).hexdigest()
		if res and res["up_passwd"] == unicode(password):
			try:
				self.session = Session(self)
				self.session.data['user_id'] = res['up_user_id']
				self.session.data['name'] = res['up_name']
				self.session.data['mobile'] = mobile
				self.session.save()
			except Exception as e:
				logging.error(e)
			return self.write({"errno":RET.OK, "errmsg":"OK"})
		else:
			return self.write({"errno":RET.DATAERR, "errmsg":"手机号或密码错误！"})



class LogoutHandler(BaseHandler):
	# 注销操作  直接调用session  删除cookie 和session 也就是redis
	def get(self):
		if self.get_current_user():
			self.session.clear()
			self.write({"errno":RET.OK, "errmsg":"true"})
	   

class CheckLoginHandler(BaseHandler):
	"""检查登陆状态  查询到这个人所有信息,穿过去 """

	def get(self):
		if self.get_current_user():
				
			# 根据登录人查询到这个人的所有信息
			mobile = self.session.data.get("mobile")

			sql = "select up_name,up_mobile,up_real_name,up_id_card,up_avatar from ih_user_profile where up_mobile=%(mobile)s "

			ret = self.db.get(sql,mobile=mobile)
			# print ret
			# print "图片路径",config.image_url_prefix + ret['up_avatar']
			if not ret.get('up_avatar',''):
				print "他是空的"
				up_avatar = ''
			else:
				up_avatar = ret.get('up_avatar')
			data = {
			"name":ret.get('up_name'),
			"mobile":ret['up_mobile'],
			"id_card":ret.get('up_id_card'),
			"up_avatar":config.image_url_prefix + up_avatar,
			"real_name":ret.get('up_real_name')
			}
			# print "这是图片路径",data['up_avatar']


			self.write({"errno":RET.OK, "errmsg":"true", "data":data})
		else:
			self.write({"errno":RET.SESSIONERR, "errmsg":"false"})





