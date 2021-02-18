import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MSPStreamMaths",
    version="0.1.0",
    author="Alexander Leris",
    author_email="aleris@melbournespaceprogram.com",
    description="A small package to process data streams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adleris/streammaths",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=['MSPStreamMaths']),
    python_requires='>=3.6',
    install_requires=[],
    setup_requires=[],
    tests_requires=['numpy','matplotlib']
)