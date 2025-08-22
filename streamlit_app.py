import streamlit as st
import requests
import random

st.set_page_config(page_title="Digital Quiz", layout="centered")
st.title("🎯 Digital Quiz")

# Fetch categories
@st.cache_data
def get_categories():
    url = 'https://opentdb.com/api_category.php'
    response = requests.get(url).json()
    categories = response.get('trivia_categories', [])
    return {cat['name']: cat['id'] for cat in categories}

categories = get_categories()
categories["Any Category"] = None

# Sidebar settings
st.sidebar.header("Quiz Settings")
category_name = st.sidebar.selectbox("Select Category", list(categories.keys()))
amount = st.sidebar.slider("Number of Questions", 1, 20, 5)

# Fetch questions
@st.cache_data
def fetch_quiz(category_id=None, amount=5):
    url = f'https://opentdb.com/api.php?amount={amount}&type=multiple'
    if category_id:
        url += f"&category={category_id}"
    data = requests.get(url).json()
    return data.get("results", [])

quiz_data = fetch_quiz(categories.get(category_name), amount)

if quiz_data:
    st.write(f"### Quiz: {len(quiz_data)} Questions")
    user_answers = {}
    
    # Display all questions
    for i, q in enumerate(quiz_data):
        st.subheader(f"Q{i+1}: {q['question']}")
        options = q['incorrect_answers'] + [q['correct_answer']]
        random.shuffle(options)
        user_answers[i] = st.radio("Choose an answer:", options, key=f"q{i}")

    # Single submit button
    if st.button("Submit Quiz"):
        score = 0
        for i, q in enumerate(quiz_data):
            if user_answers[i] == q['correct_answer']:
                score += 1
        st.success(f"✅ You scored {score} out of {len(quiz_data)}")
else:
    st.warning("No questions available. Try changing category or amount.")
