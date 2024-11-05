import matplotlib.pyplot as plt
import operations

# Given dictionary
data = operations.get_server_errors()

# Extract keys and values
keys = list(data.keys())
values = list(data.values())

# Create a bar chart
plt.figure(figsize=(10, 5))
plt.bar(keys, values, color='blue')
plt.xlabel('Server Name')
plt.ylabel('Num Tickets')
plt.title('Server Errors')
plt.xticks(rotation=45)  # Rotate x labels for better visibility
plt.grid(axis='y')

# Show the plot
plt.tight_layout()
plt.show()