# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 01:41:48 2023

@author: alexa
"""
## RODANDO O SOFTWARE - streamlit run C:\Users\alexa\Desktop\v_SW.2.py
import streamlit as stlt
import numpy as np
from numpy import random as rd
from numpy import inf
from numpy import nan
from scipy.integrate import quad
from matplotlib import pyplot as plt
import scipy.optimize as opt
from scipy import stats as st
#from fractions import Fraction
#from decimal import Decimal
#from math import log10
#from PIL import Image

def decimal(p):
    algs = len(p)
    posicao_ponto = algs+1
    for i in range(0,algs):
        if p[i] == '.':
            posicao_ponto = i
    
    if posicao_ponto == algs+1:        
        base = str(0)
        #base = p[0]
        base = base.__add__('.')
        for i in range(0,100):
            if i <= (algs-1):
                base = base.__add__(p[i])
            else:
                base = base.__add__('0')
        expo = str(algs)
        base = base.__add__('e+')
        base = base.__add__(expo)
    elif posicao_ponto >= 1:
        base_ini = ''
        for i in range(0,posicao_ponto):
            base_ini = base_ini.__add__(p[i])
        expo = str(len(base_ini))
        base = '0.'
        base = base.__add__(base_ini)
        #base = base.__add__('.')
        for i in range(posicao_ponto+1,len(p)):
            if i <= 101:
                base = base.__add__(p[i])
        tam = len(base)
        if tam < 102:
            for i in range(0,102-tam):
                base = base.__add__('0')
        base = base.__add__('e+')
        base = base.__add__(expo)
           
    return base

def vetorizar(texto, divisor):
    tam = len(texto)
    #print(tam)
    vetor_final = []
    #print(vetor_final)
    numero = ''
    #print(numero)
    for i in range(0,tam):
        if (texto[i] == ','):
            numero_f = float(numero)
            numero = ''
            vetor_final = np.append(vetor_final, numero_f)
            #print(numero_f, vetor_final)
        elif i == tam-1:
            numero = numero.__add__(texto[i])
            numero_f = float(numero)
            vetor_final = np.append(vetor_final, numero_f)
            #print(numero_f, vetor_final)
        else:
            numero = numero.__add__(texto[i])
    
    tam_vetor = len(vetor_final)
    for i in range(0,tam_vetor):
        vetor_final[i] = vetor_final[i]/divisor
    
    return(vetor_final)

#img = Image.open("C:\\Users\\alexa\\Desktop\\FAIRlogo.jpg")
#stlt.image(img, use_column_width=True)
stlt.image("FAIRlogo.jpg")

stlt.title('Sistema de Informação')
stlt.text('')
stlt.subheader('Análise de Desempenho Relativo da Manutenção e Comparação Justa do Desempenho de Sistemas')
stlt.text('')
stlt.text('Insira as informações solicitadas nos campos abaixo ')

#stlt.text("SISTEMA 1 - Informações")

stlt.write('<font color="red" size="5"><b>SISTEMA 1 - Informações</b></font>', unsafe_allow_html=True)

stlt.text('')
id_A = stlt.text_input("Identificação do sistema (S1):")

#stlt.text("Histórico de desempenho")
stlt.write('<font color="blue" size="5"><b>Histórico de desempenho</b></font>', unsafe_allow_html=True)

A_exercicio_A = stlt.number_input("Disponibilidade no período observado (% de tempo disponível) (S1):")
A_exercicio_A = A_exercicio_A/100
#stlt.text("Coleta de dados para análise de desempenho relativo (S1)")

#stlt.text("Tempo estimado de atividades de manutenção (S1)")
stlt.write('<font color="black" size="5"><b>Tempo estimado de atividades de manutenção</b></font>', unsafe_allow_html=True)

#stlt.text("Medida de tempo:")
opcoes_tempo = ["Minuto","Hora","Dia"]
unidade_A1 = stlt.selectbox("Medida de tempo (S1):", opcoes_tempo)

if unidade_A1 == 'Minuto':
    div_A1 = 60*24
elif unidade_A1 == 'Hora':
    div_A1 = 24
else:
    div_A1 = 1


Df_A_min = stlt.number_input("Tempo médio para manutenção corretiva de falhas críticas (mínimo) (S1):")
Df_A_max = stlt.number_input("Tempo médio para manutenção corretiva de falhas críticas (máximo) (S1):")
Df_A = [Df_A_min/div_A1, Df_A_max/div_A1]

Dp_A_min = stlt.number_input("Tempo médio para manutenção preventiva geral (mínimo) (S1):")
Dp_A_max = stlt.number_input("Tempo médio para manutenção preventiva geral (máximo) (S1):")
Dp_A = [Dp_A_min/div_A1, Dp_A_max/div_A1]

Dm_A_min = stlt.number_input("Tempo médio para reparo pontual (mínimo) (S1):")
Dm_A_max = stlt.number_input("Tempo médio para reparo pontual (máximo) (S1):")
Dm_A = [Dm_A_min/div_A1, Dm_A_max/div_A1]

#stlt.text("Análise de Confiabilidade (S1)")
stlt.write('<font color="black" size="5"><b>Análise de Confiabilidade</b></font>', unsafe_allow_html=True)
n_A = stlt.text_input("Número de especialistas consultados (S1):")
if n_A == '':
    n_A = 0
else:
    n_A = int(n_A)

unidade_A12 = stlt.selectbox("Medida de tempo para análise de confiabilidade (S1)", opcoes_tempo)
if unidade_A12 == 'Minuto':
    div_A12 = 60*24
elif unidade_A12 == 'Hora':
    div_A12 = 24
else:
    div_A12 = 1

t_A = list(np.zeros(n_A))
M_inf_A = list(np.zeros(n_A))
M_sup_A = list(np.zeros(n_A))
taxa_inf_A = list(np.zeros(n_A))
taxa_sup_A = list(np.zeros(n_A))

for i in range(0,n_A):
    #stlt.text(f'Especialista {i+1}')
    stlt.write(f'<font color="blue" size="5"><b>Especialista {i+1}</b></font>', unsafe_allow_html=True)
    
    t_Ai = stlt.text_input(f"Marcos temporais de referência (S1.E{i+1}):")
    t_Ai = vetorizar(t_Ai, div_A12)
    t_A[i] = t_Ai
    
    
    p_min = stlt.text_input(f"Probabilidade acumulada de falha crítica (% mínimo) (S1.E{i+1}):")
    p_min = vetorizar(p_min, 1)
    M_inf_A[i] = p_min
    
    p_max = stlt.text_input(f"Probabilidade acumulada de falha crítica (% máximo) (S1.E{i+1}):")
    p_max = vetorizar(p_max, 1)
    M_sup_A[i] = p_max
    
    tx_min = stlt.text_input(f"Taxa de falhas menores (mínimo) (S1.E{i+1}):")
    tx_min = vetorizar(tx_min, 1)
    taxa_inf_A[i] = tx_min
    
    tx_max = stlt.text_input(f"Taxa de falhas menores (máximo) (S1.E{i+1}):")
    tx_max = vetorizar(tx_max, 1)
    taxa_sup_A[i] = tx_max

##

#stlt.text("SISTEMA 2 - Informações")
stlt.write('<font color="red" size="5"><b>SISTEMA 2 - Informações</b></font>', unsafe_allow_html=True)

stlt.text('')
id_B = stlt.text_input("Identificação do sistema (S2):")

#stlt.text("Histórico de desempenho")
stlt.write('<font color="blue" size="5"><b>Histórico de desempenho</b></font>', unsafe_allow_html=True)

A_exercicio_B = stlt.number_input("Disponibilidade no período observado (% de tempo disponível) (S2):")
A_exercicio_B = A_exercicio_B/100
#stlt.text("Coleta de dados para análise de desempenho relativo (S1)")

#stlt.text("Tempo estimado de atividades de manutenção (S2)")
stlt.write('<font color="black" size="5"><b>Tempo estimado de atividades de manutenção (S2)</b></font>', unsafe_allow_html=True)

#stlt.text("Medida de tempo:")
opcoes_tempo_2 = ["Minuto","Hora","Dia"]
unidade_B1 = stlt.selectbox("Medida de tempo (S2):", opcoes_tempo_2)

if unidade_B1 == 'Minuto':
    div_B1 = 60*24
elif unidade_A1 == 'Hora':
    div_B1 = 24
else:
    div_B1 = 1


Df_B_min = stlt.number_input("Tempo médio para manutenção corretiva de falhas críticas (mínimo) (S2):")
Df_B_max = stlt.number_input("Tempo médio para manutenção corretiva de falhas críticas (máximo) (S2):")
Df_B = [Df_B_min/div_B1, Df_B_max/div_B1]

Dp_B_min = stlt.number_input("Tempo médio para manutenção preventiva geral (mínimo) (S2):")
Dp_B_max = stlt.number_input("Tempo médio para manutenção preventiva geral (máximo) (S2):")
Dp_B = [Dp_B_min/div_B1, Dp_B_max/div_B1]

Dm_B_min = stlt.number_input("Tempo médio para reparo pontual (mínimo) (S2):")
Dm_B_max = stlt.number_input("Tempo médio para reparo pontual (máximo) (S2):")
Dm_B = [Dm_B_min/div_B1, Dm_B_max/div_B1]

#stlt.text("Análise de Confiabilidade (S2)")
stlt.write('<font color="black" size="5"><b>Análise de Confiabilidade (S2)</b></font>', unsafe_allow_html=True)

n_B = stlt.text_input("Número de especialistas consultados (S2):")
if n_B == '':
    n_B = 0
else:
    n_B = int(n_B)

unidade_B12 = stlt.selectbox("Medida de tempo para análise de confiabilidade (S2)", opcoes_tempo_2)
if unidade_B12 == 'Minuto':
    div_B12 = 60*24
elif unidade_B12 == 'Hora':
    div_B12 = 24
else:
    div_B12 = 1

t_B = list(np.zeros(n_B))
M_inf_B = list(np.zeros(n_B))
M_sup_B = list(np.zeros(n_B))
taxa_inf_B = list(np.zeros(n_B))
taxa_sup_B = list(np.zeros(n_B))

for i in range(0,n_B):
    #stlt.text(f'Especialista {i+1}')
    stlt.write(f'<font color="blue" size="5"><b>Especialista {i+1}</b></font>', unsafe_allow_html=True)
    
    t_Bi = stlt.text_input(f"Marcos temporais de referência (S2.E{i+1}):")
    t_Bi = vetorizar(t_Bi, div_B12)
    t_B[i] = t_Bi
    
    
    p_min = stlt.text_input(f"Probabilidade acumulada de falha crítica (% mínimo) (S2.E{i+1}):")
    p_min = vetorizar(p_min, 1)
    M_inf_B[i] = p_min
    
    p_max = stlt.text_input(f"Probabilidade acumulada de falha crítica (% máximo) (S2.E{i+1}):")
    p_max = vetorizar(p_max, 1)
    M_sup_B[i] = p_max
    
    tx_min = stlt.text_input(f"Taxa de falhas menores (mínimo) (S2.E{i+1}):")
    tx_min = vetorizar(tx_min, 1)
    taxa_inf_B[i] = tx_min
    
    tx_max = stlt.text_input(f"Taxa de falhas menores (máximo) (S2.E{i+1}):")
    tx_max = vetorizar(tx_max, 1)
    taxa_sup_B[i] = tx_max

#

## Coleta de dados feita, hora de fazer o tratamento dos dados
#
#
# FIM DA COLETA
#
#

#
# Definição de funções básicas
def fracionamento(X):
    if (isinstance(X, str) == True):
        X_str = X
        base = ''
        potencia = ''
        for i in range(0,102):
            base = base.__add__(X_str[i])
        for i in range(103,len(X_str)):
            print(X_str[i],'X_str')
            potencia = potencia.__add__(X_str[i])
            print(potencia,'pot')

    else:    
        X_ = str(X)
        print(X_)
        X_str = decimal(X_)
        print(X_str,'X_str')
        base = ''
        potencia = ''
        for i in range(0,102):
            base = base.__add__(X_str[i])
        for i in range(103,len(X_str)):
            print(X_str[i],'X_str')
            potencia = potencia.__add__(X_str[i])
            print(potencia,'pot')
    
    base = float(base)
    potencia = float(potencia)
    base1 = base/10
    potencia1 = potencia + 1
    return (base1,potencia1)

#    y = (np.log(X))/(np.log(10))
#   k = int(y)
#    if k >= 0:
#        w = k
#    else:
#        w = k-1
#    potencia = w+1
#    base = X*(10**-potencia)
#    return (base,potencia)

#ENTRAR AQUI A FUNÇÃO PRA DISPONIBILIDADE

#definindo a função da distribuição não homogênea de Poisson

def Pm (w, t, grau_pol, coefs_pol): 
    #vou definir a função taxa de falha antes de seguir com os condicionais de formulação
    def taxa (t, grau_pol, coefs_pol):   ##ajuste polinomial que melhor representa a evolução da taxa de falhas menores
        taxa_funcao = 0
        grau_ref = grau_pol
        local = -1
            
        for ii in range (0, grau_pol+1):
            local = local + 1
            coefs_ = coefs_pol [local]
            taxa_funcao = taxa_funcao + coefs_*(t**grau_ref)
            grau_ref = grau_ref - 1 
        return taxa_funcao    
        
    #SE - Processo Homogêneo de Poisson
        
    if (grau_pol == 0):
        # não sei qual a natureza da variável
        if (isinstance(coefs_pol, int) == True) or (isinstance(coefs_pol, float) == True):
            taxa_fixa = coefs_pol
        else:
            taxa_fixa = coefs_pol[0]
            
        p1x = taxa_fixa*t
        p2x = np.exp(-(taxa_fixa*t))
            
        if (isinstance(p1x, int) == True) or (isinstance(p1x, float) == True):
            p1x = p1x
        else:
            p1x = p1x[0]
                
        if (isinstance(p2x, int) == True) or (isinstance(p2x, float) == True):
            p2x = p2x
        else:
            p2x = p2x[0]

        #p1 = '%.100e'%Decimal(p1x)
        p1 = decimal(str(p1x))
        #p2 = '%.100e'%Decimal(p2x)
        p2 = decimal(str(p2x))
                        
        #p3 = '%.100e'%Decimal(np.math.factorial(w))
        p3 = decimal(str(np.math.factorial(w)))
            
        posi = 102
        p1_string = str(p1)
        p2_string = str(p2)
        base_p1 = str()
        base_p2 = str()
        for jj in range(0,posi):
            base_p1 = base_p1.__add__(p1_string[jj])
            base_p2 = base_p2.__add__(p2_string[jj])
        potencia_p1 = str()
        potencia_p2 = str()
        for jj in range(posi+1,len(p1_string)):
            potencia_p1 = potencia_p1.__add__(p1_string[jj])
        for jj in range(posi+1,len(p2_string)):
            potencia_p2 = potencia_p2.__add__(p2_string[jj])
            
        p3_string = str(p3)
            
        if p3_string == 'inf':
            p_final = 0
        else:
            base_p3 = str()
            potencia_p3 = str()
            for jj in range(0,posi):
                base_p3 = base_p3.__add__(p3_string[jj])
            for jj in range(posi+1,len(p3_string)):
                potencia_p3 = potencia_p3.__add__(p3_string[jj])
                
            base_p1_float = float(base_p1)
            base_p2_float = float(base_p2)
            base_p3_float = float(base_p3)
            potencia_p1_float = float(potencia_p1)
            potencia_p2_float = float(potencia_p2)
            potencia_p3_float = float(potencia_p3)
                
            base_p1_decimal = base_p1_float/10
            potencia_p1_atualizado = potencia_p1_float + 1
                
            p123 = (base_p2_float / base_p3_float) * (base_p1_decimal**w)
            exp_dez = (potencia_p1_atualizado*w) + potencia_p2_float - potencia_p3_float
                
            p_final = p123*(10**exp_dez)
            
    else:    
        integral = quad(lambda x: taxa(x,grau_pol,coefs_pol), 0, t)
            
        integral_0 = fracionamento(integral[0])
            
        p1a = integral_0[0]    # base
        p1b = integral_0[1]    # potencial da fatoração
            
        p1 = p1a**w
        #stlt.write('p1a', p1a, 'w', w, 'p1', p1)
        p2 = np.exp(-integral[0])
        p3 = np.math.factorial(w)
            
        if (p1b*w <= 300) and (p3 <= 10**300):   
            #condições para trabalhar de forma direta
            p3_fr = fracionamento(p3)
            p3_base = p3_fr[0]
            p3_expoente = p3_fr[1]
            exp_de_dez = (p1b*w) - p3_expoente
                
            p12 = (p1*p2)/p3_base
            p_final = p12*(10**exp_de_dez)
                
        else:
            #uso o artifício do uso de strings para lidar com grandes números sem Overflow errors
            p2_notacao = decimal(str(p2))
            p2_string = str(p2_notacao)
                
            if p2_string[0] == '-':
                posi = 103
            else:
                posi = 102    #posição do caracter "e"
                    
            potencia_p2 = str()
            for jj in range (posi+1, len(p2_string)):
                potencia_p2 = potencia_p2.__add__(p2_string[jj])
                    
            base_p2 = str()
            for jj in range (0,posi):
                base_p2 = base_p2.__add__(p2_string[jj])
                    
            base_p2_float = float(base_p2)
            potencia_p2_float = float(potencia_p2)
                
            p3_notacao = decimal(str(p3))
            p3_string = str(p3_notacao)
                
            if p3_string == 'inf':
                p_final = 0
            else:
                posii_ = 102
                    
                potencia_p3 = str()
                for jj in range(posii_+1,len(p3_string)):
                    potencia_p3 = potencia_p3.__add__(p3_string[jj])
                        
                base_p3 = str()
                for jj in range(0,posii_):
                    base_p3 = base_p3.__add__(p3_string[jj])
                    
                base_p3_float = float(base_p3)
                potencia_p3_float = float(potencia_p3)
                    
                novo_exp_dez = (p1b*w) + potencia_p2_float - potencia_p3_float
                    
                p12 = (p1*base_p2_float)/base_p3_float
                    
                p12_notacao = decimal(str(p12))
                p12_string = str(p12_notacao)
                    
                if p12_string[0]=='-':
                    posici = 103
                else:
                    posici = 102
                        
                potencia_p12 = str()
                for jj in range(posici+1,len(p12_string)):
                    potencia_p12 = potencia_p12.__add__(p12_string[jj])
                        
                base_p12 = str()
                for jj in range(0,posici):
                    base_p12 = base_p12.__add__(p12_string[jj])
                        
                base_p12_float = float(base_p12)
                potencia_p12_float = float(potencia_p12)
                    
                novo_novo_exp_dez = novo_exp_dez + potencia_p12_float
                    
                if (p12 == 0.0) or (p12 == -0.0):
                    p_final = 0
                else:
                    p_final = base_p12_float*(10**novo_novo_exp_dez)
                    
    return (p_final)

#
# ÍNDICE RELATIVO
#

def Res(A_exercicio, eta_, beta_, grau_pol, coefs_pol, Df_, Dp_, Dm_):
    def fx(x): #densidade de probabilidade Weibull
        # avaliando a natureza da variável de entrada
        if (isinstance(x, int) == True) or (isinstance(x, float) == True):
            y = x
        else:
            y = x[0]
        return (beta_/eta_)*((y/eta_)**(beta_-1))*np.exp(-((y/eta_)**beta_))
        
    def Rx(x): #função confiabilidade
        # avaliando a natureza da variável de entrada
        if (isinstance(x, int) == True) or (isinstance(x, float) == True):
            y = x
        else:
            y = x[0]
        return np.exp(-((y/eta_)**beta_))
        
    def Fx(x): #função probabilidade acumulada
        return 1-Rx(x)

    def EL(T): #duração esperada de um ciclo de renovação    
        e1 = quad(lambda t: ((t + Df_)*fx(t)), 0, T)   # cenário de falha
        e11 = e1[0]
        EL = e11 + (T + Dp_)*Rx(T)                     # cenário de falha + cenário de preventiva
        return EL

    def ED(T): #downtime esperado no decorrer de um ciclo de renovação
        criterio = 0
        n = -1
        valor = 0
        validador = 0

        while criterio == 0:
            n = n+1
            #stlt.write('n',n)
            integral_p = quad(lambda t: Pm(n,t,grau_pol,coefs_pol)*fx(t),0,T)
            integral_probabilidade = integral_p[0] 
                
            # acumulando o downtime esperado
            valor = valor + (n*Dm_)*((Pm(n,T,grau_pol,coefs_pol)*Rx(T)) + integral_probabilidade)
                
            # critério de convergência
            validador = validador + (Pm(n,T,grau_pol,coefs_pol)*Rx(T)) + integral_probabilidade

            if ((1-validador) < 10**-2) or ((n > 5000) and ((1-validador) < 0.05)): 
                #stlt.write('validador', validador)
                criterio = 1
                    
        ED = (Df_*Fx(T)) + (Dp_*Rx(T)) + valor
        return ED

    def DT_(T): # nível de downtime
        #print(ED(T)/EL(T))
        return (ED(T)/EL(T))

    resultado_A = opt.minimize_scalar(DT_, bounds = [0.01,2*eta_], method = 'bounded')

    fun_A = resultado_A.fun
    T_politica_base = resultado_A.x
        
    A_ref = 1 - fun_A
        
    indice_relativo = (A_exercicio-A_ref) / (1-A_ref)
        
    print('T base', T_politica_base, 'Downtime', fun_A, 'Disponibilidade', A_ref)
        
    print('Índice Relativo', indice_relativo)
        
    return (indice_relativo)

#Dados de entrada - Parâmetros de execução
percentil_referencia_pl = 95
B_grande = 1000000000000000
#num_it = 150

#
#    Amostragem de Dados    
#

# n - número de informantes, elementos_t - número de pontos de análise, t - identificação dos pontos
# M_inf_aj, M_sup_aj, taxa_inf, taxa_sup - matrizes com as faixas de probabilidades
# Df - limites DT em falhas maiores, Dp - limites DT em manutenção preventiva, Dm - limites DT em minimo reparo
    
#def amostras (A_exercicio, n, t, elementos_t, M_inf_aj, M_sup_aj, taxa_inf, taxa_sup, Df, Dp, Dm):
def amostras (A_exercicio, n, t_total, M_inf, M_sup, taxa_inf_todos, taxa_sup_todos, Df, Dp, Dm):
        
    num_it = 50*n
    amostra = np.zeros(num_it)
    amostras_especificas_por_informante = np.zeros((n,num_it))

    #for i in range (0, num_it):
    n_iteracoes_validas = 0
    while n_iteracoes_validas < num_it:
        #n_iteracoes_validas = n_iteracoes_validas + 1
        try:
            #stlt.write('iteração', n_iteracoes_validas)
            #print('i =', i)
            r = rd.rand()
            p = 0     # número do informante cuja análise será considerada
            for j in range (1, n+1):
                if (r > ((j-1)*(1/n))) and (r <= (j*(1/n))):
                    p = j
                else:
                    p = p
                    # p é o número do informante cuja análise será considerada
            linha = p-1 #índice do informante considerado para coletar dados
        
            t = t_total[linha]
            t = np.array(t)
            elementos_t = len(t)
        
            M_inf_especifico = M_inf[linha]
            M_inf_aj = np.array(M_inf_especifico)
            M_inf_aj = M_inf_aj/100
        
            M_sup_especifico = M_sup[linha]
            M_sup_aj = np.array(M_sup_especifico)
            M_sup_aj = M_sup_aj/100
        
            taxa_inf = taxa_inf_todos[linha]
            taxa_inf = np.array(taxa_inf)
        
            taxa_sup = taxa_sup_todos[linha]
            taxa_sup = np.array(taxa_sup)
        

            # Parâmetros WEIBULL - falhas catastróficas
            ref = 0    # REF - probabilidade associada a um ponto no tempo, que deve ser menor ou igual a probabilidade e instantes posteriores
            vetor_prob = np.zeros (elementos_t)
    
            for k in range(0, elementos_t):
                prob = 0
                if ref < M_inf_aj[k]:
                    prob = rd.uniform(M_inf_aj[k], M_sup_aj[k], 1)
                if ref >= M_inf_aj[k] and ref <= M_sup_aj[k]:
                    prob = rd.uniform(ref, M_sup_aj[k], 1)
                if ref > M_sup_aj[k]:
                    prob = rd.uniform(ref, 1, 1)
                vetor_prob[k] = prob
                ref = prob

            #definir beta e eta a partir de regressão
            Xreg = np.zeros(elementos_t)
            Yreg = np.zeros(elementos_t)
            for k in range (0, elementos_t):
                Xreg[k] = np.log(t[k])
                Yreg[k] = np.log(np.log(1/(1-vetor_prob[k])))
            regressao = st.linregress(Xreg,Yreg)
            A_reg = - regressao.intercept
            B_reg = regressao.slope
    
            beta_ = B_reg #parâmetro de forma - distribuição de probabilidade para falha catastrófica (WEIBULL)
            eta_ = np.exp (A_reg/beta_) #parâmetro de escala - distribuição de probabilidade para falha catastrófica (WEIBULL)

            ## Função Característica da Evolução da Taxa de Falhas Menores
            escolha = 0
            
            while escolha == 0:
                vetor_taxa = np.zeros(elementos_t)
                
                for k in range (0, elementos_t):
                    vetor_taxa[k] = rd.uniform (taxa_inf[k], taxa_sup[k], 1)
                
                desvio_otm = 10**100    # começo com altíssimo limiar para início das iterações
                
                grau_pol = -1      
                coefs_pol = 0
                criterio = 0
                
                while criterio == 0:
                    grau_pol = grau_pol + 1
                    pol_ajuste = np.polyfit(t, vetor_taxa, grau_pol, full=True)
                    desvio_pol = (pol_ajuste[1])/(len(t)-(grau_pol+1))
                    
                    if desvio_pol <= desvio_otm:
                        desvio_otm = desvio_pol
                        coefs_pol = pol_ajuste[0]
                    else:
                        grau_pol = grau_pol - 1
                        criterio = 1
                        
                def taxa_teste (t):
                    taxa_funcao = 0
                    grau_ref = grau_pol
                    local = -1
            
                    for ii in range (0, grau_pol+1):
                        local = local + 1
                        coefs_ = coefs_pol [local]
                        taxa_funcao = taxa_funcao + coefs_*(t**grau_ref)
                        grau_ref = grau_ref - 1 
                    return taxa_funcao 
                
                teste_min = opt.minimize_scalar(taxa_teste, bounds = [0.01, 2*eta_], method = 'bounded')
                ponto_min = teste_min.fun
                
                if ponto_min >= 0:
                    escolha = 1
                
            print(grau_pol,coefs_pol)

            Df_ = rd.uniform (Df[0], Df[1], 1)
            Dp_ = rd.uniform (Dp[0], Dp[1], 1)
            Dm_ = rd.uniform (Dm[0], Dm[1], 1)

            indice_relativo = Res (A_exercicio, eta_, beta_, grau_pol, coefs_pol, Df_, Dp_, Dm_)
    
            amostra[n_iteracoes_validas] = indice_relativo #acumulando dados
            amostras_especificas_por_informante[linha][n_iteracoes_validas] = indice_relativo
            n_iteracoes_validas = n_iteracoes_validas + 1
            stlt.write('iteração', n_iteracoes_validas)
        except:
            #n_iteracoes_validas = n_iteracoes_validas - 1
            continue

    qtd_n = np.zeros (n, dtype=list)
    for ii in range(0,n): # contagem de observações por especialista
        qtd = 0
        for jj in range(0, num_it):
            if amostras_especificas_por_informante[ii][jj] != 0:
                qtd = qtd+1
        qtd_n[ii] = np.zeros(qtd)

    for ii in range(0,n): # criando uma matriz sem zeros com as amostras separadas por informante
        pos = -1
        for jj in range (0,num_it):
            if amostras_especificas_por_informante[ii][jj] != 0:
                pos = pos + 1
                qtd_n[ii][pos] = amostras_especificas_por_informante[ii][jj]
    
    amostras_especificas_por_informante = np.zeros(n,dtype=list) # base para filtrar zeros
    for ii in range(0,n):
        amostras_especificas_por_informante[ii] = qtd_n[ii] # amostras por especialistas atualizada, sem zeros 

    ## Elaborando as funções belief e plausibility
    massa_unitaria = 1/n

    marcos = np.zeros(2*n) ## para cada especialista eu determino dois pontos demarcando os limites inferior e superior, por isso 2n elementos
    bel_vetor = np.zeros(2*n)
    pl_vetor = np.zeros(2*n)
    matriz_comparar = np.zeros((n,2))
    marco_ref = -1
    marco_ref2 = -1

    for i in range(0,n):
        A_mmin = np.percentile ( amostras_especificas_por_informante [i] , 100 - percentil_referencia_pl)  # mínimo desempenho relativo
        A_mmax = np.percentile ( amostras_especificas_por_informante [i] , percentil_referencia_pl ) #máximo desempenho relativo
    
        marco_ref = marco_ref + 1
        marcos [marco_ref] = A_mmin
        marco_ref = marco_ref + 1
        marcos [marco_ref] = A_mmax    
        marco_ref2 = marco_ref2 + 1
        matriz_comparar [marco_ref2][0] = A_mmin
        matriz_comparar [marco_ref2][1] = A_mmax
    marcos.sort()

    for ww in range (0, (2*n)):
        bel_valor = 0
        pl_valor = 0
        for jj in range (0, n):
            if matriz_comparar[jj][0] >= marcos[ww]:
                bel_valor = bel_valor + massa_unitaria
            if (matriz_comparar[jj][0] < marcos[ww] and matriz_comparar[jj][1] >= marcos[ww]) or (matriz_comparar[jj][0] >= marcos[ww]):
                pl_valor = pl_valor + massa_unitaria
        bel_vetor[ww] = bel_valor
        pl_vetor[ww] = pl_valor
        
    ponto_minimo = min(amostra)
    ponto_maximo = max(amostra)

    return (amostra, bel_vetor, pl_vetor, marcos, ponto_minimo, ponto_maximo, num_it)

#DEFININDO AS FUNÇÕES BELIEF E PLAUSIBILITY

def bel_fun(ttt, bel_vetor, marcos):
    marcos = marcos
    nn = len(marcos)
    bel = 2
    if ttt <= marcos[0]:
        bel = 1
    if ttt > marcos[nn-1]:
        bel = 0
    if (ttt > marcos[0]) and (ttt <= marcos[nn-1]):
        for i in range(1,nn):
            if (ttt > marcos[i-1]) and (ttt <= marcos[i]):
                bel = bel_vetor[i]
    return bel

def pl_fun (ttt, pl_vetor, marcos):
    marcos = marcos
    nn = len(marcos)
    pl = 2
    if ttt <= marcos[0]:
        pl = 1
    if ttt > marcos[(nn-1)]:
        pl = 0
    if (ttt > marcos[0]) and (ttt <= marcos[nn-1]):
        for i in range (1, nn):
            if (ttt > marcos[i-1]) and (ttt <= marcos[i]):
                pl = pl_vetor[i]
    return pl

def d_empirica (t, amostra, num_it):    
    amostra.sort()
    observacoes_pmais = num_it
    tamanho_relativo = (num_it)
    vetor_pos = np.zeros(tamanho_relativo)
    vetor_probs = np.zeros(tamanho_relativo)
    pos = -1
    for i in range (0, num_it):
        observacoes_pmais = observacoes_pmais - 1
        pos = pos + 1
        vetor_pos[pos] = amostra[pos]
        vetor_probs[pos] = observacoes_pmais/num_it
    if t < amostra[0]:
        d_empirica = 1
    if t >= amostra[num_it-1]:
        d_empirica = 0

    if (t >= amostra[0]) and (t < amostra[num_it-1]):
        for i in range (1, num_it):
            if (t >= vetor_pos[i-1]) and (t < vetor_pos[i]):
                d_empirica = vetor_probs[i-1]
    return d_empirica

def comparacoes(amostra_A,amostra_B,rep):
    amostra_A.sort()
    amostra_B.sort()
    l_A = len(amostra_A)
    l_B = len(amostra_B)
    vetor_posA = np.zeros(l_A)
    vetor_probsA = np.zeros(l_A)
    vetor_posB = np.zeros(l_B)
    vetor_probsB = np.zeros(l_B)
    
    totA = l_A
    for i in range(0,l_A):
        totA = totA - 1
        vetor_posA[i] = amostra_A[i]
        vetor_probsA[i] = totA/l_A
    
    totB = l_B
    for i in range(0,l_B):
        totB = totB - 1
        vetor_posB[i] = amostra_B[i]
        vetor_probsB[i] = totB/l_B
    
    def X_inverso (Y, vetor_pos, vetor_probs):
        criterio = 0
        X_passado = 0
        X_atual = 0
        pos = -1
        while criterio == 0:
            pos = pos + 1
            if vetor_probs[pos] == Y:
                X_atual = vetor_pos[pos]
                X_passado = vetor_pos[pos]
                criterio = 1
            else:
                if vetor_probs[pos] < Y:
                    X_atual = vetor_pos[pos]
                    criterio = 1
                else:
                    X_passado = vetor_pos[pos]
        X_medio = (X_passado + X_atual)/2
        return X_medio

    contagem_A = 0
    contagem_B = 0
    
    for j in range(0,rep):
        yA = rd.rand()
        XA = X_inverso (yA, vetor_posA, vetor_probsA)
        yB = rd.rand()
        XB = X_inverso (yB, vetor_posB, vetor_probsB)
        if XA > XB:
            contagem_A = contagem_A + 1
        elif XA == XB:
            contagem_A = contagem_A + 1
            contagem_B = contagem_B + 1
        else:
            contagem_B = contagem_B + 1
            
    proporcao_A = contagem_A/rep
    proporcao_B = contagem_B/rep
            
    return (proporcao_A, proporcao_B)

#spinner = stlt.spinner("Aguarde, cálculo em andamento. O processo pode demorar vários minutos")

if stlt.button('Análise Comparativa'):
    if ((n_A < 1) or (n_B < 1)):
        stlt.write('Por favor, insira as informações solicitadas')
    else:
        with stlt.spinner('Aguarde, cálculo em andamento. O processo pode demorar vários minutos'):
            planta_A = amostras (A_exercicio_A, n_A, t_A, M_inf_A, M_sup_A, taxa_inf_A, taxa_sup_A, Df_A, Dp_A, Dm_A)
            planta_B = amostras (A_exercicio_B, n_B, t_B, M_inf_B, M_sup_B, taxa_inf_B, taxa_sup_B, Df_B, Dp_B, Dm_B)

            amostra_A = planta_A[0]
            bel_vetor_A = planta_A[1]
            pl_vetor_A = planta_A[2]
            marcos_A = planta_A[3] 
            ponto_minimo_A = planta_A[4]
            ponto_maximo_A = planta_A[5]  
            num_it_A = planta_A[6]

            amostra_B = planta_B[0]
            bel_vetor_B = planta_B[1]
            pl_vetor_B = planta_B[2]
            marcos_B = planta_B[3]
            ponto_minimo_B = planta_B[4]
            ponto_maximo_B = planta_B[5]
            num_it_B = planta_B[6]    

            minimo_grafico = min(ponto_minimo_A, ponto_minimo_B)
            maximo_grafico = max(ponto_maximo_A, ponto_maximo_B)
        
            contagens = comparacoes (amostra_A, amostra_B, 10000)
        
        stlt.success('Análise concluída')

        #print('')
        #print('')
        #print('')
        #print('RESULTADOS')
        stlt.write(f'A manutenção do sistema {id_A} tem desempenho superior à manutenção do sistema {id_B} com probabilidade', contagens[0])
        stlt.write(f'A manutenção do sistema {id_B} tem desempenho superior à manutenção do sistema {id_A} com probabilidade', contagens[1])

        # PLOTAGEM DOS GRÁFICOS

        n_pontos = 1000

        passo = (maximo_grafico - minimo_grafico)/n_pontos

        JJJ1 = np.zeros(n_pontos)
        XXX1 = np.zeros(n_pontos)
        YYY1 = np.zeros(n_pontos)
        ZZZ1 = np.zeros(n_pontos)
    
        JJJ2 = np.zeros(n_pontos)
        XXX2 = np.zeros(n_pontos)
        YYY2 = np.zeros(n_pontos)
        ZZZ2 = np.zeros(n_pontos)

        inicioJJJ1 = minimo_grafico - passo
        inicioJJJ2 = minimo_grafico - passo
        
        for i in range(0,n_pontos):
            inicioJJJ1 = inicioJJJ1 + passo
            inicioJJJ2 = inicioJJJ2 + passo
            JJJ1[i] = inicioJJJ1
            JJJ2[i] = inicioJJJ2
            XXX1[i] = bel_fun(inicioJJJ1,bel_vetor_A,marcos_A)
            XXX2[i] = bel_fun(inicioJJJ2,bel_vetor_B,marcos_B)
            YYY1[i] = pl_fun(inicioJJJ1,pl_vetor_A,marcos_A)
            YYY2[i] = pl_fun(inicioJJJ2,pl_vetor_B,marcos_B)    
            ZZZ1[i] = d_empirica(inicioJJJ1,amostra_A,len(amostra_A))
            ZZZ2[i] = d_empirica(inicioJJJ2,amostra_B,len(amostra_B)) 
        
        
        figura, ax = plt.subplots()

        ax.plot(JJJ1, XXX1, 'b:') # label='Crença (S1)')
        ax.plot(JJJ2, XXX2, 'r:') # label= 'Crença (S2)')
        ax.plot(JJJ1, YYY1, 'b--') # label='Plausibilidade (S1)')
        ax.plot(JJJ2, YYY2, 'r--') # label='Plausibilidade (S2)')
        ax.plot(JJJ1, ZZZ1, 'b') # label='Distribuição Empírica (S1)')
        ax.plot(JJJ2, ZZZ2, 'r') # label='Distribuição Empírica (S2)')

        ax.set_xlabel('Índice de Desempenho Relativo')
        #ax.legend('Análise gráfica')
        
        stlt.write('Análise gráfica')
        stlt.write(f'Dados do sistema {id_A} (S1) apresentados em azul')
        stlt.write(f'Dados do sistema {id_B} (S2) apresentados em vermelho')
        stlt.pyplot(figura)
        
        
        
        #figura = plt.plot(JJJ1,XXX1,'b:',JJJ1,YYY1,'b--',JJJ1,ZZZ1,'b',JJJ2,XXX2,'r:',JJJ2,YYY2,'r--',JJJ2,ZZZ2,'r')
        
        #stlt.write('Análise gráfica')
        #stlt.write(f'Dados do sistema {id_A} apresentados em azul')
        #stlt.write(f'Dados do sistema {id_B} apresentados em vermelho')
        #stlt.pyplot(figura)


    

