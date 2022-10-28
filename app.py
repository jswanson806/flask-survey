from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

app.config['SECRET_KEY'] = "darkphoenix"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# list to store answers from users
responses = []

# root route to show start page
@app.route('/')
def start_page():
    instructions = satisfaction_survey.instructions
    return render_template('start.html', instructions=instructions)

# route to begin the survey
@app.route('/begin')
def begin():
    return redirect('/questions/0')

# route to handle questions
@app.route('/questions/<int:question>')
def question_page(question):
    

    if responses is None:
        return redirect('/')

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/gratitude')

    if len(responses) != question:
        flash("Invalid question ID")
        return redirect(f'/questions/{len(responses)}')

    questions = satisfaction_survey.questions[question].question
    choices = satisfaction_survey.questions[question].choices
    
    return render_template('questions.html', questions=questions, choices=choices)
    

#  route to handle answers
@app.route('/answer', methods=["POST"])
def add_answers():
    response = request.form['answer']
    responses.append(response)
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/gratitude')
    else:
        return redirect(f'/questions/{len(responses)}')

# route to handle end of survey
@app.route('/gratitude')
def survey_complete():
    return render_template('gratitude.html')