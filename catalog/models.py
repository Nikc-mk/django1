from django.db import models
from django.urls import reverse
import uuid  # Требуется для уникальных экземпляров книги


# Create your models here.
class Genre(models.Model):
    """
    Модель представляющая жанр книги(детектив, фэнтези)
    """
    name = models.CharField(max_length=200, help_text="Введите жанр книги/Enter a book genre")

    def __str__(self):
        """
        Строка для представления объекта модели на сайте администратора
        """
        return self.name


class Book(models.Model):
    """
    Модель представляет книги без разделения на отдельные экземпляры
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key (один ко многим) используется потому-что мы предполагаем, что книга имеет одного автора,
    # но автор может написать много книг.
    # Автор как строка, а не как объект, потому что он еще не объявлен в файле
    summary = models.TextField(max_length=1000, help_text='Введите краткое описание книги/'
                                                          'Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/'
                                                             'content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Выберите жанр книги/Select a genre for this book')

    # ManyToManyField (многие к многим) используется так как жанр содержит много книг,
    # книга может относиться к разным жанрам

    def __str__(self):
        """
        Строка для представления объекта модели на сайте администратора
        """
        return self.title

    def get_absolute_url(self):
        # Возвращает URL-адрес для доступа к конкретному экземпляру книги
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Создает строку для жанра. Это необходимо для отображения жанра в Admin"""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Модель представляет конкретную копию книги"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный ID для конкретного '
                                                                          'экземпляра книги')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('т', "Техническое обслуживание"),
        ("п", "Предоставлена для выставки"),
        ("и", "Имеется в наличии"),
        ("з", "Зарезервирована"),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='т',
                              help_text='Забронировать книгу')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f'{self.id}, {self.book.title}'


class Author(models.Model):
    """Модель представляет автора"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """Модель представляет язык"""
    name = models.CharField(max_length=200,
                            help_text="Введите язык книги (например English, French, Japanese и т.д.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
