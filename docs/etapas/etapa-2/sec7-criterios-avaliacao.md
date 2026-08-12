# Seção 7 — Critérios de Avaliação de Risco

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 7 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 7. Critérios de Avaliação de Risco

Esta seção define os critérios formais de probabilidade e impacto aplicados a todas as ameaças identificadas no **ThesisFlow** durante a Etapa 1 (`T01–T12`), transformando-as em eventos de risco mensuráveis e comparáveis. As escalas e matrizes adotadas seguem a metodologia do **NIST CSF 2.0** e as diretrizes formais da disciplina.

---

### 7.1 Critérios de probabilidade

A escala de probabilidade reflete a facilidade de exploração e a frequência esperada de ocorrência de um evento de risco, considerando os controles vigentes, o perfil dos usuários e a arquitetura do **ThesisFlow**.

| Valor | Classificação | Critério Técnico |
| :---: | :---: | :--- |
| `1` | **Baixa** | O evento depende de condições incomuns, acesso físico/infraestrutura específico ou altíssima capacidade técnica. |
| `2` | **Média-baixa** | O evento é possível, mas exige exploração de vulnerabilidade específica ou conhecimento de configurações internas. |
| `3` | **Média-alta** | O evento é plausível e pode ocorrer em condições normais de uso ou através de ataques automatizados comuns. |
| `4` | **Alta** | O evento possui alta facilidade de execução, podendo ocorrer com frequência ou durante janelas previsíveis do sistema. |

---

### 7.2 Critérios de impacto

A escala de impacto mensura a severidade das consequências de um incidente de segurança sobre a integridade acadêmica, a privacidade dos usuários (`LGPD`), a disponibilidade do sistema e a reputação institucional.

| Valor | Classificação | Critério Técnico |
| :---: | :---: | :--- |
| `1` | **Baixo** | Causa inconveniência mínima sem perda de dados ou interrupção de serviços, com correção trivial. |
| `2` | **Moderado** | Causa interrupção localizada ou inconsistência temporária com possibilidade de recuperação direta. |
| `3` | **Alto** | Causa prejuízo relevante aos usuários, exposição de dados pessoais ou atraso em marcos do calendário acadêmico. |
| `4` | **Muito alto** | Compromete operações críticas, expõe dados em massa (LGPD), afeta a concessão de diplomas ou paralisa o sistema. |

---

### 7.3 Cálculo e matriz de classificação do nível de risco

A pontuação quantitativa de cada risco é calculada pela multiplicação escalar dos fatores de probabilidade e impacto:

$$\text{Pontuação} = \text{Probabilidade} \times \text{Impacto}$$

O valor resultante determina a severidade do nível de risco, conforme a matriz de classificação abaixo:

| Pontuação | Nível do risco | Ação Recomendada |
| :---: | :---: | :--- |
| `1 a 3` | **Baixo** | Monitoramento periódico e correções de rotina. |
| `4 a 7` | **Médio** | Mitigação planejada no ciclo de desenvolvimento. |
| `8 a 11` | **Alto** | Requer implementação prioritária de controles e requisitos de segurança. |
| `12 a 16` | **Crítico** | Exige mitigação imediata e testes de validação obrigatórios (Etapa 3 e Etapa 4). |

> A pontuação quantitativa orienta a priorização no Registro de Riscos (Seção 8), mas é complementada pela análise contextual das dependências do sistema na Seção 9 (Priorização dos Riscos).