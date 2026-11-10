def reverse_array(numbers):
    left = 0
    right = len(numbers) - 1

    while left < right:
        numbers[left], numbers[right] = numbers[right], numbers[left]

        left += 1
        right -= 1

    return numbers

numbers = [1, 2, 3, 4, 5]

answer = reverse_array(numbers)

print("Reversed array:", answer)
