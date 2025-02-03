import pygame
import random

# Card

class Card:
    def __init__(self, suit,rank,front=False):
        self.rank = rank
        self.suit = suit
        self.front = front
        self.image = self.load_image()
        self.back_face=self.load_back_image()
        self.color = 'red' if self.suit in ['heart', 'diamond'] else 'black'
        
    def face_up(self):
        if not self.front:
            self.front = True
    def load_image(self):
        image_path=f"Cards/{self.rank}_of_{self.suit}.png"
        image=pygame.image.load(image_path)
        resize=pygame.transform.scale(image, (80, 120))
        return resize
    
    def load_back_image(self):
        image_path=f"Cards/back_face.png"
        image=pygame.image.load(image_path)
        resize=pygame.transform.scale(image, (80, 120))
        return resize
    
    def display_card(self, card, screen, position):
        if card.front:
            screen.blit(card.image, position)
        else:
            screen.blit(card.back_face, position)

# Deck

class Deck:
    
    def __init__(self):
        self.cards = []
        self.initialize_deck()
        self.shuffle()

    def initialize_deck(self):
        suits = ["heart", "diamond", "club", "spade"]
        ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        return random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def remaining_cards(self):
        return len(self.cards)

# Tableau

class Tableau:
    def __init__(self, column_location):
        self.piles = [Stack() for _ in range(7)]
        self.column_location = column_location
        
    def initialize_tableau(self, deck):
        for i in range(7):
            for j in range(i + 1):
                card = deck.draw_card()
                if card is None:
                    raise ValueError("Deck ran out of cards")
                if j == i:
                    card.face_up()
                self.piles[i].push(card)
        return deck
    def can_add_card(self, to_pile, card_to_add):
        if to_pile.Head is None and card_to_add.rank=='k':
            return True
        if not card_to_add:
            return False 
        if not to_pile:
            return card_to_add.rank == 'k'
        
        top_card = to_pile.top() 
        if not top_card:
            return False
        
        top_card = to_pile.top() 
        opposite_color = card_to_add.color != top_card.color
        ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
        card_to_move_index = ranks.index(card_to_add.rank)
        top_card_index = ranks.index(top_card.rank)
        correct_rank = (card_to_move_index + 1 == top_card_index)
        
        return opposite_color and correct_rank

    def move_to_foundation(self, from_pile_index, foundation):
        from_pile = self.piles[from_pile_index]
        card_to_move = from_pile.top()

        if card_to_move and foundation.add_card(card_to_move):
            from_pile.Pop()
            new_top_card = from_pile.top()
            if new_top_card and not new_top_card.front:
                new_top_card.face_up()
            return True
        return False
    def all_cards_face_up(self):
        for pile in self.piles:
            current = pile.Head
            while current:
                card = current.Data
                if not card.front:
                    return False
                current = current.Next
        return True
    def display_tableau(self, screen):
        card_image=pygame.image.load('Cards/card.png')
        card_image=pygame.transform.scale(card_image,( 80,120))
        for i in range(7):
            screen.blit(card_image,(150+i*130, 250))
        for col_index in range(len(self.piles)):
            pile = self.piles[col_index]
            current = pile.Head 
            x, y = self.column_location[col_index]
            y_offset = 30
            i = 0
            while current:
                card = current.Data
                card_y = y + i * y_offset
                card.display_card(card, screen, (x, card_y))
                current = current.Next
                i += 1

    def detect_card_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            for col_index, pile in enumerate(self.piles):
                current = pile.Head
                i = 0
                x, y = self.column_location[col_index]
                y_offset = 30 
                visible_height = y_offset 
                
                while current:
                    card = current.Data
                    
                    rect_height = visible_height if current.Next else card.image.get_height()
                    
                    card_rect = pygame.Rect(x, y + i * y_offset, card.image.get_width(), rect_height)
                    
                    if card.front and card_rect.collidepoint(mouse_x, mouse_y):
                        return col_index, card
                    
                    current = current.Next
                    i += 1
        return None, None

    def move_card(self, from_col_index, to_col_index, card, cards_to_move):
        if from_col_index is None or to_col_index is None:
            return False
        from_pile = self.piles[from_col_index]
        to_pile = self.piles[to_col_index]
        if card and card.front and self.can_add_card(to_pile, card):
            if not from_pile.is_empty():
                from_pile.top().face_up()
            if self.can_add_card(to_pile, card) and to_pile.Head is None:
                to_pile.push_stack(cards_to_move)
                return True
            if cards_to_move.Head:
                to_pile.push_stack(cards_to_move)
                new_top_card = from_pile.top()
                if from_pile is None:
                    from_pile.Head=None
                if new_top_card and not new_top_card.front:
                    new_top_card.face_up()
                if to_pile.top() and not to_pile.top().front:
                    to_pile.top().face_up()

                return True
        return False
    
# Foundation

class Foundation:
    def __init__(self, suit):
        self.suit = suit
        self.cards = [] 
        self.ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']

    def add_card(self, card):
        if self.can_add_card(card):
            self.cards.append(card)
            return True
        return False
    def move_card(self, from_col_index, card, piles, cards_to_move):
        if from_col_index is None:
            return False
        from_pile = piles[from_col_index]
        if card is None:
            return
        if card and card.front and self.can_add_card(card):
            if cards_to_move.Head:
                new_top_card = from_pile.top()
                if from_pile is None:
                    from_pile.Head=None
                if new_top_card and not new_top_card.front:
                    new_top_card.face_up()
                self.add_card(card)
                return True, piles
        return False, piles
    
    def can_add_card(self, card):
        if not self.cards:
            return card.suit == self.suit and card.rank == 'ace'
        expected_rank = self.ranks[len(self.cards)]
        return card.suit == self.suit and card.rank == expected_rank
    
    def is_complete(self):
        return len(self.cards) == 13
    
    def display_single_foundation(self,screen, foundation, foundation_location):

        foundation_x, foundation_y = foundation_location
        if foundation.cards:
            top_card = foundation.cards[-1]
            card_image = top_card.image
            screen.blit(card_image, (foundation_x, foundation_y))
            
# StockPile

class StockPile:
    def __init__(self, deck):
        self.cards = deck.cards[:]
        self.drawn_cards = []
        self.current_draw_index = 0

    def draw_one_card(self):
        if not self.cards and self.drawn_cards:
            self.recycle()
            return
        if self.cards:
            drawn_card = self.cards.pop(0)
            drawn_card.face_up()
            self.drawn_cards.append(drawn_card)
            self.current_draw_index = len(self.drawn_cards) - 1
            return drawn_card
        elif self.drawn_cards:
            self.current_draw_index = (self.current_draw_index + 1) % len(self.drawn_cards)
            return self.drawn_cards[self.current_draw_index]
        return None

    def recycle(self):
        self.cards = self.drawn_cards[:]
        self.drawn_cards = []
        self.current_draw_index = 0

    def move_to_tableau(self, tableau, pile_index):
        if not self.drawn_cards:
            return False

        card_to_move = self.drawn_cards[self.current_draw_index]
        if tableau.can_add_card(pile_index, card_to_move):
            self.drawn_cards.pop(self.current_draw_index)
            tableau.piles[pile_index].push(card_to_move)
            return True
        return False
    def print_stockpile(self, screen, stockpile):
        card_image=pygame.image.load('Cards/card.png')
        card_image=pygame.transform.scale(card_image,( 80,120))
        Pile=['StockPile', 'WastePile']
        for i, suit in enumerate(Pile):
            if len(stockpile.cards)>0 and i==0:
                screen.blit(stockpile.cards[0].back_face, ((150+i*100), 60))
                continue
            if len(stockpile.drawn_cards)>0 and i==1:
                screen.blit(stockpile.drawn_cards[-1].image, ((150+i*100), 60))
                continue
            screen.blit(card_image,(150+i*100, 60))

    def detect_stockpile_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            stock_pile_rect = pygame.Rect(150, 60, 80, 120)
            waste_pile_rect = pygame.Rect(250, 60, 80, 120)
            if stock_pile_rect.collidepoint(mouse_x, mouse_y):
                return "StockPile"
            if waste_pile_rect.collidepoint(mouse_x, mouse_y):
                return "WastePile"

        return None
   
    def start_drag(self, event, stockpile):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_area = stockpile.detect_stockpile_click(event)
            if clicked_area == "WastePile" and stockpile.drawn_cards:
                return stockpile.drawn_cards[-1]
        return None
    def drag_card(self, screen, card, mouse_x, mouse_y):
        if card:
            screen.blit(card.image, (mouse_x - card.image.get_width() // 2, mouse_y - card.image.get_height() // 2))
   
    def place_card(self, event, dragged_card, tableau, foundations, foundation_locations):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_x, mouse_y = event.pos
            card_width = dragged_card.image.get_width() 
            card_height = dragged_card.image.get_height() 
            
            for i, pile in enumerate(tableau.piles):
                x, y = tableau.column_location[i]
                pile_rect = pygame.Rect(x, y, card_width, card_height)
                
                pile_rect.height = max(card_height, 500)
                
                if pile_rect.collidepoint(mouse_x, mouse_y) and tableau.can_add_card(pile, dragged_card):
                    pile.push(dragged_card)
                    return True

            for i, foundation in enumerate(foundations):
                foundation_x, foundation_y = foundation_locations[i]  
                pile_rect = pygame.Rect(foundation_x, foundation_y, card_width, card_height)

                if pile_rect.collidepoint(mouse_x, mouse_y) and foundation.can_add_card(dragged_card):
                    foundation.add_card(dragged_card) 
                    return True

        return False

# Stack

class Node:
    def __init__(self, Data):
        self.Data = Data
        self.Next = None
class Stack:
    def __init__(self):
        self.Head = None

    def is_empty(self):
        return self.Head is None
  
    def push(self, Data):
        NewNode = Node(Data)
        if self.Head is None:
            self.Head=NewNode
            return
        temp=self.Head
        while temp.Next is not None:
            temp=temp.Next
        temp.Next=NewNode
    def top(self):
        if self.is_empty():
            return None
        temp=self.Head
        while temp.Next is not None:
            temp=temp.Next
        return temp.Data
  
    def cut_off_at(self, node):
        
        if not node:
            return
        current = self.Head
        if self.Head.Data==node.Data:
            self.Head=None
        while current and current.Next != node:
            current = current.Next
        if current and current.Next == node:
            current.Next = None

    def remove(self, card):
        
        current = self.Head
        removed_stack = Stack()
        while current and current.Data != card:
            current = current.Next
        if current:
            removed_stack.Head = current
            self.cut_off_at(current) 
        return removed_stack


    def push_stack(self, other_stack):
        if other_stack is None:
            return
        if not other_stack.Head:
            return
        if not self.Head:
            self.Head = other_stack.Head
        else:
            current = self.Head
            while current.Next:
                current = current.Next
            current.Next = other_stack.Head
