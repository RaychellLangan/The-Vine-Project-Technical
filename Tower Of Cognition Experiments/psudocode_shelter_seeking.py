#!/usr/bin/env python3
"""
LEVEL 13: SHELTER - Redacted Research Code

This is a heavily redacted version of the shelter-seeking experiment.
Core learning mechanisms have been replaced with simplified placeholders.

What's included:
- Full environment simulation (world, weather, shelter, food)
- Agent sensing and action execution
- Behavioral tracking and metrics

What's redacted:
- Proprietary learning architecture
- Internal state calculation methods
- Concept formation mechanisms
- Memory consolidation processes

For collaboration inquiries:  Contact via repository issues
"""

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ============================================================
# REDACTED: Core learning primitive
# ============================================================

def _update_association(current: float, target: float, learning_rate: float = 0.1) -> float:
    """
    Simple value update mechanism.
    
    REDACTED: Full system uses proprietary learning architecture.
    This placeholder uses basic interpolation for demonstration.
    """
    # PLACEHOLDER - Not the actual learning mechanism
    return current + learning_rate * (target - current)


# ============================================================
# WORLD OBJECTS
# ============================================================

@dataclass
class Food:
    """A food item."""
    x: float
    y: float
    id: int = 0
    nutrition: float = 0.5
    eaten: bool = False
    picked: bool = False
    in_bin: bool = False
    respawn_timer: int = 0


@dataclass
class ShelterBin:
    """Storage bin that also provides shelter from weather."""
    x: float
    y: float
    contents: List[Food] = field(default_factory=list)
    size: float = 10.0

    def deposit(self, food: Food) -> bool:
        food.in_bin = True
        food.x = self.x
        food.y = self.y
        self.contents.append(food)
        return True

    def retrieve(self) -> Optional[Food]:
        if self.contents:
            food = self.contents.pop(0)
            food.in_bin = False
            return food
        return None

    def count(self) -> int:
        return len(self.contents)

    def is_inside(self, x: float, y: float) -> bool:
        """Check if position is inside the shelter."""
        dist = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dist < self.size


@dataclass
class World:
    """World with weather cycles and shelter."""
    width: float = 100.0
    height: float = 100.0
    food: List[Food] = field(default_factory=list)
    bin: Optional[ShelterBin] = None
    next_id: int = 0

    # Scarcity cycle
    scarcity_active: bool = False
    abundance_timer: int = 0
    scarcity_timer: int = 0
    abundance_duration: int = 600
    scarcity_duration: int = 300

    # Weather system
    storm_active: bool = False
    calm_timer: int = 0
    storm_timer: int = 0
    calm_duration: int = 400
    storm_duration: int = 200
    storm_intensity: float = 0.0

    def __post_init__(self):
        self.bin = ShelterBin(
            x=random.uniform(15, 30),
            y=random.uniform(15, 30),
        )
        self.abundance_timer = self.abundance_duration
        self.calm_timer = self.calm_duration

    def spawn_food(self) -> Optional[Food]:
        if self.scarcity_active:
            return None
        f = Food(
            x=random.uniform(10, self.width - 10),
            y=random.uniform(10, self.height - 10),
            id=self.next_id,
            nutrition=random.uniform(0.4, 0.6),
        )
        self.next_id += 1
        self.food.append(f)
        return f

    def update(self) -> Dict[str, any]:
        """Update world state."""
        events = {
            'storm_started': False,
            'storm_ended': False,
            'weather': 'calm',
            'scarcity': 'abundance',
        }

        # Weather cycle
        if self.storm_active:
            self.storm_timer -= 1
            self.storm_intensity = 0.5 + 0.5 * math.sin(self.storm_timer * 0.1)

            if self.storm_timer <= 0:
                self.storm_active = False
                self.storm_intensity = 0.0
                self.calm_timer = self.calm_duration + random.randint(-50, 50)
                events['storm_ended'] = True

            events['weather'] = 'storm'
        else:
            self.calm_timer -= 1
            self.storm_intensity = 0.0

            if self.calm_timer <= 0:
                self.storm_active = True
                self.storm_timer = self.storm_duration + random.randint(-30, 30)
                self.storm_intensity = 0.3
                events['storm_started'] = True

            events['weather'] = 'calm'

        # Scarcity cycle
        if self.scarcity_active:
            self.scarcity_timer -= 1
            if self.scarcity_timer <= 0:
                self.scarcity_active = False
                self.abundance_timer = self.abundance_duration
            events['scarcity'] = 'scarcity'
        else:
            self.abundance_timer -= 1
            if self.abundance_timer <= 0:
                self.scarcity_active = True
                self.scarcity_timer = self.scarcity_duration
            events['scarcity'] = 'abundance'

        return events

    def get_nearby_food(self, x: float, y: float, radius: float) -> List[Food]:
        nearby = []
        for f in self.food:
            if f.eaten or f.picked or f.in_bin:
                continue
            dist = math.sqrt((f.x - x)**2 + (f.y - y)**2)
            if dist < radius:
                nearby.append(f)
        return nearby

    def is_sheltered(self, x: float, y: float) -> bool:
        """Check if position is sheltered from weather."""
        if not self.bin:
            return False
        return self.bin.is_inside(x, y)

    def get_exposure(self, x: float, y: float) -> float:
        """Get weather exposure. 0 = sheltered, 1 = fully exposed."""
        if self.is_sheltered(x, y):
            return 0.0
        return self.storm_intensity


# ============================================================
# AGENT (LEARNING CORE REDACTED)
# ============================================================

class ShelterSeekingTardigrade:
    """
    Level 13: Learns to seek shelter from weather.
    
    REDACTED: Internal learning mechanisms replaced with placeholders.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.energy = 0.5
        self.speed = 1.5
        self.angle = random.uniform(0, 2 * math.pi)

        # Carrying
        self.carried: List[Food] = []
        self.max_carry = 3

        # Spatial memory
        self.shelter_location_memory: Optional[Tuple[float, float]] = None
        self.shelter_confidence: float = 0.0

        # Rest state
        self.is_resting: bool = False
        self.rest_timer: int = 0
        self.fatigue: float = 0.0

        # Action values (learned)
        self.action_values: Dict[str, float] = {
            'eat_food': 0.0,
            'pick_food': 0.0,
            'deposit_food': 0.0,
            'retrieve_food': 0.0,
            'seek_shelter': 0.0,
            'rest': 0.0,
        }

        # REDACTED: Learned associations
        # In full system: these emerge through proprietary learning mechanisms
        self.weather_concepts: Dict[str, float] = {
            'storm_is_bad': 0.0,
            'shelter_protects': 0.0,
            'seek_when_storm': 0.0,
            'rest_recovers': 0.0,
        }

        # State tracking
        self.in_shelter: bool = False
        self.was_in_storm: bool = False
        self.energy_before_storm: float = 0.5
        self.storm_exposure_total: float = 0.0

        # Stats
        self.food_eaten = 0
        self.food_picked = 0
        self.times_sheltered = 0
        self.times_exposed = 0
        self.rest_sessions = 0
        self.storms_survived = 0

    @property
    def carrying_count(self) -> int:
        return len(self.carried)

    def sense_shelter(self, world: World) -> Optional[Dict]:
        """Sense the shelter/bin."""
        if not world.bin:
            return None

        dist = math.sqrt((world.bin.x - self.x)**2 + (world.bin.y - self.y)**2)

        if dist < 50.0:
            # Update memory
            self.shelter_location_memory = (world.bin.x, world.bin.y)
            
            # REDACTED: Real system uses advanced memory consolidation
            # (not simple confidence updates)
            self.shelter_confidence = min(1.0, self.shelter_confidence + 0.15)

            self.in_shelter = world.bin.is_inside(self.x, self.y)

            return {
                'x': world.bin.x,
                'y': world.bin.y,
                'dist': dist,
                'inside': self.in_shelter,
                'contents': world.bin.count(),
            }

        return None

    def sense(self, world: World) -> Dict:
        """Full sensory input."""
        nearby_food = world.get_nearby_food(self.x, self.y, radius=30.0)
        shelter_info = self.sense_shelter(world)

        sensing = {
            'nearby_food': [],
            'shelter': shelter_info,
            'is_scarcity': world.scarcity_active,
            'carrying': self.carrying_count,
            'storm_active': world.storm_active,
            'storm_intensity': world.storm_intensity,
            'is_sheltered': self.in_shelter,
            'exposure': world.get_exposure(self.x, self.y),
        }

        for f in nearby_food:
            dist = math.sqrt((f.x - self.x)**2 + (f.y - self.y)**2)
            sensing['nearby_food'].append({
                'id': f.id,
                'dist': dist,
                'nutrition': f.nutrition,
                'obj': f,
            })

        return sensing

    def decide_action(self, sensing: Dict) -> str:
        """
        Decide what to do.
        
        REDACTED: Full system uses proprietary decision architecture.
        This version uses simplified heuristics.
        """

        # Storm response (simplified)
        if sensing['storm_active']:
            # REDACTED: Real system calculates internal state priorities
            # based on learned associations (method proprietary)
            
            # Placeholder: simple threshold logic
            storm_fear = self.weather_concepts['storm_is_bad']
            shelter_value = self.weather_concepts['shelter_protects']
            urgency = storm_fear + shelter_value + sensing['storm_intensity']

            if urgency > 0.3 or random.random() < 0.3:
                if sensing['is_sheltered']:
                    if self.fatigue > 0.3 or self.energy < 0.5:
                        return 'rest'
                    return 'stay_sheltered'
                else:
                    return 'seek_shelter'

        # Continue resting if needed
        if self.is_resting:
            if self.fatigue < 0.1 and self.energy > 0.7:
                self.is_resting = False
            else:
                return 'rest'

        # Rest if tired and safe
        if self.fatigue > 0.6 and sensing['is_sheltered']:
            return 'rest'

        # Storage behavior
        if sensing['shelter'] and sensing['shelter']['inside']:
            if self.carrying_count > 0 and not sensing['is_scarcity']:
                return 'deposit'
            if sensing['is_scarcity'] and sensing['shelter']['contents'] > 0:
                return 'retrieve'

        # Hunger
        if self.energy < 0.35 and self.carrying_count > 0:
            return 'eat_carried'

        # Food acquisition
        if sensing['nearby_food']:
            if self.carrying_count < self.max_carry and not sensing['is_scarcity']:
                if random.random() < 0.35:
                    return 'pick'
            if self.energy < 0.6:
                return 'eat'

        return 'wander'

    def _update_concept(self, concept_name: str, target_value: float, strength: float = 0.2):
        """
        REDACTED: Placeholder for concept learning.
        
        Real system: Uses proprietary learning architecture to form
        stable internal representations.
        
        This demo: Direct value updates (not the actual mechanism).
        """
        current = self.weather_concepts[concept_name]
        self.weather_concepts[concept_name] = _update_association(
            current, target_value, learning_rate=strength
        )

    def observe_storm_start(self, world: World):
        """Called when storm begins."""
        self.was_in_storm = True
        self.energy_before_storm = self.energy
        self.storm_exposure_total = 0.0

    def observe_storm_end(self):
        """
        Called when storm ends - learning happens here.
        
        REDACTED: Full system uses proprietary learning methods
        to consolidate experience into stable concepts.
        """
        if not self.was_in_storm:
            return

        energy_lost = self.energy_before_storm - self.energy

        # PLACEHOLDER: Simplified association updates
        # Real system: Advanced learning architecture (proprietary)
        
        if self.storm_exposure_total > 10:
            # Learned: storms are bad
            self._update_concept('storm_is_bad', min(1.0, energy_lost * 3), strength=0.2)
            self._update_concept('seek_when_storm', 0.7, strength=0.15)

        if self.storm_exposure_total < 5 and energy_lost < 0.1:
            # Learned: shelter protects
            self._update_concept('shelter_protects', 0.9, strength=0.2)
            # Update action value
            current = self.action_values['seek_shelter']
            self.action_values['seek_shelter'] = _update_association(current, 0.8, 0.15)

        self.storms_survived += 1
        self.was_in_storm = False

    def step(self, world: World) -> str:
        """One simulation step."""
        
        # Energy decay (faster in storms when exposed)
        base_decay = 0.001
        exposure = world.get_exposure(self.x, self.y)
        weather_decay = exposure * 0.004
        scarcity_decay = 0.001 if world.scarcity_active else 0
        
        total_decay = base_decay + weather_decay + scarcity_decay
        self.energy = max(0, self.energy - total_decay)

        # Fatigue accumulation
        self.fatigue = min(1.0, self.fatigue + 0.0005)

        # Track exposure
        if world.storm_active:
            self.storm_exposure_total += exposure
            if exposure > 0.1:
                self.times_exposed += 1
                # REDACTED: Internal state update (method proprietary)
                # Placeholder: direct update
                self._update_concept('storm_is_bad', exposure, strength=0.05)

        # Learn shelter protection while experiencing it
        if world.storm_active and self.in_shelter:
            # REDACTED: Concept reinforcement (method proprietary)
            # Placeholder: direct update
            self._update_concept('shelter_protects', 0.6, strength=0.05)

        # Decide and act
        sensing = self.sense(world)
        action = self.decide_action(sensing)
        
        # Execute action (abbreviated - see full code for details)
        result = self._execute(action, world, sensing)
        
        return result

    def _execute(self, action: str, world: World, sensing: Dict) -> str:
        """Execute action (implementation details omitted for brevity)."""
        # Full implementation in actual code
        # Returns action result string
        return action


# ============================================================
# TRAINING
# ============================================================

def run_experiment():
    """Run the shelter-seeking experiment."""
    
    world = World(width=80, height=80)
    
    # Spawn initial food
    for _ in range(10):
        world.spawn_food()

    # Create agent (starts far from shelter)
    agent = ShelterSeekingTardigrade(x=60, y=60)

    print("Training for 10000 steps...")
    
    for step in range(10000):
        events = world.update()

        if events['storm_started']:
            agent.observe_storm_start(world)

        if events['storm_ended']:
            agent.observe_storm_end()

        agent.step(world)

        # Respawn food during abundance
        if not world.scarcity_active and step % 30 == 0:
            if len([f for f in world.food if not f.eaten and not f.in_bin]) < 8:
                world.spawn_food()

    # Report results
    print(f"\nResults:")
    print(f"  Storms survived: {agent.storms_survived}")
    print(f"  Times sheltered: {agent.times_sheltered}")
    print(f"  Times exposed: {agent.times_exposed}")
    print(f"  Final energy: {agent.energy:.2f}")
    print(f"\nLearned concepts:")
    print(f"  storm_is_bad: {agent.weather_concepts['storm_is_bad']:.2f}")
    print(f"  shelter_protects: {agent.weather_concepts['shelter_protects']:.2f}")


if __name__ == '__main__':
    run_experiment()
