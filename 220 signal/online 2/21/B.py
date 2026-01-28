import numpy as np

# Stock Market Prices as a Python List
price_list = list(map(int, input("Stock Prices: ").split()))
n = int(input("Window size: "))

# price_list = [1, 2, 3, 4, 5, 6, 7, 8]
# n = 4

# Please determine uma and wma.

# Unweighted Moving Averages as a Python list
uma = []

# Weighted Moving Averages as a Python list
wma = []
m = len(price_list)
num_outputs = m-n+1
uma_weight = 1/n
for i in range(num_outputs):
    window = price_list[i:i+n]
    cur_uma = sum(window) * uma_weight
    uma.append(cur_uma)

unnormalized_weights = [i for i in range(1, n+1)]
weight_sum = sum(unnormalized_weights)
normalized_weight = [w/weight_sum for w in unnormalized_weights]

for i in range(num_outputs):
    window = price_list[i:i+n]
    cur_wma = 0
    for j in range(n):
        cur_wma += window[j]*normalized_weight[j]
    wma.append(cur_wma)

# Print the two moving averages
print("Unweighted Moving Averages: " + ", ".join(f"{num:.2f}" for num in uma))
print("Weighted Moving Averages:   " + ", ".join(f"{num:.2f}" for num in wma))