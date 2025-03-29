# AutoMeet 🚀

## 🎯 **About AutoMeet**
AutoMeet is a **meeting intelligence platform** that automates audio ingestion, transcription, and feedback analysis. It leverages:
- ✅ **Redis Streams** for real-time event-driven processing.
- ✅ **AWS S3-Compatible Storage** (Backblaze B2) for storing audio files and transcripts.
- ✅ **RunPod** for audio-to-text transcription.
- ✅ **GPT-4 / GPT-4 Mini** for generating intelligent insights, feedback, and summaries.

---

## 🔧 **Setup Instructions**

### 1️⃣ **Prerequisites**
To run AutoMeet, ensure you have the following:
- **Docker & Docker Compose**
- **Python 3.10+** (if running locally)
- **Backblaze B2 Account** (for S3 storage)
- **Redis Server** (for stream processing)
- **Terraform** (for provisioning Backblaze resources)

---

### 2️⃣ **Configure the Environment**
#### **Set Environment Variables**
You’ll need to define some environment variables before running `docker-compose up`:
```bash
export AUDIO_DIR=/Users/yourname/Music/Audio Hijack  # Update path as needed
```

Modify `docker-compose.yaml` to mount the audio directory:
```yaml
services:
  uploader:
    volumes:
      - "${AUDIO_DIR}:/mnt/audio"
```

Run `./scripts/setup.sh` to configure symlinks for **Audio Hijack** file watching.

---

#### **Provision Backblaze Resources with Terraform**
AutoMeet uses **Terraform** to provision Backblaze B2 storage and application keys.

1. Follow [Backblaze's Terraform Guide](https://www.backblaze.com/docs/cloud-storage-use-backblaze-b2-terraform) to set up your **B2 application key** and **bucket**.
2. Set the following environment variables:
```bash
export B2_APPLICATION_KEY_ID=<your_application_key_id>
export B2_APPLICATION_KEY=<your_secret_key>
```
3. Run Terraform:
```bash
terraform init
terraform apply -auto-approve
```
4. Save the generated credentials in `.secrets.yaml`:
```yaml
s3:
  application_key: <your_secret_key>
  application_key_id: <your_application_key_id>
```

---

### 3️⃣ **Run the Project**
```bash
docker-compose up -d
```

---

## 🔄 **How It Works**
AutoMeet is an **event-driven system** that automates audio uploads, transcriptions, and feedback analysis.

---

### **Core Workflow Overview**
1. 🎙️ **Audio Hijack** records a new audio file in the specified directory.
2. 📚 **`scripts/ah.js`** writes an entry to the journal.
3. 🔥 **Watcher Service** detects the new file and publishes a message to a **Redis Stream**.
4. 🚀 **Uploader Service** reads the message and uploads the file to **Backblaze B2**.
5. 📝 **Transcription Service (RunPod)** transcribes the audio and stores the transcript.
6. 🧠 **GPT Analysis Service** generates feedback, action items, and meeting summaries.

---

### 📊 **Intelligent Feedback & Insights**
AutoMeet extends beyond basic transcription to provide **AI-powered insights:**
- ✅ **Meeting Summaries & Titles** – Auto-generated by **GPT-4 Mini**.
- ✅ **Tech Lead Performance Feedback** – Evaluates if you acted like a senior engineer.
- ✅ **Action Item Extraction** – Identifies key takeaways and unresolved tasks.
- ✅ **Custom Prompts with GPT-4** – Ask questions like:
    - “Did I take ownership in this meeting?”
    - “What opportunities did I miss to delegate?”
- ✅ **Persistent Feedback Loop** – Save and retrieve meeting insights to create a **continuous growth loop**.

---

### ⚡️ **Advanced Workflow for Feedback & RAG**
1. 🤖 **Custom Prompts via UI:**  
   - Submit ad-hoc prompts directly in the meeting details page.
   - Save and persist feedback for future reference.

2. 🔁 **RAG-Enabled Context Retrieval:**  
   - Auto-fetch past meeting context to suggest relevant follow-ups.
   - Identify unfinished tasks and recommend them in the next 1-on-1.

3. 🎯 **Goal-Aware Suggestions:**  
   - Aligns feedback with your career goals (e.g., getting promoted to **G11**).
   - Nudges to mention stretch projects, leadership initiatives, and key actions.

---

## 🛠️ **Configuration**
- **Backblaze B2 Credentials:** Stored in `src/config/.secrets.yaml`.
- **Redis Streams:** Defined in `settings.yaml` under `redis.streams`.
- **Logging:** Configured in `src/shared/logging.py`.

---

## 📚 **Roadmap / TODOs**
✅ **Basic Audio Ingestion and Upload to B2**  
✅ **Integrate GPT-4 Mini for Summaries & Titles**  
✅ **Add Feedback System for Manual Prompts**  
✅ **RAG-Based Context Retrieval for Follow-Ups**  
✅ **Action Item Extraction and Carryover**  
⬜ **Meeting Insights Dashboard (Single & Multi-Meeting)**  
⬜ **Tech Lead Scorecard & Career Growth Tracking**  
⬜ **UI Enhancements for Feedback & Insights Display**  
⬜ **Automated Nudges Aligned with Promotion Goals**  
⬜ **Unit Tests & CI/CD Pipeline for Robustness**

---

## 🎉 **Current Features**
✅ **Audio File Upload & Transcription**  
✅ **Real-Time Redis Stream Processing**  
✅ **Backblaze B2 Storage Integration**  
✅ **Custom GPT-4 Prompting with Feedback Retention**  
✅ **Context-Aware Meeting Suggestions & Insights**

---

## 📜 **License**
[MIT License](LICENSE)

---

### ⚠️ **NOTE:** This README evolves as AutoMeet grows. New features and enhancements are added regularly. Stay tuned! 🛠️
---

### 🔥 **Pro Tip:**  
To maximize feedback quality and performance, configure **GPT-4 Mini** for quick tasks and **GPT-4** for in-depth insights.