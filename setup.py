from setuptools import setup, find_packages

setup(
    name="configure_dms_viz",
    version="0.1.0-beta.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "pandas"],
    entry_points={
        "console_scripts": [
            "configure-dms-viz = configure_dms_viz.configure_dms_viz:cli",
        ],
    },
)
