from flask import Flask
import json

app = Flask(__name__)

proof = "[['up', 'hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni'], ['up', 'hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni'], ['right', '6de4c2ebc51eef4be83edb4b91ef95ba395858ee398b5301339d8174ede3a9ed']]"

@app.route("/verify")
def verify():
	response = app.response_class(
			response=json.dumps(proof),
			status=200,
			mimetype='application/json'
		)
	return response


app.run(debug=True)