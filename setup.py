from setuptools import setup, find_packages
import os

# Read README file
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Augment VIP - VS Code Privacy & Database Management Tools"

setup(
    name="augment-vip",
    version="1.0.0",
    packages=find_packages(include=["src", "src.*", "augment_vip", "augment_vip.*"]),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "tqdm>=4.62.0",
    ],
    extras_require={
        "gui": [
            "PySide6>=6.5.0",
        ],
        "build": [
            "PySide6>=6.5.0", 
            "pyinstaller>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "augment-vip=cli:main",
            "augment-vip-gui=main:main",
        ],
    },
    python_requires=">=3.7",
    author="Reynald Silva",
    author_email="me@azrilaiman.my",
    description="VS Code Privacy & Database Management Tools with MVC Architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reysilva/vip-augmentai",
    project_urls={
        "Bug Reports": "https://github.com/reysilva/vip-augmentai/issues",
        "Source": "https://github.com/reysilva/vip-augmentai",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Desktop Environment",
        "Topic :: System :: System Shells",
        "Topic :: Utilities",
    ],
    keywords="vscode privacy database telemetry gui mvc qt pyside6",
)
