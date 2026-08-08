# Issues do Trabalho — ThesisFlow · GP06

**Prazo:** 14/08/2026 | **Sistema:** ThesisFlow | **Repo:** [es-seguro-gp06](https://github.com/fadekanaan/es-seguro-gp06)

---

## Estado atual

| Etapa | Status |
|---|---|
| E1 — STRIDE + Casos de abuso | ✅ Completa |
| E2 — Critérios + Registro + Priorização (sec7–sec9) | ✅ Completa |
| E2 — Tratamento + NIST CSF + Considerações finais (sec10–sec11) | ✅ Completa |
| E3 — Requisitos + Mapeamento CWE/OWASP (sec12) | ✅ Completa |
| E3 — Diagrama + Decisões de arquitetura (sec13) | ✅ Completa |
| E4 — Código seguro e testes (sec14) | 🟡 Em andamento (Prática 1 concluída) |
| E5 — Verificação ZAP | ⬜ Aberta |
| E6 — Detecção de intrusões | ✅ Completa |
| E7 — DevSecOps + Vídeo final | ⬜ Aberta |

---

## Issues abertas

### Issue #5 — [E4] Práticas de código seguro com testes

**Arquivo a criar:** `docs/etapas/etapa-4/sec14-codigo-seguro.md`  
**Pasta de código:** `codigo/etapa-4/`

O enunciado pede **2 práticas de código seguro** relacionadas aos riscos e requisitos anteriores, com testes escritos **antes** da implementação.

**Prática 1 — Controle de autorização por propriedade de recurso** (R07, RS01, DA01)
- Referência: OWASP Authorization Cheat Sheet; CWE-639
- Testes antes do código: estudante tentando acessar dados de outro → HTTP 403; orientador acessando orientando → HTTP 200; coordenador → HTTP 200
- Implementar verificação `student.uid == authenticated_user.uid` no servidor antes de qualquer consulta ao repositório

**Prática 2 — Upload seguro com validação de tipo e hash** (R03, RS03, DA02)
- Referência: OWASP File Upload Cheat Sheet; CWE-434; OWASP ASVS v4 V12.2
- Testes antes do código: arquivo `.exe` → HTTP 422; arquivo > 10 MB → HTTP 413; PDF válido → HTTP 201 + hash armazenado
- Implementar validação de `content-type` real, limite de 10 MB e cálculo de hash SHA-256 antes do upload

**Commit sugerido:**
- **Prática 1 — Controle de autorização por propriedade de recurso (R07, RS01, DA01)**: ✅ **Concluída**
  - Implementação Python: [`codigo/etapa-4/pratica-1-autorizacao-por-recurso/authorization.py`](../codigo/etapa-4/pratica-1-autorizacao-por-recurso/authorization.py)
  - Testes Pytest: [`codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py`](../codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py) (100% aprovados)

- **Prática 2 — Upload seguro com validação de tipo e hash (R03, RS03, DA02)**: 🟡 **Pendente**
  - Referência: OWASP File Upload Cheat Sheet; CWE-434; OWASP ASVS v4 V12.2
  - Testes antes do código: arquivo `.exe` → HTTP 422; arquivo > 10 MB → HTTP 413; PDF válido → HTTP 201 + hash armazenado
  - Implementar validação de `content-type` real, limite de 10 MB e cálculo de hash SHA-256 antes do upload

---

### Issue #6 — [E5] Verificação de vulnerabilidades com ZAP

**Arquivo a criar:** `evidencias/etapa-5/relatorio-da-verificacao.md`  
**Pasta de evidências:** `evidencias/etapa-5/capturas-de-tela/`

Usar o **OWASP Juice Shop** como ambiente (autorizado para treinamento):

```bash
docker run -d -p 3000:3000 bkimminich/juice-shop
# Disponível em http://localhost:3000
```

Instalar ZAP: https://www.zaproxy.org/download/

**Passos:**
1. Abrir ZAP → Quick Start → Automated Scan → `http://localhost:3000` → Attack
2. Aguardar (5–15 min) → aba Alerts
3. Capturar tela da lista de alertas e detalhe de 3 alertas
4. Gerar relatório HTML: Report → Generate Report

**Entregável — tabela com 3 achados:**

| ID | Alerta | Evidência | Impacto | Relação OWASP:2025 ou CWE | Correção |
|---|---|---|---|---|---|
| A01 | ... | captura-de-tela | ... | ... | ... |
| A02 | ... | ... | ... | ... | ... |
| A03 | ... | ... | ... | ... | ... |

Alertas comuns no Juice Shop: Missing Anti-clickjacking Header, CSP Not Set, X-Content-Type-Options Missing, Server Version Disclosure.

**Commit sugerido:**
```
Adiciona verificação ZAP com análise dos achados A01-A03 (E5)
```

---

### Issue #7 — [E6] Roteiro de detecção de intrusões (✅ Concluída)

**Arquivo:** `roteiros/etapa-6-deteccao-de-intrusoes.md` (e consolidado em `docs/modelagem-de-ameacas.md`)

Roteiro **textual** elaborado com sucesso pelo integrante Marcus:
1. Conceitos de detecção x prevenção
2. Eventos monitorados do ThesisFlow
3. **3 regras de detecção** (D01 — IDOR, D02 — Flooding, D03 — Elevação de privilégios)
4. Fluxo de resposta após alerta em 7 passos com diagrama de texto

---

### Issue #8 — [E7] Pipeline DevSecOps e roteiro do vídeo final

**Arquivo a criar:** `roteiros/etapa-7-devsecops-e-video-final.md`

**Pipeline (tabela):**

| Momento | Atividade de segurança | Evidência produzida | Condição para continuar |
|---|---|---|---|
| Planejamento | STRIDE + análise de riscos (NIST Govern + Identify) | Tabela T01–T12; Registro R01–R12 | Riscos críticos identificados |
| Requisitos | Derivação de RS01–RS03 | Documento de requisitos | Requisitos revisados |
| Design | Arquitetura segura; DA01–DA03; mapeamento CWE/OWASP | Diagrama + tabela de decisões | Diagrama revisado |
| Código | Práticas P1–P2 com testes escritos antes | Código/pseudocódigo + testes | Testes dentro do esperado |
| Testes | ZAP Automated Scan; análise A01–A03 | Relatório ZAP + capturas | Achados críticos analisados |
| Implantação | Remoção do bootstrap endpoint; Cloud Audit Logs; sem segredos no repo | Checklist de produção | Zero endpoints privilegiados expostos |
| Operação | Regras de detecção E6; resposta a alertas | Roteiro de detecção | Incidentes tratados no fluxo definido |

**≥ 3 condições de bloqueio do pipeline:**
1. Alerta Critical/High no ZAP não analisado nem justificado como falso positivo
2. Segredo (chave, token, senha) encontrado em qualquer commit do repositório
3. Teste de segurança reprovado sem justificativa
4. Endpoint privilegiado sem `@authorize` identificado pelo script de auditoria
5. Dependência com CVE crítico sem versão corrigida disponível

**Vídeo (5–8 min) — sugestão de estrutura:**

| Trecho | Conteúdo | Tempo |
|---|---|---|
| Abertura | ThesisFlow: o que é e por que foi escolhido | ~30s |
| E1 | Ameaças STRIDE mais críticas e casos de abuso | ~1min |
| E2 | Riscos prioritários R07/R01/R03 e controles propostos | ~1min |
| E3 | Diagrama de arquitetura segura e decisões DA01–DA03 | ~1min |
| E4+E5 | Práticas de código e resultados do ZAP | ~1min |
| E6+E7 | Regras de detecção e pipeline DevSecOps | ~1min |
| Encerramento | O que o grupo aprendeu | ~30s |

**Commit sugerido:**
```
Adiciona pipeline DevSecOps com condições de bloqueio e roteiro do vídeo (E7)
```

---

## Regras de commit

- Mensagens **descritivas**: `Descreve controles para R01-R03` ✅ / `ajustes` ❌
- **Versionar tudo**: imagens, diagramas, arquivos-fonte (`.drawio`, `.mmd`)
- **Risco residual é estimativa** — não afirmar que risco foi eliminado sem testes reais
- Etapa 5: testar **apenas** o Juice Shop ou o próprio sistema — nunca sistemas de terceiros
- Vídeo: **5–8 minutos**; todos participam

---

## Referências

| Item | Link |
|---|---|
| Enunciado | [`enunciado.md`](../enunciado.md) |
| Documento consolidado | [`docs/modelagem-de-ameacas.md`](modelagem-de-ameacas.md) |
| OWASP Top 10:2025 | https://owasp.org/Top10/ |
| OWASP Cheat Sheet Series | https://cheatsheetseries.owasp.org |
| OWASP ASVS v4 | https://github.com/OWASP/ASVS |
| CWE List | https://cwe.mitre.org |
| Juice Shop | `docker run -d -p 3000:3000 bkimminich/juice-shop` |
| ZAP Download | https://www.zaproxy.org/download/ |
