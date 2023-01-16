from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def root():
    """Show the home page."""
    return render_template('survey.html', survey=survey)

@app.route('/start', methods={"POST"})
def start():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def answer():
    ans = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(ans)
    session[RESPONSES_KEY] = responses
    
    if(len(responses) == len(survey.questions)):
        return redirect("/thank")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def question(qid):
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect('/')

    if(len(responses) == len(survey.questions)):
        return redirect("/thank")
    
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route('/thank')
def thank():
    return render_template('thank-you.html')