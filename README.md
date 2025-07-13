# Track Workout v3

A workout tracking application with dual purposes:

1. **Practical Tool**: A gym companion for tracking workouts in real-time
2. **Learning Project**: An exploration of the AnswerDotAI ecosystem and development practices

# Track Workout 
## changes
1 This doc contains two sections: this section called "changes"
2 A modified version of the Track Workout v1 which follows this section with the title "Pproject Goals"

Read this section, but do not implement the suggestons as they will intersect with the new presentation below.

[ ] the message "Workout started at A TIME which appears near the top of the page should be dropped. Instead that information should go to the log.
[ ] Moves section B, the list of moves, shuold appear as a pallet, not as a drop down.
[ ] Section C: the  text box for input shoud stay, but input should be therough a keypad as in the original app. Typing numbers, or typing at all is too problamatic on a mobile devicd.

Do no fix these issues, but keep them in mind when implementing the revised use cases.



## Project Goals

- Create a practical, user-friendly workout tracking tool for gym use. A user will often be out of breath, sweating, and distracted.
  - Accordingly, there should be no direct user input of data. All user input is through large, well separated buttons.
- Implement modern development practices used by AnswerDotAI
- Explore and utilize the FastCore, FastHtml, and MonsterUI ecosystem
- Maintain clean, functional code following AnswerDotAI's architectural patterns. Where possible make good use of llms.txt whhich can be found on https://monsterui.answer-getting started. 

## UI Layout 
The top of the page contains text reading "Select move tl start workout". We refer to this as component A
Two Cards are orgainized horiztonally at the top of the page.
On the left, which we refer to as component B, we have a pallet of buttons, each labeled with a move.'
On the right, which we refer to as component C, we have a card containing a formated text above numeric kepad, which includes a Del key. Below the keypad is a text area in which the numbers are entered one, by one. Close to it is a button: "Enter". A line separtethe keypad and numerica entry from two buttons: "Change Move" and "End Workout"

## Use Cases
1. User reads message at top of page and selects a move.
    1. system responds by
       1. loging event to log with time 
       2. changing the messasge at top of page from "select move" to "workout in progress"
       3. The only enabled controls are in the move list. Component C is disabled until a move is selected.
 2. User selects a move
    1. System responds by 
       1. Changing the text above the keypad to "Enter weight for move $move"
       2. highlighting, perhaps with a checkmark, the selected move.
 3. User uses key pad to enter a weight and clics "enter" when satisfied.
    1. system responds by
       1. loging move and weight to log
       2. Changing the text above the keypad to "Enter one or more reps"
 4. User uses key pad to enter a list of one or more reps.
    1. System responds by 
       1. updating the log with each new rep
       2. clearing the input box
       3. after the first rep is enabled, the pallett of moves becomes active and the usercan switch to a new move or continue to add reps.
          1. If/when the user selects a new move, 
             1. The log entry for the last set, reflects the total time for the set
             2. The log reflects that a new set is started with its start time.
 5. The cycle, select move, enter weight, enter one or more reps continues until the user clicks 'End Workout.

## Data Model

### Core Entities
As the system progreses, entities may acquire more attributes and more behavior, but they are simple now

1. **Workout**
   - Start time
   - End time
   - Notes
   - List of sets


2. **Set**
   - name of move
    - weigh: int
   - List of Reps (integers) for each Move 
   - Start time
   - End time
   - Notes (e.g., "felt heavy", "form was off")

### Relationships

- A Workout contains one or more setds
- A Set contains 
  - a move, 
  - a weight
  - a list of rep
- 
### high level flow 
The user first selects a move, starts a new set with a given move and weight. adds a list of reps (integers) to each set.

### Example Workout Data

```
Workout start time: 1:00 PM

Sets:
    Bench Press 90 lbs
        Set start time: 1:00 PM
        Reps: 20, 20, 25, 3
        Set end time: 1:04 PM
        Time for set: 4:00 minutes.
    
    Bench Press 130 lbs
        Set start time: 1:10 PM
        Reps: 6, 6, 4, 1
        Set end time: 1:12 PM
        Time for set 2:00 minutes
    
    KB Swing 30 lbs
        Set start time: 1:20 PM
        Reps: 10, 10, 15, 12, 10, 8, 8, 8
        Set end time: 1:32 PM
        Time for set 12:00 minutes
```

workouts, Moves, Sets all get their own timestamps. 


## Expected setup which may be modified

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Component Development
Since we want to use components from MonstrUI, we will begin by searching the MonsterUI docs looking for canidates. 
In all likelyhood, the app will be constructed using MonserUI's Cards as the basic builing blocks.


## Test and evaluate Monster components
we will test and evaluate Monster components before we try to integrate theem into our app.
We will start by simply implementing MonsterUI's super simple getting started app. if that runs, we know our tools are in place. Here is the link for the getting started app. 
MonsterUI maintains llms.txt at https://www.answer.ai/posts/2025-01-15-monsterui.html#getting-startedhtml

## Architecture

Following AnswerDotAI practices:
- Pure functions where possible
- Clear separation of concerns
- Modern Python patterns
- Type hints and documentation

## License

MIT 