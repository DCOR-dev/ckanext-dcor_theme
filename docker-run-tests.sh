#!/bin/bash

# Fail immediately if any command fails
set -e

EXTENSION_NAME="ckanext-dcor_theme"  # Change this to your extension's name
CKAN_CONTAINER="${EXTENSION_NAME}-dcor-test-1" # ckan ontainer name
EXTENSION_PATH="/srv/app/src_extensions"

# Create venv and install dependencies as a root user inside the container
docker exec -u root ${CKAN_CONTAINER} bash -c "
  cd ${EXTENSION_PATH};
  python3 -m venv --system-site-packages venv;
  source venv/bin/activate;
  pip install --upgrade pip wheel;
  dcor update --yes;
  pip install .;
  pip install -r ./ckanext/dcor_theme/tests/requirements.txt;
"

# Run tests as a ckan user
echo "Running tests in the virtual environment..."
docker exec -u ckan ${CKAN_CONTAINER} bash -c "
  cd ${EXTENSION_PATH};
  source venv/bin/activate;
  coverage run --source=ckanext.dcor_theme --omit=*tests* -m pytest -p no:warnings ckanext;
  coverage xml
"

echo "Tests completed!"
