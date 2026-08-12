# Seção 12 — Requisitos de Segurança e Mapeamento de Vulnerabilidades

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 12 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 12. Requisitos de Segurança e Mapeamento de Vulnerabilidades Catalogadas

Esta seção deriva três requisitos de segurança a partir dos riscos críticos e altos prioritários identificados na Etapa 2 (`R07`, `R01` e `R03`) e mapeia cada requisito a uma vulnerabilidade catalogada em referências reconhecidas (CWE, OWASP Top 10 e OWASP ASVS). Estes requisitos fundamentam diretamente a implementação prática e os testes de código seguro desenvolvidos na Etapa 4 (`codigo/etapa-4/`).

---

### 12.1 Requisitos de segurança (RS01–RS03)

Os requisitos foram derivados dos três riscos de maior prioridade do sistema ThesisFlow: **R07** (IDOR em dados do estudante — 1º), **R01** (roubo/interceptação de token JWT — 2º) e **R03** (substituição/adulteração de comprovante — 3º).

| ID | Risco de origem | Requisito de segurança | Critério de verificação |
| :---: | :---: | :--- | :--- |
| `RS01` | `R07` | **Autorização por Recurso:** A API deve verificar, em todos os endpoints que retornam dados de um estudante, que o `student_id` informado na requisição corresponde ao UID do usuário autenticado. Orientadores podem acessar apenas dados de seus próprios orientandos; coordenadores têm acesso irrestrito por papel. | Requisição com `student_id` de outro estudante deve retornar HTTP `403 Forbidden` e registrar o evento no log de auditoria. Testes automatizados com papéis `student`, `advisor` e `coordinator` devem validar o isolamento completo de acesso. |
| `RS02` | `R01` | **Proteção de Sessão e Credenciais:** O sistema deve armazenar tokens JWT exclusivamente em cookies `httpOnly` e `Secure`, com TTL máximo de 1 hora, e invalidá-los no servidor no momento do logout. Nenhum token deve ser acessível via JavaScript no frontend. | As flags `httpOnly` e `Secure` do cookie de sessão devem ser validadas via DevTools/testes de integração. Após o logout, qualquer requisição subsequente com o token revogado deve retornar HTTP `401 Unauthorized`. A tentativa de leitura do cookie via `document.cookie` no console do navegador deve retornar vazio. |
| `RS03` | `R03` | **Integridade e Upload Seguro:** Após o upload de um comprovante, o sistema deve calcular e armazenar o hash `SHA-256` do arquivo e impedir qualquer substituição do arquivo original no Firebase Storage. O orientador deve poder verificar se o hash armazenado no Firestore coincide com o do arquivo presente no Storage. | Tentativa de sobrescrever o arquivo via `PUT` diretamente no Storage deve retornar HTTP `403` pelas regras do Firebase. O hash armazenado deve coincidir perfeitamente com o `SHA-256` do arquivo. Envio de arquivo com MIME-Type diferente de `application/pdf`, `image/jpeg` ou `image/png` deve retornar HTTP `422 Unprocessable Entity`. |

---

### 12.2 Mapeamento de vulnerabilidades catalogadas (VM01–VM03)

Para cada requisito, foi identificada a vulnerabilidade correspondente em catálogos e referências reconhecidas da área de segurança de software.

| ID | Risco | Vulnerabilidade ou categoria | Referência | Relação com o ThesisFlow |
| :---: | :---: | :--- | :--- | :--- |
| `VM01` | `R07` | **Insecure Direct Object Reference (IDOR)** — Autorização quebrada por chave controlada pelo usuário | **CWE-639:** Authorization Bypass Through User-Controlled Key<br>**OWASP Top 10:2021 — A01:** Broken Access Control | A API do ThesisFlow consulta recursos de estudantes com base no `student_id` passado no parâmetro da URL sem validar se o ID pertence ao usuário logado. Isso permite que um estudante mal-intencionado altere o identificador via GET/PUT e acesse ou modifique dados de outros estudantes. |
| `VM02` | `R01` | **Cookie sensível sem flag `HttpOnly` / Autenticação imprópria** | **CWE-1004:** Sensitive Cookie Without 'HttpOnly' Flag<br>**CWE-287:** Improper Authentication<br>**OWASP Top 10:2021 — A07:** Identification and Authentication Failures | Se o token JWT for armazenado em `localStorage` ou em cookies sem a flag `httpOnly`, ele fica exposto a captura caso ocorra uma vulnerabilidade de Cross-Site Scripting (XSS). A ausência de uma lista de revogação (*blacklisting*) no servidor prolonga a janela de ataque após o logout. |
| `VM03` | `R03` | **Upload irrestrito de arquivo / Ausência de controle de integridade** | **CWE-434:** Unrestricted Upload of File with Dangerous Type<br>**OWASP ASVS v4 — V12.2:** File Integrity | O armazenamento de arquivos sem regras de imutabilidade e sem verificação criptográfica de hash permite que um usuário substitua um comprovante já enviado por um documento forjado ou alterado antes da validação final do orientador. |

---

### 12.3 Referências

- [CWE-639](https://cwe.mitre.org/data/definitions/639.html) — Authorization Bypass Through User-Controlled Key
- [CWE-1004](https://cwe.mitre.org/data/definitions/1004.html) — Sensitive Cookie Without 'HttpOnly' Flag
- [CWE-287](https://cwe.mitre.org/data/definitions/287.html) — Improper Authentication
- [CWE-434](https://cwe.mitre.org/data/definitions/434.html) — Unrestricted Upload of File with Dangerous Type
- [OWASP Top 10:2021 — A01](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) — Broken Access Control
- [OWASP Top 10:2021 — A07](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) — Identification and Authentication Failures
- [OWASP ASVS v4 — V12.2](https://github.com/OWASP/ASVS/blob/master/4.0/en/0x20-V12-Files-Resources.md) — File Integrity