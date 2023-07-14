
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
REPO_NAME=wahi_genai_demos
num=`echo $RANDOM`
BUCKET_NAME=${PROJECT_ID}_wahi_${num}
echo "Creating bucket and repo"
gcloud storage buckets create ${BUCKET_NAME}
gcloud artifacts repositories create ${REPO_NAME} --project=${PROJECT_ID} --location=${REGION} --repository-format=docker

echo "bucket_name = ${BUCKET_NAME}" > ~/src/.env
echo "project_id = ${PROJECT_ID}" >> ~/src/.env
docker build -t "us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/ai-demos:1.0.0" -f src/Dockerfile .
docker push "us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/ai-demos:1.0.0"

gcloud run deploy ai-demos --image us-central1-docker.pkg.dev/${PROJECT_ID}/genai/ai-demos:1.0.0 --cpu 2 --memory 4G --allow-unauthenticated --region us-central1 --service-account ${SA}