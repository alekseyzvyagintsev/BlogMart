import os.path

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import filepath_to_uri

from catalog.models import Product, Category
from config import settings


def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)  # Устанавливаем 12 продуктов на странице
    page_number = request.GET.get('page')  # Берём номер страницы из URL
    page_obj = paginator.get_page(page_number)  # Получаем нужную страницу
    context = {'page_obj': page_obj}
    return render(request, 'products/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'products/contact.html')


def product_detail(request, product_id=1):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('catalog:home')

    cotext = {'product': product, }
    return render(request, 'products/product_detail.html', context=cotext)


def create_product(request):
    categories = Category.objects.all()
    context = {'categories': categories,}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_in = request.POST.get('category_name')
        price = request.POST.get('price')
        image = request.POST.get('image')
        print(f'{name}, {category_in}, {price}, путь к изображению {image}, {description}')
        if not name or not description or not category_in or not price:
            messages.error(request, 'Все обязательные поля должны быть заполнены!')
            print('Все обязательные поля должны быть заполнены!')
            return render(request, 'products/create_product.html', context)
        else:
            category_use = category_in
            try:
                # Получаем категорию 'Smartphones' из базы данных
                category = Category.objects.get(name=category_in)
            except Category.DoesNotExist as e:
                raise Exception(str(e)) #"Категория {category_in} не найдена."
                messages.error(request, str(e))
                print(str(e))

            if category:
                category_use = category
            try:
                """
                Не понимаю как добиться полного локального пути. 
                Беру файл который уже имеется в конечной паке хранения.
                """
                if image:
                    product = Product.objects.create(
                        name=name,
                        description=description,
                        category=category_use,
                        price=price,
                        image=f'product_images/{image}'
                    )
                else:
                    product = Product.objects.create(
                        name=name,
                        description=description,
                        category=category_use,
                        price=price,
                        image='product_images/base_image.jpg'
                    )
                messages.success(request, f'Вы успешно создали новый товар: {product.name}')
                print(f'Вы успешно создали новый товар: {product.name}')
                return redirect('catalog:home')
            except ValueError as e:
                messages.error(request, str(e))
                print(str(e))
            except Exception as e:
                messages.error(request, str(e))
                print(str(e))
    return render(request, 'products/create_product.html', context)
