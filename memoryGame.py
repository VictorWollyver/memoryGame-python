import pygame
import random
import os

pygame.init()

# Configurações da tela
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Padrões")

# Cores
background_color = (54, 100, 139)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
hover_color = (100, 100, 255)

# Arquivo de maior pontuação
high_score_file = "high_score.txt"

class Botao:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, hover=False):
        color = hover_color if hover else self.color
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Jogador:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pattern = []
        self.score = 0

    def add_input(self, button_index):
        self.pattern.append(button_index)

class Controlador:
    def __init__(self):
        # Calcula a posição vertical central para os botões
        button_size = 50
        spacing = 20
        start_x = (screen_width - (3 * button_size + 2 * spacing)) // 2  # Centraliza horizontalmente

        self.buttons = [Botao(start_x + (i % 3) * (button_size + spacing), (i // 3) * (button_size + spacing) + 20, button_size, button_size, "", blue) for i in range(9)]
        self.player_buttons = [Botao(start_x + (i % 3) * (button_size + spacing), (i // 3) * (button_size + spacing) + 300, button_size, button_size, "", blue) for i in range(9)]
        self.pattern = []
        self.player = Jogador()
        self.showing_pattern = True

    # ... (rest of the code remains unchanged)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def draw_player_buttons(self):
        for button in self.player_buttons:
            button.draw()

    def flash_pattern(self):
        for index in self.pattern:
            screen.fill(background_color)
            self.draw_buttons()
            self.draw_player_buttons()
            self.buttons[index].draw(hover=True)
            pygame.display.flip()
            pygame.time.wait(500)
            screen.fill(background_color)
            self.draw_buttons()
            self.draw_player_buttons()
            pygame.display.flip()
            pygame.time.wait(500)

    def check_player_input(self, button_index):
        self.player.add_input(button_index)
        if self.player.pattern == self.pattern:
            self.player.score += 10  # Aumenta a pontuação ao vencer
            return True  # Jogador venceu
        elif len(self.player.pattern) == len(self.pattern):
            return False  # Jogador perdeu
        return None  # Continua jogando

    def start_game(self):
        self.pattern = [random.randint(0, 8) for _ in range(4)]
        self.player.reset()
        self.showing_pattern = True

class Menu:
    def __init__(self):
        self.buttons = [
            Botao(200, 200, 200, 50, "Iniciar", green),
            Botao(200, 270, 200, 50, "Dificuldade", yellow),
            Botao(200, 340, 200, 50, "Como Jogar", red),
            Botao(200, 410, 200, 50, "Sair", blue)
        ]
        self.difficulty_buttons = [
            Botao(200, 200, 200, 50, "Fácil", blue),
            Botao(200, 270, 200, 50, "Médio", blue),
            Botao(200, 340, 200, 50, "Difícil", blue),
            Botao(200, 410, 200, 50, "Voltar", yellow)  # Botão de voltar
        ]
        self.controlador = Controlador()
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists(high_score_file):
            with open(high_score_file, "r") as file:
                return int(file.read().strip())
        return 0

    def save_high_score(self):
        with open(high_score_file, "w") as file:
            file.write(str(self.high_score))

    def draw(self):
        screen.fill(background_color)
        for button in self.buttons:
            button.draw()

        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Maior Pontuação: {self.high_score}", True, black)
        screen.blit(score_surface, (screen_width // 2 - score_surface.get_width() // 2, 150))

    def draw_difficulty_menu(self):
        screen.fill(background_color)
        for button in self.difficulty_buttons:
            button.draw()

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Escolha a Dificuldade", True, black)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 100))

    def check_clicks(self, pos):
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(pos):
                if i == 0:  # Iniciar a partida
                    self.controlador.start_game()
                    return "start_game"
                elif i == 1:  # Modificar Dificuldade
                    return "difficulty_menu"
                elif i == 2:  # Como Jogar
                    return "how_to_play"
                elif i == 3:  # Sair
                    return "exit"

    def modify_difficulty(self):
        self.display_message("Dificuldade modificada!")

    def show_how_to_play(self):
        self.display_message("Como jogar: Siga o padrão dos botões.", is_how_to_play=True)

    def display_message(self, message, is_how_to_play=False):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, black)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

        back_button = Botao(200, screen_height // 2 + 60, 200, 50, "Voltar", blue)

        screen.fill(background_color)
        screen.blit(text_surface, text_rect)
        back_button.draw()
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if back_button.rect.collidepoint(pos):
                        waiting = False  # Retorna ao menu

        return  # Adicionado para evitar travamento

def display_game_over(score, high_score):
    font = pygame.font.Font(None, 48)
    text_surface = font.render("Game Over", True, red)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    score_surface = font.render(f"Pontos: {score}", True, white)
    score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    restart_button = Botao(200, screen_height // 2 + 60, 200, 50, "Voltar ao Menu", blue)

    screen.fill(background_color)
    screen.blit(text_surface, text_rect)
    screen.blit(score_surface, score_rect)
    restart_button.draw()

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if restart_button.rect.collidepoint(pos):
                    waiting = False

def main():
    running = True
    menu = Menu()
    game_running = False
    difficulty_menu_active = False
    how_to_play_active = False

    while running:
        if not game_running:
            if difficulty_menu_active:
                menu.draw_difficulty_menu()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for i, button in enumerate(menu.difficulty_buttons):
                            if button.rect.collidepoint(pos):
                                if i == 3:  # Voltar ao menu
                                    difficulty_menu_active = False
                                else:
                                    menu.modify_difficulty()
            elif how_to_play_active:
                menu.show_how_to_play()
                how_to_play_active = False  # Resetar estado após exibir
            else:
                menu.draw()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        action = menu.check_clicks(pos)
                        if action == "exit":
                            running = False
                        elif action == "start_game":
                            game_running = True
                        elif action == "difficulty_menu":
                            difficulty_menu_active = True
                        elif action == "how_to_play":
                            how_to_play_active = True
        else:
            screen.fill(background_color)
            menu.controlador.draw_buttons()
            menu.controlador.draw_player_buttons()

            # Exibir pontuação na parte inferior
            font = pygame.font.Font(None, 36)
            score_surface = font.render(f"Pontos: {menu.controlador.player.score}", True, white)
            screen.blit(score_surface, (screen_width // 2 - score_surface.get_width() // 2, screen_height - 50))

            if menu.controlador.showing_pattern:
                menu.controlador.flash_pattern()
                menu.controlador.showing_pattern = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, button in enumerate(menu.controlador.player_buttons):
                        if button.rect.collidepoint(pos):
                            menu.controlador.player_buttons[i].draw(hover=True)
                            pygame.display.flip()
                            pygame.time.wait(200)

                            result = menu.controlador.check_player_input(i)
                            if result is True:
                                menu.controlador.pattern.append(random.randint(0, 8))
                                menu.controlador.start_game()  # Reinicia o jogo com um novo padrão
                            elif result is False:
                                if menu.controlador.player.score > menu.high_score:
                                    menu.high_score = menu.controlador.player.score
                                    menu.save_high_score()  # Salva a nova maior pontuação
                                game_running = False
                                display_game_over(menu.controlador.player.score, menu.high_score)  # Mostra a tela de Game Over
                            break

            # Botão para voltar ao menu
            back_button = Botao(20, screen_height - 70, 100, 40, "Voltar", blue)  # Mover o botão para baixo
            back_button.draw()
            if back_button.rect.collidepoint(pygame.mouse.get_pos()):
                back_button.draw(hover=True)
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.rect.collidepoint(pos):
                game_running = False  # Volta ao menu

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
