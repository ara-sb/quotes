from setuptools import find_packages
from setuptools import setup


setup(
    name="quotes",
    version="1.0.0",
    author="Araceli Sanchez-Balbuena",
    author_email="arasanba@gmail.com",
    description="A website for posting quotes, built in Flask and sqlite database",
    url="https://github.com/ara-sb/quotes",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
