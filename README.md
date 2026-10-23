# Robô de licitações (Blue Belt)

Usa a coleta diária do PNCP (Portal Nacional de Contratações Públicas), separa as contratações com propostas em aberto que cabem nos CNAEs da Blue Belt Comércio e Serviço Ltda e publica um painel web com filtros.

- Fonte: API pública de consulta do PNCP. Pela Lei 14.133/2021, órgãos federais, estaduais e municipais publicam ali, mesmo quando a disputa acontece em outro portal (Compras.gov.br, BLL, Licitanet etc.).
- Modalidades: pregão eletrônico e presencial, concorrência eletrônica e dispensa.
- Categorias, montadas a partir do cartão CNPJ:
  - **Material de consumo**: papelaria e expediente, material escolar, limpeza e higiene, copa e descartáveis, água mineral, gêneros alimentícios, EPI e uniformes profissionais, toner e cartuchos.
  - **Material elétrico e construção**: material elétrico, lâmpadas e luminárias, material de construção e hidráulico.
  - **Manutenção e obras**: manutenção predial, instalação elétrica, ar-condicionado, hidráulica, divisórias e forros, pintura e pequenos reparos, iluminação pública e rede elétrica, paisagismo.
  - **Alimentação**: refeições prontas, quentinhas, coffee break.
- Abrangência: materiais em RJ, ES, MG e SP; manutenção, obras e alimentação só no RJ, porque exigem equipe no local.
- Ficam de fora objetos que a empresa não tem CNAE para atender, mesmo que pareçam próximos: limpeza terceirizada com mão de obra, vigilância, dedetização, móveis, eletrodomésticos, uniformes escolares, medicamentos e material hospitalar, veículos, obras de pavimentação e construção de prédios, chamadas públicas da agricultura familiar.
- Cada licitação traz avisos práticos: serviço de engenharia (CREA e responsável técnico), alimentação (licença sanitária), merenda e perecíveis (logística), toner (original ou compatível) e entrega fora do RJ.
- Para cada licitação encontrada, o robô lê os itens no PNCP e marca se há participação exclusiva ou cota para ME/EPP. A Blue Belt é ME.
- Roda no GitHub Actions às 08:00 (todo dia) e às 14:00 (dias úteis).

## De onde vêm os dados (desde 23/10/2026)

O robô não lista mais as licitações direto no PNCP. A coleta é feita uma vez só, para as 27 UFs, pelo repositório `licitacoes-ti` (robô da ISAKMP), em 6 grupos de UFs em paralelo e de forma incremental. Os dados brutos ficam publicados em `https://mbritorj.github.io/licitacoes-ti/bruto/` (endereço em `config.json`, campo `fonte_bruto`).

Este repositório só classifica esses dados com o seu `config.json`, consulta no PNCP os itens das licitações selecionadas (ME/EPP e orçamento sigiloso) e publica o painel. Com isso o PNCP recebe metade das chamadas e cada execução leva poucos minutos. A leitura de itens fica limitada a 350 contratações por rodada (as que encerram antes); o resto é completado nas rodadas seguintes.

Se a coleta compartilhada falhar ou atrasar, o painel usa a última coleta publicada e mostra no topo de quando são os dados de cada grupo.

Objetos de prestação de serviço (`padrao_servico`) não entram como material só por citarem materiais ou ferramentas no texto. Por isso uma reforma em MG com "fornecimento de materiais e ferramentas" fica de fora, enquanto a manutenção predial no RJ entra.

## Instalação (uma vez, uns 15 minutos)

1. **Criar o repositório.** Em github.com, clique em **New repository**, dê um nome (ex.: `licitacoes-bluebelt`) e marque **Public**. No plano gratuito, o painel (GitHub Pages) só funciona em repositório público. O conteúdo são dados públicos de licitação.
2. **Enviar os arquivos.** Na página do repositório, clique em **uploading an existing file** e arraste todo o conteúdo desta pasta (incluindo a pasta `.github`). No Mac, a pasta `.github` fica oculta no Finder: use `Cmd + Shift + .` para mostrá-la. Clique em **Commit changes**.
3. **Dar permissão de escrita ao robô.** Settings > Actions > General > Workflow permissions > marque **Read and write permissions** > Save.
4. **Ativar o painel.** Settings > Pages > Build and deployment > Source: **GitHub Actions**. O endereço fica no formato `https://SEU-USUARIO.github.io/licitacoes-bluebelt/`.
5. **Primeira execução.** Aba **Actions** > **Robô de licitações Blue Belt** > **Run workflow**. Quando terminar (ícone verde), abra o endereço do painel.

## Ajustes no dia a dia

Tudo fica em `config.json`, que dá para editar direto no site do GitHub (ícone de lápis):

- `ufs`: UFs consideradas (a coleta cobre o Brasil todo; aqui se escolhe o que entra no painel).
- `ufs_por_categoria`: em quais estados cada categoria vale. Categoria que não aparece aqui vale em todos.
- `modalidades`: códigos do PNCP (4 concorrência eletrônica, 5 concorrência presencial, 6 pregão eletrônico, 7 pregão presencial, 8 dispensa, 12 credenciamento).
- `categorias`: termos de busca de cada tipo, com peso. Peso 3 basta para incluir a licitação; pesos 1 e 2 precisam somar com outro termo.
- `exclusoes`: termos que derrubam falsos positivos e objetos fora do CNAE.
- `alertas_por_categoria` e `alertas_por_termo`: avisos que aparecem no cartão de cada licitação.
- `max_consultas_itens`: quantas contratações têm os itens lidos por rodada.
- `padrao_servico` e `padrao_fornecimento`: identificam objetos de prestação de serviço e de compra de bens.
- `fonte_bruto`: endereço da coleta compartilhada.
- `valor_limite_me_epp`: valor até o qual a licitação é marcada como faixa de ME/EPP (R$ 80 mil, art. 48 da LC 123).

Se a Blue Belt incluir CNAEs novos no cartão CNPJ, acrescente os termos da atividade em `categorias` e retire o que estiver em `exclusoes`.

Depois de mexer nos termos, rode o workflow manualmente para ver o efeito. O teste em `tests/teste_classificacao.py` roda antes de cada coleta e para a execução se uma alteração fizer o robô deixar de reconhecer casos básicos (ou passar a aceitar "aquisição de medicamentos", por exemplo). Se você incluir um termo novo, vale acrescentar um exemplo lá também.

## Aba "Prefeituras pequenas RJ"

Lista os 26 municípios do RJ com até 20 mil habitantes, a plataforma em que cada um faz a disputa e como se cadastrar (levantamento de outubro de 2026). Esses municípios têm até abril de 2027 para publicar tudo em meio eletrônico, então parte das compras ainda não chega ao PNCP.

## Limitações

- A classificação olha o texto do objeto. Objeto genérico ("aquisição de materiais diversos") pode ficar de fora; objeto com termo usado em outro sentido pode entrar. Ajuste os termos conforme aparecerem casos.
- A compatibilidade com o CNAE é uma triagem. Antes de participar, confira o objeto do edital contra o contrato social e as exigências de qualificação técnica.
- Só entram licitações publicadas no PNCP.
- O painel depende da coleta do repositório `licitacoes-ti`. Se esse repositório mudar de nome ou dono, atualize `fonte_bruto`.
- O PNCP às vezes fica fora do ar ou devolve erro. Nesse caso o painel mostra "coleta parcial" ou "última coleta falhou" e mantém os dados anteriores daquela UF e modalidade.
- O GitHub pode desativar workflows agendados de repositórios sem atividade por 60 dias. Se o painel parar de atualizar, entre na aba Actions e reative.

## Rodar no computador (opcional)

Com Python 3.9 ou mais novo, sem instalar nada:

```
python3 painel.py --site site --offline      # painel a partir da coleta publicada, sem consultar itens
python3 tests/teste_classificacao.py         # testes de classificação
```

Para abrir o painel localmente: `cd site && python3 -m http.server` e acesse `http://localhost:8000`.
