"""
ThesisFlow — Prática 2: Upload Seguro de Comprovantes com Validação de Tipo, Tamanho e Hash SHA-256
Mapeamento: R03 (Risco) -> RS03 (Requisito) -> DA02 (Decisão de Arquitetura)
Referências: OWASP File Upload Cheat Sheet / CWE-434 / OWASP ASVS v4 V12.2
"""

import hashlib
from pathlib import PurePosixPath
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone


class FileValidationError(Exception):
    """Exceção lançada quando o arquivo viola regras de tamanho ou extensão (HTTP 422 / 413)."""
    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message)
        self.status_code = status_code


# Configurações de segurança para upload de comprovantes (RS03)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # Limite máximo de 10 MB
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
MIME_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}

# Assinaturas de Magic Bytes conhecidas para os formatos permitidos
MAGIC_BYTES_SIGNATURES = {
    ".pdf": [b"%PDF"],
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"],
}


class UploadAuditLogger:
    """Registrador de auditoria de eventos de upload."""
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, user_uid: str, file_name: str, file_size: int, allowed: bool, detail: str = "") -> Dict[str, Any]:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "user_uid": user_uid,
            "file_name": file_name,
            "file_size": file_size,
            "allowed": allowed,
            "detail": detail
        }
        self.logs.append(entry)
        return entry


def detect_magic_bytes(file_bytes: bytes) -> Optional[str]:
    """Inspeção profunda de magic bytes (header do arquivo) sem confiar na extensão enviada."""
    for ext, signatures in MAGIC_BYTES_SIGNATURES.items():
        for sig in signatures:
            if file_bytes.startswith(sig):
                return ext
    return None


def validate_safe_file_name(file_name: str) -> str:
    """Recusa nomes vazios, bytes nulos e qualquer componente de caminho."""
    normalized = file_name.replace("\\", "/")
    base_name = PurePosixPath(normalized).name
    if (
        not normalized
        or "\x00" in normalized
        or base_name != normalized
        or base_name in {".", ".."}
    ):
        raise FileValidationError(
            "HTTP 422 Unprocessable Entity: Nome de arquivo inválido.",
            status_code=422,
        )
    return base_name


def process_secure_upload(
    file_name: str,
    file_bytes: bytes,
    user_uid: str,
    audit_logger: Optional[UploadAuditLogger] = None
) -> Dict[str, Any]:
    """
    Valida e processa o upload de um comprovante no ThesisFlow.

    Controles de Segurança (OWASP File Upload Cheat Sheet):
    1. Limite estrito de tamanho (máximo 10 MB).
    2. Validação da extensão declarada contra lista branca.
    3. Inspeção dos Magic Bytes do conteúdo real para evitar extension spoofing.
    4. Cálculo de hash imutável SHA-256 para garantia de integridade (RS03).
    """
    file_size = len(file_bytes)

    # 1. Validação de Tamanho Máximo (Prevenção de DoS / Armazenamento Excessivo)
    if file_size > MAX_FILE_SIZE_BYTES:
        if audit_logger:
            audit_logger.log_event(
                event_type="FILE_TOO_LARGE_ATTEMPT",
                user_uid=user_uid,
                file_name=file_name,
                file_size=file_size,
                allowed=False,
                detail=f"Tamanho {file_size} bytes excede o limite de {MAX_FILE_SIZE_BYTES} bytes."
            )
        raise FileValidationError(
            f"HTTP 413 Payload Too Large: O arquivo excede o limite máximo permitido de 10 MB.",
            status_code=413
        )

    try:
        safe_file_name = validate_safe_file_name(file_name)
    except FileValidationError:
        if audit_logger:
            audit_logger.log_event(
                event_type="UNSAFE_FILE_NAME_ATTEMPT",
                user_uid=user_uid,
                file_name=file_name,
                file_size=file_size,
                allowed=False,
                detail="Nome contém componente de caminho ou caractere inválido."
            )
        raise

    # 2. Validação da Extensão Declarada (Lista Branca)
    lower_file_name = safe_file_name.lower()
    detected_ext = None
    for ext in ALLOWED_EXTENSIONS:
        if lower_file_name.endswith(ext):
            detected_ext = ext
            break

    if not detected_ext:
        if audit_logger:
            audit_logger.log_event(
                event_type="INVALID_EXTENSION_ATTEMPT",
                user_uid=user_uid,
                file_name=safe_file_name,
                file_size=file_size,
                allowed=False,
                detail=f"Extensão não permitida para o arquivo '{safe_file_name}'."
            )
        raise FileValidationError(
            f"HTTP 422 Unprocessable Entity: Extensão do arquivo '{safe_file_name}' não é permitida. Extensões aceitas: PDF, PNG, JPG, JPEG.",
            status_code=422
        )

    # 3. Validação dos Magic Bytes (Inspeção Real do Conteúdo — Prevenção de Spoofing / CWE-434)
    magic_ext = detect_magic_bytes(file_bytes)
    if not magic_ext or (magic_ext != detected_ext and not (detected_ext in [".jpg", ".jpeg"] and magic_ext in [".jpg", ".jpeg"])):
        if audit_logger:
            audit_logger.log_event(
                event_type="MAGIC_BYTES_MISMATCH_ATTEMPT",
                user_uid=user_uid,
                file_name=safe_file_name,
                file_size=file_size,
                allowed=False,
                detail=f"Assinatura do arquivo (Magic Bytes '{magic_ext}') incompatível com a extensão declarada '{detected_ext}'."
            )
        raise FileValidationError(
            f"HTTP 422 Unprocessable Entity: Conteúdo do arquivo é incompatível com a extensão declarada.",
            status_code=422
        )

    # 4. Geração de Hash Imutável SHA-256 (Garantia de Integridade RS03)
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()

    if audit_logger:
        audit_logger.log_event(
            event_type="SECURE_UPLOAD_SUCCESS",
            user_uid=user_uid,
            file_name=safe_file_name,
            file_size=file_size,
            allowed=True,
            detail=f"Hash SHA-256 gerado com sucesso: {sha256_hash}"
        )

    return {
        "status": "success",
        "file_name": safe_file_name,
        "file_size_bytes": file_size,
        "mime_type": MIME_TYPES[detected_ext],
        "sha256_hash": sha256_hash,
        "storage_path": f"comprovantes/{user_uid}/{sha256_hash}_{safe_file_name}"
    }
