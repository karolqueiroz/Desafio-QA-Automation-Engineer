#language: pt

@ui @sortable
Funcionalidade: Sortable
  Como QA
  Quero reordenar elementos com drag and drop
  Para validar a ordenação crescente da lista

  Cenário: Colocar os elementos da lista em ordem crescente
    Dado que acesso o site DemoQA
    Quando escolho a opção "Interactions" na página inicial
    E clico no submenu "Sortable"
    E ordeno os elementos em ordem crescente usando drag and drop
    Então a lista exibe os elementos em ordem crescente
