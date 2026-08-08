# ThesisFlow — Análise de Segurança

**Repositório do Grupo 06 — Engenharia de Software Seguro**  
*Universidade Federal do Pampa (UNIPAMPA) — Alegrete/RS*

> **Repositório da Aplicação:** [`ThesisFlow` no GitHub](https://github.com/fadekanaan/thesis-flow)  
> **Prazo final:** 14 de agosto de 2026

---

## 👥 Integrantes do Grupo

| # | Nome do Integrante |
| :---: | :--- |
| `01` | Artur Wahlbrink Kraemer |
| `02` | Marcus Vinicius Morini Querol Junior |
| `03` | Bernardo Gomes Dorneles |
| `04` | Gustavo Fernandes dos Anjos |
| `05` | Fade Hassan Husein Kanaan |
| `06` | Rodrigo Thoma da Silva |

---

## 📋 Sobre o Trabalho

Este repositório contém a análise de segurança completa do sistema **ThesisFlow** — um sistema de acompanhamento acadêmico de mestrado desenvolvido pelo grupo na disciplina de Resolução de Problemas III (Engenharia de Software, UNIPAMPA). O trabalho cobre modelagem de ameaças com `STRIDE`, casos de abuso, análise e priorização de riscos com o `NIST Cybersecurity Framework 2.0`, projeto de arquitetura segura, práticas de código seguro, verificação de vulnerabilidades, detecção de intrusões e pipeline DevSecOps.

---

## 📄 Documento Principal

O documento consolidado com todas as etapas está em:

👉 **[`docs/modelagem-de-ameacas.md`](docs/modelagem-de-ameacas.md)**

---

## 🗂️ Entregáveis por Etapa

| Etapa | Conteúdo | Arquivos | Status |
| :---: | :--- | :--- | :---: |
| **E1** | STRIDE e Casos de Abuso | [`docs/etapas/etapa-1/`](docs/etapas/etapa-1/) | ✅ |
| **E2** | Análise, Priorização e Tratamento de Riscos (NIST CSF 2.0) | [`docs/etapas/etapa-2/`](docs/etapas/etapa-2/) | ✅ |
| **E3** | Arquitetura Segura — Requisitos, Diagrama e Decisões | [`docs/etapas/etapa-3/`](docs/etapas/etapa-3/) | ✅ |
| **E4** | Código Seguro e Testes de Segurança | [`docs/etapas/etapa-4/`](docs/etapas/etapa-4/) + [`codigo/etapa-4/`](codigo/etapa-4/) | ⬜ |
| **E5** | Verificação de Vulnerabilidades (ZAP) | [`evidencias/etapa-5/`](evidencias/etapa-5/) | ⬜ |
| **E6** | Monitoramento e Detecção de Intrusões | [`roteiros/etapa-6-deteccao-de-intrusoes.md`](roteiros/etapa-6-deteccao-de-intrusoes.md) | ✅ |
| **E7** | DevSecOps e Vídeo Final | [`roteiros/etapa-7-devsecops-e-video-final.md`](roteiros/etapa-7-devsecops-e-video-final.md) | ⬜ |

---

## 🗃️ Estrutura do Repositório

```text
es-seguro-gp06/
├── README.md                          ← Esta página
├── enunciado.md                       ← Enunciado completo da disciplina
│
├── docs/
│   ├── modelagem-de-ameacas.md        ← Documento consolidado (todas as etapas)
│   ├── issues-trabalho.md             ← Issues abertas e guia de contribuição
│   └── etapas/
│       ├── etapa-1/                   ← sec1 a sec6 (E1)
│       ├── etapa-2/                   ← sec7 a sec11 (E2)
│       ├── etapa-3/                   ← sec12 a sec13 (E3)
│       ├── etapa-4/                   ← sec14 (E4) — a fazer
│       └── etapa-5/                   ← (E5) — a fazer
│
├── diagramas/
│   ├── etapa-1/                       ← Diagramas da E1 (contexto, fluxo, casos de abuso)
│   │   ├── diagrama-contexto.png
│   │   ├── diagrama-fluxo-dados.png
│   │   └── diagrama-casos-de-abuso.png
│   └── etapa-3/                       ← Arquitetura segura (E3)
│       └── arquitetura-segura.png     ← Imagem exportada
│
├── codigo/
│   └── etapa-4/                       ← Práticas de código seguro (E4) — a fazer
│       ├── pratica-1-autorizacao-por-recurso/
│       └── pratica-2-upload-seguro/
│
├── evidencias/
│   └── etapa-5/                       ← Relatório ZAP + capturas (E5) — a fazer
│       └── capturas-de-tela/
│
└── roteiros/
    ├── etapa-6-deteccao-de-intrusoes.md    ← (E6) — concluído
    └── etapa-7-devsecops-e-video-final.md  ← (E7) — a fazer
```

---

## 🔗 Links Rápidos

| Item | Link |
| :--- | :--- |
| Repositório | [github.com/fadekanaan/es-seguro-gp06](https://github.com/fadekanaan/es-seguro-gp06) |
| Issues abertas | [`docs/issues-trabalho.md`](docs/issues-trabalho.md) |
| Enunciado da disciplina | [`enunciado.md`](enunciado.md) |
| Repositório do ThesisFlow | [github.com/fadekanaan/thesis-flow](https://github.com/fadekanaan/thesis-flow) |
