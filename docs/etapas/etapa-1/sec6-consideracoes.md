# Seção 6 — Considerações Finais da Etapa 1

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 6 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 6. Considerações Finais

### 6.1 Ameaças mais preocupantes

As ameaças consideradas mais críticas no contexto do **ThesisFlow** são a exposição de dados por IDOR (`T07`), o roubo/interceptação de token JWT (`T01`) e a falsificação de comprovantes acadêmicos (`T03`). Essas ameaças afetam diretamente a integridade, confidencialidade e não-repúdio do sistema, podendo comprometer a legitimidade de todo o processo acadêmico.

- **Ameaça `T07` (IDOR):** É a mais crítica devido à baixa complexidade de exploração — qualquer estudante autenticado pode alterar identificadores sequenciais em requisições HTTP GET. Seu impacto é gravíssimo, pois resulta em exposição em massa de dados pessoais e acadêmicos, violando diretrizes diretas da `LGPD`.
- **Ameaça `T01` (Roubo de Token JWT):** Apresenta alto impacto pela abrangência de privilégios. O comprometimento do token de um coordenador expõe todo o ambiente administrativo, enquanto o de um orientador expõe as informações e a gestão de créditos de seus orientandos.
- **Ameaça `T03` (Substituição de Comprovante):** Compromete a confiabilidade das validações de créditos quando o ambiente de armazenamento em nuvem (`Firebase Storage`) não aplica travas de imutabilidade.

---

### 6.2 Ativos mais importantes

Os ativos mais valiosos do ThesisFlow são as **credenciais e tokens de autenticação** (`JWT`), os **comprovantes de atividades e artigos** (arquivos armazenados no `Firebase Storage`), os **registros de validação de créditos** e os **logs imutáveis de auditoria** (`@audit`). Esses elementos sustentam todas as decisões acadêmicas — a integridade da emissão do diploma ao final do programa de mestrado depende estritamente da confiabilidade e imutabilidade dessas informações.

---

### 6.3 Tipos de abuso com maior impacto

Os casos de abuso identificados com maior potencial de dano institucional são:

- **`CA03` (Cadastro de Falso Orientador):** Permite acesso prolongado e não autorizado a dados sensíveis de múltiplos estudantes, apresentando elevada dificuldade de detecção inicial.
- **`CA01` (Forja de Comprovantes Acadêmicos):** Compromete a concessão de créditos, podendo levar à aprovação indevida de um estudante sem o cumprimento dos requisitos do programa.
- **`CA06` (Elevação Involuntária de Privilégios):** Subverte os controles de acesso por papéis (`RBAC`), permitindo a execução de operações administrativas por usuários não autorizados.

---

### 6.4 Principais dificuldades e aprendizados da análise

A principal dificuldade consistiu em diferenciar ameaças genéricas de cenários vulneráveis concretos do **ThesisFlow**. Por ser um software desenvolvido pelo próprio grupo, foi possível identificar pontos falhos específicos de implementação — como a vulnerabilidade na flag de configuração `ASPECTS_ENABLED` (que pode desabilitar os logs de auditoria em runtime) e a falta de regras de imutabilidade nos arquivos enviados ao `Storage`.

A aplicação da metodologia **STRIDE** permitiu estruturar a análise sob seis perspectivas complementares, revelando fragilidades que passariam despercebidas em uma análise puramente funcional. Por fim, a categoria **Repudiation** exigiu cuidado especial, pois sua mitigação depende da imutabilidade dos logs de auditoria — elemento que fundamenta a transição do projeto para a análise de riscos baseada no **NIST CSF 2.0** na Etapa 2.