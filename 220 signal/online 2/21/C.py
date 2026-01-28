# Input for first polynomial
d1 = int(input("Degree of the first polynomial: "))
poly1 = list(map(int, input("Coefficients: ").split()))


# Input for second polynomial
d2 = int(input("Degree of the second polynomial: "))
poly2 = list(map(int, input("Coefficients: ").split()))

degree_result = d1 + d2
res_coeffs = [0] * (degree_result+1)

# Multiply the polynomials using Discrete-Time Convolution
for i in range(len(poly1)):
    for j in range(len(poly2)):
        res_coeffs[i+j] += poly1[i]*poly2[j]

# Print the result
print(f"degree of the polynomials: {degree_result}")
print("coefficients: " + " ".join(map(str, res_coeffs)))