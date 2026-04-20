import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the trained model
model = pickle.load(open("models/placement_model.pkl", "rb"))

# Streamlit app
st.set_page_config(page_title="Placement Predictor", layout="wide")

# Custom CSS for attractive styling
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    h1 {
        text-align: center;
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-size: 3em;
        margin-bottom: 1em;
    }
    
    h2 {
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5em;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1em;
        padding: 12px 30px;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎓 Placement Chance Predictor</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
                border: 2px solid rgba(255,255,255,0.3);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border-left: 5px solid #10B981;'>
        <h3 style='color: white; margin: 0; font-size: 1.5em;'>📝 Enter Your Details Below:</h3>
        <p style='color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 0.9em;'>Fill in your academic and skills information</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding: 20px; background: rgba(255,255,255,0.95); border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-top: 10px;'>", unsafe_allow_html=True)

# Create input fields in better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("<hr style='border-color: #667eea;'>", unsafe_allow_html=True)
    cgpa = st.slider("🎯 CGPA", 0.0, 10.0, 7.5, help="Your Cumulative Grade Point Average")
    programming = st.slider("💻 Programming Skills", 0, 10, 7, help="Your programming expertise (0-10)")
    dsa = st.slider("🔧 DSA Skills", 0, 10, 7, help="Data Structures & Algorithms (0-10)")
    projects = st.slider("📂 Projects Count", 0, 10, 3, help="Number of projects completed")

with col2:
    st.markdown("<hr style='border-color: #667eea;'>", unsafe_allow_html=True)
    internships = st.slider("🏢 Internships", 0, 5, 1, help="Number of internships done")
    communication = st.slider("🗣️ Communication Skills", 0, 10, 7, help="Communication ability (0-10)")
    aptitude = st.slider("🧠 Aptitude Score", 0, 10, 7, help="Aptitude test score (0-10)")
    certifications = st.slider("🎖️ Certifications", 0, 10, 2, help="Number of certifications")

github = st.slider("🐙 GitHub Activity", 0, 10, 5, help="Your GitHub contributions (0-10)")

st.markdown("</div>", unsafe_allow_html=True)

# Create prediction button
st.markdown("<div style='text-align: center; margin: 30px 0;'>", unsafe_allow_html=True)
if st.button("🔮 PREDICT PLACEMENT STATUS", key="predict_btn"):
    # Prepare input data
    input_data = np.array([
        [cgpa, programming, dsa, projects, internships, 
         communication, aptitude, certifications, github]
    ])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)
    
    # Display result with color based on prediction
    if prediction == "High":
        color = "#10B981"  # Green
        emoji = "🎉"
    elif prediction == "Medium":
        color = "#F59E0B"  # Amber
        emoji = "⭐"
    else:
        color = "#EF4444"  # Red
        emoji = "💪"
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color} 0%, rgba(0,0,0,0.1) 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
            <h2 style='color: white; font-size: 2.5em;'>{emoji} {prediction.upper()}</h2>
            <p style='color: white; font-size: 1.2em;'>Your Placement Status</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display confidence with better styling
    st.markdown("<div style='background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-top: 20px;'>", unsafe_allow_html=True)
    st.write("### 📊 Confidence Levels:")
    
    col1, col2, col3 = st.columns(3)
    for idx, (class_label, col) in enumerate(zip(model.classes_, [col1, col2, col3])):
        confidence = prediction_proba[0][idx] * 100
        with col:
            if class_label == "High":
                color_hex = "#10B981"
            elif class_label == "Medium":
                color_hex = "#F59E0B"
            else:
                color_hex = "#EF4444"
            
            st.markdown(f"""
                <div style='background: {color_hex}; color: white; padding: 15px; 
                           border-radius: 10px; text-align: center;'>
                    <h3>{class_label}</h3>
                    <h2>{confidence:.1f}%</h2>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Show placement status categories
st.markdown("<h2 style='text-align: center; color: white;'>📊 Placement Status Categories</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
                    color: white; padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2); text-align: center;'>
            <h3 style='font-size: 1.8em;'>🟢 HIGH</h3>
            <p><b>Strong placement chances</b></p>
            <hr style='border-color: rgba(255,255,255,0.5);'>
            <p>✓ CGPA > 8.0<br>✓ Strong in all skills<br>✓ Active contributions</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); 
                    color: white; padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2); text-align: center;'>
            <h3 style='font-size: 1.8em;'>🟡 MEDIUM</h3>
            <p><b>Moderate placement chances</b></p>
            <hr style='border-color: rgba(255,255,255,0.5);'>
            <p>✓ CGPA 7.0-8.0<br>✓ Average skills<br>✓ Some experience</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); 
                    color: white; padding: 25px; border-radius: 15px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2); text-align: center;'>
            <h3 style='font-size: 1.8em;'>🔴 LOW</h3>
            <p><b>Low placement chances</b></p>
            <hr style='border-color: rgba(255,255,255,0.5);'>
            <p>⚠ CGPA < 7.0<br>⚠ Needs improvement<br>⚠ Limited experience</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; border-radius: 15px; text-align: center;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
        <h4>💡 Pro Tips to Improve Your Placement Chances:</h4>
        <p>📈 Keep CGPA above 8.0 | 💻 Build strong programming skills | 
        📚 Practice DSA regularly | 🎖️ Get certifications | 🐙 Active GitHub presence</p>
    </div>
""", unsafe_allow_html=True)
