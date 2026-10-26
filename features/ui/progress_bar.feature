#language: pt

@ui @progress
Funcionalidade: Progress Bar
  Como QA
  Quero controlar a barra de progresso
  Para validar parada, conclusão e reset

  Cenário: Parar antes de 25% e resetar ao chegar em 100%
    Dado que acesso o site DemoQA
    Quando escolho a opção "Widgets" na página inicial
    E clico no submenu "Progress Bar"
    E inicio a progress bar
    E paro a progress bar antes de atingir 25%
    Então o valor da progress bar é menor ou igual a 25%
    Quando inicio a progress bar novamente
    E aguardo a progress bar chegar a 100%
    E reseto a progress bar
    Então o valor da progress bar é 0%
