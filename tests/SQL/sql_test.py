from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
import random
from sqlalchemy import text
from sqlalchemy import func


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.query.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter += 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter


<<<<<<< HEAD

    


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments = Assignment.query.filter(Assignment.student_id == 1).all()
=======
def test_get_assignments_in_various_states():
    """Test to get assignments in various states"""

    # Define the expected result before any changes
    expected_result = [('DRAFT', 2), ('GRADED', 2), ('SUBMITTED', 2)]
>>>>>>> 30e5ce2456d529834a39c2021286ed8d6b8e2042

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_assignments_per_state.sql', encoding='utf8') as fo:
        sql = fo.read()

    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]
        assert result[1] == sql_result[itr][1]

    # Modify an assignment state and grade, then re-run the query and check the updated result
    expected_result = [('DRAFT', 2), ('GRADED', 3), ('SUBMITTED', 1)]

    # Find an assignment in the 'SUBMITTED' state, change its state to 'GRADED' and grade to 'C'
    submitted_assignment: Assignment = Assignment.filter(Assignment.state == AssignmentStateEnum.SUBMITTED).first()
    submitted_assignment.state = AssignmentStateEnum.GRADED
    submitted_assignment.grade = GradeEnum.C

    # Commit the changes to the database
    db.session.commit()

    # Execute the SQL query again and compare the updated result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]
        assert result[1] == sql_result[itr][1]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Find the teacher who has graded the maximum number of assignments
    max_grading_teacher = db.session.query(
        Assignment.teacher_id,
        func.count(Assignment.id).label('total_graded_assignments')
    ).filter(
        Assignment.state == 'GRADED'
    ).group_by(
        Assignment.teacher_id
    ).order_by(
        func.count(Assignment.id).desc()
    ).first()

    if max_grading_teacher:
        max_teacher_id = max_grading_teacher[0]

        # Create and grade 5 assignments for the default teacher (teacher_id=1)
        grade_a_count_1 = create_n_graded_assignments_for_teacher(5)

        # Execute the SQL query to get the count of grade A assignments for the teacher with max grading
        sql_result = db.session.query(
            func.count(Assignment.id)
        ).filter(
            Assignment.teacher_id == max_teacher_id,
            Assignment.grade == 'A'
        ).scalar()

        print("Grade A count from function:", grade_a_count_1)
        print("Grade A count from SQL query:", sql_result)
        assert grade_a_count_1 == sql_result
    else:
        print("No teachers found with graded assignments.")

