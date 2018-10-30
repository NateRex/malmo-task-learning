# ==============================================================================================
# This file contains enumerated types and constant values commonly used in setting
# up scenarios to be ran by Malmo.
# ==============================================================================================
from enum import Enum

NUMBER_OF_INVENTORY_SLOTS = 40
STRIKING_DISTANCE = 2.8

class BlockType(Enum):
    Air = "air"
    Stone = "stone"
    Grass = "grass"
    Dirt = "dirt"
    Cobblestone = "cobblestone"
    Planks = "planks"
    Sapling = "sapling"
    Bedrock = "bedrock"
    Flowing_water = "flowing_water"
    Water = "water"
    Flowing_lava = "flowing_lava"
    Lava = "lava"
    Sand = "sand"
    Gravel = "gravel"
    Gold_ore = "gold_ore"
    Iron_ore = "iron_ore"
    Coal_ore = "coal_ore"
    Log = "log"
    Leaves = "leaves"
    Sponge = "sponge"
    Glass = "glass"
    Lapis_ore = "lapis_ore"
    Lapis_block = "lapis_block"
    Dispenser = "dispenser"
    Sandstone = "sandstone"
    Noteblock = "noteblock"
    Bed = "bed"
    Golden_rail = "golden_rail"
    Detector_rail = "detector_rail"
    Sticky_piston = "sticky_piston"
    Web = "web"
    Tallgrass = "tallgrass"
    Deadbush = "deadbush"
    Piston = "piston"
    Piston_head = "piston_head"
    Wool = "wool"
    Piston_extension = "piston_extension"
    Yellow_flower = "yellow_flower"
    Red_flower = "red_flower"
    Brown_mushroom = "brown_mushroom"
    Red_mushroom = "red_mushroom"
    Gold_block = "gold_block"
    Iron_block = "iron_block"
    Double_stone_slab = "double_stone_slab"
    Stone_slab = "stone_slab"
    Brick_block = "brick_block"
    Tnt = "tnt"
    Bookshelf = "bookshelf"
    Mossy_cobblestone = "mossy_cobblestone"
    Obsidian = "obsidian"
    Torch = "torch"
    Fire = "fire"
    Mob_spawner = "mob_spawner"
    Oak_stairs = "oak_stairs"
    Chest = "chest"
    Redstone_wire = "redstone_wire"
    Diamond_ore = "diamond_ore"
    Diamond_block = "diamond_block"
    Crafting_table = "crafting_table"
    Wheat = "wheat"
    Farmland = "farmland"
    Furnace = "furnace"
    Lit_furnace = "lit_furnace"
    Standing_sign = "standing_sign"
    Wooden_door = "wooden_door"
    Ladder = "ladder"
    Rail = "rail"
    Stone_stairs = "stone_stairs"
    Wall_sign = "wall_sign"
    Lever = "lever"
    Stone_pressure_plate = "stone_pressure_plate"
    Iron_door = "iron_door"
    Wooden_pressure_plate = "wooden_pressure_plate"
    Redstone_ore = "redstone_ore"
    Lit_redstone_ore = "lit_redstone_ore"
    Unlit_redstone_torch = "unlit_redstone_torch"
    Redstone_torch = "redstone_torch"
    Stone_button = "stone_button"
    Snow_layer = "snow_layer"
    Ice = "ice"
    Snow = "snow"
    Cactus = "cactus"
    Clay = "clay"
    Reeds = "reeds"
    Jukebox = "jukebox"
    Fence = "fence"
    Pumpkin = "pumpkin"
    Netherrack = "netherrack"
    Soul_sand = "soul_sand"
    Glowstone = "glowstone"
    Portal = "portal"
    Lit_pumpkin = "lit_pumpkin"
    Cake = "cake"
    Unpowered_repeater = "unpowered_repeater"
    Powered_repeater = "powered_repeater"
    Stained_glass = "stained_glass"
    Trapdoor = "trapdoor"
    Monster_egg = "monster_egg"
    Stonebrick = "stonebrick"
    Brown_mushroom_block = "brown_mushroom_block"
    Red_mushroom_block = "red_mushroom_block"
    Iron_bars = "iron_bars"
    Glass_pane = "glass_pane"
    Melon_block = "melon_block"
    Pumpkin_stem = "pumpkin_stem"
    Melon_stem = "melon_stem"
    Vine = "vine"
    Fence_gate = "fence_gate"
    Brick_stairs = "brick_stairs"
    Stone_brick_stairs = "stone_brick_stairs"
    Mycelium = "mycelium"
    Waterlily = "waterlily"
    Nether_brick = "nether_brick"
    Nether_brick_fence = "nether_brick_fence"
    Nether_brick_stairs = "nether_brick_stairs"
    Nether_wart = "nether_wart"
    Enchanting_table = "enchanting_table"
    Brewing_stand = "brewing_stand"
    Cauldron = "cauldron"
    End_portal = "end_portal"
    End_portal_frame = "end_portal_frame"
    End_stone = "end_stone"
    Dragon_egg = "dragon_egg"
    Redstone_lamp = "redstone_lamp"
    Lit_redstone_lamp = "lit_redstone_lamp"
    Double_wooden_slab = "double_wooden_slab"
    Wooden_slab = "wooden_slab"
    Cocoa = "cocoa"
    Sandstone_stairs = "sandstone_stairs"
    Emerald_ore = "emerald_ore"
    Ender_chest = "ender_chest"
    Tripwire_hook = "tripwire_hook"
    Tripwire = "tripwire"
    Emerald_block = "emerald_block"
    Spruce_stairs = "spruce_stairs"
    Birch_stairs = "birch_stairs"
    Jungle_stairs = "jungle_stairs"
    Command_block = "command_block"
    Beacon = "beacon"
    Cobblestone_wall = "cobblestone_wall"
    Flower_pot = "flower_pot"
    Carrots = "carrots"
    Potatoes = "potatoes"
    Wooden_button = "wooden_button"
    Skull = "skull"
    Anvil = "anvil"
    Trapped_chest = "trapped_chest"
    Light_weighted_pressure_plate = "light_weighted_pressure_plate"
    Heavy_weighted_pressure_plate = "heavy_weighted_pressure_plate"
    Unpowered_comparator = "unpowered_comparator"
    Powered_comparator = "powered_comparator"
    Daylight_detector = "daylight_detector"
    Redstone_block = "redstone_block"
    Quartz_ore = "quartz_ore"
    Hopper = "hopper"
    Quartz_block = "quartz_block"
    Quartz_stairs = "quartz_stairs"
    Activator_rail = "activator_rail"
    Dropper = "dropper"
    Stained_hardened_clay = "stained_hardened_clay"
    Stained_glass_pane = "stained_glass_pane"
    Leaves2 = "leaves2"
    Log2 = "log2"
    Acacia_stairs = "acacia_stairs"
    Dark_oak_stairs = "dark_oak_stairs"
    Slime = "slime"
    Barrier = "barrier"
    Iron_trapdoor = "iron_trapdoor"
    Prismarine = "prismarine"
    Sea_lantern = "sea_lantern"
    Hay_block = "hay_block"
    Carpet = "carpet"
    Hardened_clay = "hardened_clay"
    Coal_block = "coal_block"
    Packed_ice = "packed_ice"
    Double_plant = "double_plant"
    Standing_banner = "standing_banner"
    Wall_banner = "wall_banner"
    Daylight_detector_inverted = "daylight_detector_inverted"
    Red_sandstone = "red_sandstone"
    Red_sandstone_stairs = "red_sandstone_stairs"
    Double_stone_slab2 = "double_stone_slab2"
    Stone_slab2 = "stone_slab2"
    Spruce_fence_gate = "spruce_fence_gate"
    Birch_fence_gate = "birch_fence_gate"
    Jungle_fence_gate = "jungle_fence_gate"
    Dark_oak_fence_gate = "dark_oak_fence_gate"
    Acacia_fence_gate = "acacia_fence_gate"
    Spruce_fence = "spruce_fence"
    Birch_fence = "birch_fence"
    Jungle_fence = "jungle_fence"
    Dark_oak_fence = "dark_oak_fence"
    Acacia_fence = "acacia_fence"
    Spruce_door = "spruce_door"
    Birch_door = "birch_door"
    Jungle_door = "jungle_door"
    Acacia_door = "acacia_door"
    Dark_oak_door = "dark_oak_door"
    End_rod = "end_rod"
    Chorus_plant = "chorus_plant"
    Chorus_flower = "chorus_flower"
    Purpur_block = "purpur_block"
    Purpur_pillar = "purpur_pillar"
    Purpur_stairs = "purpur_stairs"
    Purpur_double_slab = "purpur_double_slab"
    Purpur_slab = "purpur_slab"
    End_bricks = "end_bricks"
    Beetroots = "beetroots"
    Grass_path = "grass_path"
    End_gateway = "end_gateway"
    Repeating_command_block = "repeating_command_block"
    Chain_command_block = "chain_command_block"
    Frosted_ice = "frosted_ice"
    Magma = "magma"
    Nether_wart_block = "nether_wart_block"
    Red_nether_brick = "red_nether_brick"
    Bone_block = "bone_block"
    Structure_void = "structure_void"
    Observer = "observer"
    White_shulker_box = "white_shulker_box"
    Orange_shulker_box = "orange_shulker_box"
    Magenta_shulker_box = "magenta_shulker_box"
    Light_blue_shulker_box = "light_blue_shulker_box"
    Yellow_shulker_box = "yellow_shulker_box"
    Lime_shulker_box = "lime_shulker_box"
    Pink_shulker_box = "pink_shulker_box"
    Gray_shulker_box = "gray_shulker_box"
    Silver_shulker_box = "silver_shulker_box"
    Cyan_shulker_box = "cyan_shulker_box"
    Purple_shulker_box = "purple_shulker_box"
    Blue_shulker_box = "blue_shulker_box"
    Brown_shulker_box = "brown_shulker_box"
    Green_shulker_box = "green_shulker_box"
    Red_shulker_box = "red_shulker_box"
    Black_shulker_box = "black_shulker_box"
    Structure_block = "structure_block"

class ItemType(Enum):
    Iron_shovel = "iron_shovel"
    Iron_pickaxe = "iron_pickaxe"
    Iron_axe = "iron_axe"
    Flint_and_steel = "flint_and_steel"
    Apple = "apple"
    Bow = "bow"
    Arrow = "arrow"
    Coal = "coal"
    Diamond = "diamond"
    Iron_ingot = "iron_ingot"
    Gold_ingot = "gold_ingot"
    Iron_sword = "iron_sword"
    Wooden_sword = "wooden_sword"
    Wooden_shovel = "wooden_shovel"
    Wooden_pickaxe = "wooden_pickaxe"
    Wooden_axe = "wooden_axe"
    Stone_sword = "stone_sword"
    Stone_shovel = "stone_shovel"
    Stone_pickaxe = "stone_pickaxe"
    Stone_axe = "stone_axe"
    Diamond_sword = "diamond_sword"
    Diamond_shovel = "diamond_shovel"
    Diamond_pickaxe = "diamond_pickaxe"
    Diamond_axe = "diamond_axe"
    Stick = "stick"
    Bowl = "bowl"
    Mushroom_stew = "mushroom_stew"
    Golden_sword = "golden_sword"
    Golden_shovel = "golden_shovel"
    Golden_pickaxe = "golden_pickaxe"
    Golden_axe = "golden_axe"
    String = "string"
    Feather = "feather"
    Gunpowder = "gunpowder"
    Wooden_hoe = "wooden_hoe"
    Stone_hoe = "stone_hoe"
    Iron_hoe = "iron_hoe"
    Diamond_hoe = "diamond_hoe"
    Golden_hoe = "golden_hoe"
    Wheat_seeds = "wheat_seeds"
    Wheat = "wheat"
    Bread = "bread"
    Leather_helmet = "leather_helmet"
    Leather_chestplate = "leather_chestplate"
    Leather_leggings = "leather_leggings"
    Leather_boots = "leather_boots"
    Chainmail_helmet = "chainmail_helmet"
    Chainmail_chestplate = "chainmail_chestplate"
    Chainmail_leggings = "chainmail_leggings"
    Chainmail_boots = "chainmail_boots"
    Iron_helmet = "iron_helmet"
    Iron_chestplate = "iron_chestplate"
    Iron_leggings = "iron_leggings"
    Iron_boots = "iron_boots"
    Diamond_helmet = "diamond_helmet"
    Diamond_chestplate = "diamond_chestplate"
    Diamond_leggings = "diamond_leggings"
    Diamond_boots = "diamond_boots"
    Golden_helmet = "golden_helmet"
    Golden_chestplate = "golden_chestplate"
    Golden_leggings = "golden_leggings"
    Golden_boots = "golden_boots"
    Flint = "flint"
    Porkchop = "porkchop"
    Cooked_porkchop = "cooked_porkchop"
    Painting = "painting"
    Golden_apple = "golden_apple"
    Sign = "sign"
    Wooden_door = "wooden_door"
    Bucket = "bucket"
    Water_bucket = "water_bucket"
    Lava_bucket = "lava_bucket"
    Minecart = "minecart"
    Saddle = "saddle"
    Iron_door = "iron_door"
    Redstone = "redstone"
    Snowball = "snowball"
    Boat = "boat"
    Leather = "leather"
    Milk_bucket = "milk_bucket"
    Brick = "brick"
    Clay_ball = "clay_ball"
    Reeds = "reeds"
    Paper = "paper"
    Book = "book"
    Slime_ball = "slime_ball"
    Chest_minecart = "chest_minecart"
    Furnace_minecart = "furnace_minecart"
    Egg = "egg"
    Compass = "compass"
    Fishing_rod = "fishing_rod"
    Clock = "clock"
    Glowstone_dust = "glowstone_dust"
    Fish = "fish"
    Cooked_fish = "cooked_fish"
    Dye = "dye"
    Bone = "bone"
    Sugar = "sugar"
    Cake = "cake"
    Bed = "bed"
    Repeater = "repeater"
    Cookie = "cookie"
    Filled_map = "filled_map"
    Shears = "shears"
    Melon = "melon"
    Pumpkin_seeds = "pumpkin_seeds"
    Melon_seeds = "melon_seeds"
    Beef = "beef"
    Cooked_beef = "cooked_beef"
    Chicken = "chicken"
    Cooked_chicken = "cooked_chicken"
    Rotten_flesh = "rotten_flesh"
    Ender_pearl = "ender_pearl"
    Blaze_rod = "blaze_rod"
    Ghast_tear = "ghast_tear"
    Gold_nugget = "gold_nugget"
    Nether_wart = "nether_wart"
    Potion = "potion"
    Glass_bottle = "glass_bottle"
    Spider_eye = "spider_eye"
    Fermented_spider_eye = "fermented_spider_eye"
    Blaze_powder = "blaze_powder"
    Magma_cream = "magma_cream"
    Brewing_stand = "brewing_stand"
    Cauldron = "cauldron"
    Ender_eye = "ender_eye"
    Speckled_melon = "speckled_melon"
    Spawn_egg = "spawn_egg"
    Experience_bottle = "experience_bottle"
    Fire_charge = "fire_charge"
    Writable_book = "writable_book"
    Written_book = "written_book"
    Emerald = "emerald"
    Item_frame = "item_frame"
    Flower_pot = "flower_pot"
    Carrot = "carrot"
    Potato = "potato"
    Baked_potato = "baked_potato"
    Poisonous_potato = "poisonous_potato"
    Map = "map"
    Golden_carrot = "golden_carrot"
    Skull = "skull"
    Carrot_on_a_stick = "carrot_on_a_stick"
    Nether_star = "nether_star"
    Pumpkin_pie = "pumpkin_pie"
    Fireworks = "fireworks"
    Firework_charge = "firework_charge"
    Enchanted_book = "enchanted_book"
    Comparator = "comparator"
    Netherbrick = "netherbrick"
    Quartz = "quartz"
    Tnt_minecart = "tnt_minecart"
    Hopper_minecart = "hopper_minecart"
    Prismarine_shard = "prismarine_shard"
    Prismarine_crystals = "prismarine_crystals"
    Rabbit = "rabbit"
    Cooked_rabbit = "cooked_rabbit"
    Rabbit_stew = "rabbit_stew"
    Rabbit_foot = "rabbit_foot"
    Rabbit_hide = "rabbit_hide"
    Armor_stand = "armor_stand"
    Iron_horse_armor = "iron_horse_armor"
    Golden_horse_armor = "golden_horse_armor"
    Diamond_horse_armor = "diamond_horse_armor"
    Lead = "lead"
    Name_tag = "name_tag"
    Command_block_minecart = "command_block_minecart"
    Mutton = "mutton"
    Cooked_mutton = "cooked_mutton"
    Banner = "banner"
    Spruce_door = "spruce_door"
    Birch_door = "birch_door"
    Jungle_door = "jungle_door"
    Acacia_door = "acacia_door"
    Dark_oak_door = "dark_oak_door"
    Chorus_fruit = "chorus_fruit"
    Chorus_fruit_popped = "chorus_fruit_popped"
    Beetroot = "beetroot"
    Beetroot_seeds = "beetroot_seeds"
    Beetroot_soup = "beetroot_soup"
    Dragon_breath = "dragon_breath"
    Splash_potion = "splash_potion"
    Spectral_arrow = "spectral_arrow"
    Tipped_arrow = "tipped_arrow"
    Lingering_potion = "lingering_potion"
    Shield = "shield"
    Elytra = "elytra"
    Spruce_boat = "spruce_boat"
    Birch_boat = "birch_boat"
    Jungle_boat = "jungle_boat"
    Acacia_boat = "acacia_boat"
    Dark_oak_boat = "dark_oak_boat"
    Totem_of_undying = "totem_of_undying"
    Shulker_shell = "shulker_shell"
    Iron_nugget = "iron_nugget"
    Record_13 = "record_13"
    Record_cat = "record_cat"
    Record_blocks = "record_blocks"
    Record_chirp = "record_chirp"
    Record_far = "record_far"
    Record_mall = "record_mall"
    Record_mellohi = "record_mellohi"
    Record_stal = "record_stal"
    Record_strad = "record_strad"
    Record_ward = "record_ward"
    Record_11 = "record_11"
    Record_wait = "record_wait"

class ItemSlot:
    class HotBar(Enum):
        _0 = 0
        _1 = 1
        _2 = 2
        _3 = 3
        _4 = 4
        _5 = 5
        _6 = 6
        _7 = 7
        _8 = 8

    class Inventory(Enum):
        _9 = 9
        _10 = 10
        _11 = 11
        _12 = 12
        _13 = 13
        _14 = 14
        _15 = 15
        _16 = 16
        _17 = 17
        _18 = 18
        _19 = 19
        _20 = 20
        _21 = 21
        _22 = 22
        _23 = 23
        _24 = 24
        _25 = 25
        _26 = 26
        _27 = 27
        _28 = 28
        _29 = 29
        _30 = 30
        _31 = 31
        _32 = 32
        _33 = 33
        _34 = 34
        _35 = 35
    
    class Armor(Enum):
        Boots = 36
        Leggings = 37
        Chestplate = 38
        Helmet = 39

class Direction(Enum):
    North = 180
    East = -90
    South = 0
    West = 90

class MobType(Enum):
    ElderGuardian = "ElderGuardian"
    WitherSkeleton = "WitherSkeleton"
    Stray = "Stray"
    Husk = "Husk"
    ZombieVillager = "ZombieVillager"
    SkeletonHorse = "SkeletonHorse"
    ZombieHorse = "ZombieHorse"
    EvocationIllager = "EvocationIllager"
    VindicationIllager = "VindicationIllager"
    Vex = "Vex"
    Creeper = "Creeper"
    Skeleton = "Skeleton"
    Spider = "Spider"
    Giant = "Giant"
    Zombie = "Zombie"
    Slime = "Slime"
    Ghast = "Ghast"
    PigZombie = "PigZombie"
    Enderman = "Enderman"
    CaveSpider = "CaveSpider"
    Silverfish = "Silverfish"
    Blaze = "Blaze"
    LavaSlime = "LavaSlime"
    EnderDragon = "EnderDragon"
    WitherBoss = "WitherBoss"
    Bat = "Bat"
    Witch = "Witch"
    Endermite = "Endermite"
    Guardian = "Guardian"
    Shulker = "Shulker"
    Donkey = "Donkey"
    Mule = "Mule"
    Pig = "Pig"
    Sheep = ""
    Cow = "Cow"
    Chicken = "Chicken"
    Squid = "Squid"
    Wolf = "Wolf"
    MushroomCow = "MushroomCow"
    SnowMan = "SnowMan"
    Ozelot = "Ozelot"
    VillagerGolem = "VillagerGolem"
    Horse = "Horse"
    Rabbit = "Rabbit"
    PolarBear = "PolarBear"
    Llama = "Llama"
    Villager = "Villager"

class TimeOfDay(Enum):
    Dawn = 0
    Noon = 6000
    Sunset = 12000
    Midnight = 18000

class AgentCommands(Enum):
    MoveTo = 0
    Attack = 1
    Craft = 2
    GiveItem = 3
    UseItem = 4
