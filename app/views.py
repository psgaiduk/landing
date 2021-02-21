from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
all_clicks = []
all_show = []


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    if from_landing == 'test':
        all_clicks.append('test')
    elif from_landing == 'original':
        all_clicks.append('original')

    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    type_landing = request.GET.get('ab-test-arg', 'original')
    if type_landing == 'test':
        site = 'landing_alternate.html'
        all_show.append('test')
    elif type_landing == 'original':
        site = 'landing.html'
        all_show.append('original')
    return render(request, site)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    counter_show = Counter(all_show)
    counter_click = Counter(all_clicks)

    if counter_show['original'] == 0:
        original_stats = 0
    else:
        original_stats = counter_click['original']/counter_show['original']

    if counter_show['test'] == 0:
        test_stats = 0
    else:
        test_stats = counter_click['test']/counter_show['test']

    return render(request, 'stats.html', context={
        'test_conversion': test_stats,
        'original_conversion': original_stats,
    })
