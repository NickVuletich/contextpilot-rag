import streamlit as st
from pathlib import Path

from retrieve import retrieve_chunks
from generate import generate_answer

st.title("SourceRecall")
st.write("Ask questions about your documents.")

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

        st.subheader("Answer:")
        st.write(answer)

        st.subheader("Retrieved Sources")

        for chunk in chunks:
            filename = Path(chunk["metadata"]["source"]).name
            page = chunk["metadata"]["page"]
            distance = chunk["distance"]

            st.markdown(
                f"- **{filename}** — page {page} | distance `{distance:.4f}`"
            )
    else:
        st.error("Please enter a question.")
