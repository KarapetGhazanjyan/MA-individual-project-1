import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musicrecsys",
    version="0.1",
    author="Karapet Ghazanjyan",
    author_email="karapet_ghazanjyan@edu.aua.am",
    description="Music Recommendation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KarapetGhazanjyan/MA-individual-project-1",
    packages=setuptools.find_packages(),
    package_data={'package': ['data/*.csv']},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)