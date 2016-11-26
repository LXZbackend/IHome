# coding:utf-8

import logging

from .BaseHandler import BaseHandler
from utils.image_storage import storage
from utils.common import require_logined
from utils.response_code import RET
import config

class AvatarHandler(BaseHandler):
	"""头像"""
	@require_logined
	def post(self):
		# print "上传图片了"
		print"拿到数据了"
		user_id = self.session.data["user_id"]
		try:
			avatar = self.request.files["avatar"][0]["body"]
			print"拿到数据了",avatar
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
		try:
			img_name = storage(avatar)
			# 开始调用上传方法了
		except Exception as e:
			logging.error(e)
			img_name = None
		if not img_name:
			print "七牛报错了"
			return self.write({"errno":RET.THIRDERR, "errmsg":"qiniu error"})
		try:
			print "往数据库插入"
			ret = self.db.execute("update ih_user_profile set up_avatar=%s where up_user_id=%s", img_name, user_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errno":RET.DBERR, "errmsg":"upload failed"})
		print"url...."
		img_url = config.image_url_prefix + img_name
		self.write({"errno":RET.OK, "errmsg":"OK", "url":img_url})


class UpNameHandler(BaseHandler):
	@require_logined
	def post(self):
		name = self.get_argument('name')
		user_id = self.session.data["user_id"]
		# 传过来的名字,进行判断
		
		ret = self.db.execute("update ih_user_profile set up_name=%s where up_user_id=%s",name, user_id)
		print "插入数据库"









class SetAuthHandler(BaseHandler):
	def post(self):
		print "SetAuthHandler"
		# 获取这个这时候session  如果有data 就作下面的操作
		print self.get_current_user()
		if self.get_current_user():
			real_name = self.json_args.get('real_name')
			id_card = self.json_args.get('id_card')
			print "需要修改的数据",real_name,id_card
			if not all([real_name, id_card]):
				return self.write({"errmo":RET.SESSIONERR,"errmsg":"请登录"})
	
			mobile = self.session.data.get("mobile")
			print "手机号",mobile
			try:
				ret = self.db.execute("update ih_user_profile set up_real_name=%s ,up_id_card=%s where up_mobile = %s",real_name, id_card,mobile)
				print"身份信息已经插入"
				return self.write({"errno":RET.OK, "errmsg":"OK"})
			except Exception as e:
				print"插入数据库报错了"
				logging.error(e)
				return self.write({"errno":RET.DBERR, "errmsg":"upload failed"})
		