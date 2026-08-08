"""
ThesisFlow — Testes de Segurança da Prática 1 (Escritos antes da validação final)
Executados via: pytest codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py
"""

import pytest
from authorization import (
    UserContext,
    AuditLogger,
    PermissionDeniedError,
    verify_resource_ownership,
    get_student_profile
)


def test_ts01_idor_attack_attempt_denied():
    """
    TS01 — Caso Malicioso / Não Autorizado (IDOR):
    Ação: Estudante 'student_123' tenta acessar o perfil do estudante 'student_456'.
    Resultado Esperado: Acesso recusado com PermissionDeniedError (HTTP 403) e evento registrado no log de auditoria.
    """
    logger = AuditLogger()
    attacker_student = UserContext(uid="student_123", role="student")
    target_student_id = "student_456"

    # Execução do teste de segurança
    with pytest.raises(PermissionDeniedError) as exc_info:
        get_student_profile(attacker_student, target_student_id, audit_logger=logger)

    # Verificações do teste
    assert "403 Forbidden" in str(exc_info.value)
    assert len(logger.logs) == 1
    audit_entry = logger.logs[0]
    assert audit_entry["event_type"] == "UNAUTHORIZED_IDOR_ATTEMPT"
    assert audit_entry["user_uid"] == "student_123"
    assert audit_entry["target_resource"] == "student_456"
    assert audit_entry["allowed"] is False


def test_ts02_legitimate_student_access_allowed():
    """
    TS02 — Caso de Uso Válido (Próprio Recurso):
    Ação: Estudante 'student_123' acessa seu próprio perfil.
    Resultado Esperado: Acesso permitido com sucesso (HTTP 200) e dados retornados.
    """
    logger = AuditLogger()
    legitimate_student = UserContext(uid="student_123", role="student")

    profile = get_student_profile(legitimate_student, "student_123", audit_logger=logger)

    assert profile["name"] == "Ana Silva"
    assert profile["advisor_uid"] == "advisor_001"
    assert len(logger.logs) == 1
    assert logger.logs[0]["event_type"] == "AUTHORIZED_RESOURCE_ACCESS"
    assert logger.logs[0]["allowed"] is True


def test_ts03_advisor_and_coordinator_access_allowed():
    """
    TS03 — Caso de Uso Válido (Orientador e Coordenador):
    Ação: 
      - Orientador 'advisor_001' acessa seu orientando 'student_123'.
      - Coordenador 'coord_001' acessa qualquer estudante 'student_456'.
    Resultado Esperado: Ambos os acessos autorizados com sucesso.
    """
    logger = AuditLogger()
    
    # 1. Teste de Orientador autorizado
    advisor = UserContext(uid="advisor_001", role="advisor", advisee_uids=["student_123"])
    profile_advisee = get_student_profile(advisor, "student_123", audit_logger=logger)
    assert profile_advisee["name"] == "Ana Silva"

    # 2. Teste de Coordenador autorizado
    coordinator = UserContext(uid="coord_001", role="coordinator")
    profile_any_student = get_student_profile(coordinator, "student_456", audit_logger=logger)
    assert profile_any_student["name"] == "Carlos Souza"

    assert len(logger.logs) == 2
    assert all(log["allowed"] is True for log in logger.logs)


def test_ts04_advisor_unauthorized_student_denied():
    """
    TS04 — Caso Malicioso / Não Autorizado (Orientador Não Vinculado):
    Ação: Orientador 'advisor_001' tenta acessar estudante 'student_456' que não é seu orientando.
    Resultado Esperado: Recusado com PermissionDeniedError (HTTP 403).
    """
    logger = AuditLogger()
    advisor = UserContext(uid="advisor_001", role="advisor", advisee_uids=["student_123"])

    with pytest.raises(PermissionDeniedError):
        get_student_profile(advisor, "student_456", audit_logger=logger)

    assert logger.logs[0]["event_type"] == "UNAUTHORIZED_IDOR_ATTEMPT"
