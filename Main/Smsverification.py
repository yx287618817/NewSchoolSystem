# -*- coding: utf-8 -*-
# @Time    : 2019-04-24 17:20
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : Smsverification.py
# @Software: PyCharm


# -*- coding: utf-8 -*-

import requests

class ZhenziSmsClient(object):
	def __init__(self, apiUrl, appId, appSecret):
		self.apiUrl = apiUrl
		self.appId = appId
		self.appSecret = appSecret

	def send(self, number, message, messageId=''):
		data = {
			'appId': self.appId,
			'appSecret': self.appSecret,
			'message': message,
			'number': number,
			'messageId': messageId}
		res = requests.post(url=self.apiUrl + '/sms/send.do', data=data, verify=False)
		res.encoding = res.apparent_encoding
		return res.text

	def balance(self):
		data = {
			'appId': self.appId,
			'appSecret': self.appSecret}
		res = requests.post(url=self.apiUrl + '/account/balance.do', data=data, verify=False)
		res.encoding = res.apparent_encoding
		return res

	def findSmsByMessageId(self, messageId):
		data = {
			'appId': self.appId,
			'appSecret': self.appSecret,
			'messageId': messageId}
		res = requests.post(url=self.apiUrl + '/smslog/findSmsByMessageId.do', data=data, verify=False)
		res.encoding = res.apparent_encoding
		return res
