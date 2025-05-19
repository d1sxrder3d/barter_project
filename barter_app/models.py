from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    
    # avatar = models.ImageField(upload_to='/s3 в будущем', blank=True, null=True)

    ads = models.ManyToManyField('Ad', related_name='users', blank=True)
    exchanges = models.ManyToManyField('ExchangeProposal', related_name='users', blank=True)

    # last_activity = models.DateTimeField(null=True, blank=True) мейби потом сделаю 
    

    def __str__(self):
        return self.username


class Ad(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    class Category(models.TextChoices):
        ELECTRONICS = 'electronics', 'Электроника'
        CLOTHING = 'clothing', 'Одежда'
        BOOKS = 'books', 'Книги'
        OTHER = 'other', 'Другое'
    
    class Сondition(models.TextChoices):
        NEW = 'new', 'Новое'
        USED = 'used', 'Б/у'
        

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    # image = models.ImageField(upload_to='s3 в будущем', blank=True, null=True)

    category = models.CharField(max_length=20, choices=Category.choices)
    condition = models.CharField(max_length=10, choices=Сondition.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидание'
        ACCEPTED = 'accepted', 'Принято'
        REJECTED = 'rejected', 'Отклонено'

    
    id = models.AutoField(primary_key=True)

    ad_reciever_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reciever_ad')
    ad_sender_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sender_ad')

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    comment = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
