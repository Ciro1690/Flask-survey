from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route('/')
def home_page():
    return render_template("home.html", survey=survey)

@app.route('/questions/<int:post_id>')
def display_questions(post_id):
    if (post_id < 0 or post_id > len(survey.questions)-1):
        flash("You searched for a question out of range.")
        return redirect('/')
    elif (len(survey.questions) == len(responses)):
        return redirect('/questions/thank_you')
    else:
        question = survey.questions[len(responses)]
        return render_template("questions.html", question=question)

@app.route('/answer', methods=["POST"])
def log_answer():
    choice = request.form.get("choice")
    responses.append(choice)

    if (len(survey.questions) == len(responses)):
        return redirect('/questions/thank_you')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/thank_you')
def thank_you():
    return render_template('thank_you.html')
