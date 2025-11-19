import streamlit as st
import pickle
import numpy as np
import re

# Load ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ---- PAGE SETUP ----
st.set_page_config(page_title="EV Chatbot", page_icon="⚡")

st.markdown("""
    <style>
        .user-msg {background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px;}
        .bot-msg {background-color: #E8EAF6; padding: 10px; border-radius: 10px; margin: 5px;}
    </style>
""", unsafe_allow_html=True)

st.title("⚡ EV Smart Chatbot")
st.write("Ask me anything about Electric Vehicles or give specs to predict range.")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- BOT LOGIC ----
def predict_range_from_text(text):

    # Extract numbers from the user sentence
    numbers = re.findall(r"\d+\.?\d*", text)
    numbers = [float(n) for n in numbers]

    # If exactly 3 numbers → predict
    if len(numbers) == 3:
        battery, torque, efficiency = numbers
        arr = np.array([[battery, torque, efficiency]])
        result = model.predict(arr)[0]
        return f"🚗 Estimated Range: **{result:.2f} km**"

    # User asked prediction but didn’t give enough numbers
    if "predict" in text.lower() or "range" in text.lower():
        return ("To predict, please provide 3 values:\n"
                "🔋 Battery (kWh)\n⚙️ Torque (Nm)\n⚡ Efficiency (Wh/km)\n"
                "Example: `Predict range for 80 300 150`")

    return None  # No prediction intent detected


def generate_bot_reply(message):
    msg = message.lower()

    # Greeting
    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "Hello! I'm your EV assistant. Ask me anything or give specs to predict driving range."

    # Try prediction
    prediction = predict_range_from_text(message)
    if prediction:
        return prediction

    # General EV questions
    if "ev" in msg or "electric" in msg:
        return ("An EV (Electric Vehicle) runs on battery instead of fuel. "
                "It uses an electric motor and is more efficient & eco-friendly!")

    return ("I can help with EV facts or range prediction.\n"
            "Try: `Predict range for 75 250 160`")

# ---- CHAT UI ----
user_msg = st.text_input("You:")

if st.button("Send"):
    if user_msg:
        bot_reply = generate_bot_reply(user_msg)
        st.session_state.chat_history.append(("You", user_msg))
        st.session_state.chat_history.append(("Bot", bot_reply))

# Display chat bubbles
for sender, text in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"<div class='user-msg'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><b>Bot:</b> {text}</div>", unsafe_allow_html=True)

