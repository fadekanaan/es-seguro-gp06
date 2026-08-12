# Seção 8 — Registro de Riscos

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 8 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 8. Registro de Riscos

Cada ameaça identificada na Etapa 1 (`T01–T12`) originou pelo menos um evento de risco no sistema ThesisFlow. Os Casos de Abuso (`CA01–CA06`) foram consolidados como origens complementares onde a relação é direta. As avaliações de probabilidade e impacto aplicam rigorosamente a escala de 1 a 4 definida na Seção 7 ($\text{Pontuação} = \text{Probabilidade} \times \text{Impacto}$). Os riscos classificados como **Críticos** e **Altos** priorizam diretamente os requisitos e as soluções de arquitetura da Etapa 3 e os testes da Etapa 4.

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

As justificativas a seguir detalham os critérios que motivaram os valores de probabilidade e impacto atribuídos a cada risco do sistema ThesisFlow, destacando componentes, usuários e potenciais danos organizacionais e regulatórios.

---

#### R01 — Roubo de token JWT (T01)

- **Probabilidade 3 — Média-alta:** Ataques de XSS e interceptação de tokens são vetores recorrentes. O frontend desenvolvido em `React` com `Vite` exige sanitização rigorosa e bibliotecas atualizadas para evitar XSS. A ausência de revogação proativa estende o ataque por toda a janela de validade do token.
- **Impacto 4 — Muito alto:** O sequestro do token concede ao atacante acesso total à sessão da vítima, permitindo realizar operações sensíveis de acordo com o papel usurpado (como validação indevida de créditos pelo orientador ou alteração de regras por coordenadores).
- **Relação com casos de abuso:** Habilita vetores colaterais graves caso a conta comprometida possua privilégios elevados (`CA05` ou `CA06`). Origina o requisito `RS02` da Etapa 3.

---

#### R02 — Falso orientador (T02 · CA03)

- **Probabilidade 3 — Média-alta:** O auto-cadastro sem dupla verificação ou aprovação administrativa permite a criação de perfis maliciosos com e-mails plausíveis sem barreiras técnicas imediatas.
- **Impacto 3 — Alto:** Concede acesso prolongado a dados acadêmicos e pessoais de múltiplos estudantes, permitindo a aprovação fraudulenta de atividades. Envolve riscos diretos de conformidade com a `LGPD` e perda de integridade acadêmica.

---

#### R03 — Substituição de comprovante forjado (T03 · CA01)

- **Probabilidade 3 — Média-alta:** Qualquer estudante autenticado que obtenha a URL ou referência de upload no `Firebase Storage` pode tentar a substituição de arquivos se não houver trava de imutabilidade ativada no backend.
- **Impacto 4 — Muito alto:** A adulteração de comprovantes compromete a concessão de créditos e a legitimidade das bancas de defesa. É um risco crítico que fundamenta diretamente o requisito `RS03` (Etapa 3) e o serviço de upload seguro em Python (`codigo/etapa-4/`).

---

#### R04 — Alteração indevida do plano de trabalho (T04)

- **Probabilidade 2 — Média-baixa:** Requer a descoberta de falhas pontuais no controle de acesso (`@authorize` ausente ou mal configurado) em endpoints específicos de atualização do plano.
- **Impacto 3 — Alto:** Permite mascarar atrasos acadêmicos e alterar dados estruturantes do progresso do estudante, prejudicando a auditoria do programa.

---

#### R05 — Desabilitação do aspecto de auditoria (T05 · CA05)

- **Probabilidade 2 — Média-baixa:** Restrito a usuários com acesso a variáveis de ambiente ou configurações de tempo de execução (`ASPECTS_ENABLED`), caracterizando um risco do tipo insider ou pós-comprometimento de infraestrutura.
- **Impacto 4 — Muito alto:** A inativação dos logs elimina o não-repúdio das operações. Sem rastreabilidade, validações fraudulentas não podem ser vinculadas aos responsáveis, gerando passivos institucionais e jurídicos.

---

#### R06 — Repudiação de operação administrativa (T06)

- **Probabilidade 2 — Média-baixa:** Depende de fragilidades na imutabilidade dos logs aliadas à intenção maliciosa de um perfil administrativo de negar uma decisão prévia.
- **Impacto 3 — Alto:** Gera disrupção nas decisões do programa (ex.: extensões de prazo recusadas ou retratadas), prejudicando o estudante e minando a governança do sistema.

---

#### R07 — IDOR para acesso a dados de terceiros (T07 · CA02)

- **Probabilidade 3 — Média-alta:** A exploração de *Insecure Direct Object References* (IDOR) é trivial via manipulação de parâmetros sequenciais ou conhecidos na URL, dispensando ferramentas avançadas.
- **Impacto 4 — Muito alto:** Permite a raspagem (*scraping*) e exposição massiva de dados pessoais, planos de estudo e comprovantes de todos os estudantes cadastrados. É a maior prioridade do sistema, originando o risco `R07`, o requisito `RS01` (Etapa 3) e o módulo de autorização por recurso (`codigo/etapa-4/`).

---

#### R08 — URL de comprovante acessível sem autenticação (T08)

- **Probabilidade 3 — Média-alta:** URLs públicas ou assinadas com prazos longos no `Firebase Storage` podem vazar por e-mail, histórico ou varreduras automatizadas.
- **Impacto 3 — Alto:** Exposição indevida de documentos e comprovantes sensíveis protegidos pela `LGPD`.

---

#### R09 — Flooding do motor de inferência (T09 · CA04)

- **Probabilidade 3 — Média-alta:** Qualquer usuário autenticado pode disparar requisições concorrentes contra endpoints computacionalmente pesados através de scripts simples.
- **Impacto 3 — Alto:** Causa negação de serviço nos períodos mais críticos do calendário acadêmico (prazos de defesa e entregas de relatórios).

---

#### R10 — Upload massivo no Storage (T10)

- **Probabilidade 2 — Média-baixa:** Depende de um usuário autenticado explorando a ausência de cotas e validação de tamanho de arquivos de upload.
- **Impacto 2 — Moderado:** Provoca esgotamento da cota de armazenamento no Firebase, interrompendo novos envios até a limpeza manual e ampliação de limites.

---

#### R11 — Elevação de privilégios via endpoint desprotegido (T11 · CA06)

- **Probabilidade 2 — Média-baixa:** Requer a descoberta de endpoints administrativos sem a devida verificação de papéis (`@authorize(role="coordinator")`), facilitada por documentações como Swagger expostas em produção.
- **Impacto 4 — Muito alto:** Concede acesso a funcionalidades estratégicas do sistema, permitindo a aprovação indevida de créditos e alteração das regras do programa.

---

#### R12 — Exposição do script bootstrap_admin.py (T12)

- **Probabilidade 1 — Baixa:** Ocorre apenas mediante falhas graves de implantação/servidor em ambiente de produção, pois o script de inicialização deve residir em ambiente isolado.
- **Impacto 4 — Muito alto:** Permite a criação arbitrária de uma conta com superprivilégios, resultando no comprometimento total e silencioso do ThesisFlow.