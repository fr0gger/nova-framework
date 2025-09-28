from setuptools import setup, find_packages

# Core dependencies - minimal for basic functionality (keywords, basic parsing)
core_requirements = [
    "requests>=2.25.0",
    "pyyaml>=5.4.0", 
    "colorama>=0.4.4"
]

# Advanced LLM dependencies - for semantic matching and LLM evaluation
llm_requirements = [
    "sentence-transformers>=2.0.0",
    "transformers>=4.20.0",
    "openai>=1.0.0",
    "anthropic>=0.3.0"
]

# Development dependencies - for testing and development
dev_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0"
]

# Documentation dependencies - for building documentation
docs_requirements = [
    "mkdocs>=1.4.0",
    "mkdocs-material>=8.5.0",
    "mkdocs-material[imaging]>=8.5.0"
]

setup(
    name='nova-hunting',
    version='0.1.5',  # Updated version to reflect new packaging structure
    author='Thomas Roccia',
    author_email='contact@securitybreak.io',
    description='Prompt Pattern Matching Framework for Generative AI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fr0gger/nova-framework',
    packages=find_packages(exclude=["tests*", "nova_doc*", "*.pyc"]),
    install_requires=core_requirements,
    extras_require={
        'llm': llm_requirements,
        'dev': dev_requirements + llm_requirements,  # Dev includes LLM for testing
        'docs': docs_requirements,
        'all': llm_requirements + dev_requirements + docs_requirements
    },
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
    python_requires='>=3.8',
    license='MIT',
    zip_safe=False,  # This helps ensure all files are properly installed
)
