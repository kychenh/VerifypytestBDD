cd %~dp0
git status
git add --all -- :!allure/* :!traces/* :!videos/* :!test-results/* :!screenshoots/* :!.pytest_cache/*
git status
git commit -m "auto commit"
git push origin master
pause