from typing import List
from pydantic import BaseModel
from sqlalchemy import DECIMAL, BigInteger, Column, DateTime, Double, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class ProblemRating(Enum):
    EXTREME = {
        "rating": "극상위권",
        "startCorrectRateRange": 0,
        "endCorrectRateRange": 30,
        "difficultyLevel": "최상"
    }
    TIER_1 = {
        "rating": "1등급",
        "startCorrectRateRange": 30,
        "endCorrectRateRange": 50,
        "difficultyLevel": "상"
    }
    TIER_2 = {
        "rating": "2등급",
        "startCorrectRateRange": 50,
        "endCorrectRateRange": 60,
        "difficultyLevel": "중상"
    }
    TIER_3 = {
        "rating": "3등급",
        "startCorrectRateRange": 60,
        "endCorrectRateRange": 80,
        "difficultyLevel": "중"
    }
    TIER_4 = {
        "rating": "4등급",
        "startCorrectRateRange": 80,
        "endCorrectRateRange": 90,
        "difficultyLevel": "중하"
    }
    OTHER = {
        "rating": "5등급 이하",
        "startCorrectRateRange": 90,
        "endCorrectRateRange": 100,
        "difficultyLevel": "하"
    }
    

class IncorrectProblem(BaseModel):
    problemNumber: str
    correctRate: float

class RatingRow(BaseModel):
    rating: int
    rawScores: str
    standardScores: int
    percentiles: int

class RatingTable(BaseModel):
    id: int
    practiceId: int
    ratingProvider: str
    ratingRows: List[RatingRow]

class EstimatedRank(BaseModel):
    ratingProvider: str
    estimatedRating: int

class RecommendedProblem(BaseModel):
    problemNumber: str
    difficultLevel: str
    correctRate: int
    rating: str
    imageUrl: str

class TestResult(BaseModel):
    testResultId: int
    score: int
    solvingTime: str
    averageSolvingTime: str
    estimatedRatingGetResponses: List[EstimatedRank]
    incorrectProblems: List[IncorrectProblem]
    ratingTables: List[RatingTable]

class DetailResultApplication(BaseModel):
    testResultId: int
    score: int
    solvingTime: str
    averageSolvingTime: str
    estimatedRatingGetResponses: List[EstimatedRank]
    incorrectProblems: List[IncorrectProblem]
    forCurrentRating: List[RecommendedProblem]
    forNextRating: List[RecommendedProblem]
    forBeforeRating: List[RecommendedProblem]

## DB table
class PracticeTest(Base):
    __tablename__ = "practice_test"

    practice_test_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(255), nullable=False)
    round = Column(String(255), nullable=True)
    subject = Column(String, nullable=False)
    publication_year = Column(String(255), nullable=True)
    version = Column(BigInteger, nullable=True)
    average_solving_time = Column(DECIMAL(21), nullable=True)
    solves_count = Column(Integer, nullable=True)
    view_count = Column(BigInteger, nullable=True)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)

    problems = relationship("Problem", back_populates="practice_test")

class TestResultTable(Base):
    __tablename__ = "test_result"

    test_result_id = Column(BigInteger, primary_key=True, autoincrement=True)
    practice_test_id = Column(BigInteger, nullable=False)
    score = Column(Integer, nullable=True)
    solving_time = Column(DECIMAL(21), nullable=True)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)

class Problem(Base):
    __tablename__ = "problem"  # 테이블 이름 설정

    problem_id = Column(BigInteger, primary_key=True, autoincrement=True)
    practice_test_id = Column(BigInteger, ForeignKey("practice_test.practice_test_id"), nullable=False)
    problem_image_id = Column(BigInteger, ForeignKey("problem_image.problem_image_id"), nullable=True)
    point = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
    incorrect_num = Column(BigInteger, nullable=True)
    answer = Column(String(255), nullable=True)
    concept_type = Column(String(255), nullable=True)
    problem_number = Column(String(255), nullable=True)
    subunit = Column(String(255), nullable=True)
    unit = Column(String(255), nullable=True)
    answer_format = Column(String, nullable=False)
    correct_rate = Column(Double, nullable=True)
    problem_rating = Column(String, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    # 관계 설정 (옵션)
    practice_test = relationship("PracticeTest", back_populates="problems")
    problem_image = relationship("ProblemImage", back_populates="problems")

class ProblemImage(Base):
    __tablename__ = "problem_image"  # 테이블 이름 설정

    problem_image_id = Column(BigInteger, primary_key=True, autoincrement=True)
    problem_id = Column(BigInteger, nullable=True)
    file_name = Column(String(255), nullable=True)
    image_file_extension = Column(String, nullable=False)
    image_key = Column(String(36), nullable=True)
    image_url = Column(String(255), nullable=True)

    # 관계 설정 (옵션)
    problems = relationship("Problem", back_populates="problem_image")