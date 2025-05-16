# AutoMeet 🚀

## 🛑 Project Sunset Notice (May 2025)

This project has been **officially sunset** as of May 2025.

While it successfully delivered a fully functional meeting transcription pipeline,  
I have since migrated to **Notion AI**, which now provides the same experience  
natively where I already work, with better UX and zero maintenance.

---

## 🏆 Sunset Summary

### ✅ What I Built
- End-to-end system capturing meeting audio, transcribing via Runpod, storing transcripts in B2 and Supabase, and presenting them in a custom UI.
- Operational infrastructure including Hetzner VM, Redis Streams, Postgres (Supabase), B2 storage, domain management, and HTTPS via Cloudflare Tunnels.

### ✅ What It Solved
- Frictionless capture of meeting transcripts without requiring platform-specific integrations like Zoom or Webex.
- Local-first control over transcription, storage, and analysis.

### ❌ Why I Shut It Down
- Notion AI now provides the same experience where I already take notes and prepare meetings.
- The operational cost—both time and money—no longer makes sense for a single user.
- I no longer need to maintain my own transcription stack.

### 🗂️ What I'm Keeping (For Now)
- Passive archive in **B2 storage** and **Supabase**.
- Local UI can be spun up on-demand to access historical transcripts.

> Mission accomplished. Window closed. Time to move on.

---

## 📝 Historical Description

AutoMeet was a personal meeting transcription platform that automated:
- **Audio capture**
- **Transcription via Runpod**
- **Storage in B2 and Supabase**
- **Display via a custom web UI**

It included integrations with:
- **Redis Streams** for event processing
- **Backblaze B2** for audio and transcript storage
- **Supabase Postgres** for metadata storage
- **GPT-4 prompting** for meeting summaries and feedback

While functional, this system is now **deprecated** in favor of **Notion AI**.

---