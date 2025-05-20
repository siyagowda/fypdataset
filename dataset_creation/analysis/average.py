import pandas as pd

# Load your CSV file (replace 'your_file.csv' with your actual filename)
df = pd.read_csv("/vol/bitbucket/sg2121/fypdataset/dataset_large/analysis/normal_large_human_anal_output.csv")

# Drop the 'file' column since it's not numeric
numeric_df = df.drop(columns=['file'])

# Calculate the average (mean) for each column
averages = numeric_df.mean()

# Print the results
print("Column Averages:")
print(averages)
