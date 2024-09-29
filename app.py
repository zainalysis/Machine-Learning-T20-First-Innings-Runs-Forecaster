import streamlit as st
import pandas as pd
import pickle
import gzip

# Function to load the model
def load_model():
    with open('/workspaces/T20-First-Innings-Runs-Forecaster/pipe (4).pkl', 'rb') as f:
        return pickle.load(f)

# Load the model
model = load_model()


# Set the title of the app
st.title("T20 First Innings Total Runs Predictor")
st.markdown("### Created by Zain Ul Hassan @zainalysis")
st.markdown("A performance analyst with a passion for cricket analytics.")

# Input fields for user to provide match information
# List of teams
teams = ['Australia', 'Bangladesh', 'Afghanistan', 'India', 
         'England', 'New Zealand', 'South Africa', 
         'Sri Lanka', 'Pakistan', 'West Indies', 
         'Zimbabwe', 'Ireland', 'Scotland']

# Select Batting Team
team_bat = st.selectbox("Select Batting Team:", teams)

# Select Bowling Team, ensuring it's different from the Batting Team
team_bowl = st.selectbox("Select Bowling Team:", 
                         [team for team in teams if team != team_bat])

ground = st.selectbox("Select Ground:", 
                      ['Harare Sports Club', 'Shere Bangla National Stadium, Mirpur', 
           'Dubai International Cricket Stadium', 'R Premadasa Stadium, Colombo', 
           'Sharjah Cricket Stadium', 'Gaddafi Stadium, Lahore', 'Eden Park, Auckland', 
           'Sydney Cricket Ground', 'Zayed Cricket Stadium, Abu Dhabi', 
           'Central Broward Regional Park Stadium Turf Ground, Lauderhill', 
           'Kensington Oval, Bridgetown, Barbados', 'Pallekele International Cricket Stadium', 
           'Hagley Oval, Christchurch', 'Melbourne Cricket Ground', 
           'Daren Sammy National Cricket Stadium, Gros Islet, St Lucia', 'Newlands, Cape Town', 
           'Zahur Ahmed Chowdhury Stadium, Chattogram', 'Bellerive Oval, Hobart', 
           'Civil Service Cricket Club, Stormont, Belfast', 'Warner Park, Basseterre, St Kitts', 
           'Bay Oval, Mount Maunganui', 'SuperSport Park, Centurion', 
           'Grange Cricket Club Ground, Raeburn Place, Edinburgh', 'Adelaide Oval', 
           'Westpac Stadium, Wellington', 'Eden Gardens, Kolkata', 
           'Vidarbha Cricket Association Stadium, Jamtha, Nagpur', 'Bready Cricket Club, Magheramason, Bready', 
           'New Wanderers Stadium, Johannesburg', 'The Rose Bowl, Southampton', 
           'Old Trafford, Manchester', 'Providence Stadium, Guyana', 
           "National Cricket Stadium, St George's, Grenada", 'Sabina Park, Kingston, Jamaica', 
           'Seddon Park, Hamilton', 'Wankhede Stadium, Mumbai', 'Perth Stadium', 
           'Sophia Gardens, Cardiff', 'Kingsmead, Durban', 'National Stadium, Karachi', 
           'Brisbane Cricket Ground, Woolloongabba, Brisbane', 'Sylhet International Cricket Stadium', 
           'The Village, Malahide, Dublin', 'Rajiv Gandhi International Cricket Stadium, Dehradun', 
           'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh', 
           'Greater Noida Sports Complex Ground, Greater Noida', 'Narendra Modi Stadium, Ahmedabad', 
           'McLean Park, Napier', 'Rawalpindi Cricket Stadium', 'Sheikh Zayed Stadium, Abu Dhabi', 
           'Brian Lara Stadium, Tarouba, Trinidad', 
           'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow', 
           'Castle Avenue, Dublin', 'Feroz Shah Kotla, Delhi'])  # Replace with actual ground names

# Input fields
inns_runs = st.number_input("Enter Current Innings Runs:", min_value=0, max_value=300, step=1)
balls_bowled = st.number_input("Enter Total Balls Bowled So Far:", min_value=1, max_value=120, step=1)
inns_wkts = st.number_input("Enter Wickets Fallen:", min_value=0, max_value=9, step=1)

# Conditional for Last5OversRuns
if balls_bowled >= 30:
    # Last 5 overs is equivalent to 30 balls
    max_last_30_balls_runs = min(inns_runs, 150)  # Ensures it does not exceed inns_runs or 150
    Last5OversRuns = st.number_input(f"Enter Runs Scored In Last 30 Balls / 5 Overs From Now (<= {max_last_30_balls_runs}):", 
                                     min_value=0, max_value=max_last_30_balls_runs, step=1)
else:
    st.info("Less than 30 balls bowled, so last 30 balls data is not applicable.")
    Last5OversRuns = None  # or set a default value like 0


# Button to predict total runs
if st.button("Predict Total Runs"):
    # Create a DataFrame from the input data
    input_data = pd.DataFrame({
        'team_bat': [team_bat],
        'team_bowl': [team_bowl],
        'ground': [ground],
        'inns_runs': [inns_runs],
        'balls_bowled': [balls_bowled],
        'inns_wkts': [inns_wkts],
        'Last5OversRuns': [Last5OversRuns]
    })

    # Predict using the loaded model
    prediction = model.predict(input_data)

    # Display the prediction
    st.success(f"Predicted Total Runs: {int(prediction[0])}")