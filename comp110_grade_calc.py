"""Program for calculating COMP110 grade."""

from fractions import Fraction

inputting: bool = True # allows user to enter in scores

def main():
    """Main function."""
    print("COMP110 Grade Calculator")
    print("This program will compute your estimated final average for COMP110 based off of weighted values in the syllabus.")
    print("You will be prompted to enter grade values and their category. Enter END when done.")
    print("---------------------------------------------------------------------")
    while True:
        ls: list[float] = []
        qz: list[float] = []
        rd: list[float] = []
        pj: list[float] = []
        ex: list[float] = []
        final_exam: list[float] = []
        final_avg: float = 0.0
        while inputting:
            current_grade = input_grade_value()
            if inputting:
                current_grade_type = input_grade_type()
                append_to_total(current_grade, current_grade_type, ls, qz, rd, pj, ex, final_exam)
        
        # establish dictionaries to hold the scores and their weights
        grades: dict[str, list[float]] = {'qz': qz, 'pj': pj, 'ex': ex, 'final_exam': final_exam, 'ls': ls, 'rd': rd}
        weights: dict[str, float] = {'qz': 0.3, 'pj': 0.25, 'ex': 0.2, 'final_exam': 0.15, 'ls': 0.04, 'rd': 0.06}

        complete: bool = check_for_completion(grades)  # make sure user has entered a value for each category
        if not complete:
            print("NOTE: You have not entered at least 1 grade for all six categories and therefore your calculated average is incomplete.")
        else:  # adjust average if final exam score exceeds lowest quiz score
            lowest_quiz_dropped = quiz_drop(grades, weights)
            if lowest_quiz_dropped:
                quiz_scores: list[float] = grades['qz']
                lowest_qz: list[bool] = filter_lowest_qz(quiz_scores)
                grades['qz'] = remove_lowest_qz(quiz_scores, lowest_qz)
                print("NOTE: Your final exam score exceeds your lowest quiz score and your average has been adjusted accordingly.")

        final_avg = round(calculate_avg(grades, weights), 2)
        print(f"Your estimated final COMP110 grade: {final_avg} %")
        print("------------------------------------------------------")
        recalc = input("Recalculate score? (Press ENTER to recalculate score or type 'q' to quit). ")
        if recalc.lower() == 'q':
            break
        else:
            initialize()


def input_grade_value() -> float:
    """Accepts user input for grade value and checks whether it is a float or a fraction."""
    global inputting
    while True:
        user_input = input("ENTER GRADE: Must be either a fraction or number out of 100. Type 'end' if complete. ")
        if user_input.lower() == 'end':
            inputting = False
            return 0
        else:
            if '/' in user_input: # checks if input is a fractional value
                try:
                    user_input = float(Fraction(user_input)) * 100
                    return user_input
                except ValueError:
                    print("ERROR: Invalid entry.")
            else:
                try: # checks if input is of type float
                    user_input = float(user_input)
                    if user_input >= 0: # checks if input is positive
                        return user_input
                    else:
                        print("ERROR: Invalid entry.")
                except ValueError:
                    print("ERROR: Invalid entry.")


def input_grade_type() -> str:
    """Checks for the type of grade to apply weighting."""
    while True:
        possible_types: list[str] = ['ls', 'rd', 'ex', 'qz', 'pj', 'final']
        grade_type = input("ENTER CATEGORY (ls, rd, ex, qz, pj, final): ")
        if grade_type not in possible_types:
            print("ERROR: Invalid grade type. Must be: ls, rd, ex, qz, pj, or final.")
        else:
            return grade_type


def append_to_total(grade_value, grade_type, ls, qz, rd, pj, ex, final_exam) -> None:
    """Assigns the grade value to its category."""

    if grade_type == 'ls':
        ls.append(grade_value)
    elif grade_type == 'qz':
        qz.append(grade_value)
    elif grade_type == 'rd':
        rd.append(grade_value)
    elif grade_type == 'pj':
        pj.append(grade_value)
    elif grade_type == 'ex':
        ex.append(grade_value)
    else:
        final_exam.append(grade_value)


def calculate_avg(grade_values: dict[str, list[float]], weights: dict[str, float]) -> float:
    """Calculates final average."""
    weighted_avgs: list[float] = []
    for i in grade_values:
        if len(grade_values[i]) != 0:
            avg = sum(grade_values[i]) / len(grade_values[i])
            weighted_avgs.append(avg * weights[i])

    total_avg = sum(weighted_avgs)
    return total_avg


def check_for_completion(grade_values: dict[str, list[float]]) -> bool:
    """Checks whether at least one value is in each grade category."""
    for item in grade_values:
        if len(grade_values[item]) == 0:
            return False
    
    return True


def quiz_drop(grade_values: list[float], weights: dict[str, float]) -> bool:
    """Determines whether weight should be adjusted for last quiz grade."""
    if len(grade_values['qz']) != 1:
            lowest_quiz_score = min(grade_values['qz'])
            if lowest_quiz_score < grade_values['final_exam'][0]:
                weights['final_exam'] = 0.21
                weights['qz'] = 0.24
                return True
                
    return False


def filter_lowest_qz(qz_scores: list[float]) -> list[bool]:
    """Returns a list that determines if quiz score is the lowest."""
    result: list[bool] = []
    for item in qz_scores:
        result.append(item == min(qz_scores))

    return result


def remove_lowest_qz(qz_scores: list[float], lowest: list[bool]) -> list[float]:
    """Returns a list with lowest quiz score dropped."""
    result: list[float] = []
    for i in range(len(lowest)):
        if not lowest[i]:
            result.append(qz_scores[i])

    return result


def initialize() -> None:
    """Makes 'inputting' value true so user can input new scores."""
    global inputting
    inputting = True


if __name__ == "__main__":
    main()
