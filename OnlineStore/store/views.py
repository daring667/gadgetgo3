from django.shortcuts import get_object_or_404, render

from .models import Item, ItemTag
from .paginator import paginator


def store(request):
    items = Item.objects.filter(is_available=True)
    context = {
        'page_obj': paginator(request, items, 9),
        'range': [*range(1, 7)],  # For random css styles
    }

    return render(request, 'store/main_page.html', context)


def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    context = {
        'item': item,
    }
    return render(request, 'store/item_details.html', context)


def tag_details(request, slug):
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags__in=[tag])
    context = {
        'tag': tag,
        'page_obj': paginator(request, items, 3),
    }
    return render(request, 'store/tag_details.html', context)


def tag_list(request):
    query = request.GET.get('query', '')  # Получаем поисковый запрос
    tags = ItemTag.objects.all()  # Получаем все теги (категории)

    # Фильтрация товаров по запросу
    if query:
        items = Item.objects.filter(title__icontains=query, is_available=True)  # Фильтруем товары по названию
    else:
        items = Item.objects.filter(is_available=True)  # Без фильтрации, если запрос пуст

    context = {
        'page_obj': paginator(request, items, 6),  # Пагинация
        'tags': tags,  # Отображаем все теги
        'query': query,  # Передаем поисковый запрос в контекст
    }
    return render(request, 'store/tag_list.html', context)

