
#!/bin/bash

#####################################################################################################
# Script Name: deploy.sh
# Date of Creation: 7/26/2023
# Author: Ankur Wahi
# Updated: 7/26/2023
#####################################################################################################

source ./config.sh
gcloud auth login ${USER_EMAIL}

gcloud config set project ${PROJECT_ID}
REPO_NAME=wahi-genai-demos
num=`echo $RANDOM`
rm -rf ~/genai-everywhere/src/.env
BUCKET_NAME=${PROJECT_ID}-wahi-${num}
echo "Creating bucket and repo"
gcloud storage buckets create gs://${BUCKET_NAME}
gcloud auth configure-docker us-central1-docker.pkg.dev

gcloud artifacts repositories create ${REPO_NAME} --project=${PROJECT_ID} --location=${REGION} --repository-format=docker
echo "Check if bucket ${BUCKET_NAME} and articfactory repo ${REPO_NAME} were created in project ${PROJECT_ID}"
echo "bucket_name = ${BUCKET_NAME}" > ~/genai-everywhere/src/.env
echo "project_id = ${PROJECT_ID}" >> ~/genai-everywhere/src/.env
echo "region = ${REGION}" >> ~/genai-everywhere/src/.env

cd ~/genai-everywhere

docker build -t "us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/ai-demos:1.0.0" -f src/Dockerfile .
docker push "us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/ai-demos:1.0.0"

gcloud run deploy ai-demos --image us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/ai-demos:1.0.0 --cpu 2 --memory 4G --allow-unauthenticated --region us-central1 --service-account ${SA}