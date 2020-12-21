import pprint
import requests
from flask import Blueprint, request, render_template
from form import  DaySearchForm, MonthSearchForm, YearSearchForm

execute_blueprint = Blueprint('execute', __name__)
SERVER_URL='http://127.0.0.1:5000'


@execute_blueprint.route('/day', methods=['GET', 'POST'])
def day():
    form = DaySearchForm()
    if request.method == 'POST':
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
        return render_template(
            'execute.html',
            res=res.json(),
            form=form,
            menu='execute',
            sub_menu='day'
        )
    return render_template(
        'execute.html',
        res='',
        form=form,
        menu='execute',
        sub_menu='day'
    )


@execute_blueprint.route('/month', methods=['GET', 'POST'])
def month():
    form = MonthSearchForm()
    if request.method == 'POST':
        area = form.data['area']
        month = form.data['month']
        year = form.data['year']
        date = '{0}-{1}'.format(year,month)
        # URL 규칙 : 서버 주소/리소스명/{리소스}/리소스명/{리소스}
        url = '{0}/month-energy/{1}/area/{2}'.format(SERVER_URL, date, area)
        res = requests.get(
            url=url
        )
        return render_template(
            'execute.html',
            res=res.json(),
            form=form,
            menu='execute',
            sub_menu='month'
        )
    return render_template(
        'execute.html',
        res='',
        form=form,
        menu='execute',
        sub_menu='month'
    )


@execute_blueprint.route('/year', methods=['GET', 'POST'])
def year():
    form = YearSearchForm()
    if request.method == 'POST':
        area = form.data['area']
        year = form.data['year']
        # URL 규칙 : 서버 주소/리소스명/{리소스}/리소스명/{리소스}
        url = '{0}/year-energy/{1}/area/{2}'.format(SERVER_URL, year, area)
        res = requests.get(
            url=url
        )
        return render_template(
            'execute.html',
            res=res.json(),
            form=form,
            menu='execute',
            sub_menu='year'
        )
    return render_template(
        'execute.html',
        res='',
        form=form,
        menu='execute',
        sub_menu='year'
    )
