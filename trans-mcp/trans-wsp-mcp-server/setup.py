from setuptools import setup, find_packages

setup(
    name="trans-wsp-mcp-server",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=1.0.0",
        "flask>=2.0.0",
        "requests>=2.25.0"
    ],
    author="Trans Team",
    description="Wealth Management Query Service using MCP SDK",
    python_requires=">=3.8",
)