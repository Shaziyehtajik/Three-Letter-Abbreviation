The purpose of writing this report is to give details about an abbreviation program that generates and calculates the score of a three-letter abbreviation of each name. This program takes an input file, reads it afterward, and creates abbreviations based on the specified scoring criteria. This brief description outlines the key components and functions that are used in this Python code. 

Program Structure and Style:
The program adheres to a consistent indentation style (four spaces) for improved readability. Variable and function names have been made more descriptive, enhancing self-documentation. Clear and concise comments have been added to explain the purpose and functionality of key components:
1.	Loading Letter Scores: The program starts by loading letter scores from a file named "values.txt." These scores are used to calculate the overall score for each three-letter abbreviation.
2.	Generating Three-Letter Abbreviations: For each name in the list, the program generates three-letter abbreviations. It considers the first letter of the name along with all possible combinations of two subsequent letters within the name.
3.	Calculating Abbreviation Scores: The program calculates scores for each three-letter abbreviation based on the position of each letter and the letter scores loaded from the file.
4.	Validating Abbreviations: The program validates abbreviations by excluding those formed from more than one name, ensuring that only unique abbreviations are considered.
5.	Finding Best Abbreviations: The program identifies the best abbreviation with the lowest score for each name.
6.	Writing Abbreviations to File: Finally, the program prompts the user for their surname, and it writes the best abbreviations for each name to an output file named "{surname}_{filename}_3letterabbreviations.txt."
