import pprint
import requests
from flask import Blueprint, request, render_template
from form import AreaSearchForm, DaySearchForm, MonthSearchForm, YearSearchForm

example_blueprint = Blueprint('example', __name__)
SERVER_URL='http://127.0.0.1:8080'


@example_blueprint.route('/day', methods=['GET', 'POST'])
def day():
    form = DaySearchForm()
    # rest url 주소 =  서버 주소/서비스 이름/자원
    # url = http://127.0.0.1:8080/day-energy/{'2017-01-01'}/area/{'경기도'}
    # Test 용 기본 Date : 2017-01-01
    date = '2017-01-01'
    if request.method == 'POST':
        if form.validate_on_submit():
            area = form.data['area']
            day = form.data['day']
            month = form.data['month']
            year = form.data['year']
            date = '{0}-{1}-{2}'.format(year, month, day)
            # rest url 주소 =  서버 주소/서비스 이름/자원
            # url = http://127.0.0.1:8080/day-energy/{'2017-01-01'}/area/{'경기도'}
            url = '{0}/day-energy/{1}/area/{2}'.format(SERVER_URL, date, area)
            res = requests.get(
                url=url
            )
            if res.status_code == 200 :
                if res.json()['Optimal_prompt1'] == 0 :
                    code = 2
                else :
                    code = 1
                return render_template(
                    'example.html',
                    menu='example',
                    sub_menu='day',
                    res=res.json(),
                    form=form,
                    code=code
                )
            else :
                return render_template(
                    'example.html',
                    menu='example',
                    sub_menu='day',
                    res=None,
                    form=form,
                    code=3
                )

    url = 'http://127.0.0.1:8080/day-energy/2017-01-01/area/경기도'
    res = requests.get(
        url=url
    )
    if res.status_code == 200:
        if res.json()['Optimal_prompt1'] == 0:
            code = 2
        else:
            code = 1
    else:
        code = 3
    return render_template(
        'example.html',
        menu='example',
        res=res.json(),
        form=form,
        sub_menu='day'
    )


@example_blueprint.route('/month', methods=['GET', 'POST'])
def month():
    form = MonthSearchForm()
    # rest url 주소 =  서버 주소/서비스 이름/자원
    # url = http://127.0.0.1:8080/day-energy/{'2017-01-01'}/area/{'경기도'}
    # Test 용 기본 Date : 2017-01
    if request.method == 'POST':
        if form.validate_on_submit():
            area = form.data['area']
            month = form.data['month']
            year = form.data['year']
            date = '{0}-{1}'.format(year, month)
            # rest url 주소 =  서버 주소/서비스 이름/자원
            # url = http://127.0.0.1:8080/day-energy/{'2017-01-01'}/area/{'경기도'}
            url = '{0}/month-energy/{1}/area/{2}'.format(SERVER_URL, date, area)
            res = requests.get(
                url=url
            )
            print(res.json())
            if res.status_code == 200 :
                if res.json()['Optimal_prompt1'] == 0 :
                    code = 2
                else :
                    code = 1
                return render_template(
                    'example.html',
                    menu='example',
                    res=res.json(),
                    form=form,
                    sub_menu='month',
                    code=code
                )
            else :
                return render_template(
                    'example.html',
                    menu='example',
                    res=None,
                    form=form,
                    sub_menu='month',
                    code=3
                )

    url = 'http://127.0.0.1:8080/month-energy/2017-01/area/경기도'
    res = requests.get(
        url=url
    )
    if res.status_code == 200:
        if res.json()['Optimal_prompt1'] == 0:
            code = 2
        else:
            code = 1
    else:
        code = 3
    return render_template(
        'example.html',
        menu='example',
        res=res.json(),
        form=form,
        sub_menu='month',
        code=code
    )


@example_blueprint.route('/year', methods=['GET', 'POST'])
def year():
    form = YearSearchForm()
    # rest url 주소 =  서버 주소/서비스 이름/자원
    # url = http://127.0.0.1:8080/day-energy/{'2017-01-01'}/area/{'경기도'}
    # Test 용 기본 Date : 2017-01
    if request.method == 'POST':
        if form.validate_on_submit():
            area = form.data['area']
            year = form.data['year']
            # rest url 주소 =  서버 주소/서비스 이름/자원
            # url = http://127.0.0.1:8080/day-energy/{'2017-01-01'}/area/{'경기도'}
            url = '{0}/year-energy/{1}/area/{2}'.format(SERVER_URL, year, area)
            res = requests.get(
                url=url
            )

            if res.status_code == 200 :
                if res.json()['Optimal_prompt1'] == 0 :
                    code = 2
                else :
                    code = 1
                return render_template(
                    'example.html',
                    menu='example',
                    sub_menu='year',
                    res=res.json(),
                    form=form,
                    code=code
                )
            else :
                return render_template(
                    'example.html',
                    menu='example',
                    sub_menu='year',
                    res=None,
                    form=form,
                    code=3
                )

    url = 'http://127.0.0.1:8080/year-energy/2017/area/경기도'
    res = requests.get(
        url=url
    )
    if res.status_code == 200:
        if res.json()['Optimal_prompt1'] == 0:
            code = 2
        else:
            code = 1
    else:
        code = 3
    return render_template(
        'example.html',
        menu='example',
        sub_menu='year',
        res=res.json(),
        form=form,
        code=code
    )