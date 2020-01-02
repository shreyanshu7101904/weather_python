from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'CloudSEK Demo Weather app'
setup(
    name='Temprature Module',
    version='1.0',
    author='Shreyanshu Shankar',
    author_email='shreyanshuperfect13@gmail.com',
    url='https://github.com/shreyanshu7101904/weather_python.git',
    description='Weather App Demo Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'weatherapp = weatherapp.weatherTerminal:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='CloudSEK weatherdata Weather library',
    install_requires=requirements,
    zip_safe=False
)
