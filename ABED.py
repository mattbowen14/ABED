import streamlit as st
import boto3
import uuid

# ---------- AWS Bedrock Runtime Client ----------
bedrock_agent_runtime = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name="us-east-1"  # Change based on your agent's region
)

# ---------- Agent Config ----------
AGENT_ID = "GCW6LPVJWR"
AGENT_ALIAS_ID = "TZ5WSFNJYH"
SESSION_ID = str(uuid.uuid4())  # New session for each run

# ---------- Streamlit UI ----------
st.set_page_config(page_title="ABED Chat")
st.title("🤖 Chat ABED")
st.markdown("Ask me anything about Cybersecurity")

user_input = st.text_input("Your question:", placeholder="Ask a question...")

if st.button("Send") and user_input.strip():
    try:
        # Create an empty placeholder for streaming text
        output_area = st.empty()
        streamed_text = ""

        # Invoke agent with streaming response
        response = bedrock_agent_runtime.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=SESSION_ID,
            inputText=user_input
        )

        for event in response["completion"]:
            if "chunk" in event:
                chunk_text = event["chunk"]["bytes"].decode("utf-8")
                streamed_text += chunk_text
                output_area.markdown(f"**Agent:** {streamed_text}▌")

        # Final update (remove cursor)
        output_area.markdown(f"**Agent:** {streamed_text}")

    except Exception as e:
        st.error(f"Error: {e}")