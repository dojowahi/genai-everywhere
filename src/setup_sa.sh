#!/bin/bash

#####################################################################################################
# Script Name: setup_sa.sh
# Date of Creation: 7/26/2023
# Author: Ankur Wahi
# Updated: 7/26/2023
#####################################################################################################



source ./config.sh
gcloud auth login ${USER_EMAIL}
echo "Assigning IAM Permissions"
gcloud config set project ${PROJECT_ID}

##################################################
##
## Enable APIs
##
##################################################

echo "enabling the necessary APIs"

gcloud services enable compute.googleapis.com

gcloud services enable storage.googleapis.com

gcloud services enable bigquery.googleapis.com

gcloud services enable cloudfunctions.googleapis.com

gcloud services enable artifactregistry.googleapis.com

gcloud services enable run.googleapis.com

gcloud services enable cloudbuild.googleapis.com

gcloud services enable aiplatform.googleapis.com

PROJECT_NUMBER=$(gcloud projects list --filter="project_id:${PROJECT_ID}"  --format='value(project_number)')


SERVICE_ACCOUNT=${PROJECT_NUMBER}-compute@developer.gserviceaccount.com 
echo "Compute engine SA - ${SERVICE_ACCOUNT}"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=serviceAccount:${SERVICE_ACCOUNT} \
    --role=roles/serviceusage.serviceUsageAdmin

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=serviceAccount:${SERVICE_ACCOUNT} \
    --role=roles/aiplatform.admin

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=serviceAccount:${SERVICE_ACCOUNT} \
    --role=roles/storage.admin
    

sleep 15

# gcloud iam service-accounts keys create ~/eeKey.json --iam-account ${SERVICE_ACCOUNT}
# cd ~/
# cp eeKey.json ~/earth-engine-on-bigquery/src/cloud-functions/ndvi/
# cp eeKey.json ~/earth-engine-on-bigquery/src/cloud-functions/temperature/
# cp eeKey.json ~/earth-engine-on-bigquery/src/cloud-functions/crop/

# Cloud function setup for EE

project_id=${PROJECT_ID}
sa=${SERVICE_ACCOUNT}

echo "export SA=${sa}" >> ~/src/config.sh





