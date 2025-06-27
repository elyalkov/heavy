from django.db import models
from django.urls import reverse
#reverse это функция, которая делает обратное преобразование маршрута из имени маршрута

class Category(models.Model):
    name = models.CharField(max_length=20,
                            unique=True) #две категории не могут иметь одинаковое имя
    slug = models.SlugField(max_length=20,
                            unique=True)


    class Meta:
        ordering = ['name'] #[] чтобы задавать СПИСКИ полей
        indexes = [models.Index(fields=['name'])] #Index — способ создать индекс на уровне базы данных / поиск будет выполнятся по полю name
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self): #метод говорит, какой URL соответствует этому объекту
        return reverse('main:product_list_by_category',
                           args=[self.slug]) #args — это список значений, которые подставляются в путь


    def __str__(self): #функция для получения имя катигории, т.е. что мы увидим в админке
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products', #псевдоним по которому можно будет обращаться
                                 on_delete=models.CASCADE) #при удалении категории, будут удалены все продукты из этой категории
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True) #доступность товара в наличии
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(default=0.00, max_digits=4,
                                   decimal_places=2)


    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']), #поиск по дате создания
        ]


    def __str__(self):
        return self.name


    def get_absolute_url(self): #url на адрес объекта по его id
        return reverse('main:product_detail',
                       args=[self.slug]) #передаем slug чтобы сгенерировать ссылку на товар


    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price