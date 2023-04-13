echo "${PWD}"
echo "${PWD##*/}"
module_name=${PWD##*/}
echo "${module_name}"
#module_name=${PWD##*/} | sed -e "s/-/_/g"
#echo "${module_name}"
#cat ../../../aws_account/project_name.txt
project_name=$(cat ../../../aws_account/project_name.txt)
echo ${project_name}

echo ${project_name}_${module_name}
echo ${PWD}/dist/build.zip

#/Users/ihsong/Work/classu/backend.infra/python/authentication/v1_authorizer/dist/build.zip
aws lambda update-function-configuration \
    --environment { \
  "Variables": { \
    "root_log_level": "WARNING", \
    "log_level": "INFO", \
    "console_log_level": "ERROR", \
  } \
} \
    --output table --no-cli-pager

if [ -d test ]; then \
    make health-test; \
else \
    echo test/test_api_health.py 가 없습니다. 그래서 테스트 스킵
fi;
