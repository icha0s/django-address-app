from setuptools import find_packages, setup

from django_address import __version__ as version

requirements = ["Django>=2.2", "requests", "typing-extensions", "psycopg2-binary", "environs", "structlog", "swapper"]

extras_require = {
    "test": ["pytest-cov", "pytest-django", "pytest"],
    "lint": ["flake8", "wemake-python-styleguide", "isort"],
}

extras_require["dev"] = extras_require["test"] + extras_require["lint"]  # noqa: W504  # noqa: W504

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()


setup(
    name="django-address-app",
    author="Vyacheslav Onufrienko",
    author_email="onufrienkovi@gmail.com",
    description="Django models for storing and retrieving postal addresses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    url="https://github.com/onufrienkovi/django-address-app",
    extras_require=extras_require,
    packages=find_packages(exclude=["tests", "docs", "scripts", "example"]),
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
