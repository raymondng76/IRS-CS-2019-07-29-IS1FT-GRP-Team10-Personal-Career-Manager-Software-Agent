from flask import Flask, request, make_response, jsonify, render_template
import intents, utilities

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == '': #TODO: Add intent here
        resp_text = ""
    elif intent_name == '':
        resp_text = ""
    else:
        resp_text="I do not understand, could you rephrase that?"
    return make_response(jsonify({'fulfillmentText': resp_text}))


@app.route('/courserecommend')
def courserecommend():
    """
    http://localhost:5000/courserecommend
    """
    return render_template("courserecommend.html")

@app.route('/jobrecommend')
def jobrecommend():
    """
    http://localhost:5000/jobrecommend
    """
    return render_template("jobrecommend.html")

@app.route('/jobcourserecommend')
def jobcourserecommend():
    """
    http://localhost:5000/jobcourserecommend
    """
    return render_template("jobcourserecommend.html")

@app.route('/signup')
def signup():
    """
    http://localhost:5000/signup
    """
    return render_template("signup.html")

@app.route('/signupthanks')
def signupthanks():
    """
    http://localhost:5000/signupthanks
    """
    return render_template("signupthanks.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
