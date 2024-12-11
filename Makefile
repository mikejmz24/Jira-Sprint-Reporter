run-tests:
	pytest --tb=short --disable-warnings -v test_entities.py 2>&1 | grep -E "^(test_|.* (PASSED|FAILED|ERROR)$)" | grep -vE "^\[|^test_entities.py:[0-9]+: in"
