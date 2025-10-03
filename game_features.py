import streamlit as st


def show_navigation():
    """Shows navigation options in the sidebar."""
    return st.sidebar.radio("📱 Navigation",
                            ["🎮 Play", "📊 Analytics", "❓ Help", "🔄 Reset Game"])


def show_analytics():
    """Shows analytics dashboard."""
    st.subheader("📊 Analytics Dashboard")
    if st.session_state.players:
        # Overall stats
        total_questions = sum(p["questions_answered"] for p in st.session_state.players.values())
        total_correct = sum(p["correct_answers"] for p in st.session_state.players.values())
        overall_accuracy = (total_correct / max(total_questions, 1)) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Players", len(st.session_state.players))
        with col2:
            st.metric("Total Questions", total_questions)
        with col3:
            st.metric("Overall Accuracy", f"{overall_accuracy:.1f}%")

        # Player performance table
        st.markdown("### Player Performance")
        player_stats = []
        for name, data in st.session_state.players.items():
            accuracy = (data["correct_answers"] / max(data["questions_answered"], 1)) * 100
            player_stats.append({
                "Player": name,
                "Score": data["score"],
                "Questions": data["questions_answered"],
                "Accuracy": f"{accuracy:.1f}%",
                "Join Time": data["join_time"]
            })
        st.table(player_stats)
    else:
        st.info("No player data available yet.")


def show_help():
    """Shows help and instructions."""
    st.subheader("❓ Help & Instructions")
    st.markdown("""
    ### Game Modes
    - **Quick Challenge**: Practice with random questions
    - **Topic Focus**: Master specific topics
    - **Speed Round**: 60-second challenge
    - **Tournament**: Compete with others

    ### Scoring
    - Correct answer: 10 points
    - Speed bonus: Up to 5 extra points
    - Speed round: 5 points per correct answer

    ### Tips
    1. Read questions carefully
    2. Watch the time in speed rounds
    3. Practice weak topics in Topic Focus mode
    """)


def reset_game():
    """Resets the game state."""
    if st.button("Confirm Reset"):
        st.session_state.players = {}
        st.session_state.current_player = None
        st.session_state.game_mode = None
        st.session_state.question_data = {}
        st.session_state.leaderboard = []
        st.success("Game has been reset!")
        st.rerun()
