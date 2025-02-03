#!/bin/bash

# Fail immediately if any command fails
set -e

CKAN_CONTAINER="dcor-ckan-docker-ckan"
EXTENSION_NAME="ckanext-dcor_theme"  # Change this to your extension's name
EXTENSION_PATH="/srv/app/src_extensions/${EXTENSION_NAME}"

echo "Copying extension to the container..."
docker cp . ${CKAN_CONTAINER}:${EXTENSION_PATH}

echo "Creating a virtual environment inside the CKAN container..."
docker exec -it ${CKAN_CONTAINER} /bin/bash -c "
  cd ${EXTENSION_PATH};
  python3 -m venv venv;
  source venv/bin/activate;
  pip install --upgrade pip wheel;
  dcor update --yes;
  pip install .;
  pip install -r ./ckanext/dcor_theme/tests/requirements.txt;
"

echo "Running tests in the virtual environment..."
docker exec -it ${CKAN_CONTAINER} /bin/bash -c "
  cd ${EXTENSION_PATH};
  source venv/bin/activate;
  pytest --cov=/ckanext.dcor_theme --cov-omit="*tests*" -p no:warnings --cov-report=xml;
"

echo "Tests completed!"
