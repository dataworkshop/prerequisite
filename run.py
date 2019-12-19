from clint.textui import colored

from distutils.version import StrictVersion
import importlib
import argparse

packages = {
    "IPython": "4.0",
    "ipywidgets": "4.1.1",
    "pandas": "0.18",
    "numpy": "1.15",
    "matplotlib": "2.0",
    "seaborn": "0.7",
    "sklearn": "0.18",
    "xgboost": "0.7",
    "ml_metrics": "0.1.4",
	"hyperopt": "0.1",
    "hyperas": "0.4",
    "tensorflow": "1.12",
    "gensim": "3.4",
    "sqlalchemy": "1.2",
    "tqdm": "4.28",
    "xgbfir": "0.3",
    "graphviz": "0.8",
    "livelossplot": "0.3",
    "rfpimp": "1.3",
    "eli5": "0.8",
    "skimage": "0.13",
    "scikitplot": "0.3",
    "deepreplay": "0.1.1a2",
    "albumentations": "0.2",
    "clint": "0.5",
    "pandas_profiling": "1.4",
    "mpld3": "0.3",
    "modin": "0.6",
    "qgrid": "1.1",
    "imblearn": "0.5",
}


additional_visual_packages = {
    "gmplot": "1.1.1",
    "geoplotlib": "0.3.2",
    "folium": "0.2.1",
    "vincent": "0.4.4",
    "geopandas": "0.2.1",
    "mpl_toolkits.basemap": "1.0.7"
}

def verify_packages(packages):
    missing_packages = []
    upgrade_packages = []

    for package_name, package_version in packages.items():
        current_version = get_version_package(package_name)

        if False == current_version:
            print(colored.red("{0} - missing".format(package_name)))
            missing_packages.append(package_name)
        elif current_version is None:
            handle_package_without_version(current_version, package_version, package_name)
        else:
            if version_is_good(current_version, package_version):
                print(colored.green("{0}-{1} - OK".format(package_name, current_version)))
            else:
                print(colored.yellow("{0}-{1} should be upgraded to {0}-{2}".format(package_name, current_version, package_version)))
                upgrade_packages.append(package_name)

    return missing_packages, upgrade_packages

def handle_package_without_version(current_version, package_version, package_name):
    if current_version != package_version:
        print(colored.yellow("{0} exists, but has no attribute version. Expected version {1}".format(package_name, package_version)))
    else:
        print(colored.green("{0} - OK".format(package_name)))

def get_version_package(package_name):
    try:
        return importlib.import_module(package_name).__version__
    except ImportError:
        return False
    except AttributeError:
        return None

def version_is_good(actual_version, expected_version):
    return StrictVersion(actual_version) >= StrictVersion(expected_version)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prerequisite')
    parser.add_argument('--extra_visual', '-ev', action='store_true')
    args = parser.parse_args()

    if args.extra_visual:
        packages.update(additional_visual_packages)

    missing_packages, upgrade_packages = verify_packages(packages)

    if not missing_packages and not upgrade_packages:
        print("")
        print(colored.green("=" * 50))
        print(colored.green("All right, you are ready to go on DataWorkshop!"))

    if missing_packages:
        print("")
        print(colored.red("=" * 50))
        print(colored.red("REQUIRED"))
        print(colored.red("Please install those packages before DataWorkshop: " + ", ".join(missing_packages)))
        print(colored.blue("pip install {0}".format( " ".join(missing_packages) )))
        if 'xgboost' in missing_packages:
            print(colored.red("More info how to install xgboost: ") + colored.blue("http://xgboost.readthedocs.org/en/latest/build.html"))


    if upgrade_packages:
        print("")
        print(colored.yellow("=" * 50))
        print(colored.yellow("RECOMMENDATION (without upgrade some needed features could be missing)"))
        print(colored.blue("pip install --upgrade {0}".format( " ".join(upgrade_packages) )))
