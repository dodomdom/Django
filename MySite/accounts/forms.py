# -*- coding: utf-8 -*- 
from django import forms


from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		#user_qs = User.objects.filter(username=username)
		#if user_qs.count() = 1:
		#	user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("등록되지 않은 아이디 입니다.")
			if not user.check_password(password):
				raise forms.ValidationError("패스워드가 틀렸습니다.")
			if not user.is_active:
				raise forms.ValidationError("사용불가능한 아이디 입니다.")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email Email')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',		
			'password',
			'email',
			'email2',
		]

#	def clena(self, *args, **kwargs):
#		email = self.cleaned_data.get('email')
#		email2 = self.cleaned_data.get('email2')
#		if email != email2:
#			raise forms.ValidationError("이메일이 동일하지 않습니다.")
#		email_qs = User.objects.filter(email=email)
#		if email_qs.exists():
#			raise forms.ValidationError("동일한 이메일이 존재합니다.")
#
#		return super(UserRegisterForm,self).clean(*args, **kwargs)

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("이메일이 동일하지 않습니다.")

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("동일한 이메일이 존재합니다.")
		return email