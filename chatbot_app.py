import streamlit as st
import pickle
import numpy as np

# Load ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("⚡ EV Range Prediction Chatbot")
st.write("Hello! I'm your EV Assistant. Ask me anything about EVs or give EV specs to predict range.")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chatbot Logic ---
def generate_bot_reply(message):
    msg = message.lower()

    # Greetings
    if "hello" in msg or "hi" in msg:
        return "Hello! I'm your EV assistant. You can ask me anything about Electric Vehicles or ask me to predict driving range."

    # Asking about EV range prediction
    if "predict" in msg or "range" in msg:
        return "Sure! Please enter: battery capacity (kWh), torque (Nm), and efficiency (Wh/km)."

    # If user gives numbers
    words = msg.split()
    numbers = [float(w) for w in words if w.replace('.', '', 1).isdigit()]

    if len(numbers) == 3:
        battery, torque, efficiency = numbers
        user_input = np.array([[battery, torque, efficiency]])
        prediction = model.predict(user_input)[0]
        return f"🚗 Estimated Range: **{prediction:.2f} km**"

    # Default response
    return "I can help you with EV info or range prediction. Try saying: 'Predict range for 80 300 150'."

# --- Chat Interface ---
user_message = st.text_input("You:", "")

if st.button("Send"):
    if user_message.strip() != "":
        bot_response = generate_bot_reply(user_message)

        # Save to chat history
        st.session_state.chat_history.append(("You", user_message))
        st.session_state.chat_history.append(("Bot", bot_response))

# Display chat
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.write(f"**You:** {msg}")
    else:
        st.success(f"**Bot:** {msg}")
