# Etapa 1 — Seção 3: Visão Geral da Arquitetura

---

## 4. Visão geral da arquitetura

O **ThesisFlow** segue uma arquitetura em camadas estrita: `Router` → `Service` → `Repository` → `Infrastructure`. O frontend `React` se comunica com o backend `FastAPI` via `HTTP REST`. A autenticação é delegada ao `Firebase Authentication`, que emite tokens `JWT` verificados pela API a cada requisição. Os dados persistidos ficam no `Firestore`. Arquivos de comprovantes são armazenados no `Firebase Storage`.

A segurança da API é reforçada pelo aspecto `@authorize`, que valida o papel do usuário autenticado antes de qualquer operação sensível. O aspecto `@audit` registra automaticamente todas as operações de criação e alteração de dados.

---

### Diagrama de Contexto

![Diagrama de Contexto do ThesisFlow](../../../diagramas/etapa-1/diagrama-contexto.png)
*Figura 1: Diagrama de Contexto do sistema ThesisFlow*

---

### Diagrama de Fluxo de Dados

O diagrama abaixo ilustra dois fluxos críticos para a segurança: a autenticação/autorização e o registro de atividade com upload de comprovante.

![Diagrama de Fluxo de Dados](../../../diagramas/etapa-1/diagrama-fluxo-dados.png)
*Figura 2: Diagrama de Fluxo de Dados (Autenticação, Autorização e Upload de Comprovante)*

---

### Visão simplificada da arquitetura

```text
Usuário (browser)
       │
       ▼
Frontend React
       │ HTTP + Bearer token JWT
       ▼
API FastAPI ──────────────────────────────────────────────────┐
  │ @authorize → verifica role (RBAC)                         │
  │ @audit     → registra operação                            │
  │ @trigger_alerts → notifica partes interessadas            │
  │                                                           │
  ├─▶ Service Layer (regras de negócio)                       │
  │       └─▶ resolver.query() → Motor Lógico (inferência)   │
  │       └─▶ Repository → Firestore (dados estruturados)     │
  │       └─▶ Firebase Storage (comprovantes)                 │
  │                                                           │
  └─▶ Firebase Authentication (validação de token JWT) ───────┘
```
