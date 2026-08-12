# Seção 4 — Modelagem de Ameaças com STRIDE

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 4 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 4. Modelagem de Ameaças com STRIDE

A análise da metodologia `STRIDE` foi aplicada aos componentes, fluxos e ativos estratégicos do sistema **ThesisFlow**. Para cada uma das seis categorias, foram identificadas ameaças concretas e diretamente relacionadas ao contexto acadêmico do software. 

Estas ameaças originam diretamente os Eventos de Risco (`R01–R12`) avaliados na Etapa 2 e os Requisitos e Práticas de Código Seguro das Etapas 3 e 4.

---

### 4.1 Tabela consolidada de ameaças STRIDE

| ID | Categoria STRIDE | Componente ou ativo | Ameaça identificada | Possível impacto |
| :---: | :---: | :--- | :--- | :--- |
| `T01` | **Spoofing** | `Firebase Auth` / Token `JWT` | Um atacante rouba ou captura o token `JWT` de um usuário autenticado (via `XSS`, interceptação ou vazamento) e passa a utilizá-lo para autenticar requisições como se fosse a vítima. | Acesso completo à conta: leitura de dados pessoais, upload de arquivos e validação de atividades em nome da vítima. |
| `T02` | **Spoofing** | Cadastro de orientador | Um usuário se cadastra como orientador informando dados falsos de vínculo institucional, pois o sistema não valida o vínculo real com a universidade. | Acesso a dados privados de estudantes e possibilidade de validar créditos indevidamente simulando o papel de professor. |
| `T03` | **Tampering** | Comprovantes no `Firebase Storage` | Um estudante substitui o arquivo de comprovante legítimo por um documento forjado após o upload, explorando a URL de acesso ao `Storage` sem restrição de imutabilidade. | Validação de atividade creditável com documento falso, obtendo créditos acadêmicos indevidos. |
| `T04` | **Tampering** | Plano de trabalho e prazos | Um usuário com acesso indevido à API altera datas de prazo ou marcos do plano de trabalho de um estudante, modificando o registro sem autorização. | Mascaramento de atrasos acadêmicos, geração de inconsistências no histórico e dificuldade de auditoria posterior. |
| `T05` | **Repudiation** | Logs de auditoria (`@audit`) | O aspecto de auditoria é desabilitado em tempo de execução (via flag `ASPECTS_ENABLED`) ou os logs são apagados/alterados; um orientador nega ter aprovado determinada atividade. | Impossibilidade de responsabilizar o autor de uma operação, dificultando investigações de fraudes acadêmicas. |
| `T06` | **Repudiation** | Operações de coordenador | Um coordenador realiza uma operação administrativa (ex.: aprovação de extensão de prazo) e, na ausência de log imutável com identificação completa, nega posteriormente ter realizado a ação. | Contestações sem evidências formais e comprometimento da responsabilização institucional. |
| `T07` | **Information Disclosure** | API REST / `Firestore` | Um estudante autenticado modifica o identificador de outro estudante em uma requisição `GET` (ataque IDOR — *Insecure Direct Object Reference*), e a API retorna dados do outro estudante sem verificar a propriedade do recurso. | Exposição de dados pessoais, plano de trabalho, status acadêmico e produção científica de terceiros (violação da LGPD). |
| `T08` | **Information Disclosure** | `Firebase Storage` | A URL de download de um comprovante armazenado no `Firebase Storage` não exige autenticação para ser acessada; a URL é compartilhada ou descoberta por terceiros. | Exposição de documentos pessoais sensíveis (diplomas, certidões e artigos não publicados). |
| `T09` | **Denial of Service** | API FastAPI / Motor lógico | Um atacante envia um grande volume de requisições a endpoints que invocam o motor de inferência lógica, que realiza operações computacionalmente intensas sem limitação de taxa (*rate limiting*). | Degradação ou indisponibilidade do sistema durante períodos críticos (ex.: prazo final de qualificações e defesas). |
| `T10` | **Denial of Service** | `Firebase Storage` | Um usuário autenticado realiza upload massivo de arquivos de grande volume, esgotando a cota de armazenamento do plano Firebase utilizado pelo sistema. | Bloqueio de uploads legítimos de outros estudantes, impossibilitando o envio de comprovantes no prazo. |
| `T11` | **Elevation of Privilege** | Aspecto `@authorize` (`RBAC`) | Um estudante autenticado manipula uma requisição HTTP para chamar diretamente um endpoint restrito a coordenadores (ex.: `POST /activity-types`), explorando falha na verificação de papel ou ausência do decorator. | Acesso a funções administrativas: criação de tipos de atividades, aprovação de extensões e acesso a relatórios gerenciais. |
| `T12` | **Elevation of Privilege** | Script `bootstrap_admin.py` | O script de criação da conta inicial de coordenador fica acessível ou executável remotamente em ambiente de produção (ex.: via endpoint não autenticado ou acesso indevido ao servidor). | Criação arbitrária de conta de coordenador com privilégios máximos por um atacante externo, comprometendo todo o sistema. |

---

### 4.2 Interpretação e consolidação da análise

> **Análise Consolidada:** As doze ameaças identificadas abrangem todas as seis categorias do `STRIDE` no contexto específico do **ThesisFlow**. As ameaças de **Spoofing** comprometem a identidade dos usuários e a confiança nas ações realizadas. O **Tampering** afeta a integridade dos dados acadêmicos e dos comprovantes. A **Repudiation** prejudica a capacidade de auditoria e responsabilização. A **Information Disclosure** expõe dados pessoais protegidos pela `LGPD`. O **Denial of Service** pode impedir o uso do sistema em momentos críticos do calendário acadêmico. Por fim, a **Elevation of Privilege** pode comprometer toda a estrutura de controle de acesso do sistema.