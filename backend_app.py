import uvicorn
from fastapi import FastAPI
from transformers import pipeline
from neo4j import GraphDatabase
import arxiv

import os

os.environ["CURL_CA_BUNDLE"] = ""

app = FastAPI()

# Neo4j configuration
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "123456789"
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Initialize Transformers Pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

qa_pipeline = pipeline("question-answering")


# Function to Fetch Papers from Arxiv
def fetch_papers_from_arxiv(topic, max_results=5, start_year=None):
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in search.results():
        # Filter by year if specified
        if start_year and result.published.year < start_year:
            continue
        paper_info = {
            "title": result.title,
            "summary": result.summary,
            "published": result.published.year,
            "url": result.entry_id
        }
        papers.append(paper_info)
    return papers


def store_paper_in_neo4j(title, summary, published, url):
    with driver.session() as session:
        session.run(
            """
            MERGE (p:Paper {title: $title})
            SET p.summary = $summary, p.published = $published, p.url = $url
            """,
            title=title, summary=summary, published=published, url=url
        )


# Function to Fetch Paper from Database
def fetch_paper_from_db(title):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Paper {title: $title}) RETURN p.title AS title, p.summary AS summary",
            title=title
        )
        record = result.single()
        if record:
            return {"title": record["title"], "summary": record["summary"]}
    return None


@app.get("/search")
def search_papers(topic: str, start_year: int = None):
    papers = fetch_papers_from_arxiv(topic, max_results=5, start_year=start_year)

    # Save fetched papers to Neo4j
    for paper in papers:
        store_paper_in_neo4j(
            title=paper["title"],
            summary=paper["summary"],
            published=paper["published"],
            url=paper["url"]
        )

    return {"papers": papers}


# Endpoint: Summarize Research Paper
@app.get("/summarize")
def summarize_paper(title: str):
    paper = fetch_paper_from_db(title)
    if paper:
        input_length = len(paper["summary"].split())

        # Handle very short inputs
        if input_length < 20:
            return {"title": title, "summary": "The text is too short to summarize meaningfully."}

        max_length = min(100, int(input_length * 0.75))  # Adjust max_length based on input length
        min_length = min(20, max_length // 2)  # Set min_length to half of max_length, up to 20

        summary = summarizer(paper["summary"], max_length=max_length, min_length=min_length, do_sample=False)
        return {"title": title, "summary": summary[0]["summary_text"]}
    return {"error": "Paper not found"}


# Endpoint: Answer Questions about Papers
@app.get("/question")
def question_answering(title: str, question: str):
    paper = fetch_paper_from_db(title)
    if paper:
        answer = qa_pipeline(question=question, context=paper["summary"])
        return {"title": title, "question": question, "answer": answer["answer"]}
    return {"error": "Paper not found"}


# Endpoint: List Papers by Year
@app.get("/papers_by_year")
def list_papers_by_year(year: int):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Paper) WHERE p.published >= $year RETURN p.title AS title, p.summary AS summary",
            year=year
        )
        papers = [{"title": record["title"], "summary": record["summary"]} for record in result]
    return {"papers": papers}


# Endpoint: Recommend Future Works
@app.get("/future_works")
def future_works():
    suggestions = [
        "Develop scalable RLHF methods.",
        "Improve transparency in LLM decision-making.",
        "Create better evaluation metrics for safety.",
    ]
    return {"suggestions": suggestions}


# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
