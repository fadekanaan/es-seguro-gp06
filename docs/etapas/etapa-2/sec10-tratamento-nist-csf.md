# Seção 10 — Tratamento dos Riscos e Mapeamento para o NIST CSF 2.0

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 10 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 10. Tratamento dos Riscos e Mapeamento para o NIST CSF 2.0

Esta seção define as estratégias de tratamento para cada risco identificado na Seção 8, mapeia os riscos para as funções do NIST Cybersecurity Framework 2.0, apresenta o plano de tratamento com controles concretos, responsáveis e formas de verificação, estabelece a ordem inicial de implementação e estima o risco residual esperado após a aplicação dos controles.

---

### 10.1 Estratégias de tratamento

Para cada risco, foi selecionada uma estratégia principal com base na natureza da vulnerabilidade, na viabilidade técnica dos controles e no contexto acadêmico do **ThesisFlow**.

| Risco | Nível | Estratégia | Justificativa |
| :---: | :---: | :---: | :--- |
| `R01` | **Crítico** | Reduzir | Cookies `httpOnly` e TTL curto de token reduzem a janela de exploração; a eliminação completa dependeria de mudança de protocolo |
| `R02` | **Alto** | Reduzir | Validação de domínio institucional e aprovação explícita do coordenador são medidas viáveis sem eliminar o fluxo de cadastro |
| `R03` | **Crítico** | Reduzir | Imutabilidade no `Firebase Storage` e verificação de hash são implementáveis via configuração e código sem remover a funcionalidade de upload |
| `R04` | **Médio** | Reduzir | A cobertura completa dos decorators `@authorize` nos endpoints de atualização resolve a falha pontual sem redesenho da API |
| `R05` | **Alto** | Evitar | Remover a flag `ASPECTS_ENABLED["audit"]` do ambiente de produção elimina a condição que origina o risco; a auditoria torna-se não-opcional |
| `R06` | **Médio** | Reduzir | Cloud Audit Logs imutáveis do Firestore fornecem evidências irrefutáveis de operações administrativas sem alterar os fluxos existentes |
| `R07` | **Crítico** | Reduzir | Verificação de propriedade do recurso no servidor é prática padrão e correção direta, sem remover nenhuma funcionalidade |
| `R08` | **Alto** | Reduzir | Signed URLs com validade de 15 minutos já estão disponíveis no Firebase Admin SDK; nenhuma reestruturação de serviço é necessária |
| `R09` | **Alto** | Reduzir | Rate limiting por UID e cache de resultados do motor lógico reduzem probabilidade e impacto sem degradar a experiência legítima |
| `R10` | **Médio** | Reduzir | Limitar tamanho e tipo de arquivo no endpoint de upload é configuração simples; o vetor é menos crítico e dependente de intenção maliciosa |
| `R11` | **Alto** | Reduzir | Auditoria sistemática de todos os endpoints e correção dos decorators `@authorize` resolve a falha estrutural de autorização |
| `R12` | **Médio** | Evitar | Remover qualquer endpoint HTTP que invoque `bootstrap_admin.py` e documentar execução exclusivamente local elimina a superfície de ataque |

---

### 10.2 Funções do NIST CSF 2.0

O NIST Cybersecurity Framework 2.0 organiza os resultados de segurança em seis funções. A tabela abaixo as descreve no contexto específico do **ThesisFlow**, diferenciando função, resultado esperado e exemplos de controles.

| Função | Finalidade geral | Resultado esperado no ThesisFlow | Exemplos de controles |
| :---: | :--- | :--- | :--- |
| **Govern** | Definir políticas, responsabilidades e critérios de decisão de segurança | Política de uso aceitável definida; responsáveis por cada risco identificados; critérios para aceitar ou escalar riscos documentados | Política de auditoria obrigatória; atribuição de papéis de segurança por componente |
| **Identify** | Conhecer ativos, dependências, vulnerabilidades e riscos do sistema | Ativos críticos mapeados (Seção 3); riscos R01–R12 registrados; vulnerabilidades CWE/OWASP identificadas | Registro de riscos; mapeamento de componentes e pontos de interação |
| **Protect** | Implementar salvaguardas para reduzir probabilidade ou impacto dos riscos | Acesso protegido por autenticação e autorização; dados protegidos em trânsito e em repouso; uploads validados | `@authorize`; cookies `httpOnly`; imutabilidade Storage; rate limiting; validação de tipo e tamanho de arquivo |
| **Detect** | Identificar eventos suspeitos, falhas e possíveis incidentes em tempo hábil | Tentativas de IDOR, flooding e elevação de privilégios registradas e alertadas | Logs do aspecto `@audit`; alertas de HTTP 403; monitoramento de taxa de requisições |
| **Respond** | Conter, analisar, comunicar e tratar incidentes após detecção | Conta comprometida bloqueada; token revogado; coordenador notificado; incidente registrado | Endpoint de logout com revogação server-side; bloqueio temporário por UID; notificação automática |
| **Recover** | Restaurar serviços e dados após incidente e reduzir prejuízos | Sistema restaurado ao estado íntegro; usuários afetados notificados; comprovantes recuperáveis | Backup periódico do Firestore; restauração de cota do Storage; restauração de comprovantes a partir de hash |

---

### 10.3 Mapeamento dos riscos para as funções do NIST CSF

A tabela indica quais funções do NIST CSF são relevantes para o tratamento de cada risco. A marcação reflete uma análise contextualizada — não uma aplicação automática de todas as funções a todos os riscos.

| Risco | Govern | Identify | Protect | Detect | Respond | Recover |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `R01` | | | ✓ | ✓ | ✓ | ✓ |
| `R02` | ✓ | ✓ | ✓ | | ✓ | |
| `R03` | | | ✓ | ✓ | ✓ | ✓ |
| `R04` | | | ✓ | ✓ | ✓ | |
| `R05` | ✓ | | ✓ | | ✓ | |
| `R06` | ✓ | | ✓ | ✓ | ✓ | |
| `R07` | | | ✓ | ✓ | ✓ | |
| `R08` | | | ✓ | ✓ | ✓ | |
| `R09` | | | ✓ | ✓ | ✓ | ✓ |
| `R10` | | | ✓ | ✓ | ✓ | ✓ |
| `R11` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `R12` | ✓ | ✓ | ✓ | | ✓ | |

---

### 10.4 Plano de tratamento

Para cada risco, o plano especifica os controles de forma concreta e observável, os responsáveis pela implementação e as formas de verificar que os controles existem e funcionam.

| Risco | Estratégia | Controles propostos | Funções NIST | Responsáveis | Evidências e verificação |
| :---: | :---: | :--- | :--- | :--- | :--- |
| `R01` | Reduzir | 1. Armazenar JWT em cookie `httpOnly` e `Secure` (não em `localStorage`); 2. Configurar TTL do token em 1 hora com renovação silenciosa; 3. Implementar endpoint de logout que invalida o token no servidor; 4. Adicionar headers `Content-Security-Policy` no React para bloquear inline scripts | Protect, Detect, Respond, Recover | Dev frontend + Dev backend | Teste de logout com token invalidado retorna HTTP 401; cookie sem flag `httpOnly` ausente no DevTools; scan de XSS sem injeção bem-sucedida |
| `R02` | Reduzir | 1. Validar que o e-mail do orientador pertence ao domínio `@unipampa.edu.br` ou similar no cadastro; 2. Exigir aprovação explícita do coordenador para ativar conta de orientador; 3. Nenhum estudante pode ser vinculado a orientador sem aprovação ativa | Govern, Identify, Protect, Respond | Dev backend + Coordenador do programa | Teste de cadastro com e-mail externo é rejeitado; conta de orientador sem aprovação não aparece nas listagens; processo de aprovação documentado |
| `R03` | Reduzir | 1. Configurar regra no `Firebase Storage` que bloqueia sobrescrição de arquivo existente (`!resource.data.exists()`); 2. Calcular e armazenar hash `SHA-256` do arquivo no momento do upload; 3. Verificar hash no momento da validação pelo orientador | Protect, Detect, Respond, Recover | Dev backend + Configuração Firebase | Tentativa de `PUT` no mesmo caminho retorna HTTP 403 do Storage; hash armazenado no Firestore coincide com arquivo no Storage; teste de validação com hash divergente bloqueia a operação |
| `R04` | Reduzir | 1. Auditar todos os endpoints `PUT`/`PATCH` relacionados ao plano de trabalho; 2. Garantir decorator `@authorize(role=["advisor", "coordinator"])` em cada um; 3. Registrar toda alteração do plano via `@audit` | Protect, Detect, Respond | Dev backend | Script de auditoria de endpoints sem resultado de falha; log `@audit` registra quem alterou e quando; teste com token de `student` retorna HTTP 403 |
| `R05` | Evitar | 1. Remover a flag `ASPECTS_ENABLED["audit"]` do código de produção ou torná-la constante `True` não configurável em runtime; 2. Proteger configurações de auditoria via variável de ambiente sem exposição à API; 3. Ativar Cloud Audit Logs do Firebase como camada imutável adicional | Govern, Protect, Respond | Dev backend + Infraestrutura | Flag ausente no código de produção; Cloud Audit Logs ativo no console Firebase; tentativa de desabilitar via variável de ambiente sem efeito |
| `R06` | Reduzir | 1. Habilitar Cloud Audit Logs do Firestore (nível de dados, não apenas metadados); 2. Exportar logs para bucket imutável com retenção mínima de 1 ano; 3. Garantir que o `@audit` registre o UID completo do coordenador em cada operação administrativa | Govern, Protect, Detect, Respond | Infraestrutura + Dev backend | Cloud Audit Logs ativo no console Firebase; bucket de exportação com política de retenção; log de operação administrativa inclui `uid`, `timestamp` e `action` |
| `R07` | Reduzir | 1. Implementar verificação de propriedade em todos os endpoints de leitura: `student.uid == authenticated_user.uid` para estudantes; 2. Para orientadores, verificar se o estudante é seu orientando; 3. Registrar toda tentativa de acesso negado via `@audit` | Protect, Detect, Respond | Dev backend | Teste com `student_id` de outro estudante retorna HTTP 403; evento registrado no `@audit`; testes automatizados cobrem cenários de ID cruzado |
| `R08` | Reduzir | 1. Substituir URLs públicas de download por Signed URLs geradas on-demand via endpoint autenticado do backend; 2. Definir validade de 15 minutos por Signed URL; 3. Nunca expor a URL diretamente ao frontend sem passar pelo endpoint de geração | Protect, Detect, Respond | Dev backend + Configuração Firebase | Acesso com URL expirada retorna HTTP 403 do Storage; URL gerada sem autenticação no backend não é acessível; regras do Storage não permitem leitura pública |
| `R09` | Reduzir | 1. Implementar rate limiting por UID autenticado com `slowapi` (10 req/min) nos endpoints que invocam o motor lógico; 2. Implementar cache in-memory ou Redis dos resultados do motor com TTL de 5 minutos | Protect, Detect, Respond, Recover | Dev backend | Teste de 11 requisições consecutivas retorna HTTP 429 na 11ª; resultado cacheado retorna sem invocar o motor; logs de rate limit registram UID bloqueado |
| `R10` | Reduzir | 1. Validar `content-type` real do arquivo (não apenas extensão); 2. Definir tamanho máximo de 10 MB por arquivo; 3. Limitar uploads por estudante por período (ex.: 20 uploads por dia) | Protect, Detect, Respond, Recover | Dev backend | Teste com arquivo `.exe` retorna HTTP 422; arquivo de 50 MB retorna HTTP 413; 21º upload no mesmo dia retorna HTTP 429 |
| `R11` | Reduzir | 1. Criar script de auditoria que varre todos os endpoints FastAPI e verifica presença e correção do decorator `@authorize`; 2. Integrar script ao processo de revisão de código; 3. Remover o Swagger UI (`/docs`) do ambiente de produção | Govern, Identify, Protect, Detect, Respond | Dev backend + Processo de revisão | Script de auditoria sem falhas; endpoint `/docs` inacessível em produção; teste com token de `student` em endpoint de coordenador retorna HTTP 403 |
| `R12` | Evitar | 1. Remover qualquer rota HTTP que invoque `bootstrap_admin.py`; 2. Documentar que o script deve ser executado exclusivamente via terminal local na inicialização do ambiente; 3. Garantir que `BOOTSTRAP_SECRET` nunca esteja exposta em variáveis de ambiente de produção acessíveis remotamente | Govern, Identify, Protect, Respond | Dev backend + Infraestrutura | Nenhum endpoint HTTP responde ao script; variável `BOOTSTRAP_SECRET` ausente de logs e configurações expostas; processo de inicialização documentado no repositório |

---

### 10.5 Ordem inicial de implementação

A ordem considera: nível de criticidade, trivialidade de exploração, dependências técnicas, controles que reduzem múltiplos riscos e esforço de implementação estimado.

| Prioridade | Risco(s) | Controle principal | Justificativa da ordem |
| :---: | :---: | :--- | :--- |
| `1º` | `R07` | Verificação de propriedade do recurso em todos os endpoints GET de estudante | Crítico; trivial de explorar; correção direta sem redesenho; violação em massa da `LGPD` |
| `2º` | `R03` | Imutabilidade no Storage + hash `SHA-256` | Crítico; fraude de comprovante compromete a validade do programa inteiro; Storage é configuração |
| `3º` | `R01` | Cookie `httpOnly` + TTL de 1h + revogação server-side | Crítico; token comprometido habilita e amplifica R03, R05 e R11 |
| `4º` | `R11` + `R12` | Auditoria de decorators `@authorize` + remoção do endpoint bootstrap | Sistêmico; corrige a estrutura inteira de RBAC; R12 é remoção simples |
| `5º` | `R05` | Remoção da flag de auditoria + Cloud Audit Logs | Transversal: sem auditoria, os controles dos outros riscos tornam-se indetectáveis |
| `6º` | `R02` | Validação de domínio institucional + aprovação do coordenador | Alto impacto; requer mudança no fluxo de cadastro e processo humano |
| `7º` | `R08` | Signed URLs on-demand com validade de 15 minutos | Implementável via Firebase Admin SDK sem redesenho do Storage |
| `8º` | `R09` | Rate limiting + cache do motor lógico | Biblioteca `slowapi`; protege disponibilidade sem impactar experiência legítima |
| `9º` | `R04` + `R06` | Cobertura de `@authorize` em endpoints do plano + Cloud Audit Logs admin | Médio; corrige casos menos prováveis mas com impacto acadêmico relevante |
| `10º` | `R10` | Limites de tamanho e tipo no upload | Menor impacto relativo; configuração simples no endpoint existente |

---

### 10.6 Estimativa do risco residual

O risco residual representa o nível esperado de cada risco **após** a implementação dos controles propostos. As estimativas são teóricas — a confirmação real exige implementação, testes e obtenção de evidências.

| Risco | Nível inicial | Controle(s) principal(is) | Nível residual esperado | Condição para aceitar o residual |
| :---: | :---: | :--- | :---: | :--- |
| `R01` | **Crítico** (12) | Cookie `httpOnly`; TTL de 1h; revogação server-side | **Médio** (4–6) | Scan sem XSS bem-sucedido; TTL e revogação verificados em teste; cookie sem acesso via JS |
| `R02` | **Alto** (9) | Validação de domínio + aprovação do coordenador | **Baixo** (2–3) | Nenhum orientador ativo sem aprovação; teste de e-mail externo rejeitado |
| `R03` | **Crítico** (12) | Imutabilidade no Storage + hash `SHA-256` | **Médio** (4–6) | Regra de imutabilidade ativa e testada; hash verificado antes de cada validação |
| `R04` | **Médio** (6) | `@authorize` em todos os endpoints do plano de trabalho | **Baixo** (1–2) | Script de auditoria sem falhas; teste com `student` em endpoint de `advisor` retorna HTTP 403 |
| `R05` | **Alto** (8) | Remoção da flag + Cloud Audit Logs imutáveis | **Baixo** (2–3) | Flag ausente no código de produção; Cloud Audit Logs ativo e exportado para bucket imutável |
| `R06` | **Médio** (6) | Cloud Audit Logs Firestore + bucket de retenção | **Baixo** (2–3) | Logs com retenção mínima de 1 ano configurada e verificada |
| `R07` | **Crítico** (12) | Verificação de propriedade do recurso no servidor | **Baixo** (2–3) | Testes automatizados confirmam HTTP 403 para IDs cruzados; log de auditoria registra tentativas |
| `R08` | **Alto** (9) | Signed URLs com validade de 15 minutos | **Baixo** (2–3) | Acesso com URL expirada retorna HTTP 403; regras do Storage sem leitura pública |
| `R09` | **Alto** (9) | Rate limiting (10 req/min) + cache TTL de 5 min | **Médio** (4–6) | Rate limit testado com 11 requisições; cache ativo e verificado em log |
| `R10` | **Médio** (4) | Limites de tamanho (10 MB) e tipo de arquivo | **Baixo** (1–2) | Testes de upload com arquivo inválido rejeitados com código correto |
| `R11` | **Alto** (8) | `@authorize` auditado em todos os endpoints | **Baixo** (2–3) | Zero endpoints sem decorator identificados pelo script de auditoria |
| `R12` | **Médio** (4) | Remoção do endpoint + documentação de execução local | **Baixo** (1–2) | Endpoint ausente em produção; processo de inicialização documentado no repositório |