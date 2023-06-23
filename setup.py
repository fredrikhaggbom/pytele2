import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytele2api",
    version="0.1.7",
    author="Fredrik Häggbom",
    author_email="fredrik.haggbom@gmail.com",
    description="Python library for communication with Tele2 My TSO",
    download_url="https://github.com/fredrikhaggbom/pytele2/archive/refs/tags/0.1.7.tar.gz",
    keywords=["tele2"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fredrikhaggbom/pytele2",
    packages=setuptools.find_packages(),
    install_requires=["requests", "datetime"],
    tests_require=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
