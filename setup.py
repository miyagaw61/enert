from setuptools import setup, find_packages

console_scripts = [
        "calc=enert.enert:calc_command"
        ]

setup(
    name="enert",
    version="0.0.2",
    packages=find_packages(),
    description="miyagaw61's python library",
    author="Taisei Miyagawa <miyagaw61 at miyagaw61.github.io>",
    author_email="miyagaw61@gmail.com",
    entry_points = {"console_scripts": console_scripts},
    url="https://github.com/miyagaw61/enert.git",
    license="MIT"
)
