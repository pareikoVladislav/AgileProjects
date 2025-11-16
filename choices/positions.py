from enum import StrEnum

class UserPositions(StrEnum):
    CEO = "CEO"
    CTO = "CTO"
    DESIGNER = "Designer"
    PRODUCT_OWNER = "Product Owner"
    PROJECT_OWNER = "Project Owner"
    BACKEND_DEVELOPER = "Backend Developer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    IOS_DEVELOPER = "iOS Developer"
    MOBILE_DEVELOPER = "Mobile Developer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    DATA_SCIENTIST = "Data Scientist"
    DATA_ENGINEER = "Data Engineer"
    DATABASE_ADMIN = "Database Admin"
    ML_ENGINEER = "ML Engineer"
    PROJECT_MANAGER = "Project Manager"
    QA = "QA"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
