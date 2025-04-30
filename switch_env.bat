@echo off
setlocal enabledelayedexpansion

echo 环境切换工具
echo ===============================
echo 1. 开发环境 (.env)
echo 2. 测试环境 (.env.test)
echo 3. 生产环境 (.env.production)
echo ===============================
set /p choice=请选择要切换的环境 (1-3): 

if "%choice%"=="1" (
    set env_file=.env
    set env_name=开发环境
) else if "%choice%"=="2" (
    set env_file=.env.test
    set env_name=测试环境
) else if "%choice%"=="3" (
    set env_file=.env.production
    set env_name=生产环境
) else (
    echo 无效的选择！
    goto end
)

if not exist %env_file% (
    echo 错误：%env_file% 文件不存在！
    goto end
)

echo 正在切换到%env_name%...
copy /Y .env .env.backup 2>nul
copy /Y %env_file% .env
echo 环境已切换到%env_name%

:end
pause
