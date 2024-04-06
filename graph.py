import matplotlib.pyplot as plt

# Data goes here
transactions_per_block = [10, 100, 1000, 10000]  # Number of transactions per block
time_in_seconds = [0.00015, 0.00036, 0.00369, 0.02298]  # Corresponding time in seconds

# Creating the bar chart
bars = plt.bar(range(len(transactions_per_block)), time_in_seconds, color='skyblue')

# Adding time labels on bars
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{time_in_seconds[i]:.5f}", ha='center', va='bottom')

# Adding labels and title
plt.xlabel('Number of Transactions per Block')
plt.ylabel('Time in Seconds')
plt.title('Comparison of Average Time based on Transactions per Block')

# Setting x-axis labels
plt.xticks(range(len(transactions_per_block)), transactions_per_block)

# Displaying the plot without gaps between bars
plt.tight_layout()
plt.show()
