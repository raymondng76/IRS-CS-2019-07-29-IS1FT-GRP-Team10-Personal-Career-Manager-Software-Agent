from flask import Flask, request, make_response, jsonify
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
