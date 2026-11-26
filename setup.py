from setuptools import setup, find_packages

setup(
    name="my_project",
    version="1.0.0",
    description="Backend project for Database Lab 4 (Flask + MySQL)",
    author="Student",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.0.0",
        "Flask-SQLAlchemy>=3.1.0",
        "PyMySQL>=1.1.0",
        "PyYAML>=6.0.1",
    ],
    python_requires=">=3.8",
)
