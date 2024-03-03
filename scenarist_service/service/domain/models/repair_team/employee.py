from service.domain.models.repair_team.employee_grade import EmployeeGrade

from service.utils.json_serializable import IJsonSerializable


class Employee(IJsonSerializable):
    def __init__(self, name: str, grade: EmployeeGrade) -> None:
        self.name = name
        self.grade = grade

        self.is_weak = False
        self.is_busy = False

    name: str

    is_weak: bool
    is_busy: bool

    grade: EmployeeGrade
