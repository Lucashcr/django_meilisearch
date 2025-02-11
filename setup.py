from setuptools import setup, find_packages

setup(
    name="django_meilisearch",
    version="0.1.0",
    packages=find_packages("src/django_meilisearch"),
    include_package_data=True,
    install_requires=[
        "Django>=4.2",
        "meilisearch>=0.31.4",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    python_requires=">=3.9",
)
