from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 


class CustomUserManager(BaseUserManager):
    
    def create_user(self, mail, first_name, password = None, **extra_fields):
        if not mail:
            raise ValueError('Введите mail !')
        
        user = self.model(
            mail=self.normalize_email(mail),
            first_name=first_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, mail, first_name, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(mail, first_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    mail = models.EmailField(unique = True)
    first_name = models.CharField(max_length = 50, null=True, blank=True,verbose_name="Имя")
    last_name = models.CharField(max_length = 50, null=True, blank=True,verbose_name="Фамилия")
    middle_name = models.CharField(max_length = 50, null=True, blank=True,verbose_name="Отчество")
    # Сделаем адрес необязательным, чтобы создание пользователя из формы/serializers не падало
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    REQUIRED_FIELDS = ['first_name']
    USERNAME_FIELD = 'mail'
    
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
    
    class Meta:
        verbose_name = ('Пользователь')  
        verbose_name_plural = ('Пользователи')  