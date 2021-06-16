import ast
from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .forms import UserLoginForm, UserRegisterForm
from .models import UserRoles, Lesson, DisciplineDescription
from django.urls import reverse_lazy
from django.views.generic import CreateView

User = get_user_model()


class SignUp(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    # if request.method == 'POST':
    auth.logout(request)
    return redirect('/')


def get_time_price_list(disciplines):
    time_price = {}
    for el in disciplines:
        if el.name not in time_price:
            time_price[el.name] = []
        time_price[el.name].append(f'{el.duration} min - {el.price}')
    return time_price


def get_booked_times_list(lessons, count_load_days, teacher_break,
                          lesson_time):
    booked_times = [[] for _ in range(count_load_days)]
    interval = teacher_break // 15
    for el in lessons:
        time = el.start_datetime
        time = time.replace(tzinfo=None)

        delta = time - datetime.today().replace(minute=0, hour=0, second=0)

        day_idx = delta.days
        idx = (time.hour * 60 + time.minute + 1) // 15
        for i in range(-interval - lesson_time,
                       (el.duration + 1) // 15 + interval):
            if 0 <= idx + i < 24 * 4:
                booked_times[day_idx].append(idx + i)
    return booked_times


def get_lessons_obj(user_id, count_load_days):
    start_date = datetime.today().replace(minute=0, hour=0, second=0)
    end_date = start_date + timedelta(days=count_load_days)
    lessons = Lesson.objects.filter(
        student_pk=user_id,
        start_datetime__range=[start_date, end_date],
        is_cansalled=False,
    ) | Lesson.objects.filter(
        teacher_pk=user_id,
        start_datetime__range=[start_date, end_date],
        is_cansalled=False,
    )
    return lessons


def get_date_week_month(count_load_days):
    week_days_names = ['-', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    month_names = ['-', 'январь', 'февраль', 'март', 'аперь', 'май', 'июнь',
                   'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
                   'декабрь']
    week_days = ['' for _ in range(count_load_days)]
    date_number = [0 for _ in range(count_load_days)]
    month_number = ['' for _ in range(count_load_days)]
    for i in range(count_load_days):
        delta = timedelta(days=i)
        next_day = datetime.today() + delta
        day_idx = next_day.isoweekday()
        week_days[i] = week_days_names[day_idx]
        date_number[i] = next_day.day
        month_number[i] = month_names[next_day.month]
    return date_number, week_days, month_number


def get_distinct_discipline_name(disciplines):
    res = set()
    for el in disciplines:
        res.add(el.name)
    return res


@never_cache
def select_discipline(request, teacher_pk):
    teacher = get_object_or_404(User, pk=teacher_pk)
    if teacher.role != UserRoles.TEACHER or request.user.role != UserRoles.STUDENT:
        return render(request, 'misc/404.html')
    disciplines = DisciplineDescription.objects.filter(teacher_pk=teacher_pk)
    user_context = {
        'disciplines': get_distinct_discipline_name(disciplines),
    }
    return render(request, 'select_discipline.html', context=user_context)


@csrf_exempt
def get_discipline(request, teacher_pk):
    discipline_name = request.POST.get('discipline_name', None).strip('"')
    print(discipline_name)
    available_time = DisciplineDescription.objects.filter(
        teacher_pk=teacher_pk, name=discipline_name)
    time_price_list = []
    for el in available_time:
        time_price_list.append([el.duration, el.price])
    time_price_list.sort()

    html = ''

    for i in range(len(time_price_list)):
        html += f'<p class="col-12"> ' \
                f'<label name="labelName" class="col-12 btn-outline-primary btn-lg btn-block btn"> ' \
                f'<input type="radio" name="times" id="{i}" ' \
                f'autocomplete="off">{time_price_list[i][0]} минут - {time_price_list[i][1]} рублей </label></p>'

    data = {
        'html': html,
    }
    return JsonResponse(data)  # render(request, 'login.html')


count_load_days = 30
start_show_time = 10
end_show_time = 22


@csrf_exempt
def get_lessons(request, teacher_pk):
    lesson_time = int(request.POST.get('res', None).strip('"'))
    print(lesson_time)

    teacher = get_object_or_404(User, pk=teacher_pk)
    if teacher.role != UserRoles.TEACHER or request.user.role != UserRoles.STUDENT:
        return
    lessons = get_lessons_obj(request.user.id, count_load_days)
    disciplines = DisciplineDescription.objects.filter(teacher_pk=teacher_pk)
    date_number, week_days, month_number = get_date_week_month(count_load_days)

    user_context = {
        'pk': request.user.id,
        'text': get_object_or_404(User, pk=request.user.id).email,
        'lessons': lessons,
        'teacher_name': teacher.name,
        'teacher_surname': teacher.surname,
        'time_price': get_time_price_list(disciplines),
        'load_days_range': range(count_load_days),
        'booked_times': get_booked_times_list(
            lessons,
            count_load_days,
            teacher.break_time,
            lesson_time
        ),
        'time_range': range(start_show_time, end_show_time + 1),
        'count_cell_in_row': range(4),
        'week_days': week_days,
        'date_number': date_number,
        'month_number': month_number,
    }
    return render(request, 'home.html', context=user_context)


@csrf_exempt
def make_db_note(request, teacher_pk):
    teacher = get_object_or_404(User, id=teacher_pk)

    discipline_name = request.POST.get('discipline_name', None).strip('"')
    duration_15 = int(request.POST.get('duration', None).strip('"'))
    periods = ast.literal_eval(request.POST.get('periods'))
    price = int(request.POST.get('price', None).strip('"'))

    for day in periods:
        for time in periods[day]:
            delta = timedelta(days=int(day), minutes=int(time) * 15 % 60,
                              hours=int(time) * 15 // 60)
            start_time = datetime.today().replace(minute=0, hour=0,
                                                  second=0) + delta
            Lesson.objects.create(
                duration=duration_15 * 15,
                student_pk=request.user,
                teacher_pk=teacher,
                start_datetime=start_time,
                name=discipline_name,
                price=price,
            )
    print(discipline_name, duration_15, periods)
    return HttpResponse('OK')
    # return render(request, 'home.html', context=user_context)


def get_my_lesson_list(my_lessons):
    res = [[] for _ in range(count_load_days)]
    for el in my_lessons:
        print(el.__dict__)
        time = el.start_datetime
        time = time.replace(tzinfo=None)
        delta = time - datetime.today().replace(minute=0, hour=0, second=0)
        day_idx = delta.days
        teacher = User.objects.get(id=el.teacher_pk.id)
        min_ = el.start_datetime.minute
        start_minute = min_ if min_ >= 10 else '0' + str(min_)
        hr = el.start_datetime.hour
        start_hour = hr if hr >= 10 else '0' + str(hr)

        finish_time = el.start_datetime + timedelta(hours=el.duration // 60,
                                                    minutes=el.duration % 60)
        finish_min = finish_time.minute
        finish_min = finish_min if finish_min >= 10 else '0' + str(finish_min)
        finish_hour = finish_time.hour
        finish_hour = finish_hour if finish_hour >= 10 else '0' + str(
            finish_hour)

        res[day_idx].append(
            [f'{start_hour}:{start_minute} - {finish_hour}:{finish_min}',
             el.price, el.name, teacher.surname + ' ' + teacher.name, el.id])
    return res


def get_timetable(request):
    my_lessons = get_my_lesson_list(
        get_lessons_obj(request.user.id, count_load_days))
    date_number, week_days, month_number = get_date_week_month(count_load_days)
    user_context = {
        'load_days_range': range(count_load_days),
        'week_days': week_days,
        'date_number': date_number,
        'month_number': month_number,
        'lessons': my_lessons,
    }
    return render(request, 'timetable.html', context=user_context)


@csrf_exempt
def cancel_lesson(request):
    print(request)
    lesson_id = int(request.POST.get('lesson_id', None).strip('"'))
    lesson = Lesson.objects.get(id=lesson_id)
    lesson.is_cansalled = True
    lesson.save(update_fields=['is_cansalled'])
    return HttpResponse('OK')
