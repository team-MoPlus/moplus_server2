from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session

import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from PIL import Image

import models


## Problem
def get_problem(db: Session, practice_test_id: int, wrong_problem_number_list: List[int]):
    return db.query(models.Problem).filter(
        and_(
            models.Problem.practice_test_id == practice_test_id,
            models.Problem.problem_number.in_(wrong_problem_number_list)
        )
    ).all()

## Problem Image
def get_image(db: Session, problem_id: int):
    return db.query(models.ProblemImage).filter(models.ProblemImage.problem_id == problem_id).first()