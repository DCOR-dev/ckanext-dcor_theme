#!/bin/bash

# Fail immediately if any command fails
set -e

EXTENSION_NAME="ckanext-dcor_theme"  # Change this to your extension's name
CKAN_CONTAINER="${EXTENSION_NAME}-dcor-test-1"
EXTENSION_PATH="/srv/app/src_extensions"

echo "Creating a virtual environment inside the CKAN container..."
docker exec ${CKAN_CONTAINER} bash -c "
  cd ${EXTENSION_PATH};
  python3 -m venv --system-site-packages venv;
  source venv/bin/activate;
  pip install --upgrade pip wheel;
  dcor update --yes;
  pip install .;
  pip install -r ./ckanext/dcor_theme/tests/requirements.txt;
"

echo "Running tests in the virtual environment..."
docker exec ${CKAN_CONTAINER} bash -c "
  cd ${EXTENSION_PATH};
  source venv/bin/activate;
  coverage run --source=ckanext.dcor_theme --omit=*tests* -m pytest -p no:warnings ckanext;
  coverage xml
"

echo "Tests completed!"
