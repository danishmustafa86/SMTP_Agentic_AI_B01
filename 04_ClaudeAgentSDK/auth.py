def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list.")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("All elements in the list must be numeric (int or float).")
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def get_user_name(user):
    if not isinstance(user, dict):
        raise TypeError("Expected a dictionary for 'user'.")
    if "name" not in user:
        raise KeyError("The 'user' dictionary must contain a 'name' key.")
    name = user["name"]
    if not isinstance(name, str):
        raise TypeError("The 'name' value must be a string.")
    return name.upper()