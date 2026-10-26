#language: pt

@ui @form
Funcionalidade: Practice Form
  Como QA
  Quero preencher e enviar o formulário de prática
  Para validar o fluxo de cadastro de estudante

  Cenário: Preencher e enviar o formulário com valores aleatórios
    Dado que acesso o site DemoQA
    Quando escolho a opção "Forms" na página inicial
    E clico no submenu "Practice Form"
    E preencho todo o formulário com valores aleatórios
    E envio o formulário
    Então um popup de confirmação é exibido com os dados informados
    Quando fecho o popup
    Então o popup não é mais exibido
