import pygame
import sys
import os

pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

# ---------------- Global Variables ----------------
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Base directory where this .py file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to textures_escape folder
TEXTURES_DIR = os.path.join(BASE_DIR, "textures_escape")

THEME_MUSIC_PATH = os.path.join(TEXTURES_DIR, "theme.mp3")
CHEST_IMAGE_PATH = os.path.join(TEXTURES_DIR, "chest.png")
BUTTON_IMAGE_PATH = os.path.join(TEXTURES_DIR, "button.png")
DOOR_IMAGE_PATH = os.path.join(TEXTURES_DIR, "door.png")
KEYPAD_EXTRA_PATH = os.path.join(TEXTURES_DIR, "keypad_extra.png")
KEYPAD_DISPLAY_PATH = os.path.join(TEXTURES_DIR, "keypad_display.png")
KEY_IMAGE_PATH = os.path.join(TEXTURES_DIR, "key_a.png")
DOOR_OPEN_IMAGE_PATH = os.path.join(TEXTURES_DIR, "door_open.png")
OPEN_SOUND_PATH = os.path.join(TEXTURES_DIR, "open.wav")
SLOT_IMAGE_PATH = os.path.join(TEXTURES_DIR, "slot.png")
ROPE_IMAGE_PATH = os.path.join(TEXTURES_DIR, "rope.png")
BG1_PATH = os.path.join(TEXTURES_DIR, "bg.png")
BG2_PATH = os.path.join(TEXTURES_DIR, "bg2.png")
BG3_PATH = os.path.join(TEXTURES_DIR, "bg3.png")
FRAG_IMAGE_PATH = os.path.join(TEXTURES_DIR, "vase_fragment.png")


# Load music
try:
    pygame.mixer.music.load(THEME_MUSIC_PATH)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except Exception:
    pass

# Load textures safely
def load_texture(path):
    try:
        return pygame.image.load(path)
    except Exception as e:
        print(f"Failed to load texture {path}: {e}")
        return None

CHEST_IMAGE = load_texture(CHEST_IMAGE_PATH)
BUTTON_IMAGE = load_texture(BUTTON_IMAGE_PATH)
DOOR_IMAGE = load_texture(DOOR_IMAGE_PATH)
KEYPAD_EXTRA_IMAGE = load_texture(KEYPAD_EXTRA_PATH)
KEYPAD_DISPLAY_IMAGE = load_texture(KEYPAD_DISPLAY_PATH)
KEY_IMAGE = load_texture(KEY_IMAGE_PATH)
DOOR_OPEN_IMAGE = load_texture(DOOR_OPEN_IMAGE_PATH)
SLOT_IMAGE = load_texture(SLOT_IMAGE_PATH)
ROPE_IMAGE = load_texture(ROPE_IMAGE_PATH)
FRAGMENT_IMAGE = load_texture(FRAG_IMAGE_PATH)

# Load backgrounds
BG1 = pygame.image.load(BG1_PATH)
BG1 = pygame.transform.scale(BG1, (WINDOW_WIDTH, WINDOW_HEIGHT))
BG2 = pygame.image.load(BG2_PATH)
BG2 = pygame.transform.scale(BG2, (WINDOW_WIDTH, WINDOW_HEIGHT))
BG3 = pygame.image.load(BG3_PATH)
BG3 = pygame.transform.scale(BG3, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load open sound
try:
    OPEN_SOUND = pygame.mixer.Sound(OPEN_SOUND_PATH)
except Exception:
    OPEN_SOUND = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# ---------------- Classes ----------------
class KeyPad:
    def __init__(self, x, y, button_size=40, spacing=10, layer=0):
        self.x = x
        self.y = y
        self.button_size = button_size
        self.spacing = spacing
        self.input = ""
        self.buttons = []
        self.rect = pygame.Rect(x, y, button_size * 3 + spacing * 2, button_size * 4 + spacing * 3)
        self.display_rect = pygame.Rect(x, y - 50, button_size * 3 + spacing * 2, 40)
        self.hovered_button = None
        self.pressed_button = None
        self.layer = layer

        for idx in range(12):
            row, col = divmod(idx, 3)
            self.buttons.append({
                'rect': pygame.Rect(x + col * (button_size + spacing), y + row * (button_size + spacing), button_size, button_size),
                'index': idx
            })

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = next((b['index'] for b in self.buttons if b['rect'].collidepoint(mouse_pos)), None)

        if KEYPAD_EXTRA_IMAGE:
            try:
                screen.blit(pygame.transform.scale(KEYPAD_EXTRA_IMAGE, (self.rect.width, self.rect.height)), self.rect)
            except Exception:
                pygame.draw.rect(screen, DARK_GRAY, self.rect)
        else:
            pygame.draw.rect(screen, DARK_GRAY, self.rect)

        if KEYPAD_DISPLAY_IMAGE:
            try:
                screen.blit(pygame.transform.scale(KEYPAD_DISPLAY_IMAGE, (self.display_rect.width, self.display_rect.height)), self.display_rect)
            except Exception:
                pygame.draw.rect(screen, WHITE, self.display_rect)
                pygame.draw.rect(screen, BLACK, self.display_rect, 2)
        else:
            pygame.draw.rect(screen, WHITE, self.display_rect)
            pygame.draw.rect(screen, BLACK, self.display_rect, 2)

        input_text = font.render(self.input, True, BLACK)
        screen.blit(input_text, (self.display_rect.centerx - input_text.get_width() // 2, self.display_rect.centery - input_text.get_height() // 2))

        for b in self.buttons:
            if BUTTON_IMAGE:
                try:
                    img = pygame.transform.scale(BUTTON_IMAGE, (b['rect'].width, b['rect'].height))
                    if b['index'] == self.pressed_button:
                        img.set_alpha(100)
                    elif b['index'] == self.hovered_button:
                        img.set_alpha(200)
                    screen.blit(img, b['rect'])
                except Exception:
                    pygame.draw.rect(screen, GRAY, b['rect'])
            else:
                pygame.draw.rect(screen, GRAY, b['rect'])

    def check_click(self, pos):
        for b in self.buttons:
            if b['rect'].collidepoint(pos):
                idx = b['index']
                if idx == 9 and self.input:
                    self.input = self.input[:-1]
                elif idx == 11:
                    return self.input
                elif idx < 9 and len(self.input) < 5:
                    self.input += str(idx + 1)
                elif idx == 10 and len(self.input) < 5:
                    self.input += "0"
                return None
        return None

class Item:
    def __init__(self, x, y, width, height, color, name, layer=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.name = name
        self.is_collected = False
        self.is_open = False
        self.layer = layer

    def draw(self, screen):
        if self.is_collected:
            return
        img = None
        if self.name in ("door", "exit_door"):
            img = DOOR_OPEN_IMAGE if self.is_open and DOOR_OPEN_IMAGE else DOOR_IMAGE
        elif self.name == "key":
            img = KEY_IMAGE
        elif self.name == "rope":
            img = ROPE_IMAGE
        if img:
            try:
                screen.blit(pygame.transform.scale(img, (self.rect.width, self.rect.height)), self.rect)
            except Exception:
                pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

class DraggableBox:
    def __init__(self, x, y, width, height, color, image=None, layer=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.dragging = False
        self.drag_offset = (0, 0)
        self.image = image
        self.fixed_y = y
        self.layer = layer

    def start_drag(self, pos):
        if self.rect.collidepoint(pos):
            self.dragging = True
            self.drag_offset = (self.rect.x - pos[0], 0)
            return True
        return False

    def stop_drag(self):
        self.dragging = False

    def update(self, pos):
        if self.dragging:
            self.rect.x += int(((pos[0] + self.drag_offset[0]) - self.rect.x) * 0.5)
            self.rect.y = self.fixed_y
            self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def draw(self, screen):
        if self.image:
            try:
                screen.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), self.rect)
            except Exception:
                pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

# ---------------- Game ----------------
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon of Whispers")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        for tex in [CHEST_IMAGE, BUTTON_IMAGE, DOOR_IMAGE, KEY_IMAGE, DOOR_OPEN_IMAGE, KEYPAD_EXTRA_IMAGE, KEYPAD_DISPLAY_IMAGE, SLOT_IMAGE, ROPE_IMAGE]:
            if tex:
                try:
                    tex.convert_alpha()
                except Exception:
                    pass

        # Room objects
        self.chest = DraggableBox(100, 500, 150, 150, GRAY, image=CHEST_IMAGE, layer=3)
        self.door = Item(650, 235, 400, 400, GREEN, "door", layer=1)
        self.key = Item(self.chest.rect.centerx - 16, self.chest.rect.y - 40, 32, 32, YELLOW, "key", layer=4)
        self.keypad = KeyPad(50, 400, layer=1)

        self.rope = Item(500, -500, 64, 500, YELLOW, "rope", layer=2)
        self.rope.is_collected = True  # hidden initially

        self.has_key = False
        self.inventory = []
        self.dragging_item = None
        self.drag_offset = (0, 0)

        self.message = ""
        self.message_timer = 0

        # ---------------- Room 3 collectible items ----------------
        self.room3_items = []

        # Example vase fragments
        fragment_width = 50
        fragment_height = 50  # <= 220 pixels
        fragment_color = (200, 150, 100)

        # Place a few scattered in Room 3
        positions = [(200, 500), (400, 540), (700, 520)]
        for pos in positions:
            item = Item(pos[0], pos[1], fragment_width, fragment_height, fragment_color, "vase_fragment")
            self.room3_items.append(item)

        # Example Room 3 fragments
        self.room3_items = [
            Item(200, 540, 32, 32, (200, 100, 50), "vase_frag1"),
            Item(400, 550, 32, 32, (180, 150, 70), "vase_frag2"),
            Item(700, 520, 32, 32, (150, 180, 90), "vase_frag3")
        ]

        # store original positions
        for frag in self.room3_items:
            frag.home_pos = frag.rect.topleft

        # BROKEN VASE
        self.broken_vase = Item(500, 200, 64, 128, (150, 100, 50), "broken_vase")
        self.vase_repaired = False  # state of the vase



        # rooms
        self.current_room = 1
        self.backgrounds = {1: BG1, 2: BG2, 3: BG3}
        self.transition_alpha = 0
        self.transition_direction = 0
        self.target_room = None

        # animations
        self.animations = []

        # rope drop animation
        self.rope_animating = False
        self.rope_target_y = -100

        # inventory UI
        self.inv_x = 10
        self.inv_y = 10
        self.slot_size = 64
        self.inv_padding = 6
        self.slot_count = 3

    # ---------------- Utility ----------------
    def show_message(self, text, duration=180):
        self.message = text
        self.message_timer = duration

    def start_room_transition(self, target_room):
        self.transition_alpha = 0
        self.transition_direction = 1
        self.target_room = target_room

        if target_room == 3:
            self.door.is_open = False
             # Move door up 86 pixels
            self.door.rect.y -= 86
        
        else:
            # Reset to original Y when leaving room 3
            self.door.rect.y = 235


    def update_transition(self):
        if self.transition_direction != 0:
            step = 12
            self.transition_alpha += step * self.transition_direction
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.transition_direction = -1
                self.current_room = self.target_room
            elif self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transition_direction = 0

            fade = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            fade.fill((0,0,0))
            fade.set_alpha(self.transition_alpha)
            self.screen.blit(fade, (0, 0))

    def start_pickup_animation(self, image, start_pos, slot_index, duration_ms=500):
        end = self.get_slot_center(slot_index)
        iw, ih = image.get_size()
        anim = {
            'type': 'pickup',
            'image': image,
            'start_pos': tuple(start_pos),
            'end_pos': tuple(end),
            'start_time': pygame.time.get_ticks(),
            'duration': duration_ms,
            'start_scale': 1.0,
            'end_scale': 1.0,
            'start_alpha': 255,
            'end_alpha': 255,
            'size': (iw, ih)
        }
        self.animations.append(anim)

    def start_use_animation(self, image, start_pos, target_pos, duration_ms=500):
        iw, ih = image.get_size()
        anim = {
            'type': 'use',
            'image': image,
            'start_pos': tuple(start_pos),
            'end_pos': tuple(target_pos),
            'start_time': pygame.time.get_ticks(),
            'duration': duration_ms,
            'start_scale': 1.0,
            'end_scale': 0.2,
            'start_alpha': 255,
            'end_alpha': 0,
            'size': (iw, ih)
        }
        self.animations.append(anim)

    def update_and_render_animations(self):
        now = pygame.time.get_ticks()
        to_remove = []
        for anim in self.animations:
            t = min(1.0, (now - anim['start_time']) / anim['duration'])
            x = anim['start_pos'][0] + (anim['end_pos'][0] - anim['start_pos'][0]) * t
            y = anim['start_pos'][1] + (anim['end_pos'][1] - anim['start_pos'][1]) * t
            scale = anim['start_scale'] + (anim['end_scale'] - anim['start_scale']) * t
            alpha = int(anim['start_alpha'] + (anim['end_alpha'] - anim['start_alpha']) * t)
            if anim['image']:
                iw, ih = anim['size']
                w = max(1, int(iw * scale))
                h = max(1, int(ih * scale))
                img = pygame.transform.smoothscale(anim['image'], (w, h))
                img.set_alpha(alpha)
                draw_rect = img.get_rect(center=(int(x), int(y)))
                self.screen.blit(img, draw_rect)
            if t >= 1.0:
                to_remove.append(anim)
        for anim in to_remove:
            self.animations.remove(anim)

    def get_slot_center(self, index):
        sx = self.inv_x + index * (self.slot_size + self.inv_padding)
        sy = self.inv_y
        return (sx + self.slot_size // 2, sy + self.slot_size // 2)

    # ---------------- Click / Drag ----------------
    def dragging_item_dropped(self, x, y, item):
        # Room 3 fragments
        room3_names = [frag.name for frag in self.room3_items]
        if item['name'] in room3_names:
            # find the original fragment object
            frag = next(f for f in self.room3_items if f.name == item['name'])
            frag.is_collected = False
            frag.rect.topleft = frag.home_pos
            self.show_message(f"You dropped a shard back onto the floor.")
        elif item['name'] == 'key':
            self.key = Item(x - 16, y - 16, 32, 32, YELLOW, "key")
            self.key.is_collected = False
            self.has_key = False
            self.show_message("You dropped the key back onto the chest.")
        else:
            self.show_message(f"Dropped {item['name']} into the room.")
    def draw_inventory(self, mouse_pos, mouse_pressed):
        hovered_slot = None
        for i in range(self.slot_count):
            sx = self.inv_x + i * (self.slot_size + self.inv_padding)
            sy = self.inv_y
            slot_rect = pygame.Rect(sx, sy, self.slot_size, self.slot_size)
            if SLOT_IMAGE:
                try:
                    self.screen.blit(pygame.transform.scale(SLOT_IMAGE, (self.slot_size, self.slot_size)), slot_rect)
                except Exception:
                    pygame.draw.rect(self.screen, DARK_GRAY, slot_rect)
            else:
                pygame.draw.rect(self.screen, DARK_GRAY, slot_rect)
            pygame.draw.rect(self.screen, BLACK, slot_rect, 2)

            if i < len(self.inventory):
                item = self.inventory[i]
                if item.get('image'):
                    try:
                        img = pygame.transform.scale(item['image'], (self.slot_size - 10, self.slot_size - 10))
                        self.screen.blit(img, (sx + 5, sy + 5))
                    except Exception:
                        pygame.draw.rect(self.screen, YELLOW, (sx + 5, sy + 5, self.slot_size - 10, self.slot_size - 10))
                else:
                    pygame.draw.rect(self.screen, YELLOW, (sx + 5, sy + 5, self.slot_size - 10, self.slot_size - 10))

                if slot_rect.collidepoint(mouse_pos) and mouse_pressed and not self.dragging_item:
                    self.dragging_item = item
                    self.drag_offset = (slot_rect.x - mouse_pos[0], slot_rect.y - mouse_pos[1])
                    self.inventory.remove(item)
                    hovered_slot = item
        return hovered_slot

    def handle_click(self, pos):
        # ---------- Room 2 keypad ----------
        if self.current_room == 2:
            result = self.keypad.check_click(pos)
            if result:
                self.show_message(f"Code entered: {result}")
                if result == "25167":
                    self.rope.is_collected = False
                    self.rope_animating = True
                    self.rope.rect.y = -self.rope.rect.height
                    self.show_message("You hear the noise of a rope descending nearby.")
                return

        # ---------- Key pickup ----------
        if self.current_room == 1 and not self.key.is_collected and self.key.rect.collidepoint(pos):
            self.key.is_collected = True
            self.has_key = True
            if not any(it['name']=='key' for it in self.inventory):
                self.inventory.append({'name': 'key', 'image': KEY_IMAGE, 'desc': 'A small brass key'})
            self.start_pickup_animation(KEY_IMAGE, self.key.rect.center, len(self.inventory)-1)
            self.show_message("Picked up the key!")
            return

        # ---------- Chest drag ----------
        if self.current_room == 1 and self.chest.start_drag(pos):
            return

        # ---------- Door ----------
        if self.door.rect.collidepoint(pos):
            if self.current_room == 1:
                if not self.door.is_open:
                    if self.chest.rect.colliderect(self.door.rect):
                        self.show_message("The chest is blocking the door")
                    elif not self.has_key:
                        self.show_message("You need the key to open the door")
                    else:
                        self.door.is_open = True
                        if OPEN_SOUND:
                            try: OPEN_SOUND.play()
                            except Exception: pass
                        self.start_use_animation(KEY_IMAGE, pos, pos, duration_ms=600)
                        self.inventory = [it for it in self.inventory if it.get('name') != 'key']
                        self.has_key = False
                        self.show_message("You opened the door!")
                else:
                    self.start_room_transition(2)
                    self.show_message("You entered the next room.")
            elif self.current_room == 2:
                self.start_room_transition(1)
                self.show_message("You returned to the first room.")

        # ---------- Rope click ----------
        if self.current_room == 1 and not self.rope.is_collected and self.rope.rect.collidepoint(pos):
            # Check if chest is under the rope
            chest_center_x = self.chest.rect.centerx
            rope_center_x = self.rope.rect.centerx
            tolerance = 50  # pixels allowance
            if abs(chest_center_x - rope_center_x) <= tolerance:
                self.start_room_transition(3)
                self.show_message("You grab the rope and ascend to an attic.")
                self.rope.is_collected = True  # rope disappears after use
            else:
                self.show_message("The rope is too high. How can you reach it?")

        # Room 3 items pickup
        if self.current_room == 3:
            for item in self.room3_items:
                if not item.is_collected and item.rect.collidepoint(pos):
                    item.is_collected = True
                    # Add to inventory
                    self.inventory.append({
                        'name': item.name,
                        'image': FRAGMENT_IMAGE,  # can keep None if you want
                        'desc': 'A ceramic shard'
                    })
                    # create temporary image for animation
                    fragment_img = pygame.Surface((item.rect.width, item.rect.height))
                    fragment_img.fill(item.color)
                    self.start_pickup_animation(fragment_img, item.rect.center, len(self.inventory)-1)
                    self.show_message("Picked up a ceramic shard.")
                    return




    # ---------------- Main Loop ----------------
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.transition_direction == 0:
                        self.handle_click(e.pos)
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    self.chest.stop_drag()
                elif e.type == pygame.MOUSEMOTION:
                    self.chest.update(e.pos)

            self.screen.blit(self.backgrounds[self.current_room], (0,0))

            # Key stays on chest
            if self.current_room == 1 and not self.key.is_collected:
                self.key.rect.centerx = self.chest.rect.centerx
                self.key.rect.y = self.chest.rect.y - self.key.rect.height - 5

            # Draw room objects
            if self.current_room == 1:
                self.door.draw(self.screen)
                self.chest.draw(self.screen)
                self.key.draw(self.screen)
                if not self.rope.is_collected:
                    # Animate rope dropping
                    if self.rope_animating:
                        self.rope.rect.y += 8
                        if self.rope.rect.y >= self.rope_target_y:
                            self.rope.rect.y = self.rope_target_y
                            self.rope_animating = False
                    self.rope.draw(self.screen)
            elif self.current_room == 2:
                self.door.draw(self.screen)
                self.keypad.draw(self.screen, self.font)
            elif self.current_room == 3:
                self.door.draw(self.screen)
                for item in self.room3_items:
                    item.draw(self.screen)

            # Inventory
            hovered_slot = self.draw_inventory(mouse_pos, mouse_pressed)
            if self.dragging_item:
                try:
                    drag_img = pygame.transform.scale(self.dragging_item.get('image'), (self.slot_size - 10, self.slot_size - 10))
                    self.screen.blit(drag_img, (mouse_pos[0] + self.drag_offset[0] + 20, mouse_pos[1] + self.drag_offset[1] + 20))
                except Exception:
                    pygame.draw.rect(self.screen, YELLOW, (mouse_pos[0]+20, mouse_pos[1]+20, self.slot_size-10, self.slot_size-10))
                if not mouse_pressed:
                    self.dragging_item_dropped(*mouse_pos, self.dragging_item)
                    self.dragging_item = None

            if hovered_slot:
                desc = self.small_font.render(hovered_slot.get('desc', ''), True, WHITE)
                tip_bg = pygame.Surface((desc.get_width() + 10, desc.get_height() + 6))
                tip_bg.fill(DARK_GRAY)
                pygame.draw.rect(tip_bg, WHITE, tip_bg.get_rect(), 1)
                self.screen.blit(tip_bg, (mouse_pos[0]+10, mouse_pos[1]+10))
                self.screen.blit(desc, (mouse_pos[0]+15, mouse_pos[1]+13))

            self.update_and_render_animations()
            self.update_transition()

            if self.message_timer > 0:
                self.message_timer -= 1
            if self.message:
                msg = self.font.render(self.message, True, YELLOW)
                self.screen.blit(msg, (WINDOW_WIDTH - msg.get_width() - 10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

# ---------------- Run ----------------
if __name__ == "__main__":
    Game().run()
 
