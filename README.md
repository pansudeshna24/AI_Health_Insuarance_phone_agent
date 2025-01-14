# AI Phone Agent

## Overview
This project is an AI-powered phone agent that integrates with Twilio, OpenAI, and Google Translate to provide voice-based client interaction and management.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt


ai_phone_agent/
├── app.py                     # Flask/Twilio integration (handles incoming calls)
├── client_management.py       # Client handling logic (JSON-based storage)
├── config.json                # Configuration (API keys and Twilio settings)
├── features.json              # Policy and feature details (static data)
├── fine_tuning.py             # Fine-tuning dataset preparation (optional, if using custom fine-tuning)
├── payment_processing.py      # Logic for calculating and processing payments
├── requirements.txt           # Python dependencies (e.g., Flask, Twilio, OpenAI, Googletrans, etc.)
├── utils/
│   ├── translation_utils.py   # Helper functions for translations (Google Translate)
│   └── sentiment_analysis.py  # Helper functions for analyzing tone (TextBlob)
├── data/
│   ├── clients.json           # Client data in JSON format
│   ├── fine_tuning.jsonl      # Fine-tuning dataset
├── tests/
│   ├── test_client_management.py  # Unit tests for client management logic
│   ├── test_payment_processing.py # Unit tests for payment processing logic
│   └── test_translation_utils.py # Unit tests for translation and sentiment analysis
├── .env                       # Environment variables (e.g., API keys, Twilio SID)
├── .gitignore                 # Exclude sensitive files and folders from Git
└── README.md                  # Project documentation and instructions
