// Trecho do registry.ts do Estúdio de Marca (SistemaKA, branch estudiodemarca)
// com os helpers e os 10 templates do Conecta. Referência, não roda sozinho.

// ---- Conecta · Núcleo de Negócios ACIGRA ----------------------------------
// Formatos: Feed, Story, Quadrado e Apresentação 16:9 (mesmos modelos servem
// para redes sociais E slides de apresentação).
const FORMATOS_CONECTA: FormatoDef[] = [
  { formato: 'post', rotulo: 'Feed 4:5', largura: 1080, altura: 1350 },
  { formato: 'story', rotulo: 'Story 9:16', largura: 1080, altura: 1920 },
  { formato: 'card', rotulo: 'Quadrado 1:1', largura: 1080, altura: 1080 },
  { formato: 'carrossel', rotulo: 'Apresentação 16:9', largura: 1920, altura: 1080 },
]

// Fundo do card: só as famílias do Design System — Navy (gradiente), Navy CTA
// (radial) e Warm (claro). Turquesa nunca é fundo inteiro.
function campoFundoConecta(padrao: string): Campo {
  return {
    id: 'cor_fundo',
    label: 'Fundo do card',
    tipo: 'paleta',
    padrao,
    ajuda: 'Navy (escuro) ou Warm (claro). Alterne no feed: nunca 2 navy seguidos.',
    opcoes: FUNDOS_CONECTA.map((f) => ({ valor: f.valor, rotulo: f.rotulo, cor: f.hex })),
  }
}

// Tag de categoria (texto turquesa, ex.: "REUNIÃO QUINZENAL", "DICA CONECTA").
function campoTagConecta(padrao: string): Campo {
  return {
    id: 'tag',
    label: 'Tag de categoria',
    tipo: 'texto',
    placeholder: 'Ex.: DICA CONECTA',
    ajuda: 'Texto curto em maiúsculas (vira turquesa, espaçado). Sem emoji.',
    padrao,
  }
}

const AJUDA_KW =
  'Título em peso leve; a PALAVRA-CHAVE entre "aspas" ou *asteriscos* fica em ' +
  'negrito turquesa — é a identidade do sistema. Use quebras de linha. ' +
  'O texto quebra sozinho para não passar da margem.'

// Slider "volume" de tamanho de um texto (companheiro ${id}_tam, 100 = normal).
function campoTam(id: string, label: string): Campo {
  return { id: `${id}_tam`, label, tipo: 'range', min: 60, max: 160, passo: 2, padrao: 100 }
}

// Cor de UM texto (id): Automático (combina com o fundo) ou uma cor da paleta.
function campoCor(id: string, label: string): Campo {
  return {
    id: `${id}_cor`,
    label,
    tipo: 'paleta',
    padrao: 'auto',
    opcoes: [
      { valor: 'auto', rotulo: 'Automático' },
      ...COLORS_CONECTA.map((c) => ({ valor: c.valor, rotulo: c.rotulo, cor: c.hex })),
    ],
  }
}

// Cor do logo: Automático (segue o fundo) ou fixa.
function campoCorLogoConecta(): Campo {
  return {
    id: 'cor_logo',
    label: 'Cor do logo',
    tipo: 'select',
    chips: true,
    padrao: 'auto',
    opcoes: [
      { valor: 'auto', rotulo: 'Automático' },
      { valor: 'branco', rotulo: 'Branco' },
      { valor: 'turquesa', rotulo: 'Turquesa' },
      { valor: 'navy', rotulo: 'Navy' },
    ],
  }

// ... (outros clientes omitidos) ...

  // ==== Conecta · Núcleo de Negócios ACIGRA (Design System) ================
  {
    id: 'conecta-capa',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Capa',
    descricao:
      'Abertura editorial: logo centralizado, tag, título light com palavra-' +
      'chave em turquesa, linha e subtítulo. Navy ou Warm.',
    formatos: FORMATOS_CONECTA,
    campos: [
      campoTagConecta('CONECTA'),
      {
        id: 'titulo',
        label: 'Título',
        tipo: 'textarea',
        obrigatorio: true,
        placeholder: 'Ex.: Conexões com "propósito"',
        ajuda: AJUDA_KW,
        padrao: 'Conexões com\n"propósito"',
      },
      {
        id: 'subtitulo',
        label: 'Subtítulo (opcional)',
        tipo: 'textarea',
        placeholder: 'Uma linha de apoio…',
        padrao: 'O núcleo de negócios da ACIGRA em Gravataí.',
      },
      { id: 'deslize', label: 'Rodapé (ex.: Deslize →)', tipo: 'texto', padrao: 'Deslize →' },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('titulo', 'Tamanho — Título'),
      campoCor('titulo', 'Cor — Título'),
      campoTam('subtitulo', 'Tamanho — Subtítulo'),
      campoCor('subtitulo', 'Cor — Subtítulo'),
      campoTam('deslize', 'Tamanho — Rodapé'),
      campoCor('deslize', 'Cor — Rodapé'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaCapaCard,
  },
  {
    id: 'conecta-conteudo',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Conteúdo (slide interno)',
    descricao:
      'Slide de conteúdo: logo + número decorativo, tag, título light com ' +
      'keyword turquesa, linha e texto de apoio. MISSÃO, VISÃO, dicas, sinais.',
    formatos: FORMATOS_CONECTA,
    campos: [
      { id: 'numero', label: 'Número (opcional)', tipo: 'texto', maxLen: 2, placeholder: 'Ex.: 01', padrao: '01' },
      campoTagConecta('SINAL 01'),
      {
        id: 'titulo',
        label: 'Título',
        tipo: 'textarea',
        obrigatorio: true,
        ajuda: AJUDA_KW,
        padrao: 'Você decide por\n"impulso", não por\nestratégia',
      },
      {
        id: 'texto',
        label: 'Texto de apoio',
        tipo: 'textarea',
        ajuda: 'Peso leve, cinza. Frase curta de reforço.',
        padrao:
          'Sem processos claros, cada decisão vira aposta. O núcleo ajuda a trocar o achismo por método.',
      },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('titulo', 'Tamanho — Título'),
      campoCor('titulo', 'Cor — Título'),
      campoTam('texto', 'Tamanho — Texto'),
      campoCor('texto', 'Cor — Texto'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaConteudoCard,
  },
  {
    id: 'conecta-lista',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Lista (valores / objetivos)',
    descricao:
      'Tag + título + lista editorial. Cada linha “Rótulo: descrição” destaca ' +
      'o rótulo em turquesa. Ex.: VALORES, OBJETIVOS.',
    formatos: FORMATOS_CONECTA,
    campos: [
      campoTagConecta('O NÚCLEO'),
      { id: 'titulo', label: 'Título (opcional)', tipo: 'texto', placeholder: 'Ex.: Nossos valores', padrao: 'Nossos valores' },
      {
        id: 'itens',
        label: 'Itens (um por linha)',
        tipo: 'textarea',
        obrigatorio: true,
        ajuda: 'Um item por linha. Use “Rótulo: descrição” para destacar o rótulo.',
        padrao:
          'Conexão: aproximar empresários e fortalecer relações.\n' +
          'Colaboração: compartilhar conhecimento e oportunidades.\n' +
          'Desenvolvimento: aprendizado contínuo, no CNPJ e no CPF.\n' +
          'Confiança: escuta, transparência e respeito.\n' +
          'Propósito: impacto positivo na comunidade.',
      },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('titulo', 'Tamanho — Título'),
      campoCor('titulo', 'Cor — Título'),
      campoTam('itens', 'Tamanho — Itens'),
      campoCor('itens', 'Cor — Itens'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaListaCard,
  },
  {
    id: 'conecta-foto',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Card com foto (evento)',
    descricao:
      'Foto full-bleed com overlay (Navy) ou emoldurada (Warm). Logo branco, ' +
      'tag, título light e data/local. Serve Reunião Quinzenal e Palestra ' +
      '(use o sobretítulo "Convidados especiais").',
    formatos: FORMATOS_CONECTA,
    campos: [
      {
        id: 'foto',
        label: 'Foto ou vídeo',
        tipo: 'imagem',
        obrigatorio: true,
        aceitaVideo: true,
        areaPadrao: 100,
        ajuda: 'Use Posição e Zoom para enquadrar. Aceita vídeo.',
      },
      campoTagConecta('REUNIÃO QUINZENAL'),
      { id: 'sobre', label: 'Sobretítulo (opcional, ex.: Convidados especiais)', tipo: 'texto', padrao: '' },
      {
        id: 'titulo',
        label: 'Título',
        tipo: 'textarea',
        obrigatorio: true,
        ajuda: AJUDA_KW,
        padrao: 'Conexões, aprendizado\ne troca de "experiências"',
      },
      { id: 'apoio', label: 'Data — Hora · Local', tipo: 'texto', padrao: '25 Mar 2025 — 19h · ACIGRA' },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('sobre', 'Tamanho — Sobretítulo'),
      campoCor('sobre', 'Cor — Sobretítulo'),
      campoTam('titulo', 'Tamanho — Título'),
      campoCor('titulo', 'Cor — Título'),
      campoTam('apoio', 'Tamanho — Data/local'),
      campoCor('apoio', 'Cor — Data/local'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaFotoCard,
  },
  {
    id: 'conecta-1a1',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Encontro 1:1',
    descricao:
      'Foto em destaque com o selo "CONECTA 1:1" e, acima dele, os dois ' +
      'participantes (nome em CAIXA ALTA + empresa) à esquerda e à direita. ' +
      'Navy (full-bleed) ou Warm (emoldurada).',
    formatos: FORMATOS_CONECTA,
    campos: [
      {
        id: 'foto',
        label: 'Foto ou vídeo',
        tipo: 'imagem',
        obrigatorio: true,
        aceitaVideo: true,
        areaPadrao: 100,
        ajuda: 'A foto é o protagonista. Use Posição e Zoom para enquadrar.',
      },
      { id: 'nome_esq', label: 'Nome — esquerda (CAIXA ALTA)', tipo: 'texto', placeholder: 'Ex.: JOÃO SILVA', padrao: '' },
      { id: 'empresa_esq', label: 'Empresa — esquerda', tipo: 'texto', placeholder: 'Ex.: Silva Consultoria', padrao: '' },
      { id: 'nome_dir', label: 'Nome — direita (CAIXA ALTA)', tipo: 'texto', placeholder: 'Ex.: MARIA SOUZA', padrao: '' },
      { id: 'empresa_dir', label: 'Empresa — direita', tipo: 'texto', placeholder: 'Ex.: Souza & Cia', padrao: '' },
      { id: 'badge', label: 'Selo', tipo: 'texto', padrao: 'CONECTA 1:1' },
      { id: 'pos', label: 'Subir nomes e botão', tipo: 'range', min: 0, max: 700, passo: 10, padrao: 0, ajuda: 'Sobe o bloco de nomes + selo. 0 = no rodapé.' },
      campoTam('pessoaEsq', 'Tamanho — participante esquerda'),
      campoCor('pessoaEsq', 'Cor — participante esquerda'),
      campoTam('pessoaDir', 'Tamanho — participante direita'),
      campoCor('pessoaDir', 'Cor — participante direita'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaUmAUmCard,
  },
  {
    id: 'conecta-calendario',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Calendário do mês',
    descricao:
      'Mês em destaque (peso ultrafino) + ano em turquesa, com o número do ' +
      'mês gigante ao fundo. Para anunciar os eventos do mês.',
    formatos: FORMATOS_CONECTA,
    campos: [
      campoTagConecta('CALENDÁRIO'),
      { id: 'mes', label: 'Mês', tipo: 'texto', obrigatorio: true, padrao: 'Abril' },
      { id: 'ano', label: 'Ano', tipo: 'texto', padrao: '2025' },
      { id: 'rodape', label: 'Rodapé', tipo: 'texto', padrao: 'Eventos do mês →' },
      { id: 'numero', label: 'Número do mês (fundo)', tipo: 'texto', maxLen: 2, padrao: '04' },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('mes', 'Tamanho — Mês'),
      campoCor('mes', 'Cor — Mês'),
      campoTam('ano', 'Tamanho — Ano'),
      campoCor('ano', 'Cor — Ano'),
      campoTam('rodape', 'Tamanho — Rodapé'),
      campoCor('rodape', 'Cor — Rodapé'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaCalendarioCard,
  },
  {
    id: 'conecta-educativo',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Conteúdo educativo',
    descricao:
      'Capa de conteúdo: aspas decorativas, tag, título light com palavra-' +
      'chave em turquesa, texto de apoio e "Deslize →".',
    formatos: FORMATOS_CONECTA,
    campos: [
      campoTagConecta('DICA CONECTA'),
      {
        id: 'titulo',
        label: 'Título',
        tipo: 'textarea',
        obrigatorio: true,
        ajuda: AJUDA_KW,
        padrao: '5 perguntas que todo\nempresário deveria\n"se fazer"',
      },
      {
        id: 'texto',
        label: 'Texto de apoio',
        tipo: 'textarea',
        padrao: 'Antes de pensar em crescer, pare e reflita.',
      },
      { id: 'deslize', label: 'Rodapé (ex.: Deslize →)', tipo: 'texto', padrao: 'Deslize →' },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('titulo', 'Tamanho — Título'),
      campoCor('titulo', 'Cor — Título'),
      campoTam('texto', 'Tamanho — Texto'),
      campoCor('texto', 'Cor — Texto'),
      campoTam('deslize', 'Tamanho — Rodapé'),
      campoCor('deslize', 'Cor — Rodapé'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaEducativoCard,
  },
  {
    id: 'conecta-frase',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Frase de virada',
    descricao:
      'Slide de impacto: aspas decorativas e uma frase centralizada em peso ' +
      'leve, com a palavra-chave em turquesa.',
    formatos: FORMATOS_CONECTA,
    campos: [
      {
        id: 'frase',
        label: 'Frase',
        tipo: 'textarea',
        obrigatorio: true,
        ajuda: AJUDA_KW,
        padrao: 'Empresas crescem quando\nas pessoas por trás delas\ncrescem "juntas".',
      },
      campoTam('frase', 'Tamanho — Frase'),
      campoCor('frase', 'Cor — Frase'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaFraseCard,
  },
  {
    id: 'conecta-cta',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'CTA (fechamento)',
    descricao:
      'Fechamento do carrossel: logo grande, tag, frase conceitual e o tom de ' +
      'exclusividade (as vagas abrem duas vezes por ano). Fundo radial.',
    formatos: FORMATOS_CONECTA,
    campos: [
      campoTagConecta('NÚCLEO DE NEGÓCIOS ACIGRA'),
      {
        id: 'frase',
        label: 'Frase conceitual',
        tipo: 'textarea',
        obrigatorio: true,
        ajuda: AJUDA_KW,
        padrao: 'Conexão com "propósito".\nCrescimento com "consistência".',
      },
      { id: 'exclusivo', label: 'Linha de exclusividade', tipo: 'texto', padrao: 'As vagas abrem duas vezes por ano.' },
      campoTam('tag', 'Tamanho — Tag'),
      campoCor('tag', 'Cor — Tag'),
      campoTam('frase', 'Tamanho — Frase'),
      campoCor('frase', 'Cor — Frase'),
      campoTam('exclusivo', 'Tamanho — Exclusividade'),
      campoCor('exclusivo', 'Cor — Exclusividade'),
      campoCorLogoConecta(),
      campoFundoConecta('cta'),
    ],
    render: ConectaCtaCard,
  },
  {
    id: 'conecta-feedback',
    clienteSlug: 'conecta',
    clienteNome: 'Conecta · Núcleo de Negócios ACIGRA',
    nome: 'Card de Feedback',
    descricao:
      'Prova social: logo, tag e box branco com avatar, nome, estrelas e o ' +
      'depoimento real. Navy ou Warm.',
    formatos: FORMATOS_CONECTA,
    campos: [
      { id: 'rotulo', label: 'Tag do topo', tipo: 'texto', padrao: 'DEPOIMENTO' },
      {
        id: 'nome',
        label: 'Nome do nucleado',
        tipo: 'texto',
        obrigatorio: true,
        placeholder: 'Como a pessoa aparece',
        padrao: 'Fernanda Pereira',
      },
      {
        id: 'subtitulo',
        label: 'Subtítulo (opcional)',
        tipo: 'texto',
        placeholder: 'Ex.: Empresa · Segmento',
        padrao: 'Nucleada Conecta',
      },
      {
        id: 'texto',
        label: 'Depoimento',
        tipo: 'textarea',
        obrigatorio: true,
        placeholder: 'Cole aqui o depoimento real…',
        ajuda: 'Transcreva o depoimento REAL. Sem data.',
        padrao:
          'No Conecta encontrei muito mais que networking: relações de confiança ' +
          'que fortaleceram o meu negócio. Recomendo demais!',
      },
      { id: 'nota', label: 'Nota (estrelas)', tipo: 'estrelas', padrao: 5 },
      {
        id: 'inicial',
        label: 'Letra do avatar (opcional)',
        tipo: 'texto',
        maxLen: 2,
        placeholder: 'Vazio = 1ª letra do nome',
        padrao: '',
      },
      campoTam('rotulo', 'Tamanho — Tag'),
      campoCor('rotulo', 'Cor — Tag'),
      campoCorLogoConecta(),
      campoFundoConecta('navy'),
    ],
    render: ConectaFeedbackCard,
  },
