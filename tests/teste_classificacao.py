"""Confere se a classificação continua reconhecendo os casos básicos da Blue Belt.
Roda antes de cada coleta no GitHub Actions; se falhar, a coleta não acontece."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pncp import Classificador

cfg = json.loads((Path(__file__).resolve().parent.parent / "config.json").read_text(encoding="utf-8"))
c = Classificador(cfg)

MAT, ELE, MAN, ALI = "Material de consumo", "Material elétrico e construção", "Manutenção e obras", "Alimentação"

# (objeto, categoria esperada ou None para "qualquer uma")
DEVE_ENTRAR = [
    ("Registro de preços para aquisição de material de expediente para as secretarias municipais", MAT),
    ("Aquisição de material de limpeza e produtos de higiene para as unidades escolares", MAT),
    ("Aquisição de gêneros alimentícios para a merenda escolar", MAT),
    ("Fornecimento de água mineral em garrafões de 20 litros", MAT),
    ("Aquisição de EPIs (equipamentos de proteção individual) para os servidores da obra", MAT),
    ("Aquisição de uniformes profissionais para os agentes de limpeza urbana", MAT),
    ("Aquisição de toners e cartuchos para impressoras", MAT),
    ("Aquisição de copos descartáveis, café e açúcar para a copa", MAT),
    ("Aquisição de material elétrico para manutenção dos prédios públicos", ELE),
    ("Aquisição de lâmpadas LED e luminárias", ELE),
    ("Aquisição de material de construção e hidráulico", ELE),
    ("Prestação de serviços de manutenção predial preventiva e corretiva, com fornecimento de material e mão de obra", MAN),
    ("Contratação de empresa para manutenção preventiva e corretiva de aparelhos de ar condicionado tipo split", MAN),
    ("Serviços de limpeza e higienização de aparelhos de ar condicionado", MAN),
    ("Contratação de serviços de instalação elétrica e adequação do quadro de distribuição", MAN),
    ("Fornecimento e instalação de divisórias e forro de gesso acartonado", MAN),
    ("Serviços de pintura predial e pequenos reparos na sede", MAN),
    ("Manutenção da iluminação pública do município", MAN),
    ("Serviços de jardinagem e manutenção de áreas verdes", MAN),
    ("Manutenção de rede elétrica e iluminação pública", MAN),
    ("Fornecimento de refeições prontas (quentinhas) para os servidores", ALI),
    ("Contratação de serviço de coffee break para eventos da secretaria", ALI),
]

NAO_DEVE = [
    "Aquisição de medicamentos para a rede municipal de saúde",
    "Aquisição de material médico-hospitalar",
    "Contratação de serviços continuados de limpeza e conservação com dedicação exclusiva de mão de obra",
    "Aquisição de gêneros alimentícios da agricultura familiar para o PNAE - chamada pública",
    "Obras de pavimentação e drenagem no bairro",
    "Construção de creche municipal",
    "Aquisição de pneus para a frota municipal",
    "Aquisição de mobiliário escolar (mesas e cadeiras)",
    "Manutenção preventiva de elevadores",
    "Serviço de transporte escolar",
    "Aquisição de uniformes escolares para os alunos da rede",
    "Serviços de dedetização e desratização",
    "Aquisição de switches e servidores de rede",
    "Serviços de vigilância patrimonial armada",
    "Aquisição de ração para animais do canil",
    # falsos positivos vistos na primeira coleta real (23/10/2026)
    "Prestação de serviços de lavanderia, sob demanda, incluindo coleta e lavagem de uniformes e fardamentos",
    "Contratação de empresa para prestação de serviços de medicina e segurança do trabalho",
    "Contratação de empresa especializada na prestação de serviços de fornecimento e gerenciamento de auxílio-alimentação",
    "Aquisição de refrigerador vertical para armazenamento de gêneros alimentícios",
    "Registro de preços para aquisição de insumos e dispositivos médico-hospitalares descartáveis",
    "Contratação de empresa especializada na prestação de serviços de impressão monocromática, cópias, com fornecimento de papel A4 e toner",
]

# serviço fora do RJ não entra; material fora do RJ entra
POR_UF = [
    ("Manutenção predial preventiva e corretiva", "SP", False),
    ("Manutenção predial preventiva e corretiva", "RJ", True),
    ("Fornecimento de refeições prontas para servidores", "MG", False),
    ("Aquisição de material de limpeza", "ES", True),
    ("Aquisição e instalação de lâmpadas e material elétrico com manutenção elétrica", "SP", True),
    # serviço fora do RJ não pode entrar como material por citar ferramentas ou materiais
    ("Contratação de empresa especializada para execução da obra de reforma da UBS, com fornecimento de materiais, mão de obra e ferramentas", "MG", False),
    ("Contratação de empresa especializada para a prestação de serviços continuados de manutenção preventiva e corretiva em equipamentos de climatização (ar-condicionado), com ferramentas", "SP", False),
    ("Contratação de empresa especializada para prestação de serviços contínuos de nutrição e alimentação escolar, com fornecimento de gêneros alimentícios", "SP", False),
    ("Contratação de empresa para fornecimento de materiais de construção, com transporte incluso", "MG", True),
    ("Contratação de empresa especializada para manutenção predial preventiva e corretiva com fornecimento de materiais e ferramentas", "RJ", True),
]

falhas = 0
for txt, cat in DEVE_ENTRAR:
    r = c.classificar(txt)
    ok = r["relevante"] and (cat is None or cat in r["categorias"])
    falhas += not ok
    print(("OK   " if ok else "FALHA"), r["pontos"], r["categorias"], "|", txt[:80])
for txt in NAO_DEVE:
    r = c.classificar(txt)
    ok = not r["relevante"]
    falhas += not ok
    print(("OK   " if ok else "FALHA"), r["pontos"], r["termos"], r["vetos"], "|", txt[:80])
for txt, uf, esperado in POR_UF:
    r = c.classificar(txt, uf)
    ok = r["relevante"] == esperado
    falhas += not ok
    print(("OK   " if ok else "FALHA"), uf, r["categorias"], "|", txt[:80])
print("falhas:", falhas)
sys.exit(1 if falhas else 0)
