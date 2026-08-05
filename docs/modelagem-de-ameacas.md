# ThesisFlow — Modelagem de Ameaças e Análise de Riscos de Segurança

**Grupo 06 — Engenharia de Software Seguro — UNIPAMPA**

> **Aviso de Navegação:** Este documento é o arquivo principal do trabalho. Cada seção está disponível também em arquivo individual na pasta [`docs/etapas/`](etapas/) para facilitar a colaboração e os commits individuais. O conteúdo completo e final está consolidado abaixo.

---

## Índice

### Etapa 1 — Casos de Abuso e Modelagem de Ameaças com STRIDE

| # | Seção | Arquivo de trabalho |
| :---: | :--- | :--- |
| `1` | [Identificação e descrição do sistema](#1-identificação-do-sistema) | [`sec1-identificacao-descricao.md`](etapas/etapa-1/sec1-identificacao-descricao.md) |
| `2` | [Usuários, ativos e pontos de interação](#3-usuários-ativos-e-pontos-de-interação) | [`sec2-usuarios-ativos.md`](etapas/etapa-1/sec2-usuarios-ativos.md) |
| `3` | [Visão geral da arquitetura](#4-visão-geral-da-arquitetura) | [`sec3-arquitetura.md`](etapas/etapa-1/sec3-arquitetura.md) |
| `4` | [Modelagem de ameaças com STRIDE](#5-modelagem-de-ameaças-com-stride) | [`sec4-stride.md`](etapas/etapa-1/sec4-stride.md) |
| `5` | [Casos de abuso](#6-casos-de-abuso) | [`sec5-casos-de-abuso.md`](etapas/etapa-1/sec5-casos-de-abuso.md) |
| `6` | [Considerações finais](#7-considerações-finais) | [`sec6-consideracoes.md`](etapas/etapa-1/sec6-consideracoes.md) |

### Etapa 2 — Análise, Priorização e Tratamento de Riscos com o NIST CSF

| # | Seção | Arquivo de trabalho |
| :---: | :--- | :--- |
| `7` | [Critérios de avaliação de risco](#7-critérios-de-avaliação-de-risco) | [`sec7-criterios-avaliacao.md`](etapas/etapa-2/sec7-criterios-avaliacao.md) |
| `8` | [Registro de riscos](#8-registro-de-riscos) | [`sec8-registro-de-riscos.md`](etapas/etapa-2/sec8-registro-de-riscos.md) |
| `9` | [Priorização dos riscos](#9-priorização-dos-riscos) | [`sec9-priorizacao-riscos.md`](etapas/etapa-2/sec9-priorizacao-riscos.md) |
| `10` | [Tratamento dos riscos e NIST CSF 2.0](#10-tratamento-dos-riscos-e-mapeamento-para-o-nist-csf-20) | [`sec10-tratamento-nist-csf.md`](etapas/etapa-2/sec10-tratamento-nist-csf.md) |

---
---

## Etapa 1 — Casos de Abuso e Modelagem de Ameaças com STRIDE

---

## 1. Identificação do sistema

- **Nome do sistema:** **ThesisFlow** — Sistema de Acompanhamento de Mestrado
- **Integrantes do grupo:**
  - Artur Wahlbrink Kraemer
  - Marcus Vinicius Morini Querol Junior
  - Bernardo Gomes Dorneles
  - Gustavo Fernandes dos Anjos
  - Fade Hassan Husein Kanaan
  - Rodrigo Thoma da Silva
- **Repositório:** [https://github.com/fadekanaan/es-seguro-gp06](https://github.com/fadekanaan/es-seguro-gp06)
- **Justificativa:** O **ThesisFlow** foi escolhido por ser um sistema real desenvolvido pelo próprio grupo durante a disciplina de Engenharia de Software no mesmo semestre. Isso nos permite realizar uma análise contextualizada e aprofundada, pois conhecemos em detalhes sua arquitetura, seus componentes, os dados que armazena e como os usuários interagem com ele. O sistema reúne múltiplos perfis de usuário, armazena dados pessoais e acadêmicos sensíveis, realiza autenticação, controla permissões e integra serviços externos — tornando-o um objeto de estudo rico para a análise de segurança com `STRIDE` e `NIST CSF`.

---

## 2. Descrição do sistema

O **ThesisFlow** é um sistema de acompanhamento acadêmico voltado a programas de mestrado com duração de 24 meses. Seu objetivo é auxiliar estudantes, orientadores e coordenadores no acompanhamento do progresso acadêmico ao longo de todo o curso, cobrindo plano de trabalho, tarefas, atividades creditáveis, validação de créditos, prazos, status acadêmico e requisitos para a defesa de dissertação.

### Problema que o sistema resolve

Programas de pós-graduação exigem que os estudantes cumpram uma série de requisitos ao longo dos meses: completar um número mínimo de créditos, registrar atividades acadêmicas com comprovação, cumprir marcos do plano de trabalho e submeter produções científicas. Sem um sistema centralizado, esse acompanhamento é fragmentado, dependente de planilhas, e-mails e processos manuais sujeitos a erros. O **ThesisFlow** centraliza esse processo em uma plataforma web segura e auditável.

### Quem utiliza o sistema

| Perfil | Descrição |
| :---: | :--- |
| **Estudante** | Matriculado no programa de mestrado. Registra atividades, faz upload de comprovantes, acompanha seu plano de trabalho e consulta seu status acadêmico. |
| **Orientador** | Professor responsável por um ou mais estudantes. Valida atividades creditáveis, acompanha o progresso do orientando e registra produções científicas. |
| **Coordenador** | Responsável pela administração do programa. Gerencia cadastros de usuários, define tipos de atividades creditáveis, aprova extensões de prazo, emite relatórios gerenciais e configura políticas acadêmicas. |

### Principais funcionalidades

- Cadastro e gerenciamento de estudantes, orientadores e coordenadores
- Registro e acompanhamento do plano de trabalho e suas etapas
- Registro de atividades creditáveis com upload de comprovantes (artigos, certificados, diplomas)
- Validação de créditos por orientadores
- Inferência automática do status acadêmico via motor lógico interno
- Geração de alertas automáticos sobre prazos e pendências
- Emissão de relatórios gerenciais para coordenadores
- Registro de produções científicas com classificação por tipo e período

### Informações armazenadas e transmitidas

- Dados pessoais dos estudantes (nome, e-mail, matrícula)
- Credenciais de acesso (gerenciadas pelo `Firebase Authentication`)
- Planos de trabalho com datas, etapas e prazos
- Registros de atividades creditáveis com comprovantes em arquivo (`Firebase Storage`)
- Produções científicas com metadados de autoria e *venue*
- Histórico de validações e aprovações
- Logs de auditoria de todas as operações sensíveis
- Status acadêmico inferido (regular, em risco, apto para defesa, etc.)
- Relatórios gerenciais com dados agregados de todo o programa

### Recursos que precisam ser protegidos

- Credenciais de autenticação
- Dados pessoais dos estudantes
- Comprovantes e documentos (arquivos no `Firebase Storage`)
- Registros de validação e aprovação de créditos
- Logs de auditoria
- Status acadêmico de cada estudante
- Planos de trabalho e prazos
- Permissões e papéis de acesso (`RBAC`)

---

## 3. Usuários, ativos e pontos de interação

### 3.1 Usuários e perfis de acesso

| Usuário | Papel no sistema | Principais ações |
| :--- | :---: | :--- |
| **Estudante** | `student` | Registrar atividades, fazer upload de comprovantes, consultar plano de trabalho, acompanhar status acadêmico |
| **Orientador** | `advisor` | Validar atividades creditáveis, acompanhar progresso do orientando, registrar produções científicas |
| **Coordenador** | `coordinator` | Gerenciar usuários e papéis, definir tipos de atividades, aprovar extensões de prazo, emitir relatórios |
| **Administrador de sistema** | acesso via *bootstrap* | Criar a conta inicial de coordenador via script privilegiado (`bootstrap_admin.py`) |

### 3.2 Dados pessoais e sensíveis

| Dado | Quem tem acesso | Por quê é sensível |
| :--- | :--- | :--- |
| Nome, e-mail e matrícula do estudante | Orientador, Coordenador, o próprio estudante | Dados pessoais protegidos pela `LGPD` |
| Credenciais de acesso (token `JWT`) | Usuário e `Firebase Auth` | Permitem acesso total à conta se comprometidos |
| Comprovantes de atividade (arquivos) | Estudante (upload), Orientador (validação) | Podem conter diplomas, certidões, artigos não publicados |
| Produções científicas e publicações | Orientador, Coordenador | Podem incluir trabalhos ainda não publicados |
| Status acadêmico inferido | Coordenador, Orientador, Estudante | Revela situação de risco ou atraso |
| Histórico de aprovações e validações | Coordenador, Orientador | Permite rastrear responsabilidades |
| Logs de auditoria | Coordenador, Administrador | Registros de todas as operações sensíveis |

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

---

## 4. Visão geral da arquitetura

O **ThesisFlow** segue uma arquitetura em camadas estrita: `Router` → `Service` → `Repository` → `Infrastructure`. O frontend `React` se comunica com o backend `FastAPI` via `HTTP REST`. A autenticação é delegada ao `Firebase Authentication`, que emite tokens `JWT` verificados pela API a cada requisição. Os dados persistidos ficam no `Firestore`. Arquivos de comprovantes são armazenados no `Firebase Storage`.

A segurança da API é reforçada pelo aspecto `@authorize`, que valida o papel do usuário autenticado antes de qualquer operação sensível. O aspecto `@audit` registra automaticamente todas as operações de criação e alteração de dados.

### Diagrama de Contexto

![Diagrama de Contexto do ThesisFlow](../diagramas/diagrama-contexto.png)
*Figura 1: Diagrama de Contexto do sistema ThesisFlow*

### Diagrama de Fluxo de Dados

O diagrama abaixo ilustra dois fluxos críticos para a segurança: a autenticação/autorização e o registro de atividade com upload de comprovante.

![Diagrama de Fluxo de Dados](../diagramas/diagrama-fluxo-dados.png)
*Figura 2: Diagrama de Fluxo de Dados (Autenticação, Autorização e Upload de Comprovante)*

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

---

## 5. Modelagem de ameaças com STRIDE

A análise `STRIDE` foi aplicada aos componentes e ativos do **ThesisFlow**. Para cada categoria, foram identificadas ameaças concretas e relacionadas ao funcionamento do sistema.

| ID | Categoria STRIDE | Componente ou ativo | Ameaça identificada | Possível impacto |
| :---: | :---: | :--- | :--- | :--- |
| `T01` | **Spoofing** | `Firebase Auth` / Token `JWT` | Um atacante rouba ou captura o token `JWT` de um usuário autenticado (via `XSS`, interceptação ou vazamento) e passa a utilizá-lo para autenticar requisições como se fosse a vítima | Acesso completo à conta: leitura de dados, upload de arquivos, validação de atividades em nome de outro usuário |
| `T02` | **Spoofing** | Cadastro de orientador | Um usuário se cadastra como orientador informando dados falsos de vínculo institucional, pois o sistema não valida o vínculo real com a universidade | Acesso a dados privados de estudantes, possibilidade de validar créditos indevidamente como se fosse um professor legítimo |
| `T03` | **Tampering** | Comprovantes no `Firebase Storage` | Um estudante substitui o arquivo de comprovante legítimo por um documento forjado após o upload, explorando a URL de acesso ao `Storage` sem restrição de imutabilidade | Validação de atividade creditável com documento falso, obtendo créditos indevidos |
| `T04` | **Tampering** | Plano de trabalho e prazos | Um usuário com acesso indevido à API altera datas de prazo ou marcos do plano de trabalho de um estudante, modificando o registro sem autorização | Mascaramento de atrasos acadêmicos, geração de inconsistências no histórico e dificuldade de auditoria posterior |
| `T05` | **Repudiation** | Logs de auditoria (`@audit`) | O aspecto de auditoria é desabilitado em tempo de execução (via flag `ASPECTS_ENABLED`) ou os logs são apagados/alterados; um orientador nega ter aprovado determinada atividade | Impossibilidade de responsabilizar o autor de uma operação, dificultando investigação de fraudes acadêmicas |
| `T06` | **Repudiation** | Operações de coordenador | Um coordenador realiza uma operação administrativa (ex.: aprovação de extensão de prazo) e, na ausência de log imutável com identificação completa, nega posteriormente ter realizado a ação | Contestações sem evidências, comprometimento da responsabilização institucional |
| `T07` | **Information Disclosure** | API REST / `Firestore` | Um estudante autenticado modifica o identificador de outro estudante em uma requisição `GET` (ataque IDOR — *Insecure Direct Object Reference*), e a API retorna dados do outro estudante sem verificar a propriedade do recurso | Exposição de dados pessoais, plano de trabalho, status acadêmico e produção científica de terceiros |
| `T08` | **Information Disclosure** | `Firebase Storage` | A URL de download de um comprovante armazenado no `Firebase Storage` não exige autenticação para ser acessada; a URL é compartilhada ou descoberta por terceiros | Exposição de documentos pessoais sensíveis (diplomas, certidões, artigos não publicados) |
| `T09` | **Denial of Service** | API FastAPI / Motor lógico | Um atacante envia um grande volume de requisições a endpoints que invocam o motor de inferência lógica, que realiza operações computacionalmente intensas sem limitação de taxa | Degradação ou indisponibilidade do sistema durante períodos críticos (ex.: período de qualificações e defesas) |
| `T10` | **Denial of Service** | `Firebase Storage` | Um usuário autenticado realiza upload massivo de arquivos de grande volume, esgotando a cota de armazenamento do plano Firebase utilizado pelo sistema | Bloqueio de uploads legítimos de outros estudantes, impossibilitando o envio de comprovantes |
| `T11` | **Elevation of Privilege** | Aspecto `@authorize` (`RBAC`) | Um estudante autenticado manipula uma requisição HTTP para chamar diretamente um endpoint restrito a coordenadores (ex.: `POST /activity-types`), explorando falha na verificação de papel ou ausência do decorator | Acesso a funções administrativas: criação de tipos de atividades, aprovação de extensões, acesso a relatórios gerenciais |
| `T12` | **Elevation of Privilege** | Script `bootstrap_admin.py` | O script de criação da conta inicial de coordenador fica acessível ou executável remotamente em ambiente de produção (ex.: via endpoint não autenticado, variável de ambiente exposta ou acesso indevido ao servidor) | Criação de uma conta de coordenador com privilégios máximos por um atacante externo, comprometendo toda a segurança do sistema |

### 5.1 Interpretação da análise

> **Nota de Análise:** As doze ameaças identificadas abrangem todas as seis categorias do `STRIDE` no contexto específico do **ThesisFlow**. As ameaças de **Spoofing** comprometem a identidade dos usuários e a confiança nas ações realizadas. O **Tampering** afeta a integridade dos dados acadêmicos e dos comprovantes, que são a base para decisões importantes de validação. A **Repudiation** prejudica a capacidade de auditoria e responsabilização — especialmente crítica em um contexto acadêmico formal. A **Information Disclosure** expõe dados pessoais protegidos pela `LGPD`. O **Denial of Service** pode impedir o uso do sistema em momentos críticos do calendário acadêmico. Por fim, a **Elevation of Privilege** pode comprometer toda a estrutura de controle de acesso do sistema.

---

## 6. Casos de abuso

### Diagrama de Casos de Abuso

![Diagrama de Casos de Abuso](../diagramas/diagrama-casos-de-abuso.png)
*Figura 3: Diagrama de Casos de Abuso do sistema ThesisFlow*

---

### CA01 — Forja de comprovante para validação indevida de créditos

| Atributo | Detalhes |
| :---: | :--- |
| **Identificador** | `CA01` |
| **Ator Malicioso** | Estudante mal-intencionado |
| **Objetivo do Abuso** | Obter validação de créditos por meio de um comprovante falso ou de um documento legítimo de outra pessoa |
| **Condições Necessárias** | • O sistema aceita upload de arquivos sem verificar o conteúdo ou autenticidade do documento.<br>• A URL de acesso ao arquivo no `Firebase Storage` não possui controle de imutabilidade após o upload.<br>• O orientador não possui mecanismo de verificação adicional além da visualização do arquivo. |
| **Categorias STRIDE** | **Tampering**, **Repudiation** |

#### Fluxo do Abuso

1. O estudante registra uma atividade creditável no sistema com dados corretos (tipo, descrição, data).
2. O estudante faz upload de um comprovante que pode ser falso (documento adulterado) ou de terceiro (comprovante roubado ou copiado).
3. O sistema aceita o arquivo e associa a URL ao registro da atividade.
4. O orientador recebe notificação e visualiza o arquivo — que aparenta ser legítimo.
5. O orientador valida a atividade sem perceber a fraude.
6. O sistema registra os créditos como válidos na conta do estudante.

> **Impacto Estimado:** O estudante obtém créditos acadêmicos sem ter realizado a atividade correspondente, o que compromete a integridade do programa e pode permitir que ele avance para a defesa sem cumprir os requisitos reais.

---

### CA02 — Acesso indevido a dados de outro estudante via IDOR

| Atributo | Detalhes |
| :---: | :--- |
| **Identificador** | `CA02` |
| **Ator Malicioso** | Estudante autenticado no sistema |
| **Objetivo do Abuso** | Acessar informações privadas de outros estudantes — plano de trabalho, status acadêmico, produções registradas — sem autorização |
| **Condições Necessárias** | • A API não verifica se o recurso solicitado pertence ao usuário autenticado.<br>• Os identificadores de recursos (IDs de estudante, IDs de atividade) são sequenciais ou previsíveis.<br>• A resposta da API retorna o objeto completo sem filtragem por proprietário. |
| **Categorias STRIDE** | **Information Disclosure** |

#### Fluxo do Abuso

1. O estudante autentica-se normalmente com suas próprias credenciais.
2. O estudante acessa um recurso próprio e observa o identificador na URL (ex.: `GET /students/{student_id}/activities`).
3. O estudante modifica o identificador na requisição (ex.: incrementa o valor ou testa outros IDs).
4. A API processa a requisição sem verificar se o `student_id` pertence ao usuário autenticado.
5. O sistema retorna os dados do estudante correspondente ao ID modificado.
6. O estudante repete a operação sistematicamente, coletando dados de múltiplos estudantes.

> **Impacto Estimado:** Exposição de dados pessoais e acadêmicos de terceiros, violação de privacidade com implicações legais (`LGPD`), e possível uso das informações para fraudes ou pressão sobre outros estudantes.

---

### CA03 — Cadastro de falso orientador para obter acesso a dados de estudantes

| Atributo | Detalhes |
| :---: | :--- |
| **Identificador** | `CA03` |
| **Ator Malicioso** | Atacante externo que deseja se passar por orientador |
| **Objetivo do Abuso** | Obter o papel de orientador no sistema para acessar dados privados de estudantes e potencialmente validar atividades ou influenciar o progresso acadêmico de outros usuários |
| **Condições Necessárias** | • O sistema permite cadastro de orientadores sem validar o vínculo real com a instituição.<br>• O processo de criação de conta de orientador não exige confirmação por parte de um coordenador.<br>• O atacante consegue criar um e-mail com domínio institucional ou similar. |
| **Categorias STRIDE** | **Spoofing**, **Information Disclosure**, **Elevation of Privilege** |

#### Fluxo do Abuso

1. O atacante cria uma conta no `Firebase Authentication` com um e-mail plausível (ex.: com domínio institucional ou similar).
2. O atacante registra-se no sistema como orientador, informando dados falsos de nome e vínculo.
3. O sistema aceita o cadastro sem verificação adicional.
4. O atacante é associado a um ou mais estudantes como orientador.
5. O atacante passa a ter acesso aos dados pessoais, plano de trabalho e comprovantes dos estudantes orientados.
6. O atacante pode validar atividades indevidamente ou coletar dados para outros fins.

> **Impacto Estimado:** Exposição de dados pessoais de estudantes, comprometimento da confidencialidade de documentos acadêmicos, validações fraudulentas e perda de confiança no sistema.

---

### CA04 — Ataque de flooding ao motor de inferência durante período crítico

| Atributo | Detalhes |
| :---: | :--- |
| **Identificador** | `CA04` |
| **Ator Malicioso** | Atacante externo com acesso autenticado ou com credenciais comprometidas |
| **Objetivo do Abuso** | Tornar o sistema indisponível durante um período crítico do calendário acadêmico (ex.: período de qualificações, defesas ou entrega de relatórios semestrais) |
| **Condições Necessárias** | • O sistema não possui limitação de taxa de requisições (*rate limiting*) nos endpoints da API.<br>• O motor de inferência lógica realiza operações computacionalmente intensas a cada invocação.<br>• Não há mecanismo de cache para resultados já calculados recentemente. |
| **Categorias STRIDE** | **Denial of Service** |

#### Fluxo do Abuso

1. O atacante autentica-se no sistema com credenciais próprias ou roubadas.
2. O atacante identifica os endpoints que invocam o motor lógico (ex.: `GET /students/{id}/status`).
3. O atacante envia requisições em alta frequência para esses endpoints via script.
4. O motor de inferência é invocado repetidamente, consumindo CPU e memória do servidor.
5. O sistema começa a responder com lentidão ou erros para todos os usuários.
6. Estudantes e orientadores não conseguem acessar o sistema durante o período crítico.

> **Impacto Estimado:** Indisponibilidade do sistema, perda de prazos acadêmicos por parte de estudantes legítimos, aumento de carga administrativa e possível prejuízo ao calendário do programa.

---

### CA05 — Orientador nega ter aprovado validação de crédito

| Atributo | Detalhes |
| :---: | :--- |
| **Identificador** | `CA05` |
| **Ator Malicioso** | Orientador desonesto ou com interesses conflitantes |
| **Objetivo do Abuso** | Negar a responsabilidade por uma validação de crédito já realizada, seja para prejudicar o estudante, encobrir um erro próprio ou evitar consequências de uma aprovação indevida |
| **Condições Necessárias** | • O aspecto `@audit` pode ser desabilitado via flag de configuração (`ASPECTS_ENABLED["audit"] = False`).<br>• Os logs de auditoria não são imutáveis ou podem ser alterados por quem tem acesso ao banco de dados.<br>• Não há assinatura digital ou mecanismo criptográfico que vincule a validação ao orientador. |
| **Categorias STRIDE** | **Repudiation** |

#### Fluxo do Abuso

1. O orientador valida a atividade de um estudante no sistema.
2. O sistema registra a operação via `@audit`, associando-a ao token `JWT` do orientador.
3. Posteriormente, o orientador afirma não ter realizado a validação.
4. Se os logs forem incompletos, alteráveis ou sem identificação suficiente, não há prova da ação.
5. A contestação não pode ser resolvida, e o estudante pode ter seus créditos cancelados.

> **Impacto Estimado:** Prejuízo acadêmico direto ao estudante, impossibilidade de responsabilização do orientador e necessidade de processos administrativos para resolução da disputa.

---

### CA06 — Estudante eleva seus próprios privilégios para coordenador

| Atributo | Detalhes |
| :---: | :--- |
| **Identificador** | `CA06` |
| **Ator Malicioso** | Estudante com conhecimento técnico sobre APIs REST |
| **Objetivo do Abuso** | Contornar o controle de acesso baseado em papel (`RBAC`) para acessar funcionalidades restritas a coordenadores |
| **Condições Necessárias** | • Existe um endpoint administrativo sem o decorator `@authorize(role="coordinator")` ou com verificação insuficiente.<br>• O estudante consegue descobrir a URL de um endpoint restrito (via documentação Swagger em `/docs`, erros expostos ou análise de tráfego).<br>• O sistema não verifica consistência de papel no servidor além do token `JWT`. |
| **Categorias STRIDE** | **Elevation of Privilege**, **Tampering** |

#### Fluxo do Abuso

1. O estudante autentica-se normalmente.
2. O estudante explora a API buscando endpoints não protegidos (ex.: usando a documentação Swagger).
3. O estudante identifica o endpoint `POST /activity-types` ou similar.
4. O estudante envia uma requisição com seu token `JWT` de estudante para o endpoint restrito.
5. Se a verificação for ausente ou falha, o sistema processa a requisição.
6. O estudante cria ou altera configurações do sistema, afetando outros usuários.

> **Impacto Estimado:** Alteração de configurações do programa, criação de tipos de atividades falsas e comprometimento da integridade do sistema.

---

## Considerações finais

### Ameaças mais preocupantes

As ameaças consideradas mais críticas são a exposição de dados por IDOR (`T07`), o roubo de token `JWT` (`T01`) e a falsificação de comprovantes (`T03`). Essas ameaças afetam diretamente a integridade e a confidencialidade do sistema, podendo comprometer a validade do processo acadêmico.

A ameaça `T07` (IDOR) é particularmente preocupante porque exige pouco conhecimento técnico — qualquer estudante autenticado pode tentar modificar identificadores em requisições — e seu impacto é elevado, pois viola a privacidade de múltiplos usuários e pode gerar consequências legais conforme a `LGPD`.

A ameaça `T01` (roubo de token `JWT`) é crítica pela abrangência: um token de coordenador comprometido expõe todo o sistema administrativo, enquanto um token de orientador compromete os dados de todos os seus orientandos.

---

### Ativos mais importantes

Os ativos mais valiosos são as **credenciais de autenticação** (token `JWT`), os **comprovantes de atividades** (arquivos no `Firebase Storage`), os **registros de validação** e os **logs de auditoria**. Esses elementos são a base para todas as decisões acadêmicas tomadas pelo sistema — a integridade do diploma emitido ao final do programa depende diretamente da confiabilidade dessas informações.

---

### Tipos de abuso com maior impacto

Os casos de abuso com maior impacto potencial são:

- **`CA03` (falso orientador):** permite acesso prolongado e sistemático a dados de múltiplos estudantes, com grande dificuldade de detecção.
- **`CA01` (forja de comprovante):** compromete a validade acadêmica dos créditos validados, podendo levar um estudante a defender uma dissertação sem ter cumprido os requisitos reais.
- **`CA06` (elevação de privilégios):** compromete toda a estrutura de controle de acesso do sistema, permitindo alterações que afetam todos os usuários.

---

### Principais dificuldades encontradas

A maior dificuldade foi diferenciar ameaças genéricas de situações concretas e específicas ao **ThesisFlow**. O conhecimento profundo do sistema, por ter sido desenvolvido pelo grupo, facilitou a identificação de pontos realmente vulneráveis — como o flag `ASPECTS_ENABLED` que pode desabilitar a auditoria, ou a ausência de restrição de imutabilidade nos arquivos do `Storage`.

Outra dificuldade foi determinar o limite entre **ameaça** (o que pode acontecer), **vulnerabilidade** (a condição que permite) e **ataque** (a ação do agente malicioso). A utilização do `STRIDE` ajudou a estruturar essa análise por perspectivas distintas, revelando ameaças que poderiam não ser percebidas em uma análise apenas funcional.

Por fim, a categoria **Repudiation** foi a mais difícil de contextualizar, pois depende não apenas de uma falha técnica, mas também do comportamento dos usuários e da qualidade dos registros de auditoria — que no **ThesisFlow** podem ser desabilitados via configuração.

---
---

## Etapa 2 — Análise, Priorização e Tratamento de Riscos com o NIST CSF

---

## 7. Critérios de Avaliação de Risco

Esta seção define os critérios de probabilidade e impacto que serão aplicados a todas as ameaças identificadas na Etapa 1, transformando-as em eventos de risco mensuráveis e comparáveis. As escalas adotadas seguem as diretrizes da disciplina e são calibradas de acordo com o contexto específico do **ThesisFlow**.

---

### 7.1 Critérios de probabilidade

A escala de probabilidade reflete a facilidade com que um evento de risco pode ocorrer, considerando as condições técnicas do sistema, o perfil dos usuários, as vulnerabilidades existentes e o contexto de uso acadêmico.

| Valor | Classificação | Critério |
| :---: | :---: | :--- |
| `1` | Baixa | O evento depende de condições incomuns, acesso muito específico ou grande capacidade técnica |
| `2` | Média-baixa | O evento é possível, mas depende de uma vulnerabilidade ou condição específica |
| `3` | Média-alta | O evento é plausível e pode ocorrer em situações comuns de uso ou ataque |
| `4` | Alta | O evento pode ocorrer com facilidade, frequência ou durante condições previsíveis do sistema |

A probabilidade não é atribuída por intuição. Cada valor é justificado com base nas características do sistema, nas vulnerabilidades identificadas, nas condições de exploração e no contexto de uso do **ThesisFlow** (ver Seção 8).

---

### 7.2 Critérios de impacto

A escala de impacto reflete as consequências de um evento de risco bem-sucedido sobre os usuários, os dados, a integridade acadêmica e a conformidade legal do sistema.

| Valor | Classificação | Critério |
| :---: | :---: | :--- |
| `1` | Baixo | Causa pequeno transtorno e pode ser corrigido rapidamente |
| `2` | Moderado | Causa interrupção ou inconsistência limitada, com possibilidade de recuperação |
| `3` | Alto | Causa prejuízo relevante aos usuários, ao negócio, à administração ou à privacidade |
| `4` | Muito alto | Pode afetar muitos usuários, comprometer operações críticas ou causar prejuízo grave |

Na avaliação do impacto foram considerados: prejuízo direto aos usuários, exposição de dados pessoais protegidos pela `LGPD`, interrupção de operações críticas do calendário acadêmico, comprometimento da integridade das decisões de validação e dificuldade de recuperação.

---

### 7.3 Cálculo e classificação do nível de risco

A pontuação de cada risco é calculada pela seguinte fórmula:

```
Pontuação = Probabilidade × Impacto
```

O resultado é então classificado conforme a tabela abaixo:

| Pontuação | Nível do risco |
| :---: | :---: |
| `1 a 3` | **Baixo** |
| `4 a 7` | **Médio** |
| `8 a 11` | **Alto** |
| `12 a 16` | **Crítico** |

> A pontuação auxilia na comparação entre riscos, mas não substitui a análise contextual. Dois riscos com a mesma pontuação podem receber prioridades distintas em função da gravidade das consequências, das dependências entre componentes ou da dificuldade de recuperação (ver Seção 9).

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

As justificativas a seguir explicam, para cada risco, os critérios que motivaram os valores de probabilidade e impacto atribuídos.

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

---

## 9. Priorização dos Riscos

A priorização define a ordem em que os riscos devem receber atenção e recursos. A pontuação calculada é o ponto de partida, mas não o único critério. A ordenação final também considera: a gravidade das consequências, o número de usuários afetados, a facilidade de exploração, a importância do ativo comprometido, a possibilidade de recuperação e as dependências entre os riscos.

---

### 9.1 Tabela de priorização

| Prioridade | ID | Nível | Pontuação | Justificativa da prioridade |
| :---: | :---: | :---: | :---: | :--- |
| `1º` | `R07` | **Crítico** | `12` | IDOR de baixíssima complexidade técnica com impacto em massa sobre dados pessoais de todos os estudantes; violação direta da `LGPD` |
| `2º` | `R01` | **Crítico** | `12` | Token comprometido concede controle total da conta; habilita encadeamento com outros ataques (R03, R05, R11) |
| `3º` | `R03` | **Crítico** | `12` | Fraude de comprovante compromete a validade acadêmica do programa; impacto direto na decisão de quem defende a dissertação |
| `4º` | `R05` | **Alto** | `8` | Desabilitação da auditoria elimina qualquer possibilidade de responsabilização; afeta transversalmente todos os outros riscos |
| `5º` | `R11` | **Alto** | `8` | Elevação de privilégios compromete a estrutura de controle de acesso de todo o sistema |
| `6º` | `R02` | **Alto** | `9` | Falso orientador tem acesso prolongado e sistemático aos dados de múltiplos estudantes com difícil detecção |
| `7º` | `R08` | **Alto** | `9` | Exposição de documentos sensíveis sem autenticação; vetor plausível e silencioso |
| `8º` | `R09` | **Alto** | `9` | DoS durante períodos críticos tem impacto acadêmico e reputacional relevante |
| `9º` | `R04` | **Médio** | `6` | Adulteração do plano de trabalho é prejudicial, mas depende de falha específica menos provável |
| `10º` | `R06` | **Médio** | `6` | Repudiação administrativa é séria, mas depende de comportamento humano além da falha técnica |
| `11º` | `R10` | **Médio** | `4` | Impacto limitado a uploads futuros; reversível com expansão de cota e remoção de arquivos |
| `12º` | `R12` | **Médio** | `4` | Probabilidade muito baixa em implantação minimamente correta; impacto crítico, mas dependente de erro operacional grave |

---

### 9.2 Justificativa da ordem de precedência

#### Por que R07 ocupa a 1ª posição

R07, R01 e R03 compartilham a mesma pontuação máxima (12). O desempate é definido pela **trivialidade de exploração** e pela **abrangência do impacto**. O IDOR (R07) não exige ferramentas especializadas, comprometimento prévio de credenciais ou conhecimento técnico avançado — qualquer estudante autenticado consegue explorar a vulnerabilidade simplesmente alterando um identificador na URL. Além disso, o impacto afeta potencialmente **todos os estudantes do programa de forma simultânea**, caracterizando uma violação em massa de dados pessoais com implicações diretas da `LGPD`.

#### Por que R01 precede R03

Ambos têm pontuação 12. R01 (roubo de token) precede R03 (substituição de comprovante) porque um token comprometido **habilita e amplia** outros ataques: um atacante de posse do token de um orientador pode explorar a superfície completa do sistema em nome de outro usuário. O token é a chave mestra da sessão — sua proteção é condição para a segurança de todos os demais fluxos.

#### Por que R05 ocupa a 4ª posição, acima de riscos com pontuação 9

R05 (desabilitação da auditoria) tem pontuação 8, mas é posicionado acima de R02, R08 e R09 (pontuação 9) por seu **caráter transversal**: a ausência de logs de auditoria agrava a consequência de praticamente todos os outros riscos, tornando impossível detectar e responsabilizar qualquer violação. Um sistema sem auditoria ativa converte riscos altos em riscos sem possibilidade de resposta.

#### Por que R11 precede R02, R08 e R09

R11 (elevação de privilégios) tem pontuação 8, mas compromete a **estrutura de controle de acesso de todo o sistema**. Um estudante que acessa funções de coordenador pode alterar as regras do programa para todos os usuários — um dano sistêmico que transcende o impacto individual dos riscos de pontuação 9.

#### Posição de R12 (12º lugar)

Apesar de ter impacto 4 (Muito alto), R12 recebeu probabilidade 1 (Baixa) porque a exploração exige erro operacional grave de infraestrutura. Em condições normais de implantação, o script `bootstrap_admin.py` não fica exposto. A probabilidade baixa justifica a posição final, sem eliminar a necessidade de controle.

---
---

## Etapa 2 — continuação

---

## 10. Tratamento dos Riscos e Mapeamento para o NIST CSF 2.0

Esta seção define as estratégias de tratamento para cada risco, mapeia os riscos para as funções do NIST Cybersecurity Framework 2.0, apresenta o plano de tratamento com controles concretos, responsáveis e formas de verificação, estabelece a ordem inicial de implementação e estima o risco residual esperado.

> **Nota:** Esta seção está em elaboração e será completada nas próximas etapas do trabalho.
