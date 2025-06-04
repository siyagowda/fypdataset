import pandas as pd

df = pd.read_csv("/vol/bitbucket/sg2121/fypdataset/dataset_large2/analysis/normal_large_ai_aug_anal_output.csv")

# Drop the 'file' column since it's not numeric
numeric_df = df.drop(columns=['file'])

# Calculate the average for each column
averages = numeric_df.mean()

# Print the results
print("Column Averages:")
print(averages)
