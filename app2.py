import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
def download_nltk_data():
    try:
        nltk.download("punkt")
        nltk.download("stopwords")
    except Exception as e:
        st.error(f"Error downloading NLTK data: {e}")

# Load a pre-trained Hugging Face model
chatbot = pipeline("question-answering", model="deepset/bert-base-cased-squad2")

# Preprocess user input
def preprocess_input(user_input):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(user_input)
    # Filter out stopwords
    filtered_words = [word for word in words if word.lower() not in stop_words]
    # Join the words with space for readability
    return ' '.join(filtered_words)

# Define Healthcare-specific response logic
def healthcare_chatbot(user_input):
    # Preprocess user input
    user_input = preprocess_input(user_input).lower()

    # Specific healthcare-related responses
    if "sneeze" in user_input or "sneezing" in user_input:
        return "Frequent sneezing may indicate allergies or a cold. Consult a doctor if symptoms persist."
    elif "symptom" in user_input:
        return "It seems like you're experiencing symptoms. Please consult a doctor for accurate advice."
    elif "appointment" in user_input:
        return "Would you like me to schedule an appointment with a doctor?"
    elif "medication" in user_input:
        return "It's important to take your prescribed medications regularly. If you have concerns, consult your doctor."
    else:
        # Default: use the pre-trained model
        context = """
        Common healthcare-related scenarios include symptoms of colds, flu, and allergies,
        along with medication guidance and appointment scheduling.
        """
        response = chatbot(question=user_input, context=context)
        return response['answer']

# Streamlit web app interface
def main():
    download_nltk_data()  # Download necessary NLTK data once
    st.title("Healthcare Assistant Chatbot")

    user_input = st.text_input("How can I assist you today?", "")
    if st.button("Submit"):
        if user_input:
            st.write("User: ", user_input)
            response = healthcare_chatbot(user_input)
            st.write("Healthcare Assistant: ", response)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    main()
