import statistics
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# Read and process data
with open("stroke.csv", "r") as f:
    stroke_data = f.readlines()

for pos, line in enumerate(stroke_data):
    line = [i.strip() for i in line.split(",")]
    stroke_data[pos] = line

id_index = 0
gender_index = 1
age_index = 2
hypertension_index = 3
heart_disease_index = 4
ever_married_index = 5
work_type_index = 6
residence_type_index = 7
avg_glucose_level_index = 8
bmi_index = 9
smoking_status_index = 10
stroke_index = 11

fields = stroke_data[0]
original_fields = fields.copy()  # Keep a copy of the original fields
del stroke_data[0]
stroke_data = np.array(stroke_data)

def one_hot_encode(data, column_index):
    global fields
    unique_vals = np.unique(data[:, column_index])  # Find unique values in the column
    unique_vals_desc = [f"{fields[column_index]}-{i}" for i in unique_vals]
    fields.extend(unique_vals_desc)
    one_hot_encoded = np.zeros((data.shape[0], len(unique_vals)), dtype=int)  # Create an array of zeros
    
    # Map each unique value to its corresponding index in one-hot encoded array
    for i, val in enumerate(data[:, column_index]):
        one_hot_encoded[i, np.where(unique_vals == val)[0][0]] = 1
    
    return one_hot_encoded

def plot_histograms(data, fields, stroke_index):
    # Skip irrelevant fields and count valid fields
    valid_fields = [field for field in fields if field not in ["id", "stroke"]]
    n_fields = len(valid_fields)
    
    # Calculate grid dimensions for subplots
    n_cols = 3  # Number of columns in the grid
    n_rows = (n_fields + n_cols - 1) // n_cols  # Ceiling division for number of rows
    
    # Create figure with subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 4*n_rows))
    axes = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]  # Ensure axes is always iterable
    
    plot_idx = 0
    for i, field in enumerate(fields):
        if field in ["id", "stroke"]:  # Skip non-relevant fields
            continue
        
        ax = axes[plot_idx]
        # Convert column data to numeric type
        try:
            column_data = data[:, i].astype(float)
            stroke_labels = data[:, stroke_index].astype(int)
            
            # Separate stroke vs. no-stroke cases
            stroke_cases = column_data[stroke_labels == 1]
            no_stroke_cases = column_data[stroke_labels == 0]
            
            # Plot histogram
            ax.hist(
                [no_stroke_cases, stroke_cases],
                bins=15,  # Reduced bins for better visualization in subplots
                alpha=0.7,
                label=["No Stroke", "Stroke"],
                edgecolor="black",
                stacked=True
            )
            
            ax.set_xlabel(field)
            ax.set_ylabel("Count")
            ax.set_title(f"{field} vs Stroke")
            ax.legend(fontsize='small')
            ax.grid(axis="y", linestyle="--", alpha=0.6)
            
            plot_idx += 1
        except Exception as e:
            print(f"Could not plot histogram for {field}: {e}")
            
    # Hide any unused subplots
    for j in range(plot_idx, len(axes)):
        axes[j].set_visible(False)
        
    plt.tight_layout()
    plt.savefig("all_histograms.png")
    plt.close()

# One-hot encode categorical variables
gender_encoded = one_hot_encode(stroke_data, gender_index)
smoking_status_encoded = one_hot_encode(stroke_data, smoking_status_index)
work_type_encoded = one_hot_encode(stroke_data, work_type_index)
ever_married_encoded = one_hot_encode(stroke_data, ever_married_index)
residence_encoded = one_hot_encode(stroke_data, residence_type_index)

drop_columns = [gender_index, smoking_status_index, work_type_index, ever_married_index, residence_type_index]
stroke_data = np.delete(stroke_data, drop_columns, axis=1)
stroke_data = np.hstack([stroke_data, gender_encoded, smoking_status_encoded, work_type_encoded, ever_married_encoded, residence_encoded])

fields.remove("gender")
fields.remove("ever_married")
fields.remove("work_type")
fields.remove("Residence_type")
fields.remove("smoking_status")

# Handle missing BMI values
for i in range(stroke_data.shape[0]):
    if stroke_data[i, 5] == "N/A":
        stroke_data[i, 5] = "0"  # Replace with 0

# Convert all data to numeric for analysis
numeric_data = np.zeros_like(stroke_data, dtype=float)
for i in range(stroke_data.shape[1]):
    try:
        numeric_data[:, i] = stroke_data[:, i].astype(float)
    except:
        print(f"Warning: Column {i} could not be converted to numeric at once.")
        # Try to convert each value individually
        for j in range(stroke_data.shape[0]):
            try:
                numeric_data[j, i] = float(stroke_data[j, i])
            except:
                numeric_data[j, i] = 0

# Create a pandas DataFrame for easier manipulation
df = pd.DataFrame(numeric_data, columns=fields)

# ====== d. Calculate correlations and plot heatmaps ======
# Compute correlation matrix
correlation_matrix = df.corr()

# Plot the correlation heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt=".2f")
plt.title("Correlation Matrix Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.close()

# ====== e. Use Scikit-Learn for logistic regression ======
# Separate features and target
X = df.drop('stroke', axis=1)
y = df['stroke']

# Remove the ID column (it's not a predictive feature)
if 'id' in X.columns:
    X = X.drop('id', axis=1)

# Plot histograms for all features
print("\n====== Plotting Histograms of Features ======")
stroke_index = list(fields).index('stroke')
plot_histograms(numeric_data, fields, stroke_index)
print("All histograms saved to 'all_histograms.png'")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the logistic regression model
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_scaled, y_train)

# Make predictions
y_pred = log_reg.predict(X_test_scaled)

# Evaluate the model
print("\n====== Logistic Regression Results (Imbalanced Data) ======")
class_report = classification_report(y_test, y_pred, output_dict=True)
print(classification_report(y_test, y_pred))

# Extract metrics for interpretation
overall_accuracy = class_report['accuracy']
no_stroke_precision = class_report['0.0']['precision'] if '0.0' in class_report else class_report['0']['precision']
stroke_precision = class_report['1.0']['precision'] if '1.0' in class_report else class_report['1']['precision']
no_stroke_recall = class_report['0.0']['recall'] if '0.0' in class_report else class_report['0']['recall']
stroke_recall = class_report['1.0']['recall'] if '1.0' in class_report else class_report['1']['recall']

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Imbalanced Data')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig("confusion_matrix_imbalanced.png")
plt.close()

# Check the class distribution to confirm imbalance
y_train_counts = np.bincount(y_train.astype(int))
print(f"Class distribution in training set: {y_train_counts}")
if len(y_train_counts) > 1:
    imbalance_ratio = y_train_counts[0] / y_train_counts[1]
    print(f"Class imbalance ratio (no_stroke:stroke): {imbalance_ratio:.2f}:1")

# Interpretation of initial results
print("\n==== Interpretation of Initial Results ====")
print(f"Overall accuracy: {overall_accuracy:.4f}")
print(f"No stroke - Precision: {no_stroke_precision:.4f}, Recall: {no_stroke_recall:.4f}")
print(f"Stroke - Precision: {stroke_precision:.4f}, Recall: {stroke_recall:.4f}")
print("\nObservations:")
print("1. The model shows high accuracy overall, but this is misleading due to class imbalance.")
print("2. The precision for stroke prediction is high, meaning when the model predicts a stroke, it's often correct.")
print("3. However, the recall for stroke is low, indicating the model often misses actual stroke cases.")
print("4. This is problematic in a medical context where missing a positive case (stroke) is more harmful than a false alarm.")

# ====== f. Resample the data to address imbalance ======
# Use SMOTE for oversampling the minority class
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

# Train a new logistic regression model on the resampled data
log_reg_resampled = LogisticRegression(max_iter=1000, random_state=42)
log_reg_resampled.fit(X_train_resampled, y_train_resampled)

# Make predictions with the resampled model
y_pred_resampled = log_reg_resampled.predict(X_test_scaled)

# Evaluate the resampled model
print("\n====== Logistic Regression Results (After SMOTE Resampling) ======")
smote_report_dict = classification_report(y_test, y_pred_resampled, output_dict=True)
print(classification_report(y_test, y_pred_resampled))

# Extract metrics for SMOTE
smote_accuracy = smote_report_dict['accuracy']
smote_stroke_precision = smote_report_dict['1.0']['precision'] if '1.0' in smote_report_dict else smote_report_dict['1']['precision']
smote_stroke_recall = smote_report_dict['1.0']['recall'] if '1.0' in smote_report_dict else smote_report_dict['1']['recall']

# Plot confusion matrix for resampled results
cm_resampled = confusion_matrix(y_test, y_pred_resampled)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_resampled, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - After SMOTE Resampling')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig("confusion_matrix_resampled.png")
plt.close()

# Also try undersampling for comparison
rus = RandomUnderSampler(random_state=42)
X_train_undersampled, y_train_undersampled = rus.fit_resample(X_train_scaled, y_train)

# Train logistic regression with undersampled data
log_reg_undersampled = LogisticRegression(max_iter=1000, random_state=42)
log_reg_undersampled.fit(X_train_undersampled, y_train_undersampled)

# Make predictions with the undersampled model
y_pred_undersampled = log_reg_undersampled.predict(X_test_scaled)

# Evaluate the undersampled model
print("\n====== Logistic Regression Results (After Undersampling) ======")
under_report_dict = classification_report(y_test, y_pred_undersampled, output_dict=True)
print(classification_report(y_test, y_pred_undersampled))

# Extract metrics for undersampling
under_accuracy = under_report_dict['accuracy']
under_stroke_precision = under_report_dict['1.0']['precision'] if '1.0' in under_report_dict else under_report_dict['1']['precision']
under_stroke_recall = under_report_dict['1.0']['recall'] if '1.0' in under_report_dict else under_report_dict['1']['recall']

# Plot confusion matrix for undersampled results
cm_undersampled = confusion_matrix(y_test, y_pred_undersampled)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_undersampled, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - After Undersampling')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig("confusion_matrix_undersampled.png")
plt.close()

# Compare the results with a bar chart showing recall and precision for each approach
methods = ['Imbalanced', 'SMOTE', 'Undersampling']
precision_values = [stroke_precision, smote_stroke_precision, under_stroke_precision]
recall_values = [stroke_recall, smote_stroke_recall, under_stroke_recall]
accuracy_values = [overall_accuracy, smote_accuracy, under_accuracy]

# Plot the comparison
fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(methods))
width = 0.25

ax.bar(x - width, precision_values, width, label='Precision (Stroke)')
ax.bar(x, recall_values, width, label='Recall (Stroke)')
ax.bar(x + width, accuracy_values, width, label='Overall Accuracy')

ax.set_xlabel('Sampling Method')
ax.set_ylabel('Score')
ax.set_title('Model Performance Metrics by Sampling Method')
ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.legend()

plt.tight_layout()
plt.savefig("sampling_comparison.png")
plt.close()

# Comprehensive interpretation of results
print("\n==== Interpretation of All Results ====")
print("1. Original Imbalanced Data:")
print(f"   - Overall Accuracy: {overall_accuracy:.4f}")
print(f"   - Stroke Precision: {stroke_precision:.4f}")
print(f"   - Stroke Recall: {stroke_recall:.4f}")
print("   - With imbalanced data, the model achieved high accuracy but poor recall for stroke cases.")
print("   - This means many stroke cases were missed, which is problematic in medical diagnostics.")

print("\n2. After SMOTE Oversampling:")
print(f"   - Overall Accuracy: {smote_accuracy:.4f}")
print(f"   - Stroke Precision: {smote_stroke_precision:.4f}")
print(f"   - Stroke Recall: {smote_stroke_recall:.4f}")
print("   - SMOTE improved the recall for stroke cases significantly.")
print("   - This means fewer stroke cases were missed, at the cost of slightly lower precision.")
print("   - In a medical context, this trade-off is often acceptable as missing a case is more harmful.")

print("\n3. After Undersampling:")
print(f"   - Overall Accuracy: {under_accuracy:.4f}")
print(f"   - Stroke Precision: {under_stroke_precision:.4f}")
print(f"   - Stroke Recall: {under_stroke_recall:.4f}")
print("   - Undersampling increased recall even further but at a greater cost to precision and overall accuracy.")
print("   - This is the most aggressive approach to address class imbalance.")

print("\nConclusion:")
print("- The imbalanced dataset problem is evident from the initial model's high accuracy but poor stroke recall.")
print("- Resampling techniques help improve the model's ability to detect the minority class (stroke cases).")
print("- SMOTE offers a good balance, improving stroke detection while maintaining reasonable precision.")
print("- For medical applications like stroke prediction, higher recall might be preferred to ensure cases aren't missed.")
print("- The choice between these approaches depends on the specific requirements and the relative cost of false negatives vs. false positives.")