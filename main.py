#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>

<html>
	<head>
		<style>
			.error {
				color: red;
			}
		</style>
	</head>
	<body>
	<h1><a href="/"> Signup </a></h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
	</body>
</html>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
	
class MainHandler(webapp2.RequestHandler):
	def get(self):
		
		errorUserName = self.request.get("errorUserName")
		if errorUserName:
			errorUserName = cgi.escape(errorUserName, quote=True)			
		else:
			errorUserName = ''
		
		errorPassword = self.request.get("errorPassword")
		if errorPassword:
			errorPassword = cgi.escape(errorPassword, quote=True)			
		else:
			errorPassword = ''	
		
		errorVerify = self.request.get("errorVerify")
		if errorVerify:
			errorVerify = cgi.escape(errorVerify, quote=True)			
		else:
			errorVerify = ''		
			
		errorEmail = self.request.get("errorEmail")
		if errorEmail:
			errorEmail = cgi.escape(errorEmail, quote=True)			
		else:
			errorEmail = ''	
		
		postUserName = self.request.get("postUserName")
		if postUserName:
			postUserName = cgi.escape(postUserName, quote=True)			
		else:
			postUserName = ''	
		
		postEmail = self.request.get("postEmail")
		if postEmail:
			postEmail = cgi.escape(postEmail, quote=True)			
		else:
			postEmail = ''	
		
		formTag = """
		<form method="post">
			<table style='border: #000000 1px solid;'>
				<tr>
					<td><label for="username">Username</label></td>
					<td>
						<input name="username" type="text" value="{4}" required>
						<span class="error">{0}</span>
					</td>
				</tr>
				<tr>
					<td><label for="password">Password</label></td>
					<td>
						<input name="password" type="password" required>
						<span class="error">{1}</span>
					</td>
				</tr>
				<tr>
					<td><label for="verify">Verify Password</label></td>
					<td>
						<input name="verify" type="password" required>
						<span class="error">{2}</span>
					</td>
				</tr>
				<tr>
					<td><label for="email">Email</label></td>
					<td>
						<input name="email" type="email" value={5}>
						<span class="error">{3}</span>
					</td>
				</tr>
			</table>
			<input type="submit">
		</form>
		""".format(errorUserName, errorPassword, errorVerify, errorEmail, postUserName, postEmail)
		self.response.write(page_header + formTag + page_footer )
	
	def post(self):		
		errorInForm = False
		userCheck = self.request.get("username")		
		emailCheck = self.request.get("email")		
		if not valid_username(userCheck):						
			errorInForm = True
			errorUser = "Invalid user name format"			
			#self.redirect("/?errorUserName=" + error + "&postUserName=" + userCheck + "&postEmail=" + emailCheck)
		else:
			errorUser = ''
				
		passwordCheck = self.request.get("password")	
		if not valid_password(passwordCheck):						
			errorInForm = True
			errorPass = "Password does not meet the criteria"			
			#self.redirect("/?errorPassword=" + error + "&postUserName=" + userCheck + "&postEmail=" + emailCheck)
		else:
			errorPass = ''
				
		verifyCheck = self.request.get("verify")
		if passwordCheck <> verifyCheck:
			errorInForm = True
			errorVer = "Passwords do not match"			
			#self.redirect("/?errorVerify=" + error + "&postUserName=" + userCheck + "&postEmail=" + emailCheck)			
		else:
			errorVer = ''
		
		if not valid_email(emailCheck):
			errorInForm = True
			errorEmail = "Email not in correct format"			
		else:
			errorEmail = ''
		
		if not errorInForm:
			#self.response.write("Welcome: " + userCheck)
			self.redirect('/welcome?username=' + userCheck)
		else:
			self.redirect("/?errorUserName=" + errorUser + "&errorPassword=" + errorPass + "&errorVerify=" + errorVer + "&postUserName=" + userCheck + "&postEmail=" + emailCheck + "&errorEmail=" + errorEmail )

class Welcome(webapp2.RequestHandler):	
    def get(self):
		username = self.request.get('username')
		self.response.write("<p>Welcome <strong>" + username + "</strong></p>")
		
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', Welcome)
], debug=True)
