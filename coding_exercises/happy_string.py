import heapq

def longest_diverse_string(a: int, b: int, c: int) -> str:
    input_chars = []
    result_chars = []

    # heappq only support min heap, so negate all priorities to simulate max heap
    heapq.heappush(input_chars, (-a, "a"))
    heapq.heappush(input_chars, (-b, "b"))
    heapq.heappush(input_chars, (-c, "c"))

    while input_chars:
        priority, char = heapq.heappop(input_chars)

        if priority != -1:
            heapq.heappush(input_chars, (priority + 1, char))

        if len(result_chars) > 1 and result_chars[-1] == char and result_chars[-2] == char:
            continue

        result_chars.append(char)

    return "".join(result_chars)