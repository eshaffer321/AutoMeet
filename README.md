# AutoMeet

## 🚀 About AutoMeet
AutoMeet is a tool for automating audio file uploads and processing using Backblaze B2 storage. This project integrates with **Redis Streams** and **AWS S3-compatible storage** (Backblaze B2) to handle audio file ingestion and storage.


## 🔧 Setup Instructions
### 1️⃣ Prerequisites
- **Docker & Docker Compose**
- **Python 3.10+** (if running locally)
- **Backblaze B2 Account** (for S3 storage)
- **Redis Server** (for stream processing)
- **Terraform** (for provisioning Backblaze resources)

### 2️⃣ Configure the Environment
#### **Set Environment Variables**
You need to set environment variables before running `docker-compose up`. These include:
```bash
export AUDIO_DIR=/Users/yourname/Music/Audio Hijack  # Update this path accordingly
```
Modify `docker-compose.yaml` to mount the audio directory:
```yaml
services:
  uploader:
    volumes:
      - "${AUDIO_DIR}:/mnt/audio"
```

#### **Provision Backblaze Resources with Terraform**
AutoMeet uses **Terraform** to create the required **Backblaze B2 storage and application keys**.

1. Follow [Backblaze's Terraform guide](https://www.backblaze.com/docs/cloud-storage-use-backblaze-b2-terraform) to set up your **B2 application key** and **bucket**.
2. Ensure you have the following environment variables set before running Terraform:
   ```bash
   export B2_APPLICATION_KEY_ID=<your_application_key_id>
   export B2_APPLICATION_KEY=<your_secret_key>
   ```
3. Run Terraform to provision resources:
   ```bash
   terraform init
   terraform apply -auto-approve
   ```
4. Once Terraform creates the **application key and bucket**, store them in a `.secrets.yaml` file under `src/config/`:
   ```yaml
   s3:
     application_key: <your_secret_key>
     application_key_id: <your_application_key_id>
   ```

### 3️⃣ Run the Project
```bash
docker-compose up -d
```

## 🔄 How It Works
AutoMeet is an **event-driven system** that watches for **new local audio files**, uploads them to **S3 (Backblaze B2)**, and eventually processes them for transcription (work in progress).

### **Workflow Overview**
1. **Audio Hijack** records an audio file in the specified directory.
2. **`scripts/ah.js`** writes an entry to the journal.
3. **Watcher service** detects the new entry and publishes a Redis Stream message.
4. **Uploader service** reads the message and uploads the file to Backblaze B2.
5. **(Planned)** The file gets transcribed using RunPod.

### **Configuring Audio Hijack**
- You need **Audio Hijack** (or an equivalent system) to generate audio files.
- **Update `scripts/ah.js`** to reflect the correct base path for your local **AutoMeet repo**.

## 🛠️ Configuration
- **Backblaze B2 Credentials:** Stored in `src/config/.secrets.yaml`.
- **Redis Streams:** Defined in `settings.yaml` under `redis.streams`.
- **Logging:** Configured in `src/shared/logging.py`.

## 🚀 Roadmap / TODOs
✅ Implement Redis stream processing
✅ Integrate Backblaze B2 via `boto3`
⬜ Improve logging & error handling
⬜ Implement audio file post-processing (e.g., transcription via RunPod)
⬜ Add unit tests & CI/CD pipeline

## 📜 License
[MIT License](LICENSE)

---

### ⚠️ NOTE: This README is a Work in Progress! 🛠️
This is just a starting point and needs updates as the project evolves. Feel free to refine and expand it!

