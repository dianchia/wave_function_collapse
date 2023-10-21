# WAVE FUNCTION COLLAPSE

This is a Python implementation of the Wave Function Collapse algorithm, as described by Maxim Gumin in [this article](http://gridbugs.org/wave-function-collapse/).

# INSTALLATION

## Recommended

Using poetry is recommended for development and testing this project. To install poetry, run the following command:

```bash
pip install poetry
```

To spawn a shell, navigate to the project directory and run:

```bash
poetry shell
```

## Demo only
If you only intend to use this project as a demo, the built distribution can be found in releases.
Download the built wheel file or tar.gz file, and install with the following command:
```bash
pip install <name of wheel>
```

# USAGE
Once you've installed the project, run the following command:
```bash
python -m wave_function_collapse
```

If interactive mode is needed (where it shows each tile being generated), run the following command:
```bash
python -m wave_function_collapse RUN.interactive=true
```