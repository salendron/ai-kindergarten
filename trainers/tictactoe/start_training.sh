#!/bin/bash

current_date_time="`date +%Y%m%d%H%M%S`";
job_name="Job_$current_date_time"
model_version_name="model_$current_date_time"
echo $job_name;
echo $model_version_name;

gcloud ml-engine jobs submit training $job_name \
	--job-dir "gs://ai-kindergarten-models/$job_name" \
	--runtime-version 1.0 \
	--module-name trainer.train_job \
	--package-path ./trainer \
	--region europe-west1 \
	-- \
    --model_path "gs://ai-kindergarten-models/model.h5" \
    --identity_path "gs://ai-kindergarten-models/ds_identity.json"

echo "Waiting for model to be trained..."
sleep 3m

echo "Creating new model version..."
gcloud ml-engine versions create $model_version_name \
    --model tictactoe \
    --origin "gs://ai-kindergarten-models/$job_name" \
    --runtime-version 1.8

echo "Setting new model version as default..."
gcloud ml-engine versions set-default $model_version_name --model=tictactoe

echo "Cleaning up..."
gsutil rm -r gs://ai-kindergarten-models/$job_name

echo "Done!"
