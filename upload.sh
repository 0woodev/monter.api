eval CURRENT_PATH=$(PWD)
eval ROOT_DIR=$(realpath ${CURRENT_PATH}/../../../)

# 만약, realpath command not found 가 뜨신다면, 아래명령어를 쳐주세요
# brew install coreutils

echo r "${ROOT_DIR}"
echo p "${PWD}"
echo m "${PWD##*/}"
module_name=${PWD##*/}
echo "${module_name}"
#module_name=${PWD##*/} | sed -e "s/-/_/g"
#echo "${module_name}"
#cat ../../../aws_account/project_name.txt
project_name=$(cat ${ROOT_DIR}/env/project_name.txt)
echo ${project_name}

echo ${project_name}_${module_name}
echo ${PWD}/dist/build.zip

#/Users/ihsong/Work/classu/backend.infra/python/authentication/v1_authorizer/dist/build.zip
aws lambda update-function-code \
    --function-name ${project_name}_${module_name} \
    --zip-file fileb://${PWD}/dist/build.zip \
    --output table --no-cli-pager


