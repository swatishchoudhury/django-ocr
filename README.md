# OCR Date Extraction API

This project provides an API for extracting dates from images and PDFs using OCR technology.

## Features

- Extracts dates from images (JPG, JPEG, PNG) and PDF files
- Supports multiple date formats
- Returns all found dates in the document/image
- Secure API access with API key authentication

## Prerequisites

- Python 3.11 or higher
- Poppler (required for PDF processing)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/swatishchoudhury/django-ocr.git
   cd django-ocr
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and set all the required environment variables:
    A `.env.example` file is provided in the repository. Copy it to create your own `.env` file and customize the values according to your environment.

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage


### API Endpoint

The application provides a RESTful API endpoint for programmatic access.

**Endpoint:** `/api/extract-dob/`

**Method:** POST

**Headers:**
- `X-API-Key`: Your API key (required)
- `Content-Type`: multipart/form-data

**Request Body:**
- `image`: File (image or PDF)



## Project Structure

```
├── aadhar_ocr/         # Django project settings
├── ocr_app/            # Main application
│   ├── middleware.py   # API authentication middleware
│   └── views.py        # Request handlers
├── requirements.txt    # Python dependencies
└── manage.py           # Django management script
```

> [!NOTE]  
> This project was created as part of an assignment and is not intended for production use.  