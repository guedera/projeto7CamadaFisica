Voce deverá construir um equalizador de áudio capaz e atuar em 12 bandas de frequências (ou mais, se desejar). O usuário deverá poder configurar o filtro de modo a atenuar ou amplificar cada uma das frequências em diferentes níveis! A atenuação e a amplificação de cada uma das faixas deve 
estar entre -10B a +10dB e as frequências amplificadas ou atenuadas são as da figura abaixo. 
 
 
Para obter a função de transferência discreta dos filtros utilizados, você poderá usar o código fornecido filtro_peak_EQ. 

Ao iniciar a aplicação, o usuário irá configurar o 
equalizador, definindo a amplificação ou atenuação de cada uma das bandas.   
Seu código deve então de obter as funções de transferência coerentes com a configuração do equalizador. 


Após isso, 
deve aplicar os filtros um a um ao sinal.  
  
O sinal resultante deve ser executado após o sinal original, a fim de observarmos a diferença entre os áudios!  

O código deverá plotar o diagrama de Bode do filtro como um todo! Para isso você deverá pensar em como obter 
uma função de transferência que equivale a todas as funções individuais de cada banda!