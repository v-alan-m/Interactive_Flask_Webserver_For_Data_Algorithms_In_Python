#!/usr/bin/env python3
"""
Data Structures & Python Interview Quiz - Flask Web Application
Run: python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify, request
import json
from pathlib import Path

app = Flask(__name__)

# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Structures & Python Quiz</title>
    <!-- Highlight.js for syntax highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #e0f2fe 0%, #c7d2fe 100%);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 2rem;
        }

        h1 {
            text-align: center;
            color: #4f46e5;
            margin-bottom: 2rem;
            font-size: 2rem;
        }

        .filters {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .filter-group label {
            display: block;
            font-weight: 600;
            color: #374151;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
        }

        select {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 0.875rem;
        }

        .progress-bar {
            margin-bottom: 2rem;
        }

        .progress-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
            color: #6b7280;
        }

        .progress-track {
            width: 100%;
            height: 12px;
            background: #e5e7eb;
            border-radius: 6px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: #4f46e5;
            transition: width 0.3s ease;
        }

        .question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .question-number {
            font-weight: 600;
            color: #4f46e5;
            font-size: 0.875rem;
        }

        .question-badge {
            background: #e0e7ff;
            color: #4f46e5;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .question-text {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 1.5rem;
        }

        .options {
            margin-bottom: 1.5rem;
        }

        .option {
            padding: 1rem;
            margin-bottom: 0.75rem;
            border: 2px solid #d1d5db;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            background: white;
            font-size: 1rem;
        }

        .option:hover:not(.disabled) {
            border-color: #818cf8;
            background: #eef2ff;
        }

        .option.selected.correct {
            border-color: #10b981;
            background: #d1fae5;
        }

        .option.selected.incorrect {
            border-color: #ef4444;
            background: #fee2e2;
        }

        .option.correct-answer {
            border-color: #10b981;
            background: #d1fae5;
        }

        .option.disabled {
            cursor: not-allowed;
        }

        .explanation {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .explanation h3 {
            font-size: 1.125rem;
            color: #1e40af;
            margin-bottom: 1rem;
        }

        .explanation-text {
            color: #1f2937;
            line-height: 1.6;
            white-space: pre-line;
            font-size: 0.875rem;
        }

        .code-block {
            background: #282c34;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            line-height: 1.5;
        }

        .code-block code {
            display: block;
            padding: 0;
        }

        /* Override highlight.js styles for better readability */
        .hljs {
            background: #282c34;
            color: #abb2bf;
        }

        .complexity {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #bfdbfe;
        }

        .complexity p {
            color: #1e40af;
            font-size: 0.875rem;
            margin-bottom: 0.25rem;
        }

        .video-link {
            margin-top: 1rem;
            padding: 1rem;
            background: #fef3c7;
            border-radius: 8px;
            border: 1px solid #fbbf24;
        }

        .video-link h4 {
            color: #92400e;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
        }

        .video-link a {
            color: #1e40af;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.875rem;
        }

        .video-link a:hover {
            text-decoration: underline;
        }

        .navigation {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.875rem;
        }

        .btn-primary {
            background: #4f46e5;
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            background: #4338ca;
        }

        .btn-secondary {
            background: #e5e7eb;
            color: #374151;
        }

        .btn-secondary:hover:not(:disabled) {
            background: #d1d5db;
        }

        .btn-danger {
            background: #fee2e2;
            color: #dc2626;
        }

        .btn-danger:hover {
            background: #fecaca;
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .no-questions {
            text-align: center;
            padding: 3rem;
            color: #6b7280;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Data Structures & Python Interview Quiz</h1>

        <div class="filters">
            <div class="filter-group">
                <label>Topic</label>
                <select id="topicFilter">
                    <option>All Topics</option>
                    <option>Data Structures</option>
                    <option>Python</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Level</label>
                <select id="levelFilter">
                    <option>All Levels</option>
                    <option>General</option>
                    <option>Mid Level</option>
                    <option>Senior Level</option>
                </select>
            </div>
        </div>

        <div class="progress-bar">
            <div class="progress-info">
                <span id="progressText">Progress: 0/0</span>
                <span id="scoreText">Score: 0/0</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
            </div>
        </div>

        <div id="questionContainer"></div>
    </div>

    <script>
        let allQuestions = [];
        let currentQuestionIndex = 0;
        let answeredQuestions = new Set();
        let score = 0;
        let topicFilter = 'All Topics';
        let levelFilter = 'All Levels';

        // Load questions from server
        async function loadQuestions() {
            try {
                const response = await fetch('/api/questions');
                allQuestions = await response.json();
                renderQuestion();
            } catch (error) {
                document.getElementById('questionContainer').innerHTML = 
                    '<div class="no-questions">Error loading questions. Make sure question files are in the questions/ folder.</div>';
            }
        }

        // Filter questions
        function getFilteredQuestions() {
            return allQuestions.filter(q => {
                const topicMatch = topicFilter === 'All Topics' || q.topic === topicFilter;
                const levelMatch = levelFilter === 'All Levels' || q.level === levelFilter;
                return topicMatch && levelMatch;
            });
        }

        // Render current question
        function renderQuestion() {
            const filtered = getFilteredQuestions();
            const container = document.getElementById('questionContainer');

            if (filtered.length === 0) {
                container.innerHTML = '<div class="no-questions">No questions match the selected filters.</div>';
                return;
            }

            if (currentQuestionIndex >= filtered.length) {
                currentQuestionIndex = 0;
            }

            const question = filtered[currentQuestionIndex];
            const isAnswered = answeredQuestions.has(question.id);

            let html = `
                <div class="question-header">
                    <span class="question-number">Question ${currentQuestionIndex + 1} of ${filtered.length}</span>
                    <span class="question-badge">${question.topic} - ${question.level}</span>
                </div>

                <div class="question-text">${question.question}</div>

                <div class="options">
            `;

            question.options.forEach((option, index) => {
                const isSelected = isAnswered && index === question.userAnswer;
                const isCorrect = index === question.correct;
                let className = 'option';

                if (isAnswered) {
                    className += ' disabled';
                    if (isSelected && isCorrect) className += ' selected correct';
                    else if (isSelected && !isCorrect) className += ' selected incorrect';
                    else if (isCorrect) className += ' correct-answer';
                }

                html += `<div class="${className}" onclick="handleAnswer(${index}, ${question.id})">${option}</div>`;
            });

            html += '</div>';

            if (isAnswered) {
                const isCorrectAnswer = question.userAnswer === question.correct;
                html += `
                    <div class="explanation">
                        <h3>${isCorrectAnswer ? '✓ Correct!' : '✗ Incorrect'}</h3>
                        <div class="explanation-text">${formatExplanation(question.explanation)}</div>
                        <div class="complexity">
                            <p><strong>Time Complexity:</strong> ${question.timeComplexity}</p>
                            <p><strong>Space Complexity:</strong> ${question.spaceComplexity}</p>
                        </div>
                        ${question.videoUrl ? `
                            <div class="video-link">
                                <h4>📺 Video Tutorial:</h4>
                                <a href="${question.videoUrl}" target="_blank">${question.videoTitle || 'Watch explanation'}</a>
                            </div>
                        ` : ''}
                    </div>
                `;
            }

            html += `
                <div class="navigation">
                    <button class="btn btn-secondary" onclick="previousQuestion()" ${currentQuestionIndex === 0 ? 'disabled' : ''}>
                        ← Previous
                    </button>

                    <button class="btn btn-danger" onclick="resetQuiz()">
                        ↻ Reset Quiz
                    </button>

                    <button class="btn btn-primary" onclick="nextQuestion()" ${currentQuestionIndex >= filtered.length - 1 ? 'disabled' : ''}>
                        Next →
                    </button>
                </div>
            `;

            container.innerHTML = html;
            updateProgress();

            // Apply syntax highlighting to code blocks
            applySyntaxHighlighting();
        }

        // Format explanation with code blocks
        function formatExplanation(text) {
            // Split by code blocks
            const parts = text.split('```');
            let formatted = '';

            parts.forEach((part, index) => {
                if (index % 2 === 1) {
                    // Code block
                    const lines = part.split('\\n');
                    const language = lines[0].trim();
                    const code = lines.slice(1).join('\\n');

                    formatted += `<div class="code-block"><pre><code class="language-${language}">${escapeHtml(code)}</code></pre></div>`;
                } else {
                    // Regular text - preserve formatting
                    formatted += part.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                }
            });

            return formatted;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Apply syntax highlighting after rendering
        function applySyntaxHighlighting() {
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }

        // Handle answer selection
        function handleAnswer(answerIndex, questionId) {
            if (answeredQuestions.has(questionId)) return;

            const filtered = getFilteredQuestions();
            const question = filtered[currentQuestionIndex];

            question.userAnswer = answerIndex;
            answeredQuestions.add(questionId);

            if (answerIndex === question.correct) {
                score++;
            }

            renderQuestion();
        }

        // Navigation
        function nextQuestion() {
            const filtered = getFilteredQuestions();
            if (currentQuestionIndex < filtered.length - 1) {
                currentQuestionIndex++;
                renderQuestion();
            }
        }

        function previousQuestion() {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                renderQuestion();
            }
        }

        function resetQuiz() {
            if (confirm('Are you sure you want to reset the quiz?')) {
                currentQuestionIndex = 0;
                answeredQuestions.clear();
                score = 0;
                renderQuestion();
            }
        }

        // Update progress bar
        function updateProgress() {
            const total = allQuestions.length;
            const answered = answeredQuestions.size;
            const percentage = total > 0 ? (answered / total) * 100 : 0;

            document.getElementById('progressText').textContent = `Progress: ${answered}/${total}`;
            document.getElementById('scoreText').textContent = `Score: ${score}/${answered || 0}`;
            document.getElementById('progressFill').style.width = `${percentage}%`;
        }

        // Filter handlers
        document.getElementById('topicFilter').addEventListener('change', (e) => {
            topicFilter = e.target.value;
            currentQuestionIndex = 0;
            renderQuestion();
        });

        document.getElementById('levelFilter').addEventListener('change', (e) => {
            levelFilter = e.target.value;
            currentQuestionIndex = 0;
            renderQuestion();
        });

        // Initialize
        loadQuestions();
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/questions')
def get_questions():
    questions_dir = Path('questions')
    questions = []

    if not questions_dir.exists():
        questions_dir.mkdir(parents=True, exist_ok=True)

    question_files = sorted(questions_dir.glob('question_*.json'))

    for file_path in question_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                question = json.load(f)
                questions.append(question)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    return jsonify(questions)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting Quiz Web Application...")
    print("=" * 60)
    print("\n📂 Make sure your questions are in the 'questions/' folder")
    print("📝 Files should be named: question_01.json, question_02.json, etc.")
    print("\n🌐 Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n❌ Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
