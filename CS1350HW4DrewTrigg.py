"""
CS1350 - Week 2 Practice Exercise Solutions (refactored)
Lecture 3: Dictionary Iteration, Patterns & Performance
Lecture 4: Sets in Python

Run:  python week2_practice_solutions_refactored.py
"""

import time


def banner(title, char="=", width=60):
    print(f"\n{char * width}\n{title}\n{char * width}")


def level(name):
    print(f"\n--- {name} ---")


def to_letter(score):
    """Convert a numeric score to a letter grade."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"


def total_by(records, key_index, value_index=-1):
    """Sum values grouped by the field at key_index."""
    totals = {}
    for rec in records:
        key = rec[key_index]
        totals[key] = totals.get(key, 0) + rec[value_index]
    return totals


def find_duplicates(lst):
    """Return a set of elements that appear more than once."""
    seen, dupes = set(), set()
    for item in lst:
        (dupes if item in seen else seen).add(item)
    return dupes


def common_chars(s1, s2):
    """Return the set of characters shared by two strings."""
    return set(s1) & set(s2)


def unique_ordered(items):
    """Remove duplicates while preserving first-seen order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def time_lookup(container, target):
    """Time a single membership check in seconds."""
    start = time.perf_counter()
    target in container
    return time.perf_counter() - start



def unit_3_1():
    banner("UNIT 3.1 PRACTICE EXERCISES")

    level("Beginner")
    inventory = {"apples": 50, "bananas": 30, "oranges": 25}
    print("1. Product names:")
    for product in inventory:
        print(" ", product)
    print(f"2. Total items: {sum(inventory.values())}")
    print("3. Product quantities:")
    for product, qty in inventory.items():
        print(f"   {product}: {qty}")

    level("Intermediate")
    prices = {"laptop": 999, "phone": 699, "tablet": 449, "watch": 299}
    print("1. Sorted alphabetically:")
    for product in sorted(prices):
        print(f"   {product}: {prices[product]}")
    print("2. Sorted by price (cheapest first):")
    for product in sorted(prices, key=prices.get):
        print(f"   {product}: {prices[product]}")
    name, price = max(prices.items(), key=lambda kv: kv[1])
    print(f"3. Most expensive item: {name} (${price})")

    level("Advanced")
    temps = {"Mon": 72, "Tue": 68, "Wed": 75, "Thu": 80, "Fri": 65}
    avg = sum(temps.values()) / len(temps)
    print(f"1. Average temperature: {avg:.1f}")

    hot_day = cold_day = None
    hot, cold = float("-inf"), float("inf")
    for day, temp in temps.items():  # single loop
        if temp > hot:
            hot, hot_day = temp, day
        if temp < cold:
            cold, cold_day = temp, day
    print(f"2. Hottest: {hot_day} ({hot}), Coldest: {cold_day} ({cold})")
    print(f"3. Days above average: {sum(t > avg for t in temps.values())}")


def unit_3_2():
    banner("UNIT 3.2 PRACTICE EXERCISES")

    level("Beginner")
    products = {
        "laptop": {"price": 999, "stock": 15},
        "phone": {"price": 699, "stock": 50},
    }
    print(f"1. Laptop price: {products['laptop']['price']}")
    print("2. Stock levels:")
    for name, info in products.items():
        print(f"   {name}: {info['stock']} in stock")

    level("Intermediate")
    countries = ["USA", "Canada", "Mexico"]
    capitals = ["Washington", "Ottawa", "Mexico City"]
    print(f"1. Country -> Capital: {dict(zip(countries, capitals))}")

    products["tablet"] = {"price": 449, "stock": 30}
    print(f"2. Products after adding tablet: {products}")

    for name, info in list(products.items()):  # list() = safe deletion
        if info["stock"] < 20:
            del products[name]
    print(f"3. Products after removing stock < 20: {products}")

    level("Advanced")
    company = {
        "Engineering": {"Alice": 95000, "Bob": 85000},
        "Marketing": {"Carol": 75000, "Dave": 70000},
    }
    print("1. All employees:")
    for dept, staff in company.items():
        for name, salary in staff.items():
            print(f"   {dept} - {name}: ${salary}")

    print("2. Average salary per department:")
    for dept, staff in company.items():
        print(f"   {dept}: ${sum(staff.values()) / len(staff):,.2f}")

    top_salary, top_name, top_dept = max(
        (salary, name, dept)
        for dept, staff in company.items()
        for name, salary in staff.items()
    )
    print(f"3. Highest paid: {top_name} ({top_dept}) - ${top_salary}")


def unit_3_3():
    banner("UNIT 3.3 PRACTICE EXERCISES")

    level("Beginner")
    print(f"1. Cubes: { {x: x**3 for x in range(1, 6)} }")
    temps_f = {"Mon": 72, "Tue": 68, "Wed": 75}
    temps_c = {d: round((f - 32) * 5 / 9, 1) for d, f in temps_f.items()}
    print(f"2. Celsius temps: {temps_c}")

    level("Intermediate")
    scores = {"Alice": 88, "Bob": 65, "Carol": 92, "Dave": 71, "Eve": 58}
    print(f"1. Passing: { {n: s for n, s in scores.items() if s >= 70} }")
    print(f"2. Letter grades: { {n: to_letter(s) for n, s in scores.items()} }")
    student_ids = {"Alice": 101, "Bob": 102}
    print(f"3. Inverted student_ids: { {v: k for k, v in student_ids.items()} }")

    level("Advanced")
    sales = [
        ("North", "Alice", 5000), ("South", "Bob", 4500),
        ("North", "Carol", 6000), ("South", "Alice", 3500),
    ]
    print(f"1. Sales by region: {total_by(sales, 0)}")
    print(f"2. Sales by salesperson: {total_by(sales, 1)}")

    nested = {}
    for region, person, amount in sales:
        people = nested.setdefault(region, {})
        people[person] = people.get(person, 0) + amount
    print(f"3. Nested sales by region/person: {nested}")


def set_unit_1():
    banner("UNIT 1 PRACTICE EXERCISES")

    level("Beginner")
    print(f"1. Vowels: { {'a', 'e', 'i', 'o', 'u'} }")
    nums = set([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
    print(f"2. Set: {nums}, has {len(nums)} elements")
    print("3. `empty = {}` creates an empty DICTIONARY, not a set.")
    print("   Use `empty = set()` for an empty set.")

    level("Intermediate")
    chars = set("mississippi")
    print(f"1. Unique characters: {chars} -> {len(chars)} unique letters")
    emails = ["a@b.com", "c@d.com", "a@b.com", "e@f.com", "c@d.com"]
    print(f"2. Unique emails: {list(set(emails))}")
    print("3. TypeError: unhashable type: 'list'. Lists are mutable, so they")
    print("   can't be hashed. Use tuples instead: {(1, 2), (3, 4)}.")

    level("Advanced")
    big_set = set(range(1_000_000))
    big_list = list(range(1_000_000))
    print(f"1. Set lookup:  {time_lookup(big_set, 999_999):.8f}s")
    print(f"   List lookup: {time_lookup(big_list, 999_999):.8f}s")
    print("   Set is O(1) (hash table); list is O(n) (linear scan).")

    print(f"2. Frozenset as dict key: { {frozenset([1, 2, 3]): 'my frozen key'} }")

    edges = [(1, 2), (2, 3), (1, 3), (3, 4)]
    nodes = {n for edge in edges for n in edge}
    print(f"3. Unique nodes: {nodes}")


def set_unit_2():
    banner("UNIT 2 PRACTICE EXERCISES")

    level("Beginner")
    a, b = {1, 2, 3, 4}, {3, 4, 5, 6}
    print(f"1. Union: {a | b}")
    print(f"2. Intersection: {a & b}")
    print(f"3. Difference (a - b): {a - b}")

    level("Intermediate")
    morning = {"Alice", "Bob", "Carol"}
    evening = {"Carol", "Dave", "Eve"}
    weekend = {"Alice", "Eve", "Frank"}
    print(f"1. All shifts: {morning & evening & weekend}")
    print(f"2. At least one shift: {morning | evening | weekend}")
    print(f"3. Morning only: {morning - evening - weekend}")
    exactly_one = (
        (morning - evening - weekend)
        | (evening - morning - weekend)
        | (weekend - morning - evening)
    )
    print(f"4. Exactly one shift: {exactly_one}")

    level("Advanced")
    prereqs = {"Alice", "Bob", "Carol", "Dave"}
    space = {"Bob", "Carol", "Eve", "Frank"}
    paid = {"Alice", "Carol", "Eve"}
    eligible = prereqs & space & paid
    print(f"1. Eligible to enroll: {eligible}")
    print(f"2. Met prereqs, haven't paid: {prereqs - paid}")
    print(f"3. Missing at least one requirement: {(prereqs | space | paid) - eligible}")


def set_unit_3():
    banner("UNIT 3 PRACTICE EXERCISES")

    level("Beginner")
    s = {1, 2, 3}
    s.add(4)
    s.remove(1)
    print(f"1. Final set: {s}")
    print(f"2. Evens 0-20: { {x for x in range(21) if x % 2 == 0} }")

    demo = {1, 2, 3}
    demo.discard(99)  # silent
    print(f"3. discard(99): no error -> {demo}")
    try:
        demo.remove(99)
    except KeyError as e:
        print(f"   remove(99): KeyError({e})")

    level("Intermediate")
    print(f"1. Deduplicated (ordered): {unique_ordered([4, 5, 2, 4, 8, 5, 2, 1, 9, 4])}")
    sentence = "To be or not to be that is the question"
    print(f"2. Unique words: { {w.lower() for w in sentence.split()} }")
    expected = set(range(1, 11))
    actual = {1, 2, 4, 5, 7, 8, 10}
    print(f"3. Missing numbers: {expected - actual}")

    level("Advanced")
    print(f"1. find_duplicates: {find_duplicates([1, 2, 2, 3, 3, 3, 4])}")
    alice = {"Python", "SQL", "Excel", "Tableau"}
    bob = {"Python", "Java", "SQL", "AWS"}
    carol = {"Python", "R", "SQL", "Tableau"}
    print(f"2a. All three have: {alice & bob & carol}")
    print(f"2b. Only Alice has: {alice - bob - carol}")
    print(f"2c. All unique skills: {alice | bob | carol}")
    print(f"3. common_chars('hello', 'world'): {common_chars('hello', 'world')}")


def main():
    banner("WEEK 2 LECTURE 1: DICTIONARY III", char="#")
    unit_3_1()
    unit_3_2()
    unit_3_3()

    banner("WEEK 2 LECTURE 2: SETS", char="#")
    set_unit_1()
    set_unit_2()
    set_unit_3()


if __name__ == "__main__":
    main()