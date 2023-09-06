@echo off
echo PROJECT_NAME = "Module" > .env
echo log_mode="trace" >> .env
SET ROOT_DIR=%CD%
echo ROOT_DIR=%ROOT_DIR% >> .env
echo CONFIG_DIR = %ROOT_DIR%\config >> .env
echo SETTING_DIR = %ROOT_DIR%\config\settings >> .env
echo INSTRUCTION_DIR = %ROOT_DIR%\instructions >> .env
echo LOG_DIR =  %ROOT_DIR%\log\${PROJECT_NAME} >> .env
echo TEST_CONFIG_DIR = %ROOT_DIR%\config\test >> .env