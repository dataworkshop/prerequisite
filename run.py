from clint.textui import colored

from distutils.version import StrictVersion
import importlib

packages = {
    "IPython": "4.0",
    "pandas": "0.18",
    "numpy": "1.10",
    "matplotlib": "1.5",
    "seaborn": "0.7",
    "sklearn": "0.17",
    "xgboost": "0.4"
}

def verify_packages(packages):
    missing_packages = []
    upgrade_packages = []

    for package_name, package_version in packages.items():
        current_version = get_version_package(package_name)
        if False == current_version:
            print(colored.red("{0} - missing".format(package_name)))
            missing_packages.append(package_name)
        else:
            if version_is_good(current_version, package_version):
                print(colored.green("{0}-{1} - OK".format(package_name, current_version)))
            else:
                print(colored.yellow("{0}-{1} should be upgraded to {0}-{2}".format(package_name, current_version, package_version)))
                upgrade_packages.append(package_name)

    return missing_packages, upgrade_packages

def get_version_package(package_name):
    try:
        return importlib.import_module(package_name).__version__
    except ImportError:
        return False

def version_is_good(actual_version, expected_version):
    return StrictVersion(actual_version) >= StrictVersion(expected_version)

if __name__ == '__main__':
    missing_packages, upgrade_packages = verify_packages(packages)


    if not missing_packages and not upgrade_packages:
        print("")
        print(colored.green("=" * 50))
        print(colored.green("All right, you are ready to go on Data Workshop!"))

    if missing_packages:
        print("")
        print(colored.red("=" * 50))
        print(colored.red("REQUIRED"))
        print(colored.red("Please install those packages before Data Workshop: " + ", ".join(missing_packages)))
        print(colored.blue("pip install {0}".format( " ".join(missing_packages) )))
        if 'xgboost' in missing_packages:
            print(colored.red("More info how to install xgboost: ") + colored.blue("http://xgboost.readthedocs.org/en/latest/build.html"))


    if upgrade_packages:
        print("")
        print(colored.yellow("=" * 50))
        print(colored.yellow("RECOMENDATION (without upgrade some needed features could be missing)"))
        print(colored.blue("pip install --upgrade {0}".format( " ".join(upgrade_packages) )))
