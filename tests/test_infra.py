"""
Fase 2 – Validaciones de infraestructura y configuración de ambientes.
Estos tests NO requieren Docker corriendo; validan la corrección
de todos los artefactos de configuración generados en la Fase 2.
"""
import os
import re
import pytest
import yaml


# ── Fixtures de rutas ─────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def file_path(*parts):
    return os.path.join(ROOT, *parts)


def read(path):
    with open(file_path(path), encoding='utf-8') as f:
        return f.read()


# ── .env por ambiente ─────────────────────────────────────────────────────────

class TestEnvFiles:
    REQUIRED_KEYS = ['APP_ENV', 'DEBUG', 'PORT', 'HOST', 'DATABASE_PATH']

    @pytest.mark.parametrize("env_file,expected_env,expected_debug", [
        ('.env.dev',  'development', 'true'),
        ('.env.test', 'test',        'false'),
        ('.env.prod', 'production',  'false'),
    ])
    def test_env_file_exists(self, env_file, expected_env, expected_debug):
        assert os.path.isfile(file_path(env_file)), f"{env_file} no encontrado"

    @pytest.mark.parametrize("env_file,expected_env,expected_debug", [
        ('.env.dev',  'development', 'true'),
        ('.env.test', 'test',        'false'),
        ('.env.prod', 'production',  'false'),
    ])
    def test_env_file_has_required_keys(self, env_file, expected_env, expected_debug):
        content = read(env_file)
        for key in self.REQUIRED_KEYS:
            assert key in content, f"{key} no está en {env_file}"

    @pytest.mark.parametrize("env_file,expected_env,expected_debug", [
        ('.env.dev',  'development', 'true'),
        ('.env.test', 'test',        'false'),
        ('.env.prod', 'production',  'false'),
    ])
    def test_env_file_correct_values(self, env_file, expected_env, expected_debug):
        content = read(env_file)
        assert f"APP_ENV={expected_env}" in content
        assert f"DEBUG={expected_debug}" in content

    def test_prod_debug_is_false(self):
        assert "DEBUG=false" in read('.env.prod')

    def test_test_debug_is_false(self):
        assert "DEBUG=false" in read('.env.test')

    def test_dev_debug_is_true(self):
        assert "DEBUG=true" in read('.env.dev')

    def test_database_paths_are_distinct(self):
        """Cada ambiente debe usar una BD distinta para aislamiento."""
        def get_db_path(env_file):
            for line in read(env_file).splitlines():
                if line.startswith('DATABASE_PATH='):
                    return line.split('=', 1)[1].strip()
            return None

        paths = {get_db_path(f) for f in ['.env.dev', '.env.test', '.env.prod']}
        assert None not in paths, "Algún .env no tiene DATABASE_PATH"
        assert len(paths) == 3, "Los ambientes comparten DATABASE_PATH (deben ser distintos)"


# ── Dockerfile ────────────────────────────────────────────────────────────────

class TestDockerfile:
    def test_dockerfile_exists(self):
        assert os.path.isfile(file_path('Dockerfile'))

    def test_uses_slim_python_image(self):
        assert 'python:3.13-slim' in read('Dockerfile')

    def test_has_multi_stage_build(self):
        content = read('Dockerfile')
        stages = re.findall(r'^FROM\s+\S+\s+AS\s+(\w+)', content, re.MULTILINE)
        assert len(stages) >= 2, "Se esperan al menos 2 stages (builder + runtime)"
        assert 'builder' in stages
        assert 'runtime' in stages

    def test_exposes_port_5000(self):
        assert 'EXPOSE 5000' in read('Dockerfile')

    def test_has_healthcheck(self):
        assert 'HEALTHCHECK' in read('Dockerfile')

    def test_runs_as_non_root_user(self):
        content = read('Dockerfile')
        assert 'USER appuser' in content, "La imagen debe correr como usuario sin privilegios"

    def test_creates_data_directory(self):
        assert '/data' in read('Dockerfile')

    def test_copies_requirements_before_code(self):
        """requirements.txt debe copiarse antes que el código para cache eficiente."""
        content = read('Dockerfile')
        req_pos  = content.find('requirements.txt')
        code_pos = content.find('COPY app/')
        assert req_pos < code_pos, \
            "requirements.txt debe copiarse antes que el código fuente"


# ── docker-compose.yml ────────────────────────────────────────────────────────

class TestDockerCompose:
    @pytest.fixture(autouse=True)
    def load_compose(self):
        with open(file_path('docker-compose.yml'), encoding='utf-8') as f:
            self.compose = yaml.safe_load(f)

    def test_compose_file_exists(self):
        assert os.path.isfile(file_path('docker-compose.yml'))

    def test_has_three_app_services(self):
        services = self.compose.get('services', {})
        app_services = [s for s in services if s.startswith('app_')]
        assert len(app_services) == 3, "Se esperan 3 servicios app (dev, test, prod)"

    def test_has_nginx_service(self):
        assert 'nginx' in self.compose.get('services', {})

    def test_services_have_profiles(self):
        services = self.compose.get('services', {})
        for name, svc in services.items():
            assert 'profiles' in svc, f"Servicio '{name}' no tiene 'profiles'"

    def test_dev_profile_exists(self):
        services = self.compose.get('services', {})
        profiles = [p for svc in services.values() for p in svc.get('profiles', [])]
        assert 'dev'  in profiles
        assert 'test' in profiles
        assert 'prod' in profiles

    def test_app_dev_has_bind_mount_for_hot_reload(self):
        volumes = self.compose['services']['app_dev'].get('volumes', [])
        bind_mounts = [v for v in volumes if isinstance(v, str) and './app' in v]
        assert len(bind_mounts) > 0, "app_dev debe tener bind-mount de ./app para hot-reload"

    def test_app_prod_has_no_direct_port_mapping(self):
        """En prod, el puerto no debe estar expuesto directamente; usa Nginx."""
        prod_svc = self.compose['services']['app_prod']
        assert 'ports' not in prod_svc, \
            "app_prod no debe exponer puertos directamente (debe ir por Nginx)"

    def test_nginx_listens_on_port_80(self):
        nginx_ports = self.compose['services']['nginx'].get('ports', [])
        assert any('80:80' in str(p) for p in nginx_ports)

    def test_nginx_depends_on_app_prod(self):
        depends = self.compose['services']['nginx'].get('depends_on', {})
        assert 'app_prod' in depends

    def test_all_services_have_healthcheck(self):
        services = self.compose.get('services', {})
        for name, svc in services.items():
            assert 'healthcheck' in svc, f"Servicio '{name}' no tiene healthcheck"

    def test_has_named_volumes(self):
        volumes = self.compose.get('volumes', {})
        assert 'data_dev'  in volumes
        assert 'data_test' in volumes
        assert 'data_prod' in volumes

    def test_all_services_share_network(self):
        services = self.compose.get('services', {})
        for name, svc in services.items():
            nets = svc.get('networks', [])
            assert 'tasknet' in nets, f"Servicio '{name}' no está en la red 'tasknet'"

    def test_prod_restart_policy_is_always(self):
        assert self.compose['services']['app_prod']['restart'] == 'always'

    def test_test_restart_policy_is_no(self):
        assert self.compose['services']['app_test']['restart'] == 'no'


# ── Nginx config ──────────────────────────────────────────────────────────────

class TestNginxConfig:
    def test_nginx_conf_exists(self):
        assert os.path.isfile(file_path('infra', 'nginx', 'nginx.conf'))

    def test_vhost_conf_exists(self):
        assert os.path.isfile(file_path('infra', 'nginx', 'conf.d', 'taskmanager.conf'))

    def test_nginx_conf_includes_conf_d(self):
        assert 'conf.d' in read('infra/nginx/nginx.conf')

    def test_vhost_proxies_to_app_prod(self):
        assert 'app_prod:5000' in read('infra/nginx/conf.d/taskmanager.conf')

    def test_vhost_listens_on_port_80(self):
        assert 'listen 80' in read('infra/nginx/conf.d/taskmanager.conf')

    def test_vhost_sets_real_ip_header(self):
        assert 'X-Real-IP' in read('infra/nginx/conf.d/taskmanager.conf')

    def test_vhost_has_security_headers(self):
        content = read('infra/nginx/conf.d/taskmanager.conf')
        assert 'X-Frame-Options'        in content
        assert 'X-Content-Type-Options' in content
        assert 'X-XSS-Protection'       in content

    def test_vhost_blocks_hidden_files(self):
        assert r'/\.' in read('infra/nginx/conf.d/taskmanager.conf')

    def test_server_tokens_off(self):
        assert 'server_tokens   off' in read('infra/nginx/nginx.conf')

    def test_health_check_route_has_access_log_off(self):
        content = read('infra/nginx/conf.d/taskmanager.conf')
        # Verifica que la sección /api/health tenga access_log off
        health_block_match = re.search(
            r'location /api/health\s*\{[^}]*access_log\s+off', content, re.DOTALL)
        assert health_block_match, "/api/health debe tener access_log off"


# ── .dockerignore ─────────────────────────────────────────────────────────────

class TestDockerIgnore:
    def test_dockerignore_exists(self):
        assert os.path.isfile(file_path('.dockerignore'))

    def test_excludes_tests(self):
        assert 'tests/' in read('.dockerignore')

    def test_excludes_pycache(self):
        assert '__pycache__' in read('.dockerignore')

    def test_excludes_local_db(self):
        assert '*.db' in read('.dockerignore')

    def test_excludes_git_folder(self):
        assert '.git' in read('.dockerignore')
