# Seção 9 — Priorização dos Riscos

> **Arquivo de trabalho individual:** este arquivo corresponde à Seção 9 do documento principal [`docs/modelagem-de-ameacas.md`](../../modelagem-de-ameacas.md).

---

## 9. Priorização dos Riscos

A priorização define a ordem em que os riscos devem receber atenção e recursos. A pontuação calculada (Probabilidade × Impacto) é o ponto de partida, mas não o único critério. A ordenação final também considera: a gravidade das consequências, o número de usuários afetados, a facilidade de exploração, a importância do ativo comprometido, a possibilidade de recuperação e as dependências entre os riscos.

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

R07 e R01 e R03 compartilham a mesma pontuação máxima (12). O desempate é definido pela **trivialidade de exploração** e pela **abrangência do impacto**. O IDOR (R07) não exige ferramentas especializadas, comprometimento prévio de credenciais ou conhecimento técnico avançado — qualquer estudante autenticado consegue explorar a vulnerabilidade simplesmente alterando um identificador na URL. Além disso, o impacto afeta potencialmente **todos os estudantes do programa de forma simultânea**, caracterizando uma violação em massa de dados pessoais com implicações diretas da `LGPD`.

#### Por que R01 precede R03

Ambos têm pontuação 12. R01 (roubo de token) precede R03 (substituição de comprovante) porque um token comprometido **habilita e amplia** outros ataques: um atacante de posse do token de um orientador pode tanto realizar o caso de abuso CA05 (negar validações) quanto explorar outras superfícies do sistema. O token é a chave mestra da sessão — sua proteção é condição para a segurança de todos os demais fluxos.

#### Por que R05 ocupa a 4ª posição, acima de riscos com pontuação 9

R05 (desabilitação da auditoria) tem pontuação 8, mas é posicionado acima de R02, R08 e R09 (pontuação 9) por seu **caráter transversal**: a ausência de logs de auditoria agrava a consequência de praticamente todos os outros riscos, tornando impossível detectar e responsabilizar qualquer violação. Um sistema sem auditoria ativa converte riscos altos em riscos sem possibilidade de resposta.

#### Por que R11 precede R02, R08 e R09

R11 (elevação de privilégios) tem pontuação 8, mas compromete a **estrutura de controle de acesso de todo o sistema**. Um estudante que acessa funções de coordenador pode alterar as regras do programa para todos os usuários — um dano sistêmico que transcende o impacto individual dos riscos de pontuação 9.

#### Posição de R12 (12º lugar)

Apesar de ter impacto 4 (Muito alto), R12 recebeu probabilidade 1 (Baixa) porque a exploração exige erro operacional grave em infraestrutura. Em condições normais de implantação, o script `bootstrap_admin.py` não fica exposto. A probabilidade baixa justifica a posição final, sem eliminar a necessidade de controle.
