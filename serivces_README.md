# Reports Services

이 디렉토리에는 리포트 관련 서비스 로직이 포함되어 있습니다.

## 파일 구조

```
services/
├── base_pdf_generator.py       # PDF 생성 베이스 클래스
├── base_email_service.py       # 이메일 전송 베이스 클래스
├── report_email_service.py     # PDF 리포트 이메일 전송 서비스
└── README.md                   # 본 문서
```

## PDF 생성 서비스

### BasePDFGenerator

URL을 받아 PDF를 생성하는 베이스 클래스입니다.

**주요 메서드:**
- `generate_pdf(url)`: PDF를 생성하고 storage에 저장
- `get_pdf_url(file_path)`: 저장된 PDF의 URL 반환
- `delete_pdf(file_path)`: 저장된 PDF 삭제

**사용 예시:**

```python
from reports.services import BasePDFGenerator

# 기본 사용
generator = BasePDFGenerator()
file_path, expiry_date = generator.generate_pdf(url="https://example.com")

# 커스터마이징
class CustomPDFGenerator(BasePDFGenerator):
    def get_viewport_size(self):
        return {"width": 1920, "height": 1080}

    def get_pdf_format(self):
        return "A4"

generator = CustomPDFGenerator()
file_path, expiry_date = generator.generate_pdf(url="https://example.com")
```

## 이메일 전송 서비스

### BaseEmailService

이메일 전송을 위한 추상화 베이스 클래스입니다.

**주요 메서드:**
- `get_subject(**kwargs)`: 이메일 제목 반환 (추상 메서드)
- `get_body(**kwargs)`: 이메일 본문 반환 (추상 메서드)
- `get_html_body(**kwargs)`: HTML 본문 반환 (선택)
- `get_attachments(**kwargs)`: 첨부 파일 목록 반환 (선택)
- `send_email(to_email, **kwargs)`: 이메일 전송

**사용 예시:**

```python
from reports.services import BaseEmailService

class WelcomeEmailService(BaseEmailService):
    def get_subject(self, **kwargs):
        return "환영합니다!"

    def get_body(self, **kwargs):
        return "가입해 주셔서 감사합니다."

service = WelcomeEmailService()
result = service.send_email(to_email="user@example.com")
```

### FileAttachmentEmailService

파일 첨부 기능이 포함된 이메일 서비스 베이스 클래스입니다.

**주요 메서드:**
- `attach_file_from_storage(file_path, filename, mimetype)`: storage에서 파일을 첨부 파일로 변환

### ReportEmailService

PDF 리포트를 이메일로 전송하는 서비스입니다.

**주요 메서드:**
- `send_report_email(to_email, site_url, pdf_file_path, pdf_filename, site_name)`: PDF 리포트 이메일 전송

**사용 예시:**

```python
from reports.services import ReportEmailService

service = ReportEmailService()

# PDF를 새로 생성하여 전송
result = service.send_report_email(
    to_email="user@example.com",
    site_url="https://example.com/report",
)

# 이미 생성된 PDF를 전송
result = service.send_report_email(
    to_email="user@example.com",
    site_url="https://example.com/report",
    pdf_file_path="pdfs/2025/01/01/abc123.pdf",
    pdf_filename="my_report.pdf",
)
```

## Celery Tasks

비동기 작업을 위한 Celery task들이 `reports/tasks/` 디렉토리에 정의되어 있습니다.

### send_report_email_task

PDF 리포트를 비동기로 생성하고 이메일로 전송합니다.

**사용 예시:**

```python
from reports.tasks import send_report_email_task

# 비동기 실행
result = send_report_email_task.delay(
    to_email="user@example.com",
    site_url="https://example.com/report",
)

# 결과 확인
print(result.get())  # {"success": True, "message": "...", "pdf_file_path": "..."}
```

### send_report_email_with_existing_pdf_task

이미 생성된 PDF를 비동기로 이메일 전송합니다.

**사용 예시:**

```python
from reports.tasks import send_report_email_with_existing_pdf_task

result = send_report_email_with_existing_pdf_task.delay(
    to_email="user@example.com",
    site_url="https://example.com/report",
    pdf_file_path="pdfs/2025/01/01/abc123.pdf",
)
```

## SMTP 설정

### 네이버 SMTP 설정

`.env` 파일에 다음 설정을 추가하세요:

```env
# Email settings (Naver SMTP)
EMAIL_HOST=smtp.naver.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contact-kkambbaki@naver.com
EMAIL_HOST_PASSWORD=your-naver-password-or-app-password
DEFAULT_FROM_EMAIL=contact-kkambbaki@naver.com
```

**중요:** 네이버 2단계 인증을 사용하는 경우:
1. 네이버 로그인 > 보안설정 > 2단계 인증 관리
2. 애플리케이션 비밀번호 관리
3. 비밀번호 생성 후 `EMAIL_HOST_PASSWORD`에 설정

### Django Settings

`config/settings/base.py`에 이미 다음 설정이 추가되어 있습니다:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.naver.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL
```

## 테스트

Django shell에서 테스트할 수 있습니다:

```bash
# Docker 환경
./tool.sh
# shell 선택

# Django shell
python manage.py shell
```

```python
# PDF 생성 테스트
from reports.services import BasePDFGenerator
generator = BasePDFGenerator()
file_path, expiry_date = generator.generate_pdf(url="https://example.com")
print(f"PDF generated: {file_path}, expires: {expiry_date}")

# 이메일 전송 테스트
from reports.services import ReportEmailService
service = ReportEmailService()
result = service.send_report_email(
    to_email="your-email@example.com",
    site_url="https://example.com",
)
print(result)

# Celery task 테스트
from reports.tasks import send_report_email_task
result = send_report_email_task.delay(
    to_email="your-email@example.com",
    site_url="https://example.com",
)
print(result.get())  # 결과 대기
```

## 커스터마이징

### 커스텀 이메일 서비스 만들기

```python
from reports.services import BaseEmailService

class CustomEmailService(BaseEmailService):
    def get_subject(self, **kwargs):
        user_name = kwargs.get("user_name", "고객")
        return f"{user_name}님, 안녕하세요!"

    def get_body(self, **kwargs):
        return "커스텀 이메일 내용입니다."

    def get_html_body(self, **kwargs):
        return """
        <html>
        <body>
            <h1>HTML 이메일</h1>
            <p>커스텀 이메일 내용입니다.</p>
        </body>
        </html>
        """

service = CustomEmailService()
result = service.send_email(
    to_email="user@example.com",
    user_name="홍길동",
)
```

### 커스텀 PDF 생성기 만들기

```python
from reports.services import BasePDFGenerator

class LandscapePDFGenerator(BasePDFGenerator):
    def get_pdf_format(self):
        return "A4"

    def get_pdf_options(self):
        return {
            "format": self.get_pdf_format(),
            "landscape": True,  # 가로 방향
            "print_background": True,
        }

generator = LandscapePDFGenerator()
file_path, expiry_date = generator.generate_pdf(url="https://example.com")
```
