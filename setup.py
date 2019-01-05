import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvbus",
    version="0.0.1",
    author="Erwann PENET",
    author_email="erwann@zeflip.com",
    description="A Python library for processing RESOL VBus data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epenet/pyvbus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
