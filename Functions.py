
import pygame
import time

def win_conditon(foundations):
    for foundation in foundations:
        if not foundation.is_complete():
            return False
    return True 

def print_foundation(foundations,screen):
    card_image=pygame.image.load('Cards/card.png')
    card_image=pygame.transform.scale(card_image,( 80,120))
    
    for i in range(4):
        if i==0:
            card_image_heart=pygame.image.load('Cards/heart.png')
            card_image_heart=pygame.transform.scale(card_image_heart,( 75,120))
            screen.blit(card_image,(540+i*130, 60))
            screen.blit(card_image_heart,(540+i*130+2, 60))
        if i==1:
            card_image_diamond=pygame.image.load('Cards/diamond.png')
            card_image_diamond=pygame.transform.scale(card_image_diamond,( 75,120))
            screen.blit(card_image,(540+i*130, 60))
            screen.blit(card_image_diamond,(540+i*130+1, 60))
        if i==2:
            card_image_club=pygame.image.load('Cards/club.png')
            card_image_club=pygame.transform.scale(card_image_club,( 75,120))
            screen.blit(card_image,(540+i*130, 60))
            screen.blit(card_image_club,(540+i*130+2, 60))
        if i==3:
            card_image_spade=pygame.image.load('Cards/spade.png')
            card_image_spade=pygame.transform.scale(card_image_spade,( 75,120))
            screen.blit(card_image,(540+i*130, 60))
            screen.blit(card_image_spade,(540+i*130+2, 60))
    
        
def draw_timer_and_score(screen,start_time,score,moves):
    current_time = time.time() - start_time
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    time_text = f"Time: {minutes:02}:{seconds:02}"
    score_text = f"Score: {score}"
    move_text = f"Moves: {moves}"

    font = pygame.font.SysFont('Bodoni', 35)
    time_surface = font.render(time_text, True, (255, 255, 255))
    score_surface = font.render(score_text, True, (255, 255, 255)) 
    move_surface = font.render(move_text, True, (255, 255, 255))

    screen.blit(time_surface, (1200, 70))
    screen.blit(score_surface, (1200, 110))   
    screen.blit(move_surface, (1200, 150))
 