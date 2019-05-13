from random import random, randint, sample, uniform
import matplotlib.pyplot as plt
        

class Individuo():
    
    def __init__(self, tamanho_cromossomo, qtdeDimensoes, valor_objetivo, geracao = 0):        
        self.tamanho_cromossomo = tamanho_cromossomo
        self.nota_avaliacao = 0
        self.cromossomo = []
        self.valor_objetivo = valor_objetivo
        self.geracao = geracao
        self.qtdeDimensoes = qtdeDimensoes
        
        self.geraCromossomo()        
    
    def geraCromossomo(self):    
        ''' Gerando o cromossomo '''
        cromo = []
        for i in range(self.tamanho_cromossomo):
            cromo.append(uniform(5.12, -5.12))
                
        self.cromossomo = cromo               
        
    def dejong(self, dimensoes):
        v = 0
        valor = 0
        for x in dimensoes:
            v = pow(x, 2)
            valor = valor + v
        return valor
            
    def avaliacao(self):
        dejongvalue = self.dejong(self.cromossomo)
        self.nota_avaliacao = 1 / (dejongvalue + 1)
        return self.nota_avaliacao
    
    def crossover(self, outro):
        corte = randint(1, len(self.cromossomo)-1)       
      
        cross1 = self.cromossomo[0:corte] + outro.cromossomo[corte::]                
        
        newFilhos = Individuo(self.tamanho_cromossomo, self.qtdeDimensoes, self.valor_objetivo, self.geracao+1)
        
        newFilhos.cromossomo = cross1
        return newFilhos
    
    def mutacao(self, taxa):
        ''' Aqui percorro cada gene do cromossomo, quando o valor randomico
        for maior que a taxa que eu estipulei, eu inverto o gene   '''
        for i in range(len(self.cromossomo)):
            if random() < taxa:                
                self.cromossomo[i] = uniform(-5.12, 5.12)
                
        return self
            
    
class SuperAG():

    def __init__(self, tamanho_populacao, dimensoes, taxa_mutacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.melhorSolucaoEncontrada = None
        self.historicoMelhores = []
        self.taxa_mutacao = taxa_mutacao
        self.dimensoes = dimensoes
        self.historicoMedia = []
        self.somaMedia = 0.0
        
        
    def inicializaPopulacao(self, tamanho_cromossomo, valor_objetivo):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(tamanho_cromossomo, dimensoes, valor_objetivo))
            
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

        ''' Definindo uma lista de proporção conforme cada fitness '''            
        roleta = []
        try:
            for i in self.populacao:
                roleta.append([(1 / (i.nota_avaliacao / somaAvaliacao)), i])            
        except:
            print('ERR0')
            print(i.nota_avaliacao)
            print(somaAvaliacao)            
            
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
            if i.nota_avaliacao  == objetivo:
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
            #print('****** POPULAÇÃO INICIAL ****** ')
            #self.mostraPopulacao()
            
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
        
        print('Expressão: f(x**2) = %s ' % self.melhorSolucaoEncontrada.nota_avaliacao)
        
        plt.plot(self.historicoMelhores, 'r', label='Melhor')        
        plt.plot(self.historicoMedia, 'g', label='Média')        
        plt.legend()
        plt.title("Convegência das gerações NÚMERO REAIS")        

        plt.show()
        
     
if __name__ == '__main__':        
    
    populacao = 100
    repeticoes = 500
    tamanho_cromo = 100
    objetivo = 0
    taxa_mutacao = 0.01
    dimensoes = 20
    
    ag = SuperAG(populacao, dimensoes, taxa_mutacao)
    ag.run(repeticoes, tamanho_cromo, objetivo, taxa_mutacao)
    
 

    