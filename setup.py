from setuptools import setup, find_packages

setup(
    name="projecteuler",
    version="0.0.1",
    description="Project Euler solutions",
    author="Hendrik Kühne",
    author_email="hendrik.kuehne2@gmail.com",
    url="https://github.com/HendrikKuehne/projecteuler.git",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "cotengra",
        "opt_einsum",
        "networkx",
        "matplotlib",
    ],
)

