#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon

def main() -> None:
    tile_width = 10
    tile_height = 10

    screen_width = 1600
    screen_height = 900

    map_width = screen_width // tile_width
    map_height = screen_height // tile_height

    room_max_size = 20
    room_min_size = 10
    max_rooms = 12

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(map_width / 2), int(map_height / 2), "@", (255, 255, 255))
    npc = Entity(int(map_width / 2 - 5), int(map_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new(
            width=screen_width,
            height=screen_height,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial",
            vsync=True,
    ) as context:
        root_console = tcod.console.Console(map_width, map_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
