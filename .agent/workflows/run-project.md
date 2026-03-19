---
description: how to run the project
---

Follow these steps to run the Intelligent Document Verification System.

### Prerequisites

Ensure you have Python 3.8+ and Node.js installed.

### 1. Backend Setup

1. Open a terminal and navigate to the `backend` directory:
   ```powershell
   cd backend
   ```
2. Create and activate a virtual environment (if not already done):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with your **Google API Key**.
5. Start the Flask server:
   ```powershell
   python app.py
   ```
   The backend will run on `http://localhost:5000`.

### 2. Frontend Setup

1. Open a **new** terminal and navigate to the `frontend` directory:
   ```powershell
   cd frontend
   ```
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Start the Vite development server:
   ```powershell
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

### 3. Usage

Access the web interface at `http://localhost:5173`, upload a document, and view the verification results!
