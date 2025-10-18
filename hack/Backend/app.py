# Install required libraries first:
# pip install groq flask flask-cors

from groq import Groq
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Initialize Groq client - PUT YOUR API KEY HERE
client = Groq(api_key="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")  # ← Change this line only!

# Test endpoint to check if server is running
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "success": True,
        "message": "Backend is working! 🚀"
    })

# LANGUAGE LEARNER ENDPOINTS

# 1. Generate Language Learning Plan
@app.route('/api/generate-language-plan', methods=['POST'])
def generate_language_plan():
    try:
        data = request.json
        language = data.get('language', 'Spanish')
        level = data.get('level', 'beginner')
        duration = data.get('duration', '7')  # days
        
        prompt = f"""Create a gamified {duration}-day learning plan for {language} at {level} level.

Format your response as valid JSON with this EXACT structure:
{{
    "plan_title": "Quest Name",
    "language": "{language}",
    "total_xp": 500,
    "days": [
        {{
            "day": 1,
            "quest_name": "Fun quest name",
            "lessons": ["lesson 1", "lesson 2", "lesson 3"],
            "practice_tasks": ["task 1", "task 2"],
            "xp_reward": 50,
            "badge": "badge name"
        }}
    ]
}}

Make it fun and engaging like a game!"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        try:
            plan_data = json.loads(content)
        except:
            plan_data = {"raw_response": content}
        
        return jsonify({
            "success": True,
            "plan": plan_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 2. Generate Vocabulary Quiz
@app.route('/api/generate-vocab-quiz', methods=['POST'])
def generate_vocab_quiz():
    try:
        data = request.json
        language = data.get('language', 'Spanish')
        topic = data.get('topic', 'basic greetings')
        num_questions = data.get('num_questions', 5)
        
        prompt = f"""Create {num_questions} vocabulary quiz questions for learning {language}.
Topic: {topic}

Return ONLY valid JSON in this format:
{{
    "quiz_title": "Vocabulary Challenge",
    "language": "{language}",
    "questions": [
        {{
            "id": 1,
            "word": "word in {language}",
            "question": "What does this mean in English?",
            "options": ["A: option1", "B: option2", "C: option3", "D: option4"],
            "correct_answer": "A",
            "explanation": "brief explanation",
            "xp_value": 20
        }}
    ]
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        
        content = response.choices[0].message.content
        try:
            quiz_data = json.loads(content)
        except:
            quiz_data = {"raw_response": content}
        
        return jsonify({
            "success": True,
            "quiz": quiz_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 3. AI Language Tutor Chat
@app.route('/api/language-tutor', methods=['POST'])
def language_tutor():
    try:
        data = request.json
        message = data.get('message')
        language = data.get('language', 'Spanish')
        
        prompt = f"""You are a friendly AI language tutor teaching {language}.
The student says: "{message}"

Respond encouragingly and help them learn. Use emojis and keep it fun!
If they ask for translations, provide them.
If they make mistakes, gently correct them.
Always be supportive and motivating! 🌟"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        
        return jsonify({
            "success": True,
            "response": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 4. Generate Conversation Practice
@app.route('/api/generate-conversation', methods=['POST'])
def generate_conversation():
    try:
        data = request.json
        language = data.get('language', 'Spanish')
        scenario = data.get('scenario', 'ordering at a restaurant')
        
        prompt = f"""Create a practice conversation in {language} for this scenario: {scenario}

Return JSON with:
{{
    "scenario": "{scenario}",
    "conversation": [
        {{"speaker": "You", "text_native": "...", "text_english": "..."}},
        {{"speaker": "Native", "text_native": "...", "text_english": "..."}}
    ],
    "vocabulary": ["word1: translation", "word2: translation"],
    "xp_reward": 30
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        try:
            conv_data = json.loads(content)
        except:
            conv_data = {"raw_response": content}
        
        return jsonify({
            "success": True,
            "conversation": conv_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# 5. Check for XP and Achievements
@app.route('/api/check-achievement', methods=['POST'])
def check_achievement():
    try:
        data = request.json
        total_xp = data.get('total_xp', 0)
        lessons_completed = data.get('lessons_completed', 0)
        
        achievements = []
        
        if total_xp >= 50:
            achievements.append({
                "name": "🌱 First Steps",
                "desc": "Earned your first 50 XP!",
                "icon": "🌱"
            })
        if total_xp >= 200:
            achievements.append({
                "name": "🔥 On Fire!",
                "desc": "Reached 200 XP streak!",
                "icon": "🔥"
            })
        if total_xp >= 500:
            achievements.append({
                "name": "⭐ Language Star",
                "desc": "500 XP! You're unstoppable!",
                "icon": "⭐"
            })
        if lessons_completed >= 5:
            achievements.append({
                "name": "📚 Bookworm",
                "desc": "Completed 5 lessons!",
                "icon": "📚"
            })
        if lessons_completed >= 10:
            achievements.append({
                "name": "🏆 Master Learner",
                "desc": "10 lessons complete!",
                "icon": "🏆"
            })
        
        return jsonify({
            "success": True,
            "new_achievements": achievements,
            "next_milestone": 500 if total_xp < 500 else 1000
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Run the Flask server
if __name__ == '__main__':
    print("\n🚀 Language Learning Backend Starting...")
    print("📍 Server running at: http://localhost:5000")
    print("🧪 Test endpoint: http://localhost:5000/api/test")
    print("\n💡 Press Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000)
