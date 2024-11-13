import streamlit as st
import requests

# Base URL for the FastAPI backend
BASE_URL = "http://127.0.0.1:8001"

st.title("Academic Research Paper Assistant")

# Input for the research topic
topic = st.text_input("Enter Research Topic")

# Search Papers
st.header("Search Papers by Topic")
start_year = st.number_input("Start Year", min_value=1900, max_value=2100, value=2019, step=1)
if st.button("Search Papers"):
    response = requests.get(f"{BASE_URL}/search", params={"topic": topic, "start_year": start_year})
    if response.status_code == 200:
        papers = response.json().get("papers", [])
        st.write("Fetched Papers:")
        for paper in papers:
            st.write(f"**Title**: {paper['title']}")
            st.write(f"**Published**: {paper['published']}")
            st.write(f"**Summary**: {paper['summary']}")
            st.write(f"**URL**: [Link to Paper]({paper['url']})")
            st.write("\n")
    else:
        st.error("Failed to fetch papers")

# Summarize a Specific Paper
st.header("Summarize a Paper")
title_to_summarize = st.text_input("Enter the Title of the Paper to Summarize")
if st.button("Summarize Paper"):
    response = requests.get(f"{BASE_URL}/summarize", params={"title": title_to_summarize})
    if response.status_code == 200:
        summary = response.json().get("summary", "")
        st.write("Paper Summary:", summary)
    else:
        st.error("Failed to summarize paper")

# Question Answering on a Paper
st.header("Question Answering on a Paper")
title_for_qa = st.text_input("Enter the Title of the Paper for Q&A")
question = st.text_input("Ask a Question about the Paper")
if st.button("Get Answer"):
    response = requests.get(f"{BASE_URL}/question", params={"title": title_for_qa, "question": question})
    if response.status_code == 200:
        answer = response.json().get("answer", "")
        st.write("Answer:", answer)
    else:
        st.error("Failed to fetch answer")

# List Papers by Publication Year
st.header("List Papers by Publication Year")
year = st.number_input("Enter Year", min_value=1900, max_value=2100, value=2019, step=1)
if st.button("List Papers by Year"):
    response = requests.get(f"{BASE_URL}/papers_by_year", params={"year": year})
    if response.status_code == 200:
        papers = response.json().get("papers", [])
        st.write(f"Papers Published Since {year}:")
        for paper in papers:
            st.write(f"**Title**: {paper['title']}")
            st.write(f"**Summary**: {paper['summary']}")
            st.write("\n")
    else:
        st.error("Failed to fetch papers by year")

# Future Research Suggestions
st.header("Future Research Suggestions")
if st.button("Get Future Research Suggestions"):
    response = requests.get(f"{BASE_URL}/future_works")
    if response.status_code == 200:
        suggestions = response.json().get("suggestions", [])
        st.write("Future Research Suggestions:")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
    else:
        st.error("Failed to fetch future research suggestions")
