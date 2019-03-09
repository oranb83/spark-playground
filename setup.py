from setuptools import setup, find_packages


setup(
    name="spark-playground",
    version="1.0.0",
    description="A Spark playground project",
    author_email="oranb83@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7.2",
    ],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[open("requirements.txt").read().splitlines()],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==3.5.0"],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": [
            "spark-playground=spark_playground:main",
        ],
    }
)
