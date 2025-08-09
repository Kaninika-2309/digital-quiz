const startQuizBtn = document.getElementById('startQuiz');
const quizContainer = document.getElementById('quizContainer');
const submitBtn = document.getElementById('submitQuiz');
const resultDiv = document.getElementById('result');
const categorySelect = document.getElementById('category');

let quizData = [];
let userAnswers = {};

// Load categories dynamically on page load
document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/categories')
        .then(res => res.json())
        .then(data => {
            categorySelect.innerHTML = '';
            // Take first 15 categories only
            data.trivia_categories.slice(0, 15).forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.name;
                categorySelect.appendChild(option);
            });
        });
});

startQuizBtn.addEventListener('click', () => {
    const category = categorySelect.value;
    const amount = document.getElementById('amount').value;

    fetch(`/api/quiz?category=${category}&amount=${amount}`)
        .then(res => res.json())
        .then(data => {
            quizData = data.results;
            userAnswers = {};
            displayQuiz();
            submitBtn.style.display = 'inline-block';
            resultDiv.innerHTML = '';
        });
});

function displayQuiz() {
    quizContainer.innerHTML = '';

    quizData.forEach((q, idx) => {
        const questionDiv = document.createElement('div');
        questionDiv.classList.add('question');

        const questionText = document.createElement('h3');
        questionText.innerHTML = `${idx + 1}. ${decodeHTML(q.question)}`;
        questionDiv.appendChild(questionText);

        // Combine correct and incorrect answers and shuffle
        const answers = [...q.incorrect_answers];
        answers.push(q.correct_answer);
        shuffleArray(answers);

        answers.forEach(answer => {
            const optionDiv = document.createElement('div');
            optionDiv.classList.add('option');
            optionDiv.innerHTML = `<span class="dot"></span>${decodeHTML(answer)}`;
            optionDiv.addEventListener('click', () => selectAnswer(idx, answer, optionDiv));
            questionDiv.appendChild(optionDiv);
        });

        quizContainer.appendChild(questionDiv);
    });
}

function selectAnswer(questionIdx, answer, optionDiv) {
    userAnswers[questionIdx] = answer;

    const options = optionDiv.parentNode.querySelectorAll('.option');
    options.forEach(opt => opt.classList.remove('selected'));
    optionDiv.classList.add('selected');
}

submitBtn.addEventListener('click', () => {
    let score = 0;

    quizData.forEach((q, idx) => {
        const options = quizContainer.children[idx].querySelectorAll('.option');
        options.forEach(opt => {
            const text = opt.textContent.trim();
            if (text === decodeHTML(q.correct_answer)) {
                if (userAnswers[idx] === decodeHTML(q.correct_answer)) {
                    opt.classList.add('correct');
                    score++;
                } else {
                    opt.classList.add('correct');
                }
            } else if (userAnswers[idx] === text) {
                opt.classList.add('wrong');
            }
        });
    });

    resultDiv.innerHTML = `<h2>Your score: ${score} / ${quizData.length}</h2>`;
});

function shuffleArray(arr) {
    for(let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
}

function decodeHTML(html) {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
}

