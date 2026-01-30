import random
# Fix import for standalone execution
try:
    from .database import SessionLocal, Question
except ImportError:
    from modules.database import SessionLocal, Question

def generate_questions():
    questions = []

    # --- FASE 1: FÁCIL (100 Perguntas) ---
    # Mix of fixed GK and generated Math

    # 1. Math (40 questions)
    for _ in range(40):
        a = random.randint(2, 20)
        b = random.randint(2, 20)
        op = random.choice(['+', '-'])
        if op == '+': ans = a + b
        else: ans = a - b

        # Generate distractors
        distractors = set()
        while len(distractors) < 3:
            d = ans + random.randint(-5, 5)
            if d != ans: distractors.add(str(d))

        questions.append({
            "question": f"Quanto é {a} {op} {b}?",
            "option_a": str(ans), "option_b": list(distractors)[0], "option_c": list(distractors)[1], "option_d": list(distractors)[2],
            "correct_option": str(ans), "phase": 1, "difficulty": "Fácil"
        })

    # 2. General Knowledge (60 questions)
    gk_easy = [
        ("Qual é a cor do céu em um dia limpo?", "Azul", "Verde", "Vermelho", "Amarelo"),
        ("Quantas pernas tem uma aranha?", "8", "6", "4", "10"),
        ("Qual é a capital do Brasil?", "Brasília", "Rio de Janeiro", "São Paulo", "Salvador"),
        ("Quem descobriu o Brasil?", "Pedro Álvares Cabral", "Cristóvão Colombo", "Dom Pedro I", "Vasco da Gama"),
        ("Qual é o animal mais rápido do mundo?", "Gueopardo", "Leão", "Cavalo", "Águia"),
        ("Quantos dias tem um ano bissexto?", "366", "365", "364", "360"),
        ("Qual é a cor da mistura de azul e amarelo?", "Verde", "Roxo", "Laranja", "Marrom"),
        ("O que as abelhas produzem?", "Mel", "Leite", "Seda", "Algodão"),
        ("Qual planeta é conhecido como Planeta Vermelho?", "Marte", "Júpiter", "Saturno", "Vênus"),
        ("Quem pintou a Mona Lisa?", "Leonardo da Vinci", "Pablo Picasso", "Van Gogh", "Michelangelo"),
        ("Qual é a moeda dos Estados Unidos?", "Dólar", "Euro", "Real", "Peso"),
        ("Quantos continentes existem?", "7", "5", "6", "8"),
        ("Qual fruta cai do coqueiro?", "Coco", "Banana", "Maçã", "Abacaxi"),
        ("Qual é o maior animal do oceano?", "Baleia Azul", "Tubarão Branco", "Lula Gigante", "Orca"),
        ("Quem é o parceiro do Batman?", "Robin", "Coringa", "Super-Homem", "Flash"),
        ("Em que país fica a Torre Eiffel?", "França", "Itália", "Espanha", "Inglaterra"),
        ("Qual é o estado físico da água no gelo?", "Sólido", "Líquido", "Gasoso", "Plasma"),
        ("Quantos segundos tem um minuto?", "60", "100", "30", "50"),
        ("Onde o sol nasce?", "Leste", "Oeste", "Norte", "Sul"),
        ("Qual é o nome do Mickey Mouse no Brasil?", "Mickey", "Rato", "Camundongo", "Jerry"),
        ("Qual instrumento tem teclas brancas e pretas?", "Piano", "Violão", "Flauta", "Bateria"),
        ("Qual é a língua oficial do Brasil?", "Português", "Espanhol", "Inglês", "Italiano"),
        ("O que é H2O?", "Água", "Sal", "Ar", "Fogo"),
        ("Quantos jogadores tem um time de futebol em campo?", "11", "10", "12", "9"),
        ("Qual é o satélite natural da Terra?", "Lua", "Sol", "Marte", "Estrela"),
        ("Qual mês vem depois de abril?", "Maio", "Junho", "Março", "Julho"),
        ("Quem escreveu o Sítio do Picapau Amarelo?", "Monteiro Lobato", "Machado de Assis", "Ziraldo", "Mauricio de Sousa"),
        ("Qual é o rei da selva?", "Leão", "Tigre", "Elefante", "Macaco"),
        ("O que usamos para ver as horas?", "Relógio", "Bússola", "Termômetro", "Régua"),
        ("Qual é o maior país da América do Sul?", "Brasil", "Argentina", "Chile", "Colômbia"),
        ("Qual personagem come espinafre para ficar forte?", "Popeye", "Hulk", "Super-Homem", "Goku"),
        ("Qual é a cor do cavalo branco de Napoleão?", "Branco", "Preto", "Marrom", "Cinza"),
        ("Onde fica o Cristo Redentor?", "Rio de Janeiro", "São Paulo", "Bahia", "Minas Gerais"),
        ("Qual é o oposto de dia?", "Noite", "Tarde", "Manhã", "Madrugada"),
        ("Quantos dedos temos em uma mão?", "5", "4", "6", "10"),
        ("O que a vaca produz?", "Leite", "Suco", "Refrigerante", "Água"),
        ("Qual é a capital da França?", "Paris", "Londres", "Roma", "Berlim"),
        ("Quem vive no Abacaxi no fundo do mar?", "Bob Esponja", "Patrick", "Lula Molusco", "Sandy"),
        ("Qual é o formato da bola de futebol?", "Esfera", "Cubo", "Quadrado", "Triângulo"),
        ("Qual animal tem tromba?", "Elefante", "Girafa", "Rinoceronte", "Hipopótamo"),
        ("O que usamos para cortar papel?", "Tesoura", "Colher", "Garfo", "Martelo"),
        ("Qual é a estação das flores?", "Primavera", "Verão", "Outono", "Inverno"),
        ("Quem é a namorada do Mickey?", "Minnie", "Margarida", "Clarabela", "Cinderela"),
        ("Qual é o país do sushi?", "Japão", "China", "Coreia", "Tailândia"),
        ("O que o bombeiro apaga?", "Fogo", "Luz", "Água", "Vento"),
        ("Qual é o nome do nosso planeta?", "Terra", "Marte", "Júpiter", "Saturno"),
        ("Quantas rodas tem uma bicicleta?", "2", "4", "3", "1"),
        ("Qual é a cor da banana madura?", "Amarela", "Verde", "Vermelha", "Azul"),
        ("Onde vivem os pinguins?", "Polo Sul", "Polo Norte", "Deserto", "Floresta"),
        ("Qual é o nome do boneco de madeira que mentia?", "Pinóquio", "Gepeto", "Chaves", "Pica-Pau"),
        ("Quem nasce no Brasil é?", "Brasileiro", "Português", "Americano", "Espanhol"),
        ("O que usamos para escrever no quadro negro?", "Giz", "Caneta", "Lápis", "Pincel"),
        ("Qual animal mia?", "Gato", "Cachorro", "Pássaro", "Peixe"),
        ("Qual é o primeiro mês do ano?", "Janeiro", "Fevereiro", "Março", "Dezembro"),
        ("Quantas cores tem o arco-íris?", "7", "5", "10", "3"),
        ("O que usamos para ouvir música?", "Ouvido", "Nariz", "Boca", "Olho"),
        ("Qual é o herói que sobe pelas paredes?", "Homem-Aranha", "Batman", "Flash", "Hulk"),
        ("O que sai da chaminé?", "Fumaça", "Água", "Fogo", "Terra"),
        ("Qual é o alimento favorito do coelho?", "Cenoura", "Batata", "Milho", "Alface"),
        ("Quem 'descobriu' a América?", "Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Marco Polo")
    ]

    for q, ans, d1, d2, d3 in gk_easy:
        questions.append({
            "question": q,
            "option_a": ans, "option_b": d1, "option_c": d2, "option_d": d3,
            "correct_option": ans, "phase": 1, "difficulty": "Fácil"
        })

    # --- FASE 2: MÉDIO (100 Perguntas) ---

    # 1. Math (30 questions)
    for _ in range(30):
        a = random.randint(5, 12)
        b = random.randint(5, 12)
        ans = a * b
        distractors = set()
        while len(distractors) < 3:
            d = ans + random.randint(-10, 10)
            if d != ans and d > 0: distractors.add(str(d))
        questions.append({
            "question": f"Quanto é {a} x {b}?",
            "option_a": str(ans), "option_b": list(distractors)[0], "option_c": list(distractors)[1], "option_d": list(distractors)[2],
            "correct_option": str(ans), "phase": 2, "difficulty": "Médio"
        })

    # 2. General Knowledge (70 questions)
    gk_medium = [
        ("Qual é o maior planeta do Sistema Solar?", "Júpiter", "Saturno", "Terra", "Urano"),
        ("Quem escreveu 'Dom Casmurro'?", "Machado de Assis", "José de Alencar", "Jorge Amado", "Clarice Lispector"),
        ("Qual é o elemento químico com símbolo O?", "Oxigênio", "Ouro", "Ósmio", "Prata"),
        ("Em que continente fica o Egito?", "África", "Ásia", "Europa", "América"),
        ("Quantos anos durou a Guerra dos 100 Anos?", "116", "100", "99", "120"),
        ("Qual é a capital da Argentina?", "Buenos Aires", "Santiago", "Lima", "Montevidéu"),
        ("Quem pintou 'A Última Ceia'?", "Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"),
        ("Qual é o maior oceano do mundo?", "Pacífico", "Atlântico", "Índico", "Ártico"),
        ("Quantos ossos tem o corpo humano adulto?", "206", "200", "210", "198"),
        ("Qual é a moeda do Reino Unido?", "Libra Esterlina", "Euro", "Dólar", "Franco"),
        ("Quem foi o primeiro homem a pisar na Lua?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"),
        ("Qual é a fórmula da água?", "H2O", "CO2", "O2", "H2O2"),
        ("Qual país tem o formato de uma bota?", "Itália", "Portugal", "Espanha", "Grécia"),
        ("Quem inventou o telefone?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Santos Dumont"),
        ("Qual é o rio mais extenso do mundo?", "Amazonas", "Nilo", "Yangtze", "Mississipi"),
        ("Qual é a capital da Rússia?", "Moscou", "São Petersburgo", "Kiev", "Varsóvia"),
        ("Quem foi o deus grego dos mares?", "Poseidon", "Zeus", "Hades", "Ares"),
        ("Qual é o país mais populoso do mundo?", "Índia", "China", "EUA", "Indonésia"),
        ("Qual instrumento mede a temperatura?", "Termômetro", "Barômetro", "Higrômetro", "Anemômetro"),
        ("Quem escreveu 'Romeu e Julieta'?", "William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"),
        ("Qual é a velocidade da luz?", "300.000 km/s", "150.000 km/s", "1.000 km/s", "3.000 km/s"),
        ("Qual é o maior deserto do mundo?", "Antártida", "Saara", "Gobi", "Kalahari"),
        ("Quem proclamou a independência do Brasil?", "Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"),
        ("Qual é a capital do Japão?", "Tóquio", "Pequim", "Seul", "Bangkok"),
        ("O que é um animal onívoro?", "Come plantas e carne", "Come só carne", "Come só plantas", "Come insetos"),
        ("Qual é o símbolo do Ouro na tabela periódica?", "Au", "Ag", "Fe", "Cu"),
        ("Quem foi o primeiro presidente dos EUA?", "George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"),
        ("Qual é a montanha mais alta do mundo?", "Monte Everest", "K2", "Kangchenjunga", "Makalu"),
        ("Qual é o gás mais abundante na atmosfera?", "Nitrogênio", "Oxigênio", "Argônio", "Carbono"),
        ("Quem pintou 'O Grito'?", "Edvard Munch", "Van Gogh", "Picasso", "Dali"),
        ("Qual é a capital da Alemanha?", "Berlim", "Munique", "Frankfurt", "Hamburgo"),
        ("Quantos lados tem um hexágono?", "6", "5", "7", "8"),
        ("Qual é o planeta mais próximo do Sol?", "Mercúrio", "Vênus", "Terra", "Marte"),
        ("Quem escreveu 'Harry Potter'?", "J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "Stephen King"),
        ("Qual é a capital da Austrália?", "Camberra", "Sydney", "Melbourne", "Perth"),
        ("O que significa a sigla ONU?", "Organização das Nações Unidas", "Onde Nós Unimos", "Organização Nacional Unida", "Ordem Natural Universal"),
        ("Qual é o mamífero que voa?", "Morcego", "Esquilo voador", "Pinguim", "Avestruz"),
        ("Quem descobriu a gravidade?", "Isaac Newton", "Albert Einstein", "Galileu Galilei", "Copérnico"),
        ("Qual é a capital da Espanha?", "Madri", "Barcelona", "Valência", "Sevilha"),
        ("O que estuda a botânica?", "Plantas", "Animais", "Rochas", "Estrelas"),
        ("Qual é o menor país do mundo?", "Vaticano", "Mônaco", "Nauru", "San Marino"),
        ("Quem foi Ayrton Senna?", "Piloto de F1", "Jogador de Futebol", "Ator", "Cantor"),
        ("Qual é a capital do Canadá?", "Ottawa", "Toronto", "Vancouver", "Montreal"),
        ("Quantos graus tem um ângulo reto?", "90", "45", "180", "360"),
        ("Quem é o rei do pop?", "Michael Jackson", "Elvis Presley", "Prince", "Madonna"),
        ("Qual é o maior órgão do corpo humano?", "Pele", "Fígado", "Coração", "Pulmão"),
        ("O que é a Via Láctea?", "Uma galáxia", "Um planeta", "Uma estrela", "Um cometa"),
        ("Qual é a capital da Itália?", "Roma", "Milão", "Veneza", "Florença"),
        ("Quem inventou o avião?", "Santos Dumont", "Irmãos Wright", "Da Vinci", "Edison"),
        ("Qual é o metal líquido à temperatura ambiente?", "Mercúrio", "Gálio", "Ferro", "Chumbo"),
        ("Qual é a capital da China?", "Pequim", "Xangai", "Hong Kong", "Macau"),
        ("Quem pintou 'Guernica'?", "Pablo Picasso", "Salvador Dalí", "Miro", "Goya"),
        ("Qual é o livro mais vendido do mundo?", "Bíblia", "Dom Quixote", "Harry Potter", "O Pequeno Príncipe"),
        ("Qual é a capital do Egito?", "Cairo", "Alexandria", "Luxor", "Giza"),
        ("O que é clorofila?", "Pigmento das plantas", "Um remédio", "Um gás", "Uma rocha"),
        ("Quem foi Gandhi?", "Líder indiano", "Presidente dos EUA", "Rei da Inglaterra", "Filósofo grego"),
        ("Qual é a capital do México?", "Cidade do México", "Cancún", "Guadalajara", "Monterrey"),
        ("Quantas cordas tem um violão padrão?", "6", "4", "5", "7"),
        ("Quem escreveu 'O Pequeno Príncipe'?", "Antoine de Saint-Exupéry", "Victor Hugo", "Jules Verne", "Voltaire"),
        ("Qual é a capital de Portugal?", "Lisboa", "Porto", "Coimbra", "Faro"),
        ("O que é um tsunami?", "Onda gigante", "Terremoto", "Furacão", "Vulcão"),
        ("Quem foi Nelson Mandela?", "Líder sul-africano", "Presidente do Brasil", "Cantor de Jazz", "Ator"),
        ("Qual é a capital da Coreia do Sul?", "Seul", "Pyongyang", "Busan", "Incheon"),
        ("Qual é o animal símbolo da WWF?", "Panda", "Leão", "Tigre", "Urso Polar"),
        ("Quem é o autor de 'O Senhor dos Anéis'?", "J.R.R. Tolkien", "C.S. Lewis", "George R.R. Martin", "J.K. Rowling"),
        ("Qual é a capital da Turquia?", "Ancara", "Istambul", "Izmir", "Antalya"),
        ("O que é a internet?", "Rede de computadores", "Um satélite", "Um programa", "Um jogo"),
        ("Quem foi Cleópatra?", "Rainha do Egito", "Rainha da Inglaterra", "Deusa Grega", "Atriz"),
        ("Qual é a capital da Índia?", "Nova Delhi", "Mumbai", "Calcutá", "Bangalore"),
        ("O que é o PIB?", "Produto Interno Bruto", "Produto Internacional Bruto", "Preço Interno Base", "Plano Interno Básico")
    ]

    for q, ans, d1, d2, d3 in gk_medium:
        questions.append({
            "question": q,
            "option_a": ans, "option_b": d1, "option_c": d2, "option_d": d3,
            "correct_option": ans, "phase": 2, "difficulty": "Médio"
        })

    # --- FASE 3: DIFÍCIL (100 Perguntas) ---

    # 1. Math (20 questions) - Powers and simple roots
    for _ in range(20):
        base = random.randint(2, 9)
        exp = 3
        ans = base ** exp
        distractors = set()
        while len(distractors) < 3:
            d = ans + random.randint(-50, 50)
            if d != ans and d > 0: distractors.add(str(d))
        questions.append({
            "question": f"Quanto é {base} elevado ao cubo ({base}^3)?",
            "option_a": str(ans), "option_b": list(distractors)[0], "option_c": list(distractors)[1], "option_d": list(distractors)[2],
            "correct_option": str(ans), "phase": 3, "difficulty": "Difícil"
        })

    # 2. General Knowledge (80 questions)
    gk_hard = [
        ("Qual é o elemento mais abundante no universo?", "Hidrogênio", "Hélio", "Oxigênio", "Carbono"),
        ("Em que ano caiu o Muro de Berlim?", "1989", "1991", "1985", "1990"),
        ("Quem formulou a Teoria da Relatividade?", "Albert Einstein", "Isaac Newton", "Niels Bohr", "Stephen Hawking"),
        ("Qual é a capital da Nova Zelândia?", "Wellington", "Auckland", "Christchurch", "Hamilton"),
        ("Qual guerra durou de 1939 a 1945?", "Segunda Guerra Mundial", "Primeira Guerra Mundial", "Guerra do Vietnã", "Guerra Fria"),
        ("Quem escreveu 'A Divina Comédia'?", "Dante Alighieri", "Virgílio", "Homero", "Bocaccio"),
        ("Qual é o maior órgão interno do corpo humano?", "Fígado", "Coração", "Pulmão", "Estômago"),
        ("Qual é a capital da Suíça?", "Berna", "Zurique", "Genebra", "Basileia"),
        ("Quem pintou 'A Noite Estrelada'?", "Vincent van Gogh", "Claude Monet", "Salvador Dalí", "Rembrandt"),
        ("Qual é o pH da água pura?", "7", "0", "14", "5"),
        ("Em que ano o homem chegou à Lua?", "1969", "1965", "1972", "1959"),
        ("Qual é a capital da Nigéria?", "Abuja", "Lagos", "Kano", "Ibadan"),
        ("Quem descobriu a Penicilina?", "Alexander Fleming", "Louis Pasteur", "Marie Curie", "Robert Koch"),
        ("Qual é o menor osso do corpo humano?", "Estribo", "Martelo", "Bigorna", "Fêmur"),
        ("Quem foi o primeiro imperador romano?", "Augusto", "Júlio César", "Nero", "Calígula"),
        ("Qual é a capital da Polônia?", "Varsóvia", "Cracóvia", "Gdansk", "Poznan"),
        ("O que é a mitocôndria?", "Usina de energia da célula", "Núcleo da célula", "Parede celular", "DNA"),
        ("Quem escreveu 'Os Lusíadas'?", "Luís de Camões", "Fernando Pessoa", "Gil Vicente", "Eça de Queirós"),
        ("Qual é a capital da Noruega?", "Oslo", "Estocolmo", "Copenhague", "Helsinque"),
        ("Quem foi o líder da Revolução Russa de 1917?", "Lenin", "Stalin", "Trotsky", "Gorbachev"),
        ("Qual é o metal mais denso?", "Ósmio", "Chumbo", "Ouro", "Mercúrio"),
        ("Em que país nasceu o tango?", "Argentina", "Espanha", "Brasil", "Uruguai"),
        ("Qual é a capital do Irã?", "Teerã", "Bagdá", "Cabul", "Damasco"),
        ("Quem compôs a 'Nona Sinfonia'?", "Beethoven", "Mozart", "Bach", "Chopin"),
        ("Qual é a partícula subatômica com carga negativa?", "Elétron", "Próton", "Nêutron", "Fóton"),
        ("Quem foi o pai da Psicanálise?", "Sigmund Freud", "Carl Jung", "Jean Piaget", "Skinner"),
        ("Qual é a capital da Finlândia?", "Helsinque", "Oslo", "Estocolmo", "Tallinn"),
        ("O que é um número primo?", "Divisível apenas por 1 e ele mesmo", "Divisível por 2", "Número ímpar", "Número infinito"),
        ("Quem pintou a Capela Sistina?", "Michelangelo", "Leonardo da Vinci", "Rafael", "Botticelli"),
        ("Qual é a capital do Chile?", "Santiago", "Valparaíso", "Concepción", "La Serena"),
        ("Em que ano ocorreu a Revolução Francesa?", "1789", "1776", "1804", "1815"),
        ("Qual é o rio mais longo da Europa?", "Volga", "Danúbio", "Reno", "Sena"),
        ("Quem escreveu '1984'?", "George Orwell", "Aldous Huxley", "Ray Bradbury", "Isaac Asimov"),
        ("Qual é a capital da Tailândia?", "Bangkok", "Phuket", "Chiang Mai", "Pattaya"),
        ("O que é a OTAN?", "Aliança militar", "Acordo comercial", "Organização de saúde", "Banco mundial"),
        ("Quem descobriu o rádio (elemento)?", "Marie Curie", "Einstein", "Newton", "Darwin"),
        ("Qual é a capital da Arábia Saudita?", "Riad", "Jeddah", "Mecca", "Medina"),
        ("Quem escreveu 'A Metamorfose'?", "Franz Kafka", "Friedrich Nietzsche", "Thomas Mann", "Hermann Hesse"),
        ("Qual é a camada mais externa da Terra?", "Crosta", "Manto", "Núcleo", "Atmosfera"),
        ("Quem foi o primeiro presidente do Brasil?", "Deodoro da Fonseca", "Floriano Peixoto", "Getúlio Vargas", "Dom Pedro II"),
        ("Qual é a capital da Indonésia?", "Jacarta", "Bali", "Surabaya", "Bandung"),
        ("O que é a entropia?", "Medida de desordem", "Energia total", "Força da gravidade", "Velocidade da luz"),
        ("Quem pintou 'As Meninas'?", "Velázquez", "Goya", "El Greco", "Dalí"),
        ("Qual é a capital da Bélgica?", "Bruxelas", "Antuérpia", "Ghent", "Bruges"),
        ("Em que ano acabou a Primeira Guerra Mundial?", "1918", "1914", "1920", "1919"),
        ("Quem escreveu 'Cem Anos de Solidão'?", "Gabriel García Márquez", "Jorge Luis Borges", "Pablo Neruda", "Isabel Allende"),
        ("Qual é a capital da Hungria?", "Budapeste", "Viena", "Praga", "Bratislava"),
        ("O que é o DNA?", "Ácido Desoxirribonucleico", "Ácido Ribonucleico", "Proteína", "Enzima"),
        ("Quem foi Joana d'Arc?", "Heroína francesa", "Rainha da Inglaterra", "Santa italiana", "Bruxa"),
        ("Qual é a capital do Paquistão?", "Islamabad", "Karachi", "Lahore", "Peshawar"),
        ("Qual é o valor de Pi (aproximado)?", "3,1415", "3,1514", "3,1416", "3,1410"),
        ("Quem compôs 'As Quatro Estações'?", "Vivaldi", "Bach", "Mozart", "Handel"),
        ("Qual é a capital da Ucrânia?", "Kiev", "Lviv", "Odessa", "Kharkiv"),
        ("O que é a Aurora Boreal?", "Fenômeno luminoso", "Estrela cadente", "Explosão solar", "Cometa"),
        ("Quem escreveu 'Crime e Castigo'?", "Dostoiévski", "Tolstói", "Tchekhov", "Gogol"),
        ("Qual é a capital da Colômbia?", "Bogotá", "Medellín", "Cali", "Cartagena"),
        ("O que é um buraco negro?", "Região de gravidade intensa", "Estrela apagada", "Planeta escuro", "Vazio no espaço"),
        ("Quem foi Martin Luther King Jr.?", "Ativista dos direitos civis", "Presidente dos EUA", "Cantor de Jazz", "Atleta"),
        ("Qual é a capital das Filipinas?", "Manila", "Cebu", "Davao", "Quezon"),
        ("O que é a fotossíntese?", "Processo de energia das plantas", "Respiração das plantas", "Reprodução das plantas", "Morte das plantas"),
        ("Quem pintou 'O Nascimento de Vênus'?", "Botticelli", "Da Vinci", "Michelangelo", "Rafael"),
        ("Qual é a capital da Malásia?", "Kuala Lumpur", "George Town", "Ipoh", "Johor Bahru"),
        ("Em que ano o Titanic afundou?", "1912", "1905", "1920", "1898"),
        ("Quem escreveu 'O Grande Gatsby'?", "F. Scott Fitzgerald", "Hemingway", "Faulkner", "Steinbeck"),
        ("Qual é a capital do Vietnã?", "Hanói", "Ho Chi Minh", "Da Nang", "Hué"),
        ("O que é a tabela periódica?", "Organização dos elementos químicos", "Lista de países", "Calendário lunar", "Mapa estelar"),
        ("Quem foi Copérnico?", "Astrônomo polonês", "Filósofo grego", "Pintor italiano", "Rei francês"),
        ("Qual é a capital de Israel?", "Jerusalém", "Tel Aviv", "Haifa", "Eilat"),
        ("O que é um algoritmo?", "Sequência de instruções", "Um robô", "Um vírus", "Um computador"),
        ("Quem compôs 'O Lago dos Cisnes'?", "Tchaikovsky", "Stravinsky", "Prokofiev", "Rachmaninoff"),
        ("Qual é a capital da Áustria?", "Viena", "Salzburgo", "Graz", "Innsbruck"),
        ("O que é a bolsa de valores?", "Mercado de ações", "Loja de bolsas", "Banco central", "Feira de rua"),
        ("Quem foi Alexandre, o Grande?", "Rei da Macedônia", "Imperador Romano", "Faraó do Egito", "Rei Persa"),
        ("Qual é a capital da Suécia?", "Estocolmo", "Gotemburgo", "Malmo", "Uppsala"),
        ("O que é um isótopo?", "Átomo com mesmo nº de prótons", "Átomo com carga positiva", "Molécula instável", "Tipo de rocha"),
        ("Quem escreveu 'Ulisses'?", "James Joyce", "Virginia Woolf", "Beckett", "Yeats"),
        ("Qual é a capital da Dinamarca?", "Copenhague", "Aarhus", "Odense", "Aalborg"),
        ("O que é a ONU?", "Organização das Nações Unidas", "Ordem das Nações Unidas", "Organização Nacional Unida", "Onde Nós Unimos"),
        ("Quem foi Tesla?", "Inventor e engenheiro", "Fundador da Ford", "Criador do rádio", "Presidente americano"),
        ("Qual é a capital do Quênia?", "Nairobi", "Mombasa", "Kisumu", "Nakuru")
    ]

    for q, ans, d1, d2, d3 in gk_hard:
        questions.append({
            "question": q,
            "option_a": ans, "option_b": d1, "option_c": d2, "option_d": d3,
            "correct_option": ans, "phase": 3, "difficulty": "Difícil"
        })

    # --- FASE 4: MUITO DIFÍCIL (100 Perguntas) ---
    # Complex trivia, specific dates, obscure facts

    gk_very_hard = [
        ("Qual a capital do Cazaquistão (atual)?", "Astana", "Almaty", "Nur-Sultan", "Tashkent"),
        ("Quem descobriu a estrutura do DNA?", "Watson e Crick", "Darwin e Wallace", "Pasteur e Koch", "Franklin e Wilkins"),
        ("Em que ano foi assinada a Magna Carta?", "1215", "1492", "1066", "1776"),
        ("Qual é o ponto mais profundo dos oceanos?", "Fossa das Marianas", "Fossa de Tonga", "Fossa de Porto Rico", "Fossa de Java"),
        ("Quem escreveu 'Em Busca do Tempo Perdido'?", "Marcel Proust", "Balzac", "Flaubert", "Zola"),
        ("Qual é o elemento químico com número atômico 100?", "Férmio", "Einstênio", "Mendelévio", "Nobélio"),
        ("Qual guerra foi encerrada pelo Tratado de Versalhes?", "Primeira Guerra Mundial", "Segunda Guerra Mundial", "Guerra Franco-Prussiana", "Guerra dos 30 Anos"),
        ("Quem compôs a ópera 'O Anel do Nibelungo'?", "Richard Wagner", "Verdi", "Puccini", "Rossini"),
        ("Qual é a capital de Burkina Faso?", "Ouagadougou", "Bamako", "Niamey", "Dakar"),
        ("Qual físico propôs o Princípio da Incerteza?", "Heisenberg", "Schrödinger", "Planck", "Bohr"),
        ("Em que ano Constantino legalizou o cristianismo?", "313", "476", "800", "1054"),
        ("Quem pintou 'O Jardim das Delícias Terrenas'?", "Hieronymus Bosch", "Bruegel", "Van Eyck", "Dürer"),
        ("Qual é a montanha mais alta da África?", "Kilimanjaro", "Monte Quênia", "Atlas", "Ruwenzori"),
        ("Quem escreveu 'O Paraíso Perdido'?", "John Milton", "Dante", "Chaucer", "Blake"),
        ("Qual é a capital do Liechtenstein?", "Vaduz", "Schaan", "Triesen", "Balzers"),
        ("O que é a Conjectura de Poincaré?", "Teorema de topologia", "Lei da física", "Problema de xadrez", "Fórmula química"),
        ("Quem foi o último czar da Rússia?", "Nicolau II", "Alexandre III", "Pedro, o Grande", "Ivan, o Terrível"),
        ("Qual é o lago mais profundo do mundo?", "Lago Baikal", "Lago Superior", "Lago Vitória", "Mar Cáspio"),
        ("Quem descobriu os raios X?", "Röntgen", "Curie", "Becquerel", "Rutherford"),
        ("Qual é a capital do Butão?", "Thimphu", "Paro", "Punakha", "Jakar"),
        ("Quem escreveu 'Fausto'?", "Goethe", "Schiller", "Kafka", "Mann"),
        ("Qual é a estrela mais próxima do Sol?", "Próxima Centauri", "Sirius", "Alpha Centauri A", "Betelgeuse"),
        ("Em que ano ocorreu a Queda de Constantinopla?", "1453", "1204", "1099", "1571"),
        ("Quem fundou a psicanálise lacaniana?", "Jacques Lacan", "Freud", "Jung", "Klein"),
        ("Qual é a capital do Suriname?", "Paramaribo", "Caiena", "Georgetown", "Caracas"),
        ("O que é o Bóson de Higgs?", "Partícula de Deus", "Antimatéria", "Buraco de minhoca", "Onda gravitacional"),
        ("Quem pintou 'A Escola de Atenas'?", "Rafael", "Michelangelo", "Da Vinci", "Donatello"),
        ("Qual é a ilha mais garnde do mundo (não continente)?", "Groenlândia", "Nova Guiné", "Borneo", "Madagascar"),
        ("Quem escreveu 'A Riqueza das Nações'?", "Adam Smith", "Karl Marx", "Keynes", "Ricardo"),
        ("Qual é a capital da Mongólia?", "Ulaanbaatar", "Astana", "Bishkek", "Dushanbe"),
        ("O que é a Pedra de Roseta?", "Chave para hieróglifos", "Artefato alienígena", "Lei romana", "Mapa do tesouro"),
        ("Quem foi o primeiro ser vivo no espaço?", "Laika", "Gagarin", "Ham", "Belka"),
        ("Qual é a temperatura do zero absoluto?", "-273,15 °C", "-100 °C", "-500 °C", "0 °C"),
        ("Quem escreveu 'Esperando Godot'?", "Samuel Beckett", "Ionesco", "Pinter", "Sartre"),
        ("Qual é a capital de Djibuti?", "Djibuti", "Asmara", "Mogadíscio", "Addis Abeba"),
        ("O que é o paradoxo de Fermi?", "Onde estão os alienígenas?", "O gato está vivo?", "Viagem no tempo?", "Velocidade da luz?"),
        ("Quem compôs 'A Sagração da Primavera'?", "Stravinsky", "Debussy", "Ravel", "Mahler"),
        ("Qual é o metal mais caro do mundo?", "Ródio", "Ouro", "Platina", "Paládio"),
        ("Em que batalha Napoleão foi derrotado definitivamente?", "Waterloo", "Austerlitz", "Leipzig", "Trafalgar"),
        ("Quem escreveu 'Moby Dick'?", "Herman Melville", "Mark Twain", "Poe", "Hawthorne"),
        ("Qual é a capital de Quirguistão?", "Bishkek", "Tashkent", "Dushanbe", "Ashgabat"),
        ("O que são neutrinos?", "Partículas fantasmas", "Nêutrons rápidos", "Elétrons positivos", "Luz sólida"),
        ("Quem foi o arquiteto de Brasília?", "Oscar Niemeyer", "Lúcio Costa", "Burle Marx", "Le Corbusier"),
        ("Qual é a capital de Ruanda?", "Kigali", "Bujumbura", "Gitega", "Kampala"),
        ("O que é a sequência de Fibonacci?", "Soma dos anteriores", "Números primos", "Raiz quadrada", "Divisão por 2"),
        ("Quem pintou 'A Ronda Noturna'?", "Rembrandt", "Vermeer", "Rubens", "Hals"),
        ("Qual é o rio que atravessa Londres?", "Tâmisa", "Sena", "Danúbio", "Reno"),
        ("Quem escreveu 'O Processo'?", "Kafka", "Camus", "Sartre", "Hesse"),
        ("Qual é a capital do Timor-Leste?", "Dili", "Jakarta", "Kupang", "Darwin"),
        ("O que é o Efeito Doppler?", "Mudança de frequência", "Refração da luz", "Gravidade quântica", "Expansão térmica"),
        ("Quem foi o primeiro rei de Portugal?", "D. Afonso Henriques", "D. Dinis", "D. Manuel", "D. João I"),
        ("Qual é a capital de Chipre?", "Nicósia", "Limassol", "Larnaca", "Paphos"),
        ("O que é a matéria escura?", "Massa invisível", "Buraco negro", "Antimatéria", "Vácuo"),
        ("Quem escreveu 'Os Miseráveis'?", "Victor Hugo", "Dumas", "Zola", "Balzac"),
        ("Qual é a capital de Malta?", "Valeta", "Mdina", "Sliema", "Victoria"),
        ("O que é a singularidade?", "Ponto de densidade infinita", "Inteligência artificial", "Fim do universo", "Origem da vida"),
        ("Quem compôs 'Bolero'?", "Ravel", "Debussy", "Bizet", "Chopin"),
        ("Qual é o deserto mais antigo do mundo?", "Namibe", "Saara", "Atacama", "Gobi"),
        ("Quem foi o autor de 'A República'?", "Platão", "Sócrates", "Aristóteles", "Homero"),
        ("Qual é a capital da Eslovênia?", "Liubliana", "Zagreb", "Bratislava", "Sarajevo"),
        ("O que é um fractal?", "Padrão repetitivo", "Erro matemático", "Figura 3D", "Tipo de gráfico"),
        ("Quem descobriu a Antártida?", "Fabian von Bellingshausen", "Cook", "Amundsen", "Scott"),
        ("Qual é a capital da Moldávia?", "Chisinau", "Tiraspol", "Odessa", "Bucareste"),
        ("O que é a Lei de Moore?", "Transistores dobram", "Gravidade aumenta", "Velocidade constante", "Preço cai"),
        ("Quem pintou 'A Moça com o Brinco de Pérola'?", "Vermeer", "Rembrandt", "Van Gogh", "Picasso"),
        ("Qual é a capital de Omã?", "Mascate", "Dubai", "Doha", "Manama"),
        ("O que é a Constante de Planck?", "Quantum de ação", "Velocidade da luz", "Gravidade", "Pi"),
        ("Quem escreveu 'Guerra e Paz'?", "Tolstói", "Dostoiévski", "Pushkin", "Tchekhov"),
        ("Qual é a capital de Laos?", "Vientiane", "Phnom Penh", "Hanoi", "Yangon"),
        ("O que é a Teoria das Cordas?", "Universo vibratório", "Música das esferas", "Nós quânticos", "Tecido do tempo"),
        ("Quem foi o primeiro Papa?", "São Pedro", "São Paulo", "Constantino", "Bento"),
        ("Qual é a capital do Gabão?", "Libreville", "Bata", "Malabo", "Luanda"),
        ("O que é o Código de Hamurabi?", "Leis antigas", "Receita médica", "Mapa estelar", "Livro sagrado"),
        ("Quem escreveu 'Lolita'?", "Nabokov", "Joyce", "Miller", "Orwell"),
        ("Qual é a capital de Brunei?", "Bandar Seri Begawan", "Kota Kinabalu", "Kuching", "Miri")
    ]

    # Fill remaining very hard questions with generated Math/Logic if needed, but the list is ~75.
    # Let's add some complex logic math to reach 100 or close.
    for i in range(25):
        a = random.randint(11, 30)
        ans = a * a
        distractors = set()
        while len(distractors) < 3:
            d = ans + random.randint(-20, 20)
            if d != ans: distractors.add(str(d))
        questions.append({
            "question": f"Qual é o quadrado de {a}?",
            "option_a": str(ans), "option_b": list(distractors)[0], "option_c": list(distractors)[1], "option_d": list(distractors)[2],
            "correct_option": str(ans), "phase": 4, "difficulty": "Muito Difícil"
        })

    for q, ans, d1, d2, d3 in gk_very_hard:
        questions.append({
            "question": q,
            "option_a": ans, "option_b": d1, "option_c": d2, "option_d": d3,
            "correct_option": ans, "phase": 4, "difficulty": "Muito Difícil"
        })

    return questions

def seed_db():
    db = SessionLocal()

    # Check if we already have many questions
    count = db.query(Question).count()
    if count >= 300:
        print(f"Database already has {count} questions. Skipping seed.")
        db.close()
        return

    print("Seeding questions...")
    qs = generate_questions()

    # Shuffle options for randomness in storage? No, quiz logic does that or we do it here.
    # But currently UI displays A,B,C,D fixed. Let's shuffle options assignment here.

    for item in qs:
        # Create option list
        opts = [item['option_a'], item['option_b'], item['option_c'], item['option_d']]
        random.shuffle(opts)

        # New question object
        q = Question(
            question=item['question'],
            option_a=opts[0],
            option_b=opts[1],
            option_c=opts[2],
            option_d=opts[3],
            correct_option=item['correct_option'], # Text based matching
            phase=item['phase'],
            difficulty=item['difficulty']
        )
        db.add(q)

    db.commit()
    print(f"Seeded {len(qs)} questions.")
    db.close()

if __name__ == "__main__":
    seed_db()
