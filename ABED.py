import streamlit as st
import requests

# ---------- API Config ----------
API_ENDPOINT = "https://16psxb3erf.execute-api.us-east-1.amazonaws.com/chat"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="ABED Chat", page_icon="🛡️")
st.title("🛡️ ABED - A Bot Excelling Daily")
st.markdown("**AI-Powered Red Team & Security Analysis Assistant**")
st.markdown("Ask me about vulnerabilities, CVEs, attack paths, or paste in environment data for analysis.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a security question or paste environment data..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call API
    with st.chat_message("assistant"):
        with st.spinner("ABED is analyzing..."):
            try:
                response = requests.post(
                    API_ENDPOINT,
                    json={"query": prompt},
                    headers={"Content-Type": "application/json"},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "No response received.")
                    sources = data.get("sources", [])
                    num_articles = data.get("num_articles_used", 0)

                    st.markdown(answer)

                    if sources:
                        with st.expander(f" Intelligence Sources Used ({num_articles} articles)"):
                            for source in sources:
                                st.markdown(f"- `{source}`")

                    st.session_state.messages.append({"role": "assistant", "content": answer})

                else:
                    error_msg = f"API error: {response.status_code} - {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except requests.exceptions.Timeout:
                msg = "Request timed out. ABED is still processing, try again in a moment."
                st.error(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})

            except Exception as e:
                msg = f"Error: {e}"
                st.error(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})