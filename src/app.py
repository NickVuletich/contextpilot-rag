import streamlit as st

from pathlib import Path
from retrieve import retrieve_chunks
from generate import generate_answer
from store import ensure_vector_store

st.set_page_config(
    page_title="SourceRecall",
    layout="wide"
)


@st.cache_resource
def initialize_vector_store():
    ensure_vector_store()

initialize_vector_store()

st.title("SourceRecall")
st.write("Ask questions about your documents.")

with st.sidebar:
    st.header("Demo Document")
    st.write("OWASP Top 10 for LLM Applications 2025")

    st.subheader("Try asking")
    st.markdown("""
    - What is prompt injection?
    - What risks are caused by excessive agency?
    - What is sensitive information disclosure?
    - Why might pre-deployment testing fail to accurately represent how a generative AI system behaves in the real world?
    """)

    st.divider()

    st.header("Demo Document")
    st.write("Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile")
    
    st.subheader("Try asking")
    st.markdown("""
    - Why might pre-deployment testing fail to accurately represent how a generative AI system behaves in the real world?
    - What two primary information security risks does NIST identify for generative AI systems?
    - What does NIST mean by confabulation in a generative AI system?
        """)
    
    st.divider()
    st.caption("SourceRecall v2.0.1")

with st.form("query_form"):
    query = st.text_input("Ask a question")

    top_k = st.number_input(
        "Number of sources to retrieve (1-5)",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    submitted = st.form_submit_button("Ask SourceRecall")


if submitted:
    if query.strip():
        with st.spinner("Searching documents and generating answer..."):
            chunks = retrieve_chunks(query, top_k)
            answer = generate_answer(query, chunks)

        answer_col, sources_col = st.columns([2, 1])

        with answer_col:
            st.subheader("Answer")
            st.write(answer)

        with sources_col:
            st.subheader("Retrieved Sources")

            for chunk in chunks:
                filename = Path(chunk["metadata"]["source"]).name
                page = chunk["metadata"]["page"]
                distance = chunk["distance"]

                st.markdown(
                    f"**{filename}**  \n"
                    f"Page {page} | distance `{distance:.4f}`"
                )

    else:
        st.error("Please enter a question.")