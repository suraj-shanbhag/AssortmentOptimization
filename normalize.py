def get_step_one_row(initial_people_array, rest_people_array):
    rest_people_array.remove(initial_people_array)
    flat_set = set(flatten(rest_people_array))
    difference = set(initial_people_array).difference(flat_set)
    intersection_set = set(initial_people_array).difference(difference)
    return len(difference), list(intersection_set)


def get_intersection_elements_score(intersection_list, first_copy):
    intersection_elements_final_score = {}
    for element in intersection_list:
        count = 0
        for sub_category_column in first_copy:
            if (element in sub_category_column):
                count += 1
        intersection_elements_final_score[element] = float(1) / count
    return intersection_elements_final_score


def normalize(row_of_entities, principle_diagonal_element):
    normalized_row_result = [None] * len(row_of_entities)
    rest_sum = normalize_pde(normalized_row_result, principle_diagonal_element, row_of_entities)
    intersection_set = []
    for i in range(len(row_of_entities)):
        if (not i == principle_diagonal_element):
            new_initial_array = row_of_entities.iloc[i]
            new_rest_sum = list(rest_sum)
            normalized_row_result[i], intersection_per_row = get_step_one_row(new_initial_array, new_rest_sum)
            intersection_set.append(intersection_per_row)
    intersection_list = flatten(intersection_set)
    rest_sum_second_copy = list(rest_sum)
    intersection_element_score = get_intersection_elements_score(intersection_list, rest_sum_second_copy)
    for people_list_index in range(len(row_of_entities)):
        if (not people_list_index == principle_diagonal_element):
            for element in row_of_entities.iloc[people_list_index]:
                if (element in intersection_element_score.keys()):
                    normalized_row_result[people_list_index] += intersection_element_score[element]
    sum_per_row = sum(normalized_row_result)
    for idx, value in enumerate(normalized_row_result):
        normalized_row_result[idx] = (value / sum_per_row)
    return normalized_row_result


def normalize_pde(normalized_row_result, principle_diagonal_element, row_of_entities):
    rest_sum = row_of_entities.tolist()
    rest_sum.remove(rest_sum[principle_diagonal_element])
    flat_set = set(flatten(rest_sum))
    normalized_row_result[principle_diagonal_element] = len(
        set(row_of_entities.iloc[principle_diagonal_element]).difference(flat_set))
    return rest_sum


def flatten(nested_list):
    return [x for sublist in nested_list for x in sublist]


def get_demand_for_each_product(people_data_frame):
    normalized_grid = []
    for i in range(len(people_data_frame.index)):
        normalized_row = normalize(people_data_frame.iloc[i], i)
        normalized_grid.append(normalized_row)
    return normalized_grid
