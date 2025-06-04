from setuptools import setup, find_packages

setup(
    name="aemet_plugin",
    version="0.1.0",
    description="Async Python client for the AEMET Antarctica API",
    author="Challenge axpo",
    author_email="challengeaxpo@gmail.com",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "pandas",
        "python-dateutil"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    license="MIT",
    url="https://github.com/ChallengeAxpo/aemet_plugin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)