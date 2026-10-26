#language: pt

@ui @windows
Funcionalidade: Browser Windows
  Como QA
  Quero validar a abertura de uma nova janela
  Para garantir o comportamento do botão New Window

  Cenário: Abrir nova janela, validar a mensagem e fechá-la
    Dado que acesso o site DemoQA
    Quando escolho a opção "Alerts, Frame & Windows" na página inicial
    E clico no submenu "Browser Windows"
    E clico no botão "New Window"
    Então uma nova janela é aberta com a mensagem "This is a sample page"
    Quando fecho a nova janela
    Então apenas a janela original permanece aberta
