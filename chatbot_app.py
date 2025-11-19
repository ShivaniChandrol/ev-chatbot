import streamlit as st
import re

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="EV Smart Assistant", page_icon="⚡", layout="wide")

# -----------------------------
# CUSTOM CSS FOR CHAT UI
# -----------------------------
st.markdown("""
    <style>
        .user-msg {
            background-color: #1e1e1e;
            padding: 10px 15px;
            border-radius: 15px;
            color: white;
            width: fit-content;
            margin-bottom: 10px;
        }
        .bot-msg {
            background-color: #2f4f4f;
            padding: 10px 15px;
            border-radius: 15px;
            color: white;
            width: fit-content;
            margin-bottom: 10px;
        }
        .main-container {
            background-color: #111;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# CHAT MEMORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_range_inputs" not in st.session_state:
    st.session_state.awaiting_range_inputs = False

# -----------------------------
# RANGE PREDICTION FUNCTION
# -----------------------------
def predict_ev_range(battery_kwh, torque_nm, efficiency_wh_km):
    # Simple model formula (example)
    usable_energy = battery_kwh * 0.9       # 90% usable battery
    base_range = (usable_energy * 1000) / efficiency_wh_km
    torque_factor = 1 - (torque_nm / 2000)  # high torque slightly reduces range
    final_range = base_range * torque_factor
    return max(int(final_range), 1)

# -----------------------------
# MESSAGE DISPLAY FUNCTION
# -----------------------------
def display_message(role, text):
    if role == "user":
        st.markdown(f"<div class='user-msg'>You: {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>Bot: {text}</div>", unsafe_allow_html=True)

# -----------------------------
# MAIN CHATBOT LOGIC
# -----------------------------
def get_bot_reply(user_input):

    # Greeting intent
    if user_input.lower() in ["hi", "hello", "hey"]:
        return "Hello Shivani! 👋 I'm your EV smart assistant. Ask me anything about electric vehicles or say **predict range** to estimate EV driving range."

    # If bot previously asked for numbers → expect prediction input now
    if st.session_state.awaiting_range_inputs:
        numbers = re.findall(r"\d+", user_input)
        if len(numbers) == 3:
            battery, torque, efficiency = map(int, numbers)
            st.session_state.awaiting_range_inputs = False
            predicted = predict_ev_range(battery, torque, efficiency)
            return f"🔋 **Predicted Range:** approximately **{predicted} km** under normal driving conditions."
        else:
            return "Please enter values in this format: `battery_kWh torque_Nm efficiency_WhPerKm`"

    # When user wants range prediction
    if "predict" in user_input.lower() and "range" in user_input.lower():
        st.session_state.awaiting_range_inputs = True
        return "Sure! 😊 Please enter: `battery_kWh torque_Nm efficiency_WhPerKm`\n\nExample: `80 300 150`"

    # EV general knowledge
    if "what is ev range" in user_input.lower():
        return "EV range means how far an electric vehicle can travel on a single full charge. It depends on battery capacity, efficiency, driving style & road conditions."

    return "I'm not sure I understood that 🤔. You can ask me EV questions or say **predict range** to calculate EV driving distance."

# -----------------------------
# UI LAYOUT
# -----------------------------
st.title("⚡ EV Smart Assistant (Advanced Edition)")
st.write("Your personal electric vehicle expert — smarter, cleaner UI, more powerful responses.")

# Chat History Display
for msg in st.session_state.messages:
    display_message(msg["role"], msg["text"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "text": user_input})
    display_message("user", user_input)

    # Generate bot reply
    bot_reply = get_bot_reply(user_input)
    st.session_state.messages.append({"role": "bot", "text": bot_reply})
    display_message("bot", bot_reply)
