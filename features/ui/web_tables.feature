#language: pt

@ui @tables
Funcionalidade: Web Tables
  Como QA
  Quero criar, editar e deletar registros na tabela
  Para validar o CRUD da Web Table

  Cenário: Criar, editar e deletar um registro
    Dado que acesso o site DemoQA
    Quando escolho a opção "Elements" na página inicial
    E clico no submenu "Web Tables"
    E crio um novo registro
    Então o registro criado aparece na tabela
    Quando edito o registro criado
    Então o registro editado aparece na tabela com os novos dados
    Quando deleto o registro criado
    Então o registro não existe mais na tabela

  @bonus
  Cenário: Criar 12 registros dinamicamente e deletar todos
    Dado que acesso o site DemoQA
    Quando escolho a opção "Elements" na página inicial
    E clico no submenu "Web Tables"
    E exibo 50 linhas por página
    E crio 12 novos registros dinamicamente
    Então os 12 registros criados aparecem na tabela
    Quando deleto todos os registros criados
    Então nenhum dos registros criados permanece na tabela
