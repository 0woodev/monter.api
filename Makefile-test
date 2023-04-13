ROOT_DIR := $(shell eval pwd)
API_MODULE_DEPTH := 2
DOMAIN_MODULE_DEPTH := 1



setup: venv setup-makefile
	$(info ------------------------ install lib in requirements.txt ------------------------)
	./.venv/bin/pip3 install --upgrade pip
	./.venv/bin/pip3 install -r requirements.txt

venv:
	$(info ------------------------ make .venv folder ------------------------)
	python3 -m venv ./.venv

clean-venv:
	$(info ------------------------ remove .venv folder ------------------------)
	rm -rf .venv



setup-makefile: unlink-makefile link-makefile
	$(info ------------------------ renew makefile finish ------------------------)

link-makefile:
	$(info ------------------------ link new makefile ------------------------)

unlink-makefile:
	$(info ------------------------ unlink(remove) old makefile ------------------------)




clean: clean-venv unlink-makefile
	$(info ------------------------ $@ start ------------------------)
