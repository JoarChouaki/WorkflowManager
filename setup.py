import setuptools


setuptools.setup(
    name="exercise-easymovie", 
    version="0.0.1",
    author="jchouaki",
    author_email="joar.chouaki@eleves.enpc.fr",
    description="A workflow manager, allowing the user to create workflows and incorporate steps into them",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)