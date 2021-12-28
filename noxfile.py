# Standard Library
import uuid
from pathlib import Path
from typing import Dict
from typing import List

# Third Party Library
import nox

python_code_path_list: List[str] = [
    f"{Path(__file__).parent / 'app'}",
    "noxfile.py",
]
env_common: Dict[str, str] = {
    "PYTHONPATH": f"{Path(__file__).parent}",
}
nox_tmp_dir: Path = Path(__file__).parent / ".nox_tmp"
python_version_list: List[str] = ["3.10"]


def install_package(session: nox.sessions.Session, dev: bool = False):
    requirements_txt_path: Path = nox_tmp_dir / f"poetry-requirements-{str(uuid.uuid4())}.txt"
    requirements_txt_path.parent.mkdir(exist_ok=True, parents=True)
    try:
        cmd = [
            "poetry",
            "export",
            "--format",
            "requirements.txt",
            "--output",
            f"{requirements_txt_path}",
        ] + (["--dev"] if dev else [])
        session.run(*cmd, external=True)
        session.install("-r", f"{requirements_txt_path}")
    finally:
        requirements_txt_path.unlink(missing_ok=True)


@nox.session(python=python_version_list)
def test(session):
    env: Dict[str, str] = {}
    env.update(env_common)

    install_package(session, dev=True)
    session.run("pytest", env=env)


@nox.session(python=python_version_list)
def lint(session):
    env: Dict[str, str] = {}
    env.update(env_common)

    install_package(session, dev=True)
    session.run("flake8", "--statistics", "--count", "--show-source", *python_code_path_list, env=env)
    session.run("autoflake8", "--check", "--recursive", "--remove-unused-variables", *python_code_path_list, env=env)
    session.run("isort", "--check", *python_code_path_list, env=env)
    session.run("black", "--check", *python_code_path_list, env=env)
    session.run("mypy", "--check", *python_code_path_list, env=env)


@nox.session(python=python_version_list)
def format(session):
    env: Dict[str, str] = {}
    env.update(env_common)

    install_package(session, dev=True)
    session.run(
        "autoflake8",
        "--in-place",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
        "--exit-zero-even-if-changed",
        *python_code_path_list,
        env=env,
    )
    session.run("isort", *python_code_path_list, env=env)
    session.run("black", *python_code_path_list, env=env)
