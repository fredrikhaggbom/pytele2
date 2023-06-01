import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytele2api",
    version="1.0.0",
    author="Fredrik Häggbom",
    author_email="fredrik.haggbom@gmail.com",
    description="Python library for communication with Tele2 My TSO",
    keywords=["tele2"],
    license="Apache 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fredrikhaggbom/pytele2",
    packages=setuptools.find_packages(),
    install_requires=["requests", "datetime"],
    tests_require=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
)
