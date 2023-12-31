import pygame
import random
import os

DARK_RED = (139, 0, 0)
YELLOW = (235, 195, 65)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (30, 144, 255)
CYAN = (47, 237, 237)
RED = (194, 57, 33)
LIME_GREEN = (50, 205, 50)
LIGHT_RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
LIGHT_PINK = (255, 182, 193)
DARK_GREEN = (1, 100, 32)
PURPLE = (181, 60, 177)
BROWN = (150, 75, 0)
DARK_GREY = (52, 52, 52)


class Memory:
    """
    Class used to store data across game instances
    """
    def __init__(self, width, height):
        self.res_width = width
        self.res_height = height
        self.music = None

    def load_game(self):
        """ Load previous game instance, usually from a text_file"""
        pass

    def load_scenes(self):
        """ Load all scenes from a text file"""
        pass


class Text:
    """
    Class used to simplify text creation for pygame
    """

    def __init__(self, text, text_pos, font_size, font_type,
                 font_color, text_other):
        self.text = text  # Text as a string
        self.position = text_pos  # Text position as a tuple or list (x and y)
        self.font_size = int(font_size)  # Int determining how big the text is
        self.font_type = font_type  # String used to indicate what font
        """Font selection is determined by your computer and it's preset fonts
        """
        self.color = font_color
        """A constant string for a tuple or a tuple using RGB values"""
        self.other = text_other
        """PLACEHOLDER for any other variables needed or desired in text"""
        self.font = None  # Initialized here, defined in setup()
        self.text_rect = None  # Initialized here, defined in render()
        self.text_img = None  # Initialized here, defined in render()

        self.setup()  # Called to set up the font
        self.render()
        """Called to continuously update the position, rect, color, and text
        """

    def setup(self):
        """
        Uses font type and size to translate into pygame text font
        to make self.font
        """
        self.font = pygame.font.SysFont(self.font_type, self.font_size)

    def render(self):
        """
        Creates self.text_img or the pygame image of the text using self.text,
            self.color.
        Creates self.text_rect, or a rect object using the size of the text.
        Then centers the rect around the text (or the defined position)
        """
        self.text_img = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = self.position

    def scale(self, width, height):
        self.position = list(self.position)
        self.position[0] = int(self.position[0] * width)
        self.position[1] = int(self.position[1] * height)
        self.position = tuple(self.position)
        self.font_size = int(self.font_size * max(width, height))

        # Apply those changes
        self.setup()
        self.render()


class Music:
    """
    Music class containing tracks available and the current music playing.
    Also responsible for music volume and music switching.
    """

    def __init__(self, perc_vol, music_folder, width, height):
        self.music_tracks = []  # Put file_name for music here
        music_files = os.listdir("songs/")
        for each_song in music_files:
            self.music_tracks += [each_song]
        self.end = pygame.USEREVENT + 0    # Unique event, for when music ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 0)
        # Everytime music ends, return the event

        self.folder_path = music_folder   # Folder path for audio

        self.current_track_index = 0    # Everything but the main menu theme

        self.perc_vol = perc_vol   # Volume set by the player as a percentage
        self.music_vol = 0              # Adjustable music volume
        self.vol_time = pygame.time.get_ticks()     # Increment music with time
        self.max_vol = 1 * self.perc_vol / 100   # Max volume possible for music
        # Change 1 value for changing music

        self.res_width = width
        self.res_height = height

        """pygame.mixer.music.load(self.folder_path + self.music_tracks[0])"""
        #   Load this music up upon loading

        pygame.mixer.music.set_volume(self.max_vol)     # Set to max for now
        # pygame.mixer.music.play(-1)
        # Start with this song and play forever
        if 0 < len(self.music_tracks):
            self.music_text = Text("PLAYING: " +
                                   str(self.music_tracks[self.current_track_index]),
                                   (self.res_width / 2, self.res_height -
                                    (self.res_height / 10)), 20,
                                   "impact", WHITE, None)
        self.text_timer = pygame.time.get_ticks()
        # Display what's currently playing

    def switch_music(self):
        # Reset music display timer
        self.text_timer = pygame.time.get_ticks()

        # Choose a random track index
        self.music_vol = 0
        self.current_track_index = random.randint(1, len(self.music_tracks) - 2)
        # Set the boundaries between 2nd/1 and 2nd last/len - 2 to avoid
        # main menu and credits

        # Update the music display text
        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (self.res_width / 2, self.res_height -
                                (self.res_height / 10)),
                               20, "impact", WHITE, None)

        # Load the selected track
        pygame.mixer.music.load(self.folder_path +
                                (self.music_tracks[self.current_track_index]))

        # Set the volume
        pygame.mixer.music.set_volume(self.music_vol)

        pygame.mixer.music.play(0, 0, 0)  # Play the music once

    def set_music(self, track_num, vol, loops, start, fade_in):
        # Set the max volume
        self.max_vol = 0.7 * self.perc_vol / 100

        # Reset music display timer
        self.text_timer = pygame.time.get_ticks()

        # Update the current track index
        self.current_track_index = track_num

        # Update the music display text
        self.music_text = Text("PLAYING: " +
                               str(self.music_tracks[self.current_track_index]),
                               (self.res_width / 2, self.res_height -
                                (self.res_height / 10)),
                               20, "impact", WHITE, None)

        # Load the selected track
        pygame.mixer.music.load(self.folder_path +
                                (self.music_tracks[self.current_track_index]))

        # Set the volume
        self.music_vol = vol * self.perc_vol / 100
        pygame.mixer.music.set_volume(self.music_vol)

        pygame.mixer.music.play(loops, start, fade_in)  # Play the music

    def transition_music(self):
        # Slowly increase volume of music (0.01 every 0.075 seconds)
        # until volume reaches the max (0.7 or self.max_vol)
        # set the new self.max_vol if changed
        self.max_vol = 0.7 * self.perc_vol / 100
        while self.music_vol < self.max_vol and \
                75 < pygame.time.get_ticks() - self.vol_time:
            self.music_vol += 0.01  # Increase volume
            pygame.mixer.music.set_volume(self.music_vol)   # Update volume
            self.vol_time = pygame.time.get_ticks()     # Reset timer


class Scene:
    """
    Class template for creating scene based games
    """

    def __init__(self):
        """
        self.this_scene will tell the current scene it's on at that moment.
        Currently, it's set to itself, which means the
        current scene is this one.
        """
        self.this_scene = self
        self.run_scene = True
        self.level_id = -1

    def input(self, pressed, held):
        # this will be overridden in subclasses
        """
        This function should contain the pressed for loop and other held
        buttons. Pressing or holding these buttons should cause something
        to change such as a class variable (+= 1, True/False, change str.. etc.)
        or call another function.

        :param pressed: Detect buttons that are pressed (like if held, it will
        only be updated with the initial press)
        :param held: Detect buttons that are held down
        :return:
        """
        pass

    def update(self):
        # this will be overridden in subclasses
        """
        This function should check for variables that need to be updated
        continuously. A good way to distinguish this from input is that this
        update function doesn't directly respond from a button press. For
        example, let's have input add to self.x by 1, or self.x += 1. Then, if
        we wanted to keep self.x within the bounds of 0 to 10, we check for that
        in update. In update, we'd use if self.x < 0 and 10 < self.x to check
        whenever self.x goes out of these bounds to then reset self.x.

        :return:
        """
        pass

    def render(self, screen):
        # this will be overridden in subclasses
        """
        This function is solely used for rendering purposes such as
        screen.blit or pygame.draw
        :param screen:
        :return:
        """
        pass

    def change_scene(self, next_scene):
        """
        This function is used in the main pygame loop. This function is
        responsible for formally changing the scene
        """
        self.this_scene = next_scene

    def close_game(self):
        """
        Set the current scene to nothing and is used to stop the game.
        This function is responsible for ending the game loop (or scene)
        formally.
        """
        self.change_scene(None)


class Program:
    """
    Class responsible for how the game runs
    """
    def __init__(self, width, height) -> None:
        self.running = True     # Determines if the game is running
        self.memory = Memory(width, height)     # Initialize game memory

        self.memory.music = Music(100, "example_file_path", width, height)

    def run(self, width, height, current_scene):
        """
        Where the actual game loop is running.
        Everything game related is defined in scene.
        Scene is initialized by running Program (in main
        which is outer scope) with the screen size and scene.
        At this point in time, scene is run as MenuScene.

        Everything relating to calling the scene is called here, such as
        input, update, and render while the game is running.

        If the game isn't running, then in the final loop (or the loop when
        the game is told to close by various means), self.running is set to
        false and the scene is changed to nothing. Then the game is safe to
        close.

        This is also where inputs are collected before they are sent to
        the inputs for scene.

        Finally, this is where FPS is set and where the display is updated.
        """
        # self.memory.screen = pygame.display.set_mode([width, height])
        screen = pygame.display.set_mode([width, height])  # Set screen size

        pygame.scrap.init()
        if not pygame.scrap.get_init():
            raise Exception("pygame.scrap is no longer supported :(")

        # Put the resolution ratio into memory, where 1080 and 576 are the min

        scene = current_scene   # Set scene currently shown through a parameter
        # Start game loop
        while self.running:
            keys_pressed = []   # Keys pressed/tapped (key press)
            keys_held = pygame.key.get_pressed()    # Keys held collected
            for event in pygame.event.get():    # Collect all key presses
                # Quit condition if you press the X on the top right
                if event.type == pygame.QUIT:
                    # self.memory - write to your save here
                    self.running = False    # Stop running this loop
                    pygame.mixer.music.stop()   # Stop the music
                    scene.run_scene = False     # Tell scene to stop running
                # If player does a keypress, append to our list for key presses
                if event.type == pygame.KEYDOWN:
                    keys_pressed.append(event.key)

                """if event.type == self.memory.music.end:
                    self.memory.music.switch_music()"""

            # Stop the game using other conditions (running, but scene says off)
            if self.running and not scene.run_scene:
                # self.memory - write to your save here
                self.running = False    # Stop running this loop
                pygame.mixer.music.stop()   # Stop the music
                scene.close_game()      # Tell scene to shut off
            else:
                # Functional game loop

                scene.input(keys_pressed, keys_held)    # Call to use keys in
                scene.update()  # Call to dynamically use/update/check changes
                scene.render(screen)    # Visually render desired graphics
                scene = scene.this_scene
                """This line is important to allow changing scenes (if 
                this_scene is different like using 
                scene.change_scene(next_scene). Otherwise, scene will not be 
                changed and will continue being this scene (same memory
                address, no change)."""

                """if 0 != scene.level_id:
                    self.memory.music.transition_music()"""

            fps.tick(120)   # 120 frames per second
            pygame.display.update()     # Update the visual output dynamically


if __name__ == "__main__":
    pygame.init()   # Initialize pygame
    pygame.mixer.init()  # Initialize pygame's sound

    fps = pygame.time.Clock()   # Initialize the frame rate

    # Alter these values to change the resolution
    game_width = 1280
    game_height = 720

    file_path = "put_icon_file_path_here"
    """pygame.display.set_caption("display_window") # game window caption
    icon = pygame.image.load(file_path + "file_image_name") # loading image
    default_icon_image_size = (32, 32) # reducing size of image
    icon = pygame.transform.scale(icon, default_icon_image_size) 
    # scaling image correctly
    pygame.display.set_icon(icon) # game window icon"""

    start_game = Program(game_width, game_height)
    # Initialize running the game with Program
    start_scene = Scene()
    # Initialize the first scene/starting scene shown to the player
    start_game.run(game_width, game_height, start_scene)  # Run the game loop
    """The game loop will be stuck at this line (start_game.run) until the
    while loop (while self.running:) is no longer true. When self.running is
    False, the program will move onto the next line to quit"""

    pygame.quit()   # Quit the game/pygame instance
