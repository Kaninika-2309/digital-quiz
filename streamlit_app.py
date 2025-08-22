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
categories["Any Category"] = None  # Add option for any category

# Sidebar: Quiz options
st.sidebar.header("Quiz Settings")
category_name = st.sidebar.selectbox("Select Category", list(categories.keys()))
amount = st.sidebar.slider("Number of Questions", 1, 20, 5)

# Fetch quiz questions
def fetch_quiz(category_id=None, amount=5):
    url = f'https://opentdb.com/api.php?amount={amount}&type=multiple'
    if category_id:
        url += f"&category={category_id}"
    data = requests.get(url).json()
    return data.get("results", [])

quiz_data = fetch_quiz(categories.get(category_name), amount)

# Show quiz questions
score = 0
if quiz_data:
    for i, q in enumerate(quiz_data, 1):
        st.subheader(f"Q{i}: {q['question']}")
        options = q['incorrect_answers'] + [q['correct_answer']]
        random.shuffle(options)
        answer = st.radio("Choose an answer:", options, key=i)
        if st.button("Submit Answer", key=f"btn_{i}"):
            if answer == q['correct_answer']:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong! Correct: {q['correct_answer']}")
    st.write(f"### Your Score: {score}/{len(quiz_data)}")
else:
    st.warning("No questions available. Try changing category or amount.")
