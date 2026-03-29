# till will not be released poetry plugins to get possible add custom steos in build process
# https://github.com/python-poetry/poetry/pull/3733
rm -r dist
poetry build
twine check dist/*
