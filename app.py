from http.client import responses
from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

app.config['SECRET_KEY'] = "darkphoenix"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

# root route to show start page
@app.route('/')
def start_page():
    """Show survey instructions"""
    instructions = satisfaction_survey.instructions
    return render_template('start.html', instructions=instructions)

@app.route('/start', methods=["POST"])
def set_responses():
    """Clear the session of survey answers"""
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

# route to handle questions
@app.route('/questions/<int:question>')
def question_page(question):
    """Display the current question"""
    responses = session.get(RESPONSES_KEY)

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
    """Add answers to the session and go to next question"""
    # get the response choice
    answer = request.form['answer']

    # add response to the session
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    
    if len(responses) == len(satisfaction_survey.questions):
        # all questions have been answered, show /gratitude
        print(responses)
        return redirect('/gratitude')
    else:
        return redirect(f'/questions/{len(responses)}')

# route to handle end of survey
@app.route('/gratitude')
def survey_complete():
    return render_template('gratitude.html')