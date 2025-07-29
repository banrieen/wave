
uv add label-studio[postgresql,s3] -i https://pypi.tuna.tsinghua.edu.cn/simple

## config postgres
CREATE USER labelstudio WITH ENCRYPTED PASSWORD 'labelstudio@2025';
CREATE DATABASE labelstudio;
GRANT ALL PRIVILEGES ON DATABASE labelstudio TO labelstudio;
\q

ALTER USER labelstudio WITH PASSWORD 'labelstudio+2025';


## config minio s3 bucket
export MINIO_ENDPOINT=http://localhost:9000

export MINIO_ACCESS_KEY=minioadmin

export MINIO_SECRET_KEY=minioadmin
mc mb $MINIO_ENDPOINT/labelstudio

label-studio start  -db 
--host 0.0.0.0 --port 8082 --username banrieen@163.com --password thomas@2025 

DJANGO_DB=default
POSTGRE_NAME=postgres
POSTGRE_USER=labelstudio
POSTGRE_PASSWORD=labelstudio+2025
POSTGRE_PORT=5432
POSTGRE_HOST=localhost

export LABEL_STUDIO_STORAGE_TYPE=s3
export AWS_ACCESS_KEY_ID=yx0RCaaF6wj9wm9Z506x
export AWS_SECRET_ACCESS_KEY=EzQZ9nxDe58CrdWlqFr7TQObAMRQLsVACZCTh6tj
export LABEL_STUDIO_STORAGE_BUCKET=labelstudio
export LABEL_STUDIO_STORAGE_S3_ENDPOINT=http://localhost:9000

export LABEL_STUDIO_STORAGE_TYPE=s3
export AWS_ACCESS_KEY_ID=Snpo5z37BcQ0eX01bKxa
export AWS_SECRET_ACCESS_KEY=WlyDiExf9GRBzkoK6pzXAPwwq622DnYsbQtJeCaS
export LABEL_STUDIO_STORAGE_BUCKET=labelstudio
export LABEL_STUDIO_STORAGE_S3_ENDPOINT=http://localhost:9000

label-studio start OCR --init -db postgresql

    "detail": "Sentry dropped data due to a quota or internal rate limit being reached. This will not affect your application. See https://docs.sentry.io/product/accounts/quotas/ for more information."

MINIO_ROOT_USER=thomas
MINIO_ROOT_PASSWORD=thomas@2025