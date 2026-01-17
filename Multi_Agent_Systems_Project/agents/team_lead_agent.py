from utils import get_llm_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field 
import json

# ANSI color codes for logging hallucinations and errors
RED = "\033[91m"
RESET = "\033[0m"

# class that defines structured ouput format for
# Team Lead's decision
class TeamLeadDecision(BaseModel):
    target_position: int = Field(description="The integer index(0-3) of the enemy to attack.")
    guessed_identity: str = Field(description="The guessed name of the hero at that position.")
    reasoning: str = Field(description="Brief strate-gy explaining why this target/guess was chosen.")
    
# set up parser
parser = JsonOutputParser(pydantic_object=TeamLeadDecision)    

class TeamLeadAgent:
    def __init__(self, team_name, model_name):
        # initializing LLM
        self.llm = self.llm = get_llm_agent(model_name, temperature=0.2)
        self.team_name = team_name
        self.known_enemies = {} # tracks the revealed or non-revealed enemies

        # prompt for team lead agent
        self.system_prompt = """
        You are the Team Lead Agent for a two-team battle game.
        
        GAME CONTEXT:
        - There are 4 positions on the enemy team: [0, 1, 2, 3].
        - You must choose a position to attack.
        - You must also GUESS the identity of the hero at that position (e.g., Argonian, Nord, Khajit, Nord, etc.).
        - If you guess correctly, you deal massive damage.
        
        CURRENT KNOWLEDGE (Enemies Revealed So Far):
        {known_enemies}
        
        YOUR MANAGER'S ORDER:
        Selected Hero: {acting_hero_name}
        Skill to Use: {acting_hero_skill}
        
        INSTRUCTIONS: 
        1. Choose a target position (0-3).
            - CRITICAL: Do NOT target a position if 'status' is 'dead'.
            - If you already  know an enemy is at position 2 (as an example), targeting them is a safe hit.
            - If you don't know, pick a position and try to guess their identity.
        2. Do NOT guess a hero name that is already revealed at another position.
        3. Output MUST be valid JSON
        
        {format_instructions}
        """

        self.team_lead_prompt = PromptTemplate(
            template=self.system_prompt,
            input_variables=["known_enemies", "acting_hero_name", "acting_hero_skill"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        # constructing the chain
        self.chain = self.team_lead_prompt | self.llm | parser
    
    def get_turn_decision(self, manager_response):
        """
        Executes the decision making for the turn.
        """
        # check for defeat signal from Team Manager
        if manager_response.get("status") == "DEFEAT":
            return {"action": "SURRENDER"}
        
        
        if manager_response.get("status") == "ERROR":
            print(f"{RED}[{self.team_name}] Manager reported ERROR.{RESET}")
            return None
        
        acting_hero = manager_response.get("hero_name")
        skill = manager_response.get("selected_skill")
        
        # fetching attack power of selected hero
        current_ap = manager_response.get("current_ap")
        
        if current_ap is None:
            print(f"{RED}[{self.team_name}] Manager was not able correctly assign attack power.{RESET}")
            return None
        
        if acting_hero is None:
            print(f"{RED}[{self.team_name}]  Manager failed to provide Hero Name.{RESET}")  
            return None
        
        if skill is None:
            print(f"{RED}[{self.team_name}]  Manager failed to provide Skill.{RESET}")  
            return None
        
        # formatting knowledge for the prompt
        known_enemies = json.dumps(self.known_enemies, indent=2) if self.known_enemies else "No enemies revealed yet."

        # executing the chain
        try:
            decision = self.chain.invoke({
                "known_enemies": known_enemies,
                "acting_hero_name": acting_hero,
                "acting_hero_skill": skill,
            })
            
            return {
                "attacker_team": self.team_name,
                "acting_hero": acting_hero,
                "skill": skill,
                "attacker_ap": current_ap,
                "target_position": decision["target_position"],
                "guessed_identity": decision["guessed_identity"]
            }
        
        except Exception as e:
            print(f"{RED}Error in Team Lead decision: {e}{RESET}")
            return None

    def update_intel(self, position, feedback):
        """
        Updates knowledge based on the attack result (Health , Status, Identity).
        """
        if position not in self.known_enemies:
            self.known_enemies[position] = {"name": "unknown", "health": "unknown", "status": "unknown"}

        if feedback.get("guess_correct") and feedback.get("actual_identity"):
            self.known_enemies[position]["name"] = feedback["actual_identity"]
            
        if "target_health" in feedback:
            self.known_enemies[position]["health"] = feedback["target_health"]
        
        if "target_status" in feedback:
            self.known_enemies[position]["status"] = feedback["target_status"]
            
        print(f"[{self.team_name}] Intel Update Pos {position}: {self.known_enemies[position]}")            

    def receive_hostile_attack(self, attack_payload, my_manager):
        """
        Passes attack info to Manager to update stats.
        Returns feeback to attacker.
        """
        feedback = my_manager.process_incoming_attack(attack_payload)

        if feedback is None:
            print(f"{RED}[{self.team_name}] Passive Manager failed to process attack. Returning empty feedback.{RESET}")

        return feedback