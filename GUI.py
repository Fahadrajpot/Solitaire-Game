import sys
import time
import pygame
from Classes import  *
from Functions import *

# Pages

def front_page():
    pygame.init()
    width, height = 1000, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Solitaire')
    back_image=pygame.image.load('Cards/front_page.png')
    back_image=pygame.transform.scale(back_image, (width, height))
    
    font = pygame.font.SysFont('Bodoni', 28)
    
   
    button_width, button_height = 150, 50
    start_button = pygame.Rect((width - button_width) // 2, 240, button_width, button_height)
    rules_button = pygame.Rect((width - button_width) // 2, 310, button_width, button_height)
    exit_button = pygame.Rect((width - button_width) // 2, 380, button_width, button_height)
    
    
    start_button_color = (157, 205, 90) 
    rules_button_color =(157, 205, 90)
    exit_button_color = (157, 205, 90)
    button_text_color = (50, 98, 14) 
    
    screen.blit(back_image,(0,0))
    pygame.draw.rect(screen, start_button_color, start_button, border_radius=8)
    pygame.draw.rect(screen, rules_button_color, rules_button, border_radius=8)
    pygame.draw.rect(screen, exit_button_color, exit_button ,border_radius=8)
    start_text = font.render("Start Game", True, button_text_color)
    rules_text = font.render("Rules", True, button_text_color)
    exit_text = font.render("Exit", True, button_text_color)
    screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
    screen.blit(rules_text, (rules_button.centerx - rules_text.get_width() // 2, rules_button.centery - rules_text.get_height() // 2))
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))
    
    
    
    running = True
    while(running):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    game_interface()
                if rules_button.collidepoint(mouse_x,mouse_y):
                    pygame.quit()
                    rules_page()
                if exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
def game_interface():
    pygame.init()
    width, height = 1500, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Solitaire')

    start_time=time.time()
    score=0
    moves=0
    
    foundation_locations = [((540 + i * 130), 60) for i in range(4)]
    foundations = [Foundation(suit) for suit in ['heart', 'diamond', 'club', 'spade']]
    column_positions = [(150 + i * 130, 250) for i in range(7)]
    
    deck = Deck()
    tableau = Tableau(column_positions)
    deck = tableau.initialize_tableau(deck)
    stockpiles = StockPile(deck)

    selected_col_index = None
    selected_card = None
    dragging = False
    dragged_card = None 
    
    back_image=pygame.image.load('Cards/background.jpg')
    back_image=pygame.transform.scale(back_image, (width, height))
    
    
    running = True
    
    while running:
        screen.blit(back_image,(0,0))
        font = pygame.font.SysFont('Bodoni', 28)
        button_width, button_height = 150, 50
        back_button = pygame.Rect((width - button_width) -100, 650, button_width, button_height)
        back_button_color = (0, 100, 0) 
        button_text_color = (255, 255, 255) 
        pygame.draw.rect(screen, back_button_color, back_button)
        back_text = font.render("Back", True, button_text_color)
        screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))
        
        draw_timer_and_score(screen,start_time,score,moves)
        stockpiles.print_stockpile(screen, stockpiles)
        print_foundation(foundations,screen)
        for i in range(4):
            foundations[i].display_single_foundation(screen, foundations[i], foundation_locations[i])
        tableau.display_tableau(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if stockpiles.detect_stockpile_click(event) == "StockPile":
                    stockpiles.draw_one_card()
                else:
                    dragged_card = stockpiles.start_drag(event, stockpiles)
                    if stockpiles.drawn_cards and dragged_card:
                        stockpiles.drawn_cards.pop(-1)
                # dragging from tableau
                selected_col_index, selected_card = tableau.detect_card_click(event)
                if selected_card and selected_card.front:
                    dragging = True
                    from_pile=tableau.piles[selected_col_index]
                    my_card=from_pile.remove(selected_card)
                    tableau.display_tableau(screen)
                mouse_x, mouse_y = event.pos
                if back_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    front_page()
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_card:
                    mouse_x, mouse_y = event.pos
                    valid_move = False
                    
                    # Move to tableau
                    for col_index in range(len(tableau.piles)):
                        x, y = tableau.column_location[col_index]
                        pile_rect = pygame.Rect(x, y, 100, 500)
                        if pile_rect.collidepoint(mouse_x, mouse_y):
                            valid_move = tableau.move_card(selected_col_index, col_index, selected_card, my_card)
                            if valid_move:
                                score+=9
                                moves+=1
                                my_card=None
                                break

                    # Move to foundation
                    for col_index in range(len(foundations)):
                        x, y = foundation_locations[col_index]
                        pile_rect = pygame.Rect(x, y, 100, 500)
                        if pile_rect.collidepoint(mouse_x, mouse_y):
                            (valid_move, tableau.piles) = foundations[col_index].move_card(selected_col_index, selected_card, tableau.piles, my_card)
                            if valid_move:
                                score+=15
                                moves+=1
                                selected_card = None
                                my_card=None
                                break
                    if not valid_move:
                        from_pile.push_stack(my_card)
                    dragging = False
                    selected_col_index = None
                    selected_card = None

                elif dragged_card:
                    # Move from StockPile
                    if stockpiles.place_card(event, dragged_card, tableau, foundations, foundation_locations):
                        score+=6
                        moves+=1
                    else:
                        stockpiles.drawn_cards.append(dragged_card)
                    dragged_card = None   
                    
        if dragging and selected_card:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if selected_card.front:
                screen.blit(selected_card.image, (mouse_x - selected_card.image.get_width() // 2, mouse_y - selected_card.image.get_height() // 2))
        elif dragged_card:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            stockpiles.drag_card(screen, dragged_card, mouse_x, mouse_y)
            
        if win_conditon(foundations):
            pygame.quit()
            winning_page(screen,score,moves,start_time)
            running =False   
        if tableau.all_cards_face_up():
            pygame.quit()
            winning_page(screen,score,moves,start_time)
            running =False 
        pygame.display.flip()

    pygame.quit()
    sys.exit()
def rules_page():
    pygame.init()
    width, height = 600, 750
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Solitaire')
    back_image=pygame.image.load('Cards/help_page.png')
    back_image=pygame.transform.scale(back_image, (width, height))
    running = True
    while(running):
        screen.blit(back_image,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                front_page()
        pygame.display.flip()

    pygame.quit()
    sys.exit()
def winning_page(screen,score,move,start_time):
    pygame.init()
    width, height = 750, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Solitaire')
    back_image=pygame.image.load('Cards/win_page.png')
    back_image=pygame.transform.scale(back_image, (width, height))
    
    font = pygame.font.SysFont('Bodoni', 28)
    text_color = (255, 255, 255) 
    time_text = font.render(f"Time: {int((time.time() - start_time) // 60)}:{int((time.time() - start_time) % 60)}",True,text_color)
    score_text = font.render(f"Score: {score}",True, text_color)
    move_text = font.render(f"Moves: {move}",True,text_color)
    
    text_x = (width - time_text.get_width()) -30
    text_y = 15
    
    
   
    button_width, button_height = 150, 50
    restart_button = pygame.Rect((width - button_width) // 2-150, 560, button_width, button_height)
    exit_button = pygame.Rect((width - button_width) // 2+150, 560, button_width, button_height)
    
    
    restart_button_color = (255, 255, 255)  
    exit_button_color = (255, 255, 255)  
    button_text_color = (0, 200, 0)
    
    restart_text = font.render("Restart", True, button_text_color)
    exit_text = font.render("Back", True, button_text_color)
    
   
    screen.blit(back_image,(0,0))
    pygame.draw.rect(screen,restart_button_color, restart_button, border_radius=8)
    pygame.draw.rect(screen, exit_button_color, exit_button, border_radius=8)
    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))
    screen.blit(time_text, (text_x, text_y))
    screen.blit(score_text, (text_x, text_y+40))
    screen.blit(move_text, (text_x, text_y+80))    
    
    
    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    game_interface()
                if exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    front_page()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Main

if __name__=="__main__":
   front_page()