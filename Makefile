nope:
	$(error Not a valid target)

lint:
	sh scripts/lint.sh

format:
	sh scripts/format.sh

test:
	sh scripts/test.sh

test-cov:
	sh scripts/test-cov-html.sh
