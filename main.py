import os
import random
import time
import logging
import gc
import pickle
import sys

from selenium import webdriver
from bs4 import BeautifulSoup as bs


class InstaDroid:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.set_preference("intl.accept_languages", "pt,pt-BR")
        firefoxProfile.set_preference("dom.webnotifications. enabled", False)
        self.driver = webdriver.Firefox(firefox_profile=firefoxProfile, executable_path=r"./geckodriver")

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)
        user_element = driver.find_element_by_name("username")
        user_element.clear()
        user_element.send_keys(self.username)
        time.sleep(3)
        password_element = driver.find_element_by_name("password")
        password_element.clear()
        password_element.send_keys(self.password)
        time.sleep(4)
        login_button = driver.find_element_by_xpath("//form[@id='loginForm']/div/div[3]/button/div")
        login_button.click()
        time.sleep(5)

        # escolha das hashtags
        arquivo_hash = open('hashtags.txt', 'r', encoding="utf8")
        hashtags = arquivo_hash.readlines()
        arquivo_hash.close()
        random_hash = random.choice(hashtags)

        # Evita a inserção de hashtags repetidas
        try:
            # abre o arquivo e grava
            Dump = open("dump_hashtags.txt", "a", encoding='utf8')
            Dump.write(random_hash)
            Dump.close()

            # abre o arquivo e lê
            Dumped = open('dump_hashtags.txt', 'r', encoding='utf8')
            lista = Dumped.readlines()
            Dumped.close()

            # remove ultima sentença da lista
            lista.remove(lista[-1])

            # compara a variavel choice com a da lista e bloqueia duplicadas!
            if random_hash in lista:
                print('\nHashtag já usada'
                      '\nReiniciando...')

                # Removendo 1 do contador dump_hashtags
                with open('contador_hashtags.pkl', 'rb') as f:
                    load = pickle.load(f)
                    print('\nContador de hashtags em: {}'.format(load))

                with open('contador_hashtags.pkl', 'wb') as file:
                    load -= 1
                    pickle.dump(load, file)

                time.sleep(5)
                driver.close()
                os.startfile('main.exe')
                sys.exit(0)

        except Exception as ex:
            logging.error(ex)

        # função de contador para zerar o arquivo de dump_hashtags automaticamente!
        finally:
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

                    print('\n-------AVISO!-------'
                          '\nPARANDO BOT PORQUE TODAS AS HASHTAGS JA FORAM COMENTADAS!')
                    driver.close()
                    sys.exit(0)

        self.comente_nas_fotos_com_a_hashtag(random_hash)  # retorna hashtag selecionada

    # habilita o garbage collector do python!!
    gc.enable()
    print('\nGarbage collector is: {}'.format(gc.isenabled()))

    @staticmethod
    # comenta nas fotos com a frequencia de letras por minuto de um humano!
    def type_like_a_person(sentence, single_input_field):
        print("\nComeçando a digitar mensagem de texto")

        for letter in sentence:
            single_input_field.send_keys(letter)
            time.sleep(random.randint(1, 5) / 30)

    # escolhe as hashtags a serem usadas
    def comente_nas_fotos_com_a_hashtag(self, hashtag):
        links_de_posts = []
        links_filtrados = []
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(5)

        # Script para rodar scroll na pagina!
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(2, 8))

        # definindo contador para zero!
        contador = 0

        # função para resetar programa
        def restart_program():
            try:
                print("\n-------Reiniciando-------" +
                      "\n╔════════════════╗\n" +
                      "-|██████████ 100%\n" +
                      "╚════════════════╝\n")
                driver.close()
                os.startfile('main.exe')
                sys.exit(0)

            except Exception as exc:
                logging.error(exc)

        # função para curtir fotos!
        def like_pic():
            time.sleep(2)
            like = driver.find_element_by_class_name('fr66n')
            soup = bs(like.get_attribute('innerHTML'), 'html.parser')
            if soup.find('svg')['aria-label'] == 'Curtir':
                like.click()

        time.sleep(2)
        html = driver.page_source  # predefinição do BS4
        soup = bs(html, 'html.parser')

        # Função para indexar os links de posts!
        try:
            for a in soup.find_all('a', href=True):
                links_de_posts.append(a['href'])

            links_filtrados = list(filter(lambda k: '/p/' in k, links_de_posts))
            print(hashtag + "fotos escaneadas:" + str(len(links_filtrados)))

        except Exception as er:
            print(er)

        for pic_href in links_filtrados:
            driver.get('https://www.instagram.com' + pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # interação do web driver com a pagina do instagram
            try:
                arquivo = open('comentarios.txt', encoding="utf8")
                comments = arquivo.readlines()
                arquivo.close()

                driver.find_element_by_xpath("//textarea").click()
                comment_input_box = driver.find_element_by_xpath("//textarea")
                time.sleep(random.randint(2, 5))
                self.type_like_a_person(random.choice(comments), comment_input_box)
                time.sleep(random.randint(3, 5))
                driver.find_element_by_xpath("//button[@type='submit']").click()
                time.sleep(random.randint(5, 10))
                like_pic()
                print("\nCurtida!!")
                time.sleep(random.randint(300, 600))

            except Exception as e:
                logging.error(e)
                time.sleep(10)

            finally:
                # função contador
                contador += 1
                print("\nComentario No. {}".format(contador))

                # condição após contagem chegar a 50!
                if contador == 25:
                    print("\nÉ recomendado que se troque de Hashtag depois de 25 comentarios! \n" +
                          "\nReiniciando programa após termino da contagem")
                    time.sleep(random.randint(1800, 3600))
                    restart_program()


# Insira o usuário e senha aqui
Login_Function = InstaDroid("photovich_click", "3JhGHIf6Km0GeedQqFt#Ej&#0ll$D80XbeAwW&5NF3")
Login_Function.login()
