<p align="center"><img src="https://raw.githubusercontent.com/marcos-tulio/kodir.ino/master/fanart.png" width="800"></p>

## kodir.ino
Controle o kodi por meio de controle remoto IR e um Arduino.

#### Características
- Comandos enviados diretamente ao Kodi (sem simulação de teclas)
- Vários controles remotos podem ser utilizados ao mesmo tempo
- Fácil mapeamente de teclas: apontou, clicou e usou
- Personalização do uso: tempo de resposta de teclas e etc.
- Sistema inicializa juntamente com o Kodi

## Requisitos

#### Hardware
- Arduino
- Sensor IR
- Controle remoto IR

#### Software
- <a href="https://github.com/marcos-tulio/kodir.ino/tree/master/arduino">Firmware</a> para o arduino
- Addon <a href="https://github.com/marcos-tulio/kodir.ino/tree/master/dist">kodir.ino</a> instalado em seu Kodi

## Como utilizar
- Grave no Arduino uma das versões do <a href="https://github.com/marcos-tulio/kodir.ino/tree/master/arduino">código disponível</a>
- Instale o addon <a href="https://github.com/marcos-tulio/kodir.ino/tree/master/dist">kodir.ino</a>  no Kodi
- Configure o valor do `PID` e do `VID` do Arduino no Addon
- Desative e ative novamente o Addon
- Mapeie as teclas do controle remoto de acordo com o desejado

## Testado nas versões
- Kodi from debian 17.6
- Kodi 18.7
