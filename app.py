from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# 🔹 Bubble Sort
def bubble_sort(arr):
    a = arr.copy()
    start = time.perf_counter()

    for i in range(len(a)):
        for j in range(0, len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]

    end = time.perf_counter()
    return a, end - start


# 🔹 Merge Sort
def merge_sort(arr):
    start = time.perf_counter()

    def merge_sort_recursive(a):
        if len(a) <= 1:
            return a

        mid = len(a) // 2
        left = merge_sort_recursive(a[:mid])
        right = merge_sort_recursive(a[mid:])

        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    sorted_arr = merge_sort_recursive(arr.copy())
    end = time.perf_counter()

    return sorted_arr, end - start


# 🔹 Home
@app.route('/')
def home():
    return render_template('index.html')


# 🔹 API
@app.route('/sort', methods=['POST'])
def sort():
    try:
        data = request.get_json()
        numbers = data.get("numbers", "")

        arr = [int(x.strip()) for x in numbers.split(",") if x.strip()]

        if not arr:
            return jsonify({"error": "No valid numbers provided"})

        bubble_res, bubble_time = bubble_sort(arr)
        merge_res, merge_time = merge_sort(arr)

        fastest = "Bubble Sort" if bubble_time < merge_time else "Merge Sort"

        return jsonify({
            "input": arr,
            "size": len(arr),
            "bubble_time": bubble_time,
            "merge_time": merge_time,
            "bubble_result": bubble_res,
            "merge_result": merge_res,
            "fastest": fastest,
            "bubble_complexity": "O(n²)",
            "merge_complexity": "O(n log n)"
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)