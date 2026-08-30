my_info = {
    "name": "Drew",
    "age": 20,  
    "major": "Cybersecurity, Organizational Leadership"
}

print(my_info)

menu = {
    "burger": 8.99,
    "pizza": 12.99,
    "fries": 3.99,
    "salad": 6.99
}

print(menu)
course_credits = {
    "CS1350": 3,
    "MATH201": 3,
    "NET3000": 3,
    "ENG101": 3
}

print(course_credits)
weekly_temps = dict(
    Monday=72,
    Tuesday=75,
    Wednesday=70,
    Thursday=68,
    Friday=74,
    Saturday=78,
    Sunday=76
)

print(weekly_temps)

pet = {"name": "Buddy", "type": "dog", "age": 3}

print(pet["name"])
print(pet["age"])
pet = {"name": "Buddy", "type": "dog", "age": 3}

color = pet.get("color", "unknown")
print(color)
grades = {
    "Alice": 85,
    "Bob": 72,
    "Carol": 58
}

student = "Bob"
grade = grades.get(student, 0)

if grade >= 60:
    print(f"{student} passed with a grade of {grade}.")
else:
    print(f"{student} did not pass. Grade: {grade}.")
    products = {
    "laptop": 999.99,
    "mouse": 29.99,
    "keyboard": 79.99
}

product_name = "laptop"

price = products.get(product_name)

if price is not None:
    print(f"{product_name} costs ${price:.2f}")
else:
    print("Product not available")

# Test with a product that does not exist
product_name = "monitor"

price = products.get(product_name)

if price is not None:
    print(f"{product_name} costs ${price:.2f}")
else:
    print("Product not available")
    
inventory = {}

inventory["apples"] = 10
inventory["bananas"] = 15
inventory["oranges"] = 8

print(inventory)

scores = {
    "Team A": 45,
    "Team B": 38
}

scores["Team B"] = 52
scores["Team C"] = 41

print(scores)
removed_score = scores.pop("Team A")

print(f"Team A had {removed_score} points.")
print(scores)
# 1. Start with an empty cart
cart = {}

# 2. Add 3 items with prices
cart["laptop"] = 999.99
cart["mouse"] = 29.99
cart["keyboard"] = 79.99

print("Initial cart:")
print(cart)

# 3. Update the price of one item
cart["mouse"] = 24.99

print("\nAfter updating mouse price:")
print(cart)

# 4. Remove one item and print what was removed
removed_item = cart.pop("keyboard")

print("\nRemoved item:")
print(f"Keyboard: ${removed_item:.2f}")

# 5. Print the final cart
print("\nFinal cart:")
print(cart)

# Bonus: Calculate total price
total = sum(cart.values())

print(f"\nTotal price: ${total:.2f}")


print("a) 'student_name' - valid")
print("b) [1, 2, 3] - invalid")
print("c) 100 - valid")
print("d) ('x', 'y') - valid")
print("e) {'a': 1} - invalid")
print("f) frozenset({1, 2}) - valid")



locations = {
    (40.7, -74.0): "New York",
    (34.0, -118.2): "Los Angeles"
}

print("\nLocations:", locations)


data = {
    "a": 1,
    "b": 2,
    "a": 3,
    "b": 4
}

print("\nData:", data)
print("Length:", len(data))


# Intermediate 3 - Hash values
name = "Drew"

print("\nHash value of my name:", hash(name))
print("Hash value of 100:", hash(100))


# Advanced 1 - Game high scores
high_scores = {
    ("Drew", "Minecraft"): 9500,
    ("Alex", "Minecraft"): 8750,
    ("Jordan", "Fortnite"): 10200
}

score = high_scores[("Drew", "Minecraft")]

print("\nDrew's Minecraft score:", score)



import time

big_list = list(range(100000))
big_dict = {i: i for i in range(100000)}

target = 99999

start = time.time()
result = target in big_list
list_time = time.time() - start


start = time.time()
result = target in big_dict
dict_time = time.time() - start

print("\nList search:", list_time)
print("Dictionary search:", dict_time)

if dict_time > 0:
    print("Dictionary is approximately",
          list_time / dict_time,
          "x faster.")



temps = {
    "Monday": 72,
    "Tuesday": 75,
    "Wednesday": 68
}


print("\nDays:")

for day in temps.keys():
    print(day)


print("\nTemperatures:")

for temperature in temps.values():
    print(temperature)


print("\nNumber of days:", len(temps))




highest = max(temps.values())
lowest = min(temps.values())

print("\nHighest temperature:", highest)
print("Lowest temperature:", lowest)




if "Friday" in temps:
    print("Friday is in the dictionary.")
else:
    print("Friday is not in the dictionary.")


temps.setdefault("Thursday", 70)

print("\nAfter setdefault:", temps)




keys_view = temps.keys()

print("\nKeys before adding Friday:")
print(keys_view)

temps["Friday"] = 74

print("Keys after adding Friday:")
print(keys_view)




prices = {
    "laptop": 999,
    "phone": 699,
    "tablet": 449,
    "watch": 299
}



total = sum(prices.values())
average = total / len(prices)

print("\nTotal value:", total)
print("Average price:", average)



most_expensive = max(prices.items(), key=lambda x: x[1])
least_expensive = min(prices.items(), key=lambda x: x[1])

print(
    "Most expensive:",
    most_expensive[0],
    "$" + str(most_expensive[1])
)

print(
    "Least expensive:",
    least_expensive[0],
    "$" + str(least_expensive[1])
)


# 3. Compare memory usage

import sys

keys_view = prices.keys()
keys_list = list(prices.keys())

print(
    "Memory used by keys view:",
    sys.getsizeof(keys_view),
    "bytes"
)

print(
    "Memory used by keys list:",
    sys.getsizeof(keys_list),
    "bytes"
)


# 4. Use update() to add 3 products

prices.update({
    "headphones": 149,
    "monitor": 249,
    "keyboard": 89
})

print("\nAll products:")

for product, price in prices.items():
    print(f"{product}: ${price}")



colors = {
    "apple": "red",
    "banana": "yellow",
    "grape": "purple"
}

for fruit, color in colors.items():
    print(f"The {fruit} is {color}")


print("\nList of color items:")
print(list(colors.items()))


prices = {
    "coffee": 4.50,
    "tea": 3.00,
    "juice": 5.25
}


print("\nPrices with tax:")

for item, price in prices.items():
    tax = price * 0.10
    total = price + tax

    print(
        f"{item}: ${price:.2f} + tax = ${total:.2f}"
    )


count = 0

for item, price in prices.items():
    if price > 4.00:
        count += 1

print("\nItems over $4.00:", count)



x = 10
y = 20

x, y = y, x

print("\nAfter swap:")
print("x =", x)
print("y =", y)



numbers = [1, 2, 3, 4, 5]

first, *middle, last = numbers

print("\nFirst:", first)
print("Middle:", middle)
print("Last:", last)


scores = {
    "Alice": 88,
    "Bob": 65,
    "Carol": 92,
    "Dave": 71,
    "Eve": 58
}

best_student, best_score = max(
    scores.items(),
    key=lambda x: x[1]
)

print(
    "\nHighest score:",
    best_student,
    "with",
    best_score
)


passed = {}
failed = {}

for name, grade in scores.items():

    if grade >= 70:
        passed[name] = grade
    else:
        failed[name] = grade

print("\nPassed:", passed)
print("Failed:", failed)


total = sum(scores.values())
average = total / len(scores)

deviations = {}

for name, grade in scores.items():
    deviations[name] = grade - average

print("\nClass average:", average)

print("Deviations from average:")

for name, deviation in deviations.items():
    print(f"{name}: {deviation:.2f}")



big_dict = {
    i: i * 2
    for i in range(50000)
}

start = time.time()

for key, value in big_dict.items():
    result = key + value

items_time = time.time() - start

start = time.time()

for key in big_dict.keys():
    value = big_dict[key]
    result = key + value

keys_time = time.time() - start


print("\nPerformance Test:")
print(f"items() time: {items_time:.6f} seconds")
print(f"keys() + lookup time: {keys_time:.6f} seconds")

if items_time > 0:
    print(
        f"items() is approximately "
        f"{keys_time / items_time:.2f}x faster."
    )