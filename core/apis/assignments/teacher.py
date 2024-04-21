from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from enum import Enum
from core.models.assignments import Assignment, AssignmentStateEnum

class AssignmentStateEnum(Enum):
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'



from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)



def grade_assignment(_id, grade, auth_principal):
    """Grade an assignment"""
    # Find the assignment by its ID
    assignment = Assignment.query.filter_by(id=_id).first()

    # Check if the assignment exists
    if not assignment:
        # If the assignment does not exist, return a 404 error response
        return APIResponse.respond_error(status_code=404, message="Assignment not found")

    # Check if the authenticated principal is authorized to grade this assignment
    if auth_principal.teacher_id != assignment.teacher_id:
        # If not authorized, return a 403 error response
        return APIResponse.respond_error(status_code=403, message="You are not authorized to grade this assignment")

    # Check if the assignment is in the correct state to be graded
    if assignment.state == AssignmentStateEnum.DRAFT:
        # If the assignment is in the "Draft" state, return a 400 error response
        return APIResponse.respond_error(status_code=400, message="Cannot grade an assignment in Draft state")

    # Update the assignment's grade
    assignment.grade = grade

    # Change the assignment's state to GRADED
    assignment.state = AssignmentStateEnum.GRADED

    # Save the changes to the database
    db.session.commit()

    # Return a success response with the graded assignment
    graded_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=graded_assignment_dump)
