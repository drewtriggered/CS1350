# Contact records: name -> dictionary of details
contact_book = {
    "Mom": {"phone": "555-1234", "category": "Family", "city": "Fort Wayne"},
    "Dad": {"phone": "555-4321", "category": "Family", "city": "Fort Wayne"},
    "Sister": {"phone": "555-7777", "category": "Family", "city": "Chicago"},
    "Best Friend": {"phone": "555-8888", "category": "Friend", "city": "Indianapolis"},
    "Roommate": {"phone": "555-3141", "category": "Friend", "city": "Fort Wayne"},
    "Boss": {"phone": "555-0000", "category": "Work", "city": "Chicago"},
    "Professor": {"phone": "555-2718", "category": "Work", "city": "Fort Wayne"},
    "Dentist": {"phone": "555-2222", "category": "Business", "city": "Indianapolis"},
}

# Call log: name -> {month -> minutes talked that month}
# Note: not every contact was called every month.
call_log = {
    "Mom": {"Jan": 120, "Feb": 95, "Mar": 140},
    "Dad": {"Jan": 45, "Feb": 60, "Mar": 30},
    "Sister": {"Jan": 80, "Mar": 70},
    "Best Friend": {"Jan": 200, "Feb": 180, "Mar": 220},
    "Roommate": {"Feb": 15, "Mar": 25},
    "Boss": {"Jan": 60, "Feb": 90, "Mar": 75},
    "Professor": {"Feb": 20, "Mar": 35},
    "Dentist": {"Jan": 10},
}

# Tiers listed high to low so the distribution always prints in a fixed order.
TIER_ORDER = ["Platinum", "Gold", "Silver", "Bronze", "Inactive"]

# Column widths for the Phase 6 table. Two spaces sit between Minutes and Tier.
NAME_WIDTH = 13
CATEGORY_WIDTH = 10
CITY_WIDTH = 14
MINUTES_WIDTH = 8
TIER_WIDTH = 8
GAP = 2
TABLE_WIDTH = NAME_WIDTH + CATEGORY_WIDTH + CITY_WIDTH + MINUTES_WIDTH + GAP + TIER_WIDTH


def banner(title):
    """Print the heading that opens a phase."""
    print(f"=== {title} ===")


def subheading(title):
    """Print a blank line and a sub-heading inside a phase."""
    print()
    print(f"--- {title} ---")


def accumulate(totals, key, value):
    """Add value to totals[key], starting the key at 0 the first time it appears.

    This is the get() accumulation pattern written once instead of three times:
    totals[key] = totals.get(key, 0) + value
    """
    totals[key] = totals.get(key, 0) + value


def get_tier(minutes):
    """Return the loyalty tier that a contact's total minutes fall into.

    Platinum 400+, Gold 200-399, Silver 100-199, Bronze 50-99, Inactive below 50.
    """
    if minutes >= 400:
        return "Platinum"
    elif minutes >= 200:
        return "Gold"
    elif minutes >= 100:
        return "Silver"
    elif minutes >= 50:
        return "Bronze"
    else:
        return "Inactive"


def format_row(name, category, city, minutes, tier):
    """Build one line of the Phase 6 table.

    f-string field widths do the aligning, and the same function formats the
    header and the data rows so the two can never drift apart.
    """
    return (f"{name:<{NAME_WIDTH}}{category:<{CATEGORY_WIDTH}}"
            f"{city:<{CITY_WIDTH}}{minutes:>{MINUTES_WIDTH}}"
            f"{'':{GAP}}{tier}")


def phase1_quick_contacts():
    """Walk through dictionary CRUD on a small name -> phone dictionary."""
    banner("Phase 1: Quick Contacts")

    # 1. Start empty, then add five entries one key at a time.
    quick_contacts = {}
    quick_contacts["Mom"] = "555-1234"
    quick_contacts["Dad"] = "555-5678"
    quick_contacts["Best Friend"] = "555-8888"
    quick_contacts["Pizza Place"] = "555-9999"
    quick_contacts["Work"] = "555-0000"
    print(quick_contacts)

    subheading("Access and Modify")

    # 2. Bracket notation reads a key we know is there.
    print("Mom's number:", quick_contacts["Mom"])

    # 3. Assigning to an existing key overwrites the old value.
    quick_contacts["Dad"] = "555-4321"

    # 4. Assigning to a brand new key adds it.
    quick_contacts["Dentist"] = "555-2222"

    # 5. get() hands back a default instead of raising KeyError, so no crash.
    print("Looking up Grandma:", quick_contacts.get("Grandma", "Contact not found"))

    # 6. The dictionary after the update and the addition.
    print("Updated contacts:", quick_contacts)

    subheading("Delete and Analyze")

    # 7. del removes a key and throws the value away.
    del quick_contacts["Pizza Place"]

    # 8. pop() removes a key and hands the value back so we can keep it.
    old_work = quick_contacts.pop("Work")
    print("Removed work number:", old_work)

    # 9. len(), keys(), and values() summarize whatever is left.
    print("Contacts remaining:", len(quick_contacts))
    print("Contact names:", list(quick_contacts.keys()))
    print("Phone numbers:", list(quick_contacts.values()))

def phase2_contact_activity(call_log):
    """Print per-contact call stats and return name -> total minutes.

    Every later phase depends on the returned total_minutes dictionary.
    """
    banner("Phase 2: Contact Activity")

    total_minutes = {}

    for name, months in call_log.items():
        # The value of each entry is itself a dictionary, so we loop again inside it.
        month_count = len(months)
        minutes_total = 0
        busiest_month = ""
        busiest_minutes = 0  # running maximum: start at 0, replace on anything larger

        for month, minutes in months.items():
            minutes_total = minutes_total + minutes
            if minutes > busiest_minutes:
                busiest_minutes = minutes
                busiest_month = month

        average = minutes_total / month_count
        total_minutes[name] = minutes_total

        print(f"{name}: {month_count} month(s), {minutes_total} min total, "
              f"avg: {average:.2f}, busiest: {busiest_month} ({busiest_minutes})")

    return total_minutes



def build_month_stats(call_log):
    """Flip the call log from contact -> month over to month -> summary.

    Each month maps to its list of minutes plus the total, average, and how
    many contacts were called that month.
    """
    month_stats = {}

    for name, months in call_log.items():
        for month, minutes in months.items():
            # The first time a month shows up, create its record.
            if month not in month_stats:
                month_stats[month] = {"minutes": [], "total": 0, "avg": 0, "contacts": 0}
            month_stats[month]["minutes"].append(minutes)

    # Once every month holds its full list, fill in the summary fields.
    for month, stats in month_stats.items():
        stats["total"] = sum(stats["minutes"])
        stats["contacts"] = len(stats["minutes"])
        stats["avg"] = round(stats["total"] / stats["contacts"], 2)

    return month_stats


def build_rollups(contact_book, total_minutes):
    """Total minutes by category and by city, plus a headcount per city.

    Every rollup is driven by contact_book, so each contact is counted once.
    """
    minutes_by_category = {}
    minutes_by_city = {}
    contacts_per_city = {}

    for name, details in contact_book.items():
        # A contact with no calls still counts as a person living in that city.
        minutes = total_minutes.get(name, 0)

        accumulate(minutes_by_category, details["category"], minutes)
        accumulate(minutes_by_city, details["city"], minutes)
        accumulate(contacts_per_city, details["city"], 1)

    return minutes_by_category, minutes_by_city, contacts_per_city


def phase3_aggregations(call_log, contact_book, total_minutes):
    """Print the monthly summary and the category/city rollups."""
    banner("Phase 3: Aggregations")

    # Part A - months, sorted by average with a lambda key.
    month_stats = build_month_stats(call_log)

    print("Monthly summary (sorted by average, highest first):")
    for month, stats in sorted(month_stats.items(),
                               key=lambda item: item[1]["avg"], reverse=True):
        print(f"{month}: {stats['total']} min total, {stats['avg']:.2f} avg "
              f"({stats['contacts']} contacts)")

    # Part B - rollups built with the get() accumulation pattern.
    minutes_by_category, minutes_by_city, contacts_per_city = build_rollups(
        contact_book, total_minutes)

    print()
    print("Minutes by category:", minutes_by_category)
    print("Minutes by city:", minutes_by_city)
    print("Contacts per city:", contacts_per_city)


def phase4_comprehensions(contact_book, total_minutes):
    """Rebuild three views of the data, each as a one-line comprehension."""
    banner("Phase 4: Comprehensions")

    # 1. Every contact mapped to just their phone number.
    phone_book = {name: details["phone"] for name, details in contact_book.items()}

    # 2. Same idea, filtered down to one city.
    local_contacts = {name: details["phone"] for name, details in contact_book.items() if details["city"] == "Fort Wayne"}

    # 3. Labels built from the totals computed back in Phase 2.
    activity_level = {name: ("Frequent" if minutes >= 200 else "Occasional") for name, minutes in total_minutes.items()}

    print("Phone book:", phone_book)
    print("Local contacts (Fort Wayne):", local_contacts)
    print("Activity level:", activity_level)


def count_tiers(total_minutes):
    """Count how many contacts land in each tier.

    Starting every tier at 0 means a tier with no contacts still prints a 0
    instead of disappearing from the report.
    """
    tier_counts = {}
    for tier in TIER_ORDER:
        tier_counts[tier] = 0

    for name, minutes in total_minutes.items():
        tier = get_tier(minutes)
        # An if/elif chain, one branch per tier, as the assignment asks for.
        if tier == "Platinum":
            tier_counts["Platinum"] = tier_counts["Platinum"] + 1
        elif tier == "Gold":
            tier_counts["Gold"] = tier_counts["Gold"] + 1
        elif tier == "Silver":
            tier_counts["Silver"] = tier_counts["Silver"] + 1
        elif tier == "Bronze":
            tier_counts["Bronze"] = tier_counts["Bronze"] + 1
        else:
            tier_counts["Inactive"] = tier_counts["Inactive"] + 1

    return tier_counts


def find_extremes(total_minutes):
    """Return (top_name, top_minutes, bottom_name, bottom_minutes).

    Both use the running-comparison pattern. The minimum has to start above
    any real value, otherwise nothing would ever beat it.
    """
    top_name = ""
    top_minutes = 0
    bottom_name = ""
    bottom_minutes = 999999

    for name, minutes in total_minutes.items():
        if minutes > top_minutes:
            top_minutes = minutes
            top_name = name
        if minutes < bottom_minutes:
            bottom_minutes = minutes
            bottom_name = name

    return top_name, top_minutes, bottom_name, bottom_minutes


def phase5_tier_report(total_minutes):
    """Print tiers, the tier distribution, and the rankings.

    Returns the grand total and the average per contact, both of which the
    Phase 6 summary line reuses.
    """
    banner("Phase 5: Tier Report")

    # Part A - label every contact.
    for name, minutes in total_minutes.items():
        print(f"{name}: {minutes} min ({get_tier(minutes)})")

    # Part B - how many contacts sit in each tier.
    subheading("Tier Distribution")
    tier_counts = count_tiers(total_minutes)
    for tier in TIER_ORDER:
        print(f"{tier}: {tier_counts[tier]}")

    # Part C - rankings.
    subheading("Top and Bottom")
    top_name, top_minutes, bottom_name, bottom_minutes = find_extremes(total_minutes)
    print(f"Most contacted: {top_name} ({top_minutes} min)")
    print(f"Least contacted: {bottom_name} ({bottom_minutes} min)")

    grand_total = sum(total_minutes.values())
    average_per_contact = grand_total / len(total_minutes)
    print("Total minutes:", grand_total)
    print(f"Average per contact: {average_per_contact:.2f}")

    subheading("Above Average Contacts")
    for name, minutes in total_minutes.items():
        if minutes > average_per_contact:
            print(f"{name}: {minutes}")

    return grand_total, average_per_contact



def phase6_contact_hub(contact_book, total_minutes, grand_total, average_per_contact):
    """Print one aligned table of every contact, busiest first."""
    banner("Phase 6: Contact Hub Report")

    print(format_row("Name", "Category", "City", "Minutes", "Tier"))
    print("-" * TABLE_WIDTH)

    # sorted() with a lambda on the value ranks the contacts by minutes.
    for name, minutes in sorted(total_minutes.items(),
                                key=lambda item: item[1], reverse=True):
        details = contact_book[name]
        print(format_row(name, details["category"], details["city"],
                         minutes, get_tier(minutes)))

    print("-" * TABLE_WIDTH)
    print(f"{len(total_minutes)} contacts | {grand_total} total minutes | "
          f"{average_per_contact:.2f} average")



def main():
    """Run the six phases, handing each phase's results to the next one."""
    phase1_quick_contacts()

    print()
    total_minutes = phase2_contact_activity(call_log)

    print()
    phase3_aggregations(call_log, contact_book, total_minutes)

    print()
    phase4_comprehensions(contact_book, total_minutes)

    print()
    grand_total, average_per_contact = phase5_tier_report(total_minutes)

    print()
    phase6_contact_hub(contact_book, total_minutes, grand_total, average_per_contact)


main()
