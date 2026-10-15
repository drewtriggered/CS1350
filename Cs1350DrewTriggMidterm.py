import json
from abc import ABC, abstractmethod


# ============================================================
# Problem 1: Gradebook (Dictionaries)
# ============================================================
class Gradebook:
    def __init__(self):
        # {student_name: {assignment_name: score}}
        self.grades = {}

    def add_score(self, student, assignment, score):
        if student not in self.grades:
            self.grades[student] = {}
        self.grades[student][assignment] = score  # overwrites if it already exists

    def student_average(self, student):
        scores = self.grades.get(student, {})
        if not scores:
            return None
        return sum(scores.values()) / len(scores)

    def assignment_average(self, assignment):
        scores = [s[assignment] for s in self.grades.values() if assignment in s]
        if not scores:
            return None
        return sum(scores) / len(scores)

    def top_students(self, n):
        students = [s for s in self.grades if self.student_average(s) is not None]
        students.sort(key=self.student_average, reverse=True)
        return students[:n]

    def missing(self, assignment):
        return sorted(s for s in self.grades if assignment not in self.grades[s])


print("----- Problem 1 -----")
gb = Gradebook()
gb.add_score("Alice", "hw1", 90)
gb.add_score("Alice", "hw2", 80)
gb.add_score("Bob", "hw1", 70)
gb.add_score("Bob", "hw2", 60)
gb.add_score("Carol", "hw1", 100)
gb.add_score("Bob", "hw2", 75)  # overwrite
print(gb.student_average("Alice"))  # 85.0
print(gb.student_average("Bob"))  # 72.5
print(gb.student_average("Zed"))  # None
print(gb.assignment_average("hw1"))  # 86.66666666666667
print(gb.assignment_average("hw9"))  # None
print(gb.top_students(2))  # ['Carol', 'Alice']
print(gb.missing("hw2"))  # ['Carol']


# ============================================================
# Problem 2: Access Control with Sets
# ============================================================
class Door:
    def __init__(self, name):
        self.name = name
        self.authorized = set()

    def grant(self, card_id):
        self.authorized.add(card_id)

    def revoke(self, card_id):
        self.authorized.discard(card_id)  # no error if absent

    def can_open(self, card_id):
        return card_id in self.authorized


def master_cards(doors):
    if not doors:
        return set()
    result = set(doors[0].authorized)
    for door in doors[1:]:
        result &= door.authorized
    return result


def single_door_cards(doors):
    counts = {}
    for door in doors:
        for card in door.authorized:
            counts[card] = counts.get(card, 0) + 1
    return {card for card, count in counts.items() if count == 1}


def unused_cards(all_cards, doors):
    used = set()
    for door in doors:
        used |= door.authorized
    return set(all_cards) - used


def audit(doors):
    for door in doors:
        print(f"{door.name}: {len(door.authorized)} cards")
    print(f"Master cards: {master_cards(doors)}")


print("\n----- Problem 2 -----")
lobby = Door("Lobby")
for c in [101, 102, 103, 104]:
    lobby.grant(c)
lab = Door("Lab")
for c in [101, 103, 105]:
    lab.grant(c)
server = Door("Server Room")
for c in [101, 105]:
    server.grant(c)
lab.revoke(105)
lab.revoke(999)  # no error
print(lab.can_open(103), lab.can_open(105))  # True False
doors = [lobby, lab, server]
print(master_cards(doors))  # {101}
print(single_door_cards(doors))  # {102, 104}
print(unused_cards({101, 102, 105, 200}, doors))  # {200}
audit(doors)


# ============================================================
# Problem 3: Sensor Log Processor (File Processing)
# ============================================================
def process_readings(in_file, json_file, alert_file, limit):
    """
    Summarize sensor readings into a JSON file and write alerts.
    Returns:
        number of alert lines written
    """
    values = {}  # {sensor_id: [value, value, ...]}
    alert_lines = []

    with open(in_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            timestamp, sensor_id, value_str = line.split(",")
            value = float(value_str)
            values.setdefault(sensor_id, []).append(value)
            if value > limit:
                alert_lines.append(f"{timestamp} {sensor_id} {value_str}")

    summary = {}
    for sensor_id, vals in values.items():
        summary[sensor_id] = {
            "count": len(vals),
            "average": sum(vals) / len(vals),
            "max": max(vals),
        }

    with open(json_file, "w") as f:
        json.dump(summary, f, indent=2)

    with open(alert_file, "w") as f:
        for alert in alert_lines:
            f.write(alert + "\n")

    return len(alert_lines)


print("\n----- Problem 3 -----")
with open("readings.txt", "w") as f:
    f.write("08:00,temp1,21.5\n")
    f.write("08:00,temp2,19.0\n")
    f.write("\n")
    f.write("08:10,temp1,26.0\n")
    f.write("08:10,temp2,18.5\n")
    f.write("08:20,temp1,24.5\n")

alerts = process_readings("readings.txt", "summary.json", "alerts.txt", 24.0)
print(alerts)  # 2
with open("summary.json", "r") as f:
    summary = json.load(f)
print(summary["temp1"])  # {'count': 3, 'average': 24.0, 'max': 26.0}
print(summary["temp2"])  # {'count': 2, 'average': 18.75, 'max': 19.0}
with open("alerts.txt", "r") as f:
    print(f.read())


# ============================================================
# Problem 4: Shipping Rates with Inheritance
# ============================================================
class Shipment(ABC):
    def __init__(self, tracking_id, weight_kg):
        Shipment.validate_weight(weight_kg)
        self.tracking_id = tracking_id
        self.weight_kg = weight_kg

    @abstractmethod
    def cost(self):
        pass

    def label(self):
        return f"{self.tracking_id} ({self.weight_kg} kg): ${self.cost():.2f}"

    @staticmethod
    def validate_weight(weight_kg):
        if weight_kg <= 0:
            raise ValueError("Weight must be positive")


class StandardShipment(Shipment):
    def __init__(self, tracking_id, weight_kg, rate_per_kg=2.00):
        super().__init__(tracking_id, weight_kg)
        self.rate_per_kg = rate_per_kg

    def cost(self):
        return self.weight_kg * self.rate_per_kg


class ExpressShipment(StandardShipment):
    def __init__(self, tracking_id, weight_kg, rate_per_kg=2.00, surcharge=10.00):
        super().__init__(tracking_id, weight_kg, rate_per_kg)
        self.surcharge = surcharge

    def cost(self):
        return super().cost() + self.surcharge


class InternationalShipment(Shipment):
    def __init__(self, tracking_id, weight_kg, country, customs_pct=0.15):
        super().__init__(tracking_id, weight_kg)
        self.country = country
        self.customs_pct = customs_pct

    def cost(self):
        return self.weight_kg * 5.00 * (1 + self.customs_pct)


def manifest(shipments):
    total = 0
    for shipment in shipments:
        print(shipment.label())  # polymorphism: each subclass's own cost()
        total += shipment.cost()
    print(f"Total: ${total:.2f}")
    return total


print("----- Problem 4 -----")
shipments = [
    StandardShipment("S100", 4.0),
    ExpressShipment("E200", 2.5),
    InternationalShipment("I300", 3.0, country="Canada"),
]
total = manifest(shipments)
try:
    Shipment.validate_weight(-1)
except ValueError as e:
    print("Caught:", e)


# ============================================================
# Problem 5: Polynomial Class with Operator Overloading
# ============================================================
class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = list(coeffs)  # store a copy

    def degree(self):
        for i in range(len(self.coeffs) - 1, -1, -1):
            if self.coeffs[i] != 0:
                return i
        return 0

    def __str__(self):
        terms = []
        for power in range(len(self.coeffs) - 1, -1, -1):
            c = self.coeffs[power]
            if c == 0:
                continue
            if power == 0:
                terms.append(str(c))
            else:
                coeff_str = "" if c == 1 else str(c)
                x_str = "x" if power == 1 else f"x^{power}"
                terms.append(coeff_str + x_str)
        return " + ".join(terms)

    def __repr__(self):
        return f"Polynomial({self.coeffs})"

    def __len__(self):
        return len(self.coeffs)

    def __getitem__(self, i):
        if 0 <= i < len(self.coeffs):
            return self.coeffs[i]
        return 0

    def __call__(self, x):
        return sum(c * x ** i for i, c in enumerate(self.coeffs))

    def __add__(self, other):
        length = max(len(self), len(other))
        return Polynomial([self[i] + other[i] for i in range(length)])

    def __mul__(self, scalar):
        return Polynomial([c * scalar for c in self.coeffs])

    def __eq__(self, other):
        return self.degree() == other.degree()

    def __lt__(self, other):
        return self.degree() < other.degree()


print("\n----- Problem 5 -----")
p = Polynomial([1, 2, 3])  # 1 + 2x + 3x^2
q = Polynomial([0, 1])  # x
print(p)  # 3x^2 + 2x + 1
print(q)  # x
print(repr(p))  # Polynomial([1, 2, 3])
print(len(p))  # 3
print(p[2], p[7])  # 3 0
print(p(2))  # 17
print(q(5))  # 5
r = p + q
print(r)  # 3x^2 + 3x + 1
print(p * 2)  # 6x^2 + 4x + 2
print(p == Polynomial([5, 0, 1]))  # True (both degree 2)
print(q < p)  # True (degree 1 < degree 2)
