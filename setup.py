import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="generative_monster",
    version="0.1.0",
    author="Vilson Vieira",
    author_email="vilson@void.cc",
    description="A fully autonomous AI artist.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/automata/generative_monster",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)