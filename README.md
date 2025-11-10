# Team10
GAME DESIGN OVERVIEW
====================

Core Concept:
A roguelike adventure inspired by HADES, featuring randomized maps, enemies, and weapon drops. 
Players progress through multiple levels of increasing difficulty, with a possible boss encounter at the end.


PROJECT PRIORITIES (in decreasing order of importance)
-------------------------------------------------------

1) MAP DESIGN (Highest Priority)
   - Create 3–4 unique map layouts.
   - Maps should be selected randomly each floor.
   - Reference: A demonstration is included in the ZIP file.
   - Map designers should begin work on layout and visuals.

-------------------------------------------------------

2) PLAYER HEALTH AND DAMAGE SYSTEM
   - Implement a visible health bar for the player.
   - Optionally display additional player stats (e.g., attack, defense, speed).
   - Ensure smooth integration with enemy attacks and damage logic.

-------------------------------------------------------

3) ENEMY DESIGN AND SPAWN SYSTEM
   - Goes hand in hand with map design.
   - Define enemy spawn points, quantity, and types (all randomized).
   - Each enemy should have its own health and damage values.
   - Use state machines for enemy behavior.

-------------------------------------------------------

4) WEAPON DROP SYSTEM
   - One weapon drop per level (randomized).
   - Use free 16x16 pixel sprites found online or in the ZIP file as weapon art.
   - Each weapon affects stats such as damage, attack speed, and range.

-------------------------------------------------------

5) BOSS ROOM (If Time Permits)
   - A single boss encounter as part of the enemy design.
   - Can be implemented after core gameplay systems are complete.

-------------------------------------------------------

SUMMARY:
The project is a roguelike game similar in mechanics to HADES, focusing on
procedural generation, and player progression through random maps, enemies, and weapon upgrades.