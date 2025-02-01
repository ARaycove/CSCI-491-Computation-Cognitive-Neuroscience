import statistics
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# opens the stroke.csv file and returns a list object, with multiple lists, each list in the list object is a line from the csv. This should allow for quick collection by iterating over the list. But I'm sure there's a more efficient way to process this. 5000 lines of data should not take long, so we'll use the for loop iteration to summarize data.
with open("stroke.csv", "r") as f:
    data = f.read()
data_list = data.split("\n")
del data_list[0]

id_index                = 0
gender_index            = 1
age_index               = 2
hypertension_index      = 3
heart_disease_index     = 4
ever_married_index      = 5
work_type_index         = 6
Residence_type_index    = 7
avg_glucose_level_index = 8
bmi_index               = 9
smoking_status_index    = 10
stroke_index            = 11

for index, row in enumerate(data_list):
    data_list[index] = row.split(",")

num_data_lines = len(data_list)


bmi_values              = []
bmi_stroke_values       = []
bmi_not_stroke_values   = []
age_stroke_values       = []
age_not_stroke_values   = []
total_stroke        = 0
total_not_stroke    = 0
na_strokes          = 0
na_not_strokes      = 0
valid_values        = 0

age_male_stroke_values          = []
age_male_not_stroke_values      = []
age_female_stroke_values        = []
age_female_not_stroke_values    = []

for line in data_list:
    if not isinstance(line, list):
        print(line)
    has_had_stroke = int(line[stroke_index])
    gender         = (line[gender_index])
    age            = (float(line[age_index]))
    # Calculate BMI mean
    try:
        bmi = float(line[bmi_index])
        bmi_values.append(bmi)
        if has_had_stroke == 1:
            bmi_stroke_values.append(bmi)
        elif has_had_stroke == 0:
            bmi_not_stroke_values.append(bmi)
        else:
            print("Something went wrong")
    except:
        if has_had_stroke == 1:
            na_strokes += 1
        else:
            na_not_strokes += 1
    # Gather age distribution data
    if has_had_stroke == 1:
        age_stroke_values.append(age)
        total_stroke += 1
        if gender == "Male":
            age_male_stroke_values.append(age)
        elif gender == "Female":
            age_female_stroke_values.append(age)
        else:
            pass
    elif has_had_stroke == 0:
        age_not_stroke_values.append(age)
        total_not_stroke += 1
        if gender == "Male":
            age_male_not_stroke_values.append(age)
        elif gender == "Female":
            age_female_not_stroke_values.append(age)
        else:
            pass
    else:
        pass
    
bmi_mean                = sum(bmi_values)               / len(bmi_values)
bmi_stroke_mean         = sum(bmi_stroke_values)        / len(bmi_stroke_values)
bmi_not_stroke_mean     = sum(bmi_not_stroke_values)    / len(bmi_not_stroke_values)
bmi_std_dev             = statistics.stdev(bmi_values)
bmi_stroke_std_dev      = statistics.stdev(bmi_stroke_values)
bmi_not_stroke_std_dev  = statistics.stdev(bmi_not_stroke_values)

print(f"Total with Stroke:              {total_stroke}")
print(f"Total without Stroke:           {total_not_stroke}")
print(f"Overall BMI mean:               {bmi_mean}")
print(f"Stroke BMI Mean:                {bmi_stroke_mean}")
print(f"Not Stroke BMI Mean:            {bmi_not_stroke_mean}")
print(f"Overall BMI Standard Deviation: {bmi_std_dev}")
print(f"Stroke BMI Standard Dev:        {bmi_stroke_std_dev}")
print(f"Not Stroke BMI Standard Dev:    {bmi_not_stroke_std_dev}")
print(f"##############")
print(f"Unrecorded BMI total has_had_stroke:    {na_strokes:*^25}")
print(f"Unrecorded BMI total has_not_had_stroke:{na_not_strokes:*^25}")
print_graphs = False
if True:
    # Mean and std_dev
    box_plot_data_two = [[bmi_stroke_mean, bmi_stroke_std_dev], [bmi_not_stroke_mean, bmi_not_stroke_std_dev]]
    plt.boxplot(box_plot_data_two)
    plt.show()
    # Spit out Box plot
    box_plot_data = [bmi_stroke_values, bmi_not_stroke_values]
    plt.boxplot(box_plot_data)
    plt.show()
if False:
    # Plot histogram age_distributions
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    axs[0].hist(age_stroke_values, bins=30)
    axs[1].hist(age_not_stroke_values, bins=30)
    plt.show()
if False:
    # Plot density plot age dist / stroke - no stroke
    sns.kdeplot(age_stroke_values)
    plt.show()
    sns.kdeplot(age_not_stroke_values)
    plt.show()
if False:
    # Plot density plots by gender/stroke (4 graphs)
    sns.kdeplot(age_male_stroke_values)
    plt.show()
    sns.kdeplot(age_female_stroke_values)
    plt.show()
    sns.kdeplot(age_male_not_stroke_values)
    plt.show()
    sns.kdeplot(age_female_not_stroke_values)
    plt.show()



######################################################
# d) Charts show different views of the same data
# d shows a better picture of what's going on and accurately reflects the difference in standard deviation
# c doesn't appear to be that informative by comparison

# f) The histogram from point e seems to show that older people are more likely to have strokes
# The histogram from point f seems to invert the histogram, but gives the same impression that older people tend to have strokes more often. density plot f highlights the sample size better since it uses a percentage instead of a total sample size.

# h) Both charts are identical as they are both plotting by gender Male and Female, that's what I assumed by "plot by gender" point h just eliminates the "other" graph, which without any insight into what other means, the data seems erroneous. Are these identifying as other? or are they biological hermaphrodites? I believe this makes a difference in the analysis so I don't consider the other data when analyzing gender.
