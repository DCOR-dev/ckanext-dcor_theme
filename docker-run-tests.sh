#!/bin/bash

# Fail immediately if any command fails
set -e

CKAN_CONTAINER="dcor-ckan-docker-ckan"
EXTENSION_NAME="ckanext-dcor_theme"  # Change this to your extension's name
EXTENSION_PATH="/srv/app/src_extensions/${EXTENSION_NAME}"
VENV_PATH="/srv/app/src_extensions/${EXTENSION_NAME}/venv"

echo "Copying extension to the container..."
docker cp ./${EXTENSION_NAME} ${CKAN_CONTAINER}:${EXTENSION_PATH}

echo "Creating a virtual environment inside the CKAN container..."
docker exec -it ${CKAN_CONTAINER} /bin/bash -c "
  python3 -m venv ${VENV_PATH};
  source ${VENV_PATH}/bin/activate;
  pip install --upgrade pip wheel;
  dcor update --yes;
  pip install ${EXTENSION_PATH};
  pip install -r ${EXTENSION_PATH}/ckanext/dcor_theme/tests/requirements.txt;
"

echo "Running tests in the virtual environment..."
docker exec -it ${CKAN_CONTAINER} /bin/bash -c "
  source ${VENV_PATH}/bin/activate;
  cd ${EXTENSION_PATH};
  pytest --cov=${EXTENSION_NAME}/ckanext.dcor_theme --cov-omit="*tests*" -p no:warnings --cov-report=xml;
"

echo "Tests completed!"
