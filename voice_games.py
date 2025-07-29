#!/usr/bin/env python3
"""
Voice Games Module for Jarvis
Interactive games that can be played using only voice commands.
"""

import random
import time
from datetime import datetime

class VoiceGames:
    def __init__(self):
        self.current_game = None
        self.game_state = {}
        self.scores = {}
        
        # Trivia questions
        self.trivia_questions = [
            {
                "question": "What is the capital of France?",
                "answer": "paris",
                "category": "Geography"
            },
            {
                "question": "What is the largest planet in our solar system?",
                "answer": "jupiter",
                "category": "Science"
            },
            {
                "question": "Who wrote Romeo and Juliet?",
                "answer": "shakespeare",
                "category": "Literature"
            },
            {
                "question": "What is the chemical symbol for gold?",
                "answer": "au",
                "category": "Science"
            },
            {
                "question": "What year did World War II end?",
                "answer": "1945",
                "category": "History"
            },
            {
                "question": "What is the main component of the sun?",
                "answer": "hydrogen",
                "category": "Science"
            },
            {
                "question": "What is the largest ocean on Earth?",
                "answer": "pacific",
                "category": "Geography"
            },
            {
                "question": "Who painted the Mona Lisa?",
                "answer": "leonardo da vinci",
                "category": "Art"
            }
        ]
        
        # Word games
        self.word_categories = {
            "animals": ["elephant", "giraffe", "penguin", "dolphin", "kangaroo"],
            "colors": ["red", "blue", "green", "yellow", "purple", "orange"],
            "fruits": ["apple", "banana", "orange", "grape", "strawberry"],
            "countries": ["france", "japan", "brazil", "australia", "canada"]
        }
        
        # Story templates
        self.story_templates = [
            {
                "title": "The Magic Forest",
                "template": "Once upon a time, there was a {character} who lived in a {location}. One day, they found a {object} that could {power}. With this power, they decided to {action}.",
                "prompts": ["character", "location", "object", "power", "action"]
            },
            {
                "title": "Space Adventure",
                "template": "In the year {year}, Captain {name} discovered a {planet} inhabited by {aliens}. The aliens had the ability to {ability}. Together, they planned to {mission}.",
                "prompts": ["year", "name", "planet", "aliens", "ability", "mission"]
            }
        ]
    
    def start_trivia(self):
        """Start a trivia game"""
        self.current_game = "trivia"
        self.game_state = {
            "score": 0,
            "questions_asked": 0,
            "total_questions": 5
        }
        return "Trivia game started! I'll ask you 5 questions. Say 'stop trivia' to end the game."
    
    def get_trivia_question(self):
        """Get a random trivia question"""
        if self.game_state["questions_asked"] >= self.game_state["total_questions"]:
            return self.end_trivia()
        
        question_data = random.choice(self.trivia_questions)
        self.game_state["current_question"] = question_data
        self.game_state["questions_asked"] += 1
        
        return f"Question {self.game_state['questions_asked']}: {question_data['question']}"
    
    def check_trivia_answer(self, user_answer):
        """Check if the trivia answer is correct"""
        if "current_question" not in self.game_state:
            return "No active question. Say 'next question' to continue."
        
        correct_answer = self.game_state["current_question"]["answer"]
        user_answer_clean = user_answer.lower().strip()
        
        if user_answer_clean == correct_answer:
            self.game_state["score"] += 1
            return f"Correct! Your score is now {self.game_state['score']}/{self.game_state['questions_asked']}"
        else:
            return f"Sorry, the correct answer was '{correct_answer}'. Your score is {self.game_state['score']}/{self.game_state['questions_asked']}"
    
    def end_trivia(self):
        """End the trivia game and show final score"""
        if self.current_game != "trivia":
            return "No trivia game in progress."
        
        final_score = self.game_state["score"]
        total_questions = self.game_state["total_questions"]
        percentage = (final_score / total_questions) * 100
        
        result = f"Trivia game ended! Final score: {final_score}/{total_questions} ({percentage:.1f}%)"
        
        if percentage >= 80:
            result += " Excellent job!"
        elif percentage >= 60:
            result += " Good work!"
        else:
            result += " Keep practicing!"
        
        self.current_game = None
        self.game_state = {}
        return result
    
    def start_word_game(self, category=None):
        """Start a word guessing game"""
        if category and category in self.word_categories:
            selected_category = category
        else:
            selected_category = random.choice(list(self.word_categories.keys()))
        
        self.current_game = "word_game"
        self.game_state = {
            "category": selected_category,
            "score": 0,
            "words_guessed": 0,
            "total_words": 3,
            "used_words": []
        }
        
        return f"Word game started! Category: {selected_category.title()}. I'll give you clues and you guess the word. Say 'stop word game' to end."
    
    def get_word_clue(self):
        """Get a clue for the word game"""
        if self.game_state["words_guessed"] >= self.game_state["total_words"]:
            return self.end_word_game()
        
        available_words = [word for word in self.word_categories[self.game_state["category"]] 
                         if word not in self.game_state["used_words"]]
        
        if not available_words:
            return self.end_word_game()
        
        word = random.choice(available_words)
        self.game_state["current_word"] = word
        self.game_state["used_words"].append(word)
        
        # Generate clue based on category
        clues = {
            "animals": f"It's an animal that {self.get_animal_clue(word)}",
            "colors": f"It's a color that {self.get_color_clue(word)}",
            "fruits": f"It's a fruit that {self.get_fruit_clue(word)}",
            "countries": f"It's a country that {self.get_country_clue(word)}"
        }
        
        category = self.game_state["category"]
        clue = clues.get(category, f"It's a {category} word.")
        
        return f"Clue: {clue}"
    
    def get_animal_clue(self, animal):
        """Generate animal-specific clues"""
        clues = {
            "elephant": "is very large and has a long trunk",
            "giraffe": "has a very long neck and spots",
            "penguin": "lives in cold places and can't fly",
            "dolphin": "lives in water and is very smart",
            "kangaroo": "hops and carries babies in a pouch"
        }
        return clues.get(animal, "is an animal")
    
    def get_color_clue(self, color):
        """Generate color-specific clues"""
        clues = {
            "red": "is the color of fire and blood",
            "blue": "is the color of the sky and ocean",
            "green": "is the color of grass and leaves",
            "yellow": "is the color of the sun and bananas",
            "purple": "is a mix of red and blue",
            "orange": "is the color of oranges and carrots"
        }
        return clues.get(color, "is a color")
    
    def get_fruit_clue(self, fruit):
        """Generate fruit-specific clues"""
        clues = {
            "apple": "keeps the doctor away",
            "banana": "is yellow and monkeys love it",
            "orange": "is round and has segments",
            "grape": "grows in bunches and makes wine",
            "strawberry": "is red and has seeds on the outside"
        }
        return clues.get(fruit, "is a fruit")
    
    def get_country_clue(self, country):
        """Generate country-specific clues"""
        clues = {
            "france": "is famous for the Eiffel Tower",
            "japan": "is known for sushi and technology",
            "brazil": "is home to the Amazon rainforest",
            "australia": "has kangaroos and the Great Barrier Reef",
            "canada": "is known for maple syrup and cold weather"
        }
        return clues.get(country, "is a country")
    
    def check_word_answer(self, user_answer):
        """Check if the word answer is correct"""
        if "current_word" not in self.game_state:
            return "No active word. Say 'next clue' to continue."
        
        correct_word = self.game_state["current_word"]
        user_answer_clean = user_answer.lower().strip()
        
        if user_answer_clean == correct_word:
            self.game_state["score"] += 1
            self.game_state["words_guessed"] += 1
            return f"Correct! The word was '{correct_word}'. Your score is now {self.game_state['score']}/{self.game_state['words_guessed']}"
        else:
            self.game_state["words_guessed"] += 1
            return f"Sorry, the word was '{correct_word}'. Your score is {self.game_state['score']}/{self.game_state['words_guessed']}"
    
    def end_word_game(self):
        """End the word game and show final score"""
        if self.current_game != "word_game":
            return "No word game in progress."
        
        final_score = self.game_state["score"]
        total_words = self.game_state["total_words"]
        percentage = (final_score / total_words) * 100
        
        result = f"Word game ended! Final score: {final_score}/{total_words} ({percentage:.1f}%)"
        
        if percentage >= 80:
            result += " Amazing vocabulary!"
        elif percentage >= 60:
            result += " Good guessing!"
        else:
            result += " Keep learning new words!"
        
        self.current_game = None
        self.game_state = {}
        return result
    
    def start_story_generator(self):
        """Start an interactive story generator"""
        self.current_game = "story"
        story_template = random.choice(self.story_templates)
        self.game_state = {
            "template": story_template,
            "answers": {},
            "current_prompt": 0
        }
        
        return f"Story generator started! I'll ask you questions to create a story called '{story_template['title']}'. Say 'stop story' to end."
    
    def get_story_prompt(self):
        """Get the next story prompt"""
        if self.current_game != "story":
            return "No story game in progress."
        
        prompts = self.game_state["template"]["prompts"]
        current_prompt = self.game_state["current_prompt"]
        
        if current_prompt >= len(prompts):
            return self.generate_story()
        
        prompt = prompts[current_prompt]
        return f"Tell me a {prompt}:"
    
    def add_story_answer(self, answer):
        """Add an answer to the story"""
        if self.current_game != "story":
            return "No story game in progress."
        
        prompts = self.game_state["template"]["prompts"]
        current_prompt = self.game_state["current_prompt"]
        
        if current_prompt >= len(prompts):
            return "Story is complete. Say 'tell story' to hear it."
        
        prompt = prompts[current_prompt]
        self.game_state["answers"][prompt] = answer
        self.game_state["current_prompt"] += 1
        
        if self.game_state["current_prompt"] >= len(prompts):
            return "Great! Now say 'tell story' to hear your story."
        else:
            next_prompt = prompts[self.game_state["current_prompt"]]
            return f"Tell me a {next_prompt}:"
    
    def generate_story(self):
        """Generate the final story"""
        if self.current_game != "story":
            return "No story game in progress."
        
        template = self.game_state["template"]["template"]
        answers = self.game_state["answers"]
        
        try:
            story = template.format(**answers)
            self.current_game = None
            self.game_state = {}
            return f"Here's your story: {story}"
        except KeyError:
            return "Story incomplete. Please provide all answers first."
    
    def stop_current_game(self):
        """Stop the current game"""
        if self.current_game == "trivia":
            return self.end_trivia()
        elif self.current_game == "word_game":
            return self.end_word_game()
        elif self.current_game == "story":
            self.current_game = None
            self.game_state = {}
            return "Story generator stopped."
        else:
            return "No game in progress."
    
    def get_game_status(self):
        """Get current game status"""
        if not self.current_game:
            return "No game in progress."
        
        if self.current_game == "trivia":
            return f"Trivia game: {self.game_state['score']}/{self.game_state['questions_asked']} correct"
        elif self.current_game == "word_game":
            return f"Word game ({self.game_state['category']}): {self.game_state['score']}/{self.game_state['words_guessed']} correct"
        elif self.current_game == "story":
            return f"Story generator: {self.game_state['current_prompt']}/{len(self.game_state['template']['prompts'])} prompts answered"
        
        return "Unknown game in progress."

# Global instance
voice_games = VoiceGames()

def get_voice_games():
    """Get the global voice games instance"""
    return voice_games 