import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icon  = pygame.image.load("Recursos/icon.png")
van = pygame.image.load("Recursos/van.png")
fundo = pygame.image.load("Recursos/fundo.png")
girassois = pygame.image.load("Recursos/girassois.jpg")
morto = pygame.image.load("Recursos/morto.jpg")

tesoura = pygame.image.load("Recursos/tesoura.png")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Starry Night")
pygame.display.set_icon(icon)
missileSound = pygame.mixer.Sound("Recursos/missile.wav")
explosaoSound = pygame.mixer.Sound("Recursos/corte.mp3")
fonte = pygame.font.SysFont("comicsans",28)
fonteStart = pygame.font.SysFont("comicsans",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("Recursos/ironsound.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )
amarelo = (255, 255, 0)
raio_sol = 30  
velocidade_raio = 1 
crescendo = True

def jogar(nome):
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXtesoura = 400
    posicaoYtesoura = -240
    velocidadetesoura = 1
    pontos = 0
    larguraPersona = 150
    alturaPersona = 150
    larguatesoura  = 100
    alturatesoura = 100
    dificuldade  = 20

    while True:
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = 10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
                
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
        global raio_sol, velocidade_raio, crescendo
        if crescendo:
            raio_sol += velocidade_raio
            if raio_sol > 50:  
                crescendo = False
        else:
            raio_sol -= velocidade_raio
            if raio_sol < 30: 
                crescendo = True
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( van, (posicaoXPersona, posicaoYPersona) )
        
        posicaoYtesoura = posicaoYtesoura + velocidadetesoura
        if posicaoYtesoura > 600:
            posicaoYtesoura = -240
            pontos = pontos + 1
            velocidadetesoura = velocidadetesoura + 1
            posicaoXtesoura = random.randint(0,800)
            pygame.mixer.Sound.play(missileSound)
            
            
        tela.blit( tesoura, (posicaoXtesoura, posicaoYtesoura) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelstesouraX = list(range(posicaoXtesoura, posicaoXtesoura + larguatesoura))
        pixelstesouraY = list(range(posicaoYtesoura, posicaoYtesoura + alturatesoura))
        
        #print( len( list( set(pixelstesouraX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelstesouraY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelstesouraX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
    
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(morto, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Aperte Enter para continuar", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Iron Man","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(girassois, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()