"""
tests/test_scripts.py
─────────────────────────────────────────────────────────────────────────────
Fase 3 – Validación de scripts de automatización
Verifica existencia, estructura y ejecución de los scripts Bash y PowerShell.
─────────────────────────────────────────────────────────────────────────────
"""
import os
import subprocess
import sys

import pytest

# ── Helpers ───────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")


def script_path(name: str) -> str:
    return os.path.join(SCRIPTS, name)


def read_script(name: str) -> str:
    with open(script_path(name), "r", encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Existencia de archivos
# ─────────────────────────────────────────────────────────────────────────────
BASH_SCRIPTS = ["install.sh", "run.sh", "test.sh", "healthcheck.sh", "lint.sh"]
PS1_SCRIPTS  = ["install.ps1", "run.ps1", "test.ps1", "healthcheck.ps1", "lint.ps1"]
CONFIG_FILES = [".flake8", ".gitignore"]


class TestScriptExistence:
    @pytest.mark.parametrize("name", BASH_SCRIPTS)
    def test_bash_script_exists(self, name):
        assert os.path.isfile(script_path(name)), f"No encontrado: scripts/{name}"

    @pytest.mark.parametrize("name", PS1_SCRIPTS)
    def test_ps1_script_exists(self, name):
        assert os.path.isfile(script_path(name)), f"No encontrado: scripts/{name}"

    @pytest.mark.parametrize("name", CONFIG_FILES)
    def test_config_file_exists(self, name):
        path = os.path.join(ROOT, name)
        assert os.path.isfile(path), f"No encontrado: {name}"


# ─────────────────────────────────────────────────────────────────────────────
# 2. Estructura de scripts Bash
# ─────────────────────────────────────────────────────────────────────────────
class TestBashScriptStructure:
    def test_install_sh_has_shebang(self):
        content = read_script("install.sh")
        assert content.startswith("#!/usr/bin/env bash"), "install.sh debe iniciar con shebang"

    def test_install_sh_has_pipefail(self):
        assert "set -euo pipefail" in read_script("install.sh")

    def test_install_sh_creates_venv(self):
        content = read_script("install.sh")
        assert ".venv" in content

    def test_install_sh_uses_pip(self):
        content = read_script("install.sh")
        assert "pip install" in content
        assert "requirements.txt" in content

    def test_run_sh_has_shebang(self):
        content = read_script("run.sh")
        assert content.startswith("#!/usr/bin/env bash")

    def test_run_sh_has_pipefail(self):
        assert "set -euo pipefail" in read_script("run.sh")

    def test_run_sh_validates_env_arg(self):
        content = read_script("run.sh")
        assert "dev|test|prod" in content or "(dev|test|prod)" in content

    def test_run_sh_loads_env_file(self):
        content = read_script("run.sh")
        assert "source" in content
        assert ".env." in content

    def test_run_sh_calls_python(self):
        content = read_script("run.sh")
        assert "python3 run.py" in content or "python run.py" in content

    def test_test_sh_has_shebang(self):
        assert read_script("test.sh").startswith("#!/usr/bin/env bash")

    def test_test_sh_has_pipefail(self):
        assert "set -euo pipefail" in read_script("test.sh")

    def test_test_sh_sets_app_env_test(self):
        content = read_script("test.sh")
        assert "APP_ENV=test" in content

    def test_test_sh_sets_database_path(self):
        assert "DATABASE_PATH" in read_script("test.sh")

    def test_test_sh_runs_pytest(self):
        content = read_script("test.sh")
        assert "pytest" in content

    def test_test_sh_has_cleanup(self):
        content = read_script("test.sh")
        assert "trap" in content or "rm -f" in content

    def test_healthcheck_sh_has_shebang(self):
        assert read_script("healthcheck.sh").startswith("#!/usr/bin/env bash")

    def test_healthcheck_sh_uses_curl_or_retry(self):
        content = read_script("healthcheck.sh")
        assert "curl" in content or "retry" in content.lower()

    def test_healthcheck_sh_checks_api_health(self):
        assert "/api/health" in read_script("healthcheck.sh")

    def test_healthcheck_sh_has_max_retries_logic(self):
        content = read_script("healthcheck.sh")
        assert "MAX_RETRIES" in content or "max_retries" in content.lower()

    def test_lint_sh_has_shebang(self):
        assert read_script("lint.sh").startswith("#!/usr/bin/env bash")

    def test_lint_sh_has_pipefail(self):
        assert "set -euo pipefail" in read_script("lint.sh")

    def test_lint_sh_runs_flake8(self):
        assert "flake8" in read_script("lint.sh")

    def test_lint_sh_targets_app_directory(self):
        assert "app/" in read_script("lint.sh")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Estructura de scripts PowerShell
# ─────────────────────────────────────────────────────────────────────────────
class TestPowershellScriptStructure:
    def test_install_ps1_has_error_action_stop(self):
        content = read_script("install.ps1")
        assert 'ErrorActionPreference' in content and 'Stop' in content

    def test_install_ps1_creates_venv(self):
        assert ".venv" in read_script("install.ps1")

    def test_install_ps1_uses_pip(self):
        content = read_script("install.ps1")
        assert "pip install" in content
        assert "requirements.txt" in content

    def test_run_ps1_has_env_parameter(self):
        content = read_script("run.ps1")
        # Debe aceptar param $Env
        assert "param" in content.lower()
        assert "$Env" in content or "$env" in content

    def test_run_ps1_validates_env_values(self):
        content = read_script("run.ps1")
        assert "dev" in content and "test" in content and "prod" in content

    def test_run_ps1_loads_env_file(self):
        content = read_script("run.ps1")
        assert ".env." in content

    def test_run_ps1_calls_python(self):
        assert "run.py" in read_script("run.ps1")

    def test_test_ps1_accepts_extra_args(self):
        content = read_script("test.ps1")
        assert "ExtraArgs" in content or "RemainingArguments" in content

    def test_test_ps1_sets_app_env_test(self):
        content = read_script("test.ps1")
        assert 'APP_ENV' in content and '"test"' in content or "'test'" in content

    def test_test_ps1_runs_pytest(self):
        assert "pytest" in read_script("test.ps1")

    def test_test_ps1_exits_with_code(self):
        content = read_script("test.ps1")
        assert "exit $exitCode" in content or "exit $LASTEXITCODE" in content

    def test_healthcheck_ps1_has_hostname_param(self):
        content = read_script("healthcheck.ps1")
        assert "HostName" in content or "hostname" in content.lower()

    def test_healthcheck_ps1_has_port_param(self):
        assert "Port" in read_script("healthcheck.ps1")

    def test_healthcheck_ps1_checks_api_health(self):
        assert "/api/health" in read_script("healthcheck.ps1")

    def test_healthcheck_ps1_has_retry_loop(self):
        content = read_script("healthcheck.ps1")
        assert "MaxRetries" in content or "MaxRetries" in content
        assert "for" in content or "while" in content

    def test_lint_ps1_runs_flake8(self):
        assert "flake8" in read_script("lint.ps1")

    def test_lint_ps1_targets_app_directory(self):
        assert "app/" in read_script("lint.ps1") or "app\\" in read_script("lint.ps1")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Estructura de archivos de configuración
# ─────────────────────────────────────────────────────────────────────────────
class TestConfigFiles:
    def _read(self, name):
        with open(os.path.join(ROOT, name), "r", encoding="utf-8") as f:
            return f.read()

    def test_flake8_has_flake8_section(self):
        assert "[flake8]" in self._read(".flake8")

    def test_flake8_has_max_line_length(self):
        content = self._read(".flake8")
        assert "max-line-length" in content

    def test_flake8_max_line_length_value(self):
        content = self._read(".flake8")
        # Acepta valores entre 79 y 200
        import re
        match = re.search(r"max-line-length\s*=\s*(\d+)", content)
        assert match, "max-line-length debe tener valor numérico"
        assert 79 <= int(match.group(1)) <= 200

    def test_flake8_has_exclude(self):
        assert "exclude" in self._read(".flake8")

    def test_flake8_excludes_venv(self):
        assert ".venv" in self._read(".flake8")

    def test_gitignore_ignores_venv(self):
        content = self._read(".gitignore")
        assert ".venv" in content or ".venv/" in content

    def test_gitignore_ignores_pycache(self):
        content = self._read(".gitignore")
        assert "__pycache__" in content

    def test_gitignore_ignores_pyc(self):
        assert ".pyc" in self._read(".gitignore")

    def test_gitignore_ignores_db_files(self):
        content = self._read(".gitignore")
        assert "*.db" in content or "*.sqlite" in content


# ─────────────────────────────────────────────────────────────────────────────
# 5. Ejecución real de scripts (solo Windows, solo cuando powershell disponible)
# ─────────────────────────────────────────────────────────────────────────────
def _powershell_available():
    try:
        result = subprocess.run(
            ["powershell", "-Command", "echo ok"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


@pytest.mark.skipif(
    sys.platform != "win32" or not _powershell_available(),
    reason="PowerShell requerido (solo Windows)"
)
class TestScriptExecution:
    def _run_ps1(self, script_name, extra_args=None, timeout=120):
        """Ejecuta un script PowerShell y devuelve CompletedProcess."""
        cmd = [
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", script_path(script_name)
        ]
        if extra_args:
            cmd.extend(extra_args)
        return subprocess.run(
            cmd, capture_output=True, text=True, cwd=ROOT, timeout=timeout
        )

    def test_lint_ps1_passes_on_codebase(self):
        """flake8 debe salir con código 0 sobre el código del proyecto."""
        result = self._run_ps1("lint.ps1", timeout=60)
        assert result.returncode == 0, (
            f"lint.ps1 devolvió {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    def test_test_ps1_runs_suite_without_recursion(self):
        """test.ps1 debe ejecutar las suites de api e infra sin recursión."""
        result = self._run_ps1(
            "test.ps1",
            extra_args=["tests/test_tasks.py", "tests/test_infra.py"],
            timeout=120
        )
        assert result.returncode == 0, (
            f"test.ps1 devolvió {result.returncode}\n"
            f"STDOUT:\n{result.stdout[-2000:]}\n"
            f"STDERR:\n{result.stderr[-1000:]}"
        )

    def test_healthcheck_ps1_fails_gracefully_on_no_server(self):
        """healthcheck.ps1 debe salir con código != 0 si no hay servidor."""
        result = self._run_ps1(
            "healthcheck.ps1",
            extra_args=["localhost", "19999", "1"],
            timeout=30
        )
        assert result.returncode != 0, (
            "healthcheck.ps1 debería fallar cuando no hay servidor en el puerto 19999"
        )
