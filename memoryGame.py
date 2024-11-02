import pygame
import random
import os

pygame.init()

# Configurações da tela
screen_width = 600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory.Py")

# Cores
background_color = (30, 41, 59)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
hover_color = (100, 100, 255)

# Arquivo de maior pontuação
high_score_file = "high_score.txt"
font_file_path = "Poppins/Poppins-Bold.ttf"

class Botao:
    def __init__(self, x, y, width, height, text, color, textColor=black):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.textColor = textColor

    def draw(self, hover=False):
        color = hover_color if hover else self.color
        pygame.draw.rect(screen, black, self.rect.inflate(3 * 2, 3 * 2), border_radius=15)
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        font = pygame.font.Font(font_file_path, 24)
        text_surface = font.render(self.text, True, self.textColor)
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
        button_size = 50
        spacing = 20
        num_buttons_per_row = 3
        num_rows = 3
        padding = 20  # Espaçamento entre a borda da caixa e os botões

        # Calcula a largura e altura total ocupada pelos botões e espaçamentos
        total_height = num_rows * button_size + (num_rows - 1) * spacing
        total_width = num_buttons_per_row * button_size + (num_buttons_per_row - 1) * spacing
        start_y = (screen_height - total_height) // 4  # Centraliza verticalmente
        start_x = (screen_width - total_width) // 2  # Centraliza horizontalmente

        # Define a caixa ao redor dos botões com padding
        self.box_rect = pygame.Rect(start_x - padding, start_y - padding, total_width + 2 * padding, total_height + 2 * padding)
        self.player_box_rect = pygame.Rect(start_x - padding, start_y + 300 - padding, total_width + 2 * padding, total_height + 2 * padding)

        # Ajusta a posição dos botões para incluir o padding
        self.buttons = [Botao(start_x + (i % num_buttons_per_row) * (button_size + spacing), start_y + (i // num_buttons_per_row) * (button_size + spacing), button_size, button_size, "", background_color) for i in range(9)]
        self.player_buttons = [Botao(start_x + (i % num_buttons_per_row) * (button_size + spacing), start_y + (i // num_buttons_per_row) * (button_size + spacing) + 300, button_size, button_size, "", background_color) for i in range(9)]
        self.pattern = []
        self.player = Jogador()
        self.showing_pattern = True

    def draw_box(self, rect):
        pygame.draw.rect(screen, black, rect, 3, border_radius=12)  # Desenha a caixa com uma borda de 3 pixels e raio de borda de 12

    def draw_buttons(self):
        self.draw_box(self.box_rect)
        for button in self.buttons:
            button.draw()

    def draw_player_buttons(self):
        self.draw_box(self.player_box_rect)
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
    current_score = 0
    high_score = 0
    def __init__(self):
        self.buttons = [
            Botao(200, 400, 200, 50, "Iniciar", green),
            Botao(200, 470, 200, 50, "Dificuldade", yellow),
            Botao(200, 540, 200, 50, "Como Jogar", red),
            Botao(200, 610, 200, 50, "Sair", blue)
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

    def save_high_score(self, high_score):
        with open(high_score_file, "w") as file:
            file.write(str(high_score))

    def draw(self):
        screen.fill(background_color)
        
        # Carrega a imagem PNG
        png_file_path = "Group 1.png"
        png_image = pygame.image.load(png_file_path)

        # Calcula a posição para desenhar a imagem abaixo do texto
        font = pygame.font.Font(font_file_path, 36)
        fontPontuacao = pygame.font.Font(font_file_path, 24)
        score_surface = font.render(f"Memory.Py", True, white)
        margin_bottom = 40
        text_x = screen_width // 2 - score_surface.get_width() // 2
        text_y = 150 - margin_bottom
        image_x = screen_width // 2 - png_image.get_width() // 2
        image_y = text_y + score_surface.get_height() + 60  # 10 pixels de margem inferior

        # Desenha a imagem PNG
        screen.blit(png_image, (image_x, image_y))

        # Desenha o texto
        screen.blit(score_surface, (text_x, text_y))

        # Desenha os botões
        for button in self.buttons:
            button.draw()

        fontPontuacao = pygame.font.Font(font_file_path, 24)
        high_score_text = "Melhor pontuação:"
        high_score_value = str(self.high_score)

        high_score_text_surface = fontPontuacao.render(high_score_text, True, white)
        high_score_text_x = 10  # Margem esquerda
        high_score_text_y = screen_height - high_score_text_surface.get_height() - 10  # Margem inferior

        high_score_value_surface = fontPontuacao.render(high_score_value, True, (0, 255, 0))  # Verde
        high_score_value_x = high_score_text_x + high_score_text_surface.get_width() + 5  # Adiciona um pequeno espaçamento
        high_score_value_y = high_score_text_y

        screen.blit(high_score_text_surface, (high_score_text_x, high_score_text_y))
        screen.blit(high_score_value_surface, (high_score_value_x, high_score_value_y))

        pygame.display.flip()

    def draw_difficulty_menu(self):
        screen.fill(background_color)
        for button in self.difficulty_buttons:
            button.draw()

        font = pygame.font.Font(font_file_path, 24)
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
        text = (
            "Memory.py é um jogo para \n"
            "testar sua memória. Na sua tela \n"
            "você verá dois “Pads”, o pad de \n"
            "cima sendo o nosso robô que \n"
            "repetirá uma sequencia de \n"
            "botões piscando. O desafio \n"
            "será que você como jogador \n"
            "repita essa mesma sequência. \n\n"
            "Caso você acerte, acumulará \n"
            "pontos, dessa forma podendo \n"
            "bater seus recordes e \n"
            "compartilhar com os amigos."
        )
        self.display_message(text, is_how_to_play=True)

    def display_message(self, message, is_how_to_play=False):
        font = pygame.font.Font(font_file_path, 16)
        color = black

        # Divida o texto em linhas
        lines = message.split('\n')

        # Posição inicial
        x = screen_width // 2
        y = screen_height // 2 - (len(lines) * font.get_linesize()) // 2

        back_button = Botao(200, screen_height // 2 + 250, 200, 50, "Voltar", background_color, white)

        screen.fill(background_color)

        # Renderize cada linha individualmente
        for line in lines:
            rendered_line = font.render(line, True, white)
            text_rect = rendered_line.get_rect(center=(x, y))
            screen.blit(rendered_line, text_rect)
            y += font.get_linesize() + 5  # Adiciona espaçamento entre as linhas

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
    font = pygame.font.Font(font_file_path, 48)
    fontRegular = pygame.font.Font(font_file_path, 24)
    text_surface = font.render("VOCÊ PERDEU", True, red)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 300))

    score_surface = fontRegular.render(f"Sua pontuação é: {score}", True, white)
    score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 250))

    restart_button = Botao(200, screen_height // 2 + 60, 200, 50, "Voltar", background_color, white)

    screen.fill(background_color)
    screen.blit(text_surface, text_rect)
    screen.blit(score_surface, score_rect)
    restart_button.draw()

    # Verifica se a pontuação atual é maior que a maior pontuação salva
    if score > high_score:
        high_score = score
        with open(high_score_file, "w") as file:
            file.write(str(high_score))

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
    current_score = 0

    menu.load_high_score()

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
            font = pygame.font.Font(font_file_path, 24)
            score_surface = font.render(f"Pontos: {current_score}", True, white)
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
                                current_score = current_score + 1
                                print(current_score)
                                menu.controlador.pattern.append(random.randint(0, 8))
                                menu.controlador.start_game()  # Reinicia o jogo com um novo padrão
                            elif result is False:
                                if current_score > menu.high_score:
                                    menu.high_score = menu.controlador.player.score
                                    menu.save_high_score(current_score)  # Salva a nova maior pontuação
                                game_running = False
                                display_game_over(current_score, menu.high_score)  # Mostra a tela de Game Over
                                current_score = 0
                                menu.high_score = menu.load_high_score()
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