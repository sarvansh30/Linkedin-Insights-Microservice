# LinkedIn Insights Microservice

This repository contains a microservice that retrieves and analyzes LinkedIn page data. It uses FastAPI, MongoDB, Redis, and an AI service(Mistral.ai API ) to generate summaries.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
  - [Create and Activate a Virtual Environment](#create-and-activate-a-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Environment Variables](#environment-variables)
- [Running the Microservice](#running-the-microservice)
- [Endpoints](#endpoints)

## Overview

The microservice retrieves LinkedIn page data and, if not available locally in the database, scrapes the data. It also generates AI summaries using caching for better performance.

## Setup

### Create and Activate a Virtual Environment

Run the following commands in your terminal:

```bash
python -m venv myenv
source myenv/bin/activate  # On Linux/Mac
# On Windows: myenv\Scripts\activate
```

### Install Dependencies

Once your virtual environment is active, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a file named `.env` in the server folder (or where your `main.py` is located) and add the following variables:

```ini
MONGO_URL=mongodb://localhost:27017/
DB_NAME=linkedin_insights_microservice
API_KEY=<YOUR_MISTRAL_AI_API_KEY>
```

- **MONGO_URL**: Connection string to your MongoDB instance.
- **DB_NAME**: Name of the MongoDB database you want to use.
- **API_KEY**: API key obtained from Mistral.ai (or any other provider).

## Running the Microservice

1. **Start MongoDB**  
   Ensure your MongoDB server is running locally (or remotely if using a hosted MongoDB instance).

2. **Start Redis**  
   Make sure your Redis server is running on the default port 6379. If you’re using a different host or port, update your configuration accordingly.

3. **Run the FastAPI Server**  
   Inside the server directory (or wherever your `main.py` is located), run:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   The service should now be available at [http://localhost:8000](http://localhost:8000).

## Endpoints

### GET /pages/{page_id}

Retrieves (or scrapes, if not found in the database) the LinkedIn page data for the specified `page_id`.

- **Example Request:**

  ```bash
  GET http://localhost:8000/pages/linkedin
  ```

- **Example Response:**

  ```json
  {
    "page_id": "linkedin",
    "name": "LinkedIn",
    "industry": "Internet",
    "followers": 30000000
    // ... other data
  }
  ```

### GET /ai-summary/{page_id}

Generates an AI summary of the company data for the specified `page_id` and uses caching to improve performance.

- **Example Request:**

  ```bash
  GET http://localhost:8000/ai-summary/linkedin
  ```

- **Example Response:**

  ```json
  {
    "page_id": "linkedin",
    "summary": "LinkedIn is a professional networking platform that connects..."
  }
  ```

### GET /pages

Allows you to search for pages by name, industry, or follower range. Supports pagination via `limit` and `offset`.

- **Query Parameters:**
  - `name`: Search by name (optional).
  - `industry`: Search by industry (optional).
  - `followers_min`: Minimum follower count (optional).
  - `followers_max`: Maximum follower count (optional).
  - `limit`: Number of results per page (optional, default: 10).
  - `offset`: Offset for pagination (optional, default: 0).

- **Example Request:**

  ```bash
  GET http://localhost:8000/pages?industry=Internet&limit=20&offset=0
  ```
