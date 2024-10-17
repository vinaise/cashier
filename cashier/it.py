import os

# Меню, где ключи будут уникальными для каждого элемента
menu = {
    'sandwich1': {'name': 'Turkey Sandwich', 'price': 5.99, 'description': 'A delicious turkey sandwich', 'key': 'sandwich1'},
    'sandwich2': {'name': 'Ham Sandwich', 'price': 6.49, 'description': 'A tasty ham sandwich', 'key': 'sandwich2'},
    'sandwich3': {'name': 'Veggie Sandwich', 'price': 5.49, 'description': 'A fresh veggie sandwich', 'key': 'sandwich3'},
    'sandwich4': {'name': 'Chicken Sandwich', 'price': 6.99, 'description': 'Grilled chicken sandwich', 'key': 'sandwich4'},
    'drink1': {'name': 'Coca-Cola', 'price': 1.99, 'description': 'Cold can of Coca-Cola', 'key': 'drink1'},
    'drink2': {'name': 'Pepsi', 'price': 1.99, 'description': 'Cold can of Pepsi', 'key': 'drink2'},
    'drink3': {'name': 'Water', 'price': 0.99, 'description': 'Bottled water', 'key': 'drink3'},
    'drink4': {'name': 'Orange Juice', 'price': 2.49, 'description': 'Fresh orange juice', 'key': 'drink4'},
    'dessert1': {'name': 'Chocolate Chip Cookie', 'price': 0.99, 'description': 'Fresh baked cookie', 'key': 'dessert1'},
    'dessert2': {'name': 'Brownie', 'price': 1.49, 'description': 'Delicious chocolate brownie', 'key': 'dessert2'},
    'dessert3': {'name': 'Apple Pie', 'price': 1.99, 'description': 'Classic apple pie', 'key': 'dessert3'},
    'dessert4': {'name': 'Ice Cream', 'price': 2.99, 'description': 'Vanilla ice cream scoop', 'key': 'dessert4'},
}

# Функция для отображения меню
def display_menu():
    print("\nMenu:")
    for item in menu.values():
        print(f"{item['key']}: {item['name']} - ${item['price']:.2f} ({item['description']})")

# Функция для создания нового заказа
def create_order():
    order = []
    while True:
        display_menu()
        choice = input("Enter item key to add to your order (or 'done' to finish): ").lower()
        if choice == 'done':
            break
        elif choice in menu:
            try:
                quantity = int(input(f"Enter quantity for {menu[choice]['name']}: "))
                if quantity > 0:
                    order.append({'item': menu[choice], 'quantity': quantity})
                    print(f"Added {quantity} x {menu[choice]['name']} to your order.")
                else:
                    print("Quantity must be a positive integer.")
            except ValueError:
                print("Please enter a valid number for quantity.")
        else:
            print("Invalid key, please try again.")
    
    # Редактирование заказа перед сохранением
    while True:
        print("\nCurrent order:")
        for i, entry in enumerate(order, 1):
            item = entry['item']
            quantity = entry['quantity']
            print(f"{i}. {quantity} x {item['name']} - ${item['price'] * quantity:.2f}")
        edit_choice = input("\nDo you want to remove any item? (yes/no): ").lower()
        if edit_choice == 'no':
            break
        elif edit_choice == 'yes':
            try:
                item_index = int(input("Enter the item number to remove: ")) - 1
                if 0 <= item_index < len(order):
                    removed_item = order.pop(item_index)
                    print(f"Removed {removed_item['quantity']} x {removed_item['item']['name']} from your order.")
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Please enter 'yes' or 'no'.")
    
    # Сохранение заказа в текстовый файл
    if order:
        order_number = len([f for f in os.listdir() if f.endswith('.txt') and f[0].isdigit()]) + 1
        filename = f"{order_number}.txt"
        with open(filename, 'w') as file:
            file.write("Receipt\n")
            file.write("="*20 + "\n")
            total = 0
            for entry in order:
                item = entry['item']
                quantity = entry['quantity']
                # Правильный расчет subtotal
                subtotal = item['price'] * quantity
                file.write(f"{quantity} x {item['key']} - {item['name']} - ${subtotal:.2f}\n")
                total += subtotal
            file.write("="*20 + "\n")
            file.write(f"Total: ${total:.2f}\n")
        print(f"Order saved as {filename}.")
    else:
        print("No items in your order.")

# Функция для получения ежедневного отчета
def daily_report():
    report_filename = "daily_report.txt"
    order_files = [f for f in os.listdir() if f.endswith('.txt') and f[0].isdigit()]
    if not order_files:
        print("No orders have been made yet.")
        return
    
    total_sales = 0
    report_content = "Daily Report\n" + "="*20 + "\n"
    
    for order_file in order_files:
        with open(order_file, 'r') as file:
            lines = file.readlines()
        
        report_content += f"\n{order_file}:\n"
        item_count = 0
        order_total = 0
        keys = []
        for line in lines:
            if "x" in line and "$" in line:
                item_info = line.split("x")
                quantity = int(item_info[0].strip())
                item_key = item_info[1].split("-")[0].strip()
                item_price = float(line.strip().split("$")[-1]) / quantity  # Получаем цену за единицу
                subtotal = item_price * quantity  # Рассчитываем общую стоимость
                item_count += quantity
                keys.append(item_key)
                order_total += subtotal
        
        report_content += f"  Number of items: {item_count}\n"
        report_content += f"  Item keys: {', '.join(keys)}\n"
        report_content += f"  Order Total: ${order_total:.2f}\n"
        report_content += "="*20 + "\n"
        total_sales += order_total
    
    report_content += f"\nTotal Sales: ${total_sales:.2f}\n"
    
    try:
        with open(report_filename, 'w') as report_file:
            report_file.write(report_content)
        print(f"Daily report saved as {report_filename}.")
    except Exception as e:
        print(f"An error occurred while saving the report: {e}")
    
    print(report_content)

# Главное меню
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Make an Order")
        print("2. Daily Report")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            create_order()
        elif choice == '2':
            daily_report()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

# Запуск программы
if __name__ == "__main__":
    main_menu()



