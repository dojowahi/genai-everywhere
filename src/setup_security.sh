#!/bin/bash
REGION="us-central1"
PROJECT_ID=$(gcloud config get-value project)
echo PROJECT_ID=$PROJECT_ID

# project number
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(project_number)")

SERVICE_NAME="filesystem-app"
BASE_DOMAIN="endpoints.${PROJECT_ID}.cloud.goog"
## TODO if there is a need to move away from Cloud Endpoints, consider either Cloud DNS or nip.io
# Can use something like service-ip.nip.io or service-iphex.nip.io
# printf '%02X' 192 168 1 128 | tr '[:upper:]' '[:lower:]'

FQDN="${SERVICE_NAME}.${BASE_DOMAIN}"
#BRAND_TITLE=${SERVICE_NAME}
BRAND_TITLE="run"

# IAP settings
# this is a support email needed by IAP setup
SUPPORT_EMAIL="$(gcloud config get-value account)" ## use your current account
# or it can be another group address in your domain
#SUPPORT_EMAIL="support-group@kayunlam.altostrat.com"

# https://cloud.google.com/load-balancing/docs/quotas#ssl_certificates
# Domain name for Google-managed certificates has to be <= 63 characters
# This length limit only applies to Google-managed SSL certificates. In those certificates, the 64-byte limit only applies to the first domain in the certificate. The length limit for the other domains in the certificate is 253 (which applies to any domain name on the internet, and isn't specific to Google-managed certificates.
# To avoid hitting this limit, this guide always tries to set up a shorter domain
CERT_DOMAIN="cert.$BASE_DOMAIN"
echo CERT_DOMAIN="$CERT_DOMAIN"
if [ ${#CERT_DOMAIN} -gt 64 ]; then echo "The CERT_BASE_DOMAIN must be no longer than 64 characters. https://cloud.google.com/load-balancing/docs/quotas#ssl_certificates"; fi

echo FQDN="$FQDN"
if [ ${#FQDN} -gt 253 ]; then echo "The FQDN must be no longer than 253 characters. https://cloud.google.com/load-balancing/docs/quotas#ssl_certificates"; fi
