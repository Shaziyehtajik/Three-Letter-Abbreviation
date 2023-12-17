import re

def load_letter_scores(file_path="values.txt"):
    """
    Load letter scores from a file.

    Parameters:
    - file_path (str): Path to the file containing letter scores.

    Returns:
    - dict: Dictionary mapping letters to their scores.
    """
    values = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                letter, score = line.strip().split()
                values[letter] = int(score)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except ValueError:
        print(f"Error: {file_path} does not have the expected format.")
    return values

def calculate_letter_score(letter, position, values):
    """
    Calculate the score for a letter based on its position and values.

    Parameters:
    - letter (str): The letter for which to calculate the score.
    - position (int): The position of the letter.
    - values (dict): Dictionary mapping letters to their scores.

    Returns:
    - int: The calculated score.
    """
    if position == 0:
        return 0
    elif position == 1:
        return 1 if letter != 'E' else 20
    elif position == 2:
        return 2
    else:
        return 3 + values.get(letter, 0)

def generate_three_letter_abbreviations(name):
    """
    Generate three-letter abbreviations for a given name.

    Parameters:
    - name (str): The name for which to generate abbreviations.

    Returns:
    - set: Set of three-letter abbreviations.
    """
    words = re.findall(r'\b\w+\b', name.upper())
    abbreviations = set()

    for word in words:
        first_letter = word[0]
        for i in range(len(word)):
            for j in range(i + 1, len(word) + 1):
                abbreviation = f"{first_letter}{word[i:j]}"
                if len(abbreviation) == 3:
                    abbreviations.add(abbreviation)

    return abbreviations

def calculate_abbreviation_score(abbreviation, values):
    """
    Calculate the score for a three-letter abbreviation.

    Parameters:
    - abbreviation (str): The abbreviation for which to calculate the score.
    - values (dict): Dictionary mapping letters to their scores.

    Returns:
    - int: The calculated score.
    """
    score = 0
    for i, letter in enumerate(abbreviation[1:]):
        score += calculate_letter_score(letter, i + 1, values)
    return score

def write_abbreviations_to_file(best_abbreviations, filename):
    """
    Write abbreviations to an output file based on the user surname.

    Parameters:
    - best_abbreviations (dict): Dictionary mapping names to their best abbreviations.
    - filename (str): The name of the input file.

    Returns:
    - None
    """
    user_surname = input('Enter your surname: ')
    output_lines = []

    for word, abbreviations in best_abbreviations.items():
        clean_word = re.sub(r"[\n]", '', word)
        output_lines.append(f'{clean_word}\n')
        abbreviation_string = ' '.join(abbreviations)
        output_lines.append(f'{abbreviation_string}\n\n')

    with open(f'./{user_surname}_{filename}_3letterabbreviations.txt', 'w') as output:
        output.writelines(output_lines)
    print(f"Abbreviations written to {user_surname}_{filename}_3letterabbreviations.txt")

def find_best_abbreviations(names_and_scores):
    """
    Get the best abbreviation for each name based on scores.

    Parameters:
    - names_and_scores (dict): Dictionary mapping names to their abbreviation scores.

    Returns:
    - dict: Dictionary mapping names to their best abbreviations.
    """
    best_abbreviations = {}

    for name, scores in names_and_scores.items():
        if not scores:
            best_abbreviations[name] = "_____"
        else:
            sorted_scores = sorted(scores, key=lambda x: x[1])
            best_abbrev = [abbr for abbr, score in sorted_scores if score == sorted_scores[0][1]]
            best_abbreviations[name] = best_abbrev

    return best_abbreviations

def calculate_abbreviation_scores(names_and_abbreviations, values):
    """
    Calculate scores for abbreviations.

    Parameters:
    - names_and_abbreviations (dict): Dictionary mapping names to their possible abbreviations.
    - values (dict): Dictionary mapping letters to their scores.

    Returns:
    - dict: Dictionary mapping names to their abbreviation scores.
    """
    validated_abbreviations = validate_abbreviations(names_and_abbreviations)
    names_and_scores = {}
    
    for name, abbreviations in names_and_abbreviations.items():
        abbrevs_and_scores = []

        clean_name = re.sub(r"[\n+(),:']", '', name)
        cleaner_name = re.sub(r"-", ' ', clean_name).upper()
        words = cleaner_name.split()

        for abbr in abbreviations:
            score = 0
            if abbr not in validated_abbreviations:
                continue

            for i in range(1, len(abbr)):
                condition_met = False
                pos = 1 if len(words) >= 2 else 0
                
                for j in range(pos, len(words)):
                    if abbr[i] == words[j][0]:
                        score += 0
                        condition_met = True
                        break

                if condition_met:
                    continue

                for word in words:
                    if abbr[i] == word[-1]:
                        if abbr[i] == 'E':
                            score += 20
                        else:
                            score += 5
                        condition_met = True
                        break

                if condition_met:
                    continue

                position_value = 0
                for j in range(0, len(words)):
                    if len(words[j]) > 1:
                        if abbr[i] == words[j][1]:
                            position_value += 1
                        elif abbr[i] == words[j][2]:
                            position_value += 2
                        else:
                            position_value += 3

                        score += position_value + values.get(abbr[i], 0)
                        break

            abbrev_and_score = (abbr, score)
            abbrevs_and_scores.append(abbrev_and_score)
        names_and_scores[name] = abbrevs_and_scores
    
    return names_and_scores

def validate_abbreviations(names_and_abbreviations):
    """
    Validate abbreviations by excluding those formed from more than one name.

    Parameters:
    - names_and_abbreviations (dict): Dictionary mapping names to their possible abbreviations.

    Returns:
    - list: List of valid abbreviations.
    """
    counted_abbreviations = count_abbreviations(names_and_abbreviations)
    valid_abbreviations = []

    for abbr, count in counted_abbreviations.items():
        if count == 1:
            valid_abbreviations.append(abbr)

    return valid_abbreviations

def count_abbreviations(names_and_abbreviations):
    """
    Count the number of times an abbreviation appears for each name.

    Parameters:
    - names_and_abbreviations (dict): Dictionary mapping names to their possible abbreviations.

    Returns:
    - dict: Dictionary mapping abbreviations to their counts.
    """
    abbreviation_and_count = {}
    list_abbreviations = []

    for item in names_and_abbreviations.values():
        for subitem in item:
            list_abbreviations.append(subitem)
    
    for item in list_abbreviations:
        abbreviation_and_count[item] = list_abbreviations.count(item)
    
    return abbreviation_and_count

def get_abbreviations(list_of_names):
    """
    Generate a dictionary of abbreviations from each name in the list.

    Parameters:
    - list_of_names (list): List of names.

    Returns:
    - dict: Dictionary mapping names to their possible abbreviations.
    """
    names_and_abbreviations = {}
    abbreviations = set()

    for name in list_of_names:
        clean_name = re.sub(r"[\n+(),:']", '', name)
        cleaner_name = re.sub(r"-", ' ', clean_name).upper()

        for i in range(len(cleaner_name)):
            if i == 0 and len(cleaner_name) > 3:
                for j in range(1, len(cleaner_name)):
                    if cleaner_name[j] != ' ':
                        for k in range(j + 1, len(cleaner_name)):
                            if cleaner_name[k] != ' ':
                                substr = cleaner_name[i] + cleaner_name[j] + cleaner_name[k]
                                abbreviations.add(substr)
            
            elif len(cleaner_name) <= 3:
                abbreviations.add(cleaner_name)
               
        names_and_abbreviations[name] = abbreviations
        abbreviations = set()
    
    return names_and_abbreviations

def read_names_from_file():
    """
    Read file and produce a list of names.

    Returns:
    - tuple: A tuple containing a list of names and the filename.
    """
    filename = input('Please specify the name of the input file, including its extension (such as .txt, .pdf, .xml, etc.): ')
    list_of_names = []

    try:
        with open(f'./{filename}', 'r') as content:
            for line in content:
                list_of_names.append(line)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return list_of_names, filename

def generate_and_write_abbreviations():
    """
    Generate abbreviations based on user input and write them to an output file.

    Returns:
    - None
    """
    list_of_names, filename = read_names_from_file()
    letter_scores = load_letter_scores()

    if not letter_scores:
        print("Abbreviations cannot be generated without letter scores.")
        return

    names_and_abbreviations = get_abbreviations(list_of_names)
    names_and_scores = calculate_abbreviation_scores(names_and_abbreviations, letter_scores)
    best_abbreviations = find_best_abbreviations(names_and_scores)
    write_abbreviations_to_file(best_abbreviations, filename)

if __name__ == '__main__':
    generate_and_write_abbreviations()
