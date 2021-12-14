# Bem vindo ao Instadroid(OBSOLETE)

Olá, esse é um projeto criado para aumentar as suas interações e arrecadar mais seguidores no instagram.
**ThalisDev**

# Funções do instadroid

O instadroid foi feito na liguagem **python** e utilizando o **webdriver**.

## Inicio

De inicio você deve definir seu usuario e senha.

    $ Login_Function = InstaDroid("Usuario", "Senha")
    $ Login_Function.login()

## Definindo Hashtags a serem usadas

Você pode definir as hashtags a serem usadas abrindo o arquivo **hashtags.txt** e modificando 

## Contador de comentarios.
     #condição após contagem chegar a 50!
     if contador == 25:
basta mudar o número 25 para o numero de vezes que voce deseja que o programa comente.
## Contador do programa.

     with open('contador_hashtags.pkl', 'rb') as f:
                load = pickle.load(f)
                print('\nContador de hashtags em: {}'.format(load))

                if load < 35:
                    with open('contador_hashtags.pkl', 'wb') as file:
                        load += 1
                        pickle.dump(load, file)

                if load == 35:
                    with open('contador_hashtags.pkl', 'wb') as handle:
                        load = 0
                        pickle.dump(load, handle)

Basta que se altere o numero 35 para o numero desejado de vezes que o programa continue o loop.
## Comentarios que serão usados.
Você pode alterar os comentarios que estarão sendo usados no programa editando o arquivo **comentarios.txt** 
