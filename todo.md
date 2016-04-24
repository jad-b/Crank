* [ ] Implement new Workout format
    * [ ] Add 1:1, M:1, 1:M shorthand notations
        * [ ] Parse from strings
        * [ ] Print sets in format
    * [ ] Use `crank.core` classes in `crank.program.*` packages
    * [ ] Switch programs to new .wkt format
        * [ ] `fto`
        * [ ] `ratchet`
* [ ] Create workout templates
    * [ ] Use a flag?
    * [ ]
* [ ] Share them via a website
    * [ ] Download saved workouts
    * [ ] Create workouts
    * [ ] Save workout records
* [x] CI
    * [x] Remove TravisCI job
    * [x] Create Dockerfile
    * [ ] Fix Wercker job
* [x] Parse workouts from .wkt format
    * [x] Workouts
        * [x] Stream lines from a file
        * [x] Save & load JSON
            * [x] Custom JSON encoding
        * [x] Sort Workouts by timestamp
            * [x] Serialize Workout timestamp to string
            * [x] Process timestamps in Workouts.upgrade()
    * [x] Parse Exercises
        * [x] Parse string & list of strings into Workout object
        * [x] Parse exercises from string or list of strings
        * [x] Output as JSON
        * [x] Store currently unparseable workouts
    * [x] Parse Sets
        * [x] Parse Sets from string
            * [x] Consolidate successfully parsed formats to a table-driven test
            * [x] Create test cases for string formats
        * [x] Output as JSON
