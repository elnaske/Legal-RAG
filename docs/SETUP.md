# PROJECT SETUP
- - - 

1. [Installing uv](#installing-uv)
2. [Syncing project dependencies](#syncing-project-dependencies)
3. [Running files with uv](#running-files-with-uv)
- - - 

### Installing uv

*Incase you're wondering, uv is a fast tool that's meant to be an all in one for pip, virtualenv, etc...*

 - To get setup with the project dependencies, first thing is to make sure [uv](https://docs.astral.sh/uv/) is installed on your device:

**Linux & Mac OS**

From the **terminal**:
 - Use curl to download the script and execute it with sh:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
 - If for some reason you don't have `curl`, use `wget`

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

**Windows**

From **PowerShell:**

 - Use `irm` to download the script and execute it with `iex`:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#####  Verify UV installation

 - To verify you've installed it correctly, from your Terminal (or PowerShell), run:
```
uv --version
```
 - You should be returned a version of UV

- - - 
### Syncing project dependencies

#### Notes on UV:

 - UV generates a few different files that contain information about the project
     - `pyproject.toml`: Where dependencies and metadata are set
         - You also can see the python version in here under `[project]` in `requires-python`
         - The main project name is set here too in `name`
         ```toml
         [project]
         name = "Legal-RAG"
         version = "0.1.0" # version of our app, ignore
         requires-python = ">=3.9" # Just an example version
         ```
         - Also if we want to go CLI route, we can set the CLI name in `[projects.scripts]`:
         ```toml
        [project.scripts]
        Legal-RAG = "Legal-RAG:main" # may need to adjust in our project
         ```
         - Then from the console we could run
         ```bash
         uv run Legal-RAG
         ```
     - `uv.lock`: *lockfile*; file that contains and controls project metadata from `pyproject.toml` 
      - `.venv/`: Where the virtual environment is set
- - -

#### Project Sync:


**Creating the lockfile**
 - To explicitly update the lockfile (which is usually done automatically), run:
 ```bash
uv lock
 ```

**Syncing the environment**
 - Run this the first time you setup the project or after dependencies are modified
 - Syncing the environment is useful to ensure you're running the correct versions of the dependencies
 ```bash
uv sync
 ```

**Adding dependencies**
 - If you want or need to add or update a dependency, run the following
 ```bash
# uv add <whatever dependency you're adding>
# e.g.
uv add numpy
 ```
 - Doing add with automatically update the `pyproject.toml` and `uv.lock` files
 - It will also automatically run `uv sync`

**Updating/upgrading dependencies**
 - If a dependency needs to be upgraded, run:
 ```bash
# uv sync --upgrade-package <whatever dependency>
# e.g.
uv sync --upgrade-package numpy
 ```

**Ensuring your IDE sees dependencies**
 - You'll need to select the `.venv` as the interpreter for your IDE to know the dependencies you have. The `pyrightconfig.json` is for this for IDEs like Nvim. Ideally this isn't something your should have to worry about.
- - - 
#### Running files with uv:

 - If you're using VScode, your IDE should just pick up on the venv from uv. So, feel free to skip the section below if you have no issues
 - - -
 ##### Running from command line
 - To run files with uv, it's important to use the following command:
```bash
# uv run python directory/module
# e.g. from project root
uv run python src/main.py
# or
uv run src/main.py

# or you could run an individual file directly like:
cd src/ingestion
# from src/ingestion
uv run python gather.py
```
- If it's decided we want to run these as modules, which has benefits for setting up scripts and using stuff like `pytest`, we can run with the following instead:
     - *Note:* we would just need to adjust some imports for this. If we do this without fulling committing though, we can run into that *"can't find directory 'x"* error
```bash
# uv run python -m directory.module
# e.g. from project root
uv run python -m src.main
# or
uv run src.main
- - - 
# notice how -m (module) expects no file type. 
# Whereas if you just do python <file>, the .py is expected.
```
- - -