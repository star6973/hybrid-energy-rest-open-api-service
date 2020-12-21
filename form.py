from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired
from wtforms import BooleanField


class AreaSearchForm(FlaskForm):
    area = f.StringField('지역 명', validators=[DataRequired()], render_kw={"placeholder" : "지역 명"})
    display = ['area']


class DaySearchForm(FlaskForm):
    area = f.StringField('지역', validators=[DataRequired()], render_kw={"placeholder": "지역(ex : 경기도)"})
    day = f.StringField('일', validators=[DataRequired()], render_kw={"placeholder": "일(ex : 01)"})
    month = f.StringField('월', validators=[DataRequired()], render_kw={"placeholder": "월(ex : 01)"})
    year = f.StringField('연', validators=[DataRequired()], render_kw={"placeholder": "연(ex : 2017)"})
    display = ['area', 'year', 'month', 'day']


class MonthSearchForm(FlaskForm):
    area = f.StringField('지역', validators=[DataRequired()], render_kw={"placeholder": "지역(ex : 경기도)"})
    month = f.StringField('월', validators=[DataRequired()], render_kw={"placeholder": "월(ex : 01)"})
    year = f.StringField('연', validators=[DataRequired()], render_kw={"placeholder": "연(ex : 2017)"})
    display = ['area', 'year', 'month']


class YearSearchForm(FlaskForm):
    area = f.StringField('지역', validators=[DataRequired()], render_kw={"placeholder": "지역(ex : 경기도)"})
    year = f.StringField('연', validators=[DataRequired()], render_kw={"placeholder": "연(ex : 2017)"})
    display = ['area', 'year']
