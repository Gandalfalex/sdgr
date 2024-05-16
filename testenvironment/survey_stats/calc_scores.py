def calculate_tlx_score(data):
    values = [int(i) for i in data.values()]
    group_scores = [score * (100 / 9) for score in values]
    group_tlx_score = sum(group_scores) / len(group_scores)

    return group_tlx_score, values


def calculate_sus_score(data):
    values = [int(i) for i in data.values()]
    responses = [score * (5 / 6) + 1 for score in values]
    odd_responses = responses[::2]
    even_responses = responses[1::2]
    converted_odd_responses = [score - 1 for score in odd_responses]
    converted_even_responses = [5 - score for score in even_responses]
    all_converted_scores = converted_odd_responses + converted_even_responses

    sus_score = sum(all_converted_scores) * 2.5
    print(sus_score)
    return sus_score, values


def calculate_sus_score_total(data):
    responses = [0] * len(data[0])
    for i in data:
        for j in range(len(i)):
            responses[j] = responses[j] + i[j]
    responses = [i / len(data) for i in responses]
    responses = [score * (5 / 6) + 1 for score in responses]

    odd_responses = responses[::2]  # This gets the odd numbered items from the list (Python uses 0-indexing)
    even_responses = responses[1::2]  # This gets the even numbered items from the list
    # Step 2: Convert scores
    converted_odd_responses = [score - 1 for score in odd_responses]
    converted_even_responses = [5 - score for score in even_responses]
    all_converted_scores = converted_odd_responses + converted_even_responses
    sus_score = sum(all_converted_scores) * 2.5

    # Display the SUS Score
    print("The final SUS Score is:", sus_score)


def calculate_tlx_score_total(data):
    total = []
    for i, group in enumerate(data):
        group_scores = [score * (100 / 9) for score in group]
        group_tlx_score = sum(group_scores) / len(group_scores)
        total.append(group_tlx_score)
    print(sum(total) / len(total))
