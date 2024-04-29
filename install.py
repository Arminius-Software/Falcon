import subprocess

# run this file once to install all the needed librarys for Falcon
# written in python 3.10

def install_libraries(lib_versions):
    for lib, version in lib_versions.items():
        try:
            subprocess.check_call(["pip", "install", f"{lib}=={version}"])
            print(f"Successfully installed {lib} version {version}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {lib} version {version}.")

def main():

    libraries_and_versions = {"pygame" : "2.5.2", "neat-python" : "0.92"}
    install_libraries(libraries_and_versions)


# make sure this is only run if the script itself is exectued not if this is called during an import

if __name__ == "__main__":
    main()