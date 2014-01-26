ALL: test

lint:
	pyflakes .

test: lint
	python main.py
