from setuptools import find_packages, setup

setup(
    name='netbox-project-quota',
    version='1.0.0',
    description='Netbox Plugin for Manage Project',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'netbox_project_quota': ['templates/*'],
    },
    zip_safe=False,
    entry_points={
        'netbox_plugins': [
            'netbox_project_quota = netbox_project_quota:Plugin',
        ],
    },
)