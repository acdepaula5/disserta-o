

#classe para formatação de arquivos

#Cabecalho Paraview===================================================
def cabecalhoVTK(tamanho):
    cabecalho = ("# vtk DataFile Version 1.0\n"+
                    "Cube example\n"+
                    "ASCII\n\n"+
                    "DATASET POLYDATA\n"+
                    "POINTS " +str(tamanho) +" int\n")
    return cabecalho

def cabecalhoVTK2():
    cabecalho = ("POLYGONS 6 30\n"
    + "4 0 1 2 3 \n"
    + "4 4 5 6 7 \n"
    + "4 0 1 5 4 \n"
    + "4 2 3 7 6 \n"
    + "4 0 4 7 3 \n"
    + "4 1 2 6 5 \n")
    return cabecalho

def cabecalhoVTK3(tamanho):
    cabecalho = ("\nPOINT_DATA " + str(tamanho) + "\n"
                    + "SCALARS my_scalars int\n"
                    + "LOOKUP_TABLE custom_table\n")
    return cabecalho

def cabecalhoVTK4(tamanho):
    cabecalho = "\nLOOKUP_TABLE custom_table " + str(tamanho) + "\n"
    return cabecalho

def rgbVTK(r,g,b):
    def fun_aux(var):
        aux_var = str(round(int(var)/255.0,6))
        return aux_var
    newR = fun_aux(r)
    newG = fun_aux(g)
    newB = fun_aux(b)

    rgb = newR + " " + newG + " " + newB + " " + str(1) + "\n"

    return rgb

#Cabecalho Tecplot=====================================================
def cabecalhoDAT(i,j,k): 
    """Imprime no arquivo cabecalho inicial para o Tecplot"""
    #Cabeçalho Tecplot 360
    cabecalho = (
        "Title = \"ImagePorcess\"\n"+
        "variables= \"X\", \"Y\", \"Z\", \"Intensity\", \"Red\",  \"Green\", \"Blue\""+
        "\nzone\n"+
        "T=\" \"" + ",   " + "I=" + str(i) + ",   " + "J=" + str(j) + ",   " + "K=" + str(k) + ",   " + "F=point\n\n")
    return cabecalho

def pixelDAT(x,y,z,intensidade,r,g,b):
    """Imprime no arquivo os dados na formatação do Tecplot"""
    coordenadas = str(x) +"\t"+ str(y) + "\t"+ str(z)

    rgb = ((alinhamento(str(r))) + " " + alinhamento(str(g)) + " " + alinhamento(str(b)))

    pixel = (str(coordenadas) + " " + str(intensidade) + " " + str(rgb)+"\n")
    return pixel



#Formatacoes diversas==================================================

def alinhamento(var): #Faz com que os valores com casas decimais dicimais diferentes mantenham o alinhamento ex: 1, 10, 100
        if len(var)==3:
            return str(""+var[0:3])
        elif len(var)==2:
            return str(" "+var[0:2])
        elif len(var)==1:
            return str("  "+var[0:1])
        
def alinhamento2(var): #Faz com que os valores com casas decimais dicimais diferentes mantenham o alinhamento ex: 1, 10, 100, 1000, 10000, 100000
        if len(var)==6:
            return str(" "+var[0:6])
        elif len(var)==5:
            return str("  "+var[0:5])
        elif len(var)==4:
            return str("   "+var[0:4])
        elif len(var)==3:
            return str("    "+var[0:3])
        elif len(var)==2:
            return str("     "+var[0:2])
        elif len(var)==1:
            return str("      "+var[0:1])

