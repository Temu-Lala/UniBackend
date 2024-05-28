# import csv
# import random
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, f1_score
# import joblib

# # Step 1: Define Ethiopian Universities Data
# universities_data = {
#     "Hawassa University": {
#         "location": "Hawassa",
#         "fields_offered": ["Engineering", "Medicine", "Business", "Computer Science"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Addis Ababa University": {
#         "location": "Addis Ababa",
#         "fields_offered": ["Engineering", "Medicine", "Computer Science", "Arts", "Sciences"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Bahir Dar University": {
#         "location": "Bahir Dar",
#         "fields_offered": ["Engineering", "Medicine", "Sciences"],
#         "health_condition_support": ["None"]
#     },
#     "Mekelle University": {
#         "location": "Mekelle",
#         "fields_offered": ["Engineering", "Business", "Sciences"],
#         "health_condition_support": ["None", "Visual Impairment"]
#     },
#     "Jimma University": {
#         "location": "Jimma",
#         "fields_offered": ["Medicine", "Agriculture", "Business"],
#         "health_condition_support": ["None", "Physical Disability", "Visual Impairment"]
#     },
#     "Haramaya University": {
#         "location": "Dire Dawa",
#         "fields_offered": ["Agriculture", "Business", "Engineering", "Education"],
#         "health_condition_support": ["None"]
#     },
#     "Arba Minch University": {
#         "location": "Arba Minch",
#         "fields_offered": ["Engineering", "Business", "Social Sciences"],
#         "health_condition_support": ["None"]
#     },
#     "Wolaita Sodo University": {
#         "location": "Wolaita",
#         "fields_offered": ["Engineering", "Education", "Health Science"],
#         "health_condition_support": ["None"]
#     },
#     "Adama Science and Technology University": {
#         "location": "Adama",
#         "fields_offered": ["Engineering", "Computer Science", "Business"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Debre Markos University": {
#         "location": "Debre Markos",
#         "fields_offered": ["Agriculture", "Natural Science", "Social Science"],
#         "health_condition_support": ["None"]
#     },
#     "Dilla University": {
#         "location": "Dilla",
#         "fields_offered": ["Agriculture", "Business", "Education", "Health Science"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Assosa University": {
#         "location": "Assosa",
#         "fields_offered": ["Agriculture", "Business", "Education", "Law"],
#         "health_condition_support": ["None", "Visual Impairment"]
#     },
#     "Welkite University": {
#         "location": "Welkite",
#         "fields_offered": ["Agriculture", "Business", "Education", "Technology"],
#         "health_condition_support": ["None", "Hearing Impairment"]
#     },
#     "Woldia University": {
#         "location": "Woldia",
#         "fields_offered": ["Agriculture", "Business", "Education", "Engineering"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Amboseli University": {
#         "location": "Amboseli",
#         "fields_offered": ["Agriculture", "Business", "Education", "Health Science"],
#         "health_condition_support": ["None", "Visual Impairment"]
#     },
#     "Mizan-Tepi University": {
#         "location": "Mizan-Tepi",
#         "fields_offered": ["Agriculture", "Business", "Education", "Law"],
#         "health_condition_support": ["None", "Hearing Impairment"]
#     },
#     "Dire Dawa University": {
#         "location": "Dire Dawa",
#         "fields_offered": ["Engineering", "Business", "Education", "Health Science"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Shashemene University": {
#         "location": "Shashemene",
#         "fields_offered": ["Agriculture", "Business", "Education", "Technology"],
#         "health_condition_support": ["None", "Visual Impairment"]
#     },
#     "Wondo Genet College of Forestry": {
#         "location": "Wondo Genet",
#         "fields_offered": ["Forestry", "Environmental Science", "Wildlife Conservation"],
#         "health_condition_support": ["None", "Physical Disability"]
#     },
#     "Ethiopian Civil Service University": {
#         "location": "Addis Ababa",
#         "fields_offered": ["Public Administration", "Law", "Development Studies"],
#         "health_condition_support": ["None", "Visual Impairment"]
#     }
# }

# # Step 2: Generate Fake Student Data
# genders = ["Male", "Female"]
# fields = ["Engineering", "Medicine", "Business", "Computer Science", "Law", "Arts", "Sciences",
#           "Agriculture", "Education", "Health Science", "Natural Science", "Social Science"]
# health_conditions = ["None", "Physical Disability", "Visual Impairment", "Hearing Impairment"]

# def generate_exam_result():
#     return random.randint(50, 100)

# def generate_student_data(num_students):
#     students = []
#     for _ in range(num_students):
#         gender = random.choice(genders)
#         field_choices = random.sample(fields, random.randint(1, 3))
#         health_condition = random.choice(health_conditions)
#         exam_result = generate_exam_result()
#         student = {
#             "gender": gender,
#             "field_choices": field_choices,
#             "health_condition": health_condition,
#             "exam_result": exam_result
#         }
#         students.append(student)
#     return students

# num_students = 10000
# students = generate_student_data(num_students)

# # Step 3: Create a CSV file and store the student data
# import csv

# with open("student_data.csv", "w", newline="") as csvfile:
#     fieldnames = ["gender", "field_choices", "health_condition", "exam_result"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for student in students:
#         field_choices = ",".join(student["field_choices"])
#         writer.writerow({
#             "gender": student["gender"],
#             "field_choices": field_choices,
#             "health_condition": student["health_condition"],
#             "exam_result": student["exam_result"]
#         })

# # Step 4: Load data from the CSV file into a pandas DataFrame
# try:
#     student_data = pd.read_csv("student_data.csv", error_bad_lines=False, warn_bad_lines=True)
# except pd.errors.ParserError as e:
#     print(f"Error reading the CSV file: {e}")
#     student_data = pd.DataFrame()

# # Step 5: Preprocess the data for machine learning
# categorical_features = ["gender", "health_condition"]
# label_encoder = LabelEncoder()
# one_hot_encoder = OneHotEncoder(handle_unknown="ignore")

# categorical_transformer = ColumnTransformer(
#     transformers=[
#         ("encoder", one_hot_encoder, categorical_features)
#     ],
#     remainder="passthrough"
# )

# X = categorical_transformer.fit_transform(student_data.drop(columns=['field_choices']))

# y = []
# for _, row in student_data.iterrows():
#     if isinstance(row["field_choices"], str):
#         field_choices = row["field_choices"].split(",")
#     else:
#         field_choices = []
#     health_condition = row["health_condition"]
#     matching_universities = [
#         name for name, data in universities_data.items()
#         if any(field in data["fields_offered"] for field in field_choices) and
#            (health_condition in data["health_condition_support"])
#     ]

#     if matching_universities:
#         y.append(random.choice(matching_universities))
#     else:
#         y.append("No Matching University")

# label_encoder.fit(y)
# y = label_encoder.transform(y)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)

# accuracy = accuracy_score(y_test, y_pred)
# f1 = f1_score(y_test, y_pred, average='weighted')
# print(f"Model accuracy: {accuracy:.2f}")
# print(f"Model F1-score: {f1:.2f}")

# joblib.dump(model, "ethiopian_university_recommender_model.joblib")
# print("Trained model exported to 'ethiopian_university_recommender_model.joblib'")

# def recommend_universities(student):
#     gender = student["gender"]
#     field_choices = student["field_choices"]
#     health_condition = student["health_condition"]
#     exam_result = student["exam_result"]

#     student_data = pd.DataFrame({
#         "gender": [gender],
#         "health_condition": [health_condition],
#         "exam_result": [exam_result]
#     })
#     X_student = categorical_transformer.transform(student_data)

#     predicted_labels = model.predict_proba(X_student)[0]
#     sorted_indices = predicted_labels.argsort()[::-1]
#     sorted_probabilities = predicted_labels[sorted_indices]
#     sorted_universities = label_encoder.inverse_transform(sorted_indices)

#     matching_universities = [
#         name for name, data in universities_data.items()
#         if any(field in data["fields_offered"] for field in field_choices) and
#            (health_condition in data["health_condition_support"])
#     ]

#     sorted_universities = [u for u in sorted_universities if u in matching_universities]

#     print(f"Recommended universities for {gender} student interested in {', '.join(field_choices)}:")
#     for i, university in enumerate(sorted_universities):
#         probability = sorted_probabilities[i]
#         print(f"{i+1}. Name: {university}, Probability: {probability:.2f}")

# random_student = random.choice(students)
# recommend_universities(random_student)
