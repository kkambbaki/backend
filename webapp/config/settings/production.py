from .base import *  # noqa

# ========== CORS / CSRF settings ==========

CORS_ALLOWED_ORIGINS = [
  "https://frontend-git-dev-yuwon.vercel.app",
  "https://kkambbaki-frontend.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
  "https://frontend-git-dev-yuwon.vercel.app",
  "https://kkambbaki-frontend.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

# ========== END CORS / CSRF settings ==========
