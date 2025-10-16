from .base import *  # noqa

# ========== CORS / CSRF settings ==========

ALPHA_BASE_URL = "https://alpha.singun11.wtf"

CORS_ALLOWED_ORIGINS = [
  "http://localhost:3000",
  "http://localhost:8000",
  "https://frontend-git-dev-yuwon.vercel.app",
  "https://kkambbaki-frontend.vercel.app",
  ALPHA_BASE_URL,
]

CSRF_TRUSTED_ORIGINS = [
  "http://localhost:3000",
  "http://localhost:8000",
  "https://frontend-git-dev-yuwon.vercel.app",
  "https://kkambbaki-frontend.vercel.app",
  ALPHA_BASE_URL,
]

CORS_ALLOW_CREDENTIALS = True

# ========== END CORS / CSRF settings ==========
