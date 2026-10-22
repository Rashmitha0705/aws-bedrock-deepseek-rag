import boto3
from botocore.exceptions import ClientError
import streamlit as st

st.set_page_config(page_title="Bedrock DeepSeek-R1 Chatbot", layout="centered")

st.title("🤖 DeepSeek-R1 Chatbot on AWS Bedrock")
st.write(
    "Hosted on AWS EC2 with CloudWatch Model Invocation Logging & Knowledge"
    " Base RAG."
)

# Sidebar toggle for Knowledge Base RAG
st.sidebar.title("Configuration")
use_kb = st.sidebar.checkbox(
    "Search Resume Knowledge Base (RAG)",
    value=True,
    help=(
        "When checked, retrieves context from your resume KB before generating an"
        " answer."
    ),
)
st.sidebar.success("Knowledge Base: Connected (CAX6CRNPND)")


# Initialize clients
@st.cache_resource
def get_bedrock_clients():
  runtime_client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
  agent_runtime_client = boto3.client(
      service_name="bedrock-agent-runtime", region_name="us-east-1"
  )
  return runtime_client, agent_runtime_client


client, agent_runtime_client = get_bedrock_clients()
model_id = "us.deepseek.r1-v1:0"
KB_ID = "CAX6CRNPND"  # Your Knowledge Base ID

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    text_content = "".join(
        [block.get("text", "") for block in message["content"] if "text" in block]
    )
    st.markdown(text_content)

if user_input := st.chat_input("Ask a question about your resume..."):
  st.session_state.messages.append(
      {"role": "user", "content": [{"text": user_input}]}
  )

  with st.chat_message("user"):
    st.markdown(user_input)

  with st.chat_message("assistant"):
    retrieved_context = ""

    # Step 1: Retrieve context from Managed Knowledge Base using managedSearchConfiguration
    if use_kb:
      with st.spinner("Retrieving context from resume Knowledge Base..."):
        try:
          retrieval_response = agent_runtime_client.retrieve(
              knowledgeBaseId=KB_ID,
              retrievalQuery={"text": user_input},
              retrievalConfiguration={
                  "managedSearchConfiguration": {
                      "numberOfResults": 3
                  }
              },
          )

          # Extract text chunks from retrieval results
          chunks = [
              result["content"]["text"]
              for result in retrieval_response.get("retrievalResults", [])
          ]
          retrieved_context = "\n\n".join(chunks)
        except Exception as e:
          st.error(f"KB Retrieval Error: {e}")

    # Step 2: Build conversation payload, augmenting with KB context if available
    current_messages = list(st.session_state.messages)
    if retrieved_context:
      augmentation_prompt = (
          f"Here is relevant context retrieved from the user's resume:\n"
          f"---------------------\n{retrieved_context}\n---------------------\n"
          f"Please answer the user's question based on this context: {user_input}"
      )
      current_messages[-1] = {
          "role": "user",
          "content": [{"text": augmentation_prompt}],
      }

    # Step 3: Generate answer using Converse API
    with st.spinner("Thinking (DeepSeek-R1)..."):
      try:
        # Note: If you have a guardrail identifier string, include it alongside guardrailVersion.
        # Removing guardrailConfig temporarily if you haven't set up a specific guardrail ID string yet, 
        # or supply both if configured. Using safe inference configuration here:
        response = client.converse(
            modelId=model_id,
            messages=current_messages,
            inferenceConfig={
                "maxTokens": 4096, 
                "temperature": 0.6, 
                "topP": 0.9
            }
        )

        output_message = response["output"]["message"]
        assistant_reply = ""
        clean_content_blocks = []

        for content_block in output_message["content"]:
          if "text" in content_block:
            t_val = content_block["text"]
            assistant_reply += t_val
            clean_content_blocks.append({"text": t_val})

        st.markdown(assistant_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": clean_content_blocks}
        )

      except ClientError as e:
        error_msg = e.response["Error"]["Message"]
        st.error(f"AWS Error: {error_msg}")
