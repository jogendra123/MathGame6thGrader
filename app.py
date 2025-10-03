import random
import time
from datetime import datetime

import streamlit as st

from game_features import show_navigation, show_analytics, show_help, reset_game
from shared_state import load_players, add_or_update_player

# Set page config
st.set_page_config(
    page_title="NJSLA Math Challenge",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'players' not in st.session_state:
    # Load shared players from disk so multiple browser sessions can see each other
    st.session_state.players = load_players()
if 'current_player' not in st.session_state:
    st.session_state.current_player = None
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None
if 'question_data' not in st.session_state:
    st.session_state.question_data = {}
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []


class MathGame:
    def __init__(self):
        self.topics = {
            "Fractions": self.generate_fraction_question,
            "Decimals": self.generate_decimal_question,
            "Ratios & Proportions": self.generate_ratio_question,
            "Geometry": self.generate_geometry_question,
            "Algebra": self.generate_algebra_question,
            "Statistics": self.generate_statistics_question,
            "Word Problems": self.generate_word_problem
        }

    def generate_fraction_question(self):
        operation = random.choice(['+', '-', '*', '/'])

        if operation in ['+', '-']:
            # Same denominator for easier computation
            denom = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
            num1 = random.randint(1, denom - 1)
            num2 = random.randint(1, denom - 1)

            if operation == '+':
                result = (num1 + num2) / denom
                question = f"What is {num1}/{denom} + {num2}/{denom}?"
            else:
                if num1 < num2:
                    num1, num2 = num2, num1
                result = (num1 - num2) / denom
                question = f"What is {num1}/{denom} - {num2}/{denom}?"

        elif operation == '*':
            num1, denom1 = random.randint(1, 5), random.choice([2, 3, 4, 5])
            num2, denom2 = random.randint(1, 5), random.choice([2, 3, 4, 5])
            result = (num1 * num2) / (denom1 * denom2)
            question = f"What is {num1}/{denom1} × {num2}/{denom2}?"

        else:  # division
            num1, denom1 = random.randint(1, 5), random.choice([2, 3, 4, 5])
            num2, denom2 = random.randint(1, 5), random.choice([2, 3, 4, 5])
            result = (num1 * denom2) / (denom1 * num2)
            question = f"What is {num1}/{denom1} ÷ {num2}/{denom2}?"

        # Generate multiple choice options
        correct = result
        options = [correct]
        while len(options) < 4:
            wrong = correct + random.uniform(-0.5, 0.5)
            if wrong > 0 and wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        correct_index = options.index(correct)

        return {
            "question": question,
            "options": [f"{opt:.3f}".rstrip('0').rstrip('.') for opt in options],
            "correct": correct_index,
            "topic": "Fractions"
        }

    def generate_decimal_question(self):
        operation = random.choice(['+', '-', '*', '/'])

        num1 = round(random.uniform(1, 50), 2)
        num2 = round(random.uniform(1, 20), 2)

        if operation == '+':
            result = num1 + num2
            question = f"What is {num1} + {num2}?"
        elif operation == '-':
            if num1 < num2:
                num1, num2 = num2, num1
            result = num1 - num2
            question = f"What is {num1} - {num2}?"
        elif operation == '*':
            num1 = round(random.uniform(1, 10), 1)
            num2 = round(random.uniform(1, 10), 1)
            result = num1 * num2
            question = f"What is {num1} × {num2}?"
        else:  # division
            num2 = round(random.uniform(1, 10), 1)
            result = round(random.uniform(1, 10), 2)
            num1 = num2 * result
            question = f"What is {num1:.2f} ÷ {num2}?"

        correct = round(result, 2)
        options = [correct]
        while len(options) < 4:
            wrong = round(correct + random.uniform(-5, 5), 2)
            if wrong > 0 and wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        correct_index = options.index(correct)

        return {
            "question": question,
            "options": options,
            "correct": correct_index,
            "topic": "Decimals"
        }

    def generate_ratio_question(self):
        scenarios = [
            "A recipe calls for {} cups of flour and {} cups of sugar. What is the ratio of flour to sugar?",
            "In a class of {} students, {} are boys. What is the ratio of boys to total students?",
            "A car travels {} miles in {} hours. What is the ratio of miles to hours?"
        ]

        scenario = random.choice(scenarios)
        num1 = random.randint(2, 12)
        num2 = random.randint(2, 12)

        # Simplify the ratio
        from math import gcd
        common = gcd(num1, num2)
        simplified_ratio = f"{num1 // common}:{num2 // common}"

        question = scenario.format(num1, num2)

        options = [simplified_ratio]
        while len(options) < 4:
            wrong_num1 = random.randint(1, 15)
            wrong_num2 = random.randint(1, 15)
            wrong_ratio = f"{wrong_num1}:{wrong_num2}"
            if wrong_ratio not in options:
                options.append(wrong_ratio)

        random.shuffle(options)
        correct_index = options.index(simplified_ratio)

        return {
            "question": question,
            "options": options,
            "correct": correct_index,
            "topic": "Ratios & Proportions"
        }

    def generate_geometry_question(self):
        question_types = ["area_rectangle", "area_triangle", "perimeter", "volume"]
        q_type = random.choice(question_types)

        if q_type == "area_rectangle":
            length = random.randint(5, 15)
            width = random.randint(3, 12)
            area = length * width
            question = f"What is the area of a rectangle with length {length} units and width {width} units?"
            unit = "square units"

        elif q_type == "area_triangle":
            base = random.randint(6, 16)
            height = random.randint(4, 12)
            area = 0.5 * base * height
            question = f"What is the area of a triangle with base {base} units and height {height} units?"
            unit = "square units"

        elif q_type == "perimeter":
            length = random.randint(5, 15)
            width = random.randint(3, 12)
            area = 2 * (length + width)
            question = f"What is the perimeter of a rectangle with length {length} units and width {width} units?"
            unit = "units"

        else:  # volume
            length = random.randint(3, 8)
            width = random.randint(3, 8)
            height = random.randint(3, 8)
            area = length * width * height
            question = f"What is the volume of a rectangular prism with length {length}, width {width}, and height {height} units?"
            unit = "cubic units"

        correct = area
        options = [f"{correct} {unit}"]
        while len(options) < 4:
            wrong = correct + random.randint(-20, 20)
            if wrong > 0:
                wrong_option = f"{wrong} {unit}"
                if wrong_option not in options:
                    options.append(wrong_option)

        random.shuffle(options)
        correct_index = options.index(f"{correct} {unit}")

        return {
            "question": question,
            "options": options,
            "correct": correct_index,
            "topic": "Geometry"
        }

    def generate_algebra_question(self):
        # Simple one-step equations
        operations = ['+', '-', '*', '/']
        operation = random.choice(operations)

        x_value = random.randint(1, 20)

        if operation == '+':
            constant = random.randint(1, 30)
            result = x_value + constant
            question = f"Solve for x: x + {constant} = {result}"
        elif operation == '-':
            constant = random.randint(1, 30)
            result = x_value + constant
            question = f"Solve for x: x - {constant} = {x_value}"
        elif operation == '*':
            constant = random.randint(2, 8)
            result = x_value * constant
            question = f"Solve for x: {constant}x = {result}"
        else:  # division
            constant = random.randint(2, 8)
            result = x_value * constant
            question = f"Solve for x: x ÷ {constant} = {x_value}"

        correct = x_value
        options = [correct]
        while len(options) < 4:
            wrong = random.randint(1, 30)
            if wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        correct_index = options.index(correct)

        return {
            "question": question,
            "options": options,
            "correct": correct_index,
            "topic": "Algebra"
        }

    def generate_statistics_question(self):
        # Generate a dataset
        data = [random.randint(10, 50) for _ in range(random.randint(5, 8))]

        question_type = random.choice(["mean", "median", "mode", "range"])

        if question_type == "mean":
            correct = sum(data) / len(data)
            question = f"What is the mean of this dataset: {data}?"
        elif question_type == "median":
            sorted_data = sorted(data)
            n = len(sorted_data)
            if n % 2 == 0:
                correct = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
            else:
                correct = sorted_data[n // 2]
            question = f"What is the median of this dataset: {data}?"
        elif question_type == "mode":
            # Ensure there's a clear mode
            mode_value = random.choice(data)
            data.append(mode_value)
            correct = mode_value
            question = f"What is the mode of this dataset: {data}?"
        else:  # range
            correct = max(data) - min(data)
            question = f"What is the range of this dataset: {data}?"

        options = [correct]
        while len(options) < 4:
            if question_type in ["mean", "median"]:
                wrong = correct + random.uniform(-5, 5)
                wrong = round(wrong, 1)
            else:
                wrong = correct + random.randint(-10, 10)

            if wrong > 0 and wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        correct_index = options.index(correct)

        return {
            "question": question,
            "options": options,
            "correct": correct_index,
            "topic": "Statistics"
        }

    def generate_word_problem(self):
        problems = [
            {
                "text": "Sarah has {} stickers. She gives {} stickers to her friend and buys {} more. How many stickers does she have now?",
                "operation": lambda a, b, c: a - b + c,
                "params": [random.randint(20, 50), random.randint(5, 15), random.randint(8, 20)]
            },
            {
                "text": "A store sells {} apples per day. How many apples will they sell in {} days?",
                "operation": lambda a, b, c=0: a * b,
                "params": [random.randint(25, 75), random.randint(3, 7), 0]
            },
            {
                "text": "Tom has ${:.2f}. He buys a toy for ${:.2f}. How much money does he have left?",
                "operation": lambda a, b, c=0: a - b,
                "params": [random.uniform(10, 50), random.uniform(5, 25), 0]
            }
        ]

        problem = random.choice(problems)
        params = problem["params"]

        if len(params) == 3 and params[2] == 0:
            question = problem["text"].format(params[0], params[1])
            correct = problem["operation"](params[0], params[1])
        else:
            question = problem["text"].format(*params)
            correct = problem["operation"](*params)

        correct = round(correct, 2)
        options = [correct]
        while len(options) < 4:
            wrong = correct + random.uniform(-10, 10)
            wrong = round(wrong, 2)
            if wrong > 0 and wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        correct_index = options.index(correct)

        return {
            "question": question,
            "options": options,
            "correct": correct_index,
            "topic": "Word Problems"
        }

    def get_random_question(self, topic=None):
        if topic and topic in self.topics:
            return self.topics[topic]()
        else:
            topic = random.choice(list(self.topics.keys()))
            return self.topics[topic]()


# Initialize the game
game = MathGame()


def main():
    st.title("🎯 NJSLA Math Challenge")
    st.markdown("### Competitive Math Game for 6th Graders")

    # Sidebar for player management and navigation
    with st.sidebar:
        st.header("🏆 Game Setup")

        # Player registration
        player_name = st.text_input("Enter your name:")
        if st.button("Join Game") and player_name:
            if player_name not in st.session_state.players:
                info = {
                    "score": 0,
                    "questions_answered": 0,
                    "correct_answers": 0,
                    "join_time": datetime.now().strftime("%H:%M:%S")
                }
                # Persist to shared storage
                add_or_update_player(player_name, info)
                st.session_state.players[player_name] = info
                st.success(f"Welcome {player_name}!")
            else:
                st.info(f"Welcome back {player_name}!")
            st.session_state.current_player = player_name

        # Current players
        if st.session_state.players:
            st.subheader("👥 Current Players")
            for player, data in st.session_state.players.items():
                accuracy = (data["correct_answers"] / max(data["questions_answered"], 1)) * 100
                st.write(f"**{player}**: {data['score']} pts ({accuracy:.1f}%)")

        # Game mode selection
        st.subheader("🎮 Game Mode")
        game_modes = ["Quick Challenge", "Topic Focus", "Speed Round", "Tournament"]
        selected_mode = st.selectbox("Choose game mode:", game_modes)
        st.session_state.game_mode = selected_mode

        if selected_mode == "Topic Focus":
            selected_topic = st.selectbox("Choose topic:", list(game.topics.keys()))
        else:
            selected_topic = None

        # Navigation
        navigation = show_navigation()

    # Handle navigation
    if navigation == "📊 Analytics":
        show_analytics()
    elif navigation == "❓ Help":
        show_help()
    elif navigation == "🔄 Reset Game":
        reset_game()
    else:
        # Main game area
        if st.session_state.current_player:
            player_name = st.session_state.current_player

            if st.session_state.game_mode == "Quick Challenge":
                quick_challenge_mode(player_name, selected_topic)
            elif st.session_state.game_mode == "Topic Focus":
                topic_focus_mode(player_name, selected_topic)
            elif st.session_state.game_mode == "Speed Round":
                speed_round_mode(player_name)
            elif st.session_state.game_mode == "Tournament":
                tournament_mode(player_name)
        else:
            st.info("👈 Please enter your name in the sidebar to start playing!")

            # Show game instructions
            st.markdown("""
            ## 📚 How to Play

            1. **Join the Game**: Enter your name in the sidebar
            2. **Choose a Game Mode**:
               - **Quick Challenge**: Random questions from all topics
               - **Topic Focus**: Practice specific math topics
               - **Speed Round**: Answer as many questions as possible in 60 seconds
               - **Tournament**: Compete against other players
            3. **Answer Questions**: Select the correct answer from multiple choices
            4. **Earn Points**: Get points for correct answers, bonus for speed
            5. **Compete**: Compare your scores with friends on the leaderboard

            ## 📖 NJSLA Topics Covered
            - Fractions and Mixed Numbers
            - Decimals and Operations
            - Ratios and Proportions
            - Basic Geometry (Area, Perimeter, Volume)
            - Introductory Algebra
            - Statistics (Mean, Median, Mode, Range)
            - Word Problems and Real-world Applications

            ## 🚀 Getting Started
            Ready to challenge your friends? Enter your name in the sidebar and let's start practicing for NJSLA!
            """)

            # Add some motivational elements
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("🎯 **Goal**: Master 6th grade math concepts")
            with col2:
                st.info("🏆 **Compete**: Challenge friends and classmates")
            with col3:
                st.info("📈 **Track**: Monitor your progress and improvement")


def quick_challenge_mode(player_name, topic=None):
    st.subheader(f"🚀 Quick Challenge - {player_name}")

    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("🎲 New Question", type="primary"):
            st.session_state.question_data = game.get_random_question(topic)
            st.session_state.answer_submitted = False
            st.session_state.start_time = time.time()

    if 'question_data' in st.session_state and st.session_state.question_data:
        with col1:
            question = st.session_state.question_data

            st.markdown(f"**Topic**: {question['topic']}")
            st.markdown(f"**Question**: {question['question']}")

            if 'answer_submitted' not in st.session_state:
                st.session_state.answer_submitted = False

            if not st.session_state.answer_submitted:
                selected_answer = st.radio("Choose your answer:",
                                           question['options'],
                                           key=f"answer_{id(question)}")

                if st.button("Submit Answer"):
                    end_time = time.time()
                    time_taken = end_time - st.session_state.start_time

                    selected_index = question['options'].index(selected_answer)
                    is_correct = selected_index == question['correct']

                    # Update player stats
                    st.session_state.players[player_name]['questions_answered'] += 1
                    if is_correct:
                        st.session_state.players[player_name]['correct_answers'] += 1
                        # Points: base 10 + speed bonus (max 5 points)
                        speed_bonus = max(0, 5 - int(time_taken))
                        points = 10 + speed_bonus
                        st.session_state.players[player_name]['score'] += points

                        st.success(f"🎉 Correct! +{points} points (Speed bonus: +{speed_bonus})")
                        st.balloons()
                    else:
                        correct_answer = question['options'][question['correct']]
                        st.error(f"❌ Incorrect. The correct answer was: {correct_answer}")

                    st.info(f"⏱️ Time taken: {time_taken:.1f} seconds")
                    st.session_state.answer_submitted = True
                    # Persist updated player to shared storage so other sessions see it
                    add_or_update_player(player_name, st.session_state.players[player_name])

    # Show current stats
    player_stats = st.session_state.players[player_name]
    accuracy = (player_stats["correct_answers"] / max(player_stats["questions_answered"], 1)) * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", player_stats["score"])
    with col2:
        st.metric("Questions Answered", player_stats["questions_answered"])
    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")


def topic_focus_mode(player_name, topic):
    st.subheader(f"📚 Topic Focus: {topic} - {player_name}")
    quick_challenge_mode(player_name, topic)


def speed_round_mode(player_name):
    st.subheader(f"⚡ Speed Round - {player_name}")

    if 'speed_round_active' not in st.session_state:
        st.session_state.speed_round_active = False

    if not st.session_state.speed_round_active:
        if st.button("🚀 Start 60-Second Challenge!", type="primary"):
            st.session_state.speed_round_active = True
            st.session_state.speed_round_start = time.time()
            st.session_state.speed_round_score = 0
            st.session_state.speed_round_questions = 0
            st.session_state.question_data = game.get_random_question()
            st.rerun()
    else:
        elapsed = time.time() - st.session_state.speed_round_start
        remaining = max(0, 60 - elapsed)

        if remaining > 0:
            st.markdown(f"⏰ **Time Remaining: {remaining:.1f} seconds**")

            question = st.session_state.question_data
            st.markdown(f"**{question['question']}**")

            selected_answer = st.radio("Quick! Choose your answer:",
                                       question['options'],
                                       key=f"speed_{st.session_state.speed_round_questions}")

            if st.button("Submit"):
                selected_index = question['options'].index(selected_answer)
                is_correct = selected_index == question['correct']

                st.session_state.speed_round_questions += 1
                if is_correct:
                    st.session_state.speed_round_score += 5

                # Generate next question
                st.session_state.question_data = game.get_random_question()
                st.rerun()

            st.markdown(
                f"**Current Score: {st.session_state.speed_round_score} | Questions: {st.session_state.speed_round_questions}**")
        else:
            # Time's up!
            st.session_state.speed_round_active = False
            final_score = st.session_state.speed_round_score
            questions_answered = st.session_state.speed_round_questions

            st.success(f"🏁 Time's Up! Final Score: {final_score} points")
            st.info(f"Questions answered: {questions_answered}")

            # Add to player's total score
            st.session_state.players[player_name]['score'] += final_score
            st.session_state.players[player_name]['questions_answered'] += questions_answered
            # Persist updates
            add_or_update_player(player_name, st.session_state.players[player_name])

            if st.button("Play Again"):
                st.rerun()


def tournament_mode(player_name):
    st.subheader("🏆 Tournament Mode")

    if len(st.session_state.players) < 2:
        st.warning("Need at least 2 players for tournament mode!")
        return

    # Show leaderboard
    sorted_players = sorted(st.session_state.players.items(),
                            key=lambda x: x[1]['score'], reverse=True)

    st.markdown("### 🏅 Live Leaderboard")

    for i, (name, data) in enumerate(sorted_players):
        if i == 0:
            st.markdown(f"🥇 **{name}**: {data['score']} points")
        elif i == 1:
            st.markdown(f"🥈 **{name}**: {data['score']} points")
        elif i == 2:
            st.markdown(f"🥉 **{name}**: {data['score']} points")
        else:
            st.markdown(f"{i + 1}. **{name}**: {data['score']} points")

    st.markdown("---")
    quick_challenge_mode(player_name)


if __name__ == "__main__":
    main()
