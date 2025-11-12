def calculate_item_total(price, quantity):
    return price * quantity

def calculate_grand_total(total1, total2):
    return total1 + total2

print("\n--- Enter Details for Item 1 ---")
item1_name = input("Enter item name: ")
item1_price = float(input("Enter item price ($): "))
item1_quantity = int(input("Enter item quantity: "))
item1_total = calculate_item_total(item1_price, item1_quantity)

print("\n--- Enter Details for Item 2 ---")
item2_name = input("Enter item name: ")
item2_price = float(input("Enter item price ($): "))
item2_quantity = int(input("Enter item quantity: "))
item2_total = calculate_item_total(item2_price, item2_quantity)

grand_total = calculate_grand_total(item1_total, item2_total)

print("\n")

print(f"Item: {item1_name}")
print(f"Price: ${item1_price:.2f}")
print(f"Quantity: {item1_quantity}")
print(f"Total price: ${item1_total:.2f}")

print("-------------------")

print(f"Item: {item2_name}")
print(f"Price: ${item2_price:.2f}")
print(f"Quantity: {item2_quantity}")
print(f"Total price: ${item2_total:.2f}")

print("########################")
print(f"Total cart price: ${grand_total:.2f}")
print("########################")
