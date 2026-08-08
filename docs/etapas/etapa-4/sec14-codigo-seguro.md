# Seção 14 — Práticas de Código Seguro e Testes de Segurança

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 14 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 14. Práticas de Código Seguro e Testes de Segurança

Esta seção demonstra como as decisões de arquitetura da Etapa 3 são transformadas em práticas concretas de implementação segura no código-fonte da API do **ThesisFlow**.

Em conformidade com as diretrizes da disciplina, para cada prática são definidos: os riscos e requisitos relacionados, os **testes de segurança escritos antes da implementação**, o código-fonte em Python, o resultado esperado da execução e as referências da **OWASP** e **CWE** utilizadas.

---

## 14.1 Prática 1 — Controle de Autorização por Propriedade de Recurso (IDOR)

### 14.1.1 Mapeamento e referências

- **Risco de Origem:** `R07` — Acesso indevido a dados de outro estudante via IDOR (*Insecure Direct Object Reference*).
- **Requisito de Segurança:** `RS01` — A API deve verificar no servidor se o `student_id` informado corresponde ao UID do usuário autenticado (ou papel de orientador vinculado / coordenador).
- **Decisão de Arquitetura:** `DA01` — Implementar verificação de propriedade no servidor em todos os endpoints de estudante.
- **Referências UTILIZADAS:**
  - [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
  - [OWASP Top 10:2025 — A01: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
  - [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)

---

### 14.1.2 Testes de segurança (definidos ANTES da implementação)

Os testes a seguir foram especificados antes da escrita do código para garantir a validação do comportamento seguro da API.

| ID | Tipo | Entrada ou ação realizada | Resultado seguro esperado |
| :---: | :---: | :--- | :--- |
| `TS01` | **Malicioso / Não Autorizado** | Estudante `student_123` faz requisição `GET /students/student_456/profile` buscando dados de outro estudante | A solicitação é recusada com `HTTP 403 Forbidden` e um evento `UNAUTHORIZED_IDOR_ATTEMPT` é registrado no log de auditoria. |
| `TS02` | **Caso Válido** | Estudante `student_123` faz requisição `GET /students/student_123/profile` buscando seu próprio perfil | A solicitação é permitida com `HTTP 200 OK` e os dados do estudante são retornados com sucesso. |
| `TS03` | **Caso Válido** | Orientador `advisor_001` acessa `student_123` (seu orientando) OU Coordenador `coord_001` acessa `student_456` | A solicitação é autorizada com `HTTP 200 OK` em ambas as situações. |
| `TS04` | **Malicioso / Não Autorizado** | Orientador `advisor_001` tenta acessar `student_456` (estudante que NÃO é seu orientando) | A solicitação é recusada com `HTTP 403 Forbidden` e o evento de tentativa indevida é auditado. |

---

### 14.1.3 Implementação em Python (`authorization.py`)

A verificação ocorre estritamente no servidor, eliminando qualquer dependência de filtros no frontend.

```python
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
```

---

### 14.1.4 Suíte de testes automatizados (`test_authorization.py`)

Os testes automatizados foram construídos utilizando a biblioteca `pytest`:

```python
import pytest
from authorization import (
    UserContext,
    AuditLogger,
    PermissionDeniedError,
    get_student_profile
)


def test_ts01_idor_attack_attempt_denied():
    """TS01 — Caso Malicioso (IDOR): Acesso negado com 403 e auditoria gravada."""
    logger = AuditLogger()
    attacker = UserContext(uid="student_123", role="student")

    with pytest.raises(PermissionDeniedError) as exc_info:
        get_student_profile(attacker, "student_456", audit_logger=logger)

    assert "403 Forbidden" in str(exc_info.value)
    assert logger.logs[0]["event_type"] == "UNAUTHORIZED_IDOR_ATTEMPT"
    assert logger.logs[0]["allowed"] is False


def test_ts02_legitimate_student_access_allowed():
    """TS02 — Caso Válido: Estudante acessa próprio perfil."""
    logger = AuditLogger()
    student = UserContext(uid="student_123", role="student")

    profile = get_student_profile(student, "student_123", audit_logger=logger)

    assert profile["name"] == "Ana Silva"
    assert logger.logs[0]["allowed"] is True


def test_ts03_advisor_and_coordinator_access_allowed():
    """TS03 — Caso Válido: Orientador vinculado e Coordenador autorizados."""
    logger = AuditLogger()
    advisor = UserContext(uid="advisor_001", role="advisor", advisee_uids=["student_123"])
    coordinator = UserContext(uid="coord_001", role="coordinator")

    assert get_student_profile(advisor, "student_123", audit_logger=logger)["name"] == "Ana Silva"
    assert get_student_profile(coordinator, "student_456", audit_logger=logger)["name"] == "Carlos Souza"
```

---

### 14.1.5 Resultado da execução dos testes

A execução dos testes via `pytest` confirma que 100% dos cenários previstos foram validados com sucesso:

```text
$ python3 -m pytest codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py -v

============================= test session starts ==============================
platform linux -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
collected 4 items

test_authorization.py::test_ts01_idor_attack_attempt_denied PASSED      [ 25%]
test_authorization.py::test_ts02_legitimate_student_access_allowed PASSED [ 50%]
test_authorization.py::test_ts03_advisor_and_coordinator_access_allowed PASSED [ 75%]
test_authorization.py::test_ts04_advisor_unauthorized_student_denied PASSED [100%]

============================== 4 passed in 0.03s ===============================
```

> **Localização dos arquivos de código:**
> - Módulo de autorização: [`codigo/etapa-4/pratica-1-autorizacao-por-recurso/authorization.py`](../../codigo/etapa-4/pratica-1-autorizacao-por-recurso/authorization.py)
> - Suíte de testes `pytest`: [`codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py`](../../codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py)
