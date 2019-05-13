from random import random, randint, sample
import matplotlib.pyplot as plt
import pprint

pp = pprint.PrettyPrinter()
        

class Individuo():
    
    def __init__(self, tamanho_cromossomo, valor_objetivo, geracao = 0):        
        self.tamanho_cromossomo = tamanho_cromossomo
        self.nota_avaliacao = 0
        self.cromossomo = []
        self.valor_objetivo = valor_objetivo
        self.geracao = geracao
        
        self.geraCromossomo()        
        
    def __repr__(self):
        return ('Cromo: %s Fitness: %s' % (self.cromossomo, self.nota_avaliacao))
    
    def geraCromossomo(self):    
        ''' Gerando o cromossomo '''
        cromo = []
        for i in range(self.tamanho_cromossomo):
            if random() < 0.5:
                cromo.append(0)
            else:
                cromo.append(1)
                
        self.cromossomo = cromo 

    def converteDecimal(self, value):
        bi = ''
        for i in value:
            bi = bi+(str(i))        
        return int(bi,2)
        
    def avaliacao(self):
        var = self.getValoresFuncao()
        x = var[0]
        y = var[1]
        w = var[2]

        r = (2*x) + (pow(y,2)) + w       
        r = abs(r - self.valor_objetivo)
                
        self.nota_avaliacao = r
        
    def getValoresFuncao(self):
        x = self.converteDecimal(self.cromossomo[0:3])
        y = self.converteDecimal(self.cromossomo[3:6])
        w = self.converteDecimal(self.cromossomo[6:9])
        
        return [x,y,w]
    
    def crossover(self, outro):
        corte = randint(1, len(self.cromossomo)-1)             
        
      
        cross1 = self.cromossomo[0:corte] + outro.cromossomo[corte::]                
        
        newFilhos = Individuo(self.tamanho_cromossomo, self.valor_objetivo, self.geracao+1)
        
        newFilhos.cromossomo = cross1
        return newFilhos
    
    def mutacao(self, taxa):
        ''' Aqui percorro cada gene do cromossomo, quando o valor randomico
        for maior que a taxa que eu estipulei, eu inverto o gene   '''
        for i in range(len(self.cromossomo)):
            if random() < taxa:
                if self.cromossomo[i] == 0:
                    self.cromossomo[i] = 1
                else:
                    self.cromossomo[i] = 0
        return self
            
    
class SuperAG():

    def __init__(self, tamanho_populacao, taxa_mutacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.melhorSolucaoEncontrada = None
        self.historicoMelhores = []
        self.taxa_mutacao = taxa_mutacao
        self.historicoMedia = []
        self.somaMedia = 0.0
        
        
    def inicializaPopulacao(self, tamanho_cromossomo, valor_objetivo):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(tamanho_cromossomo, valor_objetivo))
            
    def avaliaPopuplacao(self):
        for i in self.populacao:
            i.avaliacao()
            
    def aplicaMutacao(self):
        for i in self.populacao:
            i.mutacao(self.taxa_mutacao)            
    
    def ordernaPopulacao(self):
        self.populacao.sort(key=lambda p: p.nota_avaliacao)    
        
    def roletaViciada(self):        
        somaAvaliacao = 0
        
        ''' Sabendo o total da avaliação da população '''
        for i in range(len(self.populacao)):
            somaAvaliacao += self.populacao[i].nota_avaliacao        

        ''' Definindo uma lista de proporção conforme cada fitness.
            A divisão por 1, server para inverter o menor fitness como
            sendo o maior '''            
        roleta = []
        for i in self.populacao:
            roleta.append([(1 / (i.nota_avaliacao / somaAvaliacao)), i])            
             
        ''' Aplicando a tecnica Windowing '''
        roleta.sort(key=lambda x: x[0])
        menorValor = int(roleta[0][0])
        
        for i in roleta:
            i[0] = i[0] - menorValor        
            
        roleta.sort(key=lambda x: x[0], reverse=True)        
        
        ponteiro = 1/somaAvaliacao         
        i = 0
        soma = 0       
            
        for i in range(len(roleta)):
            if soma < ponteiro:                
                break
            else:
                soma = soma + roleta[i][0]
                            
        return roleta[i][1]        
        
   
    def mostraPopulacao(self):
        for i in self.populacao:
            print('Cromossomo: %s', i.cromossomo)
            print('Nota      : %s', i.nota_avaliacao)

    
    def chegouObjetivo(self, objetivo):
        obj = None
        for i in self.populacao:
            if (i.nota_avaliacao + 52) == objetivo:
                obj = i
                break
        return obj
    
    def melhorSolucao(self, solucao):
        self.historicoMelhores.append(solucao.nota_avaliacao)
        if self.melhorSolucaoEncontrada == None:
            self.melhorSolucaoEncontrada = solucao
        elif solucao.nota_avaliacao < self.melhorSolucaoEncontrada.nota_avaliacao:
            self.melhorSolucaoEncontrada = solucao
        
    def setHistoricoMedia(self, solucao):
        if self.somaMedia == 0:
            self.somaMedia = solucao.nota_avaliacao
            self.historicoMedia.append(solucao.nota_avaliacao)
        else:
            self.somaMedia = self.somaMedia + solucao.nota_avaliacao        
            self.historicoMedia.append(self.somaMedia / (len(self.historicoMedia)+1))
        
        
        
    def run(self, numero_geracao, tamanho_cromossomo, valor_objetivo, taxa_mutacao):
        
        ''' Inicializando a primeira população, avaliando, ordenando '''
        self.inicializaPopulacao(tamanho_cromossomo, valor_objetivo)              
        self.avaliaPopuplacao()        
        self.ordernaPopulacao()      
        
        ''' Setando a primeira melhor avaliação '''
        self.melhorSolucao(self.populacao[0])
        
        
        ''' Checando se na primeira avaliação já se chegou no objetivo '''
        if self.chegouObjetivo(objetivo) == None:        
            print('****** POPULAÇÃO INICIAL ****** ')
            self.mostraPopulacao()
            
            ''' Este FOR é para interar as gerações '''
            for i in range(numero_geracao):
                novaPopulacao = []                
                
                '''Este for é para fazer o ciclo dos 
                   Operadores genéticos SELEÇÃO e CROSSOVER '''
                for individuo in range(self.tamanho_populacao):
                    
                    ''' Roleta. Selecionando 2 individuos para crossover '''                
                    individuoSelecionado1 = self.roletaViciada()                
                    individuoSelecionado2 = self.roletaViciada()
                    
                    ''' Aplicando crossover '''
                    filho = individuoSelecionado1.crossover(individuoSelecionado2)                
                  
                    novaPopulacao.append(filho)                
                
                ''' Trocando a populacção '''
                self.populacao = list(novaPopulacao)
                
                ''' Mutação na nova população '''
                self.aplicaMutacao()
                
                ''' Avaliando e ordenando '''
                self.avaliaPopuplacao()
                self.ordernaPopulacao()
                
                ''' Critério de parada. Se achou a solução então para '''
                self.melhorSolucao(self.populacao[0])
                self.setHistoricoMedia(self.populacao[0])
                if self.chegouObjetivo(objetivo) != None:                
                    break            
        
        print('****** POPULAÇÃO FINAL ****** ')
        self.mostraPopulacao()        
        
        print('\nMelhor solução foi na geração %s, com fitness %s e cromossomo %s' %
              (self.melhorSolucaoEncontrada.geracao, 
              self.melhorSolucaoEncontrada.nota_avaliacao,
              self.melhorSolucaoEncontrada.cromossomo))
        
        print('Expressão: (2 * %s) + (%s**2) + %s = %s' % 
              (self.melhorSolucaoEncontrada.getValoresFuncao()[0], 
               self.melhorSolucaoEncontrada.getValoresFuncao()[1],
               self.melhorSolucaoEncontrada.getValoresFuncao()[2],
               self.melhorSolucaoEncontrada.nota_avaliacao+52))
        
        
        self.historicoMelhores.sort(reverse=True)
        self.historicoMedia.sort(reverse=True)
        plt.plot(self.historicoMelhores, 'r', label='Melhor')        
        plt.plot(self.historicoMedia, 'g', label='Média')        
        plt.legend()
        plt.title("Convegência das gerações")
        
        plt.xlabel('Geração')
        plt.ylabel('Valor da função de avaliação (0 = Ótimo')
        plt.show()
        
        
     
if __name__ == '__main__':        
    
    populacao = 10
    repeticoes = 100
    tamanho_cromo = 9
    objetivo = 52
    taxa_mutacao = 0.01
    
    ag = SuperAG(populacao, taxa_mutacao)
    ag.run(repeticoes, tamanho_cromo, objetivo, taxa_mutacao)
    

