from .base import *  # noqa

# ========== CORS / CSRF settings ==========

ALPHA_BASE_URL = "https://alpha.singun11.wtf"

CORS_ALLOWED_ORIGINS = [
  "http://localhost:3000",
  "http://localhost:8000",
  ALPHA_BASE_URL,
  # TODO: 배포 후 도메인 설정
]

CSRF_TRUSTED_ORIGINS = [
  "http://localhost:3000",
  "http://localhost:8000",
  ALPHA_BASE_URL,
  # TODO: 배포 후 도메인 설정
]

CORS_ALLOW_CREDENTIALS = True

# ========== END CORS / CSRF settings ==========
