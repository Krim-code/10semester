import subprocess
import os

def run_lighthouse_to_pdf(url, report_name, mode="mobile"):
    try:
        # Выбираем режим тестирования: мобильный или десктопный
        preset = "mobile" if mode == "mobile" else "desktop"
        
        # Генерируем HTML отчёт
        html_report = f"{report_name}_{mode}.html"
        subprocess.run(
            [
                "lighthouse",
                url,
                f"--preset={preset}",
                "--output=html",
                f"--output-path={html_report}"
            ],
            check=True
        )
        print(f"HTML report generated: {html_report}")

        # Конвертируем HTML в PDF с использованием Google Chrome
        pdf_report = f"{report_name}_{mode}.pdf"
        subprocess.run(
            [
                "google-chrome",
                "--headless",
                "--disable-gpu",
                "--print-to-pdf-no-header",
                f"--print-to-pdf={pdf_report}",
                html_report
            ],
            check=True
        )
        print(f"PDF report generated: {pdf_report}")

        # Удаляем временный HTML файл
        os.remove(html_report)

    except subprocess.CalledProcessError as e:
        print(f"Error during Lighthouse run for {url} ({mode}): {e}")

def process_urls(urls):
    for i, url in enumerate(urls, start=1):
        print(f"Processing {url}...")
        report_base_name = f"report_{i}"  # Базовое имя отчёта
        run_lighthouse_to_pdf(url, report_base_name, mode="mobile")
        run_lighthouse_to_pdf(url, report_base_name, mode="desktop")

# Список URL для тестирования
urls = [
    "https://adeta.ru",
    "https://bintaga.ru",
]

process_urls(urls)
