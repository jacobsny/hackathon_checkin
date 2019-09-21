#!/usr/bin/env python
import os, pygame, argparse, math, sys

settings = {'resolution': (1280, 72), 'fullscreen': False, 'preserve_aspect_ratio': True, 'framerate': 30, 'debug': True, 'directory': '/hackathon_checkin/slideshow', 'transition': 'fade', 'transitiontime': 1, 'imagetime': 50000}

def debug(msg):
    if settings.get('debug'):
        print(msg)

class Image:
    def __init__(self, path, settings):
        self.img = pygame.image.load(path).convert()

        if settings.get('preserve_aspect_ratio'):
            imgsize = self.img.get_size()
            ratio = min(settings['resolution'][0] / float(imgsize[0]), settings['resolution'][1] / float(imgsize[1]))
            tmpimg = pygame.transform.smoothscale(self.img, (int(imgsize[0] * ratio), int(imgsize[1] * ratio)))

            tmpimgsize = tmpimg.get_size()
            pos = ((settings['resolution'][0] - tmpimgsize[0]) / 2, (settings['resolution'][1] - tmpimgsize[1]) / 2)

            self.img = pygame.Surface(settings['resolution'])
            self.img.blit(tmpimg, pos)

        else:
            self.img = pygame.transform.smoothscale(self.img, settings['resolution'])


        self.alpha = 255

    def draw(self, surf):
        self.img.set_alpha(int(self.alpha))
        surf.blit(self.img, (0,0))

class Main:
    def __init__(self, settings):
        self.settings = settings

        files = os.listdir(self.settings['directory'][0])
        self.paths = []
        for f in files:
            self.paths.append(os.path.join(self.settings['directory'][0], f))

        self.clock = pygame.time.Clock()
        if not self.settings.get('resolution'):
            if self.settings.get('fullscreen'):
                self.settings['resolution'] = pygame.display.list_modes()[0]
            else:
                self.settings['resolution'] = (800,600)

        if self.settings.get('fullscreen'):
            self.screen = pygame.display.set_mode(self.settings['resolution'], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.settings['resolution'])
        pygame.display.set_caption("Slider")

        self.index = 0
        self.currimg = self.load_image()
        self.currimg.draw(self.screen)
        pygame.display.flip()

    def load_image(self):
        try:
            path = self.paths[self.index]
        except IndexError:
            self.index = 0
            path = self.paths[0]

        image = False
        while not image:
            try:
                image = Image(path, self.settings)
            except pygame.error:
                debug('Could not load file "' + path + '", skipping.')
                self.paths.remove(path)
                image = self.load_image() # Recursion, n.: See recursion.

            return image

    def transition(self):
        self.index += 1
        previmg = self.currimg
        self.currimg = self.load_image()

        if self.settings['transition'] == 'none':
            self.currimg.draw(self.screen)
            pygame.display.flip()

        elif self.settings['transition'] == 'fade':
            steps = self.settings['framerate'] * self.settings['transition_time']
            stepsize = 255.0 / steps
            
            self.currimg.alpha = 0

            for step in range(0, int(math.floor(steps))):
                self.screen.fill([0,0,0])
                previmg.draw(self.screen)
                
                self.currimg.alpha = self.currimg.alpha + stepsize
                self.currimg.draw(self.screen)
                pygame.display.flip()

                self.clock.tick(self.settings['framerate'])

            self.currimg.alpha = 255
            self.currimg.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slider - Simple Image Slideshow')
    parser.add_argument('directory', metavar='[path]', type=str, nargs=1, help='Path to directory containing images to be displayed.')
    parser.add_argument('--resolution', '-r', metavar='HeightxWidth', type=lambda s: (int(s.split('x')[0]), int(s.split('x')[1])), nargs='?', help='Resolution of display window.')
    parser.add_argument('--fullscreen', '-f', action='store_true', help='Enables fullscreen display.')
    parser.add_argument('--preserve-aspect-ratio', '-p', action='store_true', help='Preserves aspect ratio of images when resizing.')
    parser.add_argument('--transition', '-t', default='fade', type=str, nargs='?', help='Sets image transition type, can be "fade" or "none".')
    parser.add_argument('--transition-time', '-s', default=1, type=float, nargs='?', help='Sets speed of image transition, in seconds.')
    parser.add_argument('--image-time', '-i', default=5, type=float, nargs='?', help='Sets amount of time each image is displayed, in seconds.')
    parser.add_argument('--framerate', default=30, type=int, nargs='?', help='Sets program framerate, in frames per second.')
    parser.add_argument('--debug', '-d', action='store_true', help='Enables program debugging output.')

    settings = vars(parser.parse_args())
    debug("settings:" + str(settings))

    pygame.init()

    main = Main(settings)

    pygame.time.set_timer(pygame.USEREVENT, int(settings['image_time'] * 1000))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); quit()
            if event.type == pygame.USEREVENT:
                main.transition()
