"""
ThesisFlow — Testes de Segurança da Prática 2 (Upload Seguro)
Executados via: pytest codigo/etapa-4/pratica-2-upload-seguro/test_upload_service.py
"""

import pytest
from upload_service import (
    process_secure_upload,
    FileValidationError,
    UploadAuditLogger,
    MAX_FILE_SIZE_BYTES
)


def test_ts05_prohibited_executable_extension_denied():
    """
    TS05 — Caso Malicioso (Tipo Proibido / Executável):
    Ação: Envio de script malicioso com extensão '.php' ou '.exe'.
    Resultado Esperado: Recusado com FileValidationError (HTTP 422) e evento auditado.
    """
    logger = UploadAuditLogger()
    malicious_bytes = b"<?php echo 'malware'; ?>"
    
    with pytest.raises(FileValidationError) as exc_info:
        process_secure_upload(
            file_name="script_malicioso.php",
            file_bytes=malicious_bytes,
            user_uid="student_123",
            audit_logger=logger
        )

    assert exc_info.value.status_code == 422
    assert "422 Unprocessable Entity" in str(exc_info.value)
    assert len(logger.logs) == 1
    assert logger.logs[0]["event_type"] == "INVALID_EXTENSION_ATTEMPT"
    assert logger.logs[0]["allowed"] is False


def test_ts06_excessive_file_size_denied():
    """
    TS06 — Caso Malicioso (Tamanho Excessivo / DoS):
    Ação: Envio de um arquivo PDF de 11 MB (excedendo o limite de 10 MB).
    Resultado Esperado: Recusado com FileValidationError (HTTP 413) e evento auditado.
    """
    logger = UploadAuditLogger()
    # Cria bytes simulados de 11 MB com assinatura PDF
    oversized_pdf_bytes = b"%PDF-1.5 " + (b"0" * (MAX_FILE_SIZE_BYTES + 1024 * 1024))

    with pytest.raises(FileValidationError) as exc_info:
        process_secure_upload(
            file_name="comprovante_gigante.pdf",
            file_bytes=oversized_pdf_bytes,
            user_uid="student_123",
            audit_logger=logger
        )

    assert exc_info.value.status_code == 413
    assert "413 Payload Too Large" in str(exc_info.value)
    assert len(logger.logs) == 1
    assert logger.logs[0]["event_type"] == "FILE_TOO_LARGE_ATTEMPT"
    assert logger.logs[0]["allowed"] is False


def test_ts07_extension_spoofing_magic_bytes_mismatch_denied():
    """
    TS07 — Caso Malicioso (Extension Spoofing / Incongruência de Magic Bytes):
    Ação: Arquivo com extensão '.pdf', mas cujo conteúdo real é um script executável/texto (sem header %PDF).
    Resultado Esperado: A inspeção dos Magic Bytes detecta a falsificação e recusa com HTTP 422.
    """
    logger = UploadAuditLogger()
    fake_pdf_bytes = b"#!/bin/bash\nrm -rf /"

    with pytest.raises(FileValidationError) as exc_info:
        process_secure_upload(
            file_name="comprovante_falso.pdf",
            file_bytes=fake_pdf_bytes,
            user_uid="student_123",
            audit_logger=logger
        )

    assert exc_info.value.status_code == 422
    assert "incompatível" in str(exc_info.value).lower()
    assert logger.logs[0]["event_type"] == "MAGIC_BYTES_MISMATCH_ATTEMPT"
    assert logger.logs[0]["allowed"] is False


def test_ts08_legitimate_pdf_upload_success():
    """
    TS08 — Caso de Uso Válido (Upload Legítimo de PDF com Hash SHA-256):
    Ação: Envio de um comprovante PDF legítimo com assinatura de magic bytes correta.
    Resultado Esperado: Processado com sucesso (HTTP 201), gerando o Hash SHA-256 de integridade.
    """
    logger = UploadAuditLogger()
    valid_pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Title (Comprovante de Taxa) >>\nendobj\n%%EOF"

    result = process_secure_upload(
        file_name="comprovante_pagamento.pdf",
        file_bytes=valid_pdf_content,
        user_uid="student_123",
        audit_logger=logger
    )

    assert result["status"] == "success"
    assert result["file_name"] == "comprovante_pagamento.pdf"
    assert len(result["sha256_hash"]) == 64  # Tamanho padrão do hash SHA-256
    assert logger.logs[0]["event_type"] == "SECURE_UPLOAD_SUCCESS"
    assert logger.logs[0]["allowed"] is True


@pytest.mark.parametrize(
    "unsafe_file_name",
    [
        "../../comprovante.pdf",
        "..\\..\\comprovante.pdf",
        "",
        ".",
        "..",
        "\x00comprovante.pdf",
    ],
)
def test_ts09_unsafe_file_name_denied(unsafe_file_name):
    """
    TS09 — Caso Malicioso (Nome de Arquivo Inseguro):
    Ação: Envio de PDF válido com nome vazio, byte nulo ou componentes de caminho.
    Resultado Esperado: Recusado com HTTP 422 e evento auditado antes do armazenamento.
    """
    logger = UploadAuditLogger()
    valid_pdf_content = b"%PDF-1.4\n%%EOF"

    with pytest.raises(FileValidationError) as exc_info:
        process_secure_upload(
            file_name=unsafe_file_name,
            file_bytes=valid_pdf_content,
            user_uid="student_123",
            audit_logger=logger,
        )

    assert exc_info.value.status_code == 422
    assert len(logger.logs) == 1
    assert logger.logs[0]["event_type"] == "UNSAFE_FILE_NAME_ATTEMPT"
    assert logger.logs[0]["allowed"] is False


@pytest.mark.parametrize(
    ("file_name", "file_bytes", "expected_mime"),
    [
        ("comprovante.pdf", b"%PDF-1.4\n%%EOF", "application/pdf"),
        ("comprovante.png", b"\x89PNG\r\n\x1a\ncontent", "image/png"),
        ("comprovante.jpg", b"\xff\xd8\xffcontent", "image/jpeg"),
        ("comprovante.jpeg", b"\xff\xd8\xffcontent", "image/jpeg"),
    ],
)
def test_ts10_allowed_files_return_canonical_mime_type(
    file_name, file_bytes, expected_mime
):
    """
    TS10 — Caso de Uso Válido (MIME Canônico):
    Ação: Envio de cada formato permitido com assinatura válida.
    Resultado Esperado: Retorno do tipo MIME oficial do formato processado.
    """
    result = process_secure_upload(
        file_name=file_name,
        file_bytes=file_bytes,
        user_uid="student_123",
    )

    assert result["mime_type"] == expected_mime
