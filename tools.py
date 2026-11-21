CREDIT_HOURS = {1: 17.0, 2: 18.0, 3: 18.0, 4: 18.0, 5: 18.0, 6: 19.0, 7: 18.0, 8: 15.0}

GRADE_POINTS = {
    "A": 4.0, "A-": 3.67,
    "B+": 3.33, "B": 3.0, "B-": 2.67,
    "C+": 2.33, "C": 2.0, "C-": 1.67,
    "D+": 1.33, "D": 1.0,
    "F": 0.0,
}

MAX_CGPA = 4.0


def get_credit_hours(semesters: list[int]) -> float:
    """Return the total credit hours for the given semester numbers (1 to 8).
    Use it when the student asks how many credit hours one or more semesters carry."""
    return sum(CREDIT_HOURS.get(s, 0.0) for s in semesters)


def grade_to_points(grade: str) -> float:
    """Convert a letter grade such as 'A-' or 'B+' to grade points on a 4.0 scale."""
    key = grade.strip().upper()
    if key not in GRADE_POINTS:
        raise ValueError(f"Unknown grade '{grade}'. Valid grades: {', '.join(GRADE_POINTS)}")
    return GRADE_POINTS[key]


def calculate_cgpa(grades: list[str], credit_hours: list[float]) -> float:
    """Calculate the credit-weighted GPA from parallel lists of letter grades and course credit hours.
    Use it for a semester GPA or an overall CGPA when the student gives individual course grades."""
    if len(grades) != len(credit_hours):
        raise ValueError("grades and credit_hours must have the same length")
    total_hours = sum(credit_hours)
    if total_hours <= 0:
        raise ValueError("Total credit hours must be greater than zero")
    points = sum(grade_to_points(g) * h for g, h in zip(grades, credit_hours))
    return round(points / total_hours, 2)


def project_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float:
    """Project the new CGPA after one more semester, given the current CGPA, the credit hours
    completed so far, and the GPA and credit hours of the coming semester."""
    total_hours = completed_credit_hours + semester_credit_hours
    if total_hours <= 0:
        raise ValueError("Total credit hours must be greater than zero")
    points = current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours
    return round(points / total_hours, 2)


def required_semester_gpa(
    current_cgpa: float,
    completed_credit_hours: float,
    upcoming_credit_hours: float,
    target_cgpa: float,
) -> float:
    """Return the GPA the student must earn over the upcoming credit hours to reach the target CGPA.
    A result above 4.0 means the target is not reachable in that many credit hours."""
    if upcoming_credit_hours <= 0:
        raise ValueError("upcoming_credit_hours must be greater than zero")
    needed = target_cgpa * (completed_credit_hours + upcoming_credit_hours) - current_cgpa * completed_credit_hours
    return round(needed / upcoming_credit_hours, 2)


def check_target_reachable(
    current_cgpa: float,
    completed_credit_hours: float,
    upcoming_credit_hours: float,
    target_cgpa: float,
) -> str:
    """Say whether a target CGPA can still be reached with the given upcoming credit hours,
    and what semester GPA that would take."""
    needed = required_semester_gpa(current_cgpa, completed_credit_hours, upcoming_credit_hours, target_cgpa)
    if needed > MAX_CGPA:
        best = project_cgpa(current_cgpa, completed_credit_hours, MAX_CGPA, upcoming_credit_hours)
        return f"Not reachable: it needs a {needed} GPA. The best possible CGPA with a perfect {MAX_CGPA} is {best}."
    if needed <= 0:
        return f"Already secured: the target {target_cgpa} holds even with a 0.0 GPA."
    return f"Reachable: the student needs a semester GPA of {needed} over {upcoming_credit_hours} credit hours."
