Here's a comprehensive `README.md` file for your project, detailing the setup, usage, and functionality of the Search Agent:

---

# Search Agent: Text-to-SQL Research Paper Collector

This Search Agent is a FastAPI-based backend application that fetches recent research papers on **text-to-SQL** from platforms like **Arxiv**, focuses on publications from the last five years, and stores them in both **Neo4j** (for graph-based queries) and **InfluxDB** (for time-series queries).

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [License](#license)

---

## Features

- **Fetch Recent Papers**: Fetch research papers on "text-to-SQL" published within the last five years from Arxiv.
- **Store in Databases**:
  - **Neo4j** for relational queries and graph-based analysis.
- **Summarization and Q&A**: Summarize paper content and answer questions about specific papers using transformer models.
- **Data Retrieval**: Retrieve papers by publication year, topic, or recommended future research directions.

## Installation

### Prerequisites

- **Python 3.7+**
- **Neo4j** (installed and running locally or on a server)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd search-agent
```

### Step 2: Install Required Packages

Use `pip` to install dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Neo4j and InfluxDB

1. **Neo4j Setup**:
   - Start your Neo4j instance and set up a database for this project.
   - Note the connection URI, username, and password, as you'll need to configure these in the code.

## Configuration

1. **Neo4j Configuration**:
   Update the following Neo4j credentials in the backend code (`backend_app.py`):
   
   ```python
   neo4j_uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
   neo4j_user = "neo4j"  # Replace with your Neo4j username
   neo4j_password = "password"  # Replace with your Neo4j password
   ```

## Endpoints

| Method | Endpoint              | Description                                      |
|--------|------------------------|--------------------------------------------------|
| GET    | `/search_text_to_sql`  | Fetch and store recent papers on "text-to-SQL".  |
| GET    | `/summarize`           | Summarize a specific research paper by title.    |
| GET    | `/question`            | Ask a question about a specific paper by title.  |
| GET    | `/papers_by_year`      | List papers published after a specific year.     |
| GET    | `/future_works`        | Retrieve suggestions for future research areas.  |

## Usage

### Step 1: Start the FastAPI Server

To run the FastAPI backend, execute:

```bash
uvicorn backend_app:app --reload --host 127.0.0.1 --port 8001
```

### Step 2: Use the Endpoints

1. **Fetch and Store Papers**:
   - Go to: `http://127.0.0.1:8001/search_text_to_sql`
   - This endpoint will fetch recent "text-to-SQL" papers from Arxiv (from the last 5 years) and store them in Neo4j and InfluxDB.

2. **Summarize a Paper**:
   - Go to: `http://127.0.0.1:8001/summarize?title=<PAPER_TITLE>`
   - This endpoint summarizes the content of a specific paper by title.

3. **Question Answering**:
   - Go to: `http://127.0.0.1:8001/question?title=<PAPER_TITLE>&question=<YOUR_QUESTION>`
   - This endpoint provides an answer to a question based on the content of the specified paper.

4. **Retrieve Papers by Year**:
   - Go to: `http://127.0.0.1:8001/papers_by_year?year=<YEAR>`
   - This endpoint lists all papers published after the specified year.

5. **Get Future Research Suggestions**:
   - Go to: `http://127.0.0.1:8001/future_works`
   - This endpoint returns pre-defined suggestions for future research areas.

## Example Queries

Here are some example queries to test the API:

1. **Fetch Recent Papers**:
   ```
   GET http://127.0.0.1:8001/search_text_to_sql
   ```

2. **Summarize a Specific Paper**:
   ```
   GET http://127.0.0.1:8001/summarize?title=Research%20on%20text-to-SQL%20Models
   ```

3. **Ask a Question about a Paper**:
   ```
   GET http://127.0.0.1:8001/question?title=Research%20on%20text-to-SQL%20Models&question=What%20are%20the%20main%20findings?
   ```

4. **List Papers by Year**:
   ```
   GET http://127.0.0.1:8001/papers_by_year?year=2020
   ```

## License

This project is licensed under the MIT License.

---

This README provides detailed setup instructions, configuration steps, usage guidelines, and example queries to help you get started with your Search Agent backend. Let me know if you need further customization!
