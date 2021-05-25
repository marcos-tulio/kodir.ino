<p align="center"><img src="https://raw.githubusercontent.com/marcos-tulio/kodir.ino/master/addon/fanart.png" width="800"></p>

## kodir.ino
Controle o kodi por meio de controle remoto IR e um Arduino.

#### Características
- Comandos enviados diretamente ao Kodi (sem simulação de teclas)
- Vários controles remotos podem ser utilizados ao mesmo tempo
- Fácil mapeamento de teclas: apontou, pressionou e usou
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
- Grave no Arduino alguma versão dos <a href="https://github.com/marcos-tulio/kodir.ino/tree/master/arduino">códigos disponíveis</a>
- Instale o addon <a href="https://github.com/marcos-tulio/kodir.ino/tree/master/dist">kodir.ino</a>  no Kodi
- Configure o valor do `PID` e do `VID` do Arduino no Addon
- Desative e ative novamente o Addon
- Mapeie as teclas do controle remoto de acordo com o desejado

## Testado nas versões
- Kodi from debian 17.6 (kodir.ino 1.0.1)
- Kodi 18.7 (kodir.ino 1.0.1)
- Kodi 19.0 (kodir.ino 1.0.2)
