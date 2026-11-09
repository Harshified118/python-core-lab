
def find_second_largest(numbers):
    largest = numbers[0]
    second_largest = None

    for number in numbers[1:]:
        if number > largest:
            second_largest = largest
            largest = number

        elif number != largest:
            if second_largest is None or number > second_largest:
                second_largest = number

    return second_largest


numbers = [12, 5, 27, 9, 18]

answer = find_second_largest(numbers)

print("Second largest element:", answer)
