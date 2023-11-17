PORT=5000

.PHONY: run
run:
	FLASK_APP=app.py python3 -m flask --debug run -p $(PORT)