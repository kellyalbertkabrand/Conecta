import json
O='/tmp/claude-0/-home-user/576081bf-d1ab-5bb8-804a-2a1c062f4721/scratchpad/reels/'
frases={
 'p1':{'tag':'Marcas & Líderes · Gravataí 2026','h':'A noite das marcas\n"mais lembradas"\nde Gravataí'},
 'p2':{'tag':'Realização','h':'Um prêmio realizado\npela "ACIGRA"','sub':'Associação Comercial, Industrial e\nde Serviços de Gravataí'},
 'p3':{'tag':'16ª edição','h':'Por trás de cada marca,\numa "história"'},
 'p4':{'tag':'Conecta · Núcleo de Negócios ACIGRA','h':'"04 nucleados"\ndo Conecta premiados\nnesta noite'},
 'p5':{'tag':'Os premiados do Conecta','lista':['Amor de Bicho','Pampas Garden','Parkolor','LA Cosméticos']},
 'p6':{'tag':'Pessoas que fortalecem pessoas','h':'Ouça quem viveu\nessa "noite"'},
}
nomes={
 'n1':{'tag':'Coordenação','nome':'Grazi Martini','sub':'Coordenadora do Conecta'},
 'n2':{'tag':'Premiada · Marcas & Líderes 2026','nome':'Carolina Bedin Frigeri','sub':'Amor de Bicho'},
 'n3':{'tag':'Premiada · Marcas & Líderes 2026','nome':'Pampas Garden','sub':'Jardinagem e paisagismo'},
 'n4':{'tag':'Premiada · Marcas & Líderes 2026','nome':'Eloisa Nunes','sub':'Parkolor · Fotografia'},
 'n5':{'tag':'Premiada · Marcas & Líderes 2026','nome':'Adriana Mocelin','sub':'LA Cosméticos'},
}
# legendas: (inicio, fim, texto) em segundos do arquivo original
leg={
1:[(2.93,4.50,'Olá, eu sou a Grazi,'),(4.57,6.40,'coordenadora do "Conecta ACIGRA",'),(6.41,9.70,'e estamos aqui em um grupo grande para comemorar'),(9.77,11.45,'com os nossos nucleados'),(11.51,14.40,'essa noite tão especial do "Marcas & Líderes".'),(14.51,16.20,'Temos "quatro nucleados"'),(16.27,19.90,'que foram lembrados pela nossa comunidade de Gravataí:'),(20.01,22.80,'"LA Cosméticos", da Adriana,'),(22.89,27.10,'"Amor de Bicho", da Carolina,'),(27.19,29.00,'temos a Eloisa, da "Parkolor",'),(29.03,30.90,'e a "Pampas Garden" também.')],
2:[(0.18,3.00,'Eu quero agradecer a Gravataí'),(3.02,5.65,'por mais um ano ganhando o "Marcas & Líderes",'),(5.70,8.20,'primeiro lugar pela "décima vez".'),(8.26,11.00,'"Amor de Bicho", muito obrigada.'),(11.06,12.85,'É uma honra estar aqui novamente'),(12.86,16.70,'e fazer jus a este prêmio.'),(16.80,17.80,'Muito obrigada.')],
3:[(0.50,3.75,'Hoje eu vim aqui agradecer a você'),(3.80,8.10,'que nos prestigia e votou na "Pampas Garden".'),(8.16,9.90,'É um orgulho muito grande'),(9.96,12.50,'e uma responsabilidade maior ainda,'),(12.58,16.80,'e serve de "combustível" para nós,'),(16.84,20.60,'da Pampas Garden, seguir com empenho, dedicação,'),(20.70,22.90,'estudando e muito trabalho.'),(23.00,24.38,'Muito obrigado a todos.'),(24.42,27.95,'E outra coisa: parabéns à ACIGRA'),(28.00,29.45,'e ao grupo "Conecta",'),(29.48,33.20,'do qual nossa empresa, Pampas Garden, faz parte.'),(33.30,34.00,'"Gratidão."')],
4:[(0.78,3.50,'Meu agradecimento especial à ACIGRA'),(3.54,5.45,'pelo prêmio "Marcas & Líderes":'),(5.52,6.95,'uma das marcas mais lembradas'),(6.98,8.60,'na categoria "Fotografia".'),(8.68,11.90,'E o Conecta da ACIGRA leva "quatro troféus".'),(11.98,14.00,'Um brinde a nós, parabéns a nós!')],
5:[(0.00,2.95,'Obrigada a todos os meus clientes'),(3.02,5.20,'por terem me escolhido'),(5.26,8.45,'e eu estar, pela primeira vez,'),(8.52,11.90,'no "Marcas & Líderes" de Gravataí.')],
}
json.dump({'frases':frases,'nomes':nomes,'leg':leg},open(O+'spec.json','w'),ensure_ascii=False,indent=1)
