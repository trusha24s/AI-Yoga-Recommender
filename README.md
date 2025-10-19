# 🧘‍♀️ AI Yoga Recommender

The **AI Yoga Recommender** is a web-based application built using **Python** and **Streamlit**.  
It uses a **Decision Tree Classifier (Scikit-learn)** to recommend the most suitable **yoga asanas** to users based on their **age, height, weight, fitness goal, and experience level**.  
Along with yoga recommendations, it also provides **focus body parts, benefits, and precautions** for each asana, and includes **diet suggestions** for overall wellness.

---

## 💡 Project Overview

This project aims to help users discover yoga poses that are most beneficial for their individual body type and fitness goals.  
By entering basic personal details and fitness preferences, users receive personalized yoga and diet recommendations generated using an AI model.

---

## ⚙️ Working of the System

1. The user inputs their details such as **age, height, weight**, and **experience level (beginner/intermediate/advanced)**.  
2. The user selects their **goal**, such as:
   - Flexibility  
   - Strength  
   - Relaxation  
   - Balance  
3. The trained **Decision Tree Classifier** analyzes these inputs.  
4. Based on the dataset (`asana_dataset.csv`), the system recommends the **most suitable yoga asanas**.  
5. For each asana, details are displayed:
   - Focus body parts  
   - Benefits  
   - Precautions  
6. The system also gives **diet suggestions** to complement the yoga routine.

---

## 🧠 AI Model Used

- **Model:** Decision Tree Classifier (from Scikit-learn)  
- **Purpose:** To classify and recommend yoga poses according to user inputs.  
- **Reason for use:** It handles categorical and numerical data efficiently and provides clear, interpretable decision logic.  

---

## 🛠️ Technologies Used

- **Python** — main programming language  
- **Streamlit** — web app framework for building interactive UI  
- **Scikit-learn** — machine learning library used for the decision tree model  
- **Pandas, NumPy** — for dataset handling and preprocessing  
- **Matplotlib** — for visualizations (if any)

---

## 📁 Files and Structure

```plaintext
AI-Yoga-Recommender/
│
├── app.py                # Main Streamlit app
├── asana_dataset.csv     # Dataset containing yoga asanas, focus parts, benefits, precautions
├── requirements.txt      # Required Python libraries
├── README.md             # Project documentation
└── screenshots/          # (Optional) Screenshots of the web app interface

---

