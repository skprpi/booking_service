from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, identify_hasher
from django.db import models


class UserRoles(models.TextChoices):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class CustomManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, is_admin=False, name=None,
                    surname=None, break_time=0,
                    timestamp=None, role=None, is_staff=False, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен предоставить email')
        if not password:
            raise ValueError('Пользователь должен ввесть пароль')
        email = self.normalize_email(email)

        user = self.model(email=email,
                          name=name,
                          surname=surname,
                          break_time=break_time,
                          is_admin=is_admin,
                          timestamp=timestamp,
                          role=role,
                          is_staff=is_staff,
                          )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password, is_admin=True,
                                name='', surname='', role=UserRoles.ADMIN,
                                is_staff=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    surname = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    break_time = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.STUDENT,
        verbose_name="Роль пользователя",
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        try:
            is_hash = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        # if not self.id and not self.is_staff:
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    duration = models.IntegerField(blank=False, default=45)
    is_cansalled = models.BooleanField(blank=False, default=False)
    is_payed =models.BooleanField(default=False)
    student_pk = models.ForeignKey(User, models.SET_NULL, blank=False, null=True, related_name='student_lesson')
    teacher_pk = models.ForeignKey(User, models.SET_NULL, blank=False, null=True, related_name='teacher_lesson')
    start_datetime = models.DateTimeField(blank=False)

    class Meta:
        ordering = ['start_datetime']


class Price(models.Model):
    duration = models.IntegerField(blank=False, default=45)
    price = models.IntegerField(blank=False, default=1000)


class Discipline(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()


class PriceDiscipline(models.Model):
    teacher_pk = models.ForeignKey(User, models.SET_NULL, blank=False, null=True,related_name='teacher_pk')
    discipline_pk = models.ForeignKey(Discipline, models.SET_NULL, null=True,blank=False, related_name='discipline_pk')
    price_pk = models.ForeignKey(Price, models.SET_NULL, blank=False, null=True,related_name='price_pk')
