from setuptools import find_packages, setup

setup(
    name = 'ai_course',
    version= '0.0.1',
    author= 'mounika',
    author_email= 'ramyasrimounika03@gmail.com',
    packages= find_packages(where="src"),
    package_dir={"": "src"},
    install_requires = []

)