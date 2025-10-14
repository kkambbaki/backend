from .base import *  # noqa

# ========== CORS / CSRF settings ==========

CORS_ALLOWED_ORIGINS = [
  # TODO: 배포 후 도메인 설정
]

CSRF_TRUSTED_ORIGINS = [
  # TODO: 배포 후 도메인 설정
]

CORS_ALLOW_CREDENTIALS = True

# ========== END CORS / CSRF settings ==========
