from setuptools import setup, find_packages

setup(
    name="dns-check",
    use_scm_version={"root": ".","relative_to": __file__,"local_scheme": "no-local-version"},
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    install_requires=[
        "requests",
        "geopy",
        "tqdm",
        "colorama",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "dns-check = src.main:main",
        ],
    },
    author="hesami",
    description="Performing DNS tests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hesami/dns-check",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)