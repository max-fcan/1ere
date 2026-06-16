# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 09:15:00 2025

@author: m.tanguy
"""

import time
from typing import Optional
import pygame

from sudoku_utils import Sudoku

pygame.init()

# Track buttons and mouse position for click detection
buttons = []
mouse_pos = (0, 0)

largeur, hauteur = 1080, 720
CELL_SIZE = 60

ecran = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
pygame.display.set_caption("Mon Sudoku")

sudoku = Sudoku()

_last_generation_time = 0.0
_dessiner_popup_pour_attentre_10_secondes = False
_temps = 0.0

def quit_app():
    """Quit the application (used as button callback)."""
    global running
    running = False

def dessiner(ecran: pygame.Surface):
    """Dessine la grille Sudoku sur la surface fournie."""
    blanc = (255,255,255)
    noir = (0,0,0)
    gris = (180,180,180)

    ecran.fill(blanc)
    taille = CELL_SIZE*9
    grille = pygame.Surface((taille, taille))
    grille.fill(blanc)

    # lignes fines
    for i in range(10):
        if i % 3 != 0:
            pygame.draw.line(grille, gris, (i*CELL_SIZE,0),(i*CELL_SIZE,taille),1)
            pygame.draw.line(grille, gris, (0,i*CELL_SIZE),(taille,i*CELL_SIZE),1)

    # lignes épaisses 3x3
    for i in range(4):
        pygame.draw.line(grille, noir, (i*3*CELL_SIZE,0),(i*3*CELL_SIZE,taille),4)
        pygame.draw.line(grille, noir, (0,i*3*CELL_SIZE),(taille,i*3*CELL_SIZE),4)

    # nombres
    police = pygame.font.Font(None, 40)
    for i in range(9):
        for j in range(9):
            val = sudoku.grid[i][j]
            if val:
                txt = police.render(str(val), True, noir)
                rect = txt.get_rect(center=(j*CELL_SIZE+CELL_SIZE//2, i*CELL_SIZE+CELL_SIZE//2))
                grille.blit(txt, rect)

    ecran.blit(grille, ((largeur-taille)//2, (hauteur-taille)//2))

def dessiner_bouton(ecran: pygame.Surface, x: int, y: int, w: int, h: int, texte: str, fonction: Optional[callable]): # pyright: ignore[reportGeneralTypeIssues]
    """Dessine un bouton avec le texte fourni qui appelle une fonction lors du clic."""
    global mouse_pos, buttons
    
    gris = (200,200,200)
    gris_hover = (220,220,220)
    noir = (0,0,0)
    
    rect = pygame.Rect(x, y, w, h)
    is_hovered = rect.collidepoint(mouse_pos)
    couleur = gris_hover if is_hovered else gris
    
    pygame.draw.rect(ecran, couleur, (x, y, w, h))
    pygame.draw.rect(ecran, noir, (x, y, w, h), 2)
    police = pygame.font.Font(None, 30)
    txt = police.render(texte, True, noir)
    txt_rect = txt.get_rect(center=(x + w//2, y + h//2))
    ecran.blit(txt, txt_rect)
    
    buttons.append((rect, fonction))
    return rect

def dessiner_popup(ecran: pygame.Surface, message: str):
    """Dessine une popup avec le message fourni au centre de l'écran."""
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    gris = (200, 200, 200)
    
    # Dimensions de la popup
    popup_width, popup_height = 400, 150
    popup_x = (largeur - popup_width) // 2
    popup_y = (hauteur - popup_height) // 2
    
    # Dessiner le fond semi-transparent
    overlay = pygame.Surface((largeur, hauteur))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    ecran.blit(overlay, (0, 0))
    
    # Dessiner le fond de la popup
    pygame.draw.rect(ecran, blanc, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(ecran, noir, (popup_x, popup_y, popup_width, popup_height), 3)
    
    # Dessiner le texte du message
    police = pygame.font.Font(None, 35)
    txt = police.render(message, True, noir)
    txt_rect = txt.get_rect(center=(largeur // 2, popup_y + popup_height // 2))
    ecran.blit(txt, txt_rect)

running = True
horloge = pygame.time.Clock()
while running:
    buttons.clear()
    mouse_pos = pygame.mouse.get_pos()

    dessiner(ecran)

    def new_game():
        global _last_generation_time, _dessiner_popup_pour_attentre_10_secondes, _temps
        if time.time() - _last_generation_time < 10: # Ten seconds
            _dessiner_popup_pour_attentre_10_secondes = True
            _temps = time.time()
        else:
            _last_generation_time = time.time()
            sudoku.generate_new_grid()

    dessiner_bouton(ecran, 50, 50, 150, 40, "Nouveau Jeu", new_game)
    dessiner_bouton(ecran, 50, 100, 150, 40, "Réinitialiser", sudoku.reset)
    dessiner_bouton(ecran, 50, 150, 150, 40, "Vérifier", sudoku.is_solution)
    dessiner_bouton(ecran, 50, 200, 150, 40, "Résoudre", sudoku.resoudre)
    dessiner_bouton(ecran, 50, 250, 150, 40, "Quitter", quit_app)

    if _dessiner_popup_pour_attentre_10_secondes:
        dessiner_popup(ecran, "Veuillez attendre 10 secondes avant de générer une nouvelle grille.")
        if time.time() - _temps >= 1:
            _dessiner_popup_pour_attentre_10_secondes = False

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            largeur, hauteur = event.w, event.h
            ecran = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rect, fonction in buttons:
                    if rect.collidepoint(event.pos) and fonction is not None:
                        fonction()

    horloge.tick(60)

pygame.quit()
