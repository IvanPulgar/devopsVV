# Comandos para la Ejecución de las 245 Pruebas
## Task Manager — DevOps + V&V

**Nota sobre los comandos:**
- **Windows (local):** usar `py -m pytest`
- **GitHub Codespaces (Linux):** usar `python -m pytest`
- Cada comando puede copiarse y pegarse directamente en la terminal

---

## PREPARACIÓN

### Windows (local)
```cmd
cd c:\Users\Hp\Desktop\devopsVV
.venv\Scripts\activate
```

### GitHub Codespaces
```bash
cd /workspaces/devopsVV
pip install -r requirements.txt
```

---

## COMANDO GLOBAL — Ejecutar las 245 pruebas de una sola vez

### Windows
```cmd
py -m pytest tests/ -v
```

### Codespaces
```bash
python -m pytest tests/ -v
```

---

---

# GRUPO 1 — test_ci.py (46 pruebas)
## Pipeline CI/CD

### Ejecutar el grupo completo

**Windows:**
```cmd
py -m pytest tests/test_ci.py -v
```
**Codespaces:**
```bash
python -m pytest tests/test_ci.py -v
```

---

### Subgrupo: TestWorkflowExistence (3 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_ci.py::TestWorkflowExistence::test_workflows_directory_exists" -v
py -m pytest "tests/test_ci.py::TestWorkflowExistence::test_ci_yml_exists" -v
py -m pytest "tests/test_ci.py::TestWorkflowExistence::test_docker_publish_yml_exists" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_ci.py::TestWorkflowExistence::test_workflows_directory_exists" -v
python -m pytest "tests/test_ci.py::TestWorkflowExistence::test_ci_yml_exists" -v
python -m pytest "tests/test_ci.py::TestWorkflowExistence::test_docker_publish_yml_exists" -v
```

---

### Subgrupo: TestYamlValidity (2 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_ci.py::TestYamlValidity::test_ci_yml_is_valid_yaml" -v
py -m pytest "tests/test_ci.py::TestYamlValidity::test_docker_publish_yml_is_valid_yaml" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_ci.py::TestYamlValidity::test_ci_yml_is_valid_yaml" -v
python -m pytest "tests/test_ci.py::TestYamlValidity::test_docker_publish_yml_is_valid_yaml" -v
```

---

### Subgrupo: TestCIPipelineStructure (26 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_name" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_triggers_on_push" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_triggers_on_pull_request" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_triggers_on_main_branch" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_jobs" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_lint_job" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_test_job" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_docker_build_job" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_lint_job_uses_ubuntu" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_uses_ubuntu" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_needs_lint" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_needs_test" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_has_matrix" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_matrix_has_multiple_python_versions" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_runs_pytest" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_lint_job_runs_flake8" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_job_uses_buildx" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_job_builds_image" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_job_verifies_health" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_checkout_step_present_in_all_jobs" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_uses_official_actions_versions" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_concurrency_control" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_concurrency_cancels_in_progress" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_uploads_junit_results" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_security_job" -v
py -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_ci_summary_job" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_name" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_triggers_on_push" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_triggers_on_pull_request" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_triggers_on_main_branch" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_jobs" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_lint_job" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_test_job" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_docker_build_job" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_lint_job_uses_ubuntu" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_uses_ubuntu" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_needs_lint" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_needs_test" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_has_matrix" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_matrix_has_multiple_python_versions" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_runs_pytest" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_lint_job_runs_flake8" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_job_uses_buildx" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_job_builds_image" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_docker_build_job_verifies_health" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_checkout_step_present_in_all_jobs" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_uses_official_actions_versions" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_concurrency_control" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_concurrency_cancels_in_progress" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_test_job_uploads_junit_results" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_security_job" -v
python -m pytest "tests/test_ci.py::TestCIPipelineStructure::test_has_ci_summary_job" -v
```

---

### Subgrupo: TestDockerPublishWorkflow (9 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_has_name" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_triggers_on_version_tags" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_has_publish_job" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_ghcr_registry" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_github_token" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_metadata_action" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_build_push_action" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_push_is_enabled" -v
py -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_has_write_packages_permission" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_has_name" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_triggers_on_version_tags" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_has_publish_job" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_ghcr_registry" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_github_token" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_metadata_action" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_uses_build_push_action" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_push_is_enabled" -v
python -m pytest "tests/test_ci.py::TestDockerPublishWorkflow::test_has_write_packages_permission" -v
```

---

### Subgrupo: TestCIProjectConsistency (6 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_python_version_matches_requirements" -v
py -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_ci_references_requirements_txt" -v
py -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_ci_references_app_directory_for_lint" -v
py -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_flake8_config_file_exists" -v
py -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_dockerfile_exists_for_docker_build" -v
py -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_ci_uses_gha_cache_for_docker" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_python_version_matches_requirements" -v
python -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_ci_references_requirements_txt" -v
python -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_ci_references_app_directory_for_lint" -v
python -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_flake8_config_file_exists" -v
python -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_dockerfile_exists_for_docker_build" -v
python -m pytest "tests/test_ci.py::TestCIProjectConsistency::test_ci_uses_gha_cache_for_docker" -v
```

---

---

# GRUPO 2 — test_infra.py (50 pruebas)
## Infraestructura Docker

### Ejecutar el grupo completo

**Windows:**
```cmd
py -m pytest tests/test_infra.py -v
```
**Codespaces:**
```bash
python -m pytest tests/test_infra.py -v
```

---

### Subgrupo: TestEnvFiles (13 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_exists[.env.dev-development-true]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_exists[.env.test-test-false]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_exists[.env.prod-production-false]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_has_required_keys[.env.dev-development-true]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_has_required_keys[.env.test-test-false]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_has_required_keys[.env.prod-production-false]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_correct_values[.env.dev-development-true]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_correct_values[.env.test-test-false]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_correct_values[.env.prod-production-false]" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_prod_debug_is_false" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_test_debug_is_false" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_dev_debug_is_true" -v
py -m pytest "tests/test_infra.py::TestEnvFiles::test_database_paths_are_distinct" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_exists[.env.dev-development-true]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_exists[.env.test-test-false]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_exists[.env.prod-production-false]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_has_required_keys[.env.dev-development-true]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_has_required_keys[.env.test-test-false]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_has_required_keys[.env.prod-production-false]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_correct_values[.env.dev-development-true]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_correct_values[.env.test-test-false]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_env_file_correct_values[.env.prod-production-false]" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_prod_debug_is_false" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_test_debug_is_false" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_dev_debug_is_true" -v
python -m pytest "tests/test_infra.py::TestEnvFiles::test_database_paths_are_distinct" -v
```

---

### Subgrupo: TestDockerfile (8 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_infra.py::TestDockerfile::test_dockerfile_exists" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_uses_slim_python_image" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_has_multi_stage_build" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_exposes_port_5000" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_has_healthcheck" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_runs_as_non_root_user" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_creates_data_directory" -v
py -m pytest "tests/test_infra.py::TestDockerfile::test_copies_requirements_before_code" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_infra.py::TestDockerfile::test_dockerfile_exists" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_uses_slim_python_image" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_has_multi_stage_build" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_exposes_port_5000" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_has_healthcheck" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_runs_as_non_root_user" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_creates_data_directory" -v
python -m pytest "tests/test_infra.py::TestDockerfile::test_copies_requirements_before_code" -v
```

---

### Subgrupo: TestDockerCompose (14 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_infra.py::TestDockerCompose::test_compose_file_exists" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_has_three_app_services" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_has_nginx_service" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_services_have_profiles" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_dev_profile_exists" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_app_dev_has_bind_mount_for_hot_reload" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_app_prod_has_no_direct_port_mapping" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_nginx_listens_on_port_80" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_nginx_depends_on_app_prod" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_all_services_have_healthcheck" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_has_named_volumes" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_all_services_share_network" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_prod_restart_policy_is_always" -v
py -m pytest "tests/test_infra.py::TestDockerCompose::test_test_restart_policy_is_no" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_infra.py::TestDockerCompose::test_compose_file_exists" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_has_three_app_services" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_has_nginx_service" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_services_have_profiles" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_dev_profile_exists" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_app_dev_has_bind_mount_for_hot_reload" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_app_prod_has_no_direct_port_mapping" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_nginx_listens_on_port_80" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_nginx_depends_on_app_prod" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_all_services_have_healthcheck" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_has_named_volumes" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_all_services_share_network" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_prod_restart_policy_is_always" -v
python -m pytest "tests/test_infra.py::TestDockerCompose::test_test_restart_policy_is_no" -v
```

---

### Subgrupo: TestNginxConfig (10 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_infra.py::TestNginxConfig::test_nginx_conf_exists" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_conf_exists" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_nginx_conf_includes_conf_d" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_proxies_to_app_prod" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_listens_on_port_80" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_sets_real_ip_header" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_has_security_headers" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_blocks_hidden_files" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_server_tokens_off" -v
py -m pytest "tests/test_infra.py::TestNginxConfig::test_health_check_route_has_access_log_off" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_infra.py::TestNginxConfig::test_nginx_conf_exists" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_conf_exists" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_nginx_conf_includes_conf_d" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_proxies_to_app_prod" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_listens_on_port_80" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_sets_real_ip_header" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_has_security_headers" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_vhost_blocks_hidden_files" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_server_tokens_off" -v
python -m pytest "tests/test_infra.py::TestNginxConfig::test_health_check_route_has_access_log_off" -v
```

---

### Subgrupo: TestDockerIgnore (5 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_infra.py::TestDockerIgnore::test_dockerignore_exists" -v
py -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_tests" -v
py -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_pycache" -v
py -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_local_db" -v
py -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_git_folder" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_infra.py::TestDockerIgnore::test_dockerignore_exists" -v
python -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_tests" -v
python -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_pycache" -v
python -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_local_db" -v
python -m pytest "tests/test_infra.py::TestDockerIgnore::test_excludes_git_folder" -v
```

---

---

# GRUPO 3 — test_scripts.py (64 pruebas)
## Scripts de Automatización

### Ejecutar el grupo completo

**Windows:**
```cmd
py -m pytest tests/test_scripts.py -v
```
**Codespaces:**
```bash
python -m pytest tests/test_scripts.py -v
```

---

### Subgrupo: TestScriptExistence (12 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[install.sh]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[run.sh]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[test.sh]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[healthcheck.sh]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[lint.sh]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[install.ps1]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[run.ps1]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[test.ps1]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[healthcheck.ps1]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[lint.ps1]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_config_file_exists[.flake8]" -v
py -m pytest "tests/test_scripts.py::TestScriptExistence::test_config_file_exists[.gitignore]" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[install.sh]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[run.sh]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[test.sh]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[healthcheck.sh]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_bash_script_exists[lint.sh]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[install.ps1]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[run.ps1]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[test.ps1]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[healthcheck.ps1]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_ps1_script_exists[lint.ps1]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_config_file_exists[.flake8]" -v
python -m pytest "tests/test_scripts.py::TestScriptExistence::test_config_file_exists[.gitignore]" -v
```

---

### Subgrupo: TestBashScriptStructure (22 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_has_shebang" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_has_pipefail" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_creates_venv" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_uses_pip" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_has_shebang" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_has_pipefail" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_validates_env_arg" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_loads_env_file" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_calls_python" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_has_shebang" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_has_pipefail" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_sets_app_env_test" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_sets_database_path" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_runs_pytest" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_has_cleanup" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_has_shebang" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_uses_curl_or_retry" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_checks_api_health" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_has_max_retries_logic" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_has_shebang" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_has_pipefail" -v
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_runs_flake8" -v
```

Nota: `test_lint_sh_targets_app_directory` se incluye en el bloque anterior — son 22 en total incluyendo:
```cmd
py -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_targets_app_directory" -v
```

**Codespaces:**
```bash
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_has_shebang" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_has_pipefail" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_creates_venv" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_install_sh_uses_pip" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_has_shebang" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_has_pipefail" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_validates_env_arg" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_loads_env_file" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_run_sh_calls_python" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_has_shebang" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_has_pipefail" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_sets_app_env_test" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_sets_database_path" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_runs_pytest" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_test_sh_has_cleanup" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_has_shebang" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_uses_curl_or_retry" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_checks_api_health" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_healthcheck_sh_has_max_retries_logic" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_has_shebang" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_has_pipefail" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_runs_flake8" -v
python -m pytest "tests/test_scripts.py::TestBashScriptStructure::test_lint_sh_targets_app_directory" -v
```

---

### Subgrupo: TestPowershellScriptStructure (17 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_install_ps1_has_error_action_stop" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_install_ps1_creates_venv" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_install_ps1_uses_pip" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_has_env_parameter" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_validates_env_values" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_loads_env_file" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_calls_python" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_accepts_extra_args" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_sets_app_env_test" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_runs_pytest" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_exits_with_code" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_has_hostname_param" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_has_port_param" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_checks_api_health" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_has_retry_loop" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_lint_ps1_runs_flake8" -v
py -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_lint_ps1_targets_app_directory" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_install_ps1_has_error_action_stop" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_install_ps1_creates_venv" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_install_ps1_uses_pip" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_has_env_parameter" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_validates_env_values" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_loads_env_file" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_run_ps1_calls_python" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_accepts_extra_args" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_sets_app_env_test" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_runs_pytest" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_test_ps1_exits_with_code" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_has_hostname_param" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_has_port_param" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_checks_api_health" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_healthcheck_ps1_has_retry_loop" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_lint_ps1_runs_flake8" -v
python -m pytest "tests/test_scripts.py::TestPowershellScriptStructure::test_lint_ps1_targets_app_directory" -v
```

---

### Subgrupo: TestConfigFiles (9 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_has_flake8_section" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_has_max_line_length" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_max_line_length_value" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_has_exclude" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_excludes_venv" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_venv" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_pycache" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_pyc" -v
py -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_db_files" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_has_flake8_section" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_has_max_line_length" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_max_line_length_value" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_has_exclude" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_flake8_excludes_venv" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_venv" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_pycache" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_pyc" -v
python -m pytest "tests/test_scripts.py::TestConfigFiles::test_gitignore_ignores_db_files" -v
```

---

### Subgrupo: TestScriptExecution (3 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_scripts.py::TestScriptExecution::test_lint_ps1_passes_on_codebase" -v
py -m pytest "tests/test_scripts.py::TestScriptExecution::test_test_ps1_runs_suite_without_recursion" -v
py -m pytest "tests/test_scripts.py::TestScriptExecution::test_healthcheck_ps1_fails_gracefully_on_no_server" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_scripts.py::TestScriptExecution::test_lint_ps1_passes_on_codebase" -v
python -m pytest "tests/test_scripts.py::TestScriptExecution::test_test_ps1_runs_suite_without_recursion" -v
python -m pytest "tests/test_scripts.py::TestScriptExecution::test_healthcheck_ps1_fails_gracefully_on_no_server" -v
```

---

---

# GRUPO 4 — test_tasks.py (27 pruebas)
## API REST — CRUD

### Ejecutar el grupo completo

**Windows:**
```cmd
py -m pytest tests/test_tasks.py -v
```
**Codespaces:**
```bash
python -m pytest tests/test_tasks.py -v
```

---

### Subgrupo: TestHealth (2 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_tasks.py::TestHealth::test_health_returns_200" -v
py -m pytest "tests/test_tasks.py::TestHealth::test_health_body_ok" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_tasks.py::TestHealth::test_health_returns_200" -v
python -m pytest "tests/test_tasks.py::TestHealth::test_health_body_ok" -v
```

---

### Subgrupo: TestListTasks (4 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_tasks.py::TestListTasks::test_empty_list_on_clean_db" -v
py -m pytest "tests/test_tasks.py::TestListTasks::test_returns_created_tasks" -v
py -m pytest "tests/test_tasks.py::TestListTasks::test_filter_by_status_pending" -v
py -m pytest "tests/test_tasks.py::TestListTasks::test_filter_by_invalid_status_returns_400" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_tasks.py::TestListTasks::test_empty_list_on_clean_db" -v
python -m pytest "tests/test_tasks.py::TestListTasks::test_returns_created_tasks" -v
python -m pytest "tests/test_tasks.py::TestListTasks::test_filter_by_status_pending" -v
python -m pytest "tests/test_tasks.py::TestListTasks::test_filter_by_invalid_status_returns_400" -v
```

---

### Subgrupo: TestCreateTask (9 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_returns_201" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_response_has_required_fields" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_default_status_is_pending" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_without_title_returns_400" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_empty_title_returns_400" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_invalid_status_returns_400" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_without_json_body_returns_400" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_very_long_title" -v
py -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_special_characters" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_returns_201" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_response_has_required_fields" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_default_status_is_pending" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_without_title_returns_400" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_empty_title_returns_400" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_invalid_status_returns_400" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_without_json_body_returns_400" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_very_long_title" -v
python -m pytest "tests/test_tasks.py::TestCreateTask::test_create_with_special_characters" -v
```

---

### Subgrupo: TestGetTask (2 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_tasks.py::TestGetTask::test_get_existing_task" -v
py -m pytest "tests/test_tasks.py::TestGetTask::test_get_nonexistent_returns_404" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_tasks.py::TestGetTask::test_get_existing_task" -v
python -m pytest "tests/test_tasks.py::TestGetTask::test_get_nonexistent_returns_404" -v
```

---

### Subgrupo: TestUpdateTask (6 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_status_to_completed" -v
py -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_title" -v
py -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_preserves_unmodified_fields" -v
py -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_nonexistent_returns_404" -v
py -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_with_empty_title_returns_400" -v
py -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_with_invalid_status_returns_400" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_status_to_completed" -v
python -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_title" -v
python -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_preserves_unmodified_fields" -v
python -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_nonexistent_returns_404" -v
python -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_with_empty_title_returns_400" -v
python -m pytest "tests/test_tasks.py::TestUpdateTask::test_update_with_invalid_status_returns_400" -v
```

---

### Subgrupo: TestDeleteTask (4 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_tasks.py::TestDeleteTask::test_delete_existing_task_returns_200" -v
py -m pytest "tests/test_tasks.py::TestDeleteTask::test_deleted_task_not_found_afterwards" -v
py -m pytest "tests/test_tasks.py::TestDeleteTask::test_delete_nonexistent_returns_404" -v
py -m pytest "tests/test_tasks.py::TestDeleteTask::test_double_delete_returns_404_second_time" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_tasks.py::TestDeleteTask::test_delete_existing_task_returns_200" -v
python -m pytest "tests/test_tasks.py::TestDeleteTask::test_deleted_task_not_found_afterwards" -v
python -m pytest "tests/test_tasks.py::TestDeleteTask::test_delete_nonexistent_returns_404" -v
python -m pytest "tests/test_tasks.py::TestDeleteTask::test_double_delete_returns_404_second_time" -v
```

---

---

# GRUPO 5 — test_vv.py (58 pruebas)
## V&V Ampliado

### Ejecutar el grupo completo

**Windows:**
```cmd
py -m pytest tests/test_vv.py -v
```
**Codespaces:**
```bash
python -m pytest tests/test_vv.py -v
```

---

### VV-F: TestVV_Funcionales (15 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_crear_tarea_con_todos_los_campos" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_tarea_tiene_timestamps_al_crear" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_updated_at_cambia_en_actualizacion" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_created_at_no_cambia_en_actualizacion" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_listar_tareas_ordena_mas_recientes_primero" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_filtrar_por_status_in_progress" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_filtrar_por_status_completed" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_filtro_no_contamina_entre_estados" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_actualizar_descripcion" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_actualizar_multiples_campos_simultaneamente" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_respuesta_delete_contiene_mensaje" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_tarea_creada_aparece_en_listado" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_tarea_eliminada_no_aparece_en_listado" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_health_devuelve_service_name" -v
py -m pytest "tests/test_vv.py::TestVV_Funcionales::test_id_es_autoincrementado" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_crear_tarea_con_todos_los_campos" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_tarea_tiene_timestamps_al_crear" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_updated_at_cambia_en_actualizacion" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_created_at_no_cambia_en_actualizacion" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_listar_tareas_ordena_mas_recientes_primero" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_filtrar_por_status_in_progress" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_filtrar_por_status_completed" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_filtro_no_contamina_entre_estados" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_actualizar_descripcion" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_actualizar_multiples_campos_simultaneamente" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_respuesta_delete_contiene_mensaje" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_tarea_creada_aparece_en_listado" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_tarea_eliminada_no_aparece_en_listado" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_health_devuelve_service_name" -v
python -m pytest "tests/test_vv.py::TestVV_Funcionales::test_id_es_autoincrementado" -v
```

---

### VV-N: TestVV_Negativos (12 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_sin_content_type_json_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_con_title_solo_espacios_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_con_status_none_usa_default" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_con_json_malformado_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_actualizar_sin_body_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_actualizar_status_invalido_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_actualizar_title_null_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_get_id_inexistente_retorna_404" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_delete_id_inexistente_retorna_404" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_respuesta_error_tiene_campo_error" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_filtro_status_invalido_retorna_400_con_mensaje" -v
py -m pytest "tests/test_vv.py::TestVV_Negativos::test_get_ruta_inexistente_retorna_404" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_sin_content_type_json_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_con_title_solo_espacios_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_con_status_none_usa_default" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_crear_con_json_malformado_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_actualizar_sin_body_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_actualizar_status_invalido_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_actualizar_title_null_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_get_id_inexistente_retorna_404" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_delete_id_inexistente_retorna_404" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_respuesta_error_tiene_campo_error" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_filtro_status_invalido_retorna_400_con_mensaje" -v
python -m pytest "tests/test_vv.py::TestVV_Negativos::test_get_ruta_inexistente_retorna_404" -v
```

---

### VV-B: TestVV_Borde (14 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_de_un_solo_caracter" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_de_1000_caracteres" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_descripcion_vacia_es_aceptada" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_descripcion_de_2000_caracteres" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_unicode_emojis" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_caracteres_chinos" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_html_se_almacena_sin_escapar" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_comillas_sql_injection" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_crear_100_tareas_y_listar" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_id_cero_no_encontrado" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_id_negativo_no_encontrado_o_404" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_solo_tab_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_solo_newlines_retorna_400" -v
py -m pytest "tests/test_vv.py::TestVV_Borde::test_body_json_vacio_retorna_400" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_de_un_solo_caracter" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_de_1000_caracteres" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_descripcion_vacia_es_aceptada" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_descripcion_de_2000_caracteres" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_unicode_emojis" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_caracteres_chinos" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_html_se_almacena_sin_escapar" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_comillas_sql_injection" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_crear_100_tareas_y_listar" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_id_cero_no_encontrado" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_id_negativo_no_encontrado_o_404" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_solo_tab_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_titulo_con_solo_newlines_retorna_400" -v
python -m pytest "tests/test_vv.py::TestVV_Borde::test_body_json_vacio_retorna_400" -v
```

---

### VV-I: TestVV_Integracion (7 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_flujo_completo_crud" -v
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_transicion_de_estados_pendiente_a_completado" -v
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_multiples_tareas_independientes" -v
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_eliminar_no_afecta_otras_tareas" -v
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_filtro_refleja_actualizacion_de_estado" -v
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_crear_actualizar_y_verificar_campos_individualmente" -v
py -m pytest "tests/test_vv.py::TestVV_Integracion::test_listado_vacio_tras_eliminar_todas" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_flujo_completo_crud" -v
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_transicion_de_estados_pendiente_a_completado" -v
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_multiples_tareas_independientes" -v
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_eliminar_no_afecta_otras_tareas" -v
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_filtro_refleja_actualizacion_de_estado" -v
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_crear_actualizar_y_verificar_campos_individualmente" -v
python -m pytest "tests/test_vv.py::TestVV_Integracion::test_listado_vacio_tras_eliminar_todas" -v
```

---

### VV-H: TestVV_HTTP (10 pruebas)

**Windows:**
```cmd
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_respuestas_son_json" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_post_retorna_201_al_crear" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_get_retorna_200" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_put_retorna_200_en_actualizacion_exitosa" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_delete_retorna_200_en_eliminacion_exitosa" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_errores_400_incluyen_body_json" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_errores_404_incluyen_body_json" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_respuesta_lista_es_array_json" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_respuesta_tarea_individual_es_objeto_json" -v
py -m pytest "tests/test_vv.py::TestVV_HTTP::test_campos_obligatorios_en_respuesta_de_tarea" -v
```
**Codespaces:**
```bash
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_respuestas_son_json" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_post_retorna_201_al_crear" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_get_retorna_200" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_put_retorna_200_en_actualizacion_exitosa" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_delete_retorna_200_en_eliminacion_exitosa" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_errores_400_incluyen_body_json" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_errores_404_incluyen_body_json" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_respuesta_lista_es_array_json" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_respuesta_tarea_individual_es_objeto_json" -v
python -m pytest "tests/test_vv.py::TestVV_HTTP::test_campos_obligatorios_en_respuesta_de_tarea" -v
```

---

## RESUMEN DE CONTEO

| Grupo | Archivo | Pruebas |
|---|---|---|
| Pipeline CI/CD | test_ci.py | 46 |
| Infraestructura Docker | test_infra.py | 50 |
| Scripts de Automatización | test_scripts.py | 64 |
| API REST CRUD | test_tasks.py | 27 |
| V&V Ampliado | test_vv.py | 58 |
| **TOTAL** | | **245** |
