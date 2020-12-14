from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey_1
from surveys import personality_quiz as survey_2

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def home_page():
    return render_template("home.html", survey1=survey_1, survey2 =survey_2)

@app.route('/start', methods=["POST"])
def start():
    session['responses'] = []
    session['comments'] = []
    satisfaction = request.form.get("satisfaction")
    personality = request.form.get("personality")

    if satisfaction:
        session['survey'] = 1
        return redirect('/questions/0')
    elif personality:
        session['survey'] = 2
        return redirect('/questions/0')

@app.route('/questions/<int:post_id>')
def display_questions(post_id):
    if session['survey'] == 1:
        survey = survey_1
    elif session['survey'] == 2:
        survey = survey_2
    if (post_id < 0 or post_id > len(survey.questions)-1):
        flash("You searched for a question out of range.")
        return redirect('/')
    elif (len(survey.questions) == len(session['responses'])):
        return redirect('/questions/thank_you')
    else:
        question = survey.questions[len(session['responses'])]
        return render_template("questions.html", question=question)

@app.route('/answer', methods=["POST"])
def log_answer():
    choice = request.form.get("choice")
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if request.form.get("comment"):
        comment = request.form.get("comment")
        comments = session['comments']
        comments.append(comment)
        session['comments'] = comments

    if session['survey'] == 1:
        survey = survey_1
    elif session['survey'] == 2:
        survey = survey_2

    if (len(survey.questions) == len(session['responses'])):
        return redirect('/questions/thank_you')
    else:
        return redirect(f"/questions/{len(session['responses'])}")

@app.route('/questions/thank_you')
def thank_you():
    if session['survey'] == 1:
        survey = survey_1
    elif session['survey'] == 2:
        survey = survey_2

    return render_template('thank_you.html',questions=survey.questions)
