from .dax import check_hardcoded_comparators, check_measure_descriptions
from .documentation import check_local_markdown_links
from .powerbi import check_absolute_paths, check_pbip_manifest, check_pbir_json, check_tmdl_model
from .repository import check_ci, check_license, check_readme, check_tests
from .reproducibility import check_build_entrypoint, check_generated_drift
from .security import check_secrets, check_sensitive_home_paths

CHECKS = [
    check_readme,
    check_license,
    check_tests,
    check_ci,
    check_pbip_manifest,
    check_pbir_json,
    check_tmdl_model,
    check_absolute_paths,
    check_hardcoded_comparators,
    check_measure_descriptions,
    check_secrets,
    check_sensitive_home_paths,
    check_local_markdown_links,
    check_build_entrypoint,
    check_generated_drift,
]

__all__ = ["CHECKS"]
