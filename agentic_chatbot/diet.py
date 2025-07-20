import streamlit as st
import google.generativeai as genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import PyPDF2

# Configure Gemini API
genai.configure(api_key= Gemini API_KEY ")  # Replace with your Gemini key
model = genai.GenerativeModel("gemini-1.5-pro")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Diet knowledge base
diet_knowledge = [
    "For iron, vegetarians can eat lentils, spinach, and fortified cereals.",
    "People with diabetes should prefer complex carbs and fiber-rich foods.",
    "Avoid red meat and high cholesterol foods for heart patients.",
    "Include Omega-3 foods like salmon and flaxseeds for heart health.",
    "Weight loss diet includes calorie deficit, high-protein and veggies.",
    "High protein foods: eggs, tofu, legumes, chicken, Greek yogurt.",
]

diet_embeddings = embedding_model.encode(diet_knowledge)
dimension = diet_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(diet_embeddings))

# Read uploaded file
def read_file(file):
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    else:
        text = file.read().decode("utf-8")
    return text

# Gemini-based generation
def generate_diet_plan(user_text):
    query_embedding = embedding_model.encode([user_text])
    D, I = index.search(np.array(query_embedding), k=3)
    context = "\n".join([diet_knowledge[i] for i in I[0]])

    prompt = f"""You are a smart dietary assistant. Based on the user's profile and the context below, generate a personalized diet plan.

User Info:
{user_text}

Relevant Knowledge:
{context}

Provide a customized and friendly diet plan:
"""

    response = model.generate_content(prompt)
    return response.text

# Streamlit interface
st.title("🥗 Personalized Diet Plan Generator (Gemini-powered RAG)")

uploaded_file = st.file_uploader("Upload your health profile (PDF or TXT)", type=["txt", "pdf"])
if uploaded_file:
    user_text = read_file(uploaded_file)
    st.subheader("📄 Your Health Info:")
    st.text(user_text)

    if st.button("Generate Diet Plan"):
        with st.spinner("Thinking..."):
            plan = generate_diet_plan(user_text)
        st.subheader("🍽️ Your Diet Plan:")
        st.markdown(plan)


