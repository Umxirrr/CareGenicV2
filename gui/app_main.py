import tkinter as tk
from tkinter import messagebox, Toplevel
import pandas as pd
import pickle
import numpy as np
from backend.send_sms import send_sms
from backend.db_connect import connect_db

# Load model & encoder
model = pickle.load(open('../models/xgboost_model.pkl', 'rb'))
encoder = pickle.load(open('../models/label_encoder.pkl', 'rb'))
X_columns = pd.read_csv('../data/X.csv').columns.tolist()

# Disease info mapping
disease_info = {
    "Fever": ("Paracetamol", "Dr. Saima Ansari"),
    "Migraine": ("Ibuprofen", "Dr. Zubair Ahmed"),
    "Heart Disease": ("Atenolol", "Dr. Fatima Khan"),
    "Asthma": ("Salbutamol", "Dr. Mohammed Usman"),
    "Diabetes": ("Metformin", "Dr. Zubair Ahmed"),
    "UTI": ("Nitrofurantoin", "Dr. Anjali Sharma"),
    "Skin Allergy": ("Hydrocortisone", "Dr. Ramesh K."),
    "Throat Infection": ("Amoxicillin", "Dr. Saima Ansari"),
}

# Initialize GUI
root = tk.Tk()
root.title("CareGenic AI - Symptom Checker")
root.geometry("600x600")
root.resizable(False, False)

tk.Label(root, text="CareGenic AI Symptom Prediction", font=("Helvetica", 16, "bold")).pack(pady=10)

# Input fields
tk.Label(root, text="Patient Name:").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Age:").pack()
entry_age = tk.Entry(root, width=40)
entry_age.pack()

tk.Label(root, text="Mobile No:").pack()
entry_mobile = tk.Entry(root, width=40)
entry_mobile.pack()

# Symptoms
tk.Label(root, text="\nSelect Symptoms:").pack()
symptom_vars = {}
frame = tk.Frame(root)
frame.pack(pady=10)

for i, symptom in enumerate(X_columns):
    var = tk.IntVar()
    cb = tk.Checkbutton(frame, text=symptom, variable=var)
    cb.grid(row=i // 2, column=i % 2, sticky='w', padx=5)
    symptom_vars[symptom] = var

# Predict logic
def predict():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    mobile = entry_mobile.get().strip()

    if not name or not age or not mobile:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    if not mobile.isdigit() or len(mobile) != 10:
        messagebox.showerror("Input Error", "Enter a valid 10-digit mobile number.")
        return

    # Build feature vector
    input_data = [symptom_vars[s].get() for s in X_columns]
    input_array = np.array([input_data])
    prediction_num = model.predict(input_array)[0]
    disease = encoder.inverse_transform([prediction_num])[0]
    medicine, doctor = disease_info.get(disease, ("Consult physician", "N/A"))

    # Compose SMS
    sms_text = (
        f"Hello {name},\n"
        f"Disease: {disease}\n"
        f"Medicine: {medicine}\n"
        f"Doctor: {doctor}\n"
        f"- CareGenic AI"
    )
    full_number = "+91" + mobile
    sms_success, sms_response = send_sms(full_number, sms_text)
    sms_status = "✅ SMS Sent!" if sms_success else f"❌ SMS Failed: {sms_response}"

    # Save to RDS
    try:
        conn = connect_db()
        cursor = conn.cursor()
        symptoms_selected = [s for s in X_columns if symptom_vars[s].get() == 1]
        symptoms_text = ", ".join(symptoms_selected)

        cursor.execute("""
            INSERT INTO patients (name, age, phone, symptoms, disease, medicine, doctor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, age, mobile, symptoms_text, disease, medicine, doctor))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Data saved to RDS.")
    except Exception as e:
        print("❌ RDS save failed:", str(e))

    # Show result
    result_window = Toplevel(root)
    result_window.title("Prediction Result")
    result_window.geometry("400x300")

    tk.Label(result_window, text="Prediction Result", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(result_window, text=f"Name: {name}", font=("Helvetica", 11)).pack(pady=4)
    tk.Label(result_window, text=f"Disease: {disease}", font=("Helvetica", 11)).pack(pady=4)
    tk.Label(result_window, text=f"Medicine: {medicine}", font=("Helvetica", 11)).pack(pady=4)
    tk.Label(result_window, text=f"Doctor: {doctor}", font=("Helvetica", 11)).pack(pady=4)
    tk.Label(result_window, text=sms_status, font=("Helvetica", 10, "italic")).pack(pady=10)

# Predict button
tk.Button(root, text="Predict Disease", command=predict,
          bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

root.mainloop()
