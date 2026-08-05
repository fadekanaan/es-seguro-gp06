# Seção 8 — Registro de Riscos

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 8 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 8. Registro de Riscos

Cada ameaça identificada na Etapa 1 (T01–T12) originou pelo menos um evento de risco. Os Casos de Abuso (CA01–CA06) são referenciados como origens complementares onde a relação é direta. As avaliações de probabilidade e impacto aplicam os critérios definidos na Seção 7.

---

### 8.1 Tabela consolidada do Registro de Riscos

| ID | Origem | Evento de risco | Vulnerabilidade ou condição | Prob. | Impacto | Pont. | Nível |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| `R01` | T01 · Spoofing | Token JWT de usuário autenticado é roubado via XSS ou interceptação e utilizado por um atacante para operar como a vítima | Ausência de proteção contra XSS no frontend e ausência de mecanismo de revogação proativa de tokens | `3` | `4` | `12` | **Crítico** |
| `R02` | T02 · Spoofing · CA03 | Atacante se cadastra como orientador com dados falsos e obtém acesso aos dados de estudantes e à capacidade de validar créditos | Sistema não valida vínculo institucional do orientador nem exige aprovação de coordenador para ativação da conta | `3` | `3` | `9` | **Alto** |
| `R03` | T03 · Tampering · CA01 | Estudante substitui arquivo de comprovante após upload por documento forjado, obtendo validação de créditos indevidos | URL de acesso ao `Firebase Storage` não possui controle de imutabilidade após o upload inicial | `3` | `4` | `12` | **Crítico** |
| `R04` | T04 · Tampering | Usuário com acesso indevido à API altera datas ou marcos do plano de trabalho de um estudante sem autorização | Falha ou ausência do decorator `@authorize` em endpoints de atualização do plano de trabalho | `2` | `3` | `6` | **Médio** |
| `R05` | T05 · Repudiation · CA05 | Aspecto `@audit` é desabilitado via flag de configuração e orientador nega responsabilidade por validação já realizada | Flag `ASPECTS_ENABLED["audit"]` permite desativar a auditoria em tempo de execução sem controle de acesso | `2` | `4` | `8` | **Alto** |
| `R06` | T06 · Repudiation | Coordenador realiza operação administrativa (ex.: aprovação de extensão) e, na ausência de log imutável, nega tê-la realizado | Logs de auditoria podem ser alterados ou expurgados por quem detém acesso ao banco de dados | `2` | `3` | `6` | **Médio** |
| `R07` | T07 · Info. Disclosure · CA02 | Estudante autenticado enumera IDs de outros estudantes em requisições GET e coleta dados pessoais e acadêmicos de terceiros (IDOR) | API não verifica se o recurso solicitado pertence ao usuário autenticado, retornando o objeto completo sem filtragem | `3` | `4` | `12` | **Crítico** |
| `R08` | T08 · Info. Disclosure | URL de download de comprovante no `Firebase Storage` é descoberta ou compartilhada, expondo documentos pessoais sem autenticação | Regras do `Firebase Storage` não exigem autenticação para leitura, ou a URL de acesso não possui validade limitada | `3` | `3` | `9` | **Alto** |
| `R09` | T09 · Denial of Service · CA04 | Atacante envia volume massivo de requisições aos endpoints que invocam o motor de inferência lógica, degradando ou tornando o sistema indisponível | Ausência de *rate limiting* e de cache de resultados nos endpoints computacionalmente intensos | `3` | `3` | `9` | **Alto** |
| `R10` | T10 · Denial of Service | Usuário autenticado realiza upload massivo de arquivos de grande volume, esgotando a cota de armazenamento do Firebase | Ausência de limitação de tamanho de arquivo, de cota por usuário e de restrição por tipo de conteúdo no `Firebase Storage` | `2` | `2` | `4` | **Médio** |
| `R11` | T11 · Elevation of Privilege · CA06 | Estudante autenticado chama diretamente endpoint restrito a coordenadores, explorando ausência ou falha do decorator `@authorize` | Endpoint administrativo sem o decorator `@authorize(role="coordinator")` ou com verificação de papel insuficiente | `2` | `4` | `8` | **Alto** |
| `R12` | T12 · Elevation of Privilege | Script `bootstrap_admin.py` fica acessível ou executável em produção, permitindo criação de conta de coordenador por atacante externo | Script privilegiado exposto via endpoint não autenticado ou por acesso indevido ao servidor em ambiente de produção | `1` | `4` | `4` | **Médio** |

---

### 8.2 Justificativas das avaliações

As justificativas a seguir explicam, para cada risco, os critérios que motivaram os valores de probabilidade e impacto atribuídos, bem como os componentes, usuários e consequências envolvidos.

---

#### R01 — Roubo de token JWT (T01)

- **Probabilidade 3 — Média-alta:** Ataques de XSS e interceptação de tokens são técnicas amplamente documentadas e utilizadas. O frontend `React` com `Vite` não garante proteção automática contra todos os vetores de XSS, especialmente em bibliotecas de terceiros ou renderização de conteúdo dinâmico. A ausência de mecanismo de revogação proativa torna o ataque sustentável por toda a validade do token.
- **Impacto 4 — Muito alto:** Um token comprometido concede ao atacante acesso completo à conta da vítima, permitindo realizar qualquer operação autorizada para aquele papel — incluindo validação de créditos (orientador), emissão de relatórios ou alteração de configurações (coordenador). O impacto se multiplica quando o token pertence a um perfil com privilégios elevados.
- **Relação com casos de abuso:** Esta ameaça habilita vários outros casos de abuso se o token pertencer a um orientador (CA05) ou coordenador (CA06).

---

#### R02 — Falso orientador (T02 · CA03)

- **Probabilidade 3 — Média-alta:** O cadastro de orientadores sem validação de vínculo institucional é uma falha explorada com técnicas simples: basta criar uma conta com e-mail plausível. Não há barreira técnica relevante impedindo o registro.
- **Impacto 3 — Alto:** O atacante obtém acesso prolongado aos dados pessoais, comprovantes e plano de trabalho de múltiplos estudantes, além da capacidade de aprovar atividades fraudulentamente. O impacto inclui violação de privacidade com implicações jurídicas (`LGPD`) e comprometimento da integridade acadêmica.

---

#### R03 — Substituição de comprovante forjado (T03 · CA01)

- **Probabilidade 3 — Média-alta:** A substituição de arquivo após upload é possível a qualquer estudante autenticado que conheça a URL de acesso ao `Storage`. Não há mecanismo de imutabilidade documentado que bloqueie essa operação.
- **Impacto 4 — Muito alto:** A fraude de comprovante compromete a validade dos créditos acadêmicos e pode permitir que um estudante avance para a defesa sem ter cumprido os requisitos reais. O dano é ao mesmo tempo acadêmico, institucional e difícil de detectar sem auditoria ativa.

---

#### R04 — Alteração indevida do plano de trabalho (T04)

- **Probabilidade 2 — Média-baixa:** A exploração depende de uma falha específica no controle de acesso (`@authorize` ausente ou falho) em endpoints de atualização do plano de trabalho. Esse vetor exige conhecimento técnico da API (ex.: Swagger exposto).
- **Impacto 3 — Alto:** A adulteração do plano de trabalho pode mascarar atrasos acadêmicos, criar inconsistências no histórico do estudante e dificultar a auditoria posterior. O dano afeta diretamente a confiabilidade das decisões do programa.

---

#### R05 — Desabilitação do aspecto de auditoria (T05 · CA05)

- **Probabilidade 2 — Média-baixa:** A exploração exige acesso privilegiado às configurações do sistema (variável `ASPECTS_ENABLED`), o que restringe o vetor a insiders ou a atacantes que já tenham comprometido o ambiente de execução. No entanto, a condição é uma vulnerabilidade de configuração real e documentada no código.
- **Impacto 4 — Muito alto:** A ausência de logs de auditoria elimina a capacidade de responsabilização por qualquer operação. Em um contexto acadêmico formal, a impossibilidade de comprovar quem realizou uma validação tem consequências institucionais e potencialmente jurídicas graves.

---

#### R06 — Repudiação de operação administrativa (T06)

- **Probabilidade 2 — Média-baixa:** Requer que o coordenador tenha motivação para negar a ação e que os logs sejam insuficientes ou alteráveis. A condição depende tanto de comportamento humano quanto de fragilidade técnica do log.
- **Impacto 3 — Alto:** A impossibilidade de comprovar uma decisão administrativa (ex.: aprovação de extensão de prazo) gera disputas sem resolução técnica, prejudicando estudantes e comprometendo a governança do programa.

---

#### R07 — IDOR para acesso a dados de terceiros (T07 · CA02)

- **Probabilidade 3 — Média-alta:** A técnica IDOR é trivial para qualquer estudante autenticado que observe o padrão de IDs nas requisições. Não requer ferramentas especializadas — basta modificar um valor na URL. Identificadores sequenciais ou UUIDs previsíveis ampliam o risco.
- **Impacto 4 — Muito alto:** A exploração permite enumeração sistemática dos dados de todos os estudantes do programa — dados pessoais, status acadêmico, plano de trabalho e comprovantes — configurando violação em massa com implicações diretas da `LGPD`.

---

#### R08 — URL de comprovante acessível sem autenticação (T08)

- **Probabilidade 3 — Média-alta:** URLs do `Firebase Storage` sem regras restritivas de leitura são acessíveis publicamente a qualquer um que as possua. O compartilhamento acidental (ex.: via e-mail, print de tela) ou a descoberta por varredura configuram um vetor de exploração plausível e recorrente.
- **Impacto 3 — Alto:** A exposição de comprovantes pode incluir diplomas, certidões, artigos científicos não publicados e documentos de identificação pessoal — todos sensíveis sob a `LGPD` e de valor para o titular.

---

#### R09 — Flooding do motor de inferência (T09 · CA04)

- **Probabilidade 3 — Média-alta:** O vetor de ataque é de baixa complexidade: qualquer usuário autenticado com um script básico pode disparar requisições em alta frequência. O motor de inferência, por seu custo computacional, é um alvo natural.
- **Impacto 3 — Alto:** A indisponibilidade durante períodos críticos do calendário acadêmico (defesas, qualificações, entrega de relatórios) pode causar perda de prazos, retrabalho administrativo e danos à reputação do sistema e do programa.

---

#### R10 — Upload massivo no Storage (T10)

- **Probabilidade 2 — Média-baixa:** Depende de um usuário autenticado com intenção maliciosa e conhecimento da API de upload. A ausência de limitação de tamanho facilita o ataque, mas o vetor é mais direto do que um ataque externo.
- **Impacto 2 — Moderado:** O impacto é limitado ao esgotamento da cota de armazenamento, bloqueando novos uploads legítimos. O serviço pode ser restaurado com ampliação de cota e remoção dos arquivos maliciosos, sem perda de dados existentes.

---

#### R11 — Elevação de privilégios via endpoint desprotegido (T11 · CA06)

- **Probabilidade 2 — Média-baixa:** A exploração depende da existência de um endpoint específico sem o decorator `@authorize` correto — uma falha pontual, não sistêmica. A documentação Swagger em `/docs`, quando exposta em produção, facilita a descoberta.
- **Impacto 4 — Muito alto:** O acesso a funções de coordenador permite alterar a estrutura do programa (tipos de atividades, configurações de crédito), aprovar extensões de prazo indevidamente e acessar relatórios gerenciais completos, comprometendo toda a integridade administrativa do sistema.

---

#### R12 — Exposição do script bootstrap_admin.py (T12)

- **Probabilidade 1 — Baixa:** A exposição do script em produção requer um erro de configuração de infraestrutura grave (endpoint não autenticado ativo ou acesso indevido ao servidor). Em implantações minimamente cuidadosas, o risco de exposição é baixo, pois o script deve ser executado apenas localmente na inicialização.
- **Impacto 4 — Muito alto:** Se explorado, permite a criação de uma conta de coordenador com privilégios máximos sob controle do atacante, comprometendo toda a segurança do sistema de forma imediata e potencialmente silenciosa.
