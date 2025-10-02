from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


def show_analytics():
    st.title("📊 Game Analytics")

    if not st.session_state.players:
        st.info("No game data available yet. Start playing to see analytics!")
        return

    # Create DataFrame from player data
    players_df = pd.DataFrame.from_dict(st.session_state.players, orient='index')
    players_df['accuracy'] = (players_df['correct_answers'] / players_df['questions_answered'].replace(0, 1)) * 100
    players_df['player_name'] = players_df.index

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
        total_questions = players_df['questions_answered'].sum()
        st.metric("Total Questions", total_questions)

    with col3:
        avg_accuracy = players_df['accuracy'].mean()
        st.metric("Average Accuracy", f"{avg_accuracy:.1f}%")

    with col4:
        top_scorer = players_df.loc[players_df['score'].idxmax(), 'player_name']
        st.metric("Top Scorer", top_scorer)

    # Detailed player stats table
    st.subheader("📋 Detailed Statistics")
    display_df = players_df[['score', 'questions_answered', 'correct_answers', 'accuracy', 'join_time']].round(2)
    display_df.columns = ['Score', 'Questions', 'Correct', 'Accuracy %', 'Joined At']
    st.dataframe(display_df, use_container_width=True)


def reset_game():
    st.title("🔄 Reset Game")

    st.warning("⚠️ This will reset all player data and scores!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Reset All Data", type="primary"):
            st.session_state.players = {}
            st.session_state.current_player = None
            st.session_state.question_data = {}
            st.session_state.leaderboard = []
            st.success("✅ Game data has been reset!")
            st.balloons()

    with col2:
        if st.button("📊 Export Data Before Reset"):
            if st.session_state.players:
                df = pd.DataFrame.from_dict(st.session_state.players, orient='index')
                csv = df.to_csv()
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name=f"njsla_game_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
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
        
        ### Getting Started
        1. **Join the Game**: Enter your name in the sidebar
        2. **Choose Your Game Mode**: Select from four different modes
        3. **Start Playing**: Click "New Question" to begin
        
        ### Game Modes
        
        #### 🚀 Quick Challenge
        - Random questions from all NJSLA topics
        - Earn points for correct answers
        - Speed bonus for quick responses
        
        #### 📚 Topic Focus
        - Practice specific math topics
        - Perfect for targeted study sessions
        - Choose from 7 core areas
        
        #### ⚡ Speed Round
        - 60-second challenge
        - Answer as many questions as possible
        - 5 points per correct answer
        
        #### 🏆 Tournament
        - Compete with friends
        - Live leaderboard updates
        - Crown the math champion!
        
        ### Tips for Success
        - Read questions carefully
        - Use scratch paper for calculations
        - Don't rush - accuracy matters!
        - Practice regularly to improve
        """)

    with tabs[1]:
        st.markdown("""
        ## 📚 NJSLA Topics Covered
        
        This game covers all major 6th grade math topics tested on NJSLA:
        
        ### 🔢 Fractions
        - Adding and subtracting fractions
        - Multiplying and dividing fractions
        - Converting between forms
        - Simplifying fractions
        
        ### 📊 Decimals
        - Decimal operations
        - Rounding and estimation
        - Converting fractions to decimals
        - Real-world applications
        
        ### ⚖️ Ratios & Proportions
        - Writing ratios
        - Solving proportions
        - Unit rates
        - Scale factors
        
        ### 📐 Geometry
        - Area and perimeter
        - Volume calculations
        - Basic geometric shapes
        - Coordinate geometry
        
        ### 🧮 Algebra
        - Solving simple equations
        - Variables and expressions
        - Order of operations
        - Inequalities
        
        ### 📈 Statistics
        - Mean, median, mode
        - Range and data analysis
        - Reading graphs and charts
        - Probability basics
        
        ### 📝 Word Problems
        - Multi-step problems
        - Real-world applications
        - Critical thinking
        - Problem-solving strategies
        """)

    with tabs[2]:
        st.markdown("""
        ## 🏆 Scoring System
        
        ### Points Breakdown
        - **Correct Answer**: 10 base points
        - **Speed Bonus**: Up to 5 additional points
        - **Speed Round**: 5 points per correct answer
        
        ### Speed Bonus Calculation
        - Answer in 1 second: +5 bonus points
        - Answer in 2 seconds: +4 bonus points
        - Answer in 3 seconds: +3 bonus points
        - Answer in 4 seconds: +2 bonus points
        - Answer in 5 seconds: +1 bonus point
        - Answer in 6+ seconds: No bonus
        
        ### Accuracy Tracking
        - Percentage of correct answers
        - Tracked across all game modes
        - Displayed in analytics
        
        ### Leaderboard Rankings
        - Ranked by total score
        - Real-time updates
        - Tournament mode competition
        """)

    with tabs[3]:
        st.markdown("""
        ## 🔧 Troubleshooting
        
        ### Common Issues
        
        #### Game Not Loading
        - Refresh the page
        - Check internet connection
        - Clear browser cache
        
        #### Questions Not Appearing
        - Click "New Question" button
        - Make sure you've joined the game
        - Try switching game modes
        
        #### Scores Not Updating
        - Submit your answer completely
        - Wait for confirmation message
        - Check the sidebar for updates
        
        #### Multiple Players Issues
        - Each player needs a unique name
        - Names are case-sensitive
        - Use "Reset Game" if needed
        
        ### Browser Compatibility
        - Works best on Chrome, Firefox, Safari
        - Enable JavaScript
        - Use latest browser version
        
        ### Performance Tips
        - Close unnecessary browser tabs
        - Use a stable internet connection
        - Avoid refreshing during gameplay
        
        ### Getting Help
        - Check this help section first
        - Try the troubleshooting steps
        - Reset the game if problems persist
        """)


# Navigation function
def show_navigation():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Analytics & Settings")

    nav_options = ["🎮 Play Game", "📊 Analytics", "❓ Help", "🔄 Reset Game"]
    selected = st.sidebar.radio("Navigate to:", nav_options)

    return selected
