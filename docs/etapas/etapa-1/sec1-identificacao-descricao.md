# Seção 1 — Identificação e Descrição do Sistema

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 1 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 1. Identificação do sistema

- **Nome do sistema:** **ThesisFlow** — Sistema de Acompanhamento de Pós-Graduação (Mestrado)
- **Integrantes do grupo:**
  - Artur Wahlbrink Kraemer
  - Marcus Vinicius Morini Querol Junior
  - Bernardo Gomes Dorneles
  - Gustavo Fernandes dos Anjos
  - Fade Hassan Husein Kanaan
  - Rodrigo Thoma da Silva
- **Repositório oficial:** [https://github.com/fadekanaan/es-seguro-gp06](https://github.com/fadekanaan/es-seguro-gp06)
- **Justificativa da Escolha:** O **ThesisFlow** foi selecionado por ser um sistema real desenvolvido pelo próprio grupo durante a disciplina de Engenharia de Software no mesmo semestre. Isso possibilita uma análise de segurança contextualizada, precisa e aprofundada, visto que conhecemos a fundo sua arquitetura, fluxos de dados, componentes e integrações. O sistema reúne múltiplos perfis de acesso, processa dados pessoais e acadêmicos sensíveis protegidos pela LGPD, realiza controle de acesso baseado em papéis (`RBAC`) e integra serviços externos (como `Firebase Auth` e `Firebase Storage`), tornando-o o objeto de estudo ideal para a aplicação do **STRIDE**, do **NIST CSF 2.0** e do pipeline **DevSecOps**.

---

## 2. Descrição do sistema

O **ThesisFlow** é um sistema web de acompanhamento acadêmico voltado a programas de pós-graduação (*stricto sensu*) com duração padrão de 24 meses. Seu objetivo é auxiliar estudantes, orientadores e coordenadores no gerenciamento do progresso acadêmico, cobrindo o plano de trabalho, cumprimento de tarefas, submissão e validação de atividades creditáveis, prazos, status acadêmico e verificação dos requisitos para defesa de dissertação.

### 2.1 Problema que o sistema resolve

Programas de pós-graduação exigem o cumprimento rigoroso de prazos e créditos acadêmicos ao longo do curso. Sem uma solução centralizada, o acompanhamento torna-se fragmentado em planilhas, e-mails e processos manuais passíveis de erros e fraudes. O **ThesisFlow** centraliza essa gestão em uma plataforma auditável, transparente e segura.

### 2.2 Perfis de usuários e papéis de acesso

| Perfil | Descrição e Atribuições no Sistema |
| :---: | :--- |
| **Estudante** | Usuário matriculado no programa. Registra atividades, realiza upload de comprovantes, acompanha seu plano de trabalho e consulta seu status acadêmico individual. |
| **Orientador** | Docente responsável por acompanhar e validar as atividades creditáveis e produções científicas de seus orientandos vinculados. |
| **Coordenador** | Perfil administrativo de nível elevado. Gerencia usuários, define políticas de crédito, aprova extensões de prazo, emite relatórios gerenciais e configura parâmetros do programa. |

### 2.3 Principais funcionalidades

- Cadastro e gerenciamento de estudantes, orientadores e coordenadores.
- Gestão e acompanhamento das etapas e marcos do plano de trabalho.
- Registro de atividades creditáveis com upload de comprovantes (certificados, artigos e diplomas).
- Fluxo de validação e homologação de créditos por orientadores.
- Inferência automática do status acadêmico por motor lógico interno.
- Disparo de alertas e notificações automáticas de prazos e pendências.
- Geração de relatórios gerenciais com visão consolidada para coordenadores.
- Registro de produções científicas com metadados de autoria.

### 2.4 Informações armazenadas e transmitidas

- **Dados pessoais e cadastrais:** Nome, e-mail institucional e número de matrícula.
- **Credenciais de acesso:** Gerenciadas de forma segura via `Firebase Authentication`.
- **Registros acadêmicos:** Planos de trabalho, datas, marcos, prazos e metadados de publicações.
- **Documentos e comprovantes:** Arquivos armazenados em nuvem via `Firebase Storage`.
- **Rastreabilidade:** Histórico de validações, aprovações e logs imutáveis de auditoria (`@audit`).
- **Status acadêmico:** Situação inferida do estudante (regular, pendente, apto para defesa).

### 2.5 Ativos e recursos que precisam ser protegidos

- Credenciais e tokens de autenticação (`JWT`).
- Dados pessoais dos estudantes (proteção contra vazamentos — LGPD).
- Arquivos de comprovantes e documentos anexados (`Firebase Storage`).
- Registros de validação e concessão de créditos acadêmicos (integridade).
- Logs de auditoria do sistema (não-repúdio).
- Permissões e papéis de acesso (`RBAC / ABAC`).