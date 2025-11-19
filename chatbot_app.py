import streamlit as st

# Title
st.title("🤖EV AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def chatbot_response(user_input):
    return f"You said: {user_input} — (Bot response will come here later)"

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user's message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Get bot reply
    bot_reply = chatbot_response(user_input)

    # Save bot message
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Display bot message instantly
    with st.chat_message("assistant"):
        st.write(bot_reply)
