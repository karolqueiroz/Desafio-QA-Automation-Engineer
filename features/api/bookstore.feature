#language: pt

@api
Funcionalidade: Fluxo de reserva de livros na BookStore (API)
  Como QA
  Quero validar o fluxo completo de usuário e reserva de livros
  Para garantir que as APIs da BookStore funcionam de ponta a ponta

  Cenário: Criar usuário, autorizar e reservar dois livros
    Dado que crio um novo usuário com dados válidos
    E gero um token de acesso para o usuário
    Quando confirmo que o usuário está autorizado
    E listo os livros disponíveis
    E reservo dois livros de livre escolha
    Então os detalhes do usuário exibem os dois livros reservados
