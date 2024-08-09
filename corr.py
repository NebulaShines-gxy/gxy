import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file into a Pandas DataFrame
csv_path = "std_result.csv"  # Replace with the path to your CSV file
data = pd.read_csv(csv_path)

# Calculate pairwise correlation matrix
correlation_matrix = data.corr()

# Plot a heatmap of the correlation matrix using Seaborn
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="RdYlGn", fmt=".2f", linewidths=0.5)
plt.title("Pairwise Correlation Heatmap")
plt.show()
