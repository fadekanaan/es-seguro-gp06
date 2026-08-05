# Seção 7 — Critérios de Avaliação de Risco

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 7 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

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

A probabilidade não é atribuída por intuição. Cada valor é justificado com base nas características do sistema, nas vulnerabilidades identificadas, nas condições de exploração e no contexto de uso do **ThesisFlow** (ver Seção 8 — Registro de Riscos).

---

### 7.2 Critérios de impacto

A escala de impacto reflete as consequências de um evento de risco bem-sucedido sobre os usuários, os dados, a integridade acadêmica e a conformidade legal do sistema.

| Valor | Classificação | Critério |
| :---: | :---: | :--- |
| `1` | Baixo | Causa pequeno transtorno e pode ser corrigido rapidamente |
| `2` | Moderado | Causa interrupção ou inconsistência limitada, com possibilidade de recuperação |
| `3` | Alto | Causa prejuízo relevante aos usuários, ao negócio, à administração ou à privacidade |
| `4` | Muito alto | Pode afetar muitos usuários, comprometer operações críticas ou causar prejuízo grave |

Na avaliação do impacto, foram considerados: prejuízo direto aos usuários, exposição de dados pessoais protegidos pela `LGPD`, interrupção de operações críticas do calendário acadêmico, comprometimento da integridade das decisões de validação e dificuldade de recuperação.

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

> A pontuação auxilia na comparação entre riscos, mas não substitui a análise contextual. Dois riscos com a mesma pontuação podem receber prioridades distintas em função da gravidade das consequências, das dependências entre componentes ou da dificuldade de recuperação (ver Seção 9 — Priorização dos Riscos).
