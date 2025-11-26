# services = [
#     {"name": "Fan Repair", "category": "Electrical"},
#     {"name": "Light Install", "category": "Electrical"},
#     {"name": "Tap Fix", "category": "Plumbing"},
#     {"name": "Leak Repair", "category": "Plumbing"},
# ]
#
#
# grouped = {}
#
# for item in services:
#     category = item['category']
#     if category not in grouped:
#         grouped[category] = []
#     grouped[category].append(item['name'])
# print(grouped)

# fruits = ["apple", "banana", "apple", "orange", "banana", "orange"]
#
# grouped = {}
# for item in fruits:
#     if item not in grouped:
#         grouped[item] = []
#     grouped[item].append(item)
#
# print(grouped)

# numbers = [1, 2, 3, 4, 5, 6]
# grouped = {}
# for num in numbers:
#     if num % 2 == 0:
#         if "even" not in grouped:
#             grouped["even"] = []
#         grouped["even"].append(num)
#     else:
#         if "odd" not in grouped:
#             grouped["odd"] = []
#         grouped["odd"].append(num)
# print(grouped)


# names = ["arun", "akash", "balu", "babu", "chitti"]
#
# grouped = {}
# for item in names:
#     startswith = item[0]
#     if startswith not in grouped:
#         grouped[startswith] = []
#     grouped[startswith].append(item)
# print(grouped)

#
# items = [
#     {"name": "pen", "price": 10},
#     {"name": "book", "price": 150},
#     {"name": "bag", "price": 1200},
#     {"name": "mouse", "price": 500}
# ]
#
# grouped = {}
#
# for item in items:
#     price = item['price']
#     if price < 100:
#         if "low" not in grouped:
#             grouped["low"] = []
#         grouped["low"].append(item['name'])
#     elif 100 <= price <= 500:
#         if "medium" not in grouped:
#             grouped["medium"] = []
#         grouped["medium"].append(item['name'])
#     else:
#         if "high" not in grouped:
#             grouped["high"] = []
#         grouped["high"].append(item["name"])
# print(grouped)


# employees = [
#   {"name": "Ram", "dept": "IT"},
#   {"name": "Sita", "dept": "HR"},
#   {"name": "Lakshman", "dept": "IT"},
# ]
#
# grouped = {}
#
# for emp in employees:
#     dept = emp['dept']
#     name = emp['name']
#     if dept not in grouped:
#         grouped[dept] = []
#     grouped[dept].append(name)
# print(grouped)

# products = [
#     {"name": "Mobile", "category": "Electronics", "price": 10000},
#     {"name": "Laptop", "category": "Electronics", "price": 40000},
#     {"name": "Shirt", "category": "Clothing", "price": 800}
# ]
#
# grouped = {}
#
# for item in products:
#     category = item['category']
#     name = item['name']
#     price = item['price']
#     if category not in grouped:
#         grouped[category] = {}
#         grouped[category]['items'] = []
#         grouped[category]['total_price'] = 0
#
#     grouped[category]['items'].append(name)
#     grouped[category]['total_price'] += price
#
# print(grouped)

services = [
    {
        "id": 1,
        "title": "Fan Repair",
        "description": "Fix fan not working",
        "base_fee": 300,
        "estimated_duration": 60,
        "category": {"id": 101, "name": "Electrical"},
        "provider": {"name": "Arun"}
    },
    {
        "id": 2,
        "title": "Light Install",
        "description": "Install LED light",
        "base_fee": 200,
        "estimated_duration": 30,
        "category": {"id": 101, "name": "Electrical"},
        "provider": {"name": "Prakash"}
    },
    {
        "id": 3,
        "title": "Tap Fix",
        "description": "Fix leaking tap",
        "base_fee": 150,
        "estimated_duration": 45,
        "category": {"id": 202, "name": "Plumbing"},
        "provider": {"name": "Kumar"}
    },
    {
        "id": 4,
        "title": "Leak Repair",
        "description": "Repair pipe leakage",
        "base_fee": 250,
        "estimated_duration": 60,
        "category": {"id": 202, "name": "Plumbing"},
        "provider": {"name": "Ravi"}
    },
]

grouped = {}
for item in services:
    cat_id = item["category"]["id"]
    cat_name = item["category"]["name"]
    if cat_id not in grouped:
        grouped[cat_id] = {
            "cat_id": cat_id,
            "cat_name": cat_name,
            "services": []
        }
    grouped[cat_id]["services"].append(item)
print(list(grouped.values()))