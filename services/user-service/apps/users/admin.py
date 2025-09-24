from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
	"""Форма для создания пользователя в админке с подтверждением пароля."""

	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = ('mail', 'first_name', 'last_name', 'address', 'phone')

	def clean_password2(self):
		p1 = self.cleaned_data.get('password1')
		p2 = self.cleaned_data.get('password2')
		if p1 and p2 and p1 != p2:
			raise forms.ValidationError('Пароли не совпадают')
		return p2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""Форма для изменения пользователя в админке, отображает поле хешированного пароля."""

	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CustomUser
		fields = ('mail', 'password', 'first_name', 'last_name', 'middle_name', 'address', 'phone', 'is_active', 'is_staff')

	def clean_password(self):
		# Всегда возвращаем первоначальное значение, независимо от ввода.
		return self.initial['password']


class CustomUserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('mail', 'first_name', 'last_name', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_superuser', 'is_active')
	search_fields = ('mail', 'first_name', 'last_name')
	ordering = ('mail',)
	filter_horizontal = ()

	fieldsets = (
		(None, {'fields': ('mail', 'password')}),
		('Персональные данные', {'fields': ('first_name', 'last_name', 'middle_name', 'address', 'phone')}),
		('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('mail', 'first_name', 'last_name', 'password1', 'password2'),
		}),
	)


admin.site.register(CustomUser, CustomUserAdmin)
