# Vibe Coding Base App - AppWorld 2026

**This application is the product of vibe coding.**

## Overview
This application is a training tool for the AppWorld 2026 lab "Code. Secure. Repeat.". It demonstrates a "vibe-coded" base application—built quickly using AI assistance—to highlight common architectural and security tradeoffs that students will address throughout the lab.

### What is Vibe Coding?
Vibe coding is an AI-assisted development technique where developers build applications by conversing with an AI model rather than manually writing all code. It prioritizes speed and rapid prototyping, often at the expense of traditional software engineering rigor.

## Lab-Only Disclaimer
This application is for educational and security demonstration purposes only. It is intentionally configured with security weaknesses and should not be used in a production environment.

## Getting Started

### Local Development (Host Machine)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app/app.py
   ```
   *Note: Access the application at http://localhost:5001 (mapped locally).*

### Running in Container
1. Build the image:
   ```bash
   docker build -t vibe-base-app .
   ```
2. Run the container:
   ```bash
   docker run -p 5001:5000 vibe-base-app
   ```
   *Note: Container port 5000 is mapped to host port 5001.*

## Known Limitations & Security Gaps (Lab-Safe)
- **Missing Security Headers**: The application does not implement CSP, HSTS, or other defensive headers.
- **Verbose Error Messages**: Debug mode is enabled (documented for lab visibility) to demonstrate information disclosure.
- **No Rate Limiting**: Vulnerable to basic automated requests.
- **Read-Only**: No data persistence or interactive forms in this version.

## Testing
Run unit tests using pytest:
```bash
python -m pytest
```

---
*Developed for AppWorld 2026. Code. Secure. Repeat.*
