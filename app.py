from fasthtml.common import *
from monsterui.all import *
from datetime import datetime
from typing import List, Optional
import json

# Initialize
hdrs = Theme.blue.headers()
app, rt = fast_app(hdrs=hdrs)

# Data structures
class Rep:
    def __init__(self, count: int):
        self.count = count

class Set:
    def __init__(self, move: str, weight: int):
        self.move = move
        self.weight = weight
        self.reps: List[Rep] = []
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.notes = ""
    
    def add_rep(self, count: int):
        self.reps.append(Rep(count))
    
    def end_set(self):
        self.end_time = datetime.now()

class Workout:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.sets: List[Set] = []
        self.notes = ""
    
    def add_set(self, set_data: Set):
        self.sets.append(set_data)
    
    def end_workout(self):
        self.end_time = datetime.now()

# In-memory storage (replace with database later)
current_workout: Optional[Workout] = None
current_set: Optional[Set] = None

# Common moves list
MOVES = [
    "Bench Press", "Squat", "Deadlift", "Overhead Press",
    "KB Swing", "KB Snatch", "KB Clean", "Dips", "Pull-ups",
    "Rows", "Curls", "Tricep Extension"
]

# UI Components
def control_buttons():
    """Section A: Control buttons"""
    return Card(
        H3("Controls", css_class="text-lg font-semibold mb-3"),
        Grid(
            Button(
                "🏁 Start Workout", 
                id="start-workout",
                hx_post="/start-workout",
                hx_target="#workout-status",
                css_class="w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded"
            ),
            Button(
                "⏹️ End Workout", 
                id="end-workout",
                hx_post="/end-workout",
                hx_target="#workout-status",
                disabled=True,
                css_class="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded disabled:opacity-50"
            ),
            cols=1,
            css_class="gap-2"
        ),
        css_class="h-full"
    )

def move_selector():
    """Section B: Move selection"""
    return Card(
        H3("Select Move", css_class="text-lg font-semibold mb-3"),
        Select(
            Option("Choose a move", value="", disabled=True, selected=True),
            *[Option(move, value=move) for move in MOVES],
            id="move-select",
            hx_post="/select-move",
            hx_target="#weight-input",
            disabled=True,
            css_class="w-full p-2 border rounded"
        ),
        css_class="h-full"
    )

def numeric_input():
    """Section C: Numeric input grid"""
    return Card(
        H3("Weight/Reps", id="input-label", css_class="text-lg font-semibold mb-3"),
        Div(
            Input(
                type="number",
                id="numeric-input",
                placeholder="Enter weight",
                disabled=True,
                css_class="w-full p-2 border rounded mb-2"
            ),
            Button(
                "Submit",
                id="submit-numeric",
                hx_post="/submit-numeric",
                hx_target="#workout-log",
                disabled=True,
                css_class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
            ),
            id="weight-input"
        ),
        css_class="h-full"
    )

def workout_log():
    """Section D: Workout log"""
    return Card(
        H3("📋 Workout Log", css_class="text-lg font-semibold mb-3"),
        Div(
            P("Ready to start your workout! 💪", css_class="text-gray-600"),
            id="workout-log",
            css_class="h-64 overflow-y-auto p-3 bg-gray-50 rounded"
        ),
        css_class="col-span-3"
    )

# Main UI
@rt("/")
def workout_ui():
    return Div(
        # Header
        H1("💪 Workout Tracker", css_class="text-3xl font-bold text-center mb-6 text-blue-600"),
        
        # Status bar
        Div(id="workout-status", css_class="mb-4"),
        
        # Main grid layout
        Grid(
            # Upper sections (A, B, C)
            control_buttons(),
            move_selector(),
            numeric_input(),
            
            # Lower section (D) - spans all columns
            workout_log(),
            
            cols=3,
            css_class="gap-4 max-w-6xl mx-auto"
        ),
        
        css_class="p-6 bg-gray-50 min-h-screen"
    )

# API Routes
@rt("/start-workout", methods=["POST"])
def start_workout():
    global current_workout
    current_workout = Workout()
    
    return Div(
        P(f"Workout started at {current_workout.start_time.strftime('%I:%M %p')}", 
          css_class="text-green-600 font-semibold"),
        # Enable move selector
        Script("document.getElementById('move-select').disabled = false;"),
        Script("document.getElementById('end-workout').disabled = false;"),
        Script("document.getElementById('start-workout').disabled = true;")
    )

@rt("/select-move", methods=["POST"])
def select_move(move_select: str):
    global current_set
    if move_select and current_workout:
        # Update UI to enter weight
        return Div(
            Input(
                type="number",
                id="numeric-input",
                placeholder=f"Enter weight for {move_select}",
                hx_post="/submit-weight",
                hx_vals=json.dumps({"move": move_select}),
                css_class="w-full p-2 border rounded mb-2"
            ),
            Button(
                "Set Weight",
                hx_post="/submit-weight",
                hx_vals=json.dumps({"move": move_select}),
                css_class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
            )
        )
    return ""

@rt("/submit-weight", methods=["POST"])
def submit_weight(move: str, numeric_input: str):
    global current_set
    if numeric_input and move:
        weight = int(numeric_input)
        current_set = Set(move, weight)
        
        # Log entry
        log_entry = Div(
            P(f"{move} {weight} lbs - Set started at {current_set.start_time.strftime('%I:%M %p')}", 
              css_class="font-semibold"),
            Div(id=f"set-{id(current_set)}-reps", css_class="ml-4"),
            css_class="mb-2"
        )
        
        # Update UI for rep entry
        Script("""
            document.getElementById('input-label').textContent = 'Add Reps';
            document.getElementById('numeric-input').placeholder = 'Enter rep count';
            document.getElementById('numeric-input').value = '';
            document.getElementById('submit-numeric').disabled = false;
            document.getElementById('submit-numeric').setAttribute('hx-post', '/add-rep');
        """)
        
        return log_entry
    return ""

@rt("/add-rep", methods=["POST"])
def add_rep(numeric_input: str):
    global current_set
    if numeric_input and current_set:
        rep_count = int(numeric_input)
        current_set.add_rep(rep_count)
        
        # Update rep display
        reps_display = ", ".join(str(r.count) for r in current_set.reps)
        
        return Div(
            P(f"Reps: {reps_display}", css_class="text-sm"),
            id=f"set-{id(current_set)}-reps"
        )
    return ""

@rt("/end-workout", methods=["POST"])
def end_workout():
    global current_workout, current_set
    if current_workout:
        current_workout.end_workout()
        duration = (current_workout.end_time - current_workout.start_time).seconds // 60
        
        # Reset state
        current_workout = None
        current_set = None
        
        return Div(
            P(f"Workout completed! Duration: {duration} minutes", 
              css_class="text-green-600 font-semibold"),
            Script("""
                document.getElementById('start-workout').disabled = false;
                document.getElementById('end-workout').disabled = true;
                document.getElementById('move-select').disabled = true;
                document.getElementById('numeric-input').disabled = true;
                document.getElementById('submit-numeric').disabled = true;
            """)
        )
    return ""

serve()