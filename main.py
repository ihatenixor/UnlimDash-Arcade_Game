import random
import pygame
import csv

from objects import Player, Balls, Dot, Shadow, Particle, Message, BlinkingText, Button

pygame.init()
SCREEN = WIDTH, HEIGHT = 512, 800
CENTER = WIDTH //2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

LIGHT_ORANGE = (252, 185, 76)
LIGHT_PINK = (244, 148, 255)
RED = (201, 4, 17)
LIGHT_GREEN = (84, 240, 123)
BLUE = (114, 159, 242)
PURPLE = (178, 103, 240)
WHITE = (255,255,255)
BLACK = (0,0,0)

clr_list = [PURPLE, LIGHT_ORANGE, LIGHT_GREEN, BLUE]
clr_index = 0
clr = clr_list[clr_index]
title_font = "Fonts/BruceForeverRegular-X3jd2.ttf"
tap_to_play_font = "Fonts/BruceForeverRegular-X3jd2.ttf"
score_font = "Fonts/BruceForeverRegular-X3jd2.ttf"
game_over_font = "Fonts/SportypoReguler-OVGwe.ttf"

unlim = Message(WIDTH-145, 370, 60, "Unlim", title_font, BLACK, win)
dash = Message(145, 420, 60, "Dash", title_font, WHITE, win)
tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 20, "Tap To Play", tap_to_play_font, WHITE, win)
game_msg = Message(130, 250, 50, "GAME", game_over_font, RED, win)
over_msg = Message(375, 250, 50, "OVER!", game_over_font, RED, win)
score_text = Message(150, 330, 20, "SCORE", score_font, BLACK, win)
best_text = Message(370, 330, 20, "BEST", score_font, BLACK, win)

score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)
final_score_msg = Message(150, 380, 40, "0", tap_to_play_font, BLACK, win)
high_score_msg = Message(370, 380, 40, "0", tap_to_play_font, BLACK, win)

score_fx = pygame.mixer.Sound('Sounds/point.mp3')
death_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/menu.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

home_img = pygame.image.load('Assets/homeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")


home_btn = Button(home_img, (40, 40), WIDTH // 4 - 18, 470)
replay_btn = Button(replay_img, (40, 40), WIDTH // 2  - 18, 470)
sound_btn = Button(sound_on_img, (40, 40), WIDTH - WIDTH // 4 - 18, 470)

MAX_RAD = 120
rad_delta = 50

ball_group = pygame.sprite.Group()
dot_group = pygame.sprite.Group()
shadow_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
p = Player(win)

ball_positions = [(CENTER[0]-105, CENTER[1]), (CENTER[0]+105, CENTER[1]),
					(CENTER[0]-45, CENTER[1]), (CENTER[0]+45, CENTER[1]),
					(CENTER[0], CENTER[1]-75), (CENTER[0], CENTER[1]+75)]
for index, pos in enumerate(ball_positions):
	if index in (0,1):
		type_ = 1
		inverter = 5
	if index in (2,3):
		type_ = 1
		inverter = 3
	if index in (4,5):
		type_ = 2
		inverter = 1
	ball = Balls(pos, type_, inverter, win)
	ball_group.add(ball)

dot_list = [(CENTER[0], CENTER[1]-MAX_RAD+3), (CENTER[0]+MAX_RAD-3, CENTER[1]),
			(CENTER[0], CENTER[1]+MAX_RAD-3), (CENTER[0]-MAX_RAD+3, CENTER[1])]
dot_index = random.choice([1,2,3,4])
dot_pos = dot_list[dot_index-1]
dot = Dot(*dot_pos, win)
dot_group.add(dot)

shadow = Shadow(dot_index, win)
shadow_group.add(shadow)

clicked = False
num_clicks = 0
player_alive = True
sound_on = True

score = 0
highscore = 0

home_page = True
game_page = False
score_page = False

running = True
while running:
	win.fill(clr)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN and home_page:
			home_page = False
			game_page = True
			score_page = False

			rad_delta = 50
			clicked = True
			score = 0
			num_clicks = 0
			player_alive = True

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			if not clicked:
				clicked = True
				for ball in ball_group:
					if num_clicks % ball.inverter == 0:
						ball.dtheta *= -1

				p.set_move(dot_index)

				num_clicks += 1
				if num_clicks % 5 == 0:
					clr_index += 1
					if clr_index > len(clr_list) - 1:
						clr_index = 0

					clr = clr_list[clr_index]

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			clicked = False

	if home_page:
		for radius in [30, 60, 90, 120]:
			pygame.draw.circle(win, (0,0,0), CENTER, radius, 8)
			pygame.draw.circle(win, (255,255,255), CENTER, radius, 5)

		pygame.draw.rect(win, clr, [CENTER[0]-10, CENTER[1]-MAX_RAD, MAX_RAD+50, MAX_RAD])
		pygame.draw.rect(win, clr, [CENTER[0]-MAX_RAD, CENTER[1]-10, MAX_RAD, MAX_RAD+50])

		unlim.update()
		dash.update()
		tap_to_play.update()

	if score_page:
		game_msg.update()
		over_msg.update()
		score_text.update(shadow=False)
		best_text.update(shadow=False)
		final_score_msg.update(score, shadow=False)
		high_score_msg.update(highscore, shadow=False)
		if home_btn.draw(win):
			home_page = True
			score_page = False
			game_page = False
			score = 0
			score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)

		if replay_btn.draw(win):
			home_page = False
			score_page = False
			game_page = True

			player_alive = True
			score = 0
			score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)
			p = Player(win)

		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:

		for radius in [30 + rad_delta, 60 + rad_delta, 90 + rad_delta, 120 + rad_delta]:
			if rad_delta > 0:
				radius -= 1
				rad_delta -= 1
			pygame.draw.circle(win, (0,0,0), CENTER, radius, 5)


		pygame.draw.rect(win, clr, [CENTER[0]-10, CENTER[1]-MAX_RAD, 20, MAX_RAD*2])
		pygame.draw.rect(win, clr, [CENTER[0]-MAX_RAD, CENTER[1]-10, MAX_RAD*2, 20])

		if rad_delta <= 0:
			p.update(player_alive, clr, shadow_group)
			shadow_group.update()
			ball_group.update()
			dot_group.update()
			particle_group.update()
			score_msg.update(score)

			for dot in dot_group:
				if dot.rect.colliderect(p):
					dot.kill()
					score_fx.play()

					score += 1
					if highscore <= score:
						highscore = score

			if pygame.sprite.spritecollide(p, ball_group, False) and player_alive:
				death_fx.play()
				x, y = p.rect.center
				for i in range(20):
					particle = Particle(x, y, WHITE, win)
					particle_group.add(particle)
				player_alive = False

				with open('records/records.csv', 'w+', encoding='utf-8') as f:
					reader = csv.reader(f, delimiter=';')
					writer = csv.writer(f, delimiter=';')
					writer.writerow([highscore])
					

				p.reset()

			if p.can_move and len(dot_group) == 0 and player_alive:
				dot_index = random.randint(1,4)
				dot_pos = dot_list[dot_index-1]
				dot = Dot(*dot_pos, win)
				dot_group.add(dot)

				shadow_group.empty()
				shadow = Shadow(dot_index, win)
				shadow_group.add(shadow)

			if not player_alive and len(particle_group) == 0:
				game_page = False
				score_page = True
				dot_group.empty()
				shadow_group.empty()
				for ball in ball_group:
					ball.reset()
				score_page_fx.play()
				


	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
