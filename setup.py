import pathlib

import setuptools

setuptools.setup(
    name="github-trending-api",
    version="1.0.0",
    author="Niklas Tiede",
    author_email="niklastiede2@gmail.com",
    description="trending github repositories/developers API",
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/NiklasTiede/Github-Trending-API",
    license="MIT",
    package_dir={"": "app"},
    packages=setuptools.find_packages(where="app"),
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "beautifulsoup4",
        "aiohttp",
    ],
    extras_require={
        "dev": [
            "pytest",
            "mypy",
        ],
    },
    platforms="linux",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
