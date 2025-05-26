from setuptools import setup, find_packages

setup(
    name='language_project',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    description='A custom programming language project.',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)