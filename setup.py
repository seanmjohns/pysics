import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysics-seanmjohns",
    version="0.1.1",
    author="Sean Johnson",
    author_email="seanmjohns1@gmail.com",
    description="A physics engine for python games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanmjohns/pysics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.6',
)
