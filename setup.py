from setuptools import setup, find_packages

# Include the requirements directly in setup.py to avoid file not found errors during build
requirements = [
    "sentence-transformers",
    "transformers",
    "requests",
    "pyyaml",
    "colorama",
    "openai",
    "anthropic"
]

setup(
    name='nova-hunting',
    version='0.1.4',  # Updated version from 0.1.3 to 0.1.4
    author='Thomas Roccia',
    author_email='contact@securitybreak.io',
    description='Prompt Pattern Matching Framework for Generative AI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fr0gger/nova-framework',
    packages=find_packages(exclude=["tests*", "nova_doc*", "*.pyc"]),
    install_requires=requirements,
    include_package_data=True,
    package_data={'nova': ['nova_rules/*.nov']},
    entry_points={
        'console_scripts': [
            'novarun=nova.novarun:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    license='MIT',
    zip_safe=False,  # This helps ensure all files are properly installed
)
