"""
This module provides functions for processing and analyzing user data
in a dating or recommendation system.
"""
from __future__ import annotations
from typing import Optional

import csv
import pandas as pd
import python_ta
from tree import add_priority, BinaryTree, filter_user_by_dating_goal


def data_wrangling(current_user, user_characteristics, users_list,
                   file_name: Optional[str] = "data.csv") -> None:
    """
    Creates a CSV file containing user data, including their characteristics and potential matches.

    The CSV file structure:
    - The first row contains characteristics ordered according to users' ranking.
    - The first column contains user names.
    - Each row represents a potential match, with a ranking value of 0 or 1.
      - A value of 1 indicates a match in characteristics with the current user.
      - A value of 0 indicates no match.

    """
    if isinstance(user_characteristics, list):
        heading = user_characteristics
    else:
        heading = add_priority(user_characteristics)
        current_user = users_list[-1]

    potential_users = filter_user_by_dating_goal(users_list, current_user)

    data = {"name": []}

    for person in potential_users:
        data["name"].append(person.name)

    for attribute in heading:
        answer = []
        for person in potential_users:
            # print(current_user.characteristics.religion)
            current_user_value = getattr(current_user.characteristics, attribute)
            potential_user_value = getattr(person.characteristics, attribute)

            if current_user_value == potential_user_value:
                answer.append(1)
            else:
                answer.append(0)
        data[attribute] = answer

    # print(data)
    df = pd.DataFrame(data)
    csv_file_path = file_name

    df.to_csv(csv_file_path, index=False)

    print(f'CSV file "{csv_file_path}" has been created successfully.')


def generate_10_people_list(full_list: list) -> list:
    """
    Generates a list of 10 people by sequentially removing the first element
    from the provided full_list.

    >>> people = ["Person1", "Person2", "Person3", "Person4", "Person5",
    ...           "Person6", "Person7", "Person8", "Person9", "Person10", "Person11"]
    >>> generate_10_people_list(people)
    ['Person1', 'Person2', 'Person3', 'Person4', 'Person5',
    ...           "Person6", "Person7", "Person8", "Person9", "Person10"]
    """
    new_list = []
    while len(new_list) < 10:
        new_list.append(full_list.pop(0))
    return new_list


# @check_contracts
def build_preference_tree(file: str) -> BinaryTree():
    """
    Builds a preference tree from a CSV file.

    """

    tree = BinaryTree("")

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = str(row[0])
            match = [int(item) for item in row[1:]]
            match.append(name)
            tree.insert_sequence(match)
    # print(tree)
    return tree


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'user_network', 'tree', 'csv'],
        'allowed-io': ['data_wrangling', 'build_preference_tree'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9970']
    })
