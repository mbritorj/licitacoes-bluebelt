# Robô de licitações (Blue Belt)

Consulta todo dia o PNCP (Portal Nacional de Contratações Públicas), separa as contratações com propostas em aberto que cabem nos CNAEs da Blue Belt Comércio e Serviço Ltda e publica um painel web com filtros.

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
- Roda no GitHub Actions às 06:45 (todo dia) e às 12:45 (dias úteis). Uma execução leva de 20 a 60 minutos, porque a API do PNCP limita a cerca de 12 chamadas por minuto. Na primeira execução o volume é grande; a leitura de itens fica limitada a 350 contratações por rodada (as que encerram antes) e o resto é completado nas rodadas seguintes.

## Instalação (uma vez, uns 15 minutos)

1. **Criar o repositório.** Em github.com, clique em **New repository**, dê um nome (ex.: `licitacoes-bluebelt`) e marque **Public**. No plano gratuito, o painel (GitHub Pages) só funciona em repositório público. O conteúdo são dados públicos de licitação.
2. **Enviar os arquivos.** Na página do repositório, clique em **uploading an existing file** e arraste todo o conteúdo desta pasta (incluindo a pasta `.github`). No Mac, a pasta `.github` fica oculta no Finder: use `Cmd + Shift + .` para mostrá-la. Clique em **Commit changes**.
3. **Dar permissão de escrita ao robô.** Settings > Actions > General > Workflow permissions > marque **Read and write permissions** > Save.
4. **Ativar o painel.** Settings > Pages > Source: **Deploy from a branch** > Branch: `main`, pasta `/docs` > Save. Em um ou dois minutos o endereço aparece no topo da página, no formato `https://SEU-USUARIO.github.io/licitacoes-bluebelt/`.
5. **Primeira execução.** Aba **Actions** > **Robô de licitações Blue Belt** > **Run workflow**. Quando terminar (ícone verde), abra o endereço do painel.

## Ajustes no dia a dia

Tudo fica em `config.json`, que dá para editar direto no site do GitHub (ícone de lápis):

- `ufs`: estados pesquisados.
- `ufs_por_categoria`: em quais estados cada categoria vale. Categoria que não aparece aqui vale em todos.
- `modalidades`: códigos do PNCP (4 concorrência eletrônica, 5 concorrência presencial, 6 pregão eletrônico, 7 pregão presencial, 8 dispensa, 12 credenciamento).
- `categorias`: termos de busca de cada tipo, com peso. Peso 3 basta para incluir a licitação; pesos 1 e 2 precisam somar com outro termo.
- `exclusoes`: termos que derrubam falsos positivos e objetos fora do CNAE.
- `alertas_por_categoria` e `alertas_por_termo`: avisos que aparecem no cartão de cada licitação.
- `max_consultas_itens`: quantas contratações têm os itens lidos por rodada.
- `valor_limite_me_epp`: valor até o qual a licitação é marcada como faixa de ME/EPP (R$ 80 mil, art. 48 da LC 123).

Se a Blue Belt incluir CNAEs novos no cartão CNPJ, acrescente os termos da atividade em `categorias` e retire o que estiver em `exclusoes`.

Depois de mexer nos termos, rode o workflow manualmente para ver o efeito. O teste em `tests/teste_classificacao.py` roda antes de cada coleta e para a execução se uma alteração fizer o robô deixar de reconhecer casos básicos (ou passar a aceitar "aquisição de medicamentos", por exemplo). Se você incluir um termo novo, vale acrescentar um exemplo lá também.

## Aba "Prefeituras pequenas RJ"

Lista os 26 municípios do RJ com até 20 mil habitantes, a plataforma em que cada um faz a disputa e como se cadastrar (levantamento de outubro de 2026). Esses municípios têm até abril de 2027 para publicar tudo em meio eletrônico, então parte das compras ainda não chega ao PNCP.

## Limitações

- A classificação olha o texto do objeto. Objeto genérico ("aquisição de materiais diversos") pode ficar de fora; objeto com termo usado em outro sentido pode entrar. Ajuste os termos conforme aparecerem casos.
- A compatibilidade com o CNAE é uma triagem. Antes de participar, confira o objeto do edital contra o contrato social e as exigências de qualificação técnica.
- Só entram licitações publicadas no PNCP.
- O PNCP às vezes fica fora do ar ou devolve erro. Nesse caso o painel mostra "coleta parcial" ou "última coleta falhou" e mantém os dados anteriores daquela UF e modalidade.
- O GitHub pode desativar workflows agendados de repositórios sem atividade por 60 dias. Se o painel parar de atualizar, entre na aba Actions e reative.

## Rodar no computador (opcional)

Com Python 3.9 ou mais novo, sem instalar nada:

```
python3 robo.py --max-paginas 2     # teste rápido
python3 robo.py                     # coleta completa
```

Para abrir o painel localmente: `cd docs && python3 -m http.server` e acesse `http://localhost:8000`.
