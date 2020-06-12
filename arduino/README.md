### kodir
Este código utiliza apenas um sensor IR com seu pino de leitura definido em `IR_PIN` 

### kodir_pc
Este código permite que acione um pino através de um tecla pressionada no controle. Recomendado para sistemas onde faz-se 
necessário utilizar um botão físico, como o `POWER SW` de um computador, para seu acionamento (necessário alimentação de stand-by).
- `IR_PIN` - Pino de leitura do sensor IR
- `CTL_ON_1` - Código hex. da primeira tecla para acionar o pino
- `CTL_ON_2` - Código hex. da segunda tecla para acionar o pino
- `CTL_ON_3` - Código hex. da terceira tecla para acionar o pino
- `CTL_ON_PIN_IN` - Pino para verificar se o sistema está ligado; após receber nível alto, não permite que o pino de acionamento envie mais pulsos
- `CTL_ON_PIN_OUT` - Pino que será acionado quando alguma das três teclas definidas for pressionada (pulso)

### kodir_pc_led
Similar ao `kodir_pc`, porém este código possui a capacidade de acionar um led RG -- executa com uma transição de cor de verde para vermelho
e vice-versa de acordo com o estado do sistema.
