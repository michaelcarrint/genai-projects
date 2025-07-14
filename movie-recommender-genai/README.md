# 🎬 Movie Recommender GenAI Project

This is a simple **Movie Recommendation System** powered by 
**Retrieval-Augmented Generation (RAG)** and **vector embeddings**. It was 
built as part of my learning journey through the **Orchestrating GenAI 
Workflows** course by DeepLearning.AI.

---

## 💡 Project Overview

This project helps you get **movie recommendations** based on natural 
language queries. It:
- ✅ Uses the **BAAI/bge-small-en-v1.5** embedding model to create text 
vector representations.
- ✅ Stores the vectorized data in a **Weaviate vector database**.
- ✅ Retrieves the most relevant movie based on **semantic similarity**.
- ✅ Demonstrates how to combine **embedding models**, **vector stores**, 
and **natural language queries** into a simple GenAI application.

---

## 🛠️ Tech Stack

- **Python** 🐍
- **Weaviate** (local embedded instance)
- **FastEmbed** (for generating embeddings)
- **BAAI/bge-small-en-v1.5** embedding model
- **RAG workflow** for semantic search

---

## 📁 Project Structure

movie-recommender-genai/
│
├── include/
│ └── Movie_file/ # Folder containing movie description text files
│
├── helper.py # Helper functions (e.g., suppress_output)
├── main.py # Main Python script running the full RAG pipeline
├── requirements.txt # Python dependencies
└── README.md # Project documentation (this file)


---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/genie-projects.git
   cd genie-projects/movie-recommender-genai

Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies:
pip install -r requirements.txt
Run the app:
python main.py
Example query (inside main.py):
query_str = "Show me recent sci-fi thrillers"
📝 Example Output

==================================================
🎬 Title: Dune: Part Two
🎥 Director: Denis Villeneuve
📜 Description: Paul Atreides unites with the Fremen to wage war and 
fulfill his destiny on Arrakis.
📅 Year: N/A
🎭 Genre: 
==================================================
🎉 What I Learned

Setting up a RAG pipeline end-to-end
Using Weaviate for storing and querying vector embeddings
Applying BAAI/bge-small-en-v1.5 to embed movie descriptions
Designing simple GenAI applications for real-world use cases
📌 Notes

This project is meant for learning purposes and can be extended with:

🎁 More metadata like year, genre, rating
🖥️ Front-end integration (e.g., Streamlit app)
🔍 Multi-query or chat-based interactions
🙋‍♂️ About Me

I'm learning how to orchestrate GenAI applications step by step, applying 
concepts like RAG, embeddings, and vector databases through small 
projects.

⭐️ Acknowledgements

Inspired by:

DeepLearning.AI - Orchestrating GenAI Workflows
Open-source tools like Weaviate, FastEmbed, and BAAI embeddings

