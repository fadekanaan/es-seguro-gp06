# Seção 12 — Requisitos de Segurança e Mapeamento de Vulnerabilidades

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 12 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 12. Requisitos de Segurança e Mapeamento de Vulnerabilidades Catalogadas

Esta seção deriva três requisitos de segurança a partir dos riscos críticos prioritários identificados na Etapa 2 e mapeia cada requisito a uma vulnerabilidade catalogada em referências reconhecidas.

---

### 12.1 Requisitos de segurança (RS01–RS03)

Os requisitos foram derivados dos três riscos de maior prioridade: **R07** (IDOR — 1º), **R01** (roubo de token JWT — 2º) e **R03** (substituição de comprovante — 3º).

| ID | Risco de origem | Requisito de segurança | Critério de verificação |
| :---: | :---: | :--- | :--- |
| `RS01` | `R07` | A API deve verificar, em todos os endpoints que retornam dados de um estudante, que o `student_id` informado na requisição corresponde ao UID do usuário autenticado. Orientadores podem acessar apenas dados de seus próprios orientandos; coordenadores têm acesso irrestrito por papel. | Requisição com `student_id` de outro estudante deve retornar HTTP `403 Forbidden` e registrar evento no log de auditoria. Testes com papel `student`, `advisor` e `coordinator` devem produzir os resultados esperados descritos nos critérios de cada papel. |
| `RS02` | `R01` | O sistema deve armazenar tokens JWT exclusivamente em cookies `httpOnly` e `Secure`, com TTL máximo de 1 hora, e invalidá-los no servidor no momento do logout. Nenhum token deve ser acessível via JavaScript no frontend. | O cookie de sessão deve ter as flags `httpOnly` e `Secure` verificadas no DevTools. Após o logout, o token deve ser rejeitado com HTTP `401` em qualquer requisição subsequente. Acesso ao cookie via `document.cookie` no console do browser deve ser bloqueado. |
| `RS03` | `R03` | Após o upload de um comprovante, o sistema deve calcular e armazenar o hash `SHA-256` do arquivo e impedir qualquer substituição do arquivo original no Firebase Storage. O orientador deve poder verificar que o hash armazenado coincide com o arquivo presente no Storage no momento da validação. | Tentativa de sobrescrever o arquivo via `PUT` diretamente no Storage deve retornar HTTP `403` pelas regras do Firebase. O hash armazenado no Firestore deve coincidir com o resultado de `SHA-256` do arquivo baixado do Storage. Upload de arquivo com content-type diferente de `application/pdf`, `image/jpeg` ou `image/png` deve retornar HTTP `422`. |

---

### 12.2 Mapeamento de vulnerabilidades catalogadas (VM01–VM03)

Para cada requisito, foi identificada a vulnerabilidade correspondente em catálogos e referências reconhecidas da área de segurança de software.

| ID | Risco | Vulnerabilidade ou categoria | Referência | Relação com o ThesisFlow |
| :---: | :---: | :--- | :--- | :--- |
| `VM01` | `R07` | **Insecure Direct Object Reference (IDOR)** — Autorização quebrada por chave controlada pelo usuário | CWE-639: Authorization Bypass Through User-Controlled Key; OWASP Top 10:2025 — A01: Broken Access Control | A API do ThesisFlow retorna recursos de estudante com base no `student_id` da URL sem verificar se o recurso pertence ao usuário autenticado. Qualquer estudante pode modificar o identificador em uma requisição GET e obter dados de outro estudante. |
| `VM02` | `R01` | **Cookie sensível sem flag `HttpOnly` / Autenticação imprópria** | CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag; CWE-287: Improper Authentication; OWASP Top 10:2025 — A07: Identification and Authentication Failures | Se o token JWT for armazenado em `localStorage` ou em cookie sem a flag `httpOnly`, ele pode ser capturado por scripts maliciosos injetados via XSS. A ausência de revogação server-side prolonga a janela de comprometimento após o logout. |
| `VM03` | `R03` | **Upload irrestrito de arquivo / Ausência de controle de integridade** | CWE-434: Unrestricted Upload of File with Dangerous Type; OWASP ASVS v4 — V12.2: File Integrity | O Firebase Storage sem regras de imutabilidade permite que um estudante autenticado sobrescreva o arquivo comprovante após o upload inicial, substituindo um documento legítimo por um forjado antes ou após a validação do orientador. |

---

### 12.3 Referências

- [CWE-639](https://cwe.mitre.org/data/definitions/639.html) — Authorization Bypass Through User-Controlled Key
- [CWE-1004](https://cwe.mitre.org/data/definitions/1004.html) — Sensitive Cookie Without 'HttpOnly' Flag
- [CWE-287](https://cwe.mitre.org/data/definitions/287.html) — Improper Authentication
- [CWE-434](https://cwe.mitre.org/data/definitions/434.html) — Unrestricted Upload of File with Dangerous Type
- [OWASP Top 10:2025 — A01](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) — Broken Access Control
- [OWASP Top 10:2025 — A07](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) — Identification and Authentication Failures
- [OWASP ASVS v4 — V12.2](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x20-V12-Files-Resources.md) — File Integrity
