# Cloud File Storage System ☁️

A full-stack, cloud-based file management application that allows users to securely upload, view, download, and delete files. 

The backend is built with Python and Flask, integrating directly with Amazon S3 via the Boto3 SDK to handle secure file streaming and storage. The frontend is a responsive, single-page application built with HTML, Vanilla JavaScript, and Tailwind CSS.

## 🚀 Features

* **Direct-to-Cloud Uploads:** Streams files directly to AWS S3 using `upload_fileobj`, minimizing local server memory and disk usage.
* **Secure Downloads:** Utilizes AWS Pre-signed URLs to generate temporary, secure download links that automatically expire after 1 hour.
* **Access Control & Security:** 
  * Implements strict IAM least-privilege policies.
  * Validates file types and enforces a 16MB `MAX_CONTENT_LENGTH` payload limit.
  * Uses `secure_filename` to prevent directory traversal attacks.
* **Modern UI:** Clean, responsive interface that consumes the REST API asynchronously using the JavaScript `fetch` API.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Werkzeug
* **Cloud Infrastructure:** Amazon S3, AWS IAM, Boto3 (AWS SDK for Python)
* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (via CDN)
* **Security:** `python-dotenv` for environment variable management

## 📸 Application Interface

*(Note to reviewers: Place a screenshot of your web interface here)*
![App Screenshot](link_to_your_screenshot_image.png)

## 💻 Local Setup Instructions

Follow these steps to run the application on your local machine.

### 1. Prerequisites
* Python 3.x installed
* An AWS Account with an active S3 Bucket
* An IAM User with programmatic access and a policy granting `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`, and `s3:ListBucket` for your specific bucket.

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name