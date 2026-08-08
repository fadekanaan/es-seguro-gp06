"""
ThesisFlow — Prática 1: Controle de Autorização por Propriedade de Recurso (IDOR)
Mapeamento: R07 (Risco) -> RS01 (Requisito) -> DA01 (Decisão de Arquitetura)
Referência: OWASP Authorization Cheat Sheet / CWE-639 / OWASP Top 10 A01:2025
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone


class PermissionDeniedError(Exception):
    """Exceção lançada quando uma verificação de autorização falha (HTTP 403 Forbidden)."""
    pass


@dataclass
class UserContext:
    """Representa o contexto de um usuário autenticado extraído do token JWT."""
    uid: str
    role: str  # "student", "advisor", "coordinator"
    advisee_uids: List[str] = field(default_factory=list)


class AuditLogger:
    """Registrador de eventos de auditoria de segurança (em conformidade com RS01 e E6)."""
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def log_event(self, event_type: str, user_uid: str, target_resource: str, action: str, allowed: bool) -> Dict[str, Any]:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "user_uid": user_uid,
            "target_resource": target_resource,
            "action": action,
            "allowed": allowed
        }
        self.logs.append(entry)
        return entry


def verify_resource_ownership(
    authenticated_user: UserContext,
    target_student_id: str,
    action: str = "READ_STUDENT_DATA",
    audit_logger: Optional[AuditLogger] = None
) -> bool:
    """
    Verifica no servidor se o usuário autenticado possui permissão para acessar ou modificar
    os dados do estudante identificado por `target_student_id`.

    Regras de Negócio:
    1. Coordenadores (`coordinator`): Acesso irrestrito a qualquer estudante.
    2. Orientadores (`advisor`): Acesso permitido apenas aos estudantes listados em `advisee_uids`.
    3. Estudantes (`student`): Acesso permitido exclusivamente ao seu próprio `target_student_id`.
    
    Qualquer tentativa fora dessas regras lança `PermissionDeniedError` e registra evento de auditoria.
    """
    allowed = False

    if authenticated_user.role == "coordinator":
        allowed = True
    elif authenticated_user.role == "advisor" and target_student_id in authenticated_user.advisee_uids:
        allowed = True
    elif authenticated_user.role == "student" and authenticated_user.uid == target_student_id:
        allowed = True

    if not allowed:
        if audit_logger:
            audit_logger.log_event(
                event_type="UNAUTHORIZED_IDOR_ATTEMPT",
                user_uid=authenticated_user.uid,
                target_resource=target_student_id,
                action=action,
                allowed=False
            )
        raise PermissionDeniedError(
            f"HTTP 403 Forbidden: Usuário '{authenticated_user.uid}' (papel: {authenticated_user.role}) "
            f"não tem permissão para acessar o recurso do estudante '{target_student_id}'."
        )

    if audit_logger:
        audit_logger.log_event(
            event_type="AUTHORIZED_RESOURCE_ACCESS",
            user_uid=authenticated_user.uid,
            target_resource=target_student_id,
            action=action,
            allowed=True
        )

    return True


# Banco de dados simulado de estudantes do ThesisFlow
STUDENT_DATABASE = {
    "student_123": {
        "name": "Ana Silva",
        "email": "ana.silva@aluno.unipampa.edu.br",
        "thesis_title": "Modelagem de Ameaças em Sistemas Acadêmicos",
        "advisor_uid": "advisor_001",
        "status": "Em andamento"
    },
    "student_456": {
        "name": "Carlos Souza",
        "email": "carlos.souza@aluno.unipampa.edu.br",
        "thesis_title": "Verificação Formal de Contratos Inteligentes",
        "advisor_uid": "advisor_002",
        "status": "Qualificado"
    }
}


def get_student_profile(authenticated_user: UserContext, requested_student_id: str, audit_logger: Optional[AuditLogger] = None) -> Dict[str, Any]:
    """
    Endpoint de serviço do ThesisFlow: GET /students/{student_id}/profile
    Garante autorização no servidor antes de consultar a base de dados.
    """
    # 1. Validação estrita de autorização no servidor (Prevenção de IDOR)
    verify_resource_ownership(authenticated_user, requested_student_id, action="GET_PROFILE", audit_logger=audit_logger)

    # 2. Busca do recurso após autorização confirmada
    student_data = STUDENT_DATABASE.get(requested_student_id)
    if not student_data:
        raise KeyError(f"Estudante '{requested_student_id}' não encontrado.")

    return student_data
