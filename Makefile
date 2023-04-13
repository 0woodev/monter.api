$(eval export ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST)))))
$(eval export MODULE_DEPTH := 2)
$(eval MD5_exec=md5)
$(info make ${MD5_exec})

t%:
	$(eval target=$(subst t,,$@))
	cd ../terraform && make ${target}

setup: venv clear-makefile link-makefile
	./.venv/bin/pip3 install --upgrade pip
	./.venv/bin/pip3 install -r requirements.txt

venv:
	python3 -m venv ./.venv

destroy:
	rm -rf ./venv

clean:
build:
rebuild:
health-test:

sync-test: build tapplyq health-test
sync: build tapplyq

link-makefile:
clear-makefile:


health-test:
	#./venv/bin/python3 -m unittest authentication.v1_internal_authorizer_post.test_lambda_function.TestInternalAuthorizerPost
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec echo {} \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec sh -c 'cd ${ROOT_DIR}/{} && make health-test' \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec sh -c 'cd ${ROOT_DIR}/{} && make health-test' \;

rebuild: clean build

build: common.chk
	$(info -------------------------------------------- $@)
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec echo {} \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec sh -c 'cd ${ROOT_DIR}/{} && make build' \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec sh -c 'cd ${ROOT_DIR}/{} && make build' \;
	rm -f common.chk

clean:
	$(info -------------------------------------------- $@)
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec echo {} \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec sh -c 'cd ${ROOT_DIR}/{} && make clean' \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec sh -c 'cd ${ROOT_DIR}/{} && make clean' \;
	rm -f common.chk

common.chk common.md5 logger_util.chk logger_util.md5:
	$(info -------------------------------------------- $@)
	@find ./common -maxdepth 6 -mindepth 1 -type f \
! -path '*/test/*' \
! -name 'test_*' \
! -name '*.md5' \
! -name '*.chk' \
! -name '*.log' \
! -name '*.tmp' \
-exec sh -c 'path=$${1} && ${MD5_exec} $${path} \
' sh {} \; | ${MD5_exec} > $@

link-makefile:
	$(info -------------------------------------------- $@)
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec ln -s ${ROOT_DIR}/MakefileForDeploy ${ROOT_DIR}/{}/Makefile \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec ln -s ${ROOT_DIR}/MakefileForDeploy ${ROOT_DIR}/{}/Makefile \;
	find . -maxdepth 1 -mindepth 1 -path '*/*' ! -path '*/common' ! -path '*/mock' ! -path '*/support_legacy' ! -path '*/test_tools' ! -path '*/test_util' ! -path '*/venv' ! -path '*/backoffice' ! -path '*/logger_util'  -type d -exec ln -s ${ROOT_DIR}/MakefileForDeployByDomain ${ROOT_DIR}/{}/Makefile \;


	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec ln -s ${ROOT_DIR}/upload.sh ${ROOT_DIR}/{}/upload.sh \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec ln -s ${ROOT_DIR}/upload.sh ${ROOT_DIR}/{}/upload.sh \;

	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec ln -s ${ROOT_DIR}/change_env.sh ${ROOT_DIR}/{}/change_env.sh \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec ln -s ${ROOT_DIR}/change_env.sh ${ROOT_DIR}/{}/change_env.sh \;

clear-makefile:
	$(info -------------------------------------------- $@)
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec rm -rf ${ROOT_DIR}/{}/Makefile \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec rm -rf ${ROOT_DIR}/{}/Makefile \;
	find . -maxdepth 1 -mindepth 1 -path "*"  -type d -exec rm -rf ${ROOT_DIR}/{}/Makefile \;

	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec rm -rf ${ROOT_DIR}/{}/upload.sh \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec rm -rf ${ROOT_DIR}/{}/upload.sh \;

	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/v*_*' -type d -exec rm -rf ${ROOT_DIR}/{}/change_env.sh \;
	find . -maxdepth ${MODULE_DEPTH} -mindepth 2 -path '*/build*_*' -type d -exec rm -rf ${ROOT_DIR}/{}/change_env.sh \;









clean-%:
	$(info "----------------- start --------------------" $@)
	$(eval target=$(subst clean-,,$@))
	echo ${target}
	@find . -maxdepth 6 -mindepth 1 -path '*' -type f \
! -path '*/dist/*' \
! -path '*/venv/*' \
! -path '*/package/*' \
 -name '${target}' \
! -name 'test*' \
-exec sh -c 'echo --- $${1:2} \
' sh {} \;
	@find . -maxdepth 6 -mindepth 1 -path '*' -type f \
! -path '*/dist/*' \
! -path '*/venv/*' \
! -path '*/package/*' \
 -name '${target}' \
! -name 'test*' \
-exec sh -c 'rm $${1:2} \
' sh {} \; | echo ;
