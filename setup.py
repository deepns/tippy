import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tippy-deepns", # Replace with your own username
    version="0.0.1",
    author="Deepan",
    author_email="author@example.com",
    description="My own collection of tips for easy retrieval and rememberance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepns/tippy",
    project_urls={
        "Bug Tracker": "https://github.com/deepns/tippy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    scripts=["bin/tippy"]
)