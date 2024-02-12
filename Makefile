.PHONY: clean install test docker_image

clean:
	find . -name '*.py[co]' -delete
	rm -rf build
	rm -rf *.egg-info
	rm -rf venv
	rm -rf .pytest_cache



install: clean
	virtualenv -p python3 --prompt '|> godaddy_ddns <| ' venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install pytest
	venv/bin/pip install .
	@echo
	@echo "VirtualENV Setup Complete. Now run: source venv/bin/activate"
	@echo


test:
	pytest -rA tests/



mUID:=$(shell id -u)
mGID:=$(shell id -g)


docker_image:
	docker build --build-arg UID=$(mUID) --build-arg GID=$(mGID) -t godaddy_ddns:latest .


