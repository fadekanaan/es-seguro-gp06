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
| E7 — DevSecOps + Vídeo final | ⬜ Aberta |

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

Foi utilizado o **OWASP Juice Shop 20.1.1** como ambiente local e autorizado para treinamento, com o **OWASP ZAP 2.17.0** em Baseline Scan.

```powershell
docker network create es-seguro-e5
docker run --detach `
  --name es-seguro-juice-shop `
  --network es-seguro-e5 `
  --publish 127.0.0.1:3000:3000 `
  bkimminich/juice-shop@sha256:e68144772ebaaca0ec117b38d44903af92416793230288ef7c5437fc4f26850a
```

**Resultado da sessão:**

- `158` URLs observadas;
- `59` regras aprovadas;
- `8` identificadores com aviso;
- `0` regras configuradas como falha;
- relatório HTML e JSON, log, configuração reproduzível e cinco capturas versionados.

**Entregável — tabela com 3 achados:**

| ID | Alerta | Evidência | Impacto | Relação OWASP:2025 ou CWE | Correção |
|---|---|---|---|---|---|
| A01 | CSP ausente | [captura](../evidencias/etapa-5/capturas-de-tela/03-achado-a01.jpg) | Defesa adicional contra XSS ausente | OWASP A02:2025 / CWE-693 | Implantar CSP restritiva gradualmente |
| A02 | CORS permissivo | [captura](../evidencias/etapa-5/capturas-de-tela/04-achado-a02.jpg) | Leitura entre origens; impacto limitado no recurso público observado | OWASP A02:2025 / CWE-942 | Restringir origens e escopo do CORS |
| A03 | `Feature-Policy` obsoleto em subrecursos | [captura](../evidencias/etapa-5/capturas-de-tela/05-achado-a03.jpg) | Sem impacto efetivo demonstrado nos arquivos `chunk-*.js` | OWASP A02:2025 / CWE-16 | Remover dos subrecursos e configurar `Permissions-Policy` no HTML principal, se necessário |

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
