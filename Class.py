from  Modulos import*
class read():

    def read(num_imgs,endereco,nome,exten,):
        
        #Desenvolvido utilizando o link: https://www.geeksforgeeks.org/python-creating-3d-list/

        mat = []

        for z in range(0,num_imgs,1):
            vet = []

            filename = endereco + nome + str(z) + exten
            img = np.array(cv2.imread(filename))

            for y in range(0,img.shape[0],1):
                pixel = []
                for x in range(0,img.shape[1],1):

                    b = str(img[y,x][0])
                    g = str(img[y,x][1])
                    r = str(img[y,x][2])
                    intensity = int(r) + int(int(g) * int(256)) + int(int(b) * int(256) * int(256))

                    pixel.append([x,y,z,intensity,r,g,b])

                vet.append(pixel)
                #print(pixel)

            print("img "+str(z)+" lida")

            if y == img.shape[0] -1: #ligada a linha 16, efetuado para formatacao
                mat.append(vet)

        #print(mat[0][0][0][0]) #z,y,x,info

        '''Teste com numpy, funciona relativamente parescido
        print('\n space \n')
        mat2 = np.array(mat)
        print(mat2[1,10,20])
        '''
        return mat