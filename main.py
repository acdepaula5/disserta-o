from Modulos import *

# cores
preto   = "#000000"
branco  = "#FFFFFF"
cinza   = "#7F7F7F"
azulEscuroAlto   = "#092642"
azulEscuroMedio  = "#174276"
azulEscureoBaixo = "#235A9F"
azul             = "#0078D4"
azulClaroBaixo   = "#0078D4"
azulClaroMedio   = "#80B9EE"
azulClaroAlto    = "#ADD8FF"

# Configurando a janela
janela = Tk()
janela.title("Reconstrução 3D")
janela.geometry("600x394")
janela.config(background="gray")
janela.wm_maxsize(width=600,height=396)
janela.wm_minsize(width=600,height=396)

# Aparencia da janela
frame_tela = Frame(janela,width=600,height=60,background="gray")
frame_tela.grid(row=0,column=0)

Titulo = Label(# Configurando o titulo
                frame_tela,width=600,height=1,background=azulEscuroMedio,
                text="Reconstrução em 3D",font='Calibri 22 bold',fg="white", highlightbackground=azulEscuroMedio,anchor=W)
Titulo.place(x=0,y=0)

#criacao de um frame para simplificar o posicionamento das opções para escolha do metodo
frame_marc = Frame()
frame_marc.place(x=62,y=229)

#criacao de um frame para simplificar o posicionamento das opções para escolha do tipo do arquivo de saída
frame_marc2 = Frame()
frame_marc2.place(x=200,y=43)

# Variaveis e input
tipo_arq_saida = StringVar()
"""ex: .dat , .vtk"""
nome_arq_saida = StringVar()
"""Nome do arquivo de saida sem o tipo do arquivo"""
name = StringVar()
"""Nome do arquivo antes do numero"""
ext = StringVar()
"""Nome do arquivo apos do numero"""
Endereco_Img = StringVar()
"""Local da pasta que contem as imagens"""
metodo_= StringVar()
"""metodo escolhido para trabalhar as imagens"""
NumImgTotal = IntVar()
"""Numero de imagens originais"""
plan_entre_img = IntVar()
"""Numero de imagens interpolada, ou seja, criadas pelo programa"""

#Pre estabelece valores para testes ou exemplificacao
tipo_arq_saida.set(".vtk")
nome_arq_saida.set("Micro")
name.set("Sem Titulo-")
ext.set(" (Copy).tif")
Endereco_Img.set("Imagens/Imagens2/")
metodo_.set("o")
NumImgTotal.set("2")
plan_entre_img.set("4")


def entrada(var,distx,disty):
    """Configurando os baloes de entrada de dados"""
    ent = Entry(janela, width=30,highlightthickness=0, 
                textvariable=var,font='Calibri 12 bold')
    ent.place(x=distx,y=disty)

def balaoEntrada(texto,disty,comp):
    """Configurando baloes que explicam os input's"""
    balao = Label(janela,
                  text=texto,font='Calibri 12',anchor=W,justify=LEFT,
                  bg="gray",width=comp)
    balao.place(x=0,y=disty)

def opcoes(onVal,texto, coluna):
    """Funcao que cria botoes que exibem as opcoes de metodos"""
    var = Checkbutton(frame_marc,highlightthickness=0, 
                text = texto,font='Calibri 12 bold',
                onvalue= onVal,variable=metodo_)
    var.grid(row=0,column=coluna)

def opcoes_tipo_arq(onVal,texto, coluna):
    """Funcao que cria botoes que exibem as opcoes do tipo do arquivo"""
    var = Checkbutton(frame_marc2,highlightthickness=0, 
                text = texto,font='Calibri 12 bold',
                onvalue= onVal,variable=tipo_arq_saida)
    var.grid(row=0,column=coluna)


#Criacao do front=======================================================================================================================
balaoEntrada("-Extensao do arquivo de saida:",42,24)
balaoEntrada("-Nome do arquivo de saida:",75,37)
balaoEntrada("-Parte do nome do arquivo contendo a\nimagem, *antes* do numero da imagem:",102,37)
balaoEntrada("-Parte do nome do arquivo contendo a\nimagem, *depois* do numero da imagem:",151,37)
balaoEntrada("-Diretorio que contem as imagens da amostra:",200,37)
balaoEntrada("-Metodo:",230,7)
balaoEntrada("-Numero inicial de imagens:",260,37)
balaoEntrada("-Numero de planos entre as\nimagens (planos interpolados):",290,37)


#entrada(tipo_arq_saida,200, 43)#1
opcoes_tipo_arq(".vtk","vtk",0)
opcoes_tipo_arq(".dat","dat",1)

entrada(nome_arq_saida,181, 76)#2
entrada(name,          270,122)#3
entrada(ext,           277,171)#4
entrada(Endereco_Img,  301,201)#5

#6 #https://www.geeksforgeeks.org/python-tkinter-checkbutton-widget/
opcoes("O","Original",0)
opcoes("V","Vazio",1)
opcoes("M","Media",2)
opcoes("R","Repeticao",3)

entrada(NumImgTotal,   182,261)#7
entrada(plan_entre_img,206,310)#8
#==================================================================================================================================================

def executar():
    print("Executando")
    print(tipo_arq_saida.get())
    print(nome_arq_saida.get())
    print(name.get())
    print(ext.get())
    print(Endereco_Img.get())
    print(metodo_.get())
    print(NumImgTotal.get())
    print(plan_entre_img.get())
    inicio = time.time()

    r = 0
    g = 0
    b = 0
    x = 0
    y = 0
    z = 0
    
    print("Verificando imagens...")
    #Tratamento de imagens=========================================================================================================================
    
    vet_de_img = []
    #vetor que armazena cada imagem e suas informacoes apenas para o tratamento de imagens

    for z in range(0,NumImgTotal.get(),1): 
        filename = Endereco_Img.get() + name.get() + str(z) + ext.get()
        #Define endereco completo da imagem a ser analisada

        img = np.array(cv2.imread(filename))
        #le umaa imagem como um vetor

        vet_de_img.append([Endereco_Img.get(),name.get(),z,ext.get(),img.shape])
        #define um vetor de dados da imagem
        
        #print("vet_de_img =")
        #print(vet_de_img[z])
        #print("img.shape =")
        #print(img.shape)
        
        if img.size == 1: #Se houve erro na identificação da imagem (endereço ou nome ou extensão) o programa é abortado
            print("Erro: A imagem "+ str(z)+ " nao pode ser carregada")
            exit()
        if z>0:
            if(vet_de_img[z][4]!=vet_de_img[z-1][4]):
                print("Erro: As dimensoes das imagens " + str(z-1) + " e " + str(z) + " nao conferem")
                exit()

        print("verificando img "+str(z))
    print("Imagens verificadas...")

    z=0

    print(".vtk"==str(tipo_arq_saida.get()))
    print(".vtk")
    print(tipo_arq_saida.get())
    print(metodo_.get())

    if str(tipo_arq_saida.get()) == ".vtk":
        match metodo_.get():
            case "O"|"o": #Caso Original
                print("vtk - metodo Original")

                linhas, colunas,cores = img.shape #obtém as dimensões vertical e horizontal, e "cores" recebe 3 pois é a quantidade de cores das imagens
                tamanho = linhas*colunas*NumImgTotal.get()
                cont = 0 #auxilia na horade escrever as coordenadas no .vtk; faz om que a informacao de 3 pixel ocupem uma linha e depois pule para a proxima

                meuArquivo = open("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get(),"w")

                print("Processando imagem...")
                #Cabecalho Paraview
                meuArquivo.write(str(formatacao.cabecalhoVTK(tamanho)))
                
                for z in range(0,NumImgTotal.get(),1):
                    for y in range(0,linhas,1):
                        for x in range(0,colunas,1):
                            meuArquivo.write(str(x) +"\t"+ str(y) + "\t"+ str(z) + "\t")

                            if (cont % 3 == 2):
                                meuArquivo.write("\n")
                                
                            cont += 1
                
                meuArquivo.write(str(formatacao.cabecalhoVTK2()))

                meuArquivo.write(str(formatacao.cabecalhoVTK3(tamanho)))
                
                cont = 0
                for i in range(0,tamanho,1):
                    #retirado direto do TCC da ana beatriz
                    #Escreve coordenadas (x, y, z)
                    meuArquivo.write(str(i) + "\t")

                    #Pula linha ap�s escrever 9 d�gitos
                    if (cont % 3 == 2):
                        meuArquivo.write("\n")
                    cont += 1

                meuArquivo.write(str(formatacao.cabecalhoVTK4(tamanho)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())


                for z in range(0,NumImgTotal.get(),1): #impressao das cores


                    for y in range(0,linhas,1):
                        for x in range(0,colunas,1):
                            
                            pixel = formatacao.pixelDAT(
                             matriz[z][y][x][0]
                            ,matriz[z][y][x][1]
                            ,matriz[z][y][x][2]
                            ,matriz[z][y][x][3]
                            ,matriz[z][y][x][4]
                            ,matriz[z][y][x][5]
                            ,matriz[z][y][x][6])
                            
                            rgb = formatacao.rgbVTK(
                            str(matriz[z][y][x][4]),
                            str(matriz[z][y][x][5]),
                            str(matriz[z][y][x][6]))

                            meuArquivo.write(rgb)

                    print(pixel)
                
                print("fim for")

            case "V"|"v": #Caso com vazios entre as imagens
                
                print("vtk - metodo Vazios")

                NumImgfinal = (NumImgTotal.get() + int(plan_entre_img.get())*(NumImgTotal.get()-1)) #Fórmula que calcula o número total de imagens, considerando imagens originais e imagens adicionadas
                linhas, colunas,cores = img.shape
                tamanho = linhas*colunas*NumImgfinal
                vazio = False #Variável que decide se é uma imagem média ou não, False = original e True = média
                cont = 0 #auxilia na hora de escrever as coordenadas no .vtk; faz om que a informacao de 3 pixel ocupem uma linha e depois pule para a proxima
                cont2 = 0 #Variavel que conta quantas imagens interpoladas foram criadas
                aux3 = 0 #variavel auxiliar que guarda o número da ultima imagem original e é utilizada no lugar do z pois z e o contador de imagens totais utilizado no for (nao posso ficar alterando ele). Enquanto isso, aux3 eu posso alterar sem possivelmente interferir no loop

                print("Processando imagem...")

                meuArquivo = open(str("Exportacao/" + nome_arq_saida.get() + tipo_arq_saida.get()),"w")
                
                #Cabeçalho Paraview
                meuArquivo.write(str(formatacao.cabecalhoVTK(tamanho)))

                for z in range(0,NumImgTotal.get(),1):
                    for y in range(0,linhas,1):
                        for x in range(0,colunas,1):
                            meuArquivo.write(str(x) +"\t"+ str(y) + "\t"+ str(z) + "\t")

                            if (cont % 3 == 2):
                                meuArquivo.write("\n")
                                
                            cont +=1

                meuArquivo.write(str(formatacao.cabecalhoVTK2()))

                meuArquivo.write(str(formatacao.cabecalhoVTK3))
                
                cont = 0
                for i in range(0,tamanho,1):
                    #retirado direto do TCC da ana beatriz
                    #Escreve coordenadas (x, y, z)
                    meuArquivo.write(str(i) + "\t")

                    #Pula linha ap�s escrever 9 d�gitos
                    if (cont % 3 == 2):
                        meuArquivo.write("\n")
                    cont += 1
                
                meuArquivo.write(str(formatacao.cabecalhoVTK4(tamanho)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())

                for z in range(0,NumImgfinal,1):

                    print("\nimagem "+ str(z))
                    print("ultima imagem original = " + str(aux3))

                    if cont2 == int(plan_entre_img.get()): #Este if identifica se o número de imagens interpoladas foi atingido, se sim ele reinicia o contador e torna a med false para que o procedimento (criar imagem original e em seguida criar n imagens interpoladas) seja repedito
                        vazio = False
                        cont2 = 0

                    if vazio == False: #Imagem original

                        print("img = orginal")
                        print("Img anterior = " + aux3)
                        print("cont2 = "+ str(cont2))

                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                r=matriz[aux3][y][x][4]
                                g=matriz[aux3][y][x][5]
                                b=matriz[aux3][y][x][6]


                                coordenadas = str(x) +"\t"+ str(y) + "\t"+ str(z)

                                rgb = (formatacao.alinhamento(str(r)) + " " + formatacao.alinhamento(str(g)) + " " + formatacao.alinhamento(str(b)))

                                pixel = (coordenadas+ " " + 
                                        str(intensity) 
                                        + " " + str(rgb)+"\n")
                                
                                meuArquivo.write( str(round(int(r)/255.0,6)) + " " + str(round(int(g)/255.0,6)) + " " + str(round(int(b)/255.0,6)) + " " + str(1) + "\n")

                        vazio = True #Essa variável sempre muda para que as proximas imagens interpoladas sejam iniciadas
                        aux3 += 1

                    else: #Imagem com vazio
                        print("img = Criada")
                        print("ultima imagem original = " + str(aux3))
                        print("cont2 = "+ str(cont2))

                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                coordenadas = str(x) + "\t" + str(y) + "\t" + str(z)

                                rgb = formatacao.rgbVTK(r,g,b)

                                pixel = (coordenadas+ " " + 
                                        str(0) 
                                        + "   " + str(rgb)+"\n")
                                
                                meuArquivo.write(rgb)
                        
                        cont2 += 1

                    # acompanhamento das variáveis (produzindo codigo)
                    print("cont2 = ",cont2)  
                    print(pixel)  #linha para avaliar um pixel de cada imagem e vê o que está acontecendo com os resultados

                        
                meuArquivo.close()
                print("\n")
                  
            case "R"|"r":
                print("vtk - metodo Repeticao")

                NumImgfinal = (NumImgTotal.get() + int(plan_entre_img.get())*(NumImgTotal.get()-1)) #Fórmula que calcula o número total de imagens, considerando imagens originais e imagens adicionadas
                linhas, colunas,cores = img.shape
                tamanho = linhas*colunas*NumImgfinal #É o número total de pixels trabalhados
                Repet = False #Variável que decide se é uma imagem média ou não, False = original e True = média
                cont = 0 #Variavel que conta quantas imagens interpoladas foram criadas
                cont2 = 0 #auxilia na hora de escrever as coordenadas no .vtk; faz om que a informacao de 3 pixel ocupem uma linha e depois pule para a proxima
                aux3 = 0 #variavel auxiliar que guarda o número da ultima imagem original e é utilizada no lugar do z pois z e o contador de imagens totais utilizado no for (nao posso ficar alterando ele). Enquanto isso, aux3 eu posso alterar sem possivelmente interferir no loop

                print("Processando imagem...")

                print("tamanho = " + str (tamanho))

                meuArquivo = open(str("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get()),"w")

                #Cabecalho Paraview
                meuArquivo.write(str(formatacao.cabecalhoVTK(tamanho)))
                
                for z in range(0,NumImgfinal,1):
                    for y in range(0,linhas,1):
                        for x in range(0,colunas,1):
                            meuArquivo.write(str(x) +"\t"+ str(y) + "\t"+ str(z) + "\t")

                            if (cont2 % 3 == 2):
                                meuArquivo.write("\n")
                                
                            cont2 += 1
                
                meuArquivo.write(str(formatacao.cabecalhoVTK2()))

                meuArquivo.write(str(formatacao.cabecalhoVTK3(tamanho)))

                cont2 = 0
                for i in range(0,tamanho,1):
                    #retirado direto do TCC da ana beatriz
                    #Escreve coordenadas (x, y, z)
                    meuArquivo.write(str(i) + "\t")

                    #Pula linha ap�s escrever 9 d�gitos
                    if (cont2 % 3 == 2):
                        meuArquivo.write("\n")
                    cont2 += 1

                meuArquivo.write(str(formatacao.cabecalhoVTK4(tamanho)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())


                for z in range(0,NumImgfinal,1):
                    print("\nimagem "+ str(z))
                    print("ultima imagem original = " + str(aux3))

                    if not(z == NumImgfinal-1) and z!=0: #Este if verifica se estamos na última imagem ou se estamos na primeira, se um desses casos é verdadeiro não é necessário fazer a imagem interpolada
                        aux4 = aux3-1
                        NumImgAnterior = str(aux3-1)

                    if cont == int(plan_entre_img.get()): #Este if identifica se o número de imagens interpoladas foi atingido, se sim ele reinicia o contador e torna a Repet false para que o procedimento (criar imagem original e em seguida criar n imagens interpoladas) seja repedito
                        Repet = False
                        cont = 0
                        
                    if Repet == False: #Imagem original
                        print("img = Original")
                        print("Img anterior = " + NumImgAnterior)
                        print("Img atual = " + NumImgAtual)
                        print("cont = "+ str(cont))

                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                r = str(matriz[aux3][y][x][4])
                                g = str(matriz[aux3][y][x][5])
                                g = str(matriz[aux3][y][x][6])
                                intensity = int(r) + int(int(g) * int(256)) + int(int(b) * int(256) * int(256))

                                #pixel utilizado para acompanhar o codigo
                                pixel = formatacao.pixelDAT(x,y,z,intensity,r,g,b)

                                rgb = formatacao.rgbVTK(r,g,b)
                                meuArquivo.write(rgb)

                        Repet = True #Essa variável sempre muda para que as proximas imagens interpoladas sejam iniciadas
                        aux3 +=1
                        print("cont = ",cont)


                    else: #Imagem Repetida
                        print("img = Criada")
                        print("Img anterior = " + NumImgAnterior)
                        print("Img atual = " + NumImgAtual)
                        print("cont = "+ str(cont))
                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                r = str(matriz[aux4][y][x][4])
                                g = str(matriz[aux4][y][x][5])
                                b = str(matriz[aux4][y][x][6])
                                intensity = int(r) + int(int(g) * int(256)) + int(int(b) * int(256) * int(256))

                                #pixel utilizado para acompanhar o codigo
                                pixel = formatacao.pixelDAT(x,y,z,intensity,r,g,b)

                                rgb = formatacao.rgbVTK(r,g,b)
                                meuArquivo.write(rgb)


                        cont += 1
                        print("cont = ",cont)
                        
                    print(pixel)  #linha para avaliar um pixel de cada imagem e vê o que está acontecendo com os resultados
            
            case "M"|"m":

                print("vtk - metodo Media")

                NumImgfinal = (NumImgTotal.get() + int(plan_entre_img.get())*(NumImgTotal.get()-1)) #Fórmula que calcula o número total de imagens, considerando imagens originais e imagens adicionadas
                linhas, colunas,cores = img.shape
                tamanho = linhas*colunas*NumImgfinal #É o número total de pixels trabalhados
                med = False #Variável que decide se é uma imagem média ou não, False = original e True = média
                cont = 0 #Variavel que conta quantas imagens interpoladas foram criadas
                cont2 = 0 #auxilia na hora de escrever as coordenadas no .vtk; faz om que a informacao de 3 pixel ocupem uma linha e depois pule para a proxima
                aux3 = 0 #variavel auxiliar que guarda o número da ultima imagem original e é utilizada no lugar do z pois z e o contador de imagens totais utilizado no for (nao posso ficar alterando ele). Enquanto isso, aux3 eu posso alterar sem possivelmente interferir no loop
                n = plan_entre_img.get() + 1 #n é o número de imagens interpoladas acrecido de 1, pois conta o "pulo" da imagem original para a primeira imagem criada, assim por diante, até chegar no último pulo que seria para a próxima imagem original. Esse acrescimo se dá para que haja o último pulo necessário para chegar na próxima imagem original

                print("Processando imagem...")

                print("tamanho = " + str (tamanho))

                meuArquivo = open(str("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get()),"w")

                #Cabecalho Paraview
                meuArquivo.write(str(formatacao.cabecalhoVTK(tamanho)))
                
                for z in range(0,NumImgfinal,1):
                    for y in range(0,linhas,1):
                        for x in range(0,colunas,1):
                            meuArquivo.write(str(x) +"\t"+ str(y) + "\t"+ str(z) + "\t")

                            if (cont2 % 3 == 2):
                                meuArquivo.write("\n")
                                
                            cont2 += 1
                
                meuArquivo.write(str(formatacao.cabecalhoVTK2()))

                meuArquivo.write(str(formatacao.cabecalhoVTK3(tamanho)))

                cont2 = 0
                for i in range(0,tamanho,1):
                    #retirado direto do TCC da ana beatriz
                    #Escreve coordenadas (x, y, z)
                    meuArquivo.write(str(i) + "\t")

                    #Pula linha ap�s escrever 9 d�gitos
                    if (cont2 % 3 == 2):
                        meuArquivo.write("\n")
                    cont2 += 1

                meuArquivo.write(str(formatacao.cabecalhoVTK4(tamanho)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())

                for z in range(0,NumImgfinal,1):
                    print("\nimagem "+ str(z))
                    print("ultima imagem original = " + str(aux3))

                    if not(z == NumImgfinal-1) and z!=0: #Este if verifica se estamos na última imagem ou se estamos na primeira, se um desses casos é verdadeiro não é necessário fazer a imagem interpolada
                        NumImgAnterior = str(aux3-1)

                    if cont == int(plan_entre_img.get()): #Este if identifica se o número de imagens interpoladas foi atingido, se sim ele reinicia o contador e torna a med false para que o procedimento (criar imagem original e em seguida criar n imagens interpoladas) seja repedito
                        med = False
                        cont = 0
                        
                    if med == False: #Imagem original
                        print("img = Original")
                        print("Img anterior = " + NumImgAnterior)
                        print("Img atual = " + NumImgAtual)
                        print("cont = "+ str(cont))

                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):
                                pixel = formatacao.pixelDAT(
                                 matriz[aux3][y][x][0]
                                ,matriz[aux3][y][x][1]
                                ,z
                                ,matriz[aux3][y][x][3]
                                ,matriz[aux3][y][x][4]
                                ,matriz[aux3][y][x][5]
                                ,matriz[aux3][y][x][6])

                                r = str(matriz[aux3][y][x][4])
                                g = str(matriz[aux3][y][x][5])
                                b = str(matriz[aux3][y][x][6])

                                rgb = formatacao.rgbVTK(r,g,b)
                                meuArquivo.write(rgb)

                        med = True #Essa variável sempre muda para que as proximas imagens interpoladas sejam iniciadas
                        aux3 +=1
                        print("cont = ",cont)


                    else: #Imagem média
                        print("img = Criada")
                        print("Img anterior = " + NumImgAnterior)
                        print("Img atual = " + NumImgAtual)
                        print("cont = "+ str(cont))
                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):
                                
                                #Pega informações da imagem original
                                r = int(matriz[aux3][y][x][4])
                                g = int(matriz[aux3][y][x][5])
                                b = int(matriz[aux3][y][x][6])
                                #Pega informações da imagem original anterior
                                r2 = int(matriz[aux3-1][y][x][4])
                                g2 = int(matriz[aux3-1][y][x][5])
                                b2 = int(matriz[aux3-1][y][x][6])
                                
                                #Conta que produz os valores medios das imagens interpoladas
                                bM = b2 + ((((b-b2)/int(n)))*(cont+1))
                                gM = g2 + ((((g-g2)/int(n)))*(cont+1))
                                rM = r2 + ((((r-r2)/int(n)))*(cont+1))

                                #(b-b2)/n é a variacaodas de duas imagens originais para o multiplo da quantidade de imagens interpoladas
                                #a formula para a cor media possui cont+1 pois ele inicia no zero, logo atrasaria a contagem e a primeira imagem interpolada seria igual a imagem original anterior.

                                intensityM = int(rM) + int(int(gM) * int(256)) + int(int(bM) * int(256) * int(256))

                                #Organiza e imprime as informações
                                pixel = formatacao.pixelDAT(x,y,z,intensityM,int(rM),int(gM),int(bM))
                                #int() nesse caso e utilizado para arredondar o numero da mesma forma que é feito no TCC da ana beatriz
                                
                                rgb = formatacao.rgbVTK(r,g,b)
                                meuArquivo.write(rgb)


                        cont += 1
                        print("cont = ",cont)
                        
                    print(pixel)  #linha para avaliar um pixel de cada imagem e vê o que está acontecendo com os resultados
            
            case "I"|"i": #Ainda à produzir
                print("\nXXXXXXXXXXXXXXXXX Ainda em desenvolvimento XXXXXXXXXXXXXXXXX\n")


    elif tipo_arq_saida.get() == ".dat":
        
        match metodo_.get():
            case "O"|"o": #Caso Original
                
                print("Dat - metodo Original")

                linhas, colunas,cores = img.shape #obtém as dimensões vertical e horizontal, e "cores" recebe 3 pois é a quantidade de cores das imagens

                print("Processando imagem...")
                
                meuArquivo = open("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get(),"w")

                #Cabeçalho Tecplot 360
                meuArquivo.write(str(formatacao.cabecalhoDAT(colunas,linhas,NumImgTotal.get())))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())
                #print(matriz[0][0][150])

                for z in range(0,NumImgTotal.get(),1):
                    for y in range(0,linhas,1):
                        for x in range(0,colunas,1):
                            meuArquivo.write(formatacao.pixelDAT(
                             matriz[z][y][x][0]
                            ,matriz[z][y][x][1]
                            ,matriz[z][y][x][2]
                            ,matriz[z][y][x][3]
                            ,matriz[z][y][x][4]
                            ,matriz[z][y][x][5]
                            ,matriz[z][y][x][6]))
                    #print(matriz[z][y][x])
                print("img "+str(z))            
                #meuArquivo.write(str(matriz))

                meuArquivo.close()
                
            case "V"|"v": #Caso com vazios entre as imagens

                print("Dat - metodo Vazios")

                NumImgfinal = (NumImgTotal.get() + int(plan_entre_img.get())*(NumImgTotal.get()-1)) #Fórmula que calcula o número total de imagens, considerando imagens originais e imagens adicionadas
                linhas, colunas, cores = img.shape
                tamanho = linhas*colunas*NumImgfinal
                vazio = False #Variável que decide se é uma imagem média ou não, False = original e True = média
                cont = 0 #Variavel que conta quantas imagens interpoladas foram criadas
                aux3 = 0 #variavel auxiliar que guarda o número da ultima imagem original e é utilizada no lugar do z pois z e o contador de imagens totais utilizado no for (nao posso ficar alterando ele). Enquanto isso, aux3 eu posso alterar sem possivelmente interferir no loop

                print("Processando imagem...")
                print("tamanho = "+ str (tamanho))
                meuArquivo = open(str("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get()),"w")

                #Cabeçalho Tecplot 360
                meuArquivo.write(str(formatacao.cabecalhoDAT(colunas,linhas,NumImgfinal)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())

                for z in range(0,NumImgfinal,1):
                    print("\nimagem "+ str(z))
                    print("ultima imagem original = " + str(aux3))

                    filename = Endereco_Img.get() + name.get() + str(aux3) + ext.get()
                    img = np.array(cv2.imread(filename))


                    filename2 = ""
                    if not(z == NumImgfinal-1) and z!=0: #Este if verifica se estamos na última imagem ou se estamos na primeira, se um desses casos é verdadeiro não é necessário fazer a imagem interpolada
                        filename2 = Endereco_Img.get() + name.get() + str(aux3-1) + ext.get()
                        img2 = np.array(cv2.imread(filename2))
                        #print("img2 = " + filename2)

                    if cont == int(plan_entre_img.get()): #Este if identifica se o número de imagens interpoladas foi atingido, se sim ele reinicia o contador e torna a vazio false para que o procedimento (criar imagem original e em seguida criar n imagens interpoladas) seja repedito
                        vazio = False
                        cont = 0
                        
                    if vazio == False: #Imagem original
                        print("img = Original")
                        print("cont = "+ str(cont))


                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                pixel = formatacao.pixelDAT(
                                 matriz[aux3][y][x][0]
                                ,matriz[aux3][y][x][1]
                                ,matriz[aux3][y][x][2]
                                ,matriz[aux3][y][x][3]
                                ,matriz[aux3][y][x][4]
                                ,matriz[aux3][y][x][5]
                                ,matriz[aux3][y][x][6])
                                meuArquivo.write(pixel)
                                
                        vazio = True #Essa variável sempre muda para que as proximas imagens interpoladas sejam iniciadas
                        aux3 +=1
                        print("cont = ",cont)


                    else: #Imagem vazia
                        print("img = Criada")
                        print("cont = "+ str(cont))
                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):
                                
                                pixel = formatacao.pixelDAT(x,y,z,0,int(0),int(0),int(0))
                                
                                meuArquivo.write(pixel)

                        cont += 1
                        print("cont = ",cont)
                        
                    print(pixel)  #linha para avaliar um pixel de cada imagem e vê o que está acontecendo com os resultados
            
                meuArquivo.close()

            case "R"|"r": #Caso com imagens repetidas inseridas entre as originais 
                
                print("Dat - metodo Repeticao")

                NumImgfinal = (NumImgTotal.get() + int(plan_entre_img.get())*(NumImgTotal.get()-1)) #Fórmula que calcula o número total de imagens, considerando imagens originais e imagens adicionadas
                linhas, colunas,cores = img.shape
                tamanho = linhas*colunas*NumImgfinal
                Repet = False #Variável que decide se é uma imagem média ou não, False = original e True = média
                cont = 0 #Variavel que conta quantas imagens interpoladas foram criadas
                aux3 = 0 #variavel auxiliar que guarda o número da ultima imagem original e é utilizada no lugar do z pois z e o contador de imagens totais utilizado no for (nao posso ficar alterando ele). Enquanto isso, aux3 eu posso alterar sem possivelmente interferir no loop
                #Apos implementacao de classes a variavel "aux3" serve apenas para acompanhar o programa pelo terminal
                aux4 = 0 #Variavel para auxiliar no acesso na matriz da imagem correta, utilizado apenas ao produzir imagem repetida

                print("Processando imagem...")
                print("tamanho = "+ str (tamanho))
                meuArquivo = open(str("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get()),"w")


                #Cabeçalho Tecplot 360
                meuArquivo.write(str(formatacao.cabecalhoDAT(colunas,linhas,NumImgfinal)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())

                for z in range(0,NumImgfinal,1):
                    print("\nimagem "+ str(z))
                    print("ultima imagem original = " + str(aux3))

                    filename = Endereco_Img.get() + name.get() + str(aux3) + ext.get()

                    filename2 = ""

                    if not(z == NumImgfinal-1) and z!=0: #Este if verifica se estamos na última imagem ou se estamos na primeira, se um desses casos é verdadeiro não é necessário fazer a imagem interpolada
                        aux4 = aux3-1
                        filename2 = Endereco_Img.get() + name.get() + str(aux3-1) + ext.get()

                    if cont == int(plan_entre_img.get()): #Este if identifica se o número de imagens interpoladas foi atingido, se sim ele reinicia o contador e torna a Repet false para que o procedimento (criar imagem original e em seguida criar n imagens interpoladas) seja repedito
                        Repet = False
                        cont = 0
                        
                    
                    if Repet == False: #Imagem original
                        print("img = Original")
                        print("filename1 = " + filename)
                        print("filename2 = " + filename2)

                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                pixel = formatacao.pixelDAT(
                                 matriz[aux3][y][x][0]
                                ,matriz[aux3][y][x][1]
                                ,matriz[aux3][y][x][2]
                                ,matriz[aux3][y][x][3]
                                ,matriz[aux3][y][x][4]
                                ,matriz[aux3][y][x][5]
                                ,matriz[aux3][y][x][6])

                                meuArquivo.write(pixel)
                                
                        Repet = True #Essa variável sempre muda para que as proximas imagens interpoladas sejam iniciadas
                        aux3 +=1
                        print("cont = ",cont)


                    else: #Imagem repetida
                        print("img = Criada")
                        print("filename1 = " + filename)
                        print("filename2 = " + filename2)
                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                '''b = str(img2[y,x][0])
                                g = str(img2[y,x][1])
                                r = str(img2[y,x][2])
                                intensity = int(r) + int(int(g) * int(256)) + int(int(b) * int(256) * int(256))

                                pixel = formatacao.pixelDAT(x,y,z,intensity,r,g,b)
                                meuArquivo.write(pixel)'''

                                pixel = formatacao.pixelDAT(
                                 matriz[aux4][y][x][0]
                                ,matriz[aux4][y][x][1]
                                ,matriz[aux4][y][x][2]
                                ,matriz[aux4][y][x][3]
                                ,matriz[aux4][y][x][4]
                                ,matriz[aux4][y][x][5]
                                ,matriz[aux4][y][x][6])

                                meuArquivo.write(pixel)
                                

                        cont += 1
                        print("cont = ",cont)
                        
                    print(pixel)  #linha para avaliar um pixel de cada imagem e vê o que está acontecendo com os resultados
            
                meuArquivo.close()

            case "M"|"m": #Caso com imagens que são imagens médias entre a anterior e a posterior

                print("Dat - metodo Media")

                NumImgfinal = (NumImgTotal.get() + int(plan_entre_img.get())*(NumImgTotal.get()-1)) #Fórmula que calcula o número total de imagens, considerando imagens originais e imagens adicionadas
                linhas, colunas,cores = img.shape
                tamanho = linhas*colunas*NumImgfinal
                med = False #Variável que decide se é uma imagem média ou não, False = original e True = média
                cont = 0 #Variavel que conta quantas imagens interpoladas foram criadas
                aux3 = 0 #variavel auxiliar que guarda o número da ultima imagem original e é utilizada no lugar do z pois z e o contador de imagens totais utilizado no for (nao posso ficar alterando ele). Enquanto isso, aux3 eu posso alterar sem possivelmente interferir no loop
                aux4 = 0 #Variavel para auxiliar no acesso na matriz da imagem correta, utilizado apenas ao produzir imagem repetida
                n = plan_entre_img.get() + 1 #n é o número de imagens interpoladas acrecido de 1, pois conta o "pulo" da imagem original para a primeira imagem criada, assim por diante, até chegar no último pulo que seria para a próxima imagem original. Esse acrescimo se dá para que haja o último pulo necessário para chegar na próxima imagem original

                print("Processando imagem...")
                print("tamanho = "+ str (tamanho))
                meuArquivo = open(str("Exportacao/"+nome_arq_saida.get()+tipo_arq_saida.get()),"w")


                #Cabeçalho Tecplot 360
                meuArquivo.write(str(formatacao.cabecalhoDAT(colunas,linhas,NumImgfinal)))

                matriz = Class.read.read(NumImgTotal.get(),Endereco_Img.get(),name.get(),ext.get())

                NumImgAtual = "0"
                NumImgAnterior = "0"
                
                for z in range(0,NumImgfinal,1):
                    print("\nimagem "+ str(z))
                    print("ultima imagem original = " + str(aux3))
                    
                    NumImgAtual = str(aux3)
                    if not(z == NumImgfinal-1) and z!=0: #Este if verifica se estamos na última imagem ou se estamos na primeira, se um desses casos é verdadeiro não é necessário fazer a imagem interpolada
                        
                        NumImgAnterior = str(aux3-1)

                    if cont == int(plan_entre_img.get()): #Este if identifica se o número de imagens interpoladas foi atingido, se sim ele reinicia o contador e torna a med false para que o procedimento (criar imagem original e em seguida criar n imagens interpoladas) seja repedito
                        med = False
                        cont = 0
                        
                    
                    if med == False: #Imagem original
                        print("img = Original")
                        print("Img anterior = " + NumImgAnterior)
                        print("Img atual = " + NumImgAtual)
                        print("cont = "+ str(cont))

                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):

                                pixel = formatacao.pixelDAT(
                                 matriz[aux3][y][x][0]
                                ,matriz[aux3][y][x][1]
                                ,z
                                ,matriz[aux3][y][x][3]
                                ,matriz[aux3][y][x][4]
                                ,matriz[aux3][y][x][5]
                                ,matriz[aux3][y][x][6])

                                meuArquivo.write(pixel)
                                
                        med = True #Essa variável sempre muda para que as proximas imagens interpoladas sejam iniciadas
                        aux3 +=1
                        print("cont = ",cont)


                    else: #Imagem média
                        print("img = Criada")
                        print("Img anterior = " + NumImgAnterior)
                        print("Img atual = " + NumImgAtual)
                        print("cont = "+ str(cont))
                        
                        for y in range(0,linhas,1):
                            
                            for x in range(0,colunas,1):
                                
                                #Pega informações da imagem original
                                b = int(matriz[aux3][y][x][6])
                                g = int(matriz[aux3][y][x][5])
                                r = int(matriz[aux3][y][x][4])
                                #Pega informações da imagem original anterior
                                b2 = int(matriz[aux3-1][y][x][6])
                                g2 = int(matriz[aux3-1][y][x][5])
                                r2 = int(matriz[aux3-1][y][x][4])
                                
                                #Conta que produz os valores medios das imagens interpoladas
                                bM = b2 + ((((b-b2)/int(n)))*(cont+1))
                                gM = g2 + ((((g-g2)/int(n)))*(cont+1))
                                rM = r2 + ((((r-r2)/int(n)))*(cont+1))

                                #(b-b2)/n é a média das duas imagens originais para o multiplo da quantidade de imagens interpoladas
                                #((((b-b2)/int(n)))*(cont+1)) é a variação da imagem original para a próxima imagem (interpolada por média)
                                #a formula para a cor media possui cont+1 pois ele inicia no zero, logo atrasaria a contagem e a primeira imagem interpolada seria igual a imagem original anterior.

                                intensityM = int(rM) + int(int(gM) * int(256)) + int(int(bM) * int(256) * int(256))

                                #Organiza e imprime as informações
                                pixel = formatacao.pixelDAT(x,y,z,intensityM,int(rM),int(gM),int(bM))
                                #int() nesse caso e utilizado para arredondar o numero da mesma forma que é feito no TCC da ana beatriz
                                meuArquivo.write(pixel)


                        cont += 1
                        print("cont = ",cont)
                        
                    print(pixel) #linha para avaliar um pixel de cada imagem e vê o que está acontecendo com os resultados
            
                meuArquivo.close()


            case "I"|"i": #Ainda à produzir
                print("\nXXXXXXXXXXXXXXXXX Ainda em desenvolvimento XXXXXXXXXXXXXXXXX\n")

    fim = time.time()

    print("Imagem processada!")
    print(nome_arq_saida.get()+tipo_arq_saida.get()+" pronto")
    tempo_total = fim - inicio
    print("tempo total=",tempo_total)
    


#botões
b_1 = Button( # Botao que ao pressionado, executa o programa e exporta o arquivo de imagem RGB
             janela,
             text= "Executar",font='Calibri 16 bold',
             width=10,height=1,background="green", 
             command=executar
             )
b_1.place(x=482,y=350)

turn_off = Button( # Botao de sair do programa
                  janela, 
                  text="EXIT",font='Calibri 16 bold',
                  width=10,height=1,background="red", 
                  command=janela.quit
                  )
turn_off.place(x=0,y=350)


janela.mainloop()