# Etapa 1 — Seção 2: Usuários, Ativos e Pontos de Interação

---

## 3. Usuários, ativos e pontos de interação

### 3.1 Usuários e perfis de acesso

| Usuário | Papel no sistema | Principais ações |
| :--- | :---: | :--- |
| **Estudante** | `student` | Registrar atividades, fazer upload de comprovantes, consultar plano de trabalho, acompanhar status acadêmico |
| **Orientador** | `advisor` | Validar atividades creditáveis, acompanhar progresso do orientando, registrar produções científicas |
| **Coordenador** | `coordinator` | Gerenciar usuários e papéis, definir tipos de atividades, aprovar extensões de prazo, emitir relatórios |
| **Administrador de sistema** | acesso via *bootstrap* | Criar a conta inicial de coordenador via script privilegiado (`bootstrap_admin.py`) |

---

### 3.2 Dados pessoais e sensíveis

| Dado | Quem tem acesso | Por que é sensível |
| :--- | :--- | :--- |
| Nome, e-mail e matrícula do estudante | Orientador, Coordenador, o próprio estudante | Dados pessoais protegidos pela `LGPD` |
| Credenciais de acesso (token `JWT`) | Usuário e `Firebase Auth` | Permitem acesso total à conta se comprometidos |
| Comprovantes de atividade (arquivos) | Estudante (upload), Orientador (validação) | Podem conter diplomas, certidões, artigos não publicados |
| Produções científicas e publicações | Orientador, Coordenador | Podem incluir trabalhos ainda não publicados |
| Status acadêmico inferido | Coordenador, Orientador, Estudante | Revela situação de risco ou atraso |
| Histórico de aprovações e validações | Coordenador, Orientador | Permite rastrear responsabilidades |
| Logs de auditoria | Coordenador, Administrador | Registros de todas as operações sensíveis |

---

### 3.3 Ativos importantes

Os ativos listados abaixo podem causar prejuízo significativo caso sejam acessados, alterados, destruídos ou indisponibilizados de forma indevida:

1. **Credenciais e tokens de autenticação** — comprometê-los permite assumir a identidade de qualquer usuário.
2. **Dados pessoais dos estudantes** — exposição viola privacidade e pode acarretar consequências legais (`LGPD`).
3. **Comprovantes de atividades creditáveis** — falsificação pode levar à validação indevida de créditos.
4. **Registros de validação e aprovação** — alteração pode modificar o progresso acadêmico de um estudante.
5. **Planos de trabalho e prazos** — adulteração pode mascarar atrasos ou criar inconsistências.
6. **Logs de auditoria** — sem eles, não é possível responsabilizar autores de operações incorretas.
7. **Status acadêmico inferido** — alteração pode permitir que estudantes inelegíveis avancem para a defesa.
8. **Permissões e papéis (`RBAC`)** — elevação indevida de privilégios compromete toda a segurança.

---

### 3.4 Pontos de interação e componentes

| Componente | Função | Tecnologia |
| :--- | :--- | :--- |
| **Frontend React** | Interface web utilizada pelos usuários | `React 18` + `TypeScript` + `Vite` |
| **API REST (backend)** | Processa todas as regras de negócio e operações | `FastAPI` (`Python 3.11+`) |
| **Firebase Authentication** | Valida identidade e emite tokens `JWT` | `Firebase Auth` (Google) |
| **Firestore** | Armazena todos os dados estruturados do sistema | `Firebase Firestore` (NoSQL) |
| **Firebase Storage** | Armazena os arquivos comprovantes das atividades | `Firebase Storage` (Google) |
| **Motor de inferência lógica** | Infere status acadêmico via cláusulas Horn | Implementação própria em `Python` |
| **Aspecto `@authorize`** | Controla acesso baseado em papel (`RBAC`) | Decorator `Python` (*before advice*) |
| **Aspecto `@audit`** | Registra todas as operações sensíveis | Decorator `Python` + `inspect` (*after advice*) |
| **Aspecto `@trigger_alerts`** | Envia notificações automáticas | Decorator `Python` (*after advice*) |
