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
| E4 — Código seguro e testes (sec14) | ✅ Completa |
| E5 — Verificação ZAP | ✅ Completa |
| E6 — Detecção de intrusões | ✅ Completa |
| E7 — DevSecOps + Vídeo final | ✅ Completa |

---

## Issues abertas

*(Etapa 7)*

---

## Issues concluídas

### Issue #5 — [E4] Práticas de código seguro com testes (✅ Concluída)

**Arquivo:** `docs/etapas/etapa-4/sec14-codigo-seguro.md` (e consolidado em `docs/modelagem-de-ameacas.md`)  
**Pasta de código:** `codigo/etapa-4/`

- **Prática 1 — Controle de autorização por propriedade de recurso (R07, RS01, DA01)**: ✅ **Concluída**
  - Módulo Python: [`codigo/etapa-4/pratica-1-autorizacao-por-recurso/authorization.py`](../codigo/etapa-4/pratica-1-autorizacao-por-recurso/authorization.py)
  - Testes Pytest: [`codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py`](../codigo/etapa-4/pratica-1-autorizacao-por-recurso/test_authorization.py) (100% aprovados)

- **Prática 2 — Upload seguro com validação de tipo e hash (R03, RS03, DA02)**: ✅ **Concluída**
  - Módulo Python: [`codigo/etapa-4/pratica-2-upload-seguro/upload_service.py`](../codigo/etapa-4/pratica-2-upload-seguro/upload_service.py)
  - Testes Pytest: [`codigo/etapa-4/pratica-2-upload-seguro/test_upload_service.py`](../codigo/etapa-4/pratica-2-upload-seguro/test_upload_service.py) (100% aprovados)


---

### Issue #6 — [E5] Verificação de vulnerabilidades com ZAP (✅ Concluída)

**Arquivo:** [`evidencias/etapa-5/relatorio-da-verificacao.md`](../evidencias/etapa-5/relatorio-da-verificacao.md)

**Análise acadêmica:** [`docs/etapas/etapa-5/sec15-verificacao-vulnerabilidades.md`](etapas/etapa-5/sec15-verificacao-vulnerabilidades.md)

**Pasta de evidências:** `evidencias/etapa-5/capturas-de-tela/`

Foi utilizado o próprio **ThesisFlow**, revisão `486219c46ffce643e567a76b737e1f7b4cfc9964`, com o **OWASP ZAP 2.17.0**. A sessão foi local, autenticada e passiva. Firebase Authentication e Firestore foram emulados porque as credenciais reais não estavam disponíveis; frontend e backend permaneceram os componentes reais do projeto.

**Resultado da sessão:**

- `104` URLs registradas;
- `18` rotas autenticadas do backend responderam `HTTP 200`;
- `62` instâncias de alerta: 14 médias, 39 baixas e 9 informativas;
- `9` tipos únicos no relatório: 2 médios, 4 baixos e 3 informativos;
- relatório HTML e JSON, log, configuração e seis capturas versionados.

**Entregável — tabela com 3 achados:**

| ID | Alerta | Evidência | Impacto | Relação OWASP:2025 ou CWE | Correção |
|---|---|---|---|---|---|
| A01 | CSP ausente | [captura](../evidencias/etapa-5/capturas-de-tela/04-achado-a01-csp.jpg) | Defesa adicional contra XSS ausente | R01 / OWASP A05:2025 / CWE-693 | Implantar CSP restritiva gradualmente |
| A02 | Proteção contra clickjacking ausente | [captura](../evidencias/etapa-5/capturas-de-tela/05-achado-a02-clickjacking.jpg) | Possibilidade de enquadrar a interface e induzir cliques | OWASP A05:2025 / CWE-1021 | Aplicar `frame-ancestors 'none'` e `X-Frame-Options: DENY` |
| A03 | Identificador inválido retorna `HTTP 500` | [captura](../evidencias/etapa-5/capturas-de-tela/06-achado-a03-erros-http-500.jpg) | Tratamento de entrada/erro inadequado; sem detalhe sensível observado | OWASP A05:2025 / CWE-550 / CWE-1295 | Validar o ID e responder `404` ou `422` |

Os achados foram interpretados sem afirmar exploração. As limitações do spider tradicional e da navegação sem autenticação foram registradas no relatório; diagnósticos não versionados de tentativas preparatórias foram excluídos das conclusões.

**Commits realizados:**
```
Documenta ambiente e configuração da verificação ZAP (E5)
Adiciona relatório e evidências da execução do ZAP (E5)
Analisa os achados A01-A03 e propõe correções (E5)
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

### Issue #8 — [E7] Pipeline DevSecOps e roteiro do vídeo final (✅ Concluída)

**Arquivos criados:** `roteiros/etapa-7-devsecops.md` e `roteiros/etapa-7-video-final.md`

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
- Etapa 5: testar **apenas** ambiente autorizado; nesta entrega, o próprio ThesisFlow local — nunca sistemas de terceiros
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
| Firebase Local Emulator Suite | https://firebase.google.com/docs/emulator-suite |
| ZAP Download | https://www.zaproxy.org/download/ |
