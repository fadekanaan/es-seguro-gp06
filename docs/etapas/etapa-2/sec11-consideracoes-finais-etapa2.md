# Seção 11 — Considerações Finais da Etapa 2

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 11 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 11. Considerações Finais da Etapa 2

### 11.1 Riscos mais importantes e razões da priorização

Os três riscos considerados mais críticos são **R07** (IDOR), **R01** (roubo de token JWT) e **R03** (substituição de comprovante forjado), todos com pontuação 12. A priorização não foi determinada apenas pela pontuação, mas pela combinação de criticidade, trivialidade de exploração e abrangência do impacto.

O **R07** encabeça a lista porque não exige ferramentas ou conhecimento técnico avançado — qualquer estudante autenticado pode tentar modificar um identificador na URL e obter dados de outro estudante. O impacto é imediato e em massa, com implicações diretas da `LGPD`. O **R01** precede o **R03** porque um token comprometido funciona como chave mestra: um atacante com o token de um orientador ou coordenador pode realizar operações que ampliam o efeito de praticamente todos os outros riscos.

O **R05** (desabilitação da auditoria), apesar de pontuação 8, recebeu alta prioridade de tratamento por seu caráter **transversal**: sem logs de auditoria funcionando, todos os outros controles tornam-se indetectáveis quando falharem.

### 11.2 Estratégias de tratamento predominantes

A estratégia **Reduzir** foi aplicada a dez dos doze riscos. Isso reflete a natureza do sistema: a maioria das vulnerabilidades identificadas admite controles técnicos específicos — verificação de propriedade de recurso, imutabilidade de arquivo, rate limiting, cookies seguros — sem necessidade de eliminar as funcionalidades que originam o risco.

A estratégia **Evitar** foi aplicada apenas a **R05** e **R12**, onde a condição que origina o risco é desnecessária em produção: a flag de desabilitação da auditoria e o endpoint que invoca o script de bootstrap não têm justificativa de existência em ambiente de produção, portanto a solução correta é eliminá-los, não controlá-los.

Nenhum risco foi classificado como **Aceitar** nesta etapa, em função da maturidade ainda baixa dos controles implementados e da sensibilidade dos dados acadêmicos envolvidos.

### 11.3 Funções do NIST CSF mais relevantes

As funções **Protect** e **Detect** são as mais relevantes para o **ThesisFlow** neste momento. Protect porque os controles mais urgentes — verificação de propriedade de recurso, imutabilidade de arquivos, cookies seguros, rate limiting — são todos salvaguardas preventivas. Detect porque o sistema depende fortemente dos logs do aspecto `@audit` para responsabilizar ações de orientadores e coordenadores; sem detecção, as ameaças de Repudiation tornam-se irresolúveis.

A função **Govern** é especialmente relevante para **R02**, **R05**, **R11** e **R12** — riscos que dependem de políticas e decisões organizacionais (processo de aprovação de orientadores, obrigatoriedade de auditoria, revisão de código com checklist de decorators), não apenas de implementação técnica.

### 11.4 Controles considerados essenciais

1. **Verificação de propriedade de recurso** (R07): controle de maior retorno por menor custo — elimina o IDOR com uma verificação de igualdade de UID no servidor.
2. **Remoção da flag de auditoria + Cloud Audit Logs** (R05): assegura a rastreabilidade transversal de todas as operações.
3. **Cookie `httpOnly` + TTL curto** (R01): reduz o impacto de XSS e limita a janela de exploração de tokens comprometidos.
4. **Imutabilidade no Storage + hash SHA-256** (R03): protege a integridade dos comprovantes, que são a base de todas as decisões de validação acadêmica.

### 11.5 Principais dificuldades

A maior dificuldade desta etapa foi definir controles **específicos e observáveis** sem recair em propostas genéricas. Expressões como "usar criptografia" ou "melhorar a autenticação" são insuficientes: é necessário especificar onde o controle é aplicado, como funciona, quem é responsável e como será verificado.

Outra dificuldade foi estimar o risco residual de forma realista. Como os controles ainda não foram implementados, qualquer afirmação sobre redução de risco é uma estimativa — e o enunciado é claro ao dizer que a redução só pode ser confirmada após implementação, testes e evidências.

Por fim, a diferenciação entre **função do NIST** (ex: Protect), **resultado esperado** (ex: acesso às contas protegido) e **controle específico** (ex: cookie `httpOnly`) exigiu atenção constante para não confundir os três níveis na análise.

### 11.6 Limitações da avaliação

- Os controles propostos são teóricos: nenhum foi implementado e testado nesta etapa.
- As estimativas de risco residual dependem de implementação correta e de ausência de outros vetores não mapeados.
- A análise cobre os riscos identificados na Etapa 1; ameaças não contempladas no STRIDE original não foram avaliadas aqui.
- O contexto acadêmico do sistema reduz alguns vetores (ex: flooding menos provável entre estudantes reais) e amplifica outros (ex: motivação para fraude de comprovantes é alta quando créditos estão em jogo).

### 11.7 Pontos a detalhar nas próximas etapas

- **Etapa 3:** Traduzir os controles prioritários em requisitos verificáveis e decisões de arquitetura; produzir diagrama com posição dos controles.
- **Etapa 4:** Implementar ou descrever em pseudocódigo as práticas de código seguro para R07 (verificação de propriedade) e R03 (upload com validação e hash).
- **Etapa 5:** Verificar com ferramenta (ZAP) se vulnerabilidades conhecidas são detectáveis no ambiente de teste.
- **Etapas 6–7:** Definir regras de detecção baseadas nos riscos prioritários e integrar segurança ao ciclo de desenvolvimento como prática contínua.
