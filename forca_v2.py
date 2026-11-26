"""
FORCA - jogo da forca com interface gráfica, loja de skins e progresso salvo
Instale a biblioteca uma vez:   pip install customtkinter
Rode no VSCode com:             python forca.py

Dá para jogar clicando nas letras ou digitando no teclado.
Seus pontos e compras ficam salvos em  ~/.forca_save.json
(para zerar o progresso, é só apagar esse arquivo).
"""

import json
import math
import random
import tkinter as tk
import unicodedata
from pathlib import Path

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0b1220"
CARD = "#16213a"
CARD_HOVER = "#1f3157"
ACCENT = "#38bdf8"
OK = "#22c55e"
ERRO = "#ef4444"
OURO = "#facc15"
TEXTO = "#e2e8f0"
MUTED = "#64748b"

SAVE_PATH = Path.home() / ".forca_save.json"

# ----------------------------------------------------------------- categorias
CATEGORIAS = {
    "⚽ Times de Futebol": [
        "Flamengo", "Palmeiras", "Corinthians", "São Paulo", "Santos", "Grêmio",
        "Internacional", "Cruzeiro", "Atlético Mineiro", "Botafogo", "Fluminense",
        "Vasco da Gama", "Bahia", "Fortaleza", "Real Madrid", "Barcelona",
        "Manchester United", "Liverpool", "Chelsea", "Arsenal", "Juventus", "Milan",
        "Inter de Milão", "Bayern de Munique", "Borussia Dortmund",
        "Paris Saint-Germain", "Benfica", "Porto", "Boca Juniors", "River Plate",
        "Ajax", "Atlético de Madrid", "Napoli", "Roma",
    ],
    "🌎 Países": [
        "Brasil", "Argentina", "Uruguai", "Paraguai", "Chile", "Colômbia", "Peru",
        "Venezuela", "Bolívia", "Equador", "México", "Canadá", "Estados Unidos",
        "Portugal", "Espanha", "França", "Alemanha", "Itália", "Inglaterra",
        "Holanda", "Bélgica", "Suíça", "Suécia", "Noruega", "Dinamarca", "Finlândia",
        "Polônia", "Croácia", "Grécia", "Turquia", "Rússia", "Ucrânia", "Egito",
        "Marrocos", "África do Sul", "Nigéria", "Japão", "China", "Índia",
        "Coreia do Sul", "Austrália", "Nova Zelândia", "Islândia", "Camboja",
        "Cazaquistão",
    ],
    "🐾 Animais": [
        "Elefante", "Girafa", "Crocodilo", "Ornitorrinco", "Tamanduá", "Capivara",
        "Papagaio", "Tartaruga", "Camaleão", "Golfinho", "Hipopótamo", "Rinoceronte",
        "Pinguim", "Jacaré", "Onça-pintada", "Lobo-guará", "Borboleta", "Escorpião",
        "Tubarão", "Canguru", "Flamingo", "Preguiça", "Tucano", "Arara", "Leopardo",
        "Orangotango", "Suricato", "Morcego",
    ],
    "🍓 Frutas": [
        "Abacaxi", "Morango", "Melancia", "Maracujá", "Jabuticaba", "Carambola",
        "Pitanga", "Goiaba", "Mamão", "Framboesa", "Tangerina", "Damasco", "Cupuaçu",
        "Graviola", "Acerola", "Romã", "Kiwi", "Pêssego", "Nectarina", "Lichia",
        "Caqui", "Amora", "Banana", "Laranja",
    ],
    "💼 Profissões": [
        "Engenheiro", "Advogado", "Enfermeiro", "Arquiteto", "Bombeiro", "Carpinteiro",
        "Jornalista", "Veterinário", "Programador", "Eletricista", "Fisioterapeuta",
        "Cozinheiro", "Professor", "Dentista", "Piloto", "Astronauta", "Pedreiro",
        "Farmacêutico", "Motorista", "Mecânico", "Padeiro", "Fotógrafo",
    ],
    "🚗 Marcas de Carro": [
        "Volkswagen", "Chevrolet", "Fiat", "Toyota", "Honda", "Hyundai", "Renault",
        "Peugeot", "Citroën", "Ford", "Nissan", "Mitsubishi", "Ferrari", "Lamborghini",
        "Porsche", "Mercedes-Benz", "Jeep", "Volvo", "Land Rover", "Tesla", "Mazda",
        "Kia", "Suzuki", "Bugatti",
    ],
    "🎬 Filmes": [
        "Titanic", "Avatar", "Gladiador", "Matrix", "Shrek", "Frozen", "Interestelar",
        "Coringa", "Batman", "Homem-Aranha", "Tropa de Elite", "Cidade de Deus",
        "Central do Brasil", "O Auto da Compadecida", "Parasita", "Toy Story",
        "Ratatouille", "Jurassic Park", "Vingadores", "Harry Potter", "Star Wars",
        "Rei Leão", "Procurando Nemo",
    ],
    "🎲 Mix Surpresa": None,  # sorteia de qualquer categoria
}

DIFICULDADES = {
    "Normal": {"erros": 6, "dica": True, "tempo": None, "mult": 1},
    "Difícil": {"erros": 5, "dica": False, "tempo": None, "mult": 2},
    "Insano": {"erros": 4, "dica": False, "tempo": 30, "mult": 3},
}

# ------------------------------------------------------------------- a loja
SKINS = {
    "classico": {"nome": "Clássico", "preco": 0, "cor": "#f1f5f9", "cabeca": "oval", "extra": None},
    "neon": {"nome": "Neon", "preco": 3000, "cor": "#22d3ee", "cabeca": "oval", "extra": None},
    "robo": {"nome": "Robô", "preco": 5000, "cor": "#94a3b8", "cabeca": "quadrada", "extra": "antena"},
    "ouro": {"nome": "Rei Dourado", "preco": 6000, "cor": OURO, "cabeca": "oval", "extra": "coroa"},
    "alien": {"nome": "Alienígena", "preco": 7000, "cor": "#4ade80", "cabeca": "oval", "extra": "antenas"},
    "ninja": {"nome": "Ninja", "preco": 8000, "cor": "#e5e7eb", "cabeca": "oval", "extra": "bandana"},
    "mago": {"nome": "Mago", "preco": 10000, "cor": "#c084fc", "cabeca": "oval", "extra": "chapeu"},
}

CENARIOS = {
    "classico": {"nome": "Noite Azul", "preco": 0, "bg": CARD, "forca": "#94a3b8"},
    "madeira": {"nome": "Madeira", "preco": 4000, "bg": "#1c1410", "forca": "#b45309"},
    "gelo": {"nome": "Gelo", "preco": 5000, "bg": "#0c1f33", "forca": "#7dd3fc"},
    "floresta": {"nome": "Floresta", "preco": 6000, "bg": "#0d1f14", "forca": "#84cc16"},
    "neon": {"nome": "Neon Rosa", "preco": 8000, "bg": "#0a0a1a", "forca": "#f0abfc"},
}

ITENS = {
    "dica": {"nome": "Dica Grátis", "preco": 1500, "icone": "🎁",
             "desc": "Revela uma letra sem perder vida. Funciona em qualquer dificuldade."},
    "coracao": {"nome": "Coração Extra", "preco": 2500, "icone": "❤",
                "desc": "Recupera 1 vida durante a partida."},
}

CATALOGOS = {"skins": SKINS, "cenarios": CENARIOS}
EQUIPADO = {"skins": "skin", "cenarios": "cenario"}


# ---------------------------------------------------------------- utilidades
def normalizar(texto):
    """Tira acentos e deixa maiúsculo (ç vira C, á vira A...)."""
    sem = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return sem.upper()


def eh_letra(ch):
    return normalizar(ch).isalpha()


def carregar_save():
    dados = {
        "pontos": 0, "melhor": 0,
        "skins": ["classico"], "skin": "classico",
        "cenarios": ["classico"], "cenario": "classico",
        "estoque": {"dica": 0, "coracao": 0},
    }
    try:
        lido = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        for chave in ("pontos", "melhor"):
            if isinstance(lido.get(chave), int):
                dados[chave] = max(0, lido[chave])
        dados["skins"] = list(dict.fromkeys(["classico"] + [s for s in lido.get("skins", []) if s in SKINS]))
        dados["cenarios"] = list(dict.fromkeys(["classico"] + [s for s in lido.get("cenarios", []) if s in CENARIOS]))
        if lido.get("skin") in dados["skins"]:
            dados["skin"] = lido["skin"]
        if lido.get("cenario") in dados["cenarios"]:
            dados["cenario"] = lido["cenario"]
        for chave in ("dica", "coracao"):
            valor = lido.get("estoque", {}).get(chave)
            if isinstance(valor, int):
                dados["estoque"][chave] = max(0, valor)
    except (OSError, ValueError, AttributeError):
        pass
    return dados


# ------------------------------------------------------------------- desenho
def _transforma(s, dx, dy):
    def P(*pts):
        return [v * s + (dx if i % 2 == 0 else dy) for i, v in enumerate(pts)]
    return P


def desenhar_forca(c, cenario, s=1.0, dx=0, dy=0):
    P = _transforma(s, dx, dy)
    cor = cenario["forca"]
    w = max(2, round(6 * s))
    c.create_line(*P(40, 310, 230, 310), width=w, fill=cor, capstyle="round")
    c.create_line(*P(80, 310, 80, 40), width=w, fill=cor, capstyle="round")
    c.create_line(*P(80, 40, 190, 40), width=w, fill=cor, capstyle="round")
    c.create_line(*P(190, 40, 190, 75), width=max(1, round(4 * s)), fill=cor, capstyle="round")


def desenhar_boneco(c, skin, partes, s=1.0, dx=0, dy=0, perdeu=False):
    P = _transforma(s, dx, dy)
    cor = skin["cor"]
    w = max(2, round(4 * s))
    cabeca = "rect" if skin["cabeca"] == "quadrada" else "oval"
    corpo = [
        (cabeca, (170, 75, 210, 115)),
        ("line", (190, 115, 190, 205)),
        ("line", (190, 140, 158, 178)),
        ("line", (190, 140, 222, 178)),
        ("line", (190, 205, 164, 262)),
        ("line", (190, 205, 216, 262)),
    ]
    for tipo, co in corpo[:partes]:
        if tipo == "oval":
            c.create_oval(*P(*co), outline=cor, width=w)
        elif tipo == "rect":
            c.create_rectangle(*P(*co), outline=cor, width=w)
        else:
            c.create_line(*P(*co), fill=cor, width=w, capstyle="round")

    if partes >= 1:
        extra = skin["extra"]
        w2 = max(1, round(2 * s))
        if extra == "coroa":
            c.create_polygon(*P(172, 77, 172, 60, 181, 68, 190, 56, 199, 68, 208, 60, 208, 77),
                             fill=OURO, outline="#a16207", width=w2)
        elif extra == "chapeu":
            c.create_polygon(*P(172, 77, 208, 77, 190, 44), fill="#7c3aed", outline="#c084fc", width=w2)
            c.create_line(*P(163, 77, 217, 77), fill="#c084fc", width=w, capstyle="round")
        elif extra == "bandana":
            c.create_rectangle(*P(170, 83, 210, 90), fill=ERRO, outline=ERRO)
            c.create_line(*P(210, 86, 224, 79), fill=ERRO, width=w)
            c.create_line(*P(210, 86, 224, 94), fill=ERRO, width=w)
        elif extra == "antena":
            c.create_line(*P(200, 75, 207, 62), fill=cor, width=w)
            c.create_oval(*P(203, 57, 211, 65), fill=ERRO, outline=ERRO)
        elif extra == "antenas":
            for xa, xb in ((182, 175), (198, 205)):
                c.create_line(*P(xa, 76, xb, 62), fill=cor, width=w)
                c.create_oval(*P(xb - 3, 58, xb + 3, 64), fill=cor, outline=cor)
        if perdeu:  # olhos em X
            for x in (182, 198):
                c.create_line(*P(x - 3, 88, x + 3, 94), fill=ERRO, width=w2)
                c.create_line(*P(x - 3, 94, x + 3, 88), fill=ERRO, width=w2)


# ------------------------------------------------------------------- aplicação
class Forca(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Forca")
        self.geometry("980x780")
        self.minsize(920, 740)
        self.configure(fg_color=BG)

        self.dados = carregar_save()
        self.dificuldade = ctk.StringVar(value="Normal")
        self.categoria = None
        self.config_jogo = DIFICULDADES["Normal"]
        self.sequencia = 0
        self.usadas = set()
        self.timer_id = None
        self.tela = None
        self.jogo_ativo = False
        self.aguardando_proxima = False
        self.botoes = {}

        self.bind("<Key>", self.tecla_fisica)
        self.mostrar_menu()

    # ------------------------------------------------------------- utilidades
    def salvar(self):
        try:
            SAVE_PATH.write_text(json.dumps(self.dados, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    def limpar(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        if self.tela:
            self.tela.destroy()
        self.tela = ctk.CTkFrame(self, fg_color="transparent")
        self.tela.pack(fill="both", expand=True, padx=24, pady=20)
        self.jogo_ativo = False
        self.aguardando_proxima = False

    def descricao(self):
        d = DIFICULDADES[self.dificuldade.get()]
        partes = [f"{d['erros']} erros permitidos"]
        partes.append("1 dica (custa uma vida)" if d["dica"] else "sem dicas")
        if d["tempo"]:
            partes.append(f"{d['tempo']}s por palavra")
        partes.append(f"pontos x{d['mult']}")
        return "  •  ".join(partes)

    # ------------------------------------------------------------------- menu
    def mostrar_menu(self):
        self.limpar()
        f = self.tela
        ctk.CTkLabel(f, text="FORCA", font=("Segoe UI", 56, "bold"), text_color=ACCENT).pack(pady=(10, 0))
        ctk.CTkLabel(f, text="Escolha a dificuldade e depois a categoria",
                     font=("Segoe UI", 16), text_color=MUTED).pack(pady=(0, 20))

        info = ctk.CTkLabel(f, text=self.descricao(), font=("Segoe UI", 14), text_color=TEXTO)

        def atualizar(_valor=None):
            info.configure(text=self.descricao())

        ctk.CTkSegmentedButton(
            f, values=list(DIFICULDADES), variable=self.dificuldade, command=atualizar,
            font=("Segoe UI", 16, "bold"), height=42,
        ).pack(pady=(0, 8))
        info.pack(pady=(0, 18))

        grade = ctk.CTkFrame(f, fg_color="transparent")
        grade.pack(pady=10)
        for i, nome in enumerate(CATEGORIAS):
            ctk.CTkButton(
                grade, text=nome, width=200, height=84, corner_radius=16,
                font=("Segoe UI", 17, "bold"), fg_color=CARD, hover_color=CARD_HOVER,
                command=lambda n=nome: self.iniciar(n),
            ).grid(row=i // 4, column=i % 4, padx=8, pady=8)

        ctk.CTkLabel(
            f, text=f"🪙 {self.dados['pontos']} pontos   •   Melhor sequência: {self.dados['melhor']}",
            font=("Segoe UI", 18, "bold"), text_color=OURO,
        ).pack(pady=(22, 8))
        ctk.CTkButton(
            f, text="🛒  Loja de skins e itens", width=280, height=48, corner_radius=14,
            font=("Segoe UI", 17, "bold"), fg_color="#f59e0b", hover_color="#d97706",
            text_color="black", command=self.mostrar_loja,
        ).pack()

    def iniciar(self, categoria):
        self.categoria = categoria
        self.config_jogo = DIFICULDADES[self.dificuldade.get()]
        self.nova_rodada()

    # ------------------------------------------------------------------- loja
    def mostrar_loja(self, aba="Skins"):
        self.limpar()
        f = self.tela
        topo = ctk.CTkFrame(f, fg_color="transparent")
        topo.pack(fill="x")
        ctk.CTkButton(topo, text="← Voltar", width=90, height=34, fg_color=CARD,
                      hover_color=CARD_HOVER, command=self.mostrar_menu).pack(side="left")
        ctk.CTkLabel(topo, text="🛒 LOJA", font=("Segoe UI", 30, "bold"),
                     text_color=ACCENT).pack(side="left", expand=True)
        ctk.CTkLabel(topo, text=f"🪙 {self.dados['pontos']}", font=("Segoe UI", 24, "bold"),
                     text_color=OURO).pack(side="right")

        tv = ctk.CTkTabview(f, fg_color=CARD, corner_radius=18)
        tv.pack(fill="both", expand=True, pady=(12, 0))
        for nome in ("Skins", "Cenários", "Itens"):
            tv.add(nome)
        self.montar_grade(tv.tab("Skins"), "skins", "Skins")
        self.montar_grade(tv.tab("Cenários"), "cenarios", "Cenários")
        self.montar_itens(tv.tab("Itens"))
        tv.set(aba)

    def _cartao(self, area, i):
        card = ctk.CTkFrame(area, fg_color=BG, corner_radius=16)
        card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="n")
        return card

    def montar_grade(self, pai, tipo, aba):
        area = ctk.CTkScrollableFrame(pai, fg_color="transparent")
        area.pack(fill="both", expand=True)
        area.grid_columnconfigure((0, 1, 2), weight=1)
        catalogo = CATALOGOS[tipo]
        for i, (chave, item) in enumerate(catalogo.items()):
            card = self._cartao(area, i)
            if tipo == "skins":
                cv = tk.Canvas(card, width=100, height=140, bg="#0f1a30", highlightthickness=0)
                cv.pack(padx=40, pady=(14, 6))
                desenhar_boneco(cv, item, 6, s=0.5, dx=-45, dy=-11)
            else:
                cv = tk.Canvas(card, width=100, height=140, bg=item["bg"], highlightthickness=0)
                cv.pack(padx=40, pady=(14, 6))
                desenhar_forca(cv, item, 0.4, -4, -4)
                desenhar_boneco(cv, SKINS[self.dados["skin"]], 6, 0.4, -4, -4)
            ctk.CTkLabel(card, text=item["nome"], font=("Segoe UI", 16, "bold"),
                         text_color=TEXTO).pack()

            tem = chave in self.dados[tipo]
            equipado = self.dados[EQUIPADO[tipo]] == chave
            if equipado:
                btn = ctk.CTkButton(card, text="✔ Equipado", width=170, height=36, state="disabled",
                                    fg_color=OK, text_color_disabled="white")
            elif tem:
                btn = ctk.CTkButton(card, text="Equipar", width=170, height=36,
                                    command=lambda t=tipo, c=chave: self.equipar(t, c, aba))
            else:
                pode = self.dados["pontos"] >= item["preco"]
                btn = ctk.CTkButton(card, text=f"Comprar  🪙 {item['preco']}", width=170, height=36,
                                    fg_color="#f59e0b" if pode else "#334155",
                                    hover_color="#d97706", text_color="black" if pode else "#94a3b8",
                                    text_color_disabled="#94a3b8",
                                    state="normal" if pode else "disabled",
                                    command=lambda t=tipo, c=chave: self.comprar(t, c, aba))
            btn.pack(pady=(8, 14), padx=14)

    def montar_itens(self, pai):
        area = ctk.CTkScrollableFrame(pai, fg_color="transparent")
        area.pack(fill="both", expand=True)
        area.grid_columnconfigure((0, 1, 2), weight=1)
        for i, (chave, item) in enumerate(ITENS.items()):
            card = self._cartao(area, i)
            ctk.CTkLabel(card, text=item["icone"], font=("Segoe UI", 48)).pack(padx=40, pady=(14, 0))
            ctk.CTkLabel(card, text=item["nome"], font=("Segoe UI", 16, "bold"),
                         text_color=TEXTO).pack()
            ctk.CTkLabel(card, text=item["desc"], font=("Segoe UI", 12), text_color=MUTED,
                         wraplength=190, justify="center").pack(padx=10, pady=4)
            ctk.CTkLabel(card, text=f"Você tem: {self.dados['estoque'][chave]}",
                         font=("Segoe UI", 13, "bold"), text_color=ACCENT).pack()
            pode = self.dados["pontos"] >= item["preco"]
            ctk.CTkButton(card, text=f"Comprar  🪙 {item['preco']}", width=170, height=36,
                          fg_color="#f59e0b" if pode else "#334155", hover_color="#d97706",
                          text_color="black" if pode else "#94a3b8", text_color_disabled="#94a3b8",
                          state="normal" if pode else "disabled",
                          command=lambda c=chave: self.comprar("itens", c, "Itens")).pack(pady=(8, 14), padx=14)

    def comprar(self, tipo, chave, aba):
        if tipo == "itens":
            preco = ITENS[chave]["preco"]
        else:
            preco = CATALOGOS[tipo][chave]["preco"]
        if self.dados["pontos"] < preco:
            return
        self.dados["pontos"] -= preco
        if tipo == "itens":
            self.dados["estoque"][chave] += 1
        else:
            self.dados[tipo].append(chave)
            self.dados[EQUIPADO[tipo]] = chave  # já equipa ao comprar
        self.salvar()
        self.mostrar_loja(aba)

    def equipar(self, tipo, chave, aba):
        self.dados[EQUIPADO[tipo]] = chave
        self.salvar()
        self.mostrar_loja(aba)

    # ------------------------------------------------------------------ rodada
    def nova_rodada(self):
        self.limpar()
        if CATEGORIAS[self.categoria] is None:
            pool = [(p, c) for c, lista in CATEGORIAS.items() if lista for p in lista]
        else:
            pool = [(p, self.categoria) for p in CATEGORIAS[self.categoria]]
        livres = [x for x in pool if x[0] not in self.usadas]
        if not livres:
            self.usadas -= {p for p, _ in pool}
            livres = pool
        self.palavra, self.cat_palavra = random.choice(livres)
        self.usadas.add(self.palavra)

        self.chutadas = set()
        self.erros = 0
        self.dica_usada = False
        self.jogo_ativo = True
        self.tempo_restante = self.config_jogo["tempo"]

        self.construir_tela_jogo()
        self.atualizar_placar()
        self.atualizar_botoes_itens()
        self.desenhar()
        self.atualizar_palavra()
        self.atualizar_info()
        if self.tempo_restante:
            self.timer_id = self.after(1000, self.tick)

    def construir_tela_jogo(self):
        f = self.tela
        topo = ctk.CTkFrame(f, fg_color="transparent")
        topo.pack(fill="x")
        ctk.CTkButton(topo, text="← Menu", width=90, height=34, fg_color=CARD,
                      hover_color=CARD_HOVER, command=self.mostrar_menu).pack(side="left")
        ctk.CTkLabel(topo, text=self.cat_palavra, font=("Segoe UI", 22, "bold"),
                     text_color=ACCENT).pack(side="left", expand=True)
        self.lbl_placar = ctk.CTkLabel(topo, text="", font=("Segoe UI", 14), text_color=MUTED)
        self.lbl_placar.pack(side="right")

        meio = ctk.CTkFrame(f, fg_color="transparent")
        meio.pack(fill="both", expand=True, pady=14)

        card = ctk.CTkFrame(meio, fg_color=CARD, corner_radius=18)
        card.pack(side="left", padx=(0, 14))
        self.canvas = tk.Canvas(card, width=300, height=330, bg=CARD, highlightthickness=0)
        self.canvas.pack(padx=14, pady=14)

        direita = ctk.CTkFrame(meio, fg_color=CARD, corner_radius=18)
        direita.pack(side="left", fill="both", expand=True)
        self.lbl_palavra = ctk.CTkLabel(direita, text="", font=("Consolas", 38, "bold"),
                                        text_color=TEXTO, wraplength=520, justify="center")
        self.lbl_palavra.pack(expand=True, padx=16, pady=(20, 6))
        self.lbl_info = ctk.CTkLabel(direita, text="", font=("Segoe UI", 20), text_color=TEXTO)
        self.lbl_info.pack(pady=4)
        self.lbl_status = ctk.CTkLabel(direita, text="", font=("Segoe UI", 18, "bold"))
        self.lbl_status.pack(pady=4)

        self.acoes = ctk.CTkFrame(direita, fg_color="transparent")
        self.acoes.pack(pady=(4, 18))
        self.btn_dica = self.btn_dica_gratis = self.btn_coracao = None
        if self.config_jogo["dica"]:
            self.btn_dica = ctk.CTkButton(self.acoes, text="💡 Dica (-1 vida)", width=150,
                                          height=38, command=self.dica)
            self.btn_dica.pack(side="left", padx=4)
        if self.dados["estoque"]["dica"] > 0:
            self.btn_dica_gratis = ctk.CTkButton(self.acoes, text="", width=150, height=38,
                                                 fg_color="#0d9488", hover_color="#0f766e",
                                                 command=self.usar_dica_gratis)
            self.btn_dica_gratis.pack(side="left", padx=4)
        if self.dados["estoque"]["coracao"] > 0:
            self.btn_coracao = ctk.CTkButton(self.acoes, text="", width=140, height=38,
                                             fg_color="#be123c", hover_color="#9f1239",
                                             command=self.usar_coracao)
            self.btn_coracao.pack(side="left", padx=4)

        teclado = ctk.CTkFrame(f, fg_color="transparent")
        teclado.pack(pady=(0, 4))
        self.botoes = {}
        for linha in ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"):
            row = ctk.CTkFrame(teclado, fg_color="transparent")
            row.pack(pady=3)
            for letra in linha:
                b = ctk.CTkButton(
                    row, text=letra, width=48, height=48, corner_radius=10,
                    font=("Segoe UI", 18, "bold"), fg_color="#243354", hover_color="#2f4470",
                    command=lambda x=letra: self.chutar(x),
                )
                b.pack(side="left", padx=3)
                self.botoes[letra] = b

    # ----------------------------------------------------------------- desenho
    def desenhar(self):
        c = self.canvas
        cenario = CENARIOS[self.dados["cenario"]]
        c.configure(bg=cenario["bg"])
        c.delete("all")
        perdeu = self.erros >= self.config_jogo["erros"]
        partes = min(6, math.ceil(self.erros * 6 / self.config_jogo["erros"]))
        desenhar_forca(c, cenario)
        desenhar_boneco(c, SKINS[self.dados["skin"]], partes, perdeu=perdeu)

    def texto_palavra(self, revelar=False):
        linhas = []
        for palavra in self.palavra.split(" "):
            letras = []
            for ch in palavra:
                if not eh_letra(ch):
                    letras.append(ch)
                elif revelar or normalizar(ch) in self.chutadas:
                    letras.append(ch.upper())
                else:
                    letras.append("_")
            linhas.append(" ".join(letras))
        sep = "\n" if len(self.palavra) > 13 else "     "
        return sep.join(linhas)

    def atualizar_palavra(self):
        self.lbl_palavra.configure(text=self.texto_palavra())

    def atualizar_info(self):
        restantes = self.config_jogo["erros"] - self.erros
        texto = "♥ " * restantes + "♡ " * self.erros
        if self.tempo_restante is not None:
            texto += f"     ⏱ {self.tempo_restante}s"
        self.lbl_info.configure(text=texto.strip(),
                                text_color=ERRO if restantes <= 1 else TEXTO)

    def atualizar_placar(self):
        self.lbl_placar.configure(
            text=f"🪙 {self.dados['pontos']}  •  Sequência {self.sequencia}  •  Recorde {self.dados['melhor']}")

    def atualizar_botoes_itens(self):
        if self.btn_dica_gratis:
            n = self.dados["estoque"]["dica"]
            self.btn_dica_gratis.configure(text=f"🎁 Dica grátis x{n}",
                                           state="normal" if n > 0 and self.jogo_ativo else "disabled")
        if self.btn_coracao:
            n = self.dados["estoque"]["coracao"]
            self.btn_coracao.configure(text=f"❤ Coração x{n}",
                                       state="normal" if n > 0 and self.jogo_ativo else "disabled")

    # ------------------------------------------------------------------ jogadas
    def tecla_fisica(self, evento):
        if self.aguardando_proxima and evento.keysym == "Return":
            self.nova_rodada()
            return
        if not self.jogo_ativo or not evento.char:
            return
        letra = evento.char.upper()
        if letra in self.botoes:
            self.chutar(letra)

    def letras_ocultas(self):
        return sorted({normalizar(ch) for ch in self.palavra
                       if eh_letra(ch) and normalizar(ch) not in self.chutadas})

    def revelar(self, letra):
        self.chutadas.add(letra)
        self.botoes[letra].configure(state="disabled", fg_color=ACCENT, text_color_disabled="black")

    def chutar(self, letra):
        if not self.jogo_ativo or letra in self.chutadas:
            return
        self.chutadas.add(letra)
        if letra in normalizar(self.palavra):
            self.botoes[letra].configure(state="disabled", fg_color=OK, text_color_disabled="white")
        else:
            self.erros += 1
            self.botoes[letra].configure(state="disabled", fg_color=ERRO, text_color_disabled="white")
        self.lbl_status.configure(text="")
        self.desenhar()
        self.atualizar_palavra()
        self.atualizar_info()
        self.verificar_fim()

    def dica(self):
        if not self.jogo_ativo or self.dica_usada:
            return
        if self.erros >= self.config_jogo["erros"] - 1:
            self.lbl_status.configure(text="Dica indisponível: é a sua última vida!", text_color=ERRO)
            return
        letra = random.choice(self.letras_ocultas())
        self.dica_usada = True
        self.btn_dica.configure(state="disabled")
        self.erros += 1
        self.revelar(letra)
        self.lbl_status.configure(text=f"Dica: a palavra tem a letra {letra}", text_color=ACCENT)
        self.desenhar()
        self.atualizar_palavra()
        self.atualizar_info()
        self.verificar_fim()

    def usar_dica_gratis(self):
        if not self.jogo_ativo or self.dados["estoque"]["dica"] <= 0:
            return
        ocultas = self.letras_ocultas()
        if not ocultas:
            return
        letra = random.choice(ocultas)
        self.dados["estoque"]["dica"] -= 1
        self.salvar()
        self.revelar(letra)
        self.lbl_status.configure(text=f"🎁 Dica grátis: a palavra tem a letra {letra}", text_color=ACCENT)
        self.atualizar_palavra()
        self.verificar_fim()
        self.atualizar_botoes_itens()

    def usar_coracao(self):
        if not self.jogo_ativo or self.dados["estoque"]["coracao"] <= 0:
            return
        if self.erros <= 0:
            self.lbl_status.configure(text="Você ainda está com todas as vidas!", text_color=MUTED)
            return
        self.dados["estoque"]["coracao"] -= 1
        self.salvar()
        self.erros -= 1
        self.lbl_status.configure(text="❤ Vida recuperada!", text_color=OK)
        self.desenhar()
        self.atualizar_info()
        self.atualizar_botoes_itens()

    def verificar_fim(self):
        letras = {normalizar(ch) for ch in self.palavra if eh_letra(ch)}
        if letras <= self.chutadas:
            self.finalizar(True)
        elif self.erros >= self.config_jogo["erros"]:
            self.finalizar(False)

    def tick(self):
        if not self.jogo_ativo:
            return
        self.tempo_restante -= 1
        self.atualizar_info()
        if self.tempo_restante <= 0:
            self.finalizar(False, "⏰ Tempo esgotado!")
            return
        self.timer_id = self.after(1000, self.tick)

    def finalizar(self, venceu, motivo=""):
        self.jogo_ativo = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        for b in self.botoes.values():
            b.configure(state="disabled")

        if venceu:
            self.sequencia += 1
            self.dados["melhor"] = max(self.dados["melhor"], self.sequencia)
            ganho = (100 + (self.config_jogo["erros"] - self.erros) * 30) * self.config_jogo["mult"]
            ganho += (self.sequencia - 1) * 25
            if self.tempo_restante:
                ganho += self.tempo_restante * 2
            self.dados["pontos"] += ganho
            self.lbl_palavra.configure(text=self.texto_palavra(revelar=True), text_color=OK)
            self.lbl_status.configure(text=f"🎉 Acertou! +{ganho} pontos", text_color=OK)
        else:
            self.sequencia = 0
            self.lbl_palavra.configure(text=self.texto_palavra(revelar=True), text_color=ERRO)
            self.lbl_status.configure(text=f"{motivo} Era: {self.palavra.upper()}".strip(),
                                      text_color=ERRO)
        self.salvar()
        self.atualizar_placar()
        self.desenhar()

        for b in (self.btn_dica, self.btn_dica_gratis, self.btn_coracao):
            if b:
                b.pack_forget()
        ctk.CTkButton(self.acoes, text="Próxima (Enter)", width=150, height=40,
                      command=self.nova_rodada).pack(side="left", padx=4)
        ctk.CTkButton(self.acoes, text="Categorias", width=110, height=40,
                      fg_color="#243354", hover_color="#2f4470",
                      command=self.mostrar_menu).pack(side="left", padx=4)
        ctk.CTkButton(self.acoes, text="🛒 Loja", width=100, height=40,
                      fg_color="#f59e0b", hover_color="#d97706", text_color="black",
                      command=self.mostrar_loja).pack(side="left", padx=4)
        self.aguardando_proxima = True


if __name__ == "__main__":
    Forca().mainloop()
