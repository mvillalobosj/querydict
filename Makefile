build_readme:
	docker-compose run --rm pandoc

test_build:
	docker-compose build unittest

test_unit_run: build_readme test_build test_functional
	docker-compose run --rm unittest coverage run -m pytest tests/unit
	docker-compose run --rm unittest coverage report -m --omit="tests/*"
	docker-compose run --rm unittest coverage xml

test_benchmark:
	docker-compose run --rm unittest pytest tests/benchmark

test_unit:
	docker-compose run --rm unittest pytest tests/unit

test_functional:
	docker-compose run --rm unittest pytest -s -vv tests/functional
