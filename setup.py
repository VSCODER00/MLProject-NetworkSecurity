from setuptools import find_packages,setup
from typing import List
def get_requirements():
    requirements_List=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!= '-e .':
                    requirements_List.append(requirement)
    except FileNotFoundError:
         print("requirements.txt file not found")
    return requirements_List

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Vatsal Shah",
    author_email="vatsalshah1290@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)