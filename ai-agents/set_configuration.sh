# Set the active project
export PROJECT_ID="ai-automation-458319"
gcloud config set project $PROJECT_ID

# Enable APIs (Vertex AI, BigQuery, GCS, and Service Usage)
gcloud services enable aiplatform.googleapis.com \
                       bigquery.googleapis.com \
                       storage.googleapis.com \
                       serviceusage.googleapis.com

# Create the Service Account
SA_NAME="ai-sa-admin"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $SA_NAME --display-name="AI Automation SA"

# Assign Roles (The "Power Trio" + MCP Gateway Access)
ROLES=(
    "roles/storage.objectViewer"              # Discovery: Scan GCS for .gz files
    "roles/bigquery.dataEditor"               # Execution: Create/Modify staging tables
    "roles/bigquery.jobUser"                  # Execution: Run SQL queries
    "roles/serviceusage.serviceUsageConsumer" # Infrastructure: Authorize API calls
    "roles/iam.serviceAccountTokenCreator"    # Authentication: Required for MCP Registry
    "roles/aiplatform.user"                   # AI Platform
)

for ROLE in "${ROLES[@]}"; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
      --member="serviceAccount:$SA_EMAIL" \
      --role="$ROLE"
done

# Create the JSON Key
gcloud iam service-accounts keys create ~/.gcp/$SA_NAME-key.json \
    --iam-account=$SA_EMAIL

RESOURCE_LABEL="mta_dev_ai"
REGION="us-central1"

# Create the GCS Bucket (Regional to match Vertex AI)
# Note: Bucket names must be globally unique
export BUCKET_NAME=$RESOURCE_LABEL
gcloud storage buckets create gs://$RESOURCE_LABEL --location=$REGION

# create the BigQuery Dataset
gcloud bq datasets create $RESOURCE_LABEL --location=$REGION