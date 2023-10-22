import hydra
import pygame
from omegaconf import DictConfig

from .visualizer import PyGameVisualizer
from .world import World


def poll_event() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


def non_interactive_mode(
    world: World, visualizer: PyGameVisualizer, surface: pygame.Surface, clock: pygame.time.Clock
) -> None:
    while not world.wave_function_collapse():
        pass

    visualizer.update()

    while True:
        if poll_event():
            break
        visualizer.draw(surface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def interactive_mode(
    world: World, visualizer: PyGameVisualizer, surface: pygame.Surface, clock: pygame.time.Clock
) -> None:
    is_running = True
    is_paused = False

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_RIGHT and is_paused:
                    world.wave_function_collapse()
                    visualizer.update()

        if not is_paused and not world.is_collapsed:
            world.wave_function_collapse()
            visualizer.update()

        visualizer.draw(surface)
        pygame.display.flip()
        clock.tick(60)


@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig) -> None:
    pygame.init()
    clock = pygame.time.Clock()

    size_x = cfg.WORLD.WIDTH * cfg.TILE.SIZE * cfg.TILE.SCALE
    size_y = cfg.WORLD.HEIGHT * cfg.TILE.SIZE * cfg.TILE.SCALE
    display_surface = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("Wave Function Collapse")

    world = World(cfg)
    visualizer = PyGameVisualizer(world, cfg)

    if cfg.RUN.interactive:
        interactive_mode(world, visualizer, display_surface, clock)
    else:
        non_interactive_mode(world, visualizer, display_surface, clock)


if __name__ == "__main__":
    main()

