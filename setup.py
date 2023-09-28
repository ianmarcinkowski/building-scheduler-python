from setuptools import setup, find_packages

setup(
    name='building_scheduler',
    description="3 hour coding challenge",
    author='Ian Marcinkowski',
    author_email='ian@desrt.ca',
    version='1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "pytest"
    ],
    python_requires='>=3.8',
)
