"""
Report Email Service

PDF 리포트를 이메일로 전송하는 서비스입니다.
"""

import logging
from typing import Optional

from reports.services.base_pdf_generator import BasePDFGenerator
from reports.services.email import FileAttachmentEmailService

logger = logging.getLogger(__name__)


class ReportEmailService(FileAttachmentEmailService):
    """
    PDF 리포트를 생성하고 이메일로 전송하는 서비스

    Usage:
        service = ReportEmailService()
        result = service.send_report_email(
            to_email="user@example.com",
            site_url="https://example.com/report",
        )
    """

    def get_subject(self, **kwargs) -> str:
        """
        이메일 제목을 반환합니다.

        Args:
            **kwargs: 제목 생성에 필요한 추가 파라미터
                - site_name: 사이트 이름 (선택)

        Returns:
            str: 이메일 제목
        """
        site_name = kwargs.get("site_name", "깜빡이")
        return f"[{site_name}] 집중력 분석 리포트가 도착했습니다"

    def get_body(self, **kwargs) -> str:
        """
        이메일 본문을 반환합니다. / 텍스트 형식 제공하지 않음.
        """
        return ""

    def get_html_body(self, **kwargs) -> Optional[str]:
        """
        HTML 형식의 이메일 본문을 반환합니다.

        Args:
            **kwargs: 본문 생성에 필요한 추가 파라미터
                - site_url: 사이트 URL (선택)

        Returns:
            Optional[str]: HTML 형식의 이메일 본문
        """
        html_body = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #FFE3A7;
            color: #000000;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }
        .content {
            background-color: #FFF4DF;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>리포트가 도착했습니다</h1>
    </div>
    <div class="content">
        <p>안녕하세요,</p>
        <p>집중력 분석 리포트가 도착했습니다.</p>
        <p>첨부된 PDF 파일을 확인해 주세요.</p>
        <p>감사합니다.</p>
    </div>
    <div class="footer">
        <p>@깜빡이팀</p>
    </div>
</body>
</html>
"""
        return html_body

    def get_attachments(self, **kwargs) -> list[tuple[str, bytes, str]]:
        """
        첨부 파일 목록을 반환합니다.

        Args:
            **kwargs: 첨부 파일 생성에 필요한 추가 파라미터
                - pdf_file_path: PDF 파일 경로 (필수)
                - pdf_filename: PDF 파일명 (선택, 기본값: report.pdf)

        Returns:
            list[tuple[str, bytes, str]]: 첨부 파일 목록
        """
        pdf_file_path = kwargs.get("pdf_file_path")
        pdf_filename = kwargs.get("pdf_filename", "report.pdf")

        if not pdf_file_path:
            logger.warning("No PDF file path provided for email attachment")
            return []

        try:
            attachment = self.attach_file_from_storage(
                file_path=pdf_file_path, filename=pdf_filename, mimetype="application/pdf"
            )
            return [attachment]
        except FileNotFoundError as e:
            logger.error(f"PDF file not found: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to attach PDF file: {e}", exc_info=True)
            return []

    def send_report_email(
        self,
        to_email: str,
        site_url: str,
        pdf_file_path: Optional[str] = None,
        pdf_filename: str = "report.pdf",
        site_name: str = "깜빡이",
    ) -> dict:
        """
        PDF 리포트를 생성하고 이메일로 전송합니다.

        Args:
            to_email: 수신자 이메일 주소
            site_url: 리포트를 생성할 사이트 URL
            pdf_file_path: 이미 생성된 PDF 파일 경로 (선택, None이면 site_url로부터 새로 생성)
            pdf_filename: PDF 첨부 파일명 (기본값: report.pdf)
            site_name: 사이트 이름 (기본값: 깜빡이)

        Returns:
            dict: {
                "success": bool,
                "message": str,
                "pdf_file_path": str,  # 성공 시 PDF 파일 경로
            }
        """
        try:
            # PDF 파일이 제공되지 않은 경우 생성
            if not pdf_file_path:
                logger.info(f"Generating PDF for URL: {site_url}")
                generator = BasePDFGenerator()
                pdf_file_path, expiry_date = generator.generate_pdf(url=site_url)
                logger.info(f"PDF generated successfully: {pdf_file_path}, expires at {expiry_date}")

            # 이메일 전송
            result = self.send_email(
                to_email=to_email,
                site_url=site_url,
                site_name=site_name,
                pdf_file_path=pdf_file_path,
                pdf_filename=pdf_filename,
            )

            if result["success"]:
                result["pdf_file_path"] = pdf_file_path

            return result

        except Exception as e:
            logger.error(f"Failed to send report email: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to send report email: {e!s}",
            }
