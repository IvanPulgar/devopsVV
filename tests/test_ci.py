"""
tests/test_ci.py
─────────────────────────────────────────────────────────────────────────────
Fase 4 – Validación del pipeline CI/CD
Verifica la estructura y correctitud de los archivos GitHub Actions.
─────────────────────────────────────────────────────────────────────────────
"""
import os
import re

import pytest
import yaml

# ── Helpers ───────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS_DIR = os.path.join(ROOT, ".github", "workflows")
CI_FILE = os.path.join(WORKFLOWS_DIR, "ci.yml")
PUBLISH_FILE = os.path.join(WORKFLOWS_DIR, "docker-publish.yml")


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Existencia de archivos
# ─────────────────────────────────────────────────────────────────────────────
class TestWorkflowExistence:
    def test_workflows_directory_exists(self):
        assert os.path.isdir(WORKFLOWS_DIR), ".github/workflows/ no encontrado"

    def test_ci_yml_exists(self):
        assert os.path.isfile(CI_FILE), ".github/workflows/ci.yml no encontrado"

    def test_docker_publish_yml_exists(self):
        assert os.path.isfile(PUBLISH_FILE), ".github/workflows/docker-publish.yml no encontrado"


# ─────────────────────────────────────────────────────────────────────────────
# 2. Validez YAML
# ─────────────────────────────────────────────────────────────────────────────
class TestYamlValidity:
    def test_ci_yml_is_valid_yaml(self):
        try:
            data = load_yaml(CI_FILE)
            assert isinstance(data, dict), "ci.yml debe ser un objeto YAML válido"
        except yaml.YAMLError as e:
            pytest.fail(f"ci.yml tiene YAML inválido: {e}")

    def test_docker_publish_yml_is_valid_yaml(self):
        try:
            data = load_yaml(PUBLISH_FILE)
            assert isinstance(data, dict)
        except yaml.YAMLError as e:
            pytest.fail(f"docker-publish.yml tiene YAML inválido: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Estructura del pipeline CI
# ─────────────────────────────────────────────────────────────────────────────
class TestCIPipelineStructure:
    @pytest.fixture(scope="class")
    def ci(self):
        return load_yaml(CI_FILE)

    def test_has_name(self, ci):
        assert "name" in ci, "ci.yml debe tener un nombre de workflow"
        assert ci["name"], "El nombre no puede estar vacío"

    def test_triggers_on_push(self, ci):
        # PyYAML parsea 'on' como boolean True
        on = ci.get(True, ci.get("on", {}))
        assert "push" in on, "El workflow debe dispararse en push"

    def test_triggers_on_pull_request(self, ci):
        on = ci.get(True, ci.get("on", {}))
        assert "pull_request" in on, "El workflow debe dispararse en pull_request"

    def test_triggers_on_main_branch(self, ci):
        on = ci.get(True, ci.get("on", {}))
        push_branches = on.get("push", {}).get("branches", [])
        assert "main" in push_branches, "El trigger push debe incluir la rama main"

    def test_has_jobs(self, ci):
        assert "jobs" in ci and ci["jobs"], "ci.yml debe definir al menos un job"

    def test_has_lint_job(self, ci):
        assert "lint" in ci["jobs"], "Debe existir un job de lint"

    def test_has_test_job(self, ci):
        assert "test" in ci["jobs"], "Debe existir un job de test"

    def test_has_docker_build_job(self, ci):
        assert "docker-build" in ci["jobs"], "Debe existir un job de docker-build"

    def test_lint_job_uses_ubuntu(self, ci):
        runs_on = ci["jobs"]["lint"].get("runs-on", "")
        assert "ubuntu" in runs_on, "El job lint debe ejecutarse en ubuntu"

    def test_test_job_uses_ubuntu(self, ci):
        runs_on = ci["jobs"]["test"].get("runs-on", "")
        assert "ubuntu" in runs_on

    def test_test_job_needs_lint(self, ci):
        needs = ci["jobs"]["test"].get("needs", [])
        if isinstance(needs, str):
            needs = [needs]
        assert "lint" in needs, "El job test debe depender del job lint"

    def test_docker_build_needs_test(self, ci):
        needs = ci["jobs"]["docker-build"].get("needs", [])
        if isinstance(needs, str):
            needs = [needs]
        assert "test" in needs, "docker-build debe depender del job test"

    def test_test_job_has_matrix(self, ci):
        strategy = ci["jobs"]["test"].get("strategy", {})
        matrix = strategy.get("matrix", {})
        assert "python-version" in matrix, "El job test debe tener matrix de python-version"

    def test_matrix_has_multiple_python_versions(self, ci):
        strategy = ci["jobs"]["test"].get("strategy", {})
        versions = strategy.get("matrix", {}).get("python-version", [])
        assert len(versions) >= 2, "La matrix debe probar al menos 2 versiones de Python"

    def test_test_job_runs_pytest(self, ci):
        steps = ci["jobs"]["test"].get("steps", [])
        step_contents = [str(s) for s in steps]
        all_content = " ".join(step_contents)
        assert "pytest" in all_content.lower(), "El job test debe ejecutar pytest"

    def test_lint_job_runs_flake8(self, ci):
        steps = ci["jobs"]["lint"].get("steps", [])
        all_content = " ".join(str(s) for s in steps)
        assert "flake8" in all_content.lower(), "El job lint debe ejecutar flake8"

    def test_docker_build_job_uses_buildx(self, ci):
        steps = ci["jobs"]["docker-build"].get("steps", [])
        uses_list = [s.get("uses", "") for s in steps if isinstance(s, dict)]
        assert any("buildx" in u for u in uses_list), \
            "docker-build debe usar docker/setup-buildx-action"

    def test_docker_build_job_builds_image(self, ci):
        steps = ci["jobs"]["docker-build"].get("steps", [])
        uses_list = [s.get("uses", "") for s in steps if isinstance(s, dict)]
        assert any("build-push-action" in u for u in uses_list), \
            "docker-build debe usar docker/build-push-action"

    def test_docker_build_job_verifies_health(self, ci):
        steps = ci["jobs"]["docker-build"].get("steps", [])
        all_content = " ".join(str(s) for s in steps)
        assert "health" in all_content.lower() or "healthcheck" in all_content.lower() or \
               "/api/health" in all_content, \
            "docker-build debe verificar el healthcheck del contenedor"

    def test_checkout_step_present_in_all_jobs(self, ci):
        for job_name, job in ci["jobs"].items():
            steps = job.get("steps", [])
            uses_list = [s.get("uses", "") for s in steps if isinstance(s, dict)]
            has_checkout = any("checkout" in u for u in uses_list)
            # Los jobs de summary pueden no tener checkout
            if job_name not in ("ci-summary",):
                assert has_checkout, f"Job '{job_name}' debe tener un paso de checkout"

    def test_uses_official_actions_versions(self, ci):
        """Todas las actions deben usar versiones fijadas (vX o vX.Y.Z)."""
        version_pattern = re.compile(r"@v\d+")
        for job_name, job in ci["jobs"].items():
            for step in job.get("steps", []):
                if isinstance(step, dict) and "uses" in step:
                    uses = step["uses"]
                    assert version_pattern.search(uses), \
                        f"Action '{uses}' en job '{job_name}' debe usar versión fijada (e.g. @v4)"

    def test_has_concurrency_control(self, ci):
        assert "concurrency" in ci, "ci.yml debe tener control de concurrencia"

    def test_concurrency_cancels_in_progress(self, ci):
        concurrency = ci.get("concurrency", {})
        assert concurrency.get("cancel-in-progress") is True, \
            "concurrency.cancel-in-progress debe ser true"

    def test_test_job_uploads_junit_results(self, ci):
        steps = ci["jobs"]["test"].get("steps", [])
        uses_list = [s.get("uses", "") for s in steps if isinstance(s, dict)]
        all_content = " ".join(str(s) for s in steps)
        has_upload = any("upload-artifact" in u for u in uses_list)
        has_junit = "junitxml" in all_content or "junit" in all_content.lower()
        assert has_upload and has_junit, \
            "El job test debe generar reportes JUnit y subirlos como artifact"

    def test_has_security_job(self, ci):
        assert "security" in ci["jobs"], "Debe existir un job de security scan"

    def test_has_ci_summary_job(self, ci):
        assert "ci-summary" in ci["jobs"], "Debe existir un job de resumen final"


# ─────────────────────────────────────────────────────────────────────────────
# 4. Estructura del workflow de publicación Docker
# ─────────────────────────────────────────────────────────────────────────────
class TestDockerPublishWorkflow:
    @pytest.fixture(scope="class")
    def pub(self):
        return load_yaml(PUBLISH_FILE)

    def test_has_name(self, pub):
        assert "name" in pub

    def test_triggers_on_version_tags(self, pub):
        on = pub.get(True, pub.get("on", {}))
        push = on.get("push", {})
        tags = push.get("tags", [])
        assert any("v" in str(t) for t in tags), \
            "El workflow de publicación debe dispararse en tags tipo v*.*.*"

    def test_has_publish_job(self, pub):
        jobs = pub.get("jobs", {})
        assert len(jobs) >= 1, "docker-publish.yml debe tener al menos un job"

    def test_uses_ghcr_registry(self, pub):
        content = str(pub)
        assert "ghcr.io" in content, "El workflow de publicación debe usar GHCR (ghcr.io)"

    def test_uses_github_token(self, pub):
        content = str(pub)
        assert "GITHUB_TOKEN" in content, "Debe autenticarse con secrets.GITHUB_TOKEN"

    def test_uses_metadata_action(self, pub):
        jobs = pub.get("jobs", {})
        for job in jobs.values():
            uses_list = [s.get("uses", "") for s in job.get("steps", [])
                         if isinstance(s, dict)]
            if any("metadata-action" in u for u in uses_list):
                return
        pytest.fail("docker-publish.yml debe usar docker/metadata-action")

    def test_uses_build_push_action(self, pub):
        jobs = pub.get("jobs", {})
        for job in jobs.values():
            uses_list = [s.get("uses", "") for s in job.get("steps", [])
                         if isinstance(s, dict)]
            if any("build-push-action" in u for u in uses_list):
                return
        pytest.fail("docker-publish.yml debe usar docker/build-push-action")

    def test_push_is_enabled(self, pub):
        jobs = pub.get("jobs", {})
        for job in jobs.values():
            for step in job.get("steps", []):
                if isinstance(step, dict) and "build-push-action" in step.get("uses", ""):
                    with_params = step.get("with", {})
                    assert with_params.get("push") is True, \
                        "build-push-action debe tener push: true en docker-publish.yml"
                    return
        pytest.fail("No se encontró build-push-action en docker-publish.yml")

    def test_has_write_packages_permission(self, pub):
        content = str(pub)
        assert "packages" in content and "write" in content, \
            "El job debe tener permiso write en packages para publicar en GHCR"


# ─────────────────────────────────────────────────────────────────────────────
# 5. Consistencia entre CI y el proyecto
# ─────────────────────────────────────────────────────────────────────────────
class TestCIProjectConsistency:
    @pytest.fixture(scope="class")
    def ci(self):
        return load_yaml(CI_FILE)

    def test_python_version_matches_requirements(self, ci):
        """La versión de Python en el CI debe estar en la lista de la matrix."""
        strategy = ci["jobs"]["test"].get("strategy", {})
        versions = strategy.get("matrix", {}).get("python-version", [])
        str_versions = [str(v) for v in versions]
        # Al menos debe incluir una versión 3.x
        assert any(v.startswith("3.") for v in str_versions), \
            "La matrix debe incluir al menos una versión Python 3.x"

    def test_ci_references_requirements_txt(self, ci):
        """El CI debe instalar dependencias desde requirements.txt."""
        jobs = ci.get("jobs", {})
        all_content = str(jobs)
        assert "requirements.txt" in all_content, \
            "El CI debe instalar desde requirements.txt"

    def test_ci_references_app_directory_for_lint(self, ci):
        """El job lint debe analizar el directorio app/."""
        steps = ci["jobs"]["lint"].get("steps", [])
        all_content = " ".join(str(s) for s in steps)
        assert "app/" in all_content, \
            "El job lint debe analizar app/"

    def test_flake8_config_file_exists(self):
        """Debe existir .flake8 para configurar el linter."""
        assert os.path.isfile(os.path.join(ROOT, ".flake8")), \
            ".flake8 debe existir para configurar flake8 en el CI"

    def test_dockerfile_exists_for_docker_build(self):
        """Debe existir Dockerfile para el job docker-build."""
        assert os.path.isfile(os.path.join(ROOT, "Dockerfile")), \
            "Dockerfile debe existir para el job docker-build"

    def test_ci_uses_gha_cache_for_docker(self, ci):
        """El job docker-build debe usar cache de GitHub Actions."""
        steps = ci["jobs"]["docker-build"].get("steps", [])
        all_content = " ".join(str(s) for s in steps)
        assert "gha" in all_content or "cache-from" in all_content, \
            "docker-build debe usar cache de GHA para acelerar builds"
