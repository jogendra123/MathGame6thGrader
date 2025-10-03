import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from shared_state import load_players, reset_players


@st.cache_data(ttl=3)  # Cache for 3 seconds to avoid too frequent disk reads
def get_players_cached():
    """Load players from shared file store and return (players_dict, timestamp).
    Cached briefly to reduce disk reads when multiple components need player data.
    """
    players = load_players()
    return players, datetime.utcnow().isoformat()


@st.cache_data(ttl=5)  # Cache for 5 seconds
def get_players_cached():
    """Load players from shared file store with 5-second refresh."""
    players = load_players()
    return players, datetime.utcnow().isoformat()


def show_analytics():
    st.title("📊 Game Analytics")

    # Auto-refresh implementation
    auto_refresh = st.sidebar.toggle("Auto-refresh", value=False)
    if auto_refresh:
        st.empty()  # Create placeholder for rerun trigger
        time.sleep(5)  # Wait 5 seconds
        st.rerun()  # Force page refresh

    # Load latest shared players
    players, last_updated = get_players_cached()
    if not players:
        st.info("No game data available yet. Start playing to see analytics!")
        return

    # Rest of your analytics code remains the same
    st.caption(f"🔄 Last updated: {last_updated}")
    # Create DataFrame from player data
    players_df = pd.DataFrame.from_dict(players, orient='index')
    players_df['accuracy'] = (players_df['correct_answers'] / players_df['questions_answered'].replace(0, 1)) * 100
    players_df['player_name'] = players_df.index

    # Show active players count
    st.sidebar.metric("👥 Active Players", len(players))

    col1, col2 = st.columns(2)

    with col1:
        # Score comparison chart
        fig_scores = px.bar(
            players_df,
            x='player_name',
            y='score',
            title="Player Scores Comparison",
            color='score',
            color_continuous_scale='viridis'
        )
        fig_scores.update_layout(showlegend=False)
        st.plotly_chart(fig_scores, use_container_width=True)

    with col2:
        # Accuracy comparison
        fig_accuracy = px.bar(
            players_df,
            x='player_name',
            y='accuracy',
            title="Accuracy Percentage",
            color='accuracy',
            color_continuous_scale='RdYlGn'
        )
        fig_accuracy.update_layout(showlegend=False)
        st.plotly_chart(fig_accuracy, use_container_width=True)

    # Performance metrics
    st.subheader("🎯 Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_score = players_df['score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}")

    with col2:
        total_questions = int(players_df['questions_answered'].sum())
        st.metric("Total Questions", total_questions)

    with col3:
        avg_accuracy = players_df['accuracy'].mean()
        st.metric("Average Accuracy", f"{avg_accuracy:.1f}%")

    with col4:
        try:
            top_scorer = players_df.loc[players_df['score'].idxmax(), 'player_name']
            st.metric("Top Scorer", top_scorer)
        except:
            st.metric("Top Scorer", "-")

    # Detailed player stats table
    st.subheader("📋 Detailed Statistics")
    display_df = players_df[['score', 'questions_answered', 'correct_answers', 'accuracy']].copy()
    display_df.columns = ['Score', 'Questions', 'Correct', 'Accuracy %']
    if 'join_time' in players_df.columns:
        display_df['Joined At'] = players_df['join_time']
    st.dataframe(display_df.round(2), use_container_width=True)


def reset_game():
    st.title("🔄 Reset Game")
    st.warning("⚠️ This will reset all player data and scores!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Reset All Data", type="primary"):
            # Reset shared file as well as local session state
            reset_players()
            # Clear local session state keys that may store game state
            for key in ('players', 'current_player', 'question_data', 'leaderboard'):
                if key in st.session_state:
                    del st.session_state[key]
            st.success("✅ Game data has been reset!")
            st.balloons()

    with col2:
        if st.button("📊 Export Data Before Reset"):
            players = load_players()
            if players:
                df = pd.DataFrame.from_dict(players, orient='index')
                csv = df.to_csv()
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"njsla_game_data_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data to export")


def show_help():
    st.title("❓ Help & Instructions")

    tabs = st.tabs(["🎮 How to Play", "📚 Topics Covered", "🏆 Scoring System", "🔧 Troubleshooting"])

    with tabs[0]:
        st.markdown("""
        ## 🎮 How to Play

        1. **Join the Game**: Enter your name in the sidebar
        2. **Choose Your Game Mode**: Select from available modes:
           - **Quick Challenge**: Random questions from all topics
           - **Topic Focus**: Practice specific math topics
           - **Speed Round**: 60-second challenge
           - **Tournament**: Compete with friends
        3. **Start Playing**: Click "New Question" to begin

        ### Tips
        - Read questions carefully
        - Work quickly for speed bonuses
        - Compare scores with friends
        - Try all game modes!
        """)

    with tabs[1]:
        st.markdown("""
        ## 📚 Topics Covered

        This game covers major 6th grade math topics:

        - **🔢 Fractions**: Addition, subtraction, multiplication, division
        - **📊 Decimals**: Operations and conversions
        - **⚖️ Ratios & Proportions**: Unit rates, scaling
        - **📐 Geometry**: Area, perimeter, volume
        - **🧮 Algebra**: Simple equations
        - **📈 Statistics**: Mean, median, mode, range
        - **📝 Word Problems**: Real-world applications
        """)

    with tabs[2]:
        st.markdown("""
        ## 🏆 Scoring System

        - **Correct Answer**: 10 base points
        - **Speed Bonus**: Up to 5 extra points
           - Answer in 1s: +5 points
           - Answer in 2s: +4 points
           - Answer in 3s: +3 points
           - Answer in 4s: +2 points
           - Answer in 5s: +1 point
        - **Speed Round**: 5 points per correct answer
        """)

    with tabs[3]:
        st.markdown("""
        ## 🔧 Troubleshooting

        - **Game Not Loading**: Refresh the page
        - **Scores Not Updating**: Check auto-refresh settings
        - **Players Not Visible**: Enable auto-refresh
        - **Need to Start Over**: Use Reset Game option
        """)


def show_navigation():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Analytics & Settings")

    nav_options = ["🎮 Play Game", "📊 Analytics", "❓ Help", "🔄 Reset Game"]
    selected = st.sidebar.radio("Navigate to:", nav_options)

    return selected
