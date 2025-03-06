#1(a) Bmi mean and standard deviation for patients who have had a stroke.
import pandas as pd
data = pd.read_csv("stroke.csv")
print(data)

print(data.stroke)

# 1(b) NA values in the data. Count the rows that have stroke as 0 and 1 respectively when bmi is null

Bmi = data[data["bmi"].notnull()]
Bmi_Null = data[data["bmi"].isnull()]

Bmi_no_stroke = Bmi[Bmi['stroke'] == 0]

Bmi_no_stroke.shape[0]

Bmi_stroke = Bmi[Bmi['stroke'] == 1]
Bmi_stroke.shape[0]
print(f"Number of rows where stroke = 0 and bmi is null: {len(Bmi_Null)}")
print("Number of rows where stroke = 1 and bmi is null: ['Bmi_stroke']")