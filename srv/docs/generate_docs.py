import os
import subprocess
import shutil

# Correct PACKAGE_DIR to point to the root of your 'srv' package
PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # d:\\Fork\\on-time\\srv

# Correct DOCS_DIR to point to 'd:\\Fork\\on-time\\srv\\docs'
DOCS_DIR = os.path.join(PACKAGE_DIR, "srv", "docs")  # This will now point to 'd:\\Fork\\on-time\\srv\\docs'

SCRIPT_NAME = os.path.basename(__file__)

def clear_docs(directory):
    """Clear existing documentation files."""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file != SCRIPT_NAME:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

def setup_sphinx():
    """Set up the basic Sphinx configuration."""
    sphinx_dir = os.path.join(DOCS_DIR, "docs")

    if os.path.exists(sphinx_dir):
        shutil.rmtree(sphinx_dir)  # Clean up previous docs folder

    os.makedirs(sphinx_dir)  # Create the new docs folder

    # Run `sphinx-quickstart` to set up the Sphinx project
    subprocess.run(["sphinx-quickstart", sphinx_dir], check=True)

    # Ensure autodoc extension is enabled in conf.py (corrected to conf.py)
    conf_file = os.path.join(sphinx_dir, "conf.py")
    with open(conf_file, "a") as f:
        f.write("\n# Add autodoc extension\n")
        f.write("extensions = ['sphinx.ext.autodoc']\n")

    # Add the package to the Sphinx path so it can be imported
    with open(conf_file, "a") as f:
        f.write(f"\nimport sys\nsys.path.insert(0, '{PACKAGE_DIR}')\n")

    return sphinx_dir

def generate_docs(package_name, output_dir=DOCS_DIR):
    """Generate Sphinx-based documentation."""
    clear_docs(output_dir)

    # Setup Sphinx if it's not already done
    sphinx_dir = setup_sphinx()

    # Create a .rst file for the package (srv.rst)
    package_rst = os.path.join(sphinx_dir, f"{package_name}.rst")
    with open(package_rst, "w") as f:
        f.write(f"{package_name} package documentation\n")
        f.write("=" * (len(f"{package_name} package documentation") + 2) + "\n\n")
        f.write(f".. automodule:: {package_name}\n")
        f.write("   :members:\n")

    # Update index.rst to include the srv.rst file in the toctree (fixed)
    index_file = os.path.join(sphinx_dir, "index.rst")
    with open(index_file, "w") as f:
        f.write(f"Welcome to the documentation for {package_name}!\n")
        f.write("=" * (len(f"Welcome to the documentation for {package_name}!") + 2) + "\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 2\n")
        f.write(f"   {package_name}.rst\n\n")  # Fixed to point to {package_name}.rst without docutils

    # Now, run Sphinx to generate the HTML documentation
    subprocess.run(["sphinx-build", "-b", "html", sphinx_dir, os.path.join(output_dir, "build")], check=True)

    # Move the generated documentation to the target directory
    move_docs(os.path.join(output_dir, "build"))

def move_docs(output_dir):
    """Move generated documentation to output directory."""
    for file in os.listdir(output_dir):
        if file.endswith(".html"):
            shutil.move(os.path.join(output_dir, file), os.path.join(DOCS_DIR, file))

if __name__ == "__main__":
    package_name = "srv"  # Ensure that this package exists in the path
    generate_docs(package_name)
    print(f"Documentation generated in {DOCS_DIR}")
