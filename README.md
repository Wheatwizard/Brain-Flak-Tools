# Brain-Flak-Tools
The following are a few tools I have writen to help me to write Brain-Flak code.  You can see the original project [here](github.com/DJMcMayhem/Brain-Flak/)

## Compress

Compress removes all comments whitespace and stray characters that may have been placed while you were writing the code.

## Unpack

Unpack adds whitespace to Brain-Flak code to make it more readable.  Unpack splits different units onto different lines and indents inside of the `{ }` and `< >` monads.

## Optimize

Optimize is the most complicated of the three tools.  It takes in some Brain-Flak code and attempts to simplify it to the shortest possible equivalent code using rules it knows.  
Optimize is fairly modular.
