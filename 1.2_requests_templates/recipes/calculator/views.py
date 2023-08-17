from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def recipes(request: HttpRequest, recipe_name: str) -> HttpResponse:
    template_name = 'calculator/index.html'

    recipe = DATA.get(recipe_name)

    servings = int(request.GET.get('servings', 1))

    if recipe and servings > 1:
        recipe = {k: round(v * servings, 2) for k, v in recipe.items()}
    
    context = {
        'recipe_name': recipe_name,
        'servings': servings,
        'recipe': recipe
    }

    return render(request, template_name, context)