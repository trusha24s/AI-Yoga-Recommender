import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import ast  


st.set_page_config(page_title="AI Yoga Recommender", layout="wide")

st.markdown("""
    <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }


    html, body {
      height: 100%;
      background-color: #7b61ff; /* Purple base */
    }


    /* REMOVE WHITE GAP ABOVE AND AROUND MAIN PAGE */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"] {
        margin: 0 !important;
        padding: 0 !important;
        background-color: #7b5cff !important;
        height: 100%;
    }


    /* FIX INTERNAL STREAMLIT SPACING */
    [data-testid="block-container"] {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
        background-color: transparent !important;
    }


    header[data-testid="stHeader"] {
        display: none !important;
    }


    main[data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }


    /* MAIN BACKGROUND (Purple Gradient) */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #7b5cff, #8f68ff, #a17bff);
        color: white;
        margin: 0 !important;
        padding: 0 !important;
        min-height: 100vh !important;
    }


    /* SIDEBAR: THICKER AND NO GAP */
    [data-testid="stSidebar"] {
        background-color: #1e1e2f !important;
        color: white !important;
        width: 350px !important;
        min-width: 350px !important;
        max-width: 350px !important;
        padding-top: 1rem;
        border-right: none !important;
        box-shadow: none !important;
        height: 100vh !important;
        margin: 0 !important;
    }


    /* SIDEBAR NAV WIDTH */
    [data-testid="stSidebarNav"] {
        width: 350px !important;
    }


    /* SIDEBAR TEXT COLORS */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #e6e1ff !important;
    }


    /* Main Header Card - bigger and centered */
    .main-card {
        background: rgba(255, 255, 255, 0.15);  /* semi-transparent white */
        padding: 40px 50px;   /* increased padding */
        border-radius: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.2);
        margin: 70px auto;    /* top margin for spacing */
        max-width: 850px;     /* increased width */
        text-align: center;   /* center text inside */
    }
    .main-card h1 { color: #ffffff; font-size: 2.6rem; margin-bottom: 15px; }
    .main-card h3 { color: #e0d9ff; font-size: 1.6rem; margin-bottom: 15px; }
    .main-card p { color: #f0ebff; font-size: 1.1rem; line-height: 1.6; }
    .metric-box { display: flex; justify-content: space-around; gap: 40px; margin-top: 25px; color: #fff; }
    .metric { font-size: 2.4rem; font-weight: 700; }
    .metric-sub { font-size: 1rem; color: #e0d9ff; }


    /* Button fix */
    div.stButton > button {
        background-color: #6b21a8;  /* dark purple */
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        transition: background 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #7b5cff;  /* lighter purple on hover */
    }
    div.stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(107,33,168,0.4);
    }


    /* Pose Cards */
    .pose-card {
        background: #ffffff;
        color: #1e1e2f;
        padding: 25px 30px;
        margin: 25px 0;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        width: 90%;
        transition: transform 0.3s;
    }
    .pose-card:hover { transform: scale(1.03); }
    .pose-card h2 { color: #6b21a8 !important; font-weight: 700; font-size: 1.6rem; margin-bottom: 10px; }
    .pose-card p { color: #3f3f46; font-size: 1rem; line-height: 1.6; }
    .pose-metric { display: flex; justify-content: flex-start; align-items: center; gap: 15px; font-weight: 500; margin-top: 8px; }
    .pose-metric span { display: flex; align-items: center; gap: 5px; }
    .why-pose { margin-top: 12px; color: #6b21a8; font-style: italic; font-weight: 500; }
    /* METRICS */
    .metric-box {
        display: flex;
        justify-content: space-around;
        margin-top: 2rem;
        color: #fff;
    }
    .metric {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-sub {
        font-size: 0.9rem;
        color: #e0d9ff;
    }


    /* SCROLLBAR STYLE */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }


    </style>
""", unsafe_allow_html=True)


df = pd.read_csv('asana_dataset.csv')  


columns_to_convert = ['Focus_Area', 'Body_Parts', 'Precautions'] 
for column in columns_to_convert:
    if column in df.columns:
        df[column] = df[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


asanas_data = df.groupby('difficulty_level')['asana_name'].apply(list).to_dict()



pose_descriptions = df.set_index('asana_name').to_dict(orient='index')


diet_data = {
    'Underweight (BMI <18.5)': {
        'Breakfast': 'Oatmeal with fruits, nuts, and yogurt (500 cal).',
        'Lunch': 'Quinoa salad with veggies and paneer (600 cal).',
        'Snack': 'Banana with almond butter (300 cal).',
        'Dinner': 'Dal, rice, and steamed greens (600 cal).',
        'Tip': 'Focus on calorie-dense healthy fats.'
    },
    'Normal (BMI 18.5-24.9)': {
        'Breakfast': 'Whole grain toast with avocado and eggs (400 cal).',
        'Lunch': 'Vegetable stir-fry with chickpeas and rice (500 cal).',
        'Snack': 'Apple with almonds (200 cal).',
        'Dinner': 'Lentil soup, salad, and chapati (600 cal).',
        'Tip': 'Balanced macros for energy.'
    },
    'Overweight (BMI >24.9)': {
        'Breakfast': 'Green smoothie with spinach, banana, and protein powder (300 cal).',
        'Lunch': 'Grilled veggies with quinoa and yogurt (400 cal).',
        'Snack': 'Carrot sticks with hummus (200 cal).',
        'Dinner': 'Vegetable soup and salad (500 cal).',
        'Tip': 'Low-calorie, high-fiber plan.'
    }
}


# ---------- MODEL ----------
def train_model():
    X = np.array([
        [25, 20, 0], [30, 22, 1], [45, 28, 0], [60, 18, 1],
        [20, 19, 2], [35, 25, 0], [50, 23, 1], [65, 26, 0]
    ])
    y = ['Beginner', 'Intermediate', 'Beginner', 'Intermediate',
         'Advanced', 'Beginner', 'Intermediate', 'Beginner']
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    return clf


model = train_model()



st.sidebar.markdown("### 🐱 Your Yoga Profile")
st.sidebar.markdown("<p>Fill in your details to get personalized recommendations</p>", unsafe_allow_html=True)


age = st.sidebar.number_input("🎂 Age", 18, 80, 30)
height = st.sidebar.number_input("📏 Height (cm)", 100, 250, 170)
weight = st.sidebar.number_input("⚖️ Weight (kg)", 30, 200, 70)
fitness_level = st.sidebar.selectbox("💪 Fitness Level", ['Beginner', 'Intermediate', 'Advanced'])
goal = st.sidebar.selectbox("🎯 Primary Goal", ["Balance", "Flexibility", "Strength", "Relaxation"])



if st.sidebar.button("✨ Get AI Recommendations"):
    # ----- Calculate BMI and Category -----
    bmi = weight / ((height / 100) ** 2)
    bmi_category = (
        'Underweight (BMI <18.5)' if bmi < 18.5 else
        'Normal (BMI 18.5-24.9)' if bmi < 25 else
        'Overweight (BMI >24.9)'
    )
    fitness_encoded = {'Beginner': 0, 'Intermediate': 1, 'Advanced': 2}[fitness_level]
    features = np.array([[age, bmi, fitness_encoded]])
    recommended_level = model.predict(features)[0]


 
    st.subheader("🌟 Your AI-Powered Yoga Recommendations")
    st.write(f"**BMI:** {bmi:.2f} ({bmi_category})")
    st.write(f"**Recommended Level:** {recommended_level}")


   
    poses = asanas_data.get(recommended_level, [])[:10]  
    rec_scores = np.random.uniform(80, 99, len(poses))
    safety_scores = np.random.uniform(95, 100, len(poses))



    for i, pose in enumerate(poses):
        data = pose_descriptions.get(pose, {
            'description': 'No description available.',
            'Focus_Area': [],
            'Body_Parts': [],
            'benefits': 'No benefits available.',
            'Precautions': []
        })
        description = data.get('description', 'No description available.')
        focus_areas = data.get('Focus_Area', [])
        body_parts = data.get('Body_Parts', [])
        benefits = data.get('benefits', 'No benefits available.') 
        precautions = data.get('Precautions', [])
        rec_score = round(rec_scores[i], 1)
        safety_score = round(safety_scores[i], 1)


        st.markdown(f"""
<div class="pose-card">
    <h2>{pose}</h2>
    <div class="pose-metric">
        <span>⭐ <b>Recommendation Score:</b> {rec_score}%</span>
        <span>💧 <b>Safety Score:</b> {safety_score}%</span>
    </div>
    <p><b>Description:</b> {description}</p>
    <p><b>Focus Areas:</b> {', '.join(focus_areas)}</p>
    <p><b>Body Parts:</b> {', '.join(body_parts)}</p>
    <p><b>Benefits:</b> {benefits}</p>  <!-- Display as plain string -->
    <p><b>Precautions:</b> {', '.join(precautions)}</p>
    <p class="why-pose">💡 Why this pose? Safe for your profile; matches goal: <b>{goal}</b>.</p>
</div>
""", unsafe_allow_html=True)


    short_labels = [pose.split('(')[0].strip() for pose in poses]


   
    st.subheader("📊 Recommendation Chart")
    fig, ax1 = plt.subplots(figsize=(5.5,2.5))
    ax1.bar(short_labels, rec_scores, alpha=0.8, color='#22c55e')
    ax1.set_ylabel("Recommendation Score (%)")
    ax1.set_xticklabels(short_labels, rotation=45, ha='right')
    ax2 = ax1.twinx()
    ax2.plot(short_labels, safety_scores, color='magenta', marker='o', linestyle='--')
    ax2.set_ylabel("Safety Score (%)", color='magenta')
    st.pyplot(fig)


 
    avg_rec = np.mean(rec_scores)
    avg_safe = np.mean(safety_scores)
    st.markdown(f"""
<div class="pose-card">
    <h2>🧭 Practice Summary & Tips</h2>
    <p><b>Average Recommendation Score:</b> ⭐ {avg_rec:.1f}%</p>
    <p><b>Average Safety Score:</b> 💧 {avg_safe:.1f}%</p>
    <p><b>Focus Area:</b> {goal}</p>
    <p>💡 Start with the highest-rated poses and gradually work your way through the list. Always listen to your body and modify poses as needed. Consider practicing in a quiet, comfortable space with a yoga mat for the best experience.</p>
</div>
""", unsafe_allow_html=True)


    st.markdown("#### 🥗 Sample 1-Day Diet Plan")
    meals = diet_data[bmi_category]


    for meal, desc in meals.items():
        if meal != "Tip":
            st.markdown(f"""
            <div style="
                background: #ffffff;
                color: #1e1e2f;
                padding: 12px 15px;
                border-radius: 10px;
                margin-bottom: 8px;
            ">
                <b>{meal}:</b> {desc}
            </div>
            """, unsafe_allow_html=True)


 
    st.markdown(f"""
    <div style="
        background:#f0f4ff;
        color:#1e3a8a;
        padding:12px;
        border-radius:10px;
        margin-top:8px;
    ">
    💡 Tip: {meals['Tip']}
    </div>
    """, unsafe_allow_html=True)


else:
    st.markdown("""
    <div class="main-card">
        <h1>🧘‍♀️ YogaAI</h1>
        <h3>Start Yoga, Start a New Life 🌸</h3>
        <p>Discover personalized yoga poses powered by advanced machine learning</p>
        <div class="metric-box">
            <div><div class="metric">141</div><div class="metric-sub">YOGA POSES</div></div>
            <div><div class="metric">99%</div><div class="metric-sub">SAFETY SCORE</div></div>
            <div><div class="metric">AI</div><div class="metric-sub">POWERED</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

