from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy, model
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///daily-failure-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
x = []
class Add(FlaskForm):

    STN_CODE = StringField("enter STN_CODE", validators=[DataRequired()])
    STN_NAME = StringField("enter STN_NAME")
    ADSTE = StringField("enter ADSTE")
    SSE = StringField("enter SSE")
    ROUTE = StringField("enter  ROUTE")
    SEC = StringField("enter  SEC")
    DIV = StringField("enter DIV")
    FAIL_TIME =StringField("enter FAIL_TIME")
    RIGHT_TIME = StringField("enter RIGHT_TIME ")
    DURATION =StringField("enter  DURATION")
    FAILURE_REMARKS =StringField("enter FAILURE_REMARKS")
    NAME_OF_GEAR_FAILED = StringField("enter NAME_OF_GEAR_FAILED")
    TYPE_OF_MAIN_GEAR_FAILED = StringField("enter TYPE_OF_MAIN_GEAR_FAILED")
    Failed_Gear_Desc = StringField("enter Failed_Gear_Desc")
    DEPTT = StringField("enter DEPTT")
    Cause = StringField("enter Cause ")
    Train_Detention = StringField("enter Train_Detention")
    submit = SubmitField('submit')

class Search(FlaskForm):
    STN_CODE = StringField("enter STN_CODE", validators=[DataRequired()])
    search = SubmitField('search')

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    S_NO = db.Column(db.String(250) ,nullable=False, unique= True)
    STN_CODE = db.Column(db.String(250), nullable=False)
    STN_NAME = db.Column(db.String(250), nullable=False)
    ADSTE = db.Column(db.String(250), nullable=False)
    SSE= db.Column(db.String(250), nullable=False)
    ROUTE=db.Column(db.String(250),nullable=False)
    SEC=db.Column(db.String(250), nullable=False)
    DIV=db.Column(db.String(250), nullable=False)
    FAIL_TIME=db.Column(db.String(250), nullable=False)
    RIGHT_TIME=db.Column(db.String(250), nullable=False)
    DURATION=db.Column(db.String(250), nullable=False)
    FAILURE_REMARKS=db.Column(db.String(1000), nullable=False)
    NAME_OF_GEAR_FAILED=db.Column(db.String(250), nullable=False)
    TYPE_OF_MAIN_GEAR_FAILED =db.Column(db.String(250), nullable=False)
    Failed_Gear_Desc=db.Column(db.String(250),nullable=False)
    DEPTT=db.Column(db.String(250), nullable=False)
    Cause=db.Column(db.String(250), nullable=False)
    Train_Detention=db.Column(db.String(250), nullable=False)

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


def to_json(all_vendors):
    v = [ ven.dobule_to_dict() for ven in all_vendors ]
    return v
users = Data.query.all()
sheet_data = to_json(users)
failure_event = ["S_NO","STN_CODE","STN_NAME","ADSTE","SSE"," ROUTE","SEC","DIV","FAIL_TIME","RIGHT_TIME","DURATION","FAILURE_REMARKS","NAME_OF_GEAR_FAILED","TYPE_OF_MAIN_GEAR_FAILED","Failed_Gear_Desc","DEPTT","Cause","Train_Detention"]

@app.route("/")
def home():


    return render_template("index.html", data = sheet_data,header = failure_event, asked =x)

@app.route('/search', methods=["GET", "POST"])
def search():
    form = Search()
    if request.method == 'POST':
        name = form.STN_CODE.data
        two_rows = Data.query.filter_by(STN_CODE=f"{name}").all()
        # global x
        # if x == []:
        #     x = failure_event
        return render_template("index.html", data = two_rows,header = failure_event, asked =x)
    return render_template("search.html", form= form)
@app.route("/add", methods =["GET", "POST"])
def add():
    form = Add()
    new_S_NO = len( db.session.query(Data).all())+1
    if form.validate_on_submit():
        new_data = Data(S_NO = new_S_NO,
                        STN_CODE = form.STN_CODE.data,
                        STN_NAME = form.STN_NAME.data,
                        ADSTE = form.ADSTE.data,
                        SSE = form.SSE.data,
                        ROUTE = form.ROUTE.data,
                        SEC = form.SEC.data,
                        DIV = form.DIV.data,
                        FAIL_TIME = form.FAIL_TIME.data,
                        RIGHT_TIME = form.RIGHT_TIME.data,
                        DURATION = form.DURATION.data,
                        FAILURE_REMARKS = form.FAILURE_REMARKS.data,
                        NAME_OF_GEAR_FAILED = form.NAME_OF_GEAR_FAILED.data,
                        TYPE_OF_MAIN_GEAR_FAILED = form.TYPE_OF_MAIN_GEAR_FAILED.data,
                        Failed_Gear_Desc = form.Failed_Gear_Desc.data,
                        DEPTT = form.DEPTT.data,
                        Cause = form.Cause.data,
                        Train_Detention = form.Train_Detention.data,
                        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("Add.html", form = form)

@app.route("/display", methods=['GET','POST'])
def dropdown():

    if request.method == 'POST':
        hidden_skills = request.form['hidden_skills']
        demand = re.split(',+', hidden_skills)
        global x
        x = demand
        return render_template("index.html", data= sheet_data,header = failure_event, asked =demand)
    return render_template("dropdown.html", dropdown_list = failure_event)
if __name__ == "__main__":
    app.run(debug=True)